# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['img_dice']

package_data = \
{'': ['*'], 'img_dice': ['resources/*']}

install_requires = \
['PySide2>=5.15.2,<6.0.0',
 'fire>=0.4.0,<0.5.0',
 'pyshp>=2.2.0,<3.0.0',
 'rasterio>=1.2.10,<2.0.0']

entry_points = \
{'console_scripts': ['img-dice = img_dice.cli:main']}

setup_kwargs = {
    'name': 'img-dice',
    'version': '0.3.0',
    'description': 'Dice tif images into smaller sections using a shapefile of polygons',
    'long_description': None,
    'author': 'Taylor Denouden',
    'author_email': 'taylor.denouden@hakai.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tayden/img-dice-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
