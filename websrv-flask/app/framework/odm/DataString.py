from framework.odm.DataObject import DataObject
from framework.internationalization import _


class I18n(object):
    def __init__(self, msgid: str):
        self.__msgid = msgid

    @property
    def msgid(self):
        return self.__msgid

    @property
    def text(self):
        return _(self.msgid)


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

    def __init__(self, cls: type, name: str, serialize: bool=True):
        """
        :param cls: type The class to which to add the attribute. This argument is needed to keep the target class
         aware of which DataAttributes exist, to automatically make subclasses of DataObject json
         serializable.
        :param name: str The name of the DataAttribute. This is how it will show up in the database and in json.
        :param serialize: bool whether the object encoder should automatically serialize this attribute
        """
        if not hasattr(cls, "data_strings"):
            cls.data_strings= dict({})  # let cls keep track of all persistent attributes
        cls.data_strings[name] = self
        self.__external_name = name
        self.__name = "__data_str_{}".format(name)
        self.__serialize = serialize

    @property
    def name(self):
        return self.__external_name

    @property
    def internal_name(self):
        """
        The name of the target classes internal attribute keeping track of the attributes value.
        Never use the internal attribute directly, instead use this descriptor class, or it's __get__() method.
        :return: 
        """
        return self.__name

    @property
    def serialize(self):
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

    def __set__(self, obj: DataObject, i18n: I18n):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, i18n.msgid)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)