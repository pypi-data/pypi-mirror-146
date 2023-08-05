# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hpke']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.4.7,<4.0.0']

setup_kwargs = {
    'name': 'hpke',
    'version': '0.1.0',
    'description': 'HPKE implementation',
    'long_description': None,
    'author': 'Joseph Birr-Pixton',
    'author_email': 'jpixton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
