"""`usaddress` is a Python library for parsing unstructured United States address strings 
into address components, using advanced NLP methods."""

from .usaddress import tag, parse
from . import usaddress
from . import resources
from . import errors

__all__ = ["tag", "parse", "usaddress", "resources", "errors"]
