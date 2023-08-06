# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['word2quiz']

package_data = \
{'': ['*']}

install_requires = \
['docx2python>=2.0.4,<3.0.0', 'python-docx>=0.8.11,<0.9.0']

setup_kwargs = {
    'name': 'word2quiz',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Nico de Groot',
    'author_email': 'ndegroot0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
