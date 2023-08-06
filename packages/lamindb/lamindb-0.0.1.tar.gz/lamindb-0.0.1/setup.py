# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lamindb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lamindb',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Lamin Labs',
    'author_email': 'laminlabs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
