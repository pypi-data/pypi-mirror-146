"""
Command definition for "import".
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(name="import", short_help="Import a note.")
@click.argument("name", type=Name())
@click.argument("file", type=click.File("r", encoding="utf-8"))
@click.option("-e", "--edit", help="Edit note after import.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def import_(book, name, file, edit):
    """
    Copy a file on-disk to a new or existing note.
    """

    note = book.get(name, create=True)
    body = tools.vals.body(file.read())
    note.write(body)

    if edit:
        if text := tools.jobs.edit(note):
            note.write(text)
