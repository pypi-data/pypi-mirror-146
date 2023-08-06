# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh>=0.12']

setup_kwargs = {
    'name': 'xontrib-django',
    'version': '0.0.2',
    'description': 'Django auto-completions for Xonsh shell',
    'long_description': 'Django auto-completions for Xonsh shell\n\n\n## Installation\n\nTo install use pip:\n\n```bash\nxpip install xontrib-django\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-django\n```\n\n## Usage\n\n```bash\nxontrib load django\n```\n\n## Releasing your package\n\n- Bump the version of your package.\n- Create a GitHub release (The release notes are automatically generated as a draft release after each push).\n- And publish with `poetry publish --build` or `twine`\n',
    'author': 'Noortheen Raja',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
