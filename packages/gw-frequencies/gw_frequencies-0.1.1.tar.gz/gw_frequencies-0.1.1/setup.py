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
    'version': '0.1.1',
    'description': 'A convenience package to make reduced frequency arrays for the representation of gravitational waveforms.',
    'long_description': '# gw_frequencies\nA convenience package to make reduced frequency arrays for the representation of gravitational waveforms.\n\nIt makes available the following functions; here they are documented \nvery shortly, see their docstrings (`help(func_name)`  in an interactive console)\nfor more details.\n\n- `seglen_from_freq`, which computes the duration T(f), in seconds, \n    of a gravitational wave signal starting at a given frequency, in Hertz.\n- `high_frequency_grid`, a uniform grid in frequency\n- `low_frequency_grid`, a non-uniform grid in frequency satisfying dN/df = 1/T(f) at each frequency \n- `mixed_frequency_grid`, a grid with the low-frequency specification below some pivot \n    and the high-frequency specification above it.\n\nThe main idea here is the `low_frequency_grid`, which is a slightly different implementation of the \nconcepts outlined by [Vinciguerra et al, 2017](http://arxiv.org/abs/1703.02062).\n\nTo install this package, do:\n```bash\npip install gw-frequencies\n```\n\nTo import the required functions, do \n```python\nfrom gw_frequencies.multibanding import <func_name>\n```\nwhere `<func name>` is the name of the function you want.\n\n',
    'author': 'jacopok',
    'author_email': 'jacopok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jacopok/gw_frequencies',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
