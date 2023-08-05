# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ulidgen']

package_data = \
{'': ['*']}

install_requires = \
['ulid-py>=1.1,<2.0']

entry_points = \
{'console_scripts': ['ulidgen = ulidgen.cli:main']}

setup_kwargs = {
    'name': 'ulidgen',
    'version': '0.1.0',
    'description': 'CLI tool to generate ULID strings',
    'long_description': None,
    'author': 'Enam Mijbah Noor',
    'author_email': 'enammijbahnoor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
