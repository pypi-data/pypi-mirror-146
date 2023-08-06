# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_lists', 'netbox_lists.api']

package_data = \
{'': ['*']}

install_requires = \
['netaddr>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'netbox-lists',
    'version': '2.1.0',
    'description': '',
    'long_description': None,
    'author': 'Devon Mar',
    'author_email': 'devonm@mdmm.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
