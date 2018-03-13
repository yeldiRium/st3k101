from framework.internationalization import _
from framework.odm.DataPointer import DataPointer
from framework.odm.DataString import DataString
from model.I15dString import I15dString
from model.query_access_control.QACParameter import QACParameter


class QACI15dTextParameter(QACParameter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def new(text:str=None) -> "QACI15dTextParameter":
        the_new_param = QACI15dTextParameter()
        if text is not None and type(text) is str:
            the_new_param.text = I15dString.new(text)
        else:
            the_new_param.text = I15dString.new(_("This is a placeholder text, "
                                                  "replace it to your liking."))
        return the_new_param

    def set_text(self, text):
        if type(text) is not str:
            raise TypeError

        self.text.set_locale(text)

QACI15dTextParameter.name = DataString(QACI15dTextParameter, "name")
QACI15dTextParameter.description = DataString(QACI15dTextParameter, "description")
QACI15dTextParameter.text = DataPointer(QACI15dTextParameter, "text",
                                        I15dString)