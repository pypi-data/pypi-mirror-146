# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_updater']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0',
 'ehelply-logger>=0.0.8,<0.0.9',
 'pydantic>=1.9.0,<2.0.0',
 'python-slugify>=6.1.1,<7.0.0',
 'requests>=2.27.1,<3.0.0',
 'wheel>=0.37.1,<0.38.0']

setup_kwargs = {
    'name': 'ehelply-updater',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Updater\nMicroservice updater\n',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
