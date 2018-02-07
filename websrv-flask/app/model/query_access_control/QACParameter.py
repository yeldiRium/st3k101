from framework.odm.DataObject import DataObject
from framework.odm.DataString import DataString


class QACParameter(DataObject):
    pass


QACParameter.name = DataString(QACParameter, "name")
QACParameter.description = DataString(QACParameter, "description")