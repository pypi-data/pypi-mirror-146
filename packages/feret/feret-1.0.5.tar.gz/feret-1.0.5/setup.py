# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feret']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.3,<2.0.0',
 'opencv-python>=4.5,<5.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'feret',
    'version': '1.0.5',
    'description': 'Calculate Feret diameter.',
    'long_description': "# *Feret*: A Python Module to calculate the Feret Diameter of Binary Images\n\n[![Downloads](https://static.pepy.tech/personalized-badge/feret?period=total&units=abbreviation&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/feret)\n\nThis python module can calculate the following parameters for binary images:\n\n* maximum Feret diameter (maxferet, maxf)\n* minimum Feret diameter (minferet, minf)\n* Feret diameter 90 ° to the minferet (minferet90, minf90) \n* Feret diameter 90 ° to maxferet (maxferet90, maxf90) \n\nSee this [Wikipedia page](https://en.wikipedia.org/wiki/Feret_diameter) to get the definition of those parameters.\n\nThis module gives the exact results as ImageJ (use `edge=True` as shown below), all the parameters are exactly calculated and **not** approximated.\n\n## Installations\nThis project is available via pip:\n\n`pip install feret`\n\n## Pieces of Information\n\n#### Convex Hull\n\nThe definition of the maxferet and minferet uses the image of a caliper. Therefore, only the points which correspond to the convex hull of the object play a role. That is why before any calculations the convex hull is determined to reduce the runtime.\n\n#### Maxferet\nThe maxferet is calculated as the maximum Euclidean distance of all pixels.\n\n#### Minferet\n\nThe minferet is exactly calculated and **not** approximated. My algorithm uses the fact, that the calipers that define the minferet run on one side through two points and on the other through one point. The script iterates over all edge points and defines a line through the point and the one next to it. Then all the distances to the other points are calculated and the maximum is taken. The minimum of all those maximums is the minferet. The maximum of all those maximums is **not** the maxferet, that is the reason it is calculated separately. The runtime of this is already pretty good but hopefully I can improve it in the future.\n\n## Use\nThe module can be used as followed:\n\n```python\nimport feret\n\n# tifffile is not required nor included in this module.\nimport tifffile as tif\nimg = tif.imread('example.tif') # Image has to be a numpy 2d-array.\n\n\n# get the values\nmaxf, minf, minf90, maxf90 = feret.all(img)\n\n# get only maxferet\nmaxf = feret.max(img)\n\n# get only minferet\nminf = feret.min(img)\n\n# get only minferet90\nminf90 = feret.min90(img)\n\n# get only maxferet90\nmaxf90 = feret.max90(img)\n\n# get all the informations\nres = feret.calc(img)\nmaxf = res.maxf\nminf =  res.minf\nminf90 = res.minf90\nminf_angle = res.minf_angle\nminf90_angle = res.minf90_angle\nmaxf_angle = res.maxf_angle\nmaxf90_angle = res.maxf90_angle\n```\n\nThere is an option to calculate the Feret diameters for the pixel edges instead of the centers. Just add an `edge=True` in the call as shown below. This works for all calls analogous.\n\n```python\nimport feret\n\n# tifffile is not required nor included in this module.\nimport tifffile as tif\nimg = tif.imread('example.tif') # Image has to be a numpy 2d-array.\n\n# get only maxferet\nmaxf = feret.max(img, edge=True)\n```\n\n### Future Releases\n\n* add a return_angle in the calls\n* add the possibility to show plots of the results\n",
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
