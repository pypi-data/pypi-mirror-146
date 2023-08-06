# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memorable']

package_data = \
{'': ['*'], 'memorable': ['_resources/*', '_resources/nouns/*']}

setup_kwargs = {
    'name': 'memorable',
    'version': '1.0.0',
    'description': 'A library for creating memorable strings.',
    'long_description': None,
    'author': 'Kevin Schiroo',
    'author_email': 'kjschiroo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
