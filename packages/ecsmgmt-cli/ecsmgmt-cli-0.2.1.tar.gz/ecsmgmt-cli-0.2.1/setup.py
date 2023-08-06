# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecsmgmt', 'ecsmgmt._util', 'ecsmgmt.secret-key', 'ecsmgmt.user']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.0.1,<9.0.0',
 'inquirer>=2.7.0,<3.0.0',
 'python-ecsclient>=1.1.11,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['ecsmgmt = ecsmgmt:cli']}

setup_kwargs = {
    'name': 'ecsmgmt-cli',
    'version': '0.2.1',
    'description': 'Small CLI tool for interacting with the ECS Management API',
    'long_description': "# ecsmgmt-cli\n\nSmall CLI tool for interacting with the ECS Management API. ECS is Dell EMC's Object Storage (S3) Solution.\n\n## usage\n\n### config file\n**Warning: It's not recommended to store you're credentials in an plaintext file. If you decide nevertheless to do so, please be shure to limit the access to the config file, for example with `chmod 600 $configfilepath`.**\n\nThe config file is expected to be in the common config directories for the following platforms:\n* unix: `~/.config/ecsmgmt-cli/config.yml`\n* macOS: `~/Library/Application Support/ecsmgmt-cli/config.yml`\n* Windows: `C:\\Users\\<user>\\AppData\\Local\\ecsmgmt-cli\\config.yml`\n\n",
    'author': 'Dominik Rimpf',
    'author_email': 'dominik.rimpf@kit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/domrim/ecsmgmt-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
