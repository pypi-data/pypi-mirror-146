# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salix_containers']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.0,<2.0.0', 'salix-jmespath-tools>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'salix-containers',
    'version': '0.1.0',
    'description': 'Occasionally handy container types',
    'long_description': None,
    'author': 'Salix',
    'author_email': 'salix@pilae.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
