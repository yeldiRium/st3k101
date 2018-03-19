from framework.odm.DataObject import DataObject
from framework.internationalization import _


class I18n(object):
    """
    An internationalized constant string, which is translated before runtime.
    Contains a msgid identifying the string and a text, which contains the
    appropriate localized version of the string for the current request.
    
    The translation of the string is achieved with gettext.
    """
    def __init__(self, msgid: str):
        self.__msgid = msgid

    @property
    def msgid(self) -> str:
        """
        Getter for I18n.msgid
        :return: str The msgid
        """
        return self.__msgid

    @property
    def text(self) -> str:
        """
        Getter for localized version of I18n.msgid. Gets the appropriate version
        according to g._locale.
        :return: str Localized version of I18n.msgid
        """
        return _(self.msgid)

    def __eq__(self, other: "I18n") -> bool:
        """
        Method to compare I18n objects. I18n objects are equivalent, when their
        msgids are equivalent.
        :param other: I18n The other object to compare to
        :return: bool Whether the objects are equivalent
        """
        if not type(other) == I18n:
            return False
        return self.msgid == other.msgid


class DataString(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the 
    database persistent behavior of DataObject attributes that are 
    interantionalized strings. 
    Use cls.attribute_name = DataString(cls, "attribute_name") to add a
    database persistent string attribute to some class cls.
    Usages 
    """

    def __init__(self, cls: type, name: str, serialize: bool=True,
                 no_acl:bool=False):
        """
        :param cls: type The class to which to add the attribute. This argument is needed to keep the target class
         aware of which DataAttributes exist, to automatically make subclasses of DataObject json
         serializable.
        :param name: str The name of the DataAttribute. This is how it will show up in the database and in json.
        :param serialize: bool whether the object encoder should automatically serialize this attribute
        """
        cls: DataObject

        if not hasattr(cls, "data_strings"):
            cls.data_strings= dict({})  # let cls keep track of all persistent attributes
        cls.data_strings[name] = self
        self.__external_name = name
        self.__name = "__data_str_{}".format(name)
        self.__serialize = serialize
        self.__no_acl = no_acl

        if no_acl:
            cls.acl_exclusions.append(self.__name)

    @property
    def name(self) -> str:
        """
        Getter for DataString.name
        :return: str DataString.name
        """
        return self.__external_name

    @property
    def internal_name(self) -> str:
        """
        The name of the target classes internal attribute keeping track of the attributes value.
        Never use the internal attribute directly, instead use this descriptor class, or it's __get__() method.
        :return: str DataString.internal_name
        """
        return self.__name

    @property
    def serialize(self) -> bool:
        """
        Getter for DataString.serialize
        :return: bool Whether this member should be json serialized by 
                      DataObjectEncoder
        """
        return self.__serialize

    def __get__(self, obj, obj_type=None) -> I18n:
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)
        return I18n(value)  # return localized version of string

    def __set__(self, obj: DataObject, i18n: I18n) -> None:
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, i18n.msgid)

    def __delete__(self, obj) -> None:
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)