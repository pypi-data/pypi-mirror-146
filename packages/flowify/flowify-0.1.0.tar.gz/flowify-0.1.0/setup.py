# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowify']

package_data = \
{'': ['*']}

install_requires = \
['fontfeatures', 'inflect', 'numpy', 'ufo2ft', 'ufoLib2']

entry_points = \
{'console_scripts': ['flowify = flowify:main']}

setup_kwargs = {
    'name': 'flowify',
    'version': '0.1.0',
    'description': 'Interrogate a font file',
    'long_description': None,
    'author': 'Simon Cozens',
    'author_email': 'simon@simon-cozens.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)
