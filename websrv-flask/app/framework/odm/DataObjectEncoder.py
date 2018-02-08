import json

from framework import classname
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataPointer import DataPointer
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString, I18n
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.odm.SetProxy import SetProxy


class DataObjectEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__seen = set({})

    def default(self, o):

        if type(o) == I18n:
            return {
                "msgid": o.msgid,
                "text": o.text
            }

        if DataObject in o.__class__.__mro__:

            obj_dict = {
                "uuid": o.uuid,
                "class": classname(o),
                "fields": {}
            }

            if o.uuid in self.__seen:
                return obj_dict

            self.__seen.add(o.uuid)

            for name, a in o.persistent_members().items():

                if not a.serialize:
                    continue

                if type(a) == DataAttribute:
                    obj_dict["fields"][name] = a.__get__(o)

                if type(a) == DataString:
                    obj_dict["fields"][name] = self.default(a.__get__(o))

                elif type(a) == DataPointer:
                    obj_dict["fields"][name] = self.default(a.__get__(o))

                elif type(a) in (DataPointerSet, MixedDataPointerSet):
                    reflist = []
                    for ref_obj in a.__get__(o):
                        reflist.append(self.default(ref_obj))
                    obj_dict["fields"][name] = reflist

            for name in o.exposed_properties:
                obj_dict["fields"][name] = getattr(o, name)

            return obj_dict

        if type(o) is SetProxy:
            return [self.default(x) for x in o]

        return json.JSONEncoder.default(self, o)
