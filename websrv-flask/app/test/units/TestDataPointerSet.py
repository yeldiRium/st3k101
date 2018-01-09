from test import TestUnit
from test.units.TestDataObject import TestObject


class TestDataPointerSet(TestUnit):
    def default_to_empty_list(self):
        t = TestObject()

        self.test_assert(t.some_pointers == [], "Unset pointer set didn't default to []")

        t.remove()

    def persist_pointer_set(self):
        self.fail()
        t = TestObject()
        r = TestObject()
        t.some_reference = r

        # remove from singleton dict to really instantiate a new object
        del g._persistent_objects[t.uuid]

        t2 = TestObject(t.uuid)
        self.test_assert(t2.some_reference is r, "Reference wasn't persisted")

        t.remove()
        r.remove()

    def strong_reference_refcount(self):
        self.fail()
        t = TestObject()
        r = TestObject()
        m = TestObject()

        self.test_assert(t.ref_count == 0, "Newly created object 't' has nonzero refcount")
        self.test_assert(r.ref_count == 0, "Newly created object 'r' has nonzero refcount")
        self.test_assert(m.ref_count == 0, "Newly created object 'm' has nonzero refcount")

        t.some_strongref = r

        self.test_assert(t.ref_count == 0, "Object 't's refcount changed unexpectedly")
        self.test_assert(r.ref_count == 1, "Referenced object 'r' didn't increase refcount")
        self.test_assert(m.ref_count == 0, "Object 'm's refcount changed unexpectedly")

        t.some_strongref = m

        self.test_assert(t.ref_count == 0, "Object 't's refcount changed unexpectedly")
        self.test_assert(r.ref_count == 0, "Referenced object 'r' didn't decrease refcount")
        self.test_assert(m.ref_count == 1, "Referenced object 'm' didn't increase refcount")

        t.some_strongref = None

        self.test_assert(t.ref_count == 0, "Object 't's refcount changed unexpectedly")
        self.test_assert(r.ref_count == 0, "Object 'r's refcount changed unexpectedly")
        self.test_assert(m.ref_count == 0, "Referenced object 'm' didn't decrease refcount")

        t.remove()
        r.remove()
        m.remove()

    def weak_reference_refcount(self):
        self.fail()
        t = TestObject()
        r = TestObject()
        m = TestObject()

        self.test_assert(t.ref_count == 0, "Wek reference influenced objects 't' refcount")
        self.test_assert(r.ref_count == 0, "Wek reference influenced objects 'r' refcount")
        self.test_assert(m.ref_count == 0, "Wek reference influenced objects 'm' refcount")

        t.some_reference = r

        self.test_assert(t.ref_count == 0, "Wek reference influenced objects 't' refcount")
        self.test_assert(r.ref_count == 0, "Wek reference influenced objects 'r' refcount")
        self.test_assert(m.ref_count == 0, "Wek reference influenced objects 'm' refcount")

        t.some_reference = m

        self.test_assert(t.ref_count == 0, "Wek reference influenced objects 't' refcount")
        self.test_assert(r.ref_count == 0, "Wek reference influenced objects 'r' refcount")
        self.test_assert(m.ref_count == 0, "Wek reference influenced objects 'm' refcount")

        t.some_reference = None

        self.test_assert(t.ref_count == 0, "Wek reference influenced objects 't' refcount")
        self.test_assert(r.ref_count == 0, "Wek reference influenced objects 'r' refcount")
        self.test_assert(m.ref_count == 0, "Wek reference influenced objects 'm' refcount")

        t.remove()
        r.remove()
        m.remove()

    def cascading_delete(self):
        self.fail()
        t = TestObject()
        r = TestObject()
        m = TestObject()

        t.some_cascading_del_ref = r
        r.some_cascading_del_ref = m

        t.remove()

        self.test_assert(t.deleted, "Object couldn't be deleted")
        self.test_assert(r.deleted, "Cascading delete didn't delete linked object")
        self.test_assert(m.deleted, "Cascading delete didn't recursively delete linked objects")

    def cascading_delete_blocked_by_strongref(self):
        self.fail()
        t = TestObject()
        r = TestObject()
        m = TestObject()
        v = TestObject()
        o = TestObject()

        t.some_cascading_del_ref = r
        r.some_cascading_del_ref = m
        m.some_cascading_del_ref = v
        o.some_strongref = m

        t.remove()

        self.test_assert(t.deleted, "Object couldn't be deleted")
        self.test_assert(r.deleted, "Cascading delete didn't delete linked object")
        self.test_assert(not m.deleted, "Cascading delete deleted m despite existing strong pointer")
        self.test_assert(not v.deleted, "Cascading delete deleted v despite existing strong pointer")

        m.remove()
        v.remove()