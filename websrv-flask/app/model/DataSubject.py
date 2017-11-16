from model.PersistentObject import PersistentObject, PersistentAttribute


class DataSubject(PersistentObject): pass


DataSubject.email = PersistentAttribute(DataSubject, "email")
