from collections import Iterator

import importlib

from framework.odm import PointerType
from framework.odm.DataObject import DataObject


def instantiate_by_name(module_name: str, class_name: str, uuid: str) -> DataObject:
    # Load "module.submodule.MyClass"
    the_klass = getattr(importlib.import_module(module_name), class_name)
    return the_klass(uuid)


class MixedSetProxyIter(Iterator):
    def __init__(self, proxy):
        self.__proxy = proxy
        self.__i = 0

    def __next__(self):
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

    def _get_proxee(self) -> list:  # type List[Tuple[module_name, class_name, uuid]]
        return getattr(self.__instance, self.__attr_name)

    def __contains__(self, item):
        return any([item.uuid == uuid for _, _, uuid in self._get_proxee()])

    def __iter__(self):
        return MixedSetProxyIter(self)

    def __len__(self):
        return len(self._get_proxee())

    def __le__(self, other):
        return len(self) <= len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __eq__(self, other):
        return all([o in self for o in other])

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return len(self) > len(other)

    def __ge__(self, other):
        return len(self) >= len(other)

    def __and__(self, other):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    def add(self, item):
        if item not in self:
            instance_record = [item.__module__, item.__class__.__name__, item.uuid]
            self._get_proxee().append(instance_record)
            if self.__reference_type == PointerType.STRONG:
                item.inc_refcount()
            self.__instance._set_member(self.__attr_name, self._get_proxee())

    def discard(self, item):
        instance_record = [item.__module__, item.__class__.__name__, item.uuid]
        try:
            self._get_proxee().remove(instance_record)
            if self.__reference_type == PointerType.STRONG:
                item.dec_refcount()
            self.__instance._set_member(self.__attr_name, self._get_proxee())
        except: pass

    def remove(self, item):
        instance_record = [item.__module__, item.__class__.__name__, item.uuid]
        if instance_record not in self._get_proxee():
            raise KeyError
        self._get_proxee().remove(instance_record)
        if self.__reference_type == PointerType.STRONG:
            item.dec_refcount()
        self.__instance._set_member(self.__attr_name, self._get_proxee())
