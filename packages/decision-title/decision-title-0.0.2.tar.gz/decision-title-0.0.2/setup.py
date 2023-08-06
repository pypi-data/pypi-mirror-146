# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decision_title']

package_data = \
{'': ['*']}

install_requires = \
['citation-decision>=0.0.3,<0.0.4', 'decision-title-vs-inre>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'decision-title',
    'version': '0.0.2',
    'description': 'Get & format case titles from cleaned Philippine Supreme Court decisions',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
