"""
Command definition for "export".
"""

import click

from sonse.tasks.base import group, Name


@group.command(short_help="export a note")
@click.argument("name", type=Name())
@click.argument("file", type=click.File("w", encoding="utf-8"))
@click.pass_obj
def export(book, name, file):
    """
    Copy an existing note to a file on-disk.
    """

    if note := book.get(name):
        file.write(note.read())

    else:
        click.echo(f"Error: {name!r} does not exist.")
