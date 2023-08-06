# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambdashim']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lambdashim',
    'version': '0.1.0',
    'description': 'A little wsgi shim for AWS Lambda.',
    'long_description': None,
    'author': 'Abram Isola',
    'author_email': 'abram@isola.mn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
