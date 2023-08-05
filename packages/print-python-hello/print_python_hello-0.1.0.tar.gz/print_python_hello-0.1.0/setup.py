# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_python_hello']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.3,<5.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'print-python-hello',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'YaroslavYaryk',
    'author_email': 'duhanov2003@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
