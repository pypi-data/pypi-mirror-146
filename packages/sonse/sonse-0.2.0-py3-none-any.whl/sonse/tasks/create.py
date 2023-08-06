"""
Command definition for "create".
"""

import click

from sonse.tasks.base import group, Name


@group.command(short_help="create a note")
@click.argument("name", type=Name())
@click.pass_obj
def create(book, name):
    """
    Create a new empty note.
    """

    if name in book:
        click.echo(f"Error: {name!r} already exists.")

    else:
        book.create(name)
