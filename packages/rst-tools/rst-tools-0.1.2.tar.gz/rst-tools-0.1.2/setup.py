# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rst_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'rst-tools',
    'version': '0.1.2',
    'description': 'Rough sets implementation for Python',
    'long_description': None,
    'author': 'Rofilde Hasudungan',
    'author_email': 'rofilde@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
