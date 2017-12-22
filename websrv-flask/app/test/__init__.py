import inspect
import pkgutil
from typing import List, Tuple, Any, Dict

import sys

from test import units


class TestAssertFailed(Exception):
    def __init__(self, message: str = None):
        super().__init__()
        self.message = message


class TestResult(object):
    def __init__(self, passed, message, case_name, unit_name:str=None):
        self.passed = passed
        self.message = message
        self.case_name = case_name
        self.unit_name = unit_name

    def as_dict(self) -> dict:
        return {
            "passed": self.passed,
            "message": self.message,
            "case_name": self.case_name,
            "unit_name": self.unit_name
        }


class TestUnit(object):

    def __init__(self):
        self.name = type(self).__name__

    def execute(self) -> List[TestResult]:
        test_cases = self.get_test_cases()
        results = []

        for name, case, case_self in test_cases:
            try:
                case(case_self)
                results.append(TestResult(True, "", name, self.name))

            except TestAssertFailed as a:
                results.append(TestResult(False, a.message, name, self.name))
            except Exception as e:
                results.append(TestResult(False, e.__repr__(), name, self.name))

        return results

    def get_test_cases(self) -> List[Tuple[str, Any]]:
        methods = inspect.getmembers(self.__class__, predicate=inspect.isfunction)  # type: List[Tuple[str, Any]]
        special_members = inspect.getmembers(TestUnit)  # type: List[Tuple[str, Any]]
        special_method_names = [sm[0] for sm in special_members]  # type: List[str]
        test_cases = []

        for name, method in methods:
            if name in special_method_names:
                continue
            test_cases.append((name, method, self))

        return test_cases

    @staticmethod
    def test_assert(predicate, failure_message):
        assert predicate is not None
        if not predicate:
            raise TestAssertFailed(failure_message)


def _discover_test_modules() -> List[Any]:

    modules = []

    package = units
    prefix = package.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        if ispkg:  # do not consider packages inside units, only modules
            continue
        module = __import__(modname, fromlist=["dummy"])
        modules.append(module)

    return modules


def _get_test_units(moedool) -> List[Any]:
    classes_in_module = inspect.getmembers(moedool, predicate=inspect.isclass)
    units = []
    for classname, cls in classes_in_module:
        if not issubclass(cls, TestUnit):
            continue
        if cls == TestUnit:
            continue
        units.append(cls())
    return units


def run_all() -> List[TestResult]:

    results = []

    tests_modules = _discover_test_modules()
    for mod in tests_modules:
        units = _get_test_units(mod)  # type: List[TestUnit]
        for u in units:
            unit_results = u.execute()  # type: List[TestResult]
            sorted_by_passed = sorted(unit_results, key=lambda res: res.passed)
            for res in sorted_by_passed:
                results.append(res.as_dict())

    return results