from typing import Tuple, Iterator

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataPointerSet import DataPointerSet
from model.I15dEnumElement import I15dEnumElement
from model.I15dString import I15dString
from model.query_access_control.QACParameter import QACParameter


class QACSelectParameter(QACParameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_multi = False

    @property
    def choices(self) -> Iterator[Tuple[str, str]]:
        return ((c.name, c.label) for c in self.i15d_choices)

    @property
    def values(self) -> Iterator[Tuple[str, str]]:
        return ((v.name, v.label) for v in self.i15d_values)

    @values.setter
    def values(self, value):
        if all([type(v) == str for v in value]):  # argument is list of names
            self.i15d_values = [I15dEnumElement.by_name(n) for n in value]

        elif all([type(v) == tuple for v in value]):  # arg is (name, label)
            self.i15d_values = [I15dEnumElement.by_name(n) for n, _ in value]



QACSelectParameter.i15d_choices = DataPointerSet(QACSelectParameter, "choices",
                                                 I15dEnumElement)
# Points to one or more elements of QACParameter.i15d_choices
QACSelectParameter.i15d_values = DataPointerSet(QACSelectParameter, "values",
                                           I15dString)
QACSelectParameter.allow_multi = DataAttribute(QACSelectParameter,
                                               "allow_multi")
