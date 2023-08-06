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
    'version': '0.1.2',
    'description': 'Toolforge client',
    'long_description': "# toolforge-cli\n\nCLI to run toolforge related commands\n\n## Local development environment (guideline)\n\n### Tox on debian testing\n\nClone the repo including commit hooks (instructions here https://gerrit.wikimedia.org/r/admin/repos/cloud/toolforge/toolforge-cli).\n\nInstall tox:\n```\n~:$ apt install tox\n```\n\nMove to the directory where you cloned the repo, and run tox:\n```\n/path/to/repo/toolforge-cli:$ tox\n```\n\nThat will run the tests and create a virtualenv that you can use to manually debug anything you need, to enter it:\n```\n/path/to/repo/toolforge-cli:$ source .tox/py-tests/bin/activate\n```\n\n## Building the debian packages\nFor this you'll need debuild installed:\n```\n~:$ sudo apt install debuild\n```\n\nInstall the build dependencies, this requires devscripts and equivs:\n```\n~:$ sudo apt install devscripts equivs\n...\n/path/to/repo/toolforge-cli:$ sudo mk-build-deps --install debian/control\n```\n\nOr just manually check the `debian/control` file `Build-Dependencies` and install them manually.\n\nNote that it will build a debian package right there, and install it, you can remove it to clean up the dependencies any time.\n\n\nNow for the actuall build:\n```\n/path/to/repo/toolforge-cli:$ debuild -uc -us\n```\n\nThat will end up creating an unsigned package under `../toolforge-cli.*.deb`.\nIf you want to sign it, you will have to do something like:\n```\n/path/to/repo/toolforge-cli:$ debuild -kmy@key.org\n```\n",
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
