"""Module holds various helper functions"""


def clean_string(val, default=""):
    if val is not None:
        val = val.strip()
        if val:
            return val
    return default
