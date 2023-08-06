# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shinyutils']

package_data = \
{'': ['*']}

install_requires = \
['corgy>=4.1,<5.0']

extras_require = \
{':python_version < "3.9"': ['typing_extensions>=4.0,<5.0'],
 'colors': ['rich>=10.0,<11.0', 'crayons>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'shinyutils',
    'version': '12.4.0',
    'description': 'Personal collection of common utilities',
    'long_description': '# shinyutils\nVarious utilities for common tasks. :sparkles: :sparkles: :sparkles:\n\n## Setup\nInstall with `pip` (Python 3.7 or higher is required).\n\n```bash\npip install shinyutils  # basic install\npip install "shinyutils[colors]"  # install with color support\n```\n\n## Usage\nFor documentation on usage, refer to docs/index.md.\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jayanthkoushik/shinyutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
