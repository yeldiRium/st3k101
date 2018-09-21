from typing import Tuple, List

from flask_babel import gettext
from .babel_languages import babel_languages

__author__ = "Noah Hummel, Hannes Leutloff"


def _(msgid: str) -> str:
    """
    Syntactical sugar for wrapping string messages in the gettext() function.
    :param msgid: str The msgid of the string to be translated
    :return: str The translated version of the string
    """
    return gettext(msgid)


def __(msgid: str) -> str:
    """
    Syntactical sugar for marking a string for translation. Does _not_ actually
    translate the string, but instead just returns the string as-is.
    This is useful for when you want to store the string to translate in a
    variable and pass that variable to gettext later.
    Wrapping a string in __() will add it to the message catalogue so that it
    may be extracted with pybabel.

    Example:
    >>> some_string = __('This will be translated at some point, but not now.')
    >>> some_string
    'This will be translated at some point, but not now.'
    >>> _(some_string)
    'Dies wird irgendwann übersetzt werden, aber nicht jetzt.'

    :param msgid: The string to mark for translation.
    :return: The string as-ís.
    """
    return msgid


def list_sorted_by_long_name() -> List[Tuple[str, str]]:
    """
    Utility function which returns the supported languages listed in 
    framework/i18n/babel_languages.py sorted by name.
    :return: List[Tuple[str, str]] List of tuples: (shorthand, name) sorted by 
                                   name
    """
    return sorted(babel_languages.items(), key=lambda aTuple: aTuple[1])
