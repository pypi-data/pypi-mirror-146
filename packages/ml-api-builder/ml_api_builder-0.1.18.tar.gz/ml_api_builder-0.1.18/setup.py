# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ml_api_builder']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.1,<2.0.0', 'requests>=2.20.1,<3.0.0']

setup_kwargs = {
    'name': 'ml-api-builder',
    'version': '0.1.18',
    'description': '',
    'long_description': None,
    'author': 'Michael Henzl',
    'author_email': 'michael.henzl@seznam.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
