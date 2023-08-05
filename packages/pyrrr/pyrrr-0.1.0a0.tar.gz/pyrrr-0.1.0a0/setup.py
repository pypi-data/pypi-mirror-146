# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrrr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyrrr',
    'version': '0.1.0a0',
    'description': 'Reduced-Rank Regression',
    'long_description': None,
    'author': 'chrisaddy',
    'author_email': 'chris.william.addy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
