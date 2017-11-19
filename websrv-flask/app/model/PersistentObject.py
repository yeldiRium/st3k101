import random
import time
from typing import Any, List

from bson.objectid import ObjectId
from flask import g
from memcache import Client
from pymongo import MongoClient

from framework.exceptions import ObjectDoesntExistException, BadQueryException
from framework.memcached import get_memcache

_client = MongoClient("db-mongo")  # the database server
_db = _client['efla-web']  # the database used for persisting objects


class PersistentObject(object):
    __db = _db

    @classmethod
    def _collection(cls):
        """
        Returns the name of the mongodb collection used for persisting instances of cls.
        The collection name will be Python's representation of the class name, including containing parent modules.
        This class, for example, will use 'model.PersistentObject.PersistentObject' as collection name.
        :return: str
        """
        return cls.__db[str(cls)[8:-2]]  # same as framework.classname(o) method

    def __init__(self, uuid: str = None):
        """
        :param uuid: str If passed, self will be a representant of the object with the given uuid. Important: If two
        instances of the same PersistentObject are created, the instances do not update each other, when values are
        changed. Only one request context may access the same uuid at once. As a consequence, the constructor may be 
        deferred until the database resource becomes available.
        """
        self.__id = None

        if uuid:  # initialize self from mongodb document with the given uuid
            document = self._collection().find_one({u'_id': ObjectId(uuid)})
            if not document:
                raise ObjectDoesntExistException("No PersistentObject with uuid {}".format(uuid))
            self.__from_document(document)

        else:  # create a new mongodb document for self
            self.__id = self._collection().insert_one(self._document_skeleton()).inserted_id

        # lock object by shared mutex in memcached while object is alive
        # only one app context may access a PersistentObject at a time.
        # This is used to prevent race conditions and data corruption between requests.
        mutex_uuid = self.__mutex_uuid  # string identifying mutex to PersistentObject with this self.uuid uniquely
        mutex_polling_time = g._config["SHARED_MUTEX_POLLING_TIME"]

        if hasattr(g, "_local_mutexes"):
            if mutex_uuid in g._local_mutexes:  # if this context has already acquired the mutex, don't acquire again
                return

        while True:  # until mutex is acquired

            mutex_locked = get_memcache().get(mutex_uuid)
            while mutex_locked:
                # wait random time to avoid deadlocks
                time.sleep(mutex_polling_time + random.uniform(0, mutex_polling_time / 10))
                mutex_locked = get_memcache().get(mutex_uuid)

            if not get_memcache().cas(mutex_uuid, True) != 0:  # atomic write, if memcached wasn't modified
                continue  # atomic write failed

            break  # atomic write succeeded, mutex is acquired

        if not hasattr(g, "_local_mutexes"):
            g._local_mutexes = []
        g._local_mutexes.append(mutex_uuid)  # save mutex uuid in request context

    @property
    def __mutex_uuid(self):
        """
        An uuid identifying the shared mutex to the mongodb document of which self is an representant uniquely
        :return: str
        """
        return "mutex_{}".format(self.uuid)

    def __del__(self):
        """
        Called, when instance is garbage collected. In Python >= 3.5, this happens when self's reference count reaches
         0. Because the first request context which accesses the PersistentObject with self.uuid creates a shared
         mutex in memcached, this method automatically releases the mutex, so that a mutex will never outlive the 
         request context.
        """
        mutex_uuid = self.__mutex_uuid
        if g:  # request context is still valid
            g._local_mutexes.remove(mutex_uuid)
        Client(['memcached']).delete(mutex_uuid)  # context is already destroyed, can't use framework

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
        """
        Returns self in dict representation. This representation is used to store all instances of cls in the 
        database. The returned representation will not contain any data yet.
        :return: dict
        """
        return {a.internal_name: None for _, a in cls.persistent_members().items()}


class PersistentAttribute(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the database persistent behavior of
    PersistentObject attributes. Use cls.attribute_name = PersistentAttribute(cls, "attribute_name") to add a
    database persistent attribute to some class cls.
    """

    def __init__(self, cls: type, name: str):
        """
        :param cls: type The class to which to add the attribute. This argument is needed to keep the target class
         aware of which PersistentAttributes exist, to automatically make subclasses of PersistentObject json
         serializable.
        :param name: str The name of the PersistentAttribute. This is how it will show up in the database and in json.
        """
        if not hasattr(cls, "persistent_attributes"):
            cls.persistent_attributes = dict({})  # let cls keep track of all persistent attributed
        cls.persistent_attributes[name] = self
        self.__external_name = name
        self.__name = "__persistent_attr_{}".format(name)

    @property
    def name(self):
        return self.__external_name

    @property
    def internal_name(self):
        """
        The name of the target classes internal attribute keeping track of the attributes value.
        Never use the internal attribute directly, instead use this descriptor class, or it's __get__() method.
        :return: 
        """
        return self.__name

    def __get__(self, obj, obj_type=None):
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)
        return value

    def __set__(self, obj: PersistentObject, value):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, value)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)


class PersistentReference(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the database persistent behavior of
    PersistentObject attributes, which are references to other PersistentObject.
    Use cls.attribute_name = PersistentAttribute(cls, "attribute_name", other_cls) to add a database persistent ref-
    erence to ome other PersistentObject.
    """

    def __init__(self, cls: type, name: str, other_class: type):
        """
        :param cls: type See documentation for PersistentAttribute.
        :param name: str See documentation for PersistentAttribute.
        :param other_class: type The class that is referenced by this attribute. Needed to instantiate other_class
        when this attribute is accessed.
        """
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
        """
        The name of the target classes internal attribute keeping track of the attributes value.
        Never use the internal attribute directly, instead use this descriptor class, or it's __get__() method.
        :return: 
        """
        return self.__name

    def __get__(self, obj, obj_type=None):
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)  # only stores uuid
        if value is None:
            return None
        return self.__other_class(value)  # instantiate referenced PersistentObject by it's uuid

    def __set__(self, obj: PersistentObject, value: PersistentObject):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        uuid = value.uuid  # store only the object's uuid
        obj._set_member(self.__name, uuid)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)


class PersistentReferenceList(object):
    """
    Emulate PyProperty_Type() in Objects/descrobject.c
    This class uses the descriptor pattern used in Python, to implement the database persistent behavior of
    PersistentObject attributes, which are lists of references to other PersistentObjects.
    Use cls.attribute_name = PersistentAttribute(cls, "attribute_name", other_cls) to add a database persistent ref-
    erence list to some other PersistentObject.
    """

    def __init__(self, cls: type, name: str, other_class: type):
        """
        :param cls: type See documentation for PersistentAttribute.
        :param name: str See documentation for PersistentAttribute.
        :param other_class: See documentation for PersistentReference
        """
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
        """
        The name of the target classes internal attribute keeping track of the attributes value.
        Never use the internal attribute directly, instead use this descriptor class, or it's __get__() method.
        :return: 
        """
        return self.__name

    def __get__(self, obj, obj_type=None):
        """
        Called when attribute is accessed.
        See Python's descriptor protocol.
        """
        if obj is None:
            return self

        value = getattr(obj, self.__name, None)  # stores list of uuids
        if not value:
            return []
        return [self.__other_class(uuid) for uuid in value]  # instantiate all referenced objects

    def __set__(self, obj: PersistentObject, value: List[PersistentObject]):
        """
        Called when attribute is set.
        See Python's descriptor protocol.
        """
        uuids = [e.uuid for e in value]
        obj._set_member(self.__name, uuids)

    def __delete__(self, obj):
        """
        Called when attribute is deleted.
        See Python's descriptor protocol.
        """
        obj._set_member(self.__name, None)
