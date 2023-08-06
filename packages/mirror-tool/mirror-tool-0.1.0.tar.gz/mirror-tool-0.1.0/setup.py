# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirror_tool']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.17.21']

entry_points = \
{'console_scripts': ['mirror-tool = mirror_tool.cmd:entrypoint']}

setup_kwargs = {
    'name': 'mirror-tool',
    'version': '0.1.0',
    'description': 'A tool for managing git mirrors.',
    'long_description': None,
    'author': 'Rohan McGovern',
    'author_email': 'rohan@mcgovern.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
