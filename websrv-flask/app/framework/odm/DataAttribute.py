from framework.odm.DataObject import DataObject


class DataAttribute(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the database persistent behavior of
    PersistentObject attributes. Use cls.attribute_name = PersistentAttribute(cls, "attribute_name") to add a
    database persistent attribute to some class cls.
    """

    def __init__(self, cls: type, name: str):
        """
        :param cls: type The class to which to add the attribute. This argument is needed to keep the target class
         aware of which PersistentAttributes exist, to automatically make subclasses of PersistentObject json
         serializable.
        :param name: str The name of the PersistentAttribute. This is how it will show up in the database and in json.
        """
        if not hasattr(cls, "persistent_attributes"):
            cls.persistent_attributes = dict({})  # let cls keep track of all persistent attributed
        cls.persistent_attributes[name] = self
        self.__external_name = name
        self.__name = "__persistent_attr_{}".format(name)

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

    def __get__(self, obj, obj_type=None):
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)
        return value

    def __set__(self, obj: DataObject, value):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, value)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)