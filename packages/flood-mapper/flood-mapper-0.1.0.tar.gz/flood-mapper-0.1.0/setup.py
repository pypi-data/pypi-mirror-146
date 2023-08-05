# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flood_mapper']

package_data = \
{'': ['*']}

install_requires = \
['earthengine-api>=0.1.288,<0.2.0']

setup_kwargs = {
    'name': 'flood-mapper',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'cate',
    'author_email': 'catherineseale@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cateseale/flood-mapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
