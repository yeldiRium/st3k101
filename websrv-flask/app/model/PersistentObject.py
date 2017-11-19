import random
import time
from typing import Any, List

from bson.objectid import ObjectId
from flask import g
from memcache import Client
from pymongo import MongoClient

from framework.exceptions import ObjectDoesntExistException, BadQueryException
from framework.memcached import get_memcache

_client = MongoClient("db-mongo")
_db = _client['efla-web']


class PersistentObject(object):
    __db = _db

    @classmethod
    def _collection(cls):
        return cls.__db[str(cls)[8:-2]]  # same as classname method

    def __init__(self, uuid: str = None):
        """
        :param uuid: str If passed, self will be a representant of the object with the given uuid. Important: If two
        instances of the same PersistentObject are created, the instances do not update each other, when values are
        changed.
        """
        self.__id = None
        if uuid:
            document = self._collection().find_one({u'_id': ObjectId(uuid)})
            if not document:
                raise ObjectDoesntExistException("No PersistentObject with uuid {}".format(uuid))
            self.__from_document(document)
        else:
            self.__id = self._collection().insert_one(self._document_skeleton()).inserted_id

        # lock object by shared mutex in memcached while object is alive
        # only one app context may access a PersistentObject at a time.
        # This is used to prevent race conditions and data corruption between requests.
        mutex_key = "mutex_{}".format(self.uuid)
        mutex_polling_time = g._config["DISTRIBUTED_MUTEX_POLLING_TIME"]

        if hasattr(g, "_local_mutexes"):
            if mutex_key in g._local_mutexes:
                self.__mutex_set = True
                return

        while True:

            mutex_set = get_memcache().get(mutex_key)
            while mutex_set:
                time.sleep(mutex_polling_time + random.uniform(0, mutex_polling_time / 10))
                mutex_set = get_memcache().get(mutex_key)

            if not get_memcache().cas(mutex_key, True) != 0:
                continue

            break

        if not hasattr(g, "_local_mutexes"):
            g._local_mutexes = []
        g._local_mutexes.append(mutex_key)
        self.__mutex_set = True

    def __del__(self):
        Client(['memcached']).delete("mutex_{}".format(self.uuid))  # context is already destroyed, can't use framework

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
        new_query = dict({})
        for name, value in query.items():
            attr = cls.persistent_members().get(name)
            if not attr:
                raise BadQueryException("No attribute {} for class {}".format(name, str(cls)[8:-2]))

            new_query[attr.internal_name] = value

        document = cls._collection().find_one(new_query)
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
        new_query = dict({})
        for name, value in query.items():
            attr = cls.persistent_members().get(name)
            if not attr:
                raise BadQueryException("No attribute {} for class {}".format(name, str(cls)[8:-2]))

            new_query[attr.internal_name] = value

        documents = cls._collection().find(new_query)
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

    @classmethod
    def persistent_members(cls) -> dict:
        """
        Returns data of self as dict in external representation.
        Used for serialization (storing to mongodb, to_json())
        :return: dict
        """
        pers_attrs = {}
        if hasattr(cls, "persistent_attributes"):
            pers_attrs.update(cls.persistent_attributes)

        if hasattr(cls, "persistent_references"):
            pers_attrs.update(cls.persistent_references)

        if hasattr(cls, "persistent_reference_lists"):
            pers_attrs.update(cls.persistent_reference_lists)

        return pers_attrs

    @classmethod
    def _document_skeleton(cls) -> dict:

        return {a.internal_name: None for _, a in cls.persistent_members().items()}


class PersistentAttribute(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, cls: type, name: str):
        if not hasattr(cls, "persistent_attributes"):
            cls.persistent_attributes = dict({})
        cls.persistent_attributes[name] = self
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
            cls.persistent_references = dict({})
        cls.persistent_references[name] = self
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
            cls.persistent_references = dict({})
        cls.persistent_references[name] = self
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
