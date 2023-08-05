"""
Command definition for "read".
"""

import click

from sonse.tasks.base import group, Name


@group.command(short_help="print a note")
@click.argument("name", type=Name())
@click.pass_obj
def read(book, name):
    """
    Print an existing note.
    """

    if note := book.get(name):
        print(note.read())
