# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-mpl',
    'version': '0.0.2',
    'description': "Matplotlib hooks for xonsh, including the new 'mpl' alias that displays the current figure on the screen",
    'long_description': '<p align="center">\nMatplotlib hooks for xonsh, including the new \'mpl\' alias that displays the current figure on the screen\n</p>\n\n<p align="center">  \nIf you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/xonsh/xontrib-mpl" target="_blank">tweet</a>.\n</p>\n\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-mpl\n# or: xpip install -U git+https://github.com/xonsh/xontrib-mpl\n```\n\n## Usage\n\n```bash\nxontrib load mpl\n# TODO: what\'s next?\n```\n\n## Examples\n\n...\n\n## Known issues\n\n...\n\n## Releasing your package\n\n- Bump the version of your package.\n- Create a GitHub release (The release notes are automatically generated as a draft release after each push).\n- And publish with `poetry publish --build` or `twine`\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raa',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xonsh/xontrib-mpl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
