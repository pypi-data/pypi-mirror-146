# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spec2json', 'spec2json.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'click>=8.1.2,<9.0.0',
 'html5lib>=1.1,<2.0',
 'httpx>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['spec2json = spec2json.cli:main']}

setup_kwargs = {
    'name': 'spec2json',
    'version': '0.1.0',
    'description': 'Extract section metadata and algorithm steps from specification HTML documents as JSON.',
    'long_description': '# spec2json\n\n> Extract section metadata and algorithm steps from specification HTML documents\n> as JSON.\n\n[![PyPI](https://img.shields.io/pypi/v/spec2json)](https://pypi.org/project/spec2json/)\n![Python Version](https://img.shields.io/pypi/pyversions/spec2json)\n[![License](https://img.shields.io/github/license/linusg/spec2json?color=d63e97)](https://github.com/linusg/spec2json/blob/main/LICENSE)\n[![Black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/ambv/black)\n\n## Installation\n\nInstall from PyPI:\n\n```console\npip3 install spec2json\n```\n\n## Usage\n\nSee `spec2json --help`.\n\nExample:\n\n```console\nspec2json --numbered https://tc39.es/ecma262/ https://tc39.es/ecma402/ > ecmascript.json\n```\n\n## Supported formats\n\n- [Bikeshed](https://tabatkins.github.io/bikeshed/) (various Web specs),\n- [Ecmarkup](https://tc39.es/ecmarkup/) (ECMAScript)\n- [Wattsi](https://github.com/whatwg/wattsi) (HTML standard)\n',
    'author': 'Linus Groh',
    'author_email': 'mail@linusgroh.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linusg/spec2json',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
