from pymongo.collection import Collection

__author__ = "Noah Hummel"

from pymongo import MongoClient

client = MongoClient('mongo')
db = client.xapi
collection: Collection = db.publications
