"""
Command definition for "edit".
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Edit a note.")
@click.argument("name", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def edit(book, name):
    """
    Edit an existing note in the default editor.
    """

    if note := book.get(name):
        if text := tools.jobs.edit(note):
            note.write(text)

    else:
        click.echo(f"Error: {name!r} does not exist.")
