import json

from framework import classname
from model.PersistentObject import PersistentObject, PersistentAttribute, PersistentReference, PersistentReferenceList


class PersistentObjectEncoder(json.JSONEncoder):

    def default(self, o):

        if PersistentObject in o.__class__.__mro__:

            obj_dict = {
                "uuid": o.uuid,
                "class": classname(o),
                "fields": {}
            }

            for name, a in o.persistent_members().items():
                if type(a) == PersistentAttribute:
                    obj_dict["fields"][name] = a.__get__(o)

                elif type(a) == PersistentReference:
                    obj_dict["fields"][name] = self.default(a.__get__(o))

                elif type(a) == PersistentReferenceList:
                    reflist = []
                    for ref_obj in a.__get__(o):
                        reflist.append(self.default(ref_obj))
                    obj_dict["fields"][name] = reflist

            return obj_dict

        return json.JSONEncoder.default(self, o)
