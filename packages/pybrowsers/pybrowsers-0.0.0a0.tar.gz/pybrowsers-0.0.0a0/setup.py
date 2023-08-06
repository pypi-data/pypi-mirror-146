# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['browsers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybrowsers',
    'version': '0.0.0a0',
    'description': 'Python library for detecting and launching browsers',
    'long_description': '<table>\n    <tr>\n        <td>License</td>\n        <td><img src=\'https://img.shields.io/pypi/l/pybrowsers.svg?style=for-the-badge\' alt="License"></td>\n        <td>Version</td>\n        <td><img src=\'https://img.shields.io/pypi/v/pybrowsers.svg?logo=pypi&style=for-the-badge\' alt="Version"></td>\n    </tr>\n    <tr>\n        <td>Github Actions</td>\n        <td><img src=\'https://img.shields.io/github/workflow/status/roniemartinez/pybrowsers/Python?label=actions&logo=github%20actions&style=for-the-badge\' alt="Github Actions"></td>\n        <td>Coverage</td>\n        <td><img src=\'https://img.shields.io/codecov/c/github/roniemartinez/pybrowsers/branch?label=codecov&logo=codecov&style=for-the-badge\' alt="CodeCov"></td>\n    </tr>\n    <tr>\n        <td>Supported versions</td>\n        <td><img src=\'https://img.shields.io/pypi/pyversions/pybrowsers.svg?logo=python&style=for-the-badge\' alt="Python Versions"></td>\n        <td>Wheel</td>\n        <td><img src=\'https://img.shields.io/pypi/wheel/pybrowsers.svg?style=for-the-badge\' alt="Wheel"></td>\n    </tr>\n    <tr>\n        <td>Status</td>\n        <td><img src=\'https://img.shields.io/pypi/status/pybrowsers.svg?style=for-the-badge\' alt="Status"></td>\n        <td>Downloads</td>\n        <td><img src=\'https://img.shields.io/pypi/dm/pybrowsers.svg?style=for-the-badge\' alt="Downloads"></td>\n    </tr>\n</table>\n\n# browsers\n\nPython library for detecting and launching browsers\n\n> I recently wrote a snippet for detecting installed browsers in an OSX machine in \n> https://github.com/mitmproxy/mitmproxy/issues/5247#issuecomment-1095337723 based on https://github.com/httptoolkit/browser-launcher\n> and I thought this could be useful to other devs since I cannot seem to find an equivalent library in Python\n\n## Installation\n\n```bash\npip install pybrowsers\n```\n\n## Usage\n\n### Python\n\n```python\nimport browsers\n\nbrowser = browsers.get("chrome")\n```\n\n## TODO:\n\n- [x] Detect browser on OSX\n- [ ] Detect browser on Linux/Unix\n- [ ] Detect browser on Windows\n- [ ] Launch browser with arguments\n- [ ] Get browser by version (support wildcards)\n\n## Author\n\n- [Ronie Martinez](mailto:ronmarti18@gmail.com)\n',
    'author': 'Ronie Martinez',
    'author_email': 'ronmarti18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roniemartinez/browsers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
