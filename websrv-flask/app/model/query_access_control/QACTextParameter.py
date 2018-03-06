from flask import g

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataPointer import DataPointer
from framework.odm.DataString import DataString
from framework.internationalization import _
from model.I15dString import I15dString
from model.query_access_control.QACParameter import QACParameter

class QACTextParameter(QACParameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = _("This is a placeholder text, replace it to your liking.")


QACTextParameter.name = DataString(QACTextParameter, "name")
QACTextParameter.description = DataString(QACTextParameter, "description")
QACTextParameter.text = DataAttribute(QACTextParameter, "text")


class QACI15dTextParameter(QACParameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = I15dString()
        self.text.set_locale(_("This is a placeholder text, "
                               "replace it to your liking."), g._locale)


QACI15dTextParameter.name = DataString(QACI15dTextParameter, "name")
QACI15dTextParameter.description = DataString(QACI15dTextParameter, "description")
QACI15dTextParameter.text = DataPointer(QACI15dTextParameter, "text", I15dString)
