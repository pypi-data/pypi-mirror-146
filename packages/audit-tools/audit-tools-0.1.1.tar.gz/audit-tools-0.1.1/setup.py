# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audit_tools', 'audit_tools.core', 'audit_tools.core.functions']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rich>=12.2.0,<13.0.0']

setup_kwargs = {
    'name': 'audit-tools',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'pixl',
    'author_email': 'jakewjevans@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
