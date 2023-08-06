# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['run_logger']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'gql>=2.0.0,<3.0.0',
 'jsonlines>=2.0.0,<3.0.0',
 'numpy>=1.19.2,<2.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'run-logger',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Ethan Brooks',
    'author_email': 'ethanabrooks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
