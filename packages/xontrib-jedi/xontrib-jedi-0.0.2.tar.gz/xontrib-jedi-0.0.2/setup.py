# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['jedi>=0.18.1', 'xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-jedi',
    'version': '0.0.2',
    'description': "Improved Xonsh's Python completions using jedi",
    'long_description': '<p align="center">\nXonsh Python completions using <a href="https://jedi.readthedocs.io/en/latest/">jedi</a>.\n</p>\n\n<p align="center">  \nIf you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/xonsh/xontrib-jedi" target="_blank">tweet</a>.\n</p>\n\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-jedi\n# or: xpip install -U git+https://github.com/xonsh/xontrib-jedi\n```\n\n## Usage\n\n```bash\nxontrib load jedi\n# TODO: what\'s next?\n```\n\n## Examples\n\n...\n\n## Known issues\n\n...\n\n## Releasing your package\n\n- Bump the version of your package.\n- Create a GitHub release (The release notes are automatically generated as a draft release after each push).\n- And publish with `poetry publish --build` or `twine`\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).\n',
    'author': 'Xonsh Dev',
    'author_email': 'xonsh@email.address',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xonsh/xontrib-jedi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
