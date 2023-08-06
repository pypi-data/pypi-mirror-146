"""
Command definition for "repl".
"""

import click

from sonse import tools
from sonse.comms.base import group


@group.command(hidden=True, short_help="Launch a REPL.")
@click.help_option("-h", "--help")
@click.pass_obj
def repl(book):
    """
    Launch an interactive REPL with archive objects.
    """

    tools.jobs.repl(book)
