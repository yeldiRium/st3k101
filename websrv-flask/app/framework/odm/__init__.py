from enum import Enum, auto

__author__ = "Noah Hummel, Hannes Leutloff"


class PointerType(Enum):
    """
    Enumeration of all pointer types.
    Pointer types are used in reference counting and the cascading delete
    feature. For more information see docs/odm.md
    """
    WEAK = auto()
    STRONG = auto()
