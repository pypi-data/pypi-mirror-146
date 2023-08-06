# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['char_picture']

package_data = \
{'': ['*']}

install_requires = \
['cowpy>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'char-picture',
    'version': '0.1.3',
    'description': 'generate char picture demo',
    'long_description': '# this is in readme.rst\n## this my first project.',
    'author': 'winfred_wu',
    'author_email': '869286203@qq.com',
    'maintainer': 'm1',
    'maintainer_email': '869286203@qq.com',
    'url': 'http://www.qudoor.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
