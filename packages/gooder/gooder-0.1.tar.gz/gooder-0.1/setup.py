# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gooder']
install_requires = \
['cssselect>=1.1.0,<2.0.0', 'lxml>=4.8.0,<5.0.0', 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'gooder',
    'version': '0.1',
    'description': 'Simple Google parser',
    'long_description': None,
    'author': 'slavatar',
    'author_email': 'nslavatar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/9Slavatar/gooder',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
