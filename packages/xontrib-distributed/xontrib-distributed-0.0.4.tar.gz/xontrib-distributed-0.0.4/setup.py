# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['distributed>=2022.3.0', 'xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-distributed',
    'version': '0.0.4',
    'description': 'The distributed parallel computing library hooks for xonsh',
    'long_description': '<p align="center">  \nThe <a href="https://pypi.org/project/distributed/">distributed</a> parallel computing library hooks for xonsh\n<br><br>\nIf you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/xonsh/xontrib-distributed" target="_blank">tweet</a>.\n</p>\n\n\nImportantly this provides a substitute \'dworker\' command\nwhich enables distributed workers to have access to xonsh builtins.\n\nFurthermore, this xontrib adds a \'DSubmitter\' context manager\nfor executing a block remotely.\nMoreover, this also adds a convenience function \'dsubmit()\'\nfor creating DSubmitter and Executor instances at the same time.\n\nThus users may submit distributed jobs with::\n\n```pycon\nwith dsubmit(\'127.0.0.1:8786\', rtn=\'x\') as dsub:\n    x = $(echo I am elsewhere)\nres = dsub.future.result()\nprint(res)\n```\n\nThis is useful for long running or non-blocking jobs.\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-distributed\n# or: xpip install -U git+https://github.com/xonsh/xontrib-distributed\n```\n\n## Usage\n\n```bash\nxontrib load distributed\n# TODO: what\'s next?\n```\n\n## Releasing your package\n\n- Bump the version of your package.\n- Create a GitHub release (The release notes are automatically generated as a draft release after each push).\n- And publish with `poetry publish --build` or `twine`\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).\n\n',
    'author': 'Xonsh Dev',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xonsh/xontrib-distributed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
