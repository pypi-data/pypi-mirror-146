"""
Click base group and type definitions.
"""

import os

import click

from sonse import tools
from sonse import VERSION_STRING
from sonse.items import Book

BOOK_DIRE = tools.path.expand("$HOME/.config/sonse")
BOOK_PATH = tools.path.expand("$HOME/.config/sonse/sonse.zip")


@click.group(name="sonse", no_args_is_help=True)
@click.help_option("--help")
@click.version_option("", "--version", message=VERSION_STRING)
@click.pass_context
def group(ctx):
    """
    Stephen's Obsessive Note-Storage Engine.
    """

    if ctx.obj == None:
        if not os.path.isdir(BOOK_DIRE):
            os.makedirs(BOOK_DIRE)

        if not os.path.isfile(BOOK_PATH):
            tools.file.create(BOOK_PATH)

        ctx.obj = Book(BOOK_PATH)


class Name(click.ParamType):
    """
    A Custom Click type for name strings.
    """

    name = "name"

    def convert(self, value, param, ctx):
        """
        Convert a user value to a name string.
        """

        return tools.vals.name(str(value))
