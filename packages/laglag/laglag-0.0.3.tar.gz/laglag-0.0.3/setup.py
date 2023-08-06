# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['cli==0.0.1']

setup_kwargs = {
    'name': 'laglag',
    'version': '0.0.3',
    'description': 'test',
    'long_description': None,
    'author': 'LAG',
    'author_email': 'lucaactisgrosso@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
