# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convert_shp_to_csv']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.1,<2.0.0',
 'geopandas>=0.10.2,<0.11.0',
 'haversine>=2.5.1,<3.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pygeos>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['convert-shp-to-csv = convert_shp_to_csv.main:main']}

setup_kwargs = {
    'name': 'convert-shp-to-csv',
    'version': '0.2.0',
    'description': 'Converts shape files (.shp) to a gridded csv file',
    'long_description': '# convert-shp-to-csv\n\nThis tool will take a shape file (.shp), and convert it to a gridded csv file with lat/long of the\ncenter of the grid as columns.\n\nAny shapes that overlap this point when the shape is overlaid on to the grid will be reflected in\nadditional columns\n\n## Usage:\n\n```\nusage: convert-shp-to-csv [-h] [--output-file OUTPUT_FILE] [--cell-size CELL_SIZE] shape_file\n\nConverts a shape file (.shp) to a gridded csv file.\n    \n\npositional arguments:\n  shape_file            Shape file (.shp) to convert\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --output-file OUTPUT_FILE, -o OUTPUT_FILE\n                        Name of csv file to output\n  --cell-size CELL_SIZE\n                        Cell size, in lat/long segments. Default: 0.1\n```\n\n## Example output:\n\n```\nlatitude,longitude,EthGLG,EthHGComb\n7.4488230199999546,34.35153731999999,Unconsolidated sedimentary - Miocene to Recent (minor consolidated Alwero Sandstone),U-LM\n7.4488230199999546,34.35153731999999,Igneous Volcanic,I-M/H\n7.4488230199999546,34.35153731999999,Precambrian Mobile/Orogenic Belt,B-L\n7.548823019999955,34.35153731999999,Unconsolidated sedimentary - Miocene to Recent (minor consolidated Alwero Sandstone),U-LM\n7.548823019999955,34.35153731999999,Igneous Volcanic,I-M/H\n7.548823019999955,34.35153731999999,Unconsolidated sedimentary - Miocene to Recent (minor consolidated Alwero Sandstone),U-LM\n```',
    'author': 'Brandon Rose',
    'author_email': 'brandon@jataware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
