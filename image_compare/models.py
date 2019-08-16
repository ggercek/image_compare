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
        return f"[{self.line_num}]:{self.image1}<->{self.image2}~{self.similarity}, elapsed:{self.elapsed}"


class Config:
    def __init__(self, input_file, output_file, distance="ssim", log_level="INFO"):
        self.input_file = input_file
        self.output_file = output_file
        self.distance = distance
        self.log_level = log_level

    def __repr__(self):
        return f"Config [input:{self.input_file.name}, output:{self.output_file.name}, distance:{self.distance}, log_level:{self.log_level}]"
