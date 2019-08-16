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
        self.runner = CliRunner()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_cli_error_no_args(self):
        result = self.runner.invoke(cli.main, [])
        assert result.exit_code == 2, result.exit_code
        assert 'Missing argument "INPUT_FILE"' in result.output, result.output

    def test_cli_error_no_output(self):
        result = self.runner.invoke(cli.main, ["files/tests/dummy.csv"])
        assert result.exit_code == 2, result.exit_code
        assert 'Missing argument "OUTPUT_FILE"' in result.output, result.output

    def test_cli_error_invalid_input(self):
        result = self.runner.invoke(cli.main, ["input.csv", "output.csv"])
        assert result.exit_code == 2, result.exit_code
        assert 'Invalid value for "INPUT_FILE"' in result.output

    def test_cli_error_invalid_distance(self):
        args = ["files/tests/dummy.csv", "output.csv", "--distance=NoSuchDistance"]
        result = self.runner.invoke(cli.main, args)
        assert result.exit_code == 2, result.exit_code
        assert "Invalid value for \"--distance\": invalid choice:" in result.output

    def test_cli_error_invalid_log_level(self):
        args = ["files/tests/dummy.csv", "output.csv", "--log-level=NoSuchDistance"]
        result = self.runner.invoke(cli.main, args)
        assert result.exit_code == 2, result.exit_code
        assert "Invalid value for \"--log-level\": invalid choice:" in result.output

    def test_cli(self):
        result = self.runner.invoke(cli.main, ["files/tests/dummy.csv", "output.csv"])
        assert result.exit_code == 0

    def test_cli(self):
        help_result = self.runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert "--help" in help_result.output and "Show this message and exit." in help_result.output
