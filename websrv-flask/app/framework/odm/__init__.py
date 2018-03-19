from enum import Enum, auto


class PointerType(Enum):
    """
    Enumeration of all pointer types.
    Pointer types are used in reference counting and the cascading delete
    feature. For more information see docs/odm.md
    """
    WEAK = auto()
    STRONG = auto()
