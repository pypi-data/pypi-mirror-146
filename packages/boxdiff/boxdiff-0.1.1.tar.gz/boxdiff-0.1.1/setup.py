# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boxdiff', 'boxdiff.models']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'boxdiff',
    'version': '0.1.1',
    'description': 'Utilities for comparing bounding boxes',
    'long_description': None,
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kevinsbarnard/box-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
