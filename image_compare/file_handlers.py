""" This module contains the file handler classes.
    Currently supports only CSV format
"""
import csv
import os.path
from image_compare.models import FilePair
from image_compare.util import clean_string
from image_compare.exceptions import IOICError


class CSVInputHandler():
    def __init__(self, filename, delimiter=',', quotechar='"'):
        self.filename = filename
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.records = []

    def read(self):
        if os.path.isfile(self.filename):
            self.__process_file()
        else:
            raise IOICError(self.filename, "No such file exists")

        return self.records

    def __process_file(self):
        self.records = []
        with open(self.filename, 'r') as csv_file:
            file_pair_reader = csv.DictReader(csv_file, delimiter=self.delimiter, quotechar=self.quotechar)
            for row in file_pair_reader:
                image1 = clean_string(row["image1"])
                image2 = clean_string(row["image2"])
                # If the input is missing just skip the file and log it as warning
                skip = (image1 == "") | (image2 == "")
                self.records.append(
                    FilePair(filename1=image1, filename2=image2, skipped=skip))
