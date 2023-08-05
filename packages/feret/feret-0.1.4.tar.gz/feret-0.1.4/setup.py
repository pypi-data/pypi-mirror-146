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
    'version': '0.1.4',
    'description': 'Calculate Feret diameter.',
    'long_description': "# Feret\n\nThis python module can calculate the maximum and minimum Feret Diameter of a binary image. For a detailed explanation see this [wikipedia page](https://en.wikipedia.org/wiki/Feret_diameter).\n\nAt this early development stage, it can only calculate the maximum and minimum Feret Diameter but feature releases will offer the Feret diameter 90° to maximum and minimum. The module will also not return the angle of the diameters. Many things will come in the future.\n\nThe module can be used as followed:\n\n```python\nimport feret\nimport tifffile as tif\n\nimg = tif.imread('example.tif')\n\nres = feret.calc(img)\n\nprint(res.maxferet, res.minferet)\n```\n\n",
    'author': 'matthiasnwt',
    'author_email': '62239991+matthiasnwt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthiasnwt/feret',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
