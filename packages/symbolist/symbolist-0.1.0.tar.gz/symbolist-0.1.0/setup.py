# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symbolist']

package_data = \
{'': ['*'], 'symbolist': ['fonts/*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0',
 'Pillow>=9.1.0,<10.0.0',
 'rectpack>=0.2.2,<0.3.0',
 'svgwrite>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'symbolist',
    'version': '0.1.0',
    'description': 'A list of railway symbols',
    'long_description': None,
    'author': 'DGEX Solutions',
    'author_email': 'contact@dgexsol.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
