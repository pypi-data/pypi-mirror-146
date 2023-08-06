# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lawsql_trees']

package_data = \
{'': ['*']}

install_requires = \
['citation-decision>=0.0.1,<0.0.2',
 'lawsql-tree-unit>=0.0.1,<0.0.2',
 'sqlite-utils>=3.25,<4.0',
 'statute-matcher>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'lawsql-trees',
    'version': '0.0.2',
    'description': 'Pull and format statute / codification data (tree structures) from local path to raw yaml files.',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
