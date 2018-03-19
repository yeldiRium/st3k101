import json
from typing import Any

from framework import classname
from framework.exceptions import AccessControlException
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataPointer import DataPointer
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString, I18n
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.odm.SetProxy import SetProxy
from framework.odm.MixedSetProxy import MixedSetProxy

__author__ = "Noah Hummel, Hannes Leutloff"


class DataObjectEncoder(json.JSONEncoder):
    """
    A JSONEncoder which is able to encode all DataObjects to json.
    
    It obeys the ODM's access control and serialization flags. The encoder
    serializes DataAttributes, follows DataPointers to other DataObject and
    recursively serializes an entire object hierarchy. It also detects cycles
    within the object graph and omits serialization if an object was already
    serialized somewhere.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__seen = set({})  # used to detect back-edges while traversing

    def default(self, o: Any) -> Any:
        """
        Overrides JSONEncoder.default.
        JSONEncoder.default is the marshalling method called when a JSONEncoder
        encounters a value for which it doesn't know how to serialize it.
        The job of the default method is to return a json serializable value
        for the non-serializable value.
        
        This implementation follows DataAttribute, DataPointer & DataPointerSet
        members of DataObject and returns a serializable form.
        :param o: Any The value that is not serializable
        :return: Any A serializable form of o
        """

        if o is None:
            return o

        if type(o) == I18n:  # serialize I18n as object of msgid, text
            return {
                "msgid": o.msgid,
                "text": o.text
            }

        if DataObject in o.__class__.__mro__:  # if o is subclass of DataObject

            obj_dict = {  # header for DataObject
                "uuid": o.uuid,
                "class": classname(o),
                "fields": {}  # actual members of object go here
            }

            if o.uuid in self.__seen:  # skip serialization if back-edge
                return obj_dict

            self.__seen.add(o.uuid)

            for name, a in o.persistent_members().items():

                if not a.serialize:  # obey serialize=False flag
                    continue

                if type(a) == DataAttribute:  # just return the value
                    obj_dict["fields"][name] = a.__get__(o)

                if type(a) == DataString:  # recursively serialize I18n
                    obj_dict["fields"][name] = self.default(a.__get__(o))

                elif type(a) == DataPointer:
                    try:  # recursively serialize DataObject
                        obj_dict["fields"][name] = self.default(a.__get__(o))
                    # obey access control
                    except AccessControlException:
                        if not o.readonly:
                            raise AccessControlException()

                # recursively serialize all DataObjects in PointerSet
                elif type(a) in (DataPointerSet, MixedDataPointerSet):
                    reflist = []
                    try:
                        for ref_obj in a.__get__(o):
                            reflist.append(self.default(ref_obj))

                    except AccessControlException:
                        if not o.readonly:
                            raise AccessControlException()

                    obj_dict["fields"][name] = reflist

            # additionally serialize all exposed_properties
            for name in o.exposed_properties:
                obj_dict["fields"][name] = getattr(o, name)

            return obj_dict

        # support for serializing a SetProxy of DataObjects directly
        if type(o) is SetProxy or type(o) is MixedSetProxy:
            result = []
            for e in o:
                try:
                    result.append(self.default(e))
                except AccessControlException:
                    pass

            return result

        # if all else fails, return the base method (which will fail)
        return json.JSONEncoder.default(self, o)
