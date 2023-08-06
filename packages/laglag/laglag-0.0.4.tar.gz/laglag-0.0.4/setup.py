# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "cli"': ['cli==0.0.1']}

setup_kwargs = {
    'name': 'laglag',
    'version': '0.0.4',
    'description': 'test',
    'long_description': None,
    'author': 'LAG',
    'author_email': 'lucaactisgrosso@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
