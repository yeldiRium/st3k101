from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString
from model.query_access_control.QACParameter import QACParameter


class QACCheckboxParameter(QACParameter):
    exposed_properties = {
        "value"
    }

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, le_value):
        if type(le_value) is not bool:
            raise TypeError

        self._value = le_value


QACCheckboxParameter.name = DataString(QACCheckboxParameter, "name")
QACCheckboxParameter.description = DataString(QACCheckboxParameter,
                                              "description")
QACCheckboxParameter._value = DataAttribute(QACCheckboxParameter, "_value",
                                            serialize=False)
