from framework.internationalization import _
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString
from model.query_access_control.QACParameter import QACParameter


class QACTextParameter(QACParameter):

    @staticmethod
    def new(text:str=None) -> "QACTextParameter":
        the_new_param = QACTextParameter()
        if text is not None and type(text) is str:
            the_new_param.text = text
        else:
            the_new_param.text = _("This is a placeholder text, replace it to "
                                   "your liking.")
        return the_new_param

    def set_text(self, text):
        if type(text) is not str:
            raise TypeError

        self.text = text


QACTextParameter.name = DataString(QACTextParameter, "name")
QACTextParameter.description = DataString(QACTextParameter, "description")
QACTextParameter.text = DataAttribute(QACTextParameter, "text")
