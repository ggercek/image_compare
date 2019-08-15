#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `util` module."""


import unittest
from image_compare.util import clean_string


class TestUtilMethods(unittest.TestCase):
    """Tests for `util` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_clean_string(self):
        assert clean_string(None) == ""
        assert clean_string("") == ""

        assert clean_string("     ") == ""
        assert clean_string("     ", None) is None

        assert clean_string("", None) is None
        assert clean_string(None, 'a') == 'a'

        assert clean_string("    a") == "a"
        assert clean_string("a    ") == "a"
        assert clean_string("    a     ") == "a"

        assert clean_string("    a", None) == "a"
        assert clean_string("a    ", None) == "a"
        assert clean_string("    a     ", None) == "a"


