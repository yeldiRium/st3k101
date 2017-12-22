import inspect

from test import TestUnit

class OneSimpleTest(TestUnit):
    """
    The mother of all tests ;)
    """

    def one_simple_testcase(self):
        self.test_assert(True == True, "Better get yourself a new set of axioms")

    def one_simple_failing_testcase(self):
        self.test_assert(True == False, "Things are in order.")

    def fail_a(self):
        self.test_assert("h" not in "nämlich", "Wer nämlich mit h schreibt ist dämlich.")

    def fail_b(self):
        self.test_assert(issubclass(type((i for i in [1,2,3])), type([1,2,3])), "Get it?")

    def pass_a(self):
        self.test_assert(hasattr(inspect, "getmembers"), "Duck typing is love.")

    def pass_b(self):
        self.test_assert(not [n for n in [1, 2, 3, 4, 5] if 17 % n ==  0], "~~(//)8>")


class TwoSimpleTest(TestUnit):
    """
    This is madness!
    """

    def one_simple_testcase(self):
        self.test_assert(True == True, "Better get yourself a new set of axioms")

    def one_simple_failing_testcase(self):
        self.test_assert(True == False, "Things are in order.")

    def fail_a(self):
        self.test_assert("h" not in "nämlich", "Wer nämlich mit h schreibt ist dämlich.")

    def fail_b(self):
        self.test_assert(issubclass(type((i for i in [1,2,3])), type([1,2,3])), "Get it?")

    def pass_a(self):
        self.test_assert(hasattr(inspect, "getmembers"), "Duck typing is love.")

    def pass_b(self):
        self.test_assert(not [n for n in [1, 2, 3, 4, 5] if 17 % n ==  0], "~~(//)8>")
