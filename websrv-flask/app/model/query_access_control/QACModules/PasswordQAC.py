from typing import Any, List

from flask import request, render_template

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACTextParameter import QACTextParameter


class PasswordQAC(QACModule):

    def set_config_value(self, param_uuid: str, value: Any):
        updated = False

        for param in self.parameters:
            if param_uuid != param.uuid:
                continue

            if type(param) is QACTextParameter:
                if type(value) is not str:
                    return _("QACParameter has wrong type")

                param.text = value
                updated = True

        if not updated:
            return _("QACParameter not found")

    def render_questionnaire_template(self, previous_errors: List[I18n]):
        return render_template(
            "PasswordQAC.html",
            error=[e.text for e in previous_errors]
        )

    def control(self) -> List[I18n]:
        if 'preshared_passphrase' not in request.form:
            return [I18n("Missing pre-shared password.")]

        preshared_passphrase = None

        for param in self.parameters:
            if param.name == I18n("Pre-shared Password"):
                preshared_passphrase = param.text

        if preshared_passphrase is None:
            return [I18n("No password set.")]

        if preshared_passphrase == request.form["preshared_passphrase"]:
            return []

        return [I18n("Wrong password.")]

    @staticmethod
    def new() -> "PasswordQAC":
        # Set up params
        pass_qac_password = QACTextParameter()
        pass_qac_password.name = I18n("Pre-shared Password")
        pass_qac_password.description = I18n("The password that a DataSubject"
                                             "has to fill in to submit a"
                                             "survey.")
        pass_qac_password.text = "gandalf1"

        # set up new qac instance
        the_new_qac = PasswordQAC()
        the_new_qac.name = I18n("Password check")
        the_new_qac.description = I18n("Only let DataSubjects submit answers "
                                       "to surveys, if they know the "
                                       "pre-shared password.")
        the_new_qac.parameters = {
            pass_qac_password
        }

        return the_new_qac


PasswordQAC.name = DataString(PasswordQAC, "name")
PasswordQAC.description = DataString(PasswordQAC, "description")
PasswordQAC.parameters = MixedDataPointerSet(PasswordQAC, "parameters")
