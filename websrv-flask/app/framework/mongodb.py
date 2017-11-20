from flask import g
from pymongo import MongoClient


def get_db():
    client = MongoClient(
        g._config["MONGODB_HOSTNAME"],
        username=g._config["MONGODB_USERNAME"],
        password=g._config["MONGODB_PASSWORD"],
        authSource=g._config["MONGODB_DATABASE"]
    )  # the database server
    return client[g._config["MONGODB_DATABASE"]]  # the database used for persisting objects
