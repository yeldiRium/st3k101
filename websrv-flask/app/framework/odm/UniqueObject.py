from flask import g

__author__ = "Noah Hummel, Hannes Leutloff"


class UniqueObject(object):
    """
    This class mainly exists to calm PyCharm's linter.
    See it as a kind of forward declaration.
    """

    @property
    def uuid(self) -> str:
        """
        Getter for UnqiueObject.uuid.
        :return: str An unique and uniformly used identifier for the 
                     UniqueObject.
        """
        return str(self._id)

    def __init__(self, uuid: str, **kwargs):
        self._id = uuid


class UniqueHandle(type):
    """
    A metaclass which creates only one UniqueObject instance for a given uuid. 
    Any subsequent calls to the class constructor are omitted and the previous 
    instance is returned.
    It uses flasks g object to achieve this.
    This means that for any given flask request context, only one instance of 
    UniqueObject with a given uuid can exist.
    """

    def __call__(cls, uuid: str=None, **kwargs):
        # uuid should be str, but we will also allow types which support string
        # representations
        if uuid:
            if type(uuid) != str:
                uuid = str(uuid)

        # this is where we will keep track of already created instances
        if not hasattr(g, "_persistent_objects"):
            g._persistent_objects = dict({})

        if not uuid or (uuid not in g._persistent_objects.keys()):
            # if uuid is omitted, a new object is requested, which is different
            # to every already existing object by definition
            instance: UniqueObject = object.__new__(cls)
            instance.__init__(uuid, **kwargs)
            # in case uuid was None and was set during __init__()
            uuid = instance.uuid
            g._persistent_objects[uuid] = instance

        return g._persistent_objects[uuid]
