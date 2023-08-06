# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scarfs']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.55.1,<0.56.0', 'numpy>=1.18,<1.22']

setup_kwargs = {
    'name': 'scarfs',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Erik Brinkman',
    'author_email': 'erik.brinkman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
