class ICError(Exception):
    """Base class for exceptions in this module"""
    pass


class FileError(ICError):
    """Exception for file IO errors."""
    def __init__(self, filename, message):
        self.filename = filename
        self.message = message

    def __repr__(self):
        return f"{self.message}: {self.filename}"

    def __str__(self):
        return f"{self.message}: {self.filename}"


class ArgumentError(ICError):
    def __init__(self, message):
        self.message = message
