"""
Command definition for "read".
"""

import click

from sonse.comms.base import group, Name


@group.command(short_help="Read a note.")
@click.argument("name", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def read(book, name):
    """
    Print an existing note.
    """

    if note := book.get(name):
        print(note.read())
