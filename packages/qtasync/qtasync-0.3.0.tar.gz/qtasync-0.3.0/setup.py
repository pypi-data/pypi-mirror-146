# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtasync',
 'qtasync.qasyncio',
 'qtasync.qconcurrent',
 'qtasync.qthreading',
 'qtasync.types']

package_data = \
{'': ['*']}

extras_require = \
{'PyQt5': ['PyQt5>=5.15.6,<6.0.0', 'PyQt5-stubs>=5.15.2,<6.0.0'],
 'PyQt6': ['PyQt6>=6.2.2,<7.0.0'],
 'PySide2': ['PySide2==5.15.2'],
 'PySide6': ['PySide6>=6.2.2,<7.0.0']}

setup_kwargs = {
    'name': 'qtasync',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Brian Cefali',
    'author_email': 'brian@atakama.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
