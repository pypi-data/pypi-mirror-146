# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['okp4_grpc_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'okp4-grpc-client',
    'version': '1.0.0',
    'description': 'Python gRPC client for ØKP4 and by extension, CØSMOS based blockchains.',
    'long_description': '# ØKP4 CØSMOS proto\n\n> Python gRPC client for ØKP4 and by extension, CØSMOS based blockchains.\n\n[![build](https://github.com/okp4/okp4-cosmos-proto/actions/workflows/build.yml/badge.svg)](https://github.com/okp4/okp4-cosmos-proto/actions/workflows/build.yml)\n[![conventional commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n\n## Purpose\n\nProvides Python [gRPC clients](https://grpc.io/docs/languages/python/quickstart/) for ØKP4 and by extension, CØSMOS based blockchains generated from their Protobuf definitions.\n\n## Quick Start\n\n```sh\npip install okp4_grpc_client\n```\n',
    'author': 'OKP4',
    'author_email': 'opensource@okp4.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/okp4/okp4-cosmos-proto',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
