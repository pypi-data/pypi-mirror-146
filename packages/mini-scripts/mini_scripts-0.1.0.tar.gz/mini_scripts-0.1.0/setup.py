# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mini_scripts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mini-scripts',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'lordralinc',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
