# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['st_bridge']

package_data = \
{'': ['*'],
 'st_bridge': ['bridge/.gitignore',
               'bridge/.gitignore',
               'bridge/.gitignore',
               'bridge/.gitignore',
               'bridge/package-lock.json',
               'bridge/package-lock.json',
               'bridge/package-lock.json',
               'bridge/package-lock.json',
               'bridge/package.json',
               'bridge/package.json',
               'bridge/package.json',
               'bridge/package.json',
               'bridge/public/*',
               'bridge/src/*',
               'bridge/tsconfig.json',
               'bridge/tsconfig.json',
               'bridge/tsconfig.json',
               'bridge/tsconfig.json',
               'html/.gitignore',
               'html/.gitignore',
               'html/.gitignore',
               'html/.gitignore',
               'html/package-lock.json',
               'html/package-lock.json',
               'html/package-lock.json',
               'html/package-lock.json',
               'html/package.json',
               'html/package.json',
               'html/package.json',
               'html/package.json',
               'html/public/*',
               'html/src/*',
               'html/tsconfig.json',
               'html/tsconfig.json',
               'html/tsconfig.json',
               'html/tsconfig.json']}

install_requires = \
['orjson>=3.0.0,<4.0.0', 'streamlit>=0.63']

setup_kwargs = {
    'name': 'streamlit-bridge',
    'version': '1.0.0',
    'description': 'A hidden streamlit component that allows client side (javascript) to trigger events on the server side (python) and vice versa',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
