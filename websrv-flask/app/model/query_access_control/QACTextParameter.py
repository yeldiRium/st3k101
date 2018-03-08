from flask import g

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataPointer import DataPointer
from framework.odm.DataString import DataString
from framework.internationalization import _
from model.I15dString import I15dString
from model.query_access_control.QACParameter import QACParameter


class QACTextParameter(QACParameter):

    exposed_properties = {
        "text"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._text is None:
            self._text = _("This is a placeholder text, replace it to your "
                           "liking.")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        if type(text) is not str:
            raise TypeError

        self._text = text


QACTextParameter.name = DataString(QACTextParameter, "name")
QACTextParameter.description = DataString(QACTextParameter, "description")
QACTextParameter._text = DataAttribute(QACTextParameter, "_text",
                                       serialize=False)


class QACI15dTextParameter(QACParameter):

    exposed_properties = {
        "text"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._text is None:
            self._text = I15dString()
            self._text.set_locale(_("This is a placeholder text, replace it to "
                                   "your liking."))

        @property
        def text(self):
            return self._text

        @text.setter
        def text(self, text: str):
            if type(text) is not str:
                raise TypeError

            self._text.set_locale(text)


QACI15dTextParameter.name = DataString(QACI15dTextParameter, "name")
QACI15dTextParameter.description = DataString(QACI15dTextParameter, "description")
QACI15dTextParameter._text = DataPointer(QACI15dTextParameter, "_text",
                                         I15dString, serialize=False)
