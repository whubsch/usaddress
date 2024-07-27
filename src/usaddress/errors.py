"""
Errors for usaddress
"""


class RepeatedLabelError(Exception):
    """Class for errors raised when more than one area of the string has the same label"""

    MESSAGE = """
ERROR: Unable to tag this string because more than one area of the string has the same label

ORIGINAL STRING:  {original_string}
PARSED TOKENS:    {parsed_string}
UNCERTAIN LABEL:  {repeated_label}

To report an error in labeling a valid name, open an issue at {repo_url}."""

    def __init__(self, original_string, parsed_string, repeated_label):

        self.message = self.MESSAGE.format(
            original_string=original_string,
            parsed_string=parsed_string,
            repeated_label=repeated_label,
            repo_url="https://github.com/whubsch/usaddress/issues",
        )

        self.original_string = original_string
        self.parsed_string = parsed_string

    def __str__(self):
        return self.message
