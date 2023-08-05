# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lamedec']

package_data = \
{'': ['*']}

install_requires = \
['lame-ctypes>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'lamedec',
    'version': '0.1.2',
    'description': '',
    'long_description': '# LAME MP3 decoding wrapper\n\n## Usage\n\n```python\nlamedec.decode(src, dst)\n```\n\n### Parameters\n\n_src_ Instance of io.RawIOBase (eg. FileIO, ByteIO ...).\n\n_dst_ Same parameter for wave module.\n\n## Sample\n\n```python\nimport io\nimport lamedec\n\n\nsrc = io.FileIO("src.mp3", "rb")\ndst = "dst.wav"\n\nlamedec.decode(src, dst)\n```\n\nSee [samples](https://github.com/sengokyu/python-lamedec/blob/main/samples).\n',
    'author': 'sengokyu',
    'author_email': 'sengokyu+gh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sengokyu/python-lamedec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
