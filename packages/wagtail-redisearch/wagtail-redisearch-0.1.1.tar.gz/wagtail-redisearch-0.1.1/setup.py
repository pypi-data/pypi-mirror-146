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
    'version': '0.1.1',
    'description': 'A Django app to use RediSearch as a search backend in Wagtail.',
    'long_description': '# wagtail-redisearch\n\nA Django app to use [RediSearch](https://redis.com/modules/redis-search/) as a search\nbackend in Wagtail.\n\n## Requirements\n\n- Django >= 3.2\n- Wagtail >= 2.15\n- RediSearch v2\n\n## Usage\n\nInstall [`wagtail-redisearch`](https://pypi.org/project/wagtail-redisearch/) from PyPi.\n\nIn your `settings.py` configure your search backend as follows:\n\n```py\nWAGTAILSEARCH_BACKENDS = {\n    "default": {\n        "BACKEND": "wagtail_redisearch",\n        # optional parameters\n        "INDEX": "custom-index-name", # default: "wagtail"\n        "HOST": "127.0.0.1",\n        "PORT": 6379,\n        # you can add any option here to be used when initializing\n        # a Redis client with redis-py.\n        # e.g.\n        "retry_on_error": True\n    }\n}\n```\n\nFor more information about what options you can pass to the Redis client, look at the [official documentation](https://redis.readthedocs.io/en/stable/connections.html#generic-client).\n\n`wagtail-redisearch` implements the interfaces described in [Backends Rolling your own](https://docs.wagtail.org/en/stable/topics/search/backends.html#rolling-your-own), thus usage in Wagtail requires no special adjustment.\n\nTo configure search on your models, follow the [official Wagtail documentation](https://docs.wagtail.org/en/stable/topics/search/index.html).\n\n## Contributing\n\nTo contribute to this project you\'ll need RediSearch installed and `poetry`.\n\n```sh\n# install dependencies\npoetry install\n\n# run tests\nmake test\n\n# run tests with tox\nmake test-all\n\n# to run a minimal Wagtail application to test things out\nmake run\n```\n',
    'author': 'Tommaso Amici',
    'author_email': 'me@tommasoamici.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TommasoAmici/wagtail-redisearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
