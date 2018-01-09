from flask import g

from framework.exceptions import ObjectDoesntExistException
from framework.memcached import get_memcache
from framework.odm import PointerType
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from test import TestUnit


class TestObject(DataObject): pass

# for testing DataAttribute
TestObject.some_attribute = DataAttribute(TestObject, "some_attribute")

# for testing DataPointer
TestObject.some_reference = DataPointer(TestObject, "some_reference", TestObject)
TestObject.some_strongref = DataPointer(TestObject, "some_strongref", TestObject, pointer_type=PointerType.STRONG)
TestObject.some_cascading_del_ref = DataPointer(TestObject, "some_cascading_del_ref", TestObject, cascading_delete=True)

# for testing DataPointerSet
TestObject.some_pointers = DataPointerSet(TestObject, "some_pointers", TestObject)
TestObject.some_strongptrs = DataPointerSet(TestObject, "some_strongprts", TestObject, pointer_type=PointerType.STRONG)
TestObject.some_cascading_del_ptrs = DataPointerSet(TestObject, "some_cascading_del_ptrs", TestObject, cascading_delete=True)


class TestDataObject(TestUnit):

    def create_new(self):
        t = TestObject()
        self.test_assert(len(t.uuid) > 5, "Object has no valid uuid")
        self.test_assert(t.ref_count == 0, "New Object has refcount != 0")

        mutex_uuid = "mutex_" + t.uuid
        self.test_assert(get_memcache().get(mutex_uuid), "Mutex wasn't acquired during __init__")

        t.remove()

    def remove(self):
        t = TestObject()
        uuid = t.uuid
        t.remove()

        mutex_uuid = "mutex_" + uuid
        self.test_assert(not get_memcache().get(mutex_uuid), "Mutex wasn't released")

        self.test_assert(uuid not in g._persistent_objects, "Singleton reference wasn't removed from local context")

        try:
            t = TestObject(uuid)
        except ObjectDoesntExistException:
            pass
        except Exception as e:
            raise e
        else:
            self.test_assert(False, "Object {} was deleted, but still exists.".format(uuid))

    def get_by_id(self):
        t = TestObject()
        uuid = t.uuid

        del t

        t = TestObject(uuid)
        self.test_assert(t.uuid == uuid, "Object created from uuid has wrong uuid")

        t.remove()

    def one_from_query(self):
        t = TestObject()
        t.some_attribute = "foobarbaz"
        uuid = t.uuid

        t2 = TestObject.one_from_query({"some_attribute": "foobarbaz"})
        t.remove()
        self.test_assert(t2.uuid == uuid, "Couldn't retrieve the correct object")

    def many_from_query(self):
        t1 = TestObject()
        t2 = TestObject()

        t1.some_attribute = "bazbarfoo"
        t2.some_attribute = "bazbarfoo"

        ts = TestObject.many_from_query({"some_attribute": "bazbarfoo"})

        self.test_assert(len(ts) == 2, "Couldn't find all matching objects")
        expected_uuids = [t1.uuid, t2.uuid]
        for t in ts:
            expected_uuids.remove(t.uuid)
        self.test_assert(len(expected_uuids) == 0, "Didn't find the correct objects")

        t1.remove()
        t2.remove()

    def is_singleton(self):
        t1 = TestObject()
        t1.some_attribute = "bar"
        t2 = TestObject(t1.uuid)
        t3 = TestObject.one_from_query({"some_attribute": "bar"})
        ts = TestObject.many_from_query({"some_attribute": "bar"})

        self.test_assert(t1 is t2, "After get by id: Not a singleton")
        self.test_assert(t1 is t3, "After one by query: Not a singleton")
        self.test_assert(all([ti is t1 for ti in ts]), "After many by query: Not a singleton")

        t1.remove()


