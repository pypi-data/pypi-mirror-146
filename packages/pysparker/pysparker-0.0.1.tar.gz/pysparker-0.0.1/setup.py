# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysparker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysparker',
    'version': '0.0.1',
    'description': 'Some utility functions for PySpark.',
    'long_description': None,
    'author': 'Ben Du',
    'author_email': 'longendu@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
