# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umigap']

package_data = \
{'': ['*']}

install_requires = \
['bvh>=0.3,<0.4',
 'dataclasses-json>=0.5.7,<0.6.0',
 'future-fstrings>=1.2.0,<2.0.0',
 'mathutils>=2.81.2,<3.0.0',
 'pygltflib>=1.15.1,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'simple-term-menu>=1.4.1,<2.0.0',
 'typer>=0.4.1,<0.5.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib-metadata>=4.11.3,<5.0.0'],
 ':python_version >= "3.8"': ['importlib>=1.0.4,<2.0.0']}

entry_points = \
{'console_scripts': ['umigap = umigap.cli:app']}

setup_kwargs = {
    'name': 'umigap',
    'version': '0.1.1',
    'description': 'umigap is an art-as-code tool for describing and managing 3D assets from autorigging to mocap in an indie game asset pipeline',
    'long_description': None,
    'author': 'Luke Miller',
    'author_email': 'dodgyville@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
