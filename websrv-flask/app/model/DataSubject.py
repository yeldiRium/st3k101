from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class DataSubject(DataObject):
    has_owner = False


DataSubject.email = DataAttribute(DataSubject, "email")
