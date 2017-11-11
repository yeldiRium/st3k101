from flask import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from framework.exceptions import ClassnameMismatchException, UuidMismatchException

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
        fields = {k: v for k, v in o.__dict__.items() if not 'internal_' in k}
        return {'classname': classname(o), 'fields': fields}


class DefaultDecoder(object):

    @staticmethod
    def decode(d):
        if not ('classname' in d and 'fields' in d):
            raise TypeError
        return d['fields']


class PersistentObject(object):

    __internal_db = _db
    __internal_collection = None
    _internal_encoder = DefaultEncoder
    _internal_decoder = DefaultDecoder

    def __init__(self, uuid: str=None):
        """
        TODO: lock object for duration of request
        :param query: 
        """
        self._internal_id = None
        self.__internal_collection = self.__internal_db[classname(self)]
        if uuid:
            self.__from_document(self.__internal_collection.find_one({u'_id': ObjectId(uuid)}))
            self._internal_id = ObjectId(uuid)

    @property
    def uuid(self):
        return str(self._internal_id)

    def __from_document(self, document: dict):
        if not document:
            return
        self.__dict__.update(self._internal_decoder().decode(document))

    def as_json(self):
        as_dict = self._internal_encoder().encode(self)
        as_dict['uuid'] = self.uuid
        return json.dumps(as_dict)

    def update_from_json(self, json_data: str):
        if type(json_data) is not str:
            raise TypeError

        as_dict = json.loads(json_data)
        as_dict = self._internal_decoder().decode(as_dict)

        if as_dict['classname'] is not classname(self):
            raise ClassnameMismatchException(
                "Tried to update PersistentObject {} with data of wrong class: {}".format(
                    classname(self), as_dict['classname']))

        if as_dict['uuid'] is not self.uuid:
            raise UuidMismatchException(
                "Tried to update PersistentObject {} having uuid {} with data of Object having uuid {}".format(
                    classname(self), self.uuid, as_dict['uuid']
                ))

        del as_dict['uuid']
        self.__from_document(as_dict)

    def set_member(self, member, value):
        """
        Saves a field of self to the database.
        :param member: The member / field name
        :return: None
        """
        setattr(self, member, value)
        self.__internal_collection.update_one(
            {u'_id': self._internal_id},
            {u'$set': {'fields.{}'.format(member): value}}
        )

    def save(self):
        """
        Saves all fields of object encoded by __encoder, does not discriminate
        between changed and unchanged fields, but instead replaces whole document
        :return: None
        """
        if not self._internal_id:
            self._internal_id = self.__internal_collection.insert_one(self._internal_encoder().encode(self)).inserted_id
        else:
            self.__internal_collection.replace_one({u'_id': self._internal_id}, self._internal_encoder().encode(self))

    def remove(self):
        self.__internal_collection.delete_one({u'_id': self._internal_id})
