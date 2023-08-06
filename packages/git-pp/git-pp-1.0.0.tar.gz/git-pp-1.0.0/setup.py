# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_pp']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['git-pp = git_pp.git_pp:main_sync']}

setup_kwargs = {
    'name': 'git-pp',
    'version': '1.0.0',
    'description': 'Git utility for auto-commiting and concurrent pushing',
    'long_description': None,
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
