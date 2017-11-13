from flask import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from framework.exceptions import ClassnameMismatchException, UuidMismatchException, ObjectDoesntExistException

_client = MongoClient("db-mongo")
_db = _client['efla-web']


def classname(o):
    """
    Resolves to model.modulename.classname
    :param o: object
    :return: str
    """
    return str(o.__class__)[8:-2]


class DefaultEncoder(object):

    @staticmethod
    def encode(o):
        fields = {k: v for k, v in o.__dict__.items() if not '__' in k}
        return {'classname': classname(o), 'fields': fields}


class DefaultDecoder(object):

    @staticmethod
    def decode(d):
        if not ('classname' in d and 'fields' in d):
            raise TypeError
        return d['fields']


class PersistentObject(object):

    __db = _db
    __collection = None
    __encoder = DefaultEncoder
    __decoder = DefaultDecoder


    @classmethod
    def _collection(cls):
        return cls.__db[str(cls)[8:2]]  # same as classname method


    def __init__(self, uuid: str=None):
        """
        TODO: lock object for duration of request
        :param query: 
        """
        self.__id = None
        if uuid:
            document = self._collection().find_one({u'_id': ObjectId(uuid)})
            if not document:
                raise ObjectDoesntExistException("No PersistentObject with uuid {}".format(uuid))
            self.__from_document(document)
            self.__id = ObjectId(uuid)
        else:
            self.__id = self._collection().insert_one(self.__encoder().encode(self)).inserted_id

    @property
    def uuid(self):
        return str(self.__id)

    def __from_document(self, document: dict):
        if not document:
            return
        self.__dict__.update(self.__decoder().decode(document))

    def as_json(self):
        as_dict = self.__encoder().encode(self)
        as_dict['uuid'] = self.uuid
        as_dict['fields'] = {k[1:]: v for k, v in as_dict['fields'].items()}
        return json.dumps(as_dict)

    def update_from_json(self, json_data: str):
        if type(json_data) is not str:
            raise TypeError

        as_dict = json.loads(json_data)
        fields = self.__decoder().decode(as_dict)

        if as_dict['classname'] != classname(self):
            raise ClassnameMismatchException(
                "Tried to update PersistentObject {} with data of wrong class: {}".format(
                    classname(self), as_dict['classname']))

        if as_dict['uuid'] != self.uuid:
            raise UuidMismatchException(
                "Tried to update PersistentObject {} having uuid {} with data of Object having uuid {}".format(
                    classname(self), self.uuid, as_dict['uuid']
                ))

        for k, v in {"_" + k: v for k, v in fields.items()}.items():
            self.set_member(k, v)

    def set_member(self, member, value):
        """
        Saves a field of self to the database.
        :param member: The member / field name
        :return: None
        """
        setattr(self, member, value)
        self._collection().update_one(
            {u'_id': self.__id},
            {u'$set': {'fields.{}'.format(member): value}}
        )

    def remove(self):
        self._collection().delete_one({u'_id': self.__id})


    @staticmethod
    def __transform_query(query: dict) -> dict:
        """
        Transforms mongodb filter dict from external representation (e.g. object.name)
        to internal representation (e.g. object.__name)
        :param query: dict A filter dictionary
        :return: dict Another filter dictionary
        """
        return {k.replace("__", ""): v for k, v in query.items()}


    @classmethod
    def one_from_query(cls, query: dict):
        """
        Returns one PersistentObject of class cls which matches query
        :param cls: The class of PersistentObject to find
        :param query: The query the object should match
        :return: PersistentObject The PersistentObject instance if found, None otherwise
        """
        query = cls.__transform_query(query)
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
        query = cls.__transform_query(query)
        documents = cls._collection().find(query)
        results = []

        for doc in documents:
            results.append(cls(doc['_id']))

        return results