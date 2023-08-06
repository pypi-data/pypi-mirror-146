# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xonsh_jupyter', 'xontrib']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0', 'xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-jupyter-shell',
    'version': '0.0.2',
    'description': 'A shell for the Jupyter kernel.',
    'long_description': '<p align="center">\nXonsh provides a kernel for Jupyter Notebook and Lab so you can execute\nxonsh commands in a notebook cell without any additional magic.\n</p>\n\n<p align="center">  \nIf you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/xonsh/xontrib-jupyter-shell" target="_blank">tweet</a>.\n</p>\n\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-jupyter-shell\n# or: xpip install -U git+https://github.com/xonsh/xontrib-jupyter-shell\n```\n\n## Usage\n\n```bash\n$ xontrib load jupyter\n$ xonfig jupyter-kernel\nInstalling Jupyter kernel spec:\n  root: None\n  prefix: <env_prefix>\n  as user: False\n```\n\n`<env_prefix>` is the path prefix of the Jupyter and Xonsh\nenvironment. `xonfig jupyter-kernel --help` shows options for installing\nthe kernel spec in the user config folder or in a non-standard\nenvironment prefix.\n\nYou can confirm the status of the installation:\n\n``` xonshcon\n$ xonfig info\n+------------------+-----------------------------------------------------+\n| xonsh            | 0.9.21                                              |\n| Git SHA          | d42b4140                                            |\n\n               . . . . .\n\n| on jupyter       | True                                                |\n| jupyter kernel   | <env_prefix>\\share\\jupyter\\kernels\\xonsh            |\n+------------------+-----------------------------------------------------+\n```\n\nOr:\n\n``` xonshcon\n$ jupyter kernelspec list\nAvailable kernels:\n  python3    <env_prefix>\\share\\jupyter\\kernels\\python3\n  xonsh      <env_prefix>\\share\\jupyter\\kernels\\xonsh\n```\n\n## Releasing your package\n\n- Bump the version of your package.\n- Create a GitHub release (The release notes are automatically generated as a draft release after each push).\n- And publish with `poetry publish --build` or `twine`\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).\n',
    'author': 'Xonsh Dev',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xonsh/xontrib-jupyter-shell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
