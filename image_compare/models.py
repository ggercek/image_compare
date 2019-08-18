# -*- coding: utf-8 -*-


class FilePair:
    def __init__(self, image1, image2, similarity=-1.0, elapsed=-1.0, line_num=-1, skipped=False):
        self.image1 = image1
        self.image2 = image2
        self.similarity = similarity
        self.elapsed = elapsed
        self.line_num = line_num
        self.skipped = skipped

    def __repr__(self):
        return f"[{self.line_num}]:{self.image1}<->{self.image2}, " \
               f"similarity:{self.similarity}, elapsed:{self.elapsed}, skipped:{self.skipped}"


class Config:
    def __init__(self, input_file, output_file, overwrite_output=False, quiet=False, distance="dhash",
                 log_level="INFO", log_filename="image_compare.log"):
        self.input_file = input_file
        self.output_file = output_file
        self.overwrite_output = overwrite_output
        self.distance = distance
        self.quiet = quiet
        self.log_level = log_level
        self.log_filename = log_filename

    def __repr__(self):
        return f"Config [input:{self.input_file}, output:{self.output_file}, " \
               f"overwrite_output: {self.overwrite_output}, quiet:{self.quiet}, " \
               f"distance:{self.distance}, log_level:{self.log_level}, log_filename:{self.log_filename}]"
