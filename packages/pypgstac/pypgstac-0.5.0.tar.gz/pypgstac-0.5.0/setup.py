# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypgstac']

package_data = \
{'': ['*'], 'pypgstac': ['migrations/*']}

install_requires = \
['fire>=0.4.0,<0.5.0',
 'orjson>=3.5.2',
 'plpygis>=0.2.0,<0.3.0',
 'psycopg-pool>=3.1.1,<4.0.0',
 'psycopg>=3.0.10,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'smart-open>=4.2.0,<5.0.0',
 'tenacity>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['pypgstac = pypgstac.pypgstac:cli']}

setup_kwargs = {
    'name': 'pypgstac',
    'version': '0.5.0',
    'description': '',
    'long_description': 'Python tools for working with PGStac\n',
    'author': 'David Bitner',
    'author_email': 'bitner@dbspatial.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stac-utils/pgstac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
