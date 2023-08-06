"""
Zipfile reading and writing functions.
"""

import os
import zipfile
import zlib

from sonse.tools.path import clean

ZARGS = {
    "compression": zipfile.ZIP_DEFLATED,
    "compresslevel": zlib.Z_DEFAULT_COMPRESSION,
}


@clean
def _read_dict(path):
    """
    Return a file:body string dictionary from an existing zipfile.
    """

    data = {}
    with zipfile.ZipFile(path, "r", **ZARGS) as zipf:
        for file in zipf.namelist():
            data[file] = zipf.read(file).decode("utf-8").strip() + "\n"

    return data


@clean
def _write_dict(path, data):
    """
    Write a file:body string dictionary to a new zipfile.
    """

    with zipfile.ZipFile(path, "x", **ZARGS) as zipf:
        for file, body in data.items():
            zipf.writestr(file, body.strip() + "\n")


@clean
def create(path):
    """
    Create an empty zipfile archive.
    """

    _write_dict(path, {})


@clean
def delete(path, file):
    """
    Delete an existing file in a zipfile, by creating a new zipfile without the
    deleted file's contents and overwriting the original.
    """

    temp = path + ".temp"
    data = _read_dict(path)
    del data[file]
    _write_dict(temp, data)
    os.replace(temp, path)


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

    data = _read_dict(path)
    return data.get(file, "")


@clean
def rename(path, orig, dest):
    """
    Rename an existing file in a zipfile to a new name.
    """

    write(path, dest, read(path, orig))
    delete(path, orig)


@clean
def write(path, file, body):
    """
    Write a string to a new or existing file in a zipfile, by creating a new
    zipfile with the modified contents and overwriting the original.
    """

    temp = path + ".temp"
    data = _read_dict(path)
    data[file] = body.strip() + "\n"
    _write_dict(temp, data)
    os.replace(temp, path)
