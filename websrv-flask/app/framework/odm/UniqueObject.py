from flask import g


class UniqueObject(object):
    """
    This class mainly exists to calm PyCharm's linter.
    See it as a kind of forward declaration.
    """

    @property
    def uuid(self):
        return str(self._id)

    def __init__(self, uuid: str, **kwargs):
        self._id = uuid


class UniqueHandle(type):
    """
    A metaclass which creates only one UniqueObject instance for a given uuid. Any subsequent calls to the
    class constructor are omitted and the previous instance is returned.
    It uses flasks g object to achieve this.
    This means that for any given flask request context, only one instance of UniqueObject with a given uuid
    can exist.
    """

    def __call__(cls, uuid=None, **kwargs):
        if uuid:  # uuid should be str, but we will also allow types which support string representations
            if type(uuid) != str:
                uuid = str(uuid)

        if not hasattr(g, "_persistent_objects"):  # this is where we will keep track of already created instances
            g._persistent_objects = dict({})

        if not uuid or (uuid not in g._persistent_objects.keys()):
            # if uuid is omitted, a new object is requested, which is different to every already existing object by def
            instance = object.__new__(cls)  # type: UniqueObject
            instance.__init__(uuid, **kwargs)
            uuid = instance.uuid  # in case uuid was None and was set during __init__()
            g._persistent_objects[uuid] = instance

        return g._persistent_objects[uuid]
