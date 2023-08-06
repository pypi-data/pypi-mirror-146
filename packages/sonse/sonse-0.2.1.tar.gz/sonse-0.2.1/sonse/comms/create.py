"""
Command definition for "create".
"""

import click

from sonse import tools
from sonse.comms.base import group, Name


@group.command(short_help="Create a note.")
@click.argument("name", type=Name())
@click.option("-e", "--edit", help="Edit note after creation.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def create(book, name, edit):
    """
    Create a new empty note.
    """

    if name in book:
        click.echo(f"Error: {name!r} already exists.")

    else:
        note = book.create(name)
        if edit:
            if text := tools.jobs.edit(note):
                note.write(text)
