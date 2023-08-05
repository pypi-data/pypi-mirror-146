"""
Command definition for "import".
"""

import click

from sonse import tools
from sonse.tasks.base import group, Name


@group.command(name="import", short_help="import a note")
@click.argument("name", type=Name())
@click.argument("file", type=click.File("r", encoding="utf-8"))
@click.pass_obj
def import_(book, name, file):
    """
    Copy a file on-disk to a new or existing note.
    """

    note = book.get(name, create=True)
    body = tools.vals.body(file.read())
    note.write(body)
