from framework.internationalization import _
from framework.odm.DataPointer import DataPointer
from framework.odm.DataString import DataString
from model.I15dString import I15dString
from model.query_access_control.QACParameter import QACParameter


class QACI15dTextParameter(QACParameter):
    """
    A QACParameter which models an HTML text input, which also supports
    internationalized input.
    
    Wraps an I15dString (see docs/translating.md) with a name and a description
    for displaying in the frontend.
    
    To set this parameter in different languages, perform the API request to
    configure this parameter in a different language.
    """

    @staticmethod
    def new(text: str=None) -> "QACI15dTextParameter":
        """
        Factory method for QACI15dTextParameter to create a new instance with
        default values.
        :param text: str The initial text for the new QACI15dTextParameter
        :return: QACI15dTextParameter The newly created QACI15dTextParameter
        """
        the_new_param = QACI15dTextParameter()
        if text is not None and type(text) is str:
            the_new_param.text = I15dString.new(text)
        else:
            the_new_param.text = I15dString.new(_("This is a placeholder text, "
                                                  "replace it to your liking."))
        return the_new_param

    def set_text(self, text: str) -> None:
        """
        Setter for QACI15dTextParameter.text, type checks text and raises
        TypeError if check fails.
        
        To set this parameter in different languages, perform the API request to
        configure this parameter in a different language.
        :param text: str The new text for the QACI15dTextParameter
        :return: None
        """
        if type(text) is not str:
            raise TypeError

        self.text.set_locale(text)

QACI15dTextParameter.name = DataString(QACI15dTextParameter, "name")
QACI15dTextParameter.description = DataString(QACI15dTextParameter, "description")
QACI15dTextParameter.text = DataPointer(QACI15dTextParameter, "text",
                                        I15dString)