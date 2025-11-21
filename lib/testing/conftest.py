#!/usr/bin/env python3
"""Pytest configuration and helpers for the test suite.

This module customizes pytest's test item naming to display class docstrings
alongside test method docstrings. It helps make test output more readable.
"""


def pytest_itemcollected(item):
    """Customize test item node ID to include class and method docstrings.
    
    When a test method has a docstring, pytest normally displays the method name.
    This hook changes the displayed name to "<class docstring> <method docstring>"
    for more readable test output.
    
    Args:
        item: A pytest Item object representing a collected test.
    """
    par = item.parent.obj
    node = item.obj
    # Get docstring from parent class (test class), fall back to class name
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    # Get docstring from test method, fall back to method name
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))