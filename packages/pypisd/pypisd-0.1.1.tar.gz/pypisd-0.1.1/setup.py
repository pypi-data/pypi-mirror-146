# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypisd']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.27.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['pypisd = pypisd.main:cli']}

setup_kwargs = {
    'name': 'pypisd',
    'version': '0.1.1',
    'description': 'CLI tool to fetch source distribution url links from https://pypi.org for a given python package and its version.',
    'long_description': None,
    'author': 'Fernando',
    'author_email': 'fegoa89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
