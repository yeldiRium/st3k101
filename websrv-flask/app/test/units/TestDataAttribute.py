from flask import g

from test import TestUnit
from test.units.TestDataObject import TestObject


class TestDataAttribute(TestUnit):

    def default_to_none(self):
        t = TestObject()

        self.test_assert(t.some_attribute is None, "Unset attribute didn't default to None")

        t.remove()

    def persist_attribute(self):
        t1 = TestObject()
        t1.some_attribute = "we'll meet again"

        # remove from singleton dict to really instantiate a new object
        del g._persistent_objects[t1.uuid]

        t2 = TestObject(t1.uuid)
        self.test_assert(t2.some_attribute == "we'll meet again", "Attribute was not persisted")

        t2.remove()