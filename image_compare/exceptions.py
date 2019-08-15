class ICError(Exception):
    """Base class for exceptions in this module"""
    pass


class IOICError(ICError):
    """Exception for file IO errors."""
    def __init__(self, filename, message):
        self.filename = filename
        self.message = message

    def __repr__(self):
        return f"{self.message}: {self.filename}"

    def __str__(self):
        return f"{self.message}: {self.filename}"
