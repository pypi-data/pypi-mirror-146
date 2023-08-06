# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_preprocessors']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'data-preprocessors',
    'version': '0.2.0',
    'description': 'An easy to use tool for Data Preprocessing specially for Text Preprocessing',
    'long_description': '# Data-Preprocessor\n\nPreprocess your data before training a model.',
    'author': 'Md. Musfiqur Rahaman',
    'author_email': 'musfiqur.rahaman@northsouth.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MusfiqDehan/data-preprocessors',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
