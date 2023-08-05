# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bintest']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'scripttest>=1.3,<2.0']

setup_kwargs = {
    'name': 'bintest',
    'version': '0.2.0',
    'description': 'python library for test binarys',
    'long_description': '',
    'author': 'Artur Gomes',
    'author_email': 'contato@arturgomes.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arturgoms/python-bintest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
