# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web2dataset']

package_data = \
{'': ['*']}

install_requires = \
['docarray>=0.12.4,<0.13.0',
 'matplotlib>=3.5.1,<4.0.0',
 'rich>=12,<13',
 'selenium>=4.1.0,<5.0.0',
 'typer>=0.4.1,<0.5.0',
 'uuid>=1.30,<2.0']

extras_require = \
{'torch': ['torch>=1.11.0,<2.0.0', 'torchvision>=0.12.0,<0.13.0']}

entry_points = \
{'console_scripts': ['web2dataset = web2dataset.cli:cli']}

setup_kwargs = {
    'name': 'web2dataset',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sami jaghouar',
    'author_email': 'sami.jaghouar@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
