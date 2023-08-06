"""
High-level command support functions.
"""

import code
import sys

import click

from sonse import VERSION_STRING


def edit(note):
    """
    Open a Note in the default editor and return the edited text. If this
    function is called during a pytest, return a test value instead.
    """

    if "pytest" in sys.modules:
        return f"Edited {note.name!r}."

    else:
        return click.edit(note.read(), require_save=True)


def repl(book):
    """
    Open a Book in a read-eval-print loop.  If this function is called during
    a pytest, print a test value instead.
    """

    if "pytest" in sys.modules:
        print("Opened REPL.")

    else:
        args = {"book": book, "notes": book.read().values()}
        code.interact(banner=VERSION_STRING, local=args, exitmsg="")
