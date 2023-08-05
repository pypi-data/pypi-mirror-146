# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rst_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas']

setup_kwargs = {
    'name': 'rst-tools',
    'version': '0.1.5',
    'description': 'Rough sets implementation for Python',
    'long_description': '# Guidelines \n\n## Instalation\nTo install this package use pip as following \n\n`pip install rst-tools`\n\n## Usage \n\n```python\nimport pandas as pd\nfrom rst_tools.roughsets import RoughSets as RST\nfrom rst_tools.roughsets import QuickReduct as QR\n\ndf = pd.read_csv("YOUR/FILE.csv")\nconditional_attributes = list(df.column.values)\ndecision_attribute = conditional_attributes[-1]\ndel conditional_attributes[-1]\n\nroughsets = RST(df)\n\n\'\'\'....\'\'\'\n```',
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
