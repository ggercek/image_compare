#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `file_handlers` module."""


import os
import unittest
from image_compare.util import get_timestamp_str
from image_compare.models import FilePair
from image_compare.file_handlers import CSVInputHandler, CSVOutputHandler, FileHandlerFactory
from image_compare.exceptions import FileError


def get_number_of_skipped_pairs(records):
    """helper function"""
    return len([pair for pair in records if pair.skipped])


class TestCSVInputHandler(unittest.TestCase):
    """Tests for `CSVInputHandler` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_initial_values(self):
        csv_handler = CSVInputHandler("files/tests/input1.csv")
        assert csv_handler.filename == "files/tests/input1.csv"
        assert csv_handler.delimiter == ','
        assert csv_handler.quotechar == '"'
        assert len(csv_handler.records) == 0

    def test_missing_input_file(self):
        csv_handler = CSVInputHandler("files/tests/there_no_such_file.csv")
        with self.assertRaises(FileError):
            csv_handler.read()

    def test_input_file_with_2_empty_file_names(self):
        csv_handler = CSVInputHandler("files/tests/input1-with-2-missing-elements.csv")
        csv_handler.read()
        assert get_number_of_skipped_pairs(csv_handler.records) == 2

    def test_input_file_with_4_empty_file_names(self):
        csv_handler = CSVInputHandler("files/tests/input1-with-4-missing-elements.csv")
        csv_handler.read()
        assert get_number_of_skipped_pairs(csv_handler.records) == 4

    def test_reading_input_file(self):
        csv_handler = CSVInputHandler("files/tests/input1.csv")
        records = csv_handler.read()
        assert len(records) == 4

    def test_read_and_line_nums_of_file_pairs(self):
        csv_handler = CSVInputHandler("files/tests/input1.csv")
        records = csv_handler.read()
        # check the line_num assignment, should start with 1
        assert set([pair.line_num for pair in records]) == set([1, 2, 3, 4])


class TestCSVOutputHandler(unittest.TestCase):
    """Tests for `CSVOutputHandler` class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.temp_files = []
        self.temp_file_folder = "files/tests/tmp"
        self.headers = ["image1", "image2"]
        self.dummy_file = "files/tests/dummy.csv"
        self.sample_pairs = [FilePair("image1","image2",), FilePair("image3", "image4", ), FilePair("image5", "image6")]

        # Create the temp folder if
        if not os.path.exists(self.temp_file_folder):
            os.makedirs(self.temp_file_folder)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        for temp_file in self.temp_files:
            os.remove(temp_file)

    def get_temp_file_name(self):
        tmp_file = os.path.join(self.temp_file_folder, f"output_{get_timestamp_str()}.csv")
        self.temp_files.append(tmp_file)
        return tmp_file

    def test_output_filename_is_a_folder(self):
        csv_handler = CSVOutputHandler("files/", self.headers)
        with self.assertRaises(FileError):
            csv_handler.write(self.sample_pairs)

    def test_output_filename_already_exist_no_overwrite(self):
        csv_handler = CSVOutputHandler(self.dummy_file, self.headers)
        with self.assertRaises(FileError):
            csv_handler.write(self.sample_pairs)

    def test_output_filename_already_exist_with_overwrite(self):
        tmp_file = self.get_temp_file_name()
        # Create a temp file
        csv_handler = CSVOutputHandler(tmp_file, self.headers)
        csv_handler.write(self.sample_pairs)
        # Write again to temp file with overwrite
        csv_handler2 = CSVOutputHandler(tmp_file, self.headers)
        csv_handler2.write(self.sample_pairs, overwrite=True)
        # Read temp file anc check entry count
        csv_input_handler = CSVInputHandler(tmp_file)
        assert len(csv_input_handler.read()) == len(self.sample_pairs)


class TestFileHandlerFactory(unittest.TestCase):
    """Tests for `CSVInputHandler` class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.factory = FileHandlerFactory()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_return_type(self):
        assert type(self.factory.getInputHandler("tests/files/dummy.csv")) == CSVInputHandler
        assert type(self.factory.getOutputHandler("tests/files/dummy.csv", headers=[])) == CSVOutputHandler

    def test_input_handler(self):
        input_handler = self.factory.getInputHandler("tests/files/dummy.csv")
        assert input_handler is not None

    def test_input_invalid_extension(self):
        with self.assertRaises(FileError):
            input_handler = self.factory.getInputHandler("tests/files/dummy.json")

    def test_output_handler(self):
        output_handler = self.factory.getOutputHandler("tests/files/dummy.csv", headers=[])
        assert output_handler is not None

    def test_output_invalid_extension(self):
        with self.assertRaises(FileError):
            output_handler = self.factory.getOutputHandler("tests/files/dummy.json")
