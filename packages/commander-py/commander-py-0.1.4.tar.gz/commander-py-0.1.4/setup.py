# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commander']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'commander-py',
    'version': '0.1.4',
    'description': 'A very simple tool to create beautiful console application.',
    'long_description': '# Commander\n\nA very simple tool to create beautiful console application.\n\n| Project       | Tabler                                       |\n|---------------|----------------------------------------------|\n| Author        | Özcan Yarımdünya                             |\n| Documentation | https://ozcanyarimdunya.github.io/commander/ |\n| Source code   | https://github.com/ozcanyarimdunya/commander |\n\n## Installation\n\n```shell\npip install commander-py\n```\n\n## Example\n\n![gif](docs/images/money.gif)\n\nFor more checkout [documentation.](https://ozcanyarimdunya.github.io/commander/)\n',
    'author': 'Özcan Yarımdünya',
    'author_email': 'ozcanyd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ozcanyarimdunya.github.io/commander/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
