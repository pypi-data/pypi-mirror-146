# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salix_jmespath_tools']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'salix-jmespath-tools',
    'version': '0.1.0',
    'description': 'Custom functions for jmespath',
    'long_description': None,
    'author': 'Salix',
    'author_email': 'codegreen@pilae.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
