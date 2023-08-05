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
    'version': '0.4.0',
    'description': 'Calculate Feret diameter.',
    'long_description': "# *Feret*: A Python Module to calculate the Feret Diameter of Binary Images\n\nThis python module can calculate the maximum Feret diameter (maxferet, maxf), the minimum Feret diameter (minferet, minf), the Feret diameter 90 ° to the minferet (minferet90, minf90) and to maxferet (maxferet90, maxf90) of a binary image. For a detailed explanation see this [Wikipedia page](https://en.wikipedia.org/wiki/Feret_diameter).\n\n## Installation\nThis project is available via pip:\n\n`pip install feret`\n\n## Informations\n\n#### Maxferet\nThe maxferet is calculated as the maximum Euclidean distance of all pixels.\n\n#### Minferet\nThe minferet is only approximated in two steps at the moment. First, the distance of to parallel lines, which surround the object, is calculated for all angles from 0° to 180°. The minimum of this first calculation is used as the initial guess for a minimization algorithm, which is the second part of the approximation. Even if this method is not perfect, the difference to the true minferet can be neglected in most cases.\n\n\nAt this early development stage, it can only calculate the maximum and minimum Feret Diameter but feature releases will offer the Feret diameter 90° to maximum and minimum. The module will also not return the angle of the diameters. Many things will come in the future.\n\n## Use\nThe module can be used as followed:\n\n```python\nimport feret\n\n# tifffile is not required nor included in this module.\nimport tifffile as tif\nimg = tif.imread('example.tif') # Image has to be a numpy 2d-array.\n\n\n# get the values\nmaxf, minf, minf90, maxf90 = feret.all(img)\n\n# get only maxferet\nmaxf = feret.max(img)\n\n# get only minferet\nminf = feret.min(img)\n\n# get only minferet90\nminf90 = feret.min90(img)\n\n# get only maxferet90\nmaxf90 = feret.max90(img)\n\n# get all the informations\nres = feret.calc(img)\nmaxf = res.maxf\nminf =  res.minf\nminf90 = res.minf90\nminf_angle = res.minf_angle\nminf90_angle = res.minf90_angle\nmaxf_angle = res.maxf_angle\nmaxf90_angle = res.maxf90_angle\n```\n\nThere is an option to calculate the Feret diameters for the pixel edges instead of the centers. Just add an `edge=True` in the call as shown below. This works for all calls analogous.\n\n```python\nimport feret\n\n# tifffile is not required nor included in this module.\nimport tifffile as tif\nimg = tif.imread('example.tif') # Image has to be a numpy 2d-array.\n\n# get only maxferet\nmaxf = feret.max(img, edge=True)\n```\n\n",
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
