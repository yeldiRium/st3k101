from framework.odm.DataAttribute import DataAttribute
from model.query_access_control.QACParameter import QACParameter


class QACTextParameter(QACParameter):
    pass


QACTextParameter.value = DataAttribute(QACTextParameter, "value")
