# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netdisc']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'netmiko>=4.0.0,<5.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'netdisc',
    'version': '0.1.0',
    'description': 'Discovers VLAN interfaces on specific network devices',
    'long_description': None,
    'author': 'Codie Jones',
    'author_email': 'codiejones1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
