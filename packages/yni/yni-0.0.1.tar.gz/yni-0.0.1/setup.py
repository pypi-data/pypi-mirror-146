# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yni']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yni',
    'version': '0.0.1',
    'description': 'A parser for the yni config file.',
    'long_description': '',
    'author': 'Alex Hutz',
    'author_email': 'frostiiweeb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FrostiiWeeb/yni',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
