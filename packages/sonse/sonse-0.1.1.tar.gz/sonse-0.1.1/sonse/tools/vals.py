"""
Object value parsing and validation functions.
"""

import fnmatch
import re
import string

DATE_FORM = "%Y-%m-%d %H:%M:%S"
NAME_OKAY = string.ascii_letters + string.digits + "-_"


def body(text):
    """
    Return a text body with trimmed whitespace.
    """

    return text.strip() + "\n"


def glob(name, pttn):
    """
    Return True if a name string matches a glob pattern.
    """

    regx = fnmatch.translate(pttn).rstrip("\\Z")
    return bool(re.match(regx, name))


def name(text):
    """
    Return a lowercase name string without punctuation.
    """

    text = str(text).strip().lower()
    return "".join(char for char in text if char in NAME_OKAY)
