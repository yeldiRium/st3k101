from typing import List

from framework.odm import PointerType
from framework.odm.DataObject import DataObject
from framework.odm.MixedSetProxy import MixedSetProxy, instantiate_by_name


class MixedDataPointerSet(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the 
    database persistent behavior of DataObject attributes, which are sets
    of references to other DataObject. This class also allows the set to contain
    DataObjects of different types.
    Use cls.attribute_name = MixedDataPointerSet(cls, "attribute_name",
                                                 other_cls)
    to add a database persistent reference set to a DataObject.
    """

    def __init__(self, cls: type, name: str, serialize:bool=True,
                 cascading_delete: bool = False,
                 pointer_type: PointerType = PointerType.WEAK,
                 no_acl:bool=False):
        """
        :param cls: type See documentation for PersistentAttribute.
        :param name: str See documentation for PersistentAttribute.
        :param other_class: See documentation for PersistentReference
        :param serialize: bool whether the object encoder should automatically
                               serialize this attribute
        :param cascading_delete: bool whether the object pointed to should be 
                                      deleted when the last strong pointer to it
                                      is deleted
        :param pointer_type: PointerType The type of pointer, strong pointers to
                                         objects stop objects from being deleted
                                         during a cascading delete. 
                                         Weak pointers do not count into the 
                                         reference count of objects.
        """
        cls: DataObject

        if not hasattr(cls, "mixed_data_pointer_sets"):
            cls.mixed_data_pointer_sets = dict({})
        cls.mixed_data_pointer_sets[name] = self
        self.__external_name = name
        self.__name = "__mixed_data_pointer_set_{}".format(name)
        self.__serialize = serialize
        self.__cascading_delete = cascading_delete
        self.__reference_type = pointer_type
        self.__no_acl = no_acl

        if no_acl:
            cls.acl_exclusions.append(self.__name)

    @property
    def cascading_delete(self) -> bool:
        """
        Getter for MixedDataPointerSet.cascading_delete
        :return: bool MixedDataPointerSet.cascading_delete
        """
        return self.__cascading_delete

    @property
    def name(self) -> str:
        """
        Getter for MixedDataPointerSet.name
        :return: str MixedDataPointerSet.name
        """
        return self.__external_name

    @property
    def internal_name(self) -> str:
        """
        The name of the target classes internal attribute keeping track of the 
        attributes value. Never use the internal attribute directly, instead use
        this descriptor class, or it's __get__() method.
        :return: str MixedDataPointerSet.internal_name
        """
        return self.__name

    @property
    def serialize(self) -> bool:
        """
        Getter for MixedDataPointerSet.serialize
        :return: bool Whether this member should be json serialized by 
                      DataObjectEncoder
        """
        return self.__serialize

    def __get__(self, obj, obj_type=None) -> MixedSetProxy:
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)  # stores list of (module_name, class_name, uuid)
        if not value:
            obj._set_member(self.__name, [])
        return MixedSetProxy(obj, self.__name, reference_type=self.__reference_type)

    def __set__(self, obj: DataObject, value: List[DataObject]) -> None:
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        self.__delete__(obj)
        instance_references = [(e.__module__, e.__class__.__name__, e.uuid) for e in value]
        if self.__reference_type == PointerType.STRONG:
            for o in value:
                o.inc_refcount()
        obj._set_member(self.__name, instance_references)

    def __delete__(self, obj) -> None:
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        if self.__reference_type == PointerType.STRONG:
            instance_references = getattr(self, self.__name, [])  # type [(module_name, class_name, uuid)]
            for m, c, uuid in instance_references:
                instantiate_by_name(m, c, uuid) .dec_refcount()
        obj._set_member(self.__name, None)
