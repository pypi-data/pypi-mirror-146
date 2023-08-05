# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mambio']

package_data = \
{'': ['*']}

install_requires = \
['pytorch>=1.0.2,<2.0.0', 'scikit-image>=0.19.2,<0.20.0']

setup_kwargs = {
    'name': 'mambio',
    'version': '0.1.2',
    'description': 'Machine learning multi analysis batch IO',
    'long_description': None,
    'author': 'Charles N. Christensen',
    'author_email': 'charles.n.chr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
