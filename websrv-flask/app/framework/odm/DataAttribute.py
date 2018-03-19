from typing import Any

from framework.odm.DataObject import DataObject

__author__ = "Noah Hummel, Hannes Leutloff"


class DataAttribute(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the 
    database persistent behavior of DataObject attributes. 
    Use cls.attribute_name = DataAttribute(cls, "attribute_name") to add a
    database persistent attribute to some class cls.
    """

    def __init__(self, cls: type, name: str, serialize: bool=True,
                 no_acl:bool=False):
        """
        :param cls: type The class to which to add the attribute. 
                         This argument is needed to keep the target class aware 
                         of which DataAttributes exist, to automatically make 
                         subclasses of DataObject json serializable.
        :param name: str The name of the DataAttribute. This is how it will show
                         up in the database and in json.
        :param serialize: bool whether the object encoder should automatically 
                               serialize this attribute
        :param no_acl: bool Whether access control is disabled for this member                       
        """
        cls: DataObject

        if not hasattr(cls, "data_attributes"):
            # let cls keep track of all persistent attributes
            cls.data_attributes = dict({})
        cls.data_attributes[name] = self
        self.__external_name = name
        self.__name = "__data_attr_{}".format(name)
        self.__serialize = serialize
        self.__no_acl = no_acl

        if no_acl:
            cls.acl_exclusions.append(self.__name)

    @property
    def name(self) -> str:
        """
        Getter for DataAttribute.name
        :return: str DataAttribute.name
        """
        return self.__external_name

    @property
    def internal_name(self) -> str:
        """
        The name of the target classes internal attribute keeping track of the 
        attributes value. Never use the internal attribute directly, instead use
         this descriptor class, or it's __get__() method.
        :return: str DataAttribute.internal_name
        """
        return self.__name

    @property
    def serialize(self) -> bool:
        """
        Getter for DataAttribute.serialize
        :return: bool Whether this member should be json serialized by 
                      DataObjectEncoder
        """
        return self.__serialize

    def __get__(self, obj: DataObject, obj_type=None) -> Any:
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)
        return value

    def __set__(self, obj: DataObject, value: Any) -> None:
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, value)

    def __delete__(self, obj: DataObject) -> None:
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)