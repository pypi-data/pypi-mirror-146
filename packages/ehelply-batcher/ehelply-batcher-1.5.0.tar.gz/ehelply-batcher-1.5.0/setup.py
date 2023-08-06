# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ehelply_batcher', 'ehelply_batcher.tests']

package_data = \
{'': ['*']}

install_requires = \
['ehelply-logger>=0.0.8,<0.0.9',
 'pytest-asyncio>=0.18.3,<0.19.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'typer>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'ehelply-batcher',
    'version': '1.5.0',
    'description': '',
    'long_description': '# Batcher\nAutomatic, scheduled, configurable, and scalable batching.\n\n`pip install ehelply-batcher`\n',
    'author': 'Shawn Clake',
    'author_email': 'shawn.clake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ehelply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
