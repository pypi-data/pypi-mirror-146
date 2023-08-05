# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feret']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.3,<2.0.0', 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'feret',
    'version': '0.2.2',
    'description': 'Calculate Feret diameter.',
    'long_description': "# Python Module to calculate the Feret Diameter of Binary Images\n\nThis python module can calculate the maximum Feret diameter (maxferet) and minimum Feret diameter (minferet) of a binary image. For a detailed explanation see this [wikipedia page](https://en.wikipedia.org/wiki/Feret_diameter).\n\n## Installation\nThis project is available with pip\n\n`pip install feret`\n\n## Informations\n\n### Maxferet\nThe maxferet is calculated as the maximum euclidean distance of all pixels.\n\n### Minferet\nThe minferet is only approximated in two steps at the moment. First , the distance of to parallel lines, which surrund the object, are calculated for all angles from 0° to 180°. The minimum of of this first calculation is used as initial guess for a minimization algorithm, which is the second part of the approximation. Even if this method is not perfect, the difference to the true minferet can be neglegted for most cases.\n\n\nAt this early development stage, it can only calculate the maximum and minimum Feret Diameter but feature releases will offer the Feret diameter 90° to maximum and minimum. The module will also not return the angle of the diameters. Many things will come in the future.\n\n## Use\nThe module can be used as followed:\n\n```python\nimport feret\nimport tifffile as tif\n\nimg = tif.imread('example.tif')\n\n# get the class\nres = feret.calc(img)\nmaxf, minf = res.maxferet, res.minferet\n\n# get the values\nmaxf, minf = feret.all(img)\n\n# get only maxferet\nmaxf = feret.max(img)\n\n# get only minferet\nminf = feret.min(img)\n```\n\nAt the moment there is only one option. It is possible to use the pixel corners instead of the pixel centers. ImageJ uses the pixel corners. Here the keyword `edge` is used. See the following code to get maxferet und minferet for the edges.\n\n```python\nimport feret\nimport tifffile as tif\n\nimg = tif.imread('example.tif')\n\n# get the class\nres = feret.calc(img, edge=True)\nmaxf, minf = res.maxferet, res.minferet\n\n# get the values\nmaxf, minf = feret.all(img, edge=True)\n\n# get only maxferet\nmaxf = feret.max(img, edge=True)\n\n# get only minferet\nminf = feret.min(img, edge=True)\n```\n\n",
    'author': 'matthiasnwt',
    'author_email': '62239991+matthiasnwt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthiasnwt/feret',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
