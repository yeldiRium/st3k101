from typing import Any, List

from bson.objectid import ObjectId
from pymongo import MongoClient

from framework.exceptions import ObjectDoesntExistException

_client = MongoClient("db-mongo")
_db = _client['efla-web']


class PersistentObject(object):

    __db = _db

    @classmethod
    def _collection(cls):
        return cls.__db[str(cls)[8:-2]]  # same as classname method

    def __init__(self, uuid: str=None):
        """
        :param uuid: str If passed, self will be a representant of the object with the given uuid
        """
        self.__id = None
        if uuid:
            document = self._collection().find_one({u'_id': ObjectId(uuid)})  # TODO: lock object for duration of reques
            if not document:
                raise ObjectDoesntExistException("No PersistentObject with uuid {}".format(uuid))
            self.__from_document(document)
        else:
            self.__id = self._collection().insert_one(self.__persistent_members()).inserted_id

    @property
    def uuid(self):
        """
        :return: str The universal & unique identifier of self 
        """
        return str(self.__id)

    @classmethod
    def one_from_query(cls, query: dict):
        """
        Returns one PersistentObject of class cls which matches query
        :param cls: The class of PersistentObject to find
        :param query: The query the object should match
        :return: PersistentObject The PersistentObject instance if found, None otherwise
        """
        document = cls._collection().find_one(query)
        if not document:
            return None

        return cls(document['_id'])

    @classmethod
    def many_from_query(cls, query: dict):
        """
        Returns all PersistentObjects of class cls which match query
        :param cls: The class of PersistentObject to find
        :param query: The query the objects should match
        :return: List[PersistentObject] The list of all matching PersistentObject instances
        """
        documents = cls._collection().find(query)
        results = []

        for doc in documents:
            results.append(cls(doc['_id']))

        return results

    def _set_member(self, member: str, value: Any) -> None:
        """
        Saves a field of self to the database.
        :param value: The member value
        :param member: The member / field name
        :return: None
        """
        setattr(self, member, value)
        self._collection().update_one(
            {u'_id': self.__id},
            {u'$set': {member: value}}
        )

    def remove(self):
        """
        Removes the database entry represented by self from mongodb.
        :return: None
        """
        self._collection().delete_one({u'_id': self.__id})

    def __from_document(self, document: dict):
        """
        Helper function to initialize self from mongodb document
        :param document: 
        :return: 
        """
        if not document:
            return
        self.__id = document['_id']
        del document['_id']
        self.__dict__.update(document)

    def __persistent_members(self) -> dict:
        """
        Returns data of self as dict in external representation.
        Used for serialization (storing to mongodb, to_json())
        :return: dict
        """
        pers_attrs = {}
        if hasattr(self, "persistent_attributes"):
            pers_attrs = {a.internal_name: getattr(self, a.internal_name, None)
                          for a in self.persistent_attributes}

        pers_refs = {}
        if hasattr(self, "persistent_references"):
            pers_refs = {a.internal_name: getattr(self, a.internal_name, None)
                         for a in self.persistent_references}

        pers_ref_lists = {}
        if hasattr(self, "persistent_reference_lists"):
            pers_ref_lists = {a.internal_name: getattr(self, a.internal_name, [])
                              for a in self.persistent_reference_lists}

        pers_attrs.update(pers_refs)
        pers_attrs.update(pers_ref_lists)
        return pers_attrs


    def persistent_members(self) -> list:

        pers_attrs = []
        if hasattr(self, "persistent_attributes"):
            pers_attrs.extend([a.internal_name for a in self.persistent_attributes])

        if hasattr(self, "persistent_references"):
            pers_attrs.extend([a.internal_name for a in self.persistent_references])

        if hasattr(self, "persistent_reference_lists"):
            pers_attrs.extend([a.internal_name for a in self.persistent_reference_lists])

        return pers_attrs


class PersistentAttribute(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, cls: type, name: str):
        if not hasattr(cls, "persistent_attributes"):
            cls.persistent_attributes = []
        cls.persistent_attributes.append(self)
        self.__external_name = name
        self.__name = "__persistent_attr_{}".format(name)

    @property
    def name(self):
        return self.__external_name

    @property
    def internal_name(self):
        return self.__name

    def __get__(self, obj, obj_type=None):
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)
        return value

    def __set__(self, obj: PersistentObject, value):
        obj._set_member(self.__name, value)

    def __delete__(self, obj):
        obj._set_member(self.__name, None)


class PersistentReference(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, cls: type, name: str, other_class: type):
        if not hasattr(cls, "persistent_references"):
            cls.persistent_references = []
        cls.persistent_references.append(self)
        self.__external_name = name
        self.__name = "__persistent_ref_{}".format(name)
        self.__other_class = other_class

    @property
    def name(self):
        return self.__external_name

    @property
    def internal_name(self):
        return self.__name

    def __get__(self, obj, obj_type=None):
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)  # stores uuid
        if value is None:
            return None
        return self.__other_class(value)

    def __set__(self, obj: PersistentObject, value: PersistentObject):
        uuid = value.uuid
        obj._set_member(self.__name, uuid)

    def __delete__(self, obj):
        obj._set_member(self.__name, None)


class PersistentReferenceList(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, cls: type, name: str, other_class: type):
        if not hasattr(cls, "persistent_reference_lists"):
            cls.persistent_references = []
        cls.persistent_references.append(self)
        self.__external_name = name
        self.__name = "__persistent_reflist_{}".format(name)
        self.__other_class = other_class

    @property
    def name(self):
        return self.__external_name

    @property
    def internal_name(self):
        return self.__name

    def __get__(self, obj, obj_type=None):
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)  # stores uuid
        if not value:
            return []
        return [self.__other_class(uuid) for uuid in value]

    def __set__(self, obj: PersistentObject, value: List[PersistentObject]):
        uuids = [e.uuid for e in value]
        obj._set_member(self.__name, uuids)

    def __delete__(self, obj):
        obj._set_member(self.__name, None)
