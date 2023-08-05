"""
Command definition for "list".
"""

import click

from sonse.tasks.base import group


@group.command(name="list", short_help="list notes")
@click.argument("glob", default="*")
@click.pass_obj
def list_(book, glob):
    """
    List all existing notes, or notes matching GLOB.
    """

    for note in book.glob(glob):
        click.echo(note.name)
