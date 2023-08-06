# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoodat_utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.35,<2.0.0',
 'google-cloud-storage>=2.2.1,<3.0.0',
 'pytest>=7.1.1,<8.0.0']

setup_kwargs = {
    'name': 'hoodat-utils',
    'version': '0.0.4',
    'description': '',
    'long_description': None,
    'author': 'Eugene Brown',
    'author_email': 'efbbrown@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
