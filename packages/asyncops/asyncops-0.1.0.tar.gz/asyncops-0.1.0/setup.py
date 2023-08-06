# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncops']

package_data = \
{'': ['*']}

install_requires = \
['contextvars>=2.4,<3.0']

setup_kwargs = {
    'name': 'asyncops',
    'version': '0.1.0',
    'description': 'The library for async operations.',
    'long_description': None,
    'author': 'Zeb Taylor',
    'author_email': 'zceboys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
