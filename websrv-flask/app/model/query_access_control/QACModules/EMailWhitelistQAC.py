import re
from typing import List, Any

from flask import request, render_template

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _
from model.query_access_control.QACModule import QACModule
from model.query_access_control.QACTextParameter import QACTextParameter

__author__ = "Noah Hummel, Hannes Leutloff"


class EMailWhitelistQAC(QACModule):
    """
    A QACModule which matches the DataSubject's email address against a list
    of allowed email addresses. The list of allowed email addresses supports
    wildcard expressions like *@*.uni-frankfurt.de.

    For a full documentation of the methods see model/qac/QACModule
    """

    @staticmethod
    def _parse_email_list(text: str) -> List[re._pattern_type]:
        """
        Helper method to parse the user submitted list of allowed emails.
        Checks syntax and builds regex patterns from the list.
        :param text: str The user submitted list of allowed emails
        :return: List[re.pattern] A list of regex patterns which match allowed
                                  email addresses
        """
        # separate comma separated list and strip whitespace between commas
        entries = list(map(str.strip, text.split(",")))

        # if whitespace is found in entries, it's not valid syntax
        if any((" " in e for e in entries)):
            raise ValueError(_("Whitespace in email address."))

        patterns = []

        def to_regex(part):
            if part == "*":
                return ".*"
            else:
                return re.escape(part)

        for e in entries:
            # split wildcard portions from rest of email
            expr = filter(lambda x: x, e.replace("*", ",*,").split(","))
            # escape normal portions, build regex for wildcards
            expr = map(to_regex, expr)
            # concat
            expr = "".join(expr)
            # add string delimiters to pattern
            expr = "^" + expr + "$"
            pattern = re.compile(expr)
            patterns.append(pattern)

        return patterns

    def set_config_value(self, param_uuid: str, value: Any):
        """
        Overridden to implement syntax checking when updating the email list

        For a full documentation of the method see model/qac/QACModule
        """
        super().set_config_value(param_uuid, value)
        try:
            self._parse_email_list(next(self.parameters.__iter__()).text)
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
        regexes = self._parse_email_list(next(self.parameters.__iter__()).text)

        if all((m is None for m in (r.match(email) for r in regexes))):
            return [I18n("This email address is not allowed to participate "
                         "in this survey.")]

        return []

    @staticmethod
    def new() -> "EMailWhitelistQAC":
        email_list_str = QACTextParameter.new("*@*.*")
        email_list_str.name = I18n("Email Whitelist")
        email_list_str.description = I18n("A comma separated list of email "
                                          "addresses which are allowed when "
                                          "submitting a survey. Wildcard "
                                          "expressions like *@uni-frankfurt.de "
                                          "are also supported.")

        the_new_qac = EMailWhitelistQAC()
        the_new_qac.name = I18n("Email Whitelist")
        the_new_qac.description = I18n("Only allow users with a certain email "
                                       "address to submit answers.")

        the_new_qac.parameters = {
            email_list_str
        }

        return the_new_qac


EMailWhitelistQAC.name = DataString(EMailWhitelistQAC, "name")
EMailWhitelistQAC.description = DataString(EMailWhitelistQAC, "description")
EMailWhitelistQAC.parameters = MixedDataPointerSet(EMailWhitelistQAC,
                                                   "parameters")
