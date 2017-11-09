from flask import json
from pymongo import MongoClient
from bson.objectid import ObjectId

_client = MongoClient("db-mongo")


class PersistentObject(object):

    __client = _client

    __collection = None
    __encoder = None  # type: json.JSONEncoder
    __decoder = None  # type: json.JSONDecoder

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
