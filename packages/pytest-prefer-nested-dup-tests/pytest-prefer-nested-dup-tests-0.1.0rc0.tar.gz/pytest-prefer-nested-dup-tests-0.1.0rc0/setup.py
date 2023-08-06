# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_prefer_nested_dup_tests']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.1,<8.0.0']

entry_points = \
{'pytest11': ['prefer-nested-dup-tests = pytest_prefer_nested_dup_tests']}

setup_kwargs = {
    'name': 'pytest-prefer-nested-dup-tests',
    'version': '0.1.0rc0',
    'description': 'A Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.',
    'long_description': 'pytest-prefer-nested-dup-tests\n===================================\n\n.. .. image:: http://img.shields.io/pypi/v/pytest-prefer-nested-dup-tests.svg\n..    :target: https://pypi.python.org/pypi/pytest-prefer-nested-dup-tests\n\n.. .. image:: https://github.com/nicoddemus/pytest-prefer-nested-dup-tests/workflows/main/badge.svg\n..   :target: https://github.com/nicoddemus/pytest-prefer-nested-dup-tests/actions\n\n\nA Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.\n\nPytest by default will collect all tests from directories or files given\nin the command-line. For example, if you execute::\n\n    pytest tests/unit tests/\n\nTests from ``tests/unit`` will appear twice, because they will be collected\nagain when pytest sees the ``tests`` directory in the command-line.\n\nThis plugin is intended for the cases where the user wants to run all tests\nfrom ``tests/unit`` first and then the rest of the tests under ``tests``,\nwithout duplicates.\n\n\nInstallation\n------------\n\nYou can install via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-prefer-nested-dup-tests\n\n\nUsage\n-----\n\nThe plugin is enabled by default, no other action is necessary.\n\nContributing\n------------\nContributions are very welcome. Tests can be run with `tox`_, please ensure\nthe coverage at least stays the same before you submit a pull request.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-prefer-nested-dup-tests" is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`file an issue`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`tox`: https://tox.readthedocs.org/en/latest/\n.. _`pip`: https://pypi.python.org/pypi/pip/\n.. _`PyPI`: https://pypi.python.org/pypi\n',
    'author': 'Marximus Maximus',
    'author_email': 'marximus@marximus.com',
    'maintainer': 'Marximus Maximus',
    'maintainer_email': 'marximus@marximus.com',
    'url': 'https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
