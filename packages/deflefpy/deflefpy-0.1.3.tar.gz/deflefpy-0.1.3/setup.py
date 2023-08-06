# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deflefpy']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'deflefpy',
    'version': '0.1.3',
    'description': 'A DEF/LEF (Library Exchange Format) file parser written in Python.',
    'long_description': None,
    'author': 'dasdias',
    'author_email': 'das.dias6@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/das-dias/deflefpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
