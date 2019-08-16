# -*- coding: utf-8 -*-
""" This module contains the file handler classes.
    Currently supports only CSV format
"""
import csv
import pathlib
import os.path
from collections import defaultdict
from image_compare.models import FilePair
from image_compare.util import clean_string
from image_compare.exceptions import FileError


class FileHandlerFactory:
    def __init__(self):
        self.input_handlers = defaultdict(None, {".csv": CSVInputHandler})
        self.output_handlers = defaultdict(None, {".csv": CSVOutputHandler})

    def getInputHandler(self, filename, *args, **kwargs):
        return self.__getFileHandler(self.input_handlers, filename, *args, **kwargs)

    def getOutputHandler(self, filename, *args, **kwargs):
        return self.__getFileHandler(self.output_handlers, filename, *args, **kwargs)

    def __getFileHandler(self, handler_dict, filename, *args, **kwargs):
        # TODO: move os.path calls to pathlib if possible.
        extension = pathlib.Path(filename).suffix
        handler = handler_dict.get(extension)
        if handler:
            return handler(filename, *args, **kwargs)
        else:
            raise FileError(filename, f"{extension} is not a supported type")


class CSVInputHandler:
    def __init__(self, filename, delimiter=',', quotechar='"', default_filename="<NO_FILE_GIVEN>"):
        self.filename = filename
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.default_filename = default_filename
        self.records = []

    def read(self):
        if os.path.isfile(self.filename):
            self.__process_file()
        else:
            raise FileError(self.filename, "No such file exists")

        return self.records

    def __process_file(self):
        self.records = []
        with open(self.filename, 'r') as csv_file:
            file_pair_reader = csv.DictReader(csv_file, delimiter=self.delimiter, quotechar=self.quotechar)
            for line_num, row in enumerate(file_pair_reader):
                image1 = clean_string(row["image1"], default=self.default_filename)
                image2 = clean_string(row["image2"], default=self.default_filename)
                # If the input is missing just skip the file and log it as warning
                skip = (image1 == self.default_filename) | (image2 == self.default_filename)
                self.records.append(FilePair(image1=image1, image2=image2, line_num=line_num + 1, skipped=skip))


class CSVOutputHandler:
    def __init__(self, filename, headers, delimiter=',', quotechar='"'):
        self.filename = filename
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.headers = headers

    def write(self, pairs, overwrite=False):
        # Check headers if they are missing get the field info from private obj.__dict__
        if self.headers is None or len(self.headers) == 0:
            pair = pairs[0]
            self.headers = pair.__dict__.keys()

        # Check if file exists
        if os.path.exists(self.filename):
            # Can be a folder, report and stop execution
            if os.path.isdir(self.filename):
                raise FileError(self.filename, "Can not use a folder as output file.")

            if os.path.isfile(self.filename) and overwrite is False:
                raise FileError(self.filename, "File already exists. Use overwrite=True if you want to replace it.")

        with open(self.filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delimiter,
                                quotechar=self.quotechar, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(self.headers)
            writer.writerows([self.to_list(pair.__dict__) for pair in pairs])

    def to_list(self, pair_dict):
        return [pair_dict[fieldname] for fieldname in self.headers]
