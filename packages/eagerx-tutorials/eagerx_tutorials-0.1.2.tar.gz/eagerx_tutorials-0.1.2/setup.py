# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eagerx_tutorials',
 'eagerx_tutorials.pendulum',
 'eagerx_tutorials.pendulum.ode']

package_data = \
{'': ['*']}

install_requires = \
['eagerx-ode>=0.1.5,<0.2.0',
 'eagerx>=0.1.14,<0.2.0',
 'notebook>=6.4.10,<7.0.0',
 'stable-baselines3>=1.2,<2.0']

setup_kwargs = {
    'name': 'eagerx-tutorials',
    'version': '0.1.2',
    'description': 'Tutorials on how to use EAGERx.',
    'long_description': None,
    'author': 'Jelle Luijkx',
    'author_email': 'j.d.luijkx@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eager-dev/eagerx_tutorials',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
