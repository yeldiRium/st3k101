from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class DataSubject(DataObject):
    has_owner = False


DataSubject.confirmation_token = DataAttribute(DataSubject, "confirmation_token", serialize=False)
DataSubject.email_hash = DataAttribute(DataSubject, "email_hash")  # TODO hash this
DataSubject.ip_hash = DataAttribute(DataSubject, "ip_hash")
