"""
Command definition for "delete".
"""

import click

from sonse.comms.base import group, Name


@group.command(short_help="Delete a note.")
@click.argument("name", type=Name())
@click.option("-f", "--force", help="Bypass confirmation prompt.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def delete(book, name, force):
    """
    Delete an existing note.
    """

    if note := book.get(name):
        if force or click.confirm(f"Are you sure you want to delete {name!r}?"):
            note.delete()
        else:
            click.echo("Delete cancelled.")

    else:
        click.echo(f"Error: {name!r} does not exist.")
