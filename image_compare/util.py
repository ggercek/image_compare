# -*- coding: utf-8 -*-
"""Module holds utility functions"""
from datetime import datetime


def clean_string(val, default=""):
    if val is not None:
        val = val.strip()
        if val:
            return val
    return default


def get_timestamp_str():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
