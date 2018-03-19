from typing import Tuple, List

from flask.ext.babel import gettext
from .babel_languages import babel_languages

__author__ = "Noah Hummel, Hannes Leutloff"


def _(msgid: str) -> str:
    """
    Syntactical sugar for wrapping string messages in the gettext() function.
    :param msgid: str The msgid of the string to be translated
    :return: str The translated version of the string
    """
    return gettext(msgid)

def list_sorted_by_long_name() -> List[Tuple[str, str]]:
    """
    Utility function which returns the supported languages listed in 
    framework/i18n/babel_languages.py sorted by name.
    :return: List[Tuple[str, str]] List of tuples: (shorthand, name) sorted by 
                                   name
    """
    return sorted(babel_languages.items(), key=lambda aTuple: aTuple[1])
