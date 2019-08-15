class FilePair:
    def __init__(self, filename1, filename2, similarity=-1.0, elapsed=-1.0, line_num=-1, skipped=False):
        self.file1 = filename1
        self.file2 = filename2
        self.similarity = similarity
        self.elapsed = elapsed
        self.line_num = line_num
        self.skipped = skipped

    def __repr__(self):
        return f"[{self.line_num}]:{self.file1}<->{self.file2}~{self.similarity}, elapsed:{self.elapsed}"
