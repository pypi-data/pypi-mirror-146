# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparkle_session']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sparkle-session',
    'version': '1.3.0',
    'description': 'Common patterns and often used code from dozens of pyspark projects available at your fingertips',
    'long_description': None,
    'author': 'Machiel Keizer Groeneveld',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
