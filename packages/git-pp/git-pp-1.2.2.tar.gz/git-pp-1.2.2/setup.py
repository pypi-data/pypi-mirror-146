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
    'version': '1.2.2',
    'description': 'Git utility for auto-committing and concurrent pushing',
    'long_description': "## Usage:\n```\n$ git pp -h\nusage: git pp [-h] [-m COMMIT_MESSAGE] [-v] [-so] [-p] [-po] [-r REMOTE [REMOTE ...]] [-b BRANCH] [-f] [-t TIMEOUT] [DIRS ...]\n\nGit utility for auto-committing and concurrent pushing\n\npositional arguments:\n  DIRS                  Dirs to operate on (default: ['.'])\n\noptions:\n  -h, --help            show this help message and exit\n  -m COMMIT_MESSAGE, --commit-message COMMIT_MESSAGE\n                        commit message (default: None)\n  -v, --version         show program's version number and exit\n  -so, --status-only    Prints status only (default: False)\n  -p, --push            Push to all remotes (default: False)\n  -po, --push-only      Push to all remotes, without pre_pull (default: False)\n  -r REMOTE [REMOTE ...], --remote REMOTE [REMOTE ...]\n                        Remote name (default: None)\n  -b BRANCH, --branch BRANCH\n                        Branch name (default: None)\n  -f, --force           Force push (default: False)\n  -t TIMEOUT, --timeout TIMEOUT\n                        Timeout for a single push (default: None)\n```",
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
