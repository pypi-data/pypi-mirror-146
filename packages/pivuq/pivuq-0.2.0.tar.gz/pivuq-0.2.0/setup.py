# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pivuq']

package_data = \
{'': ['*']}

install_requires = \
['numpy<1.22.0', 'scikit-image>=0.19.2,<0.20.0']

extras_require = \
{':python_version < "3.10"': ['scipy>=1.8.0,<2.0.0', 'numba>=0.55.1,<0.56.0']}

setup_kwargs = {
    'name': 'pivuq',
    'version': '0.2.0',
    'description': 'A library for PIV Uncertainty Quantification',
    'long_description': '# PIV-UQ: PIV Uncertainty Quantification\n\n`Note: Primary aim is to implement UQ algorithms for PIV techniques. Future goals include possible extensions to other domains including but not limited to optical flow and BOS.`\n\n## Description\n\nThis package contains python implementations of uncertainty quantification (UQ) for Particle Image Velocimetry (PIV). Implements:\n\n* `pivuq.diparity.ilk`: Iterative Lucas-Kanade based disparity estimation. [[scikit-image](https://scikit-image.org/docs/dev/api/skimage.registration.html#skimage.registration.optical_flow_ilk)]\n* `pivuq.disparity.sws`: Python implementation of Sciacchitano, A., Wieneke, B., & Scarano, F. (2013). PIV uncertainty quantification by image matching. *Measurement Science and Technology, 24* (4). [https://doi.org/10.1088/0957-0233/24/4/045302](https://doi.org/10.1088/0957-0233/24/4/045302). [[piv.de](http://piv.de/uncertainty/)]\n\n\n## Installation\n\nInstall using pip\n\n```bash\npip install pivuq\n```\n',
    'author': 'MrLento234',
    'author_email': 'lento.manickathan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lento234/pivuq',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
