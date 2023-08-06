# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gtfs_kit']

package_data = \
{'': ['*']}

install_requires = \
['folium>=0',
 'geopandas>=0',
 'json2html>=1',
 'pandas>=1',
 'pycountry>=19',
 'requests>=2',
 'rtree>=0',
 'shapely>=1',
 'utm>=0']

setup_kwargs = {
    'name': 'gtfs-kit',
    'version': '5.2.1',
    'description': 'A Python 3.8+ library for analyzing GTFS feeds.',
    'long_description': "GTFS Kit\n********\n.. image:: https://travis-ci.com/mrcagney/gtfs_kit.svg?branch=master\n    :target: https://travis-ci.come/mrcagney/gtfs_kit\n\nGTFS Kit is a Python 3.8+ library for analyzing `General Transit Feed Specification (GTFS) <https://en.wikipedia.org/wiki/GTFS>`_ data in memory without a database.\nIt uses Pandas and Shapely to do the heavy lifting.\n\nThis project supersedes `GTFSTK <https://github.com/mrcagney/gtfstk>`_.\n\n\nInstallation\n=============\n``poetry add gtfs_kit``.\n\n\nExamples\n========\nYou can find examples in the Jupyter notebook ``notebooks/examples.ipynb``.\n\n\nAuthors\n=========\n- Alex Raichev, 2019-09\n\n\nDocumentation\n=============\nDocumentation is built via Sphinx from the source code in the `docs` directory then published to Github Pages at `mrcagney.github.io/gtfs_kit_docs <https://mrcagney.github.io/gtfs_kit_docs>`_.\n\n\nNotes\n=====\n- Development status is Alpha. I use this project for work and change it breakingly to suit my needs.\n- This project uses semantic versioning.\n- Thanks to `MRCagney <http://www.mrcagney.com/>`_ for donating to this project.\n- Constructive feedback and contributions are welcome. Please issue pull requests from a feature branch into the ``develop`` branch and include tests.\n- GTFS time is measured relative noon minus 12 hours, which can mess things up when crossing into daylight savings time. I don't think this issue causes any bugs in GTFS Kit, but you and i have been warned. Thanks to derhuerst for bringing this to my attention in `closed Issue 8 <https://github.com/mrcagney/gtfs_kit/issues/8#issue-1063633457>`_.\n",
    'author': 'Alex Raichev',
    'author_email': 'araichev@mrcagney.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrcagney/gtfs_kit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
