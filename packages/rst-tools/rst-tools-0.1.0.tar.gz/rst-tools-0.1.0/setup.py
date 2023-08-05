# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rst_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rst-tools',
    'version': '0.1.0',
    'description': 'Rough sets implementation for Python',
    'long_description': None,
    'author': 'Rofilde Hasudungan',
    'author_email': 'rofilde@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
