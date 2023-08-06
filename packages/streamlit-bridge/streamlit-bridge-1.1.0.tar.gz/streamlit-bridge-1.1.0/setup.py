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
               'bridge/build/*',
               'bridge/build/static/js/*',
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
               'html/build/*',
               'html/build/static/js/*',
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
    'version': '1.1.0',
    'description': 'A hidden streamlit component that allows client side (javascript) to trigger events on the server side (python) and vice versa',
    'long_description': '<h1 align="center">Streamlit Bridge</h1>\n\n<div align="center">\n    Two <a href="https://streamlit.io/">Streamlit</a> components that allow client side (javascript) to send data to the server side (python) and render HTML content without being processed by Markdown.\n\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\n</div>\n\n## Introduction\n\nThese two components offer more flexibility in creating Streamlit applications by allowing you to easily incorporate HTML and JS.\n\nHere are some examples:\n\n1. [List of inline buttons](/examples/inline_buttons.py) ![Streamlit inline buttons](/examples/inline_buttons.gif)\n\n   ```python\n   import streamlit as st\n   from st_bridge import bridge, html\n\n   data = bridge("my-bridge", default="no button is clicked")\n\n   html("""\n   <button onClick="stBridges.send(\'my-bridge\', \'button 1 is clicked\')">Button 1</button>\n   <button onClick="stBridges.send(\'my-bridge\', \'button 2 is clicked\')">Button 2</button>\n   <button onClick="stBridges.send(\'my-bridge\', \'button 3 is clicked\')">Button 3</button>\n   """)\n\n   st.write(data)\n   ```\n\n### Installation\n\n```bash\npip install streamlit-bridge\n```\n\n### API\n\nBridge Component\n\n```python\ndef bridge(\n    name: str,\n    default: Optional[Any] = None,\n    key: Optional[str] = None,\n):\n    """Create a new instance of "Streamlit Bridge", allowing call from the client to\n    the server.\n\n    Everytime JS client send data to the server, streamlit will trigger a rerun and the data\n    is returned by this function.\n\n    Args:\n        name: unique name of the bridge to identify the bridge Javascript\'s call will send data to\n        default: the initial return value of the component before the user has interacted with it.\n        key: streamlit component\'s id\n    """\n```\n\nTo send data from the client to a corresponding bridge component with `<bridge-name>`, use the function: `window.stBridges.send(<bridge-name>, <data>);` or `window.parent.stBridges.send(<bridge-name>, <data>);` if you are running it inside an component (i.e., running inside an iframe).\n\nHTML Component\n\n```python\ndef html(html: str, iframe: bool = False, key: Optional[str]=None) -> None:\n    """Render HTML in Streamlit without being processed by Markdown.\n\n    Args:\n        html: HTML to render\n        iframe: whether to render the HTML in an iframe or in the main document.\n                By default streamlit component is rendered inside an iframe, so by\n                setting it to false, we allow the HTML to rendered in the main document.\n        key: streamlit component\'s id\n    """\n    pass\n```\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/binh-vu/streamlit-bridge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
