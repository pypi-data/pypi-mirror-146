# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lawsql_cases_raw',
 'lawsql_cases_raw.raw_sql',
 'lawsql_cases_raw.tables',
 'lawsql_cases_raw.voting']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Unidecode>=1.3.0,<2.0.0',
 'citation-docket>=0.0.1,<0.0.2',
 'citation-report>=0.0.1,<0.0.2',
 'datasette>=0.60.1,<0.61.0',
 'httpx>=0.22.0,<0.23.0',
 'lawsql-cases-justices>=0.0.1,<0.0.2',
 'sqlite-utils>=3.22,<4.0']

setup_kwargs = {
    'name': 'lawsql-cases-raw',
    'version': '0.0.2',
    'description': 'Get decision data from .html and yaml files; updates local database with field lookups.',
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
