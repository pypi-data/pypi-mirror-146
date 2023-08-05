# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cs_money_parser']
setup_kwargs = {
    'name': 'cs-money-parser',
    'version': '0.0.2',
    'description': 'Quick programmatic search for objects from the site cs.money',
    'long_description': None,
    'author': 'Dark Laybel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
