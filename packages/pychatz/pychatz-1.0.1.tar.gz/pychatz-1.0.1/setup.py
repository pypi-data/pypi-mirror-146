# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pychatz']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['pychatz = package_name:main']}

setup_kwargs = {
    'name': 'pychatz',
    'version': '1.0.1',
    'description': '',
    'long_description': 'TEST md\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MattiooFR/package_name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
