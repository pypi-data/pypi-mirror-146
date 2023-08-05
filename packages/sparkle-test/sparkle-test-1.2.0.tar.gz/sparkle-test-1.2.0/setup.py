# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparkle_test']

package_data = \
{'': ['*']}

install_requires = \
['pandas==1.3.5']

setup_kwargs = {
    'name': 'sparkle-test',
    'version': '1.2.0',
    'description': '',
    'long_description': None,
    'author': 'Machiel Keizer-Groeneveld',
    'author_email': 'machiel.groeneveldkeizer@vodafoneziggo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
