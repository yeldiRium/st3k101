from typing import Iterator

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString, I18n
from model.query_access_control.QACParameter import QACParameter


class QACSelectParameter(QACParameter):

    exposed_properties = {
        "choices",
        "values"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_multi = False

    @property
    def choices(self) -> Iterator[I18n]:
        return (I18n(msgid) for msgid in self._choices)

    @choices.setter
    def choices(self, value: Iterator[I18n]):
        self._choices = [v.msgid for v in value]

    @property
    def values(self) -> Iterator[I18n]:
        return (I18n(msgid) for msgid in self._values)

    @values.setter
    def values(self, value):
        if all([type(v) == str for v in value]):  # argument is list of msgid's
            self._values = [I18n(n) for n in value]

        elif all([type(v) == I18n for v in value]):  # arg is (name, label)
            self._values = value


QACSelectParameter.name = DataString(QACSelectParameter, "name")
QACSelectParameter.description = DataString(QACSelectParameter, "description")
QACSelectParameter._choices = DataAttribute(QACSelectParameter, "_choices")
QACSelectParameter._values = DataAttribute(QACSelectParameter, "_values")
QACSelectParameter.allow_multi = DataAttribute(QACSelectParameter,
                                               "allow_multi")
