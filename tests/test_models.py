#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `models` module."""


import unittest
from image_compare import models


class TestModelFilePair(unittest.TestCase):
    """Tests for `FilePair` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_initial_values(self):
        fp = models.FilePair("aa.png", "bb.png")
        assert fp.image1 == "aa.png"
        assert fp.image2 == "bb.png"
        assert fp.similarity == -1.0
        assert fp.elapsed == -1.0
        assert fp.line_num == -1
        assert fp.skipped is False
