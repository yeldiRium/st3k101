from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class DataSubject(DataObject): pass


DataSubject.email = DataAttribute(DataSubject, "email")
