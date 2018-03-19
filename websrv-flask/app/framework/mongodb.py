from flask import g
from pymongo import MongoClient


def get_db() -> MongoClient:
    """
    Factory method for getting the appropriate MongoClient instance.
    Only instantiates one client per request.
    :return: MongoClient A MongoClient to access the mongodb 
    """
    client = getattr(g, "_mongodb", None)
    if client is None:
        client = g._mongodb = MongoClient(
            g._config["MONGODB_HOSTNAME"],
            username=g._config["MONGODB_USERNAME"],
            password=g._config["MONGODB_PASSWORD"],
            authSource=g._config["MONGODB_DATABASE"]
        )[g._config["MONGODB_DATABASE"]]
    return client
