# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['taskwarrior_syncall',
 'taskwarrior_syncall.google',
 'taskwarrior_syncall.scripts']

package_data = \
{'': ['*'], 'taskwarrior_syncall': ['res/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'bidict>=0.21.2,<0.22.0',
 'bubop==0.1.6a',
 'click>=8.0,<9.0',
 'item-synchronizer==1.1.2',
 'loguru>=0.5.3,<0.6.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2021.1,<2022.0',
 'rfc3339>=6.2,<7.0',
 'taskw>=1.3.1,<2.0.0',
 'tqdm>=4.61.2,<5.0.0',
 'typing>=3.7.4,<4.0.0']

extras_require = \
{'gkeep': ['gkeepapi>=0.13.7,<0.14.0'],
 'google': ['google-api-python-client>=2.1.0,<3.0.0',
            'google-auth-oauthlib>=0.4.4,<0.5.0'],
 'notion': ['notion-client>=0.7.1,<0.8.0']}

entry_points = \
{'console_scripts': ['tw_gcal_sync = '
                     'taskwarrior_syncall.scripts.tw_gcal_sync:main',
                     'tw_gkeep_sync = '
                     'taskwarrior_syncall.scripts.tw_gkeep_sync:main',
                     'tw_notion_sync = '
                     'taskwarrior_syncall.scripts.tw_notion_sync:main']}

setup_kwargs = {
    'name': 'taskwarrior-syncall',
    'version': '1.2.0b2',
    'description': 'Taskwarrior <-> * bi-directional synchronization tool',
    'long_description': '# taskwarrior-syncall\n\n<p align="center">\n  <img src="https://github.com/bergercookie/taskwarrior-syncall/blob/devel/misc/meme.png"/>\n</p>\n\n<table>\n  <td>master</td>\n  <td>\n    <a href="https://github.com/bergercookie/taskwarrior-syncall/actions" alt="master">\n    <img src="https://github.com/bergercookie/taskwarrior-syncall/actions/workflows/ci.yml/badge.svg" /></a>\n  </td>\n  <td>devel</td>\n  <td>\n    <a href="https://github.com/bergercookie/taskwarrior-syncall/actions" alt="devel">\n    <img src="https://github.com/bergercookie/taskwarrior-syncall/actions/workflows/ci.yml/badge.svg?branch=devel" /></a>\n  </td>\n</table>\n\n<a href=\'https://coveralls.io/github/bergercookie/taskwarrior-syncall?branch=master\'>\n<img src=\'https://coveralls.io/repos/github/bergercookie/taskwarrior-syncall/badge.svg?branch=master\' alt=\'Coverage Status\' /></a>\n<a href="https://github.com/pre-commit/pre-commit">\n<img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit"></a>\n<a href="https://github.com/bergercookie/taskwarrior-syncall/blob/master/LICENSE" alt="LICENSE">\n<img src="https://img.shields.io/github/license/bergercookie/taskwarrior-syncall.svg" /></a>\n<a href="https://pypi.org/project/takwarrior-syncall" alt="pypi">\n<img src="https://img.shields.io/pypi/pyversions/taskwarrior-syncall.svg" /></a>\n<a href="https://badge.fury.io/py/taskwarrior-syncall">\n<img src="https://badge.fury.io/py/taskwarrior-syncall.svg" alt="PyPI version" height="18"></a>\n<a href="https://pepy.tech/project/taskwarrior-syncall">\n<img alt="Downloads" src="https://pepy.tech/badge/taskwarrior-syncall"></a>\n<a href="https://github.com/psf/black">\n<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n\n## Description\n\n`taskwarrior-syncall` is your one-stop software to synchronize a variety of\nservices with taskwarrior - in a bi-directional manner. Each synchronization\ncomes with one executable which handles the synchronization between that\nparticular service and taskwarrior.\n\nAt the moment the list of services supported is a bit limited but keeps growing\nby the day:\n\n- [[readme-gcal](https://github.com/bergercookie/taskwarrior-syncall/blob/devel/readme-gcal.md)] Taskwarrior ⬄ [Google Calendar](https://calendar.google.com/) Synchronization, via `tw_gcal_sync`\n- [[readme-notion](https://github.com/bergercookie/taskwarrior-syncall/blob/devel/readme-notion.md)] Taskwarrior ⬄ [Notion](https://notion.so) Synchronization, via `tw_notion_sync`\n- [ONGOING] [[readme-clickup](https://github.com/bergercookie/taskwarrior-syncall/blob/devel/readme-clickup.md)] Taskwarrior ⬄ [ClickUp](https://clickup.com) Synchronization, via `tw_clickup_sync`\n\nOverall, each of the above should support _bi-directional_ synchronization between\nTaskwarrior and the service of your preference. This means that on an\naddition, modification, deletion etc. of an item on one side, a corresponding\naddition, modification or deletion of a counterpart item will occur on the other\nside so that the two sides are eventually in sync. This should work\nbi-directionally, meaning an item created, modified, or deleted from a service\nshould also be created, modified, or deleted respectively in Taskwarrior and\nvice-versa.\n\nRefer to the corresponding README for the list above for instructions specific\nto the synchronization with that particular service. Before jumping to that\nREADME though, please complete the installation instructions below.\n\n## Installation instructions\n\nRequirements:\n\n- Taskwarrior - [Installation instructions](https://taskwarrior.org/download/) -\n  Tested with `2.6.1`, should work with `>=2.6`.\n- Python version >= `3.8`\n\nInstallation Options:\n\nYou have to specify at least one extra to do so use the `[]` syntax in pip:\n\n```sh\n# for installing integration with google (e.g. Google Keep / Calendar) and notion\npip3 install taskwarrior-syncall[notion,google]\n```\n\n- Pypi (may not contain latest version): `pip3 install --user --upgrade taskwarrior-syncall[notion,google]`\n- Github: `pip3 install --user git+https://github.com/bergercookie/taskwarrior-syncall`\n- Download and install `devel` branch locally - bleeding edge\n\n  ```sh\n  git clone https://github.com/bergercookie/taskwarrior-syncall\n  cd taskwarrior-syncall\n  git checkout devel\n  pip3 install --user --upgrade .\n  ```\n\n- Setup using [poetry](https://python-poetry.org/) - handy for local\n  development and for isolation of dependencies:\n\n  ```sh\n  git clone https://github.com/bergercookie/taskwarrior-syncall\n  poetry install\n  # get an interactive shell\n  poetry shell\n\n  # now the executables of all the services should be in your PATH for the\n  # current shell and you can also edit the source code without further\n  # re-installation ...\n  ```\n\n## Mechanics / Automatic synchronization\n\nTo achieve synchronization across taskwarrior and a service at hand, we use a\npush-pull mechanism which is far easier and less troublesome than an automatic\nsynchronization solution. In case the latter behavior is desired, users may just\nrun the script periodically e.g., using cron:\n\n```sh\ncrontab -e\n...\n\n# Add the following to sync every 10\' - modify the arguments according to your\n# preferences and according to the instructions of the corresponding executable\n# for example for `tw_gcal_sync`:\n#\n# See output and potential errors in your system logs (e.g., `/var/log/syslog`)\n*/10 * * * * tw_gcal_sync -c "TW Reminders" -t "remindme"\n```\n\n## Self Promotion\n\nIf you find this tool useful, please [star it on\nGithub](https://github.com/bergercookie/taskwarrior-syncall)\n\n## TODO List\n\nSee [ISSUES list](https://github.com/bergercookie/taskwarrior-syncall/issues) for\nthe things that I\'m currently either working on or interested in implementing in\nthe near future. In case there\'s something you are interesting in working on,\ndon\'t hesitate to either ask for clarifications or just do it and directly make\na PR.\n',
    'author': 'Nikos Koukis',
    'author_email': 'nickkouk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bergercookie/taskwarrior_syncall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
