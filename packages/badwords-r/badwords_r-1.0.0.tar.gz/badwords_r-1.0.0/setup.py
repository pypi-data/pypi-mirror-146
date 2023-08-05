# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['badwords_r']
setup_kwargs = {
    'name': 'badwords-r',
    'version': '1.0.0',
    'description': 'All russian bad words for bad words filters',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
