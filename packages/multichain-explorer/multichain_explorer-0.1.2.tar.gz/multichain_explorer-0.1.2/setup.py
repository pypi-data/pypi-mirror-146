# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multichain_explorer',
 'multichain_explorer.src',
 'multichain_explorer.src.models',
 'multichain_explorer.src.models.provider',
 'multichain_explorer.src.providers',
 'multichain_explorer.src.providers.eth',
 'multichain_explorer.src.services',
 'multichain_explorer.src.validators',
 'multichain_explorer.src.validators.eth']

package_data = \
{'': ['*']}

install_requires = \
['web3>=5.28,<6.0']

setup_kwargs = {
    'name': 'multichain-explorer',
    'version': '0.1.2',
    'description': 'A simple package to explore multiple blockchains in an homogeneous way',
    'long_description': None,
    'author': 'sdominguez894',
    'author_email': 'sdominguez894@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
