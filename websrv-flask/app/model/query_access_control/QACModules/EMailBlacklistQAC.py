from typing import List, Any

from flask import request, render_template

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACModules import EMailWhitelistQAC
from model.query_access_control.QACTextParameter import QACTextParameter

__author__ = "Noah Hummel, Hannes Leutloff"


class EMailBlacklistQAC(QACModule):
    """
    A QACModule which matches the DataSubject's email address against a list
    of forbidden emails when submitting answers to a questionnaire.
    
    For a full documentation of the methods see model/qac/QACModule
    """

    def set_config_value(self, param_uuid: str, value: Any):
        """
        Overridden to implement syntax checking when updating the email list

        For a full documentation of the method see model/qac/QACModule
        """
        super().set_config_value(param_uuid, value)
        try:
            EMailWhitelistQAC._parse_email_list(next(self.parameters.__iter__()).text)
        except Exception as e:
            reason = _("Unknown error")
            if len(e.args) > 0:
                reason = e.args[0]

            return _("The submitted pattern contains errors: ") + reason

    def render_questionnaire_template(self, previous_errors: List[I18n]) -> str:
        return render_template("EmailQAC.html", error=[e.text for e in previous_errors])

    def control(self) -> List[I18n]:
        if 'email' not in request.form:
            return [I18n("Please enter your email address.")]
        if not request.form['email']:
            return [I18n("Please enter your email address.")]

        email = request.form['email']
        email_list_str = next(self.parameters.__iter__()).text
        regexes = EMailWhitelistQAC._parse_email_list(email_list_str)

        if any((m is not None for m in (r.match(email) for r in regexes))):
            return [I18n("This email address is not allowed to participate "
                         "in this survey.")]

        return []

    @staticmethod
    def new() -> "EMailBlacklistQAC":
        email_list_str = QACTextParameter.new("")
        email_list_str.name = I18n("Email Blacklist")
        email_list_str.description = I18n("A comma separated list of email "
                                          "addresses which are not allowed when "
                                          "submitting a survey. Wildcard "
                                          "expressions like *@uni-frankfurt.de "
                                          "are also supported.")

        the_new_qac = EMailBlacklistQAC()
        the_new_qac.name = I18n("Email Blacklist")
        the_new_qac.description = I18n("Block users with a certain email "
                                       "address from submitting answers.")

        the_new_qac.parameters = {
            email_list_str
        }

        return the_new_qac


EMailBlacklistQAC.name = DataString(EMailBlacklistQAC, "name")
EMailBlacklistQAC.description = DataString(EMailBlacklistQAC, "description")
EMailBlacklistQAC.parameters = MixedDataPointerSet(EMailBlacklistQAC,
                                                   "parameters")
