# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kupo']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.2.0,<13.0.0', 'textual>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['kupo = kupo.app:run']}

setup_kwargs = {
    'name': 'kupo',
    'version': '0.1.0a0',
    'description': '',
    'long_description': None,
    'author': 'Darren Burns',
    'author_email': 'darrenb900@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
