from typing import List

from flask import request, render_template
from model.ODM.query_access_control.QACModule import QACModule

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from model.ODM.query_access_control.QACTextParameter import QACTextParameter

__author__ = "Noah Hummel, Hannes Leutloff"


class PasswordQAC(QACModule):
    """
    A QACModule which asks for a password when submitting answers to a 
    questionnaire.

    For a full documentation of the methods see model/qac/QACModule
    """

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
            if param.name == I18n("Password"):
                preshared_passphrase = param.text

        if preshared_passphrase is None:
            return [I18n("No password set.")]

        if preshared_passphrase == request.form["preshared_passphrase"]:
            return []

        return [I18n("Please enter the correct password to submit your "
                     "answers.")]

    @staticmethod
    def new() -> "PasswordQAC":
        # Set up params
        pass_qac_password = QACTextParameter.new("gandalf1")
        pass_qac_password.name = I18n("Password")
        pass_qac_password.description = I18n("The password that a DataSubject "
                                             "has to fill in to submit a "
                                             "survey.")

        # set up new qac instance
        the_new_qac = PasswordQAC()
        the_new_qac.name = I18n("Password")
        the_new_qac.description = I18n("Only let DataSubjects submit answers "
                                       "to surveys if they know the "
                                       "pre-shared password.")
        the_new_qac.parameters = {
            pass_qac_password
        }

        return the_new_qac


PasswordQAC.name = DataString(PasswordQAC, "name")
PasswordQAC.description = DataString(PasswordQAC, "description")
PasswordQAC.parameters = MixedDataPointerSet(PasswordQAC, "parameters")
