# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['context_engine']

package_data = \
{'': ['*']}

install_requires = \
['ctx>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'context-engine',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vkldwwk',
    'author_email': 'jeff.elliott.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
