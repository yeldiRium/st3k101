import random
import sys
import time
from typing import Any

from bson.objectid import ObjectId
from flask import g

from framework.exceptions import ObjectDoesntExistException, BadQueryException
from framework.memcached import get_memcache
from framework.mongodb import get_db
from framework.odm.UniqueObject import UniqueObject, UniqueHandle


class DataObject(UniqueObject, metaclass=UniqueHandle):
    @classmethod
    def _collection(cls):
        """
        Returns the name of the mongodb collection used for persisting instances of cls.
        The collection name will be Python's representation of the class name, including containing parent modules.
        This class, for example, will use 'model.PersistentObject.PersistentObject' as collection name.
        :return: str
        """
        db = get_db()
        return db[str(cls)[8:-2]]  # same as framework.classname(o) method

    def __init__(self, uuid: str = None):
        """
        :param uuid: str If passed, self will be a representant of the object with the given uuid. Important: If two
        instances of the same PersistentObject are created, the instances do not update each other, when values are
        changed. Only one request context may access the same uuid at once. As a consequence, the constructor may be 
        deferred until the database resource becomes available.
        """
        self.deleted = False
        self.initialized = False
        super().__init__(uuid)
        self.__memcached_client = get_memcache()

        if uuid:  # initialize self from mongodb document with the given uuid
            document = self._collection().find_one({u'_id': ObjectId(uuid)})
            if not document:
                raise ObjectDoesntExistException("No PersistentObject with uuid {}".format(uuid))
            self.__from_document(document)

        else:  # create a new mongodb document for self
            self._id = self._collection().insert_one(self._document_skeleton()).inserted_id
            setattr(self, "__ref_count", 0)

        # lock object by shared mutex in memcached while object is alive
        # only one app context may access a PersistentObject at a time.
        # This is used to prevent race conditions and data corruption between requests.
        mutex_uuid = self.__mutex_uuid  # string identifying mutex to PersistentObject with this self.uuid uniquely
        mutex_polling_time = g._config["SHARED_MUTEX_POLLING_TIME"]

        if hasattr(g, "_local_mutexes"):
            if mutex_uuid in g._local_mutexes:  # if this context has already acquired the mutex, don't acquire again
                return

        get_memcache().add(mutex_uuid, False)  # ensure key exists, doesn't set if already exists

        while True:  # until mutex is acquired

            mutex_locked, cas = get_memcache().get(mutex_uuid, get_cas=True)
            while mutex_locked:
                # wait random time to avoid deadlocks
                time.sleep(mutex_polling_time + random.uniform(0, mutex_polling_time / 10))
                mutex_locked, cas = get_memcache().get(mutex_uuid, get_cas=True)

            if not get_memcache().cas(mutex_uuid, True, cas):  # atomic write, if memcached wasn't modified
                continue  # atomic write failed

            break  # atomic write succeeded, mutex is acquired

        if not hasattr(g, "_local_mutexes"):
            g._local_mutexes = []
        g._local_mutexes.append(mutex_uuid)  # save mutex uuid in request context

        self.initialized = True

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
        if self.deleted:
            return
        if not self.initialized:
            return 
        mutex_uuid = self.__mutex_uuid
        if g:  # request context is still valid
            g._local_mutexes.remove(mutex_uuid)
        self.__memcached_client.delete(self.__mutex_uuid)  # context is already destroyed, can't use framework
        self.deleted = True

    def inc_refcount(self):
        count = getattr(self, "__ref_count")
        self._set_member("__ref_count", count + 1)

    def dec_refcount(self):
        count = getattr(self, "__ref_count")
        self._set_member("__ref_count", count - 1)
        #if self.ref_count == 0: TODO: optional flag autodelete
        #    print("Refcount of {} reached 0, deleting.".format(self.uuid), file=sys.stderr)
        #    self.remove()

    @property
    def ref_count(self):
        return getattr(self, "__ref_count")

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
            {u'_id': self._id},
            {u'$set': {member: value}}
        )

    def remove(self):
        """
        Removes the database entry represented by self from mongodb.
        :return: None
        """
        if self.ref_count > 0:
            return

        # TODO: Handle references and delete if cascading_delete
        if hasattr(self, "persistent_references"):
            for name, ref in self.persistent_references.items():

                other = None
                if ref.cascading_delete:  # get referenced obj if we need to delete it later
                    other = getattr(self, name)

                delattr(self, name)  # calls ref.__del__ to decrease ref count if necessary

                if other:
                    other.remove()  # do cascading delete

        if hasattr(self, "persistent_reference_sets"):
            for name, refset in self.persistent_reference_sets.items():

                others = []
                if refset.cascading_delete:
                    for other in getattr(self, name):
                        others.append(other)

                delattr(self, name)

                if others:
                    for other in others:
                        other.remove()

        self._collection().delete_one({u'_id': self._id})
        del g._persistent_objects[self.uuid]
        self.__del__() # TODO: called del here to free mutex, since object is gone now

    def __from_document(self, document: dict):
        """
        Helper function to initialize self from mongodb document
        :param document: 
        :return: 
        """
        if not document:
            return
        self._id = document['_id']
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

        if hasattr(cls, "persistent_reference_sets"):
            pers_attrs.update(cls.persistent_reference_sets)

        return pers_attrs

    @classmethod
    def _document_skeleton(cls) -> dict:
        """
        Returns self in dict representation. This representation is used to store all instances of cls in the 
        database. The returned representation will not contain any data yet.
        :return: dict
        """
        persistent_members = {a.internal_name: None for _, a in cls.persistent_members().items()}
        persistent_members.update({"__ref_count": 0})
        return persistent_members


