# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lnmetrics_api', 'lnmetrics_api.queries']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'gql>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'lnmetrics.api',
    'version': '0.0.1',
    'description': 'Python implementation of the lnmetrics API to query the lnmetrics services',
    'long_description': None,
    'author': 'Vincenzo Palazzo',
    'author_email': 'vincenzopalazzodev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
