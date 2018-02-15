from typing import List, Optional

from framework.internationalization import _
from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet

from model.query_access_control.QACModule import QACModule
from flask import request, render_template, g

from model.query_access_control.QACTextParameter import QACI15dTextParameter



class TOSQAC(QACModule):

    def set_config_value(self, param_uuid: str, value: str) -> Optional[str]:
        """
        Sets a QACParameter of the QACModule.
        :param param_uuid: str The QACParameter.uuid of the parameter to set
        :param value: str The value (as given by the user in http serialized
        form) to set the parameter to
        :returns: Optional[str] An error message, if the config param couldn't
        be set for some reason
        """
        updated = False

        for param in self.parameters:
            if param.uuid != param_uuid:
                continue

            if type(param) is QACI15dTextParameter:
                if type(value) is not str:
                    return  _("QACParameter has wrong type")

                param.text.add_locale(g._locale, value)
                updated = True

        if not updated:
            return _("QACParameter not found")

    def render_questionnaire_template(self, errors: List[I18n]) -> str:

        agb_agreement_text = None

        for param in self.parameters:
            if param.name.msgid == "TOS Text":
                agb_agreement_text = param.text.get()

        return render_template(
            "TOSQAC.html",
            error=[e.text for e in errors],
            agb_agreement_text=agb_agreement_text
        )

    def control(self) -> List[I18n]:
        """
        Tests the flask request parameters against the persisted config params.
        Returns a list of all found errors in user-readable form, so that they
        can be displayed as an error message.
        An empty list means there was no error.
        """
        if 'tos' not in request.form or not request.form['tos']:
                return [I18n("Please accept the terms of service.")]

        return []

    @staticmethod
    def new() -> "TOSQAC":
        """
        :return: A new instance of le QAC, avec les defaults
        """

        # Set up parameters for QAC
        tos_text = QACI15dTextParameter()
        tos_text.name = I18n("TOS Text")
        tos_text.description = I18n("The text that is displayed to the user "
                                    "as the terms of service.")

        # Set up new QAC instance
        the_new_qac = TOSQAC()
        the_new_qac.name = I18n("TOS")
        the_new_qac.description = I18n("Display a terms of service text to "
                                       "the user when they submit a survey. "
                                       "The user has to agree to the terms of "
                                       "service before a survey can be "
                                       "submitted.")

        the_new_qac.parameters = { # Add parameters to new instance
            tos_text
        }

        return the_new_qac


TOSQAC.name = DataString(TOSQAC, "name")
TOSQAC.description = DataString(TOSQAC, "description")
TOSQAC.parameters = MixedDataPointerSet(TOSQAC, "parameters")