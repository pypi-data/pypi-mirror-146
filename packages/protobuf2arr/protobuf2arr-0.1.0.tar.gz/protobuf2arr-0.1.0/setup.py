# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protobuf2arr']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.20.0,<4.0.0', 'simplejson>=3.17.6,<4.0.0']

setup_kwargs = {
    'name': 'protobuf2arr',
    'version': '0.1.0',
    'description': "Translate a protobuf message to Google's RPC array format.",
    'long_description': None,
    'author': 'Kevin Ramdath',
    'author_email': 'krpent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
