# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polarbears', 'polarbears.dataframe']

package_data = \
{'': ['*']}

install_requires = \
['polars>=0.13.16,<0.14.0']

setup_kwargs = {
    'name': 'polarbears',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Pryer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
