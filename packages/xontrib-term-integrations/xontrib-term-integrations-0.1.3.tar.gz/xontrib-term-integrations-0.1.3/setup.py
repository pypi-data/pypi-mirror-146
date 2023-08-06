# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib', 'xontrib_term_integrations']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.12.0']

setup_kwargs = {
    'name': 'xontrib-term-integrations',
    'version': '0.1.3',
    'description': 'Support shell integration of terminal programs iTerm2, Kitty...',
    'long_description': '# Terminal Emulators integration\n[Shell integration](https://iterm2.com/documentation-escape-codes.html) for Xonsh.\n\nThe following terminal emulators are supported\n- [iTerm2](https://iterm2.com/documentation-shell-integration.html)\n- [kitty](https://sw.kovidgoyal.net/kitty/shell-integration/)\n\n**Note**: If identifying current terminal fails, `iTerm2` hooks are loaded.\n\nPRs welcome on improving the support to more terminal programs :)\n\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-term-integrations\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-term-integrations\n```\n\n**Note**: [This PR](https://github.com/xonsh/xonsh/pull/4629) is needed for this to work. As of today(Mar 3, 2022), it is not released yet. So you have to install xonsh from the github like `pipx install git+https://gitlab.com/xonsh/xonsh/`.\n\n## Usage\n\n``` bash\n# this modifies the $PROMPT function. So load it after setting $PROMPT if you have a custom value\nxontrib load term_integration\n```\n\n\n## Contributing\n\nPlease make sure that you\n* Document the purpose of functions and classes.\n* When adding a new feature, please mention it in the `README.md`. Use screenshots when applicable.\n* [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) style should be used\n  for commit messages as it is used to generate changelog.\n* Please use [pre-commit](https://pre-commit.com/) to run qa checks. Configure it with\n\n```sh\npre-commit install-hooks\n```\n',
    'author': 'Noortheen Raja NJ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-term-integrations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
