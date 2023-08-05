# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['harpar']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'harpar',
    'version': '0.0.0',
    'description': 'A Har File Parser for Python3',
    'long_description': None,
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
