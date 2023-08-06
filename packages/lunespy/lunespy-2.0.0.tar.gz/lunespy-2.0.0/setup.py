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
    'version': '2.0.0',
    'description': 'Library for communication with nodes in mainnet or testnet of the lunes-blockchain network Allows the automation of sending assets, issue end reissue tokens, leasing, registry, and create new wallet.',
    'long_description': '<p align="center">\n    <img alt="Lunes" src="docs/logo.png" width="100" />\n</p>\n\n# LunesPy\n\n- Library for communication with nodes in mainnet or testnet of the lunes-blockchain network\n  Allows the automation of **sending assets**, **issue end reissue tokens**, **lease** and **create new wallet**.\n\n[![Test](https://github.com/lunes-platform/lunespy/actions/workflows/python-app.yml/badge.svg)](https://github.com/lunes-platform/lunespy/actions/workflows/python-app.yml)\n[![License](https://img.shields.io/github/license/lunes-platform/lunespy?color=blueviolet)](LICENSE)\n[![Stars](https://img.shields.io/github/stars/lunes-platform/lunespy?color=blueviolet)](https://github.com/lunes-platform/lunespy/stargazers)\n\n[![CommitActivity](https://img.shields.io/github/commit-activity/m/lunes-platform/lunespy?color=blueviolet)](https://github.com/lunes-platform/lunespy/pulse)\n[![Forks](https://img.shields.io/github/forks/lunes-platform/lunespy?color=blueviolet)](https://github.com/lunes-platform/lunespy/network/members)\n[![Contributors](https://flat.badgen.net/github/contributors/lunes-platform/lunespy?color=purple)](https://github.com/lunes-platform/lunespy/graphs/contributors)\n![ClosedIssue](https://flat.badgen.net/github/closed-issues/lunes-platform/lunespy?color=red)\n[![Branches](https://badgen.net/github/branches/lunes-platform/lunespy?color=blueviolet)](https://github.com/lunes-platform/lunespy/branches)\n[![Watchers](https://img.shields.io/github/watchers/lunes-platform/lunespy.svg?color=blueviolet)](https://github.com/lunes-platform/lunespy/watchers)\n[![Followers](https://img.shields.io/github/followers/lunes-platform.svg?style=social&label=Follow&maxAge=2592000?color=blueviolet)](https://github.com/lunes-platform?tab=followers)\n[![Website](https://img.shields.io/website?url=https%3A%2F%2Flunes.io%2F)](https://lunes.io)\n![PullRequest](https://img.shields.io/github/issues-pr/lunes-platform/lunespy?color=blueviolet)\n![PullRequestClosed](https://img.shields.io/github/issues-pr-closed/lunes-platform/lunespy?color=blueviolet)\n\n<br><br>\n<a href="https://twitter.com/LunesPlatform" target="_blank">\n<img alt="Twitter: Lunes Platform" src="https://badgen.net/twitter/follow/lunesplatform?icon=twitter&label=follow @LunesPlatform&color=blue" />\n</a>  \n <a href="https://t.me/LunesPlatformPT" target="_blank">\n<img alt="Telegram" src="https://badgen.net/badge/icon/Lunes%20Platform?icon=telegram&label=Telegram&color=blue"/>\n</a>\n\n## Documentation\n\nThe `lunespy` documentations is hosted at [Telescope](https://blockchain.lunes.io/telescope/)\n\n## Changelog\n\nThe changelog process for this project is described [here](CHANGELOG.md).\n\n## Contributing\n\n`lunespy` is still under development. Contributions are always welcome! Please follow the [Developers Guide](CONTRIBUTING.md) if you want to help.\n\nThanks to the following people who have contributed to this project:\n\n- [olivmath](https://github.com/olivmath)\n- [marcoslkz](https://github.com/marcoslkz)\n- [VanJustin](https://github.com/VanJustin)\n- [xonfps](https://github.com/xonfps)\n\n## Contact\n\nIf you want to contact me you can reach me at <development@lunes.io>.\n\n## License\n\n[Apache License Version 2.0](https://github.com/lunes-platform/lunespy/blob/main/LICENSE).\n',
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
