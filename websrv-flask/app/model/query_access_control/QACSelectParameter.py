from typing import Iterator, List

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
        if self.allow_multi is None:
            self.allow_multi = False

    @property
    def choices(self) -> Iterator[I18n]:
        return (I18n(msgid) for msgid in self._choices)

    @choices.setter
    def choices(self, values: List[I18n]):
        if not all([type(v) is I18n for v in values]):
            raise TypeError

        self._choices = [v.msgid for v in values]

    @property
    def values(self) -> Iterator[I18n]:
        return (I18n(msgid) for msgid in self._values)

    @values.setter
    def values(self, values: List[I18n]):
        if not self.allow_multi and len(values) > 1:
            raise ValueError("Only one choice is allowed")

        if not all([type(v) == I18n for v in values]):  # arg is list of (name, label)
            raise TypeError

        values = [v.msgid for v in values]
        self._values = values

    def set_values(self, values: List[str]):
        if not self.allow_multi and len(values) > 1:
            raise ValueError("Only one choice is allowed")

        if not all([type(v) == str for v in values]):  # arg is list of (name, label)
            raise TypeError

        self._values = values


QACSelectParameter.name = DataString(QACSelectParameter, "name")
QACSelectParameter.description = DataString(QACSelectParameter, "description")
QACSelectParameter._choices = DataAttribute(QACSelectParameter, "_choices",
                                            serialize=False)
QACSelectParameter._values = DataAttribute(QACSelectParameter, "_values",
                                           serialize=False)
QACSelectParameter.allow_multi = DataAttribute(QACSelectParameter,
                                               "allow_multi")
