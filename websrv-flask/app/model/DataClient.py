from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReferenceSet
from model.Survey import Survey


class DataClient(PersistentObject): pass


DataClient.email = PersistentAttribute(DataClient, "email")
DataClient.activated = PersistentAttribute(DataClient, "activated")
DataClient.password_salt = PersistentAttribute(DataClient, "password_salt")
DataClient.password_hash = PersistentAttribute(DataClient, "password_hash")
DataClient.surveys = PersistentReferenceSet(DataClient, "surveys", Survey)