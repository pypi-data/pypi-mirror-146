
# DO NOT EDIT THIS FILE -- AUTOGENERATED BY PANTS
# Target: src/python/toolchain:toolchain-pants-plugin

from setuptools import setup

setup(**{
    'author': 'Toolchain Inc',
    'author_email': 'info@toolchain.com',
    'classifiers': [
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    'description': 'Toolchain Pants plugin.',
    'entry_points': {
        'pantsbuild.plugin': [
            'rules = toolchain.pants.register:rules',
        ],
    },
    'install_requires': (
        'chardet==4.0.0',
        'requests>=2.26.0',
    ),
    'license': 'Proprietary',
    'long_description': """# Toolchain Pants plugin

A Pants build system plugin providing support for the Toolchain platform.

Speed up your builds dramatically through shared execution and caching.
View and search your team's entire build history. Use data to find
bottlenecks and optimize your development cycle.
""",
    'long_description_content_type': 'text/markdown',
    'name': 'toolchain.pants.plugin',
    'namespace_packages': (
    ),
    'package_data': {
        'toolchain.pants.auth': (
            'error.html',
            'favicon.png',
            'success.html',
        ),
    },
    'packages': (
        'toolchain',
        'toolchain.base',
        'toolchain.pants',
        'toolchain.pants.auth',
        'toolchain.pants.buildsense',
        'toolchain.pants.common',
        'toolchain.util',
    ),
    'project_urls': {
        'Changelog': 'https://docs.toolchain.com/docs/toolchain-pants-plugin-changelog',
        'Twitter': 'https://twitter.com/toolchainlabs',
    },
    'url': 'https://toolchain.com',
    'version': '0.18.0',
})
