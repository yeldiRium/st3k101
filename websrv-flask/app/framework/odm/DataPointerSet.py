from typing import List

from framework.odm import PointerType
from framework.odm.DataObject import DataObject
from framework.odm.SetProxy import SetProxy


class DataPointerSet(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the database persistent behavior of
    DataObject attributes, which are sets of references to other DataObjects.
    Use cls.attribute_name = DataAttribute(cls, "attribute_name", other_cls) to add a database persistent ref-
    erence sets to some other DataObject.
    """

    def __init__(self, cls: type, name: str, other_class: type, serialize:bool=True,
                 cascading_delete: bool = False, pointer_type: PointerType = PointerType.WEAK):
        """
        :param cls: type See documentation for DataAttribute.
        :param name: str See documentation for DataAttribute.
        :param other_class: See documentation for DataPointer
        :param serialize: bool whether the object encoder should automatically serialize this attribute
        :param cascading_delete: bool whether the object pointed to should be deleted when the last strong pointer to it
        is deleted
        :param pointer_type: PointerType the type of pointer, strong pointers to objects stop objects from being deleted
        during a cascading delete. Weak pointers do not count into the reference count of objects.
        """
        if not hasattr(cls, "data_pointer_sets"):
            cls.data_pointer_sets = dict({})
        cls.data_pointer_sets[name] = self
        self.__external_name = name
        self.__name = "__data_pointer_set_{}".format(name)
        self.__other_class = other_class
        self.__serialize = serialize
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

    @property
    def serialize(self):
        return self.__serialize

    def __get__(self, obj, obj_type=None):
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)  # stores list of uuids
        if not value:
            obj._set_member(self.__name, [])
        return SetProxy(obj, self.__name, self.__other_class, reference_type=self.__reference_type)

    def __set__(self, obj: DataObject, value: List[DataObject]):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        self.__delete__(obj)  # decreases refcount of previously set objects
        uuids = [e.uuid for e in value]
        if self.__reference_type == PointerType.STRONG:
            for o in value:
                o.inc_refcount()
        obj._set_member(self.__name, uuids)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        if self.__reference_type == PointerType.STRONG:
            uuids = getattr(self, self.__name, [])
            for uuid in uuids:
                self.__other_class(uuid).dec_refcount()
        obj._set_member(self.__name, None)