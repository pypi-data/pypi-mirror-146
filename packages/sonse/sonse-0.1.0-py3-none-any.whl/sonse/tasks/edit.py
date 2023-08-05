"""
Command definition for "edit".
"""

import click

from sonse.tasks.base import group, Name


@group.command(short_help="edit a note")
@click.argument("name", type=Name())
@click.pass_obj
def edit(book, name):
    """
    Edit an existing note in the default editor.
    """

    if note := book.get(name):
        if text := click.edit(note.read(), require_save=True):
            note.write(text)

    else:
        click.echo(f"Error: {name!r} does not exist.")
