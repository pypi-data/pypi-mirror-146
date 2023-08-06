# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpystan']

package_data = \
{'': ['*'], 'jrpystan': ['data/*']}

install_requires = \
['arviz>=0.12.0,<0.13.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pystan>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'jrpystan',
    'version': '1.0.1',
    'description': 'Jumping Rivers: Introduction to Bayesian inference using PyStan',
    'long_description': None,
    'author': 'Jumping Rivers',
    'author_email': 'info@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
