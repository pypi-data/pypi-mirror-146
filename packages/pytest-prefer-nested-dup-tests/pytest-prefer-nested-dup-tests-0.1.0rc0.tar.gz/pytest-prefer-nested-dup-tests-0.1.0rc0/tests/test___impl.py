# -*- coding: utf-8 -*-

import sys


def test___main():
    pass


def test_drop_duplicated_dir(testdir):
    testdir.makepyfile(
        """
        def test_foo():
            pass
        """
    )
    result = testdir.runpytest(".", ".")
    result.stdout.fnmatch_lines(
        [
            "* 1 passed in *",
        ]
    )
    assert result.ret == 0


def test_drop_duplicated_pkg(testdir):
    testdir.makepyfile(
        **{
            "pkg/__init__.py": "",
            "pkg/test_foo.py": """
                def test_foo():
                    pass
            """,
        }
    )
    result = testdir.runpytest("pkg", "pkg")
    result.stdout.fnmatch_lines(
        [
            "* 1 passed in *",
        ]
    )
    assert result.ret == 0


def test_drop_duplicated_files(testdir):
    testdir.makepyfile(
        **{
            "tests/test_bar.py": """
                def test_bar():
                    pass
            """,
            "tests/test_foo.py": """
                def test_foo():
                    pass
            """,
        }
    )
    result = testdir.runpytest("tests/test_foo.py", "tests", "-v")
    result.stdout.fnmatch_lines(
        [
            "tests/test_foo.py::test_foo *",
            "tests/test_bar.py::test_bar *",
            "* 2 passed *",
        ]
    )
    assert result.ret == 0


def test_nested_package(testdir):
    # we need to hide our own "tests" module in order for this to work when testing ourself.
    sys_modules_tests_old = sys.modules.get("tests")
    del sys.modules["tests"]

    # do the real test in a try so that we can fix up sys.modules later
    try:
        testdir.makepyfile(
            **{
                "tests/__init__.py": "",
                "tests/foo/__init__.py": "",
                "tests/foo/test_foo.py": """
                            def test_foo():
                                pass
                        """,
                "tests/bar/__init__.py": "",
                "tests/bar/test_bar.py": """
                            def test_bar():
                                pass
                        """,
            }
        )

        result = testdir.runpytest(".", "-v", "--collect-only")
        result.stdout.fnmatch_lines(
            [
                "collected 2 items",
                "<Package tests>",
                "  <Package bar>",
                "    <Module test_bar.py>",
                "      <Function test_bar>",
                "  <Package foo>",
                "    <Module test_foo.py>",
                "      <Function test_foo>",
            ]
        )
        assert result.ret == 0

        result = testdir.runpytest(".", "-v")
        result.stdout.fnmatch_lines(
            [
                "collected 2 items",
                "tests/bar/test_bar.py::test_bar *",
                "tests/foo/test_foo.py::test_foo *",
                "* 2 passed in *",
            ]
        )
        assert result.ret == 0

        result = testdir.runpytest("tests/foo", ".", "--collect-only")
        result.stdout.fnmatch_lines(
            [
                "collected 2 items",
                "<Package tests>",
                "  <Package foo>",
                "    <Module test_foo.py>",
                "      <Function test_foo>",
                "  <Package bar>",
                "    <Module test_bar.py>",
                "      <Function test_bar>",
            ]
        )
        assert result.ret == 0
    finally:
        # fix up sys.modules to include our "tests" module again (not the one from the temp dir)
        sys.modules["tests"] = sys_modules_tests_old


def test___toplevel_coverage():
    # this test solely exists to allow coverage.py to see the top level / outermost scope of our code
    # this is necessary b/c our code gets imported before coverage.py hooks in
    # we simply "hide" our module from python, import it, and then put it back
    # we put it back, just in case something had modified it in memory before this test runs
    old_module = sys.modules["pytest_prefer_nested_dup_tests"]  # keep a reference to it
    del sys.modules["pytest_prefer_nested_dup_tests"]  # hide it from python
    import pytest_prefer_nested_dup_tests  # import it as if new

    sys.modules["pytest_prefer_nested_dup_tests"] = old_module  # put it back

    # same as above, but for the __impl file
    old_module = sys.modules["pytest_prefer_nested_dup_tests.__impl"]
    del sys.modules["pytest_prefer_nested_dup_tests.__impl"]
    import pytest_prefer_nested_dup_tests.__impl

    sys.modules["pytest_prefer_nested_dup_tests.__impl"] = old_module
