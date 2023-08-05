# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_redisearch']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<5.0', 'redis>=4.0.0,<5.0.0', 'wagtail>=2.15,<3.0']

setup_kwargs = {
    'name': 'wagtail-redisearch',
    'version': '0.1.0',
    'description': 'A Django app to use RediSearch as a search backend in Wagtail.',
    'long_description': None,
    'author': 'Tommaso Amici',
    'author_email': 'me@tommasoamici.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
