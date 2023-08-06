# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_preprocessors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'data-preprocessors',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Md. Musfiqur Rahaman',
    'author_email': 'musfiqur.rahaman@northsouth.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
