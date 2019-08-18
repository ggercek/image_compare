# -*- coding: utf-8 -*-
"""Module holds utility functions"""
from datetime import datetime


def clean_string(val, default=""):
    """Clears the given string, removing trailing and leading spaces and returns the default value

    :param val: value to be cleaned
    :param default: value to return if the val is None or empty string
    :return: default value if empty or None
        else val without trailing or leading spaces
    """
    if val is not None:
        val = val.strip()
        if val:
            return val
    return default


def get_timestamp_str():
    """Returns current time in {YEAR}{MONTH}{DAY}_{HOUR}{MINUTE}{SECOND}_{MICROSECOND} format"""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
