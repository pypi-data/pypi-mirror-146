# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toolforge_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'requests>=2.27.1,<3.0.0',
 'urllib3>=1.26.8,<2.0.0']

entry_points = \
{'console_scripts': ['toolforge = toolforge_cli.cli:main']}

setup_kwargs = {
    'name': 'toolforge-cli',
    'version': '0.1.1',
    'description': 'Toolforge client',
    'long_description': None,
    'author': 'David Caro',
    'author_email': 'dcaro@wikimedia.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gerrit.wikimedia.org/r/admin/repos/cloud/toolforge/toolforge-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
