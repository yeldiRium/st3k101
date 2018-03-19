from collections import Iterator
from typing import List, Sized

from framework.odm import PointerType
from framework.odm.DataObject import DataObject


class SetProxyIter(Iterator):
    """
    An Iterator that is returned by SetProxy.__iter__.
    
    This allows us to use the "for x in xs:" idiom on DataPointerSets,
    as DataPointerSet will return a SetProxy when accessed and SetProxy
    supports iterating though SetProxyIter.
    """

    def __init__(self, proxy):
        self.__proxy = proxy  # reference to SetProxy
        self.__i = 0  # index

    def __next__(self) -> DataObject:
        """
        Override of Iterator.__next__(), returns the next element in the
        iterator or raises StopIteration when no more items are left to iterate.
        :return: DataObject The next element in the iterator 
        """
        if self.__i < len(self.__proxy):
            the_next = self.__proxy._get_proxee()[self.__i]
            self.__i += 1
            return self.__proxy._klass(the_next)
        else:
            raise StopIteration

class SetProxy():
    """
    A proxy class which wraps accesses to a DataPointerSet to map them to
    database actions and implements common features for set classes.
    
    (See https://docs.python.org/3/library/abc.html)
    
    When a DataPointerSet is accessed, a SetProxy is returned which operates
    on a list of DataObject uuids. When items are added or removed, the proxied
    list is also updated and the appropriate changes are made to the database.
    """

    def __init__(self, obj: DataObject, attr_name: str, klass: type,
                 reference_type: PointerType = PointerType.WEAK):
        """
        :param obj: DataObject The DataObject which contains the DataPointerSet
        :param attr_name: str The internal_name of the proxied set
        :param klass: type The class of DataObject that is pointed to
        :param reference_type: the type of pointer, strong pointers to objects 
                               stop objects from being deleted during a 
                               cascading delete. Weak pointers do not count into
                               the reference count of objects.
        """
        self.__instance = obj
        self.__attr_name = attr_name
        self._klass = klass
        self.__reference_type = reference_type

    def _get_proxee(self) -> List[str]:
        """
        Helper function to accesś the DataObject's PointerSet
        :return: List[str] The list of pointed to uuids which is attached to the
                           DataObject which contains the DataPointerSet
        """
        return getattr(self.__instance, self.__attr_name)

    def __contains__(self, item: DataObject) -> bool:
        """
        Implemented to allow the use of "object in SetProxy", checks if item
        is contained in SetProxy.
        :param item: DataObject The item that might be in this SetProxy
        :return: bool Whether the item is contained in this SetProxy
        """
        return item.uuid in self._get_proxee()

    def __iter__(self) -> SetProxyIter:
        """
        :return: SetProxyIter An iterator for this SetProxy
        """
        return SetProxyIter(self)

    def __len__(self) -> int:
        """
        :return: int The length of this SetProxy 
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
        return all([i in other for i in self]) and len(self) == len(other)

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

    def add(self, item: DataObject) -> None:
        """
        Adds a DataObject to the DataPointerSet.
        Also increments the item's reference count if pointer type is strong.
        :param item: DataObject The object to add
        :return: None
        """
        if not item.uuid in self._get_proxee():
            self._get_proxee().append(item.uuid)
            if self.__reference_type == PointerType.STRONG:
                item.inc_refcount()
            self.__instance._set_member(self.__attr_name, self._get_proxee())

    def discard(self, item: DataObject) -> None:
        """
        Discards a DataObject from the DataPointerSet.
        Does nothing if the item is not contained in the DataPointerSet.
        Also decreases reference count of the item if it is removed and the
        pointer type of the DataPointerSet is strong.
        :param item: DataObject The DataObject to discard
        :return: None
        """
        try:
            self._get_proxee().remove(item.uuid)
            if self.__reference_type == PointerType.STRONG:
                item.dec_refcount()
            self.__instance._set_member(self.__attr_name, self._get_proxee())
        except: pass

    def remove(self, item: DataObject) -> None:
        """
        Removes a DataObject from the DataPointerSet.
        Raises KeyError if the item is not contained in the DataPointerSet.
        Also decreases reference count of the item if it is removed and the
        pointer type of the DataPointerSet is strong.
        :param item: DataObject The DataObject to remove
        :return: None
        """
        if not item.uuid in self._get_proxee():
            raise KeyError
        self._get_proxee().remove(item.uuid)
        if self.__reference_type == PointerType.STRONG:
            item.dec_refcount()
        self.__instance._set_member(self.__attr_name, self._get_proxee())
