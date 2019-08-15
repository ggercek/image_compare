#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `file_handlers` module."""


import unittest
from image_compare import file_handlers
from image_compare.exceptions import IOICError


def get_number_of_skipped_pairs(records):
    """helper function"""
    return len([pair for pair in records if pair.skipped])


class TestModelFilePair(unittest.TestCase):
    """Tests for `CSVInputHandler` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_initial_values(self):
        csv_handler = file_handlers.CSVInputHandler("files/tests/input1.csv")
        assert csv_handler.filename == "files/tests/input1.csv"
        assert csv_handler.delimiter == ','
        assert csv_handler.quotechar == '"'
        assert len(csv_handler.records) == 0

    def test_missing_input_file(self):
        csv_handler = file_handlers.CSVInputHandler("files/tests/there_no_such_file.csv")
        with self.assertRaises(IOICError):
            csv_handler.read()

    def test_input_file_with_2_empty_file_names(self):
        csv_handler = file_handlers.CSVInputHandler("files/tests/input1-with-2-missing-elements.csv")
        csv_handler.read()
        assert get_number_of_skipped_pairs(csv_handler.records)  == 2

    def test_input_file_with_4_empty_file_names(self):
        csv_handler = file_handlers.CSVInputHandler("files/tests/input1-with-4-missing-elements.csv")
        csv_handler.read()
        assert get_number_of_skipped_pairs(csv_handler.records) == 4

    def test_reading_input_file(self):
        csv_handler = file_handlers.CSVInputHandler("files/tests/input1.csv")
        records = csv_handler.read()
        assert len(records) == 4
