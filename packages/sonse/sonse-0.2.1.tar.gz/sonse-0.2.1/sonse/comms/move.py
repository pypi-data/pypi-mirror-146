"""
Command definition for "move".
"""

import click

from sonse.comms.base import group, Name


@group.command(short_help="Rename a note.")
@click.argument("name", type=Name())
@click.argument("dest", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def move(book, name, dest):
    """
    Rename an existing note.
    """

    if note := book.get(name):
        if dest in book:
            click.echo(f"Error: {name!r} already exists.")
        else:
            note.rename(dest)

    else:
        click.echo(f"Error: {name!r} does not exist.")
