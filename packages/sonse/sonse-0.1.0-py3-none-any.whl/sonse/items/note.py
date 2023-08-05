"""
Class definition for "Note".
"""

from sonse import tools


class Note:
    """
    A single plaintext note in a Book.
    """

    def __init__(self, path, name):
        """
        Initialise the Note.
        """

        self.path = str(path)
        self.name = tools.vals.name(name)
        self.file = f"{self.name}.txt"

    def __eq__(self, note):
        """
        Return True if the Note is equal to another Note.
        """

        return all(
            [
                isinstance(note, Note),
                self.path == getattr(note, "path", None),
                self.name == getattr(note, "name", None),
            ]
        )

    def __hash__(self):
        """
        Return the Note's unique hash string.
        """

        return hash(("Note", self.path, self.name))

    def __iter__(self):
        """
        Yield each line in the Note's body.
        """

        yield from self.read().splitlines()

    def __len__(self):
        """
        Return the length of the Note's body.
        """

        return len(self.read())

    def __repr__(self):
        """
        Return the Note as a code-representative string.
        """

        return f"Note({self.path!r}, {self.name!r})"

    def glob(self, pttn):
        """
        Return True if the Note's name matches a glob pattern.
        """

        return tools.vals.glob(self.name, pttn)

    def read(self):
        """
        Return the contents of the Note as a string.
        """

        body = tools.file.read(self.path, self.file)
        return tools.vals.body(body)

    def write(self, body):
        """
        Overwrite the Note's contents with a string.
        """

        body = tools.vals.body(body)
        tools.file.write(self.path, self.file, body)
