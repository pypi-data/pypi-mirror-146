# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lame_ctypes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lame-ctypes',
    'version': '0.1.3',
    'description': 'Just Lame ctypes binding.',
    'long_description': '# Python Lame binding\n\n## Usage\n\n```python\nfrom lame_ctypes import *\n\nlame = lame_init()\n\nlame_close(lame, 1)\n```\n\nSee [sample](https://github.com/sengokyu/python-lame-ctypes/blob/main/samples/)\n\n## Important limitation\n\nCurrently, only decoding bindings are defined.\n',
    'author': 'sengokyu',
    'author_email': 'sengokyu+gh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sengokyu/python-lame-ctypes',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
