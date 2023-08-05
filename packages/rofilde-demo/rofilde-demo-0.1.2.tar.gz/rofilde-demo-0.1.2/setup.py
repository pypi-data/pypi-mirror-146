# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rofilde_demo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rofilde-demo',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Rofilde Hasudungan',
    'author_email': 'rofilde@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
