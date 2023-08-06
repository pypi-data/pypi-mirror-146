# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_pp']

package_data = \
{'': ['*']}

install_requires = \
['loguru[loguru]>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['git-pp = git_pp.git_pp:main_sync']}

setup_kwargs = {
    'name': 'git-pp',
    'version': '1.5.3',
    'description': 'Git utility for auto-committing and concurrent pushing',
    'long_description': '# git pp\n\nGit utility for auto-committing and concurrent pushing.\n\nPowered by `asyncio`, with no dependency besides `python>=3.10` and `git`.\n\n## Features\n- Auto-stages and commits with custom or generated commit messages\n- Pushes to multiple or all remotes of a git repository concurrently with `asyncio`\n- Operates on any number of git repositories at the same time\n\n## Demo\n\n<!-- [![asciicast](https://asciinema.org/a/487579.png)](https://asciinema.org/a/487579) -->\n<a href="https://asciinema.org/a/487579"><img src="https://asciinema.org/a/487579.png" alt="asciicast" style="width:500px;height:300px;"></a>\n\n\nIn this demo, git pp did the following in \\~/config and \\~/gui repos:\n\n- (Concurrently) Auto staged all changes and commits with ISO-8601 timestamps as commit messages;\n- (Concurrently) Pushed the changes in the checked out branch to all of their remotes, in this case, they’re origin and lab.\n\n## Installation\n\nFirst make sure the `git` executable is installed and in your `$PATH`.\n\nNote that non-UNIX systems are not officially supported.\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install git-pp\n```\n\n### [pip](https://pypi.org/project/git-pp/)\n```\n$ pip install git-pp\n```\n\n### [AUR](https://aur.archlinux.org/packages/python-git-pp)\nFor Archlinux.\n```\n$ yay -S python-git-pp\n```\n\n\n## Usage\n\nYou can either invoke this tool with `git-pp` or `git pp`,\n`--help` is unsupported when using the latter.\n\n```\n$ git pp -h\nusage: git pp [-h] [-m COMMIT_MESSAGE] [-v] [-so] [-p] [-po] [-r REMOTE [REMOTE ...]] [-b BRANCH] [-f] [-t TIMEOUT] [DIRS ...]\n\nGit utility for auto-committing and concurrent pushing\n\npositional arguments:\n  DIRS                  Dirs to operate on (default: [\'.\'])\n\noptions:\n  -h, --help            show this help message and exit\n  -m COMMIT_MESSAGE, --commit-message COMMIT_MESSAGE\n                        commit message (default: None)\n  -v, --version         show program\'s version number and exit\n  -so, --status-only    Prints status only (default: False)\n  -p, --push            Push to all remotes (default: False)\n  -po, --push-only      Push to all remotes, without pre_pull (default: False)\n  -r REMOTE [REMOTE ...], --remote REMOTE [REMOTE ...]\n                        Remote name (default: None)\n  -b BRANCH, --branch BRANCH\n                        Branch name (default: None)\n  -f, --force           Force push (default: False)\n  -t TIMEOUT, --timeout TIMEOUT\n                        Timeout for a single push (default: None)\n```\n\n## Develop\n```\n$ git clone https://github.com/tddschn/git-pp.git\n$ cd git-pp\n$ poetry install\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/git-pp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
