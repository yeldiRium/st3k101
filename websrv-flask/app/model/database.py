from flask import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from pydoc import safeimport


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
        fields = {k: v for k, v in o.__dict__.items() if not k.startswith("_")}
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
    _encoder = DefaultEncoder
    _decoder = DefaultDecoder

    def __init__(self, uuid: str):
        """
        TODO: lock object for duration of request
        :param query: 
        """
        self._id = None
        if uuid:
            self.__from_document(self.__collection.find_one({u'_id': ObjectId(uuid)}))

    @property
    def uuid(self):
        return str(self._id)

    def __from_document(self, document: dict):
        if not document:
            return
        self.__dict__.update(self.__decoder.decode(document))

    def set_member(self, member, value):
        """
        Saves a field of self to the database.
        :param member: The member / field name
        :return: None
        """
        setattr(self, member, value)
        coll = self.__client[self.__collection]
        coll.update_one(
            {u'_id': self._id},
            {u'$set': {member: self.__encoder.encode(value)}}
        )

    def save(self):
        """
        Saves all fields of object encoded by __encoder, does not discriminate
        between changed and unchanged fields, but instead replaces whole document
        :return: None
        """
        coll = self.__client[self.__collection]
        if not self._id:
            self._id = coll.insert_one(self.__encoder.encode(self)).inserted_id
        else:
            coll.replace_one({u'_id': self._id}, self.__encoder.encode(self))

    def remove(self):
        coll = self.__client[self.__collection]
        coll.delete_one({u'_id': self._id})
