# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tibian', 'tibian.sources', 'tibian.targets']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'jira>=3.1.1,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'types-PyYAML>=6.0.5,<7.0.0',
 'types-python-dateutil>=2.8.10,<3.0.0',
 'types-requests>=2.27.14,<3.0.0']

setup_kwargs = {
    'name': 'tibian',
    'version': '0.1.0',
    'description': 'Ticket birthday announcer: A package to announce all creation birthdays of your tickets that live (too) long enough',
    'long_description': None,
    'author': 'Stefan Kraus',
    'author_email': 'stefan.kraus@methodpark.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
