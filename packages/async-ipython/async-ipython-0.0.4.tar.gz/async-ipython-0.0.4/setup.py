# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aipython']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['aipython = aipython.__main__:run']}

setup_kwargs = {
    'name': 'async-ipython',
    'version': '0.0.4',
    'description': 'An enhanced async interactive python.',
    'long_description': '# aipython\n\nAn enhanced Python shell with IPython-like features.\n\n## Features\n\n[x] **Autocompletion**\n[x] **History**\n[x] **Magic commands**\n\n### Installation\n\n```bash\npip install aipython\n```\n\n### Usage\n\n```shell\n$ aipython\n```\n\n## License\n\nThis project was distributed under the [MPL-2.0 License](LICENSE).\n',
    'author': 'Alex Hutz',
    'author_email': 'frostiiweeb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FrostiiWeeb/aipython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
