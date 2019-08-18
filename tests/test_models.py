#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `models` module."""


import unittest
from image_compare import models


class TestModels(unittest.TestCase):
    """Tests for `FilePair` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_file_pair_initial_values(self):
        fp = models.FilePair("aa.png", "bb.png")
        assert fp.image1 == "aa.png"
        assert fp.image2 == "bb.png"
        assert fp.similarity == -1.0
        assert fp.elapsed == -1.0
        assert fp.line_num == -1
        assert fp.skipped is False

    def test_config_initial_values(self):
        config = models.Config("input.csv", "output.csv")
        assert config.input_file == "input.csv"
        assert config.output_file == "output.csv"
        assert config.overwrite_output is False
        assert config.quiet is False
        assert config.distance == "ssim"
        assert config.log_level == "INFO"
        assert config.log_filename == "image_compare.log"
