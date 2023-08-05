# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['integrity']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.56.0,<0.57.0', 'mecha>=0.43.3,<0.44.0']

setup_kwargs = {
    'name': 'integrity',
    'version': '0.3.0',
    'description': 'Development facilities for the bolt environment',
    'long_description': '# Integrity\n\n> Development facilities for the bolt environment\n',
    'author': 'TheWii',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thewii/integrity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
