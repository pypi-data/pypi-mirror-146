# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scarfs']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.55.1,<0.56.0', 'numpy>=1.18,<1.22']

setup_kwargs = {
    'name': 'scarfs',
    'version': '0.1.1',
    'description': 'find approximate fixed points of bounded vector valued functions',
    'long_description': 'Scarfs\n======\n[![pypi](https://img.shields.io/pypi/v/scarfs)](https://pypi.org/project/scarfs/)\n[![build](https://github.com/erikbrinkman/scarfs/actions/workflows/build.yml/badge.svg)](https://github.com/erikbrinkman/scarfs/actions/workflows/build.yml)\n\nA library to find an approximate fixed point for a for a bounded vector valued\nfunction.\n\nInstallation\n------------\n```bash\npip install scarfs\n```\n\nUsage\n-----\n\nDefine the function you want to find a fixed point of using numba:\n```python\nfrom numba import njit\n\n@njit\ndef roll(simp: np.ndarray) -> np.ndarray:\n    return np.roll(simp, 1)\n```\nFor performance reasons, this function must be compiled by numba as a cfunc or\nin nopython mode. Jitclass functions are currently not supported. The function\nmust also lie in a bounded space, three default spaces are provided: the\nsimplex, the simplotope, and the unit hypercube. If your bounded space is not\none of these, you\'ll need to first compute a homeomorphism between your space\nand one of these. The main algorithm runs on the simplex, so you may find it\nfaster if you can project there directly.\n\nOnce your function is defined, simply call one of the fixed point functions\nwith an initial position and a discretization:\n```python\nfrom scarfs import simplex_fixed_point\n\nsol = simplex_fixed_point(roll, np.array([1, 0, 0, 0], float), 100)\n```\nThe result is guaranteed to be within `1 / discretization` of a true fixed\npoint (or a little larger for the other bounded spaces).\n\nNote that fixed points are difficult to approximate generally, so this may run\nfor a very long time.\n\nAlso note that this library "trusts" you, so if you pass in invalid inputs, you\nmay get arcane errors.\n',
    'author': 'Erik Brinkman',
    'author_email': 'erik.brinkman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
