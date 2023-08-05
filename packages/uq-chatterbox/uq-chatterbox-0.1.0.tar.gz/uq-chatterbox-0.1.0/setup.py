# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chatterbox']

package_data = \
{'': ['*']}

install_requires = \
['TTS>=0.6.1,<0.7.0', 'click>=8.1.2,<9.0.0']

entry_points = \
{'console_scripts': ['chatterbox = chatterbox.__main__:cli']}

setup_kwargs = {
    'name': 'uq-chatterbox',
    'version': '0.1.0',
    'description': "A command-line text-to-speech utility for UQ's Software Architecture students to deploy as a scalable service.",
    'long_description': None,
    'author': 'Evan Hughes',
    'author_email': 'ehugh1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
