#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `image_compare` package."""


import unittest
from click.testing import CliRunner

from image_compare import image_compare
from image_compare import cli


class TestImage_compare(unittest.TestCase):
    """Tests for `image_compare` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'image_compare.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
