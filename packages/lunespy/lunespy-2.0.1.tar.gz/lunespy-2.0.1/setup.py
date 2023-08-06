# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lunespy',
 'lunespy.client.transactions',
 'lunespy.client.transactions.alias',
 'lunespy.client.transactions.burn',
 'lunespy.client.transactions.cancel_lease',
 'lunespy.client.transactions.issue',
 'lunespy.client.transactions.lease',
 'lunespy.client.transactions.mass',
 'lunespy.client.transactions.reissue',
 'lunespy.crypto',
 'lunespy.server.address',
 'lunespy.server.blocks',
 'lunespy.server.nodes',
 'lunespy.server.transactions',
 'lunespy.tx.transfer',
 'lunespy.utils',
 'lunespy.wallet']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.0,<3.0.0',
 'httpx>=0.22.0,<0.23.0',
 'pydantic>=1.9.0,<2.0.0',
 'pysha3>=1.0.2,<2.0.0',
 'python-axolotl-curve25519>=0.4.1.post2,<0.5.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'lunespy',
    'version': '2.0.1',
    'description': 'Library for communication with nodes in mainnet or testnet of the lunes-blockchain network Allows the automation of sending assets, issue end reissue tokens, leasing, registry, and create new wallet.',
    'long_description': '# LunesPy\n\n📦 Library for communication with nodes in mainnet or testnet of the lunes-blockchain network Allows the automation of sending assets, issue end reissue tokens, leasing, registry, and create new wallet.\n\n[![Test](https://github.com/lunes-platform/lunespy/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/lunes-platform/lunespy/actions/workflows/test.yml)\n![PyPI](https://img.shields.io/pypi/v/lunespy)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lunespy)\n\n![PyPI - Downloads](https://img.shields.io/pypi/dm/lunespy)\n![GitHub last commit](https://img.shields.io/github/last-commit/lunes-platform/lunespy)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/m/lunes-platform/lunespy)\n\n![PyPI - License](https://img.shields.io/pypi/l/lunespy)\n![Discord](https://img.shields.io/discord/958424925453058158)\n## Documentation\n\nThe `lunespy` documentations is hosted at [Telescope](https://lunes-platform.github.io/telescope/)\n\n## Changelog\n\nThe changelog process for this project is described [here](CHANGELOG.md).\n\n## Contributing\n\n`lunespy` is still under development. Contributions are always welcome! Please follow the [Developers Guide](CONTRIBUTING.md) if you want to help.\n\nThanks to the following people who have contributed to this project:\n\n- [olivmath](https://github.com/olivmath)\n- [marcoslkz](https://github.com/marcoslkz)\n- [VanJustin](https://github.com/VanJustin)\n- [xonfps](https://github.com/xonfps)\n\n## Contact\n\nIf you want to contact me you can reach me at <development@lunes.io>.\n\n## License\n\n[Apache License Version 2.0](https://github.com/lunes-platform/lunespy/blob/main/LICENSE).\n',
    'author': 'Lunes Platform',
    'author_email': 'development@lunes.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
