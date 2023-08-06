# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getmovieinfo', 'getmovieinfo.WebCrawler']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'jsons>=1.6.1,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'selenium>=4.1.3,<5.0.0']

entry_points = \
{'console_scripts': ['MovieInfo = getmovieinfo.MovieInfo:main']}

setup_kwargs = {
    'name': 'getmovieinfo',
    'version': '0.1.2',
    'description': 'Package to search specific video or keyword on a set of av websites',
    'long_description': '# Raincoat\n\nMovieInfo is a tool to search specific number or keyword from a set of av and get information of videos and output json. This json is use for a discord bot or automation torrent download.\n\n### Installation\n\n`pip install getmovieinfo\n\n### Requirements\n\n- python = "^3.7"\n- selenium = "^4.1.3"\n- requests = "^2.27.1"\n- lxml = "^4.8.0"\n- argparse = "^1.4.0"\n- jsons = "^1.6.1"\n- secrets\n\n\n### Usage\n\n`MovieInfo --number SSIS-356\n\n`MovieInfo --keyword 涼森れむ\n\n#### Parameters\n\n- --number\n  - Specify a video number\n- --keyword\n  - SPecify a keyword\n- --cache_dir\n  - specify a dir to store the result json\n\n\n# License\n\nThis project is licensed under the MIT License\n',
    'author': 'crvidoeVR',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/crvideo/MovieInfo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
