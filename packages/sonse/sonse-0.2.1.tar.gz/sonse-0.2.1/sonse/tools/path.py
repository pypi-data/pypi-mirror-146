"""
File path manipulation functions.
"""

import os.path


def clean(func):
    """
    Decorate a function to return the first argument as a clean path.
    """

    def wrap(path, *args, **kwargs):
        return func(os.path.normpath(str(path)), *args, **kwargs)

    return wrap


@clean
def base(path):
    """
    Return a path's base name with the extension.
    """

    return os.path.basename(path)


@clean
def exists(path):
    """
    Return True if a path exists.
    """

    return os.path.isfile(path)


@clean
def expand(path):
    """
    Return a clean path with expanded variables.
    """

    if "$" in path or "%" in path:
        path = os.path.expandvars(path)

    if "~" in path:
        path = os.path.expanduser(path)

    return os.path.normpath(path)


@clean
def name(path):
    """
    Return a path's base name without the extension.
    """

    base = os.path.basename(path)
    return os.path.splitext(base)[0]
