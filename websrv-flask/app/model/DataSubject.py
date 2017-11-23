from framework.odm.PersistentObject import PersistentObject, PersistentAttribute


class DataSubject(PersistentObject): pass


DataSubject.email = PersistentAttribute(DataSubject, "email")
