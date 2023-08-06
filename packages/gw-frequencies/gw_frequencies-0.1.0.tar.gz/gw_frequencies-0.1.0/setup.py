# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gw_frequencies']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20,<2.0']

setup_kwargs = {
    'name': 'gw-frequencies',
    'version': '0.1.0',
    'description': 'A convenience package to make reduced frequency arrays for the representation of gravitational waveforms.',
    'long_description': None,
    'author': 'jacopok',
    'author_email': 'jacopok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
