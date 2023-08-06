# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['rsacore']
setup_kwargs = {
    'name': 'rsacore',
    'version': '1.0.0',
    'description': 'A simple RSA library for python with built-in AES, which allows you to exchange encrypted data with an unlimited size.  Examples at https://github.com/DarkestStream69/RSACore',
    'long_description': None,
    'author': 'TheMade4427',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
