from pymongo.collection import Collection

__author__ = "Noah Hummel"

from pymongo import MongoClient

client = MongoClient('mongo', connect=False)
db = client.xapi
collection: Collection = db.publications
