# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['briscola_gym', 'briscola_gym.player']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.21.0,<0.22.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'briscola-gym',
    'version': '0.1.0',
    'description': 'Gym environment for Briscola game',
    'long_description': None,
    'author': 'Mikedev',
    'author_email': 'mdv1994@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
