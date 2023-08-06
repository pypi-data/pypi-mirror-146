# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepgis_utils']

package_data = \
{'': ['*']}

install_requires = \
['GeoAlchemy2>=0.11.1,<0.12.0',
 'SQLAlchemy>=1.4.35,<1.5.0',
 'geopandas>=0.10.2,<0.11.0',
 'psycopg2>=2.9.3,<2.10.0',
 'requests>=2.27.1,<2.28.0']

setup_kwargs = {
    'name': 'deepgis-utils',
    'version': '0.1.1',
    'description': 'A collection of utilities for DeepGIS',
    'long_description': '',
    'author': 'Xuanh.W',
    'author_email': 'Xuanhao.W.coding@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Rainlv/DeepGIS-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
