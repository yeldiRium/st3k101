from framework.odm.DataObject import DataObject
from framework.odm.DataString import DataString


class QACParameter(DataObject):
    readable_by_anonymous = True


QACParameter.name = DataString(QACParameter, "name")
QACParameter.description = DataString(QACParameter, "description")