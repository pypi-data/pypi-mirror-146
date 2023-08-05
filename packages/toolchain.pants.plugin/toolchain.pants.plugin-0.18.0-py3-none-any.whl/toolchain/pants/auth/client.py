# Copyright © 2020 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

from __future__ import annotations

import datetime
import json
import logging
import re
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Mapping

import requests

from toolchain.base.datetime_tools import utcnow
from toolchain.pants.auth.token import AuthToken
from toolchain.pants.common.network import get_common_request_headers
from toolchain.util.constants import REQUEST_ID_HEADER

_logger = logging.getLogger(__name__)

ACQUIRE_TOKEN_GOAL_NAME = "auth-acquire"  # nosec


@unique
class AuthState(Enum):
    UNKNOWN = "unknown"
    OK = "ok"  # We are able to auth
    UNAVAILABLE = "unavailable"  # local state is preventing auth (no or expired token file/env variable)
    FAILED = "failed"  # auth failed on the server side, don't retry (HTTP 400/403).
    TRANSIENT_FAILURE = "transient_failure"  # Server encountered a transient error (HTTP 503), it is ok to retry.

    @property
    def is_ok(self) -> bool:
        return self == self.OK

    @property
    def is_final(self) -> bool:
        return self in {self.OK, self.FAILED, self.UNAVAILABLE}

    @property
    def no_auth_possible(self) -> bool:
        return self.is_final and not self.is_ok


class AuthError(Exception):
    def __init__(
        self,
        message: str,
        context: str,
        request_id: str | None = None,
        should_retry: bool = False,
        server_failure=False,
    ) -> None:
        if request_id:
            message = f"[{context}] {message} request_id={request_id}"
        super().__init__(message)
        self._should_retry = should_retry
        self._server_failure = server_failure

    def get_state(self) -> AuthState:
        if self._should_retry:
            return AuthState.TRANSIENT_FAILURE
        if self._server_failure:
            return AuthState.FAILED
        return AuthState.UNAVAILABLE


@dataclass
class AuthClient:
    _DEFAULT_FILE = ".pants.d/toolchain_auth/auth_token.json"
    context: str
    pants_bin_name: str
    base_url: str
    auth_file: str
    env_var: str | None
    repo_slug: str | None
    ci_env_variables: tuple[str, ...]
    restricted_token_matches: dict[str, str]

    @classmethod
    def create(
        cls,
        *,
        pants_bin_name: str,
        base_url: str,
        auth_file: str | None,
        env_var: str | None = None,
        repo_slug: str | None = None,
        ci_env_vars: tuple[str, ...] = tuple(),
        restricted_token_matches: dict[str, str] | None = None,
        context: str = "N/A",
    ):
        return cls(
            context=context,
            pants_bin_name=pants_bin_name,
            base_url=base_url,
            auth_file=auth_file or cls._DEFAULT_FILE,
            env_var=env_var,
            ci_env_variables=ci_env_vars,
            repo_slug=repo_slug,
            restricted_token_matches=restricted_token_matches or {},
        )

    @property
    def auth_file_path(self) -> Path:
        return Path(self.auth_file)

    def _check_refresh_token(self, refresh_token: AuthToken | None) -> None:
        if not refresh_token:
            return
        call_to_action = f"Run `{self.pants_bin_name} {ACQUIRE_TOKEN_GOAL_NAME}` to acquire a new token."
        if refresh_token.has_expired():
            raise AuthError(f"Access token has expired - {call_to_action}", context=self.context)
        time_until_expiration = refresh_token.expires_at - utcnow()
        if time_until_expiration < datetime.timedelta(days=10):
            _logger.warning(f"Access token will expire in {time_until_expiration.days} days. - {call_to_action}")

    def acquire_access_token(self, complete_env: Mapping[str, str]) -> AuthToken:
        refresh_token = self._load_refresh_token(complete_env)
        self._check_refresh_token(refresh_token)
        if not refresh_token:
            return self._acquire_restricted_access_token(complete_env)
        headers = get_common_request_headers()
        _logger.debug(f"[{self.context}] Acquire access token")
        headers.update(refresh_token.get_headers())
        response = self._post(path="token/refresh/", headers=headers, timeout=4)
        self._process_response(response)
        return AuthToken.from_json_dict(response.json())

    def _acquire_restricted_access_token(self, complete_env: Mapping[str, str]) -> AuthToken:
        if self._should_disable(complete_env):
            raise AuthError("Restricted token expression didn't match, disabling Toolchain auth.", context=self.context)
        env_vars = {key: complete_env[key] for key in self.ci_env_variables if key in complete_env}
        if not env_vars:
            raise AuthError(
                "Can't acquire restricted access token without environment variables.", context=self.context
            )
        headers = get_common_request_headers()
        json_data = {"repo_slug": self.repo_slug, "env": env_vars}
        _logger.info(f"[{self.context}] Acquire restricted access token: {json_data}")
        response = self._post(path="token/restricted/", headers=headers, timeout=8, json_data=json_data)
        self._process_response(response)
        token = AuthToken.from_json_dict(response.json())
        _logger.info(f"[{self.context}] restricted access token acquired. expires at: {token.expires_at.isoformat()}")
        return token

    def _post(self, path: str, headers: dict[str, str], timeout: int, json_data: dict | None = None):
        url = f"{self.base_url}/{path}"
        with requests.Session() as session:
            session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
            try:
                return session.post(url, headers=headers, timeout=timeout, json=json_data)
            except requests.RequestException as error:
                raise AuthError(str(error), should_retry=True, context=self.context)

    def _process_response(self, response) -> None:
        if response.ok:
            return
        request_id = response.headers.get(REQUEST_ID_HEADER)
        if response.status_code == 503:
            raise AuthError(
                "Auth failed, transient server error",
                context=self.context,
                request_id=request_id,
                should_retry=True,
                server_failure=True,
            )
        is_json = response.headers.get("Content-Type") == "application/json"
        if not is_json:
            raise AuthError(
                "Auth failed, unknown error",
                context=self.context,
                request_id=request_id,
                should_retry=False,
                server_failure=True,
            )
        resp_json = response.json()
        if response.status_code == 403 and resp_json.get("rejected") is True:
            raise AuthError("Auth rejected by server", context=self.context, request_id=request_id, server_failure=True)
        # TODO build a better string/error message
        errors = resp_json.get("errors") or "N/A"
        raise AuthError(f"API Errors: {errors}", context=self.context, request_id=request_id, server_failure=True)

    def _should_disable(self, complete_env: Mapping[str, str]) -> bool:
        for env_var, expression in self.restricted_token_matches.items():
            if env_var not in complete_env:
                _logger.debug(f"[{self.context}] {env_var} not in env: {complete_env.keys()}")
                return True
            match = re.match(expression, complete_env[env_var]) is not None
            _logger.debug(
                f"[{self.context}] expression match={match} for {env_var}: expected={expression}  got={complete_env[env_var]}"
            )
            return not match
        return False

    def _load_refresh_token(self, complete_env: Mapping[str, str]) -> AuthToken | None:
        if self.env_var:
            token = _load_from_env(self.context, complete_env, self.env_var)
            if token:
                return token
            if not self.repo_slug or not self.ci_env_variables:
                raise AuthError(
                    f"Access token not set in environment variable: {self.env_var}. customer_slug & ci_env_vars must be defined in order to acquire restricted access token.",
                    context=self.context,
                )
            return token

        auth_file_path = self.auth_file_path
        if auth_file_path.exists():
            return _load_from_file(self.context, self.pants_bin_name, auth_file_path)
        raise AuthError(
            f"Failed to load auth token (no default file or environment variable). Run `{self.pants_bin_name} {ACQUIRE_TOKEN_GOAL_NAME}` to set up authentication.",
            context=self.context,
        )


def _load_from_env(context: str, complete_env: Mapping[str, str], env_var_name: str) -> AuthToken | None:
    token_str = complete_env.get(env_var_name)
    if not token_str:
        _logger.warning(
            f"[{context}] Failed to load Toolchain token from env var '{env_var_name}'. Please make sure the env var is set in your environment."
        )
        return None
    token = AuthToken.from_access_token_string(token_str)
    _logger.info(
        f"[{context}] Successfully loaded Toolchain token from env var '{env_var_name}', expiration: {token.expires_at.isoformat()}."
    )
    return token


def _load_from_file(context: str, pants_bin_name: str, auth_file_path: Path) -> AuthToken:
    try:
        token_json = json.loads(auth_file_path.read_text())
    except (FileNotFoundError, ValueError) as err:
        raise AuthError(
            f"Failed to load auth token: {err!r}. Run `{pants_bin_name} {ACQUIRE_TOKEN_GOAL_NAME}` to set up authentication.",
            context=context,
        )
    # TODO: Handle TypeError (due to malformed json)
    return AuthToken.from_json_dict(token_json)
