# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcutils', 'bcutils.tests']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'flake8>=4.0,<5.0',
 'pandas>1,<=1.0.5',
 'requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'bc-utils',
    'version': '0.1.0',
    'description': 'Python utility automation scripts for Barchart.com',
    'long_description': None,
    'author': 'Andy Geach',
    'author_email': 'andy@bugorfeature.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bug-or-feature/bc-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
