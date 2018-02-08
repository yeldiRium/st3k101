from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString
from model.query_access_control.QACParameter import QACParameter


class QACCheckboxParameter(QACParameter):
    pass


QACCheckboxParameter.name = DataString(QACCheckboxParameter, "name")
QACCheckboxParameter.description = DataString(QACCheckboxParameter,
                                              "description")
QACCheckboxParameter.value = DataAttribute(QACCheckboxParameter, "value")
