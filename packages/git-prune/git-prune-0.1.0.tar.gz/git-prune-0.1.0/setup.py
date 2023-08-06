# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_prune']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9']

entry_points = \
{'console_scripts': ['git-prune = git_prune.main:cli']}

setup_kwargs = {
    'name': 'git-prune',
    'version': '0.1.0',
    'description': 'Clean up your local git branches to match the remote with one command.',
    'long_description': '# git-prune\n\n![build](https://img.shields.io/circleci/build/github/rsoper/git-prune/master?token=6eec49c405bc17c010e3bb14218aacef23ccee8a)\n![git-prune-ver](https://img.shields.io/pypi/v/git-prune)\n![pythonver](https://img.shields.io/badge/python-3.8%2B-blue.svg)\n![license](https://img.shields.io/github/license/mashape/apistatus.svg)\n\n\nClean up your local git branches to match the remote with one command. This tool checks your remote location for current branches, compares this list against the local git branches, and gives you the option to remove all orphaned local branches.\n\n### Installation\n\n`pip3 install git-prune`\n\n### Usage\n\n`git-prune` -- Prunes local branches in the current working directory.\n\n`git-prune -d /Path/to/repository` -- Prunes local branches in the provided directory.\n',
    'author': 'Richard Soper',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rsoper/git-prune',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
