# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['convert_ms']
setup_kwargs = {
    'name': 'convert-ms',
    'version': '0.0.3',
    'description': 'Convert a time units to seconds',
    'long_description': None,
    'author': 'Forzy',
    'author_email': 'nikita11tzby@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
