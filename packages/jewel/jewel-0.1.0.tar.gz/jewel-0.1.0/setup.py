# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jewel', 'jewel.formats']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.1.0,<13.0.0']

entry_points = \
{'console_scripts': ['jewel = jewel.__main__:main']}

setup_kwargs = {
    'name': 'jewel',
    'version': '0.1.0',
    'description': 'Rich Python code snippets.',
    'long_description': None,
    'author': 'Aaron Stephens',
    'author_email': 'aaronjst93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
