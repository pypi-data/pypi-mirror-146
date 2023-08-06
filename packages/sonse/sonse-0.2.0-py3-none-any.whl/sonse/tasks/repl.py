"""
Command definition for "repl".
"""

import code

import click

from sonse import VERSION_STRING
from sonse.tasks.base import group


@group.command(hidden=True)
@click.pass_obj
def repl(book):
    """
    Launch an interactive REPL.
    """

    code.interact(
        banner=VERSION_STRING,
        local={"book": book},
        exitmsg="",
    )
