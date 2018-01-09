from framework.odm import PointerType
from framework.odm.DataObject import DataObject


class DataPointer(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the database persistent behavior of
    PersistentObject attributes, which are references to other PersistentObject.
    Use cls.attribute_name = PersistentAttribute(cls, "attribute_name", other_cls) to add a database persistent ref-
    erence to ome other PersistentObject.
    """

    def __init__(self, cls: type, name: str, other_class: type, cascading_delete: bool = False,
                 pointer_type: PointerType = PointerType.WEAK):
        """
        :param cls: type See documentation for PersistentAttribute.
        :param name: str See documentation for PersistentAttribute.
        :param other_class: type The class that is referenced by this attribute. Needed to instantiate other_class
        when this attribute is accessed.
        """
        if not hasattr(cls, "persistent_references"):
            cls.persistent_references = dict({})
        cls.persistent_references[name] = self
        self.__external_name = name
        self.__name = "__persistent_ref_{}".format(name)
        self.__other_class = other_class
        self.__cascading_delete = cascading_delete
        self.__reference_type = pointer_type

    @property
    def cascading_delete(self):
        return self.__cascading_delete

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

        value = getattr(obj, self.__name, None)  # only stores uuid
        if value is None:
            return None
        return self.__other_class(value)  # instantiate referenced PersistentObject by it's uuid

    def __set__(self, obj: DataObject, value: DataObject):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        if not issubclass(type(value), DataObject):
            if value is not None:
                raise TypeError("A data pointer can only be a DataObject or None.")

        if self.__reference_type == PointerType.STRONG:
            if value is not None:
                value.inc_refcount()
            # if this is already set, decrease refcount of object previously pointed to
            previous_value = getattr(obj, self.__name, None)
            if previous_value:
                self.__other_class(previous_value).dec_refcount()

        uuid = value.uuid if value is not None else None  # store only the object's uuid
        obj._set_member(self.__name, uuid)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """

        uuid = getattr(obj, self.__name, None)

        if self.__reference_type == PointerType.STRONG:
            self.__other_class(uuid).dec_refcount()

        obj._set_member(self.__name, None)