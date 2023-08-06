# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['when']

package_data = \
{'': ['*'], 'when': ['data/*']}

install_requires = \
['airportsdata>=20220406,<20220407',
 'arrow>=1.2.2,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rich-click>=1.3.0,<2.0.0',
 'rich>=12.2.0,<13.0.0',
 'typer>=0.4.1,<0.5.0',
 'tzdata>=2022.1,<2023.0',
 'tzlocal>=4.2,<5.0']

setup_kwargs = {
    'name': 'when-cli',
    'version': '1.1.0',
    'description': 'When CLI is a timezone conversion tool. It takes as input a natural time string, can also be a time range, and converts it into different timezone(s) at specific location(s).',
    'long_description': None,
    'author': 'Christian Assing',
    'author_email': 'chris@ca-net.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
