from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.Survey import Survey


class DataClient(DataObject): pass


DataClient.email = DataAttribute(DataClient, "email")
DataClient.activated = DataAttribute(DataClient, "activated")
DataClient.password_salt = DataAttribute(DataClient, "password_salt")
DataClient.password_hash = DataAttribute(DataClient, "password_hash")
DataClient.surveys = DataPointerSet(DataClient, "surveys", Survey)