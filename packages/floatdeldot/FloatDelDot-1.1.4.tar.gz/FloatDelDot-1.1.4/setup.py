# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['floatdeldot']
setup_kwargs = {
    'name': 'floatdeldot',
    'version': '1.1.4',
    'description': 'This prorgamm delete dot in float (15.0 -> 15)',
    'long_description': None,
    'author': 'GleDVIn',
    'author_email': 'gledvin.info@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
