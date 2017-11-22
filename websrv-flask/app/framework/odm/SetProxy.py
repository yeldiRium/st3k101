from collections import Iterator


class SetProxyIter(Iterator):

    def __init__(self, proxy):
        self.__proxy = proxy
        self.__i = 0

    def __next__(self):
        if self.__i < len(self.__proxy):
            the_next = self.__proxy._get_proxee()[self.__i]
            self.__i += 1
            return self.__proxy._klass(the_next)
        else:
            raise StopIteration

class SetProxy():

    def __init__(self, obj, attr_name, klass):
        self.__instance = obj
        self.__attr_name = attr_name
        self._klass = klass

    def _get_proxee(self) -> list:
        return getattr(self.__instance, self.__attr_name)

    def __contains__(self, item):
        return item.uuid in self._get_proxee()

    def __iter__(self):
        return SetProxyIter(self)

    def __len__(self):
        return len(self._get_proxee())

    def __le__(self, other):
        return len(self) <= len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __eq__(self, other):
        return all([i in other for i in self])

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
        if not item.uuid in self._get_proxee():
            self._get_proxee().append(item.uuid)

    def discard(self, item):
        try:
            self._get_proxee().remove(item.uuid)
        except: pass

    def remove(self, item):
        if not item.uuid in self._get_proxee():
            raise KeyError
        self._get_proxee().remove(item.uuid)
