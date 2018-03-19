from framework.internationalization import _
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString
from model.query_access_control.QACParameter import QACParameter

__author__ = "Noah Hummel, Hannes Leutloff"


class QACTextParameter(QACParameter):
    """
    A QACParameter that models an HTML text input.
    """

    @staticmethod
    def new(text:str=None) -> "QACTextParameter":
        """
        Factory method for creating a new QACTextParameter with default values.
        :param text: str The text value the parameter will be set to initially
        :return: QACTextParameter The newly created QACTextParameter
        """
        the_new_param = QACTextParameter()
        if text is not None and type(text) is str:
            the_new_param.text = text
        else:
            the_new_param.text = _("This is a placeholder text, replace it to "
                                   "your liking.")
        return the_new_param

    def set_text(self, text: str) -> None:
        """
        Setter for QACTextParameter.text
        :param text: str The new text for the QACTextParameter
        :return: None
        """
        if type(text) is not str:
            raise TypeError

        self.text = text


QACTextParameter.name = DataString(QACTextParameter, "name")
QACTextParameter.description = DataString(QACTextParameter, "description")
QACTextParameter.text = DataAttribute(QACTextParameter, "text")
