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


class PersistentObject(object):

    __db = _db

    @classmethod
    def _collection(cls):
        return cls.__db[str(cls)[8:-2]]  # same as classname method


    def __init__(self, uuid: str=None):
        """
        TODO: lock object for duration of request
        :param uuid: str If passed, self will be a representant of the object with the given uuid
        """
        self.__id = None
        if uuid:
            document = self._collection().find_one({u'_id': ObjectId(uuid)})
            if not document:
                raise ObjectDoesntExistException("No PersistentObject with uuid {}".format(uuid))
            self.__from_document(document)
        else:
            self.__id = self._collection().insert_one(self.__as_dict()).inserted_id

    @property
    def uuid(self):
        """
        :return: str The universal & unique identifier of self 
        """
        return str(self.__id)

    @staticmethod
    def __key_to_internal(key: str) -> str:
        """
        Transforms a key (class member name) from external representation (ie. without leading _) to internal
        representation (ie. with leading _)
        :param key: str
        :return: str
        """
        return "_" + key

    @staticmethod
    def __to_internal_repr(obj_dict: dict) -> dict:
        """
        Transforms a PersistentObject's dict from external representation to internal representation:
         Members are exposed as properties, eg. obj.name, but are stored as self._name internally.
         External representation refers to the representation {'name': value}, while internal representation
         refers to {'_name': value}.
         Some members (namely id) can not be set by external methods and are thus stripped.
        :param obj_dict: dict A dict of object members
        :return: dict A dict of object members
        """
        def __key_is_valid(key: str) -> bool:
            if key.startswith("_"):
                return False
            elif key == "id":
                return False
            elif key == "uuid":
                return False
            return True

        return {PersistentObject.__key_to_internal(k): v for k, v in obj_dict.items() if __key_is_valid(k)}

    @staticmethod
    def __key_to_external(key: str) -> str:
        """
        Transforms key (name of a class member) from internal representation (ie. with leading _) to external
        representation (ie. without leading _)
        :param key: str
        :return: str
        """
        while key.startswith("_"):
            key = key[1:]  # strip leading _
        return key

    @staticmethod
    def __to_external_repr(obj_dict: dict) -> dict:
        """
        Transforms a PersistentObject's dict from internal representation to external representation:
        In external representation, dict keys are labeled the same as their property getters/setters.
        Per default, the internal member keys (eg. '_name' in {'_name': value}) are transformed from private
        member form to property names: _name -> name.
        Because this method is used on PersistentObject.__dict__, it also strips all truly private members
        like __id or __db.
        :param obj_dict: 
        :return: 
        """
        def  __key_is_valid(key: str) -> bool:
            if "__" in key:
                return False
            elif key == "_id":
                return False
            elif key == "_uuid":
                return False
            return key.startswith("_")

        return {PersistentObject.__key_to_external(k): v for k, v in obj_dict.items() if __key_is_valid(k)}


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

    def set_member(self, member, value):
        """
        Saves a field of self to the database.
        :param member: The member / field name
        :return: None
        """
        setattr(self, member, value)
        member = self.__key_to_external(member)
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

    def __from_dict(self, obj_dict: dict, write_back=True):
        """
        Helper function to initialize self from a member dict in external representation
        :param obj_dict: dict The dict containing the data to initialize from
        :param write_back: bool Whether data from obj_dict should be written to database on load
        :return: 
        """
        obj_dict = self.__to_internal_repr(obj_dict)

        if not write_back:
            self.__dict__.update(obj_dict)

        else:
            for k, v in obj_dict.items():
                self.set_member(k, v)

    def __from_document(self, document: dict):
        """
        Helper function to initialize self from mongodb document
        :param document: 
        :return: 
        """
        if not document:
            return
        self.__id = document['_id']
        self.__from_dict(document, write_back=False)

    def __as_dict(self) -> dict:
        """
        Returns data of self as dict in external representation.
        Used for serialization (storing to mongodb, to_json())
        :return: dict
        """
        return self.__to_external_repr(self.__dict__)

    def __box(self) -> dict:
        """
        Encapsulates data from __as_dict() in external representation within dict including metadata about self.
        Used for serialization (to_json)
        :return: dict A dict containing data of self including metadata 
        """
        return {'class': classname(self), 'uuid': self.uuid, 'fields': self.__as_dict()}

    def __unbox(self, boxed_dict: dict) -> dict:
        """
        Extract fields data from boxed_dict representation, also checks if classname and uuid match self to
        make it impossible to use unboxed data within the wrong instance and class.
        Boxing: see __box() and to_json()
        :param boxed_dict: A dict containing data of PersistentObject
        :return: 
        """
        if classname(self) != boxed_dict['class']:
            raise ClassnameMismatchException(
                "Tried to unbox PersistentObject {} with data of wrong class: {}".format(
                    classname(self), boxed_dict['class']))

        if self.uuid != boxed_dict['uuid']:
            raise UuidMismatchException(
                "Tried to unbox PersistentObject {} having uuid {} into Object having uuid {}".format(
                    boxed_dict['class'], boxed_dict['uuid'], self.uuid
                ))
        return boxed_dict['fields']

    def from_json(self, json_string: str):
        """
        Update PersistentObject from json representation, see to_json()
        :param json_string: str Json encoded PersistentObject
        :return: None
        """
        if type(json_string) is not str:
            raise TypeError
        boxed_dict = json.loads(json_string)
        obj_dict = self.__unbox(boxed_dict)
        self.__from_dict(obj_dict)

    def to_json(self) -> str:
        """
        Returns a json encoded version of self.
        The encoded version includes all persistent fields.
        If references to other PersistentObjects are stored, it is convention to store their uuid values only.
        The property some_obj.some_other_obj then becomes {..., 'some_other_obj_id': uuid}
        The encoded data is boxed inside a dict containing metadata on the object:
        {
            'class': ""  # full class path (eg. model.SomeModule.SomeClass),
            'uuid': ""  # the object's uuid,
            'fields': { ... }  # the object's persistent data 
        }
        :return: 
        """
        boxed_dict = self.__box()
        return json.dumps(boxed_dict)
