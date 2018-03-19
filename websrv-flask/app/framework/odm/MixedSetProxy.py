from collections import Iterator, Sized

import importlib

from framework.odm import PointerType
from framework.odm.DataObject import DataObject


def instantiate_by_name(module_name: str, class_name: str, uuid: str) \
        -> DataObject:
    """
    Helper factory method for instantiating a DataObject subclass by module and 
    class name. The format for module_name is as follows:
    module_name: "module.submodule" 
    class_name:  "MyClass"
    :param module_name: str The name of the module that contains the subclass
    :param class_name: str The name of the subclass itself
    :param uuid: str The uuid of the DataObject to instantiate
    :return: DataObject The new instance
    """
    the_klass = getattr(importlib.import_module(module_name), class_name)
    return the_klass(uuid)


class MixedSetProxyIter(Iterator):
    """
    An Iterator that is returned by MixedSetProxy.__iter__.

    This allows us to use the "for x in xs:" idiom on MixedDataPointerSets,
    as MixedDataPointerSet will return a MixedSetProxy when accessed and 
    MixedSetProxy supports iterating though MixedSetProxyIter.
    """

    def __init__(self, proxy):
        self.__proxy = proxy
        self.__i = 0

    def __next__(self):
        """
        Override of Iterator.__next__(), returns the next element in the
        iterator or raises StopIteration when no more items are left to iterate.
        :return: DataObject The next element in the iterator 
        """
        if self.__i < len(self.__proxy):
            module_name, class_name, uuid = self.__proxy._get_proxee()[self.__i]
            self.__i += 1
            return instantiate_by_name(module_name, class_name, uuid)
        else:
            raise StopIteration


class MixedSetProxy():
    def __init__(self, obj, attr_name, reference_type: PointerType = PointerType.WEAK):
        self.__instance = obj
        self.__attr_name = attr_name
        self.__reference_type = reference_type

    def _get_proxee(self) -> list:
        return getattr(self.__instance, self.__attr_name)

    def __contains__(self, item: DataObject) -> bool:
        """
        Implemented to allow the use of "object in MixedSetProxy", checks if 
        item is contained in MixedSetProxy.
        :param item: DataObject The item that might be in this MixedSetProxy
        :return: bool Whether the item is contained in this MixedSetProxy
        """
        return any([item.uuid == uuid for _, _, uuid in self._get_proxee()])

    def __iter__(self) -> MixedSetProxyIter:
        """
        :return: MixedSetProxyIter An iterator for this MixedSetProxy
        """
        return MixedSetProxyIter(self)

    def __len__(self) -> int:
        """
        :return: int The length of this MixedSetProxy 
        """
        return len(self._get_proxee())

    def __le__(self, other: Sized) -> bool:
        """
        :param other: Sized Another collection of DataObjects
        :return: bool Whether the len of self is lesser or equal to the len of 
                      other
        """
        return len(self) <= len(other)

    def __lt__(self, other: Sized) -> bool:
        """
        :param other: Sized Another collection of DataObjects 
        :return: bool Whether the len of self is lesser than the len of other
        """
        return len(self) < len(other)

    def __eq__(self, other: Sized) -> bool:
        """
        :param other: Sized Another collection of DataObjects 
        :return: bool Whether self and other are equal (contain the same items)
        """
        return all([o in self for o in other]) and len(self) == len(other)

    def __ne__(self, other: Sized) -> bool:
        """
        :param other: Sized Another collection of DataObjects 
        :return: bool Whether self and other are not equal (contain different 
                      items)
        """
        return not self == other

    def __gt__(self, other: Sized) -> bool:
        """
        :param other: Sized Another collection of DataObjects 
        :return: bool Whether the len of self is greater than the len of other
        """
        return len(self) > len(other)

    def __ge__(self, other: Sized) -> bool:
        """
        Sized Another collection of DataObjects
        :param other: 
        :return: bool Whether the len of self is greater or equal to the len of 
                      other
        """
        return len(self) >= len(other)

    def add(self, item):
        """
        Adds a DataObject to the MixedDataPointerSet.
        Also increments the item's reference count if pointer type is strong.
        :param item: DataObject The object to add
        :return: None
        """
        if item not in self:
            instance_record = [item.__module__, item.__class__.__name__, item.uuid]
            self._get_proxee().append(instance_record)
            if self.__reference_type == PointerType.STRONG:
                item.inc_refcount()
            self.__instance._set_member(self.__attr_name, self._get_proxee())

    def discard(self, item):
        """
        Discards a DataObject from the MixedDataPointerSet.
        Does nothing if the item is not contained in the MixedDataPointerSet.
        Also decreases reference count of the item if it is removed and the
        pointer type of the MixedDataPointerSet is strong.
        :param item: DataObject The DataObject to discard
        :return: None
        """
        instance_record = [item.__module__, item.__class__.__name__, item.uuid]
        try:
            self._get_proxee().remove(instance_record)
            if self.__reference_type == PointerType.STRONG:
                item.dec_refcount()
            self.__instance._set_member(self.__attr_name, self._get_proxee())
        except: pass

    def remove(self, item):
        """
        Removes a DataObject from the MixedDataPointerSet.
        Raises KeyError if the item is not contained in the MixedDataPointerSet.
        Also decreases reference count of the item if it is removed and the
        pointer type of the MixedDataPointerSet is strong.
        :param item: DataObject The DataObject to remove
        :return: None
        """
        instance_record = [item.__module__, item.__class__.__name__, item.uuid]
        if instance_record not in self._get_proxee():
            raise KeyError
        self._get_proxee().remove(instance_record)
        if self.__reference_type == PointerType.STRONG:
            item.dec_refcount()
        self.__instance._set_member(self.__attr_name, self._get_proxee())
