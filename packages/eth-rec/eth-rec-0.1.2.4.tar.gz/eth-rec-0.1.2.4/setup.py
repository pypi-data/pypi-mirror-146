# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eth_rec']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['eth-rec = eth_rec.eth_rec:main']}

setup_kwargs = {
    'name': 'eth-rec',
    'version': '0.1.2.4',
    'description': 'Download ETH-Livestream',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
