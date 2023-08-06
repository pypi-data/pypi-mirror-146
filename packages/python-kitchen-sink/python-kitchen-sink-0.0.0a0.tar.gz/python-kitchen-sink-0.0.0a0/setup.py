# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kitchen_sink']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-kitchen-sink',
    'version': '0.0.0a0',
    'description': 'Everything but the kitchen sink',
    'long_description': '# Everything but the kitchen sink\n',
    'author': 'Ryan Munro',
    'author_email': '500774+munro@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/munro/python-kitchen-sink',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
