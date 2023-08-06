# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['constcheck']

package_data = \
{'': ['*']}

install_requires = \
['lsfiles>=0.1.1,<0.2.0',
 'object-colors>=2.0.1,<3.0.0',
 'pathlib3x>=1.3.9,<2.0.0']

entry_points = \
{'console_scripts': ['constcheck = constcheck.__main__:main']}

setup_kwargs = {
    'name': 'constcheck',
    'version': '0.1.0',
    'description': 'Check Python files for repeat use of strings',
    'long_description': 'constcheck\n==========\n.. image:: https://github.com/jshwi/constcheck/workflows/ci/badge.svg\n    :target: https://github.com/jshwi/constcheck/workflows/ci/badge.svg\n    :alt: ci\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/constcheck\n    :target: https://img.shields.io/pypi/v/constcheck\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/constcheck/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/constcheck\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nCheck Python files for repeat use of strings\n\n**Installation**\n\n.. code-block:: console\n\n    $ pip install constcheck\n..\n\n**Usage**\n\n    usage: constcheck [-h] [-f] [-n] [-v] [-c INT] [-l INT] [-p PATH] [-s STR]\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -f, --filter          filter out empty results\n      -n, --no-color        disable color output\n      -v, --version         show version and exit\n      -c INT, --count INT   minimum number of repeat strings\n      -l INT, --len INT     minimum length of repeat strings\n      -p PATH, --path PATH  path to check files for\n      -s STR, --string STR  parse a string instead of a file\n\nconstcheck will display the quantity of strings repeated for the:\n    - path\n    - each dir\n    - individual files\n\nThe default length of strings to check for is 3\n\nThe default quantity of strings to check for repeats is also 3\n\n.. code-block:: python\n\n    >>> EXAMPLE = (\n    ...     \'STRING_1 = "Hey"\'\n    ...     \'STRING_2 = "Hey"\'\n    ...     \'STRING_3 = "Hey"\'\n    ...     \'STRING_4 = "Hello"\'\n    ...     \'STRING_5 = "Hello"\'\n    ...     \'STRING_6 = "Hello"\'\n    ...     \'STRING_7 = "Hello"\'\n    ...     \'STRING_8 = "Hello, world!"\'\n    ...     \'STRING_9 = "Hello, world!"\'\n    ...     \'STRING_10 = "Hello, world!"\'\n    ...     \'STRING_11 = "Hello, world!"\'\n    ...     \'STRING_12 = "Hello, world!"\'\n    ... )\n    >>>\n    >>> import constcheck\n    >>> constcheck.main(string=EXAMPLE, no_color=True)\n    "3   | Hey"\n    "4   | Hello"\n    "5   | Hello, world!"\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
