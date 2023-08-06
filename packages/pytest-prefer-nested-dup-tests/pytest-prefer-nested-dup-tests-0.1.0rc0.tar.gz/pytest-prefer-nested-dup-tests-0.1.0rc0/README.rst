pytest-prefer-nested-dup-tests
===================================

.. .. image:: http://img.shields.io/pypi/v/pytest-prefer-nested-dup-tests.svg
..    :target: https://pypi.python.org/pypi/pytest-prefer-nested-dup-tests

.. .. image:: https://github.com/nicoddemus/pytest-prefer-nested-dup-tests/workflows/main/badge.svg
..   :target: https://github.com/nicoddemus/pytest-prefer-nested-dup-tests/actions


A Pytest plugin to drop duplicated tests during collection, but will prefer keeping nested packages.

Pytest by default will collect all tests from directories or files given
in the command-line. For example, if you execute::

    pytest tests/unit tests/

Tests from ``tests/unit`` will appear twice, because they will be collected
again when pytest sees the ``tests`` directory in the command-line.

This plugin is intended for the cases where the user wants to run all tests
from ``tests/unit`` first and then the rest of the tests under ``tests``,
without duplicates.


Installation
------------

You can install via `pip`_ from `PyPI`_::

    $ pip install pytest-prefer-nested-dup-tests


Usage
-----

The plugin is enabled by default, no other action is necessary.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-prefer-nested-dup-tests" is free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/MarximusMaximus/pytest-prefer-nested-dup-tests/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
