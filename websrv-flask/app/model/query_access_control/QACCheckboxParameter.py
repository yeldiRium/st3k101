from framework.odm.DataAttribute import DataAttribute
from model.query_access_control.QACParameter import QACParameter


class QACCheckboxParameter(QACParameter):
    pass


QACCheckboxParameter.value = DataAttribute(QACCheckboxParameter, "value")
