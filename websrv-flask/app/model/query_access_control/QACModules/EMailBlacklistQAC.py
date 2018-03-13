import re
from typing import List, Any

from flask import request

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACModules import EMailWhitelistQAC
from model.query_access_control.QACTextParameter import QACTextParameter


class EMailBlacklistQAC(QACModule):

    def set_config_value(self, param_uuid: str, value: Any):
        super().set_config_value(param_uuid, value)
        try:
            EMailWhitelistQAC._parse_email_list(next(self.parameters).text)
        except Exception as e:
            reason = _("Unknown error")
            if len(e.args) > 0:
                reason = e.args[0]

            return _("The submitted pattern contains errors: ") + reason

    def render_questionnaire_template(self, previous_errors: List[I18n]) -> str:
        return ""

    def control(self) -> List[I18n]:
        if 'email' not in request.form:
            return [I18n("Please enter your email address.")]
        if not request.form['email']:
            return [I18n("Please enter your email address.")]

        email = request.form['email']
        email_list_str = next(self.parameters).text
        regexes = EMailWhitelistQAC._parse_email_list(email_list_str)

        if any((m is not None for m in (r.match(email) for r in regexes))):
            return [I18n("This email address is not allowed to participate"
                         "in this survey.")]

        return []

    @staticmethod
    def new() -> "EMailBlacklistQAC":
        email_list_str = QACTextParameter.new("")
        email_list_str.name = I18n("List of disallowed E-Mail addresses")
        email_list_str.description = I18n("A comma separated list of email"
                                          "addresses which are not allowed when"
                                          "submitting a survey. Wildcard"
                                          "expressions like *@uni-frankfurt.de"
                                          "are also supported.")

        the_new_qac = EMailBlacklistQAC()
        the_new_qac.name = I18n("Email blacklist")
        the_new_qac.description = I18n("Block users with a certain email"
                                       "address from submitting answers.")

        the_new_qac.parameters = {
            email_list_str
        }

        return the_new_qac


EMailBlacklistQAC.name = DataString(EMailBlacklistQAC, "name")
EMailBlacklistQAC.description = DataString(EMailBlacklistQAC, "description")
EMailBlacklistQAC.parameters = MixedDataPointerSet(EMailBlacklistQAC,
                                                   "parameters")
