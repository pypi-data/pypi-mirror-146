"""
Zipfile reading and writing functions.
"""

import zipfile
import zlib

from sonse.tools.path import clean

ZARGS = {
    "compression": zipfile.ZIP_DEFLATED,
    "compresslevel": zlib.Z_DEFAULT_COMPRESSION,
}


@clean
def create(path):
    """
    Create an empty zipfile archive.
    """

    with zipfile.ZipFile(path, "x", **ZARGS) as zipf:
        pass


@clean
def iterate(path):
    """
    Return all files in a zipfile in alphabetical order.
    """

    with zipfile.ZipFile(path, "r", **ZARGS) as zipf:
        return sorted(zipf.namelist())


@clean
def read(path, file):
    """
    Return the contents of a file in a zipfile as a string.
    """

    with zipfile.ZipFile(path, "r", **ZARGS) as zipf:
        body = zipf.read(file).decode("utf-8")
        return body.strip() + "\n"


@clean
def write(path, file, body):
    """
    Write a string to a new or existing file in a zipfile.
    """

    with zipfile.ZipFile(path, "r", **ZARGS) as zipf:
        data = {file: read(path, file) for file in zipf.namelist()}

    data[file] = body.strip() + "\n"

    with zipfile.ZipFile(path, "w", **ZARGS) as zipf:
        for file, body in data.items():
            zipf.writestr(file, body)
