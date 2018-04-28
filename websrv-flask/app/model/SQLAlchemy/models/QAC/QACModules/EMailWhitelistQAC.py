from typing import Optional, List, Any, Pattern

import re
from deprecated import deprecated
from flask import request, render_template

from framework.internationalization import __, _
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from model.SQLAlchemy.models.QAC.QACTextParameter import QACTextParameter

__author__ = "Noah Hummel"


class EMailWhitelistQAC(QACModule):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_module.id'),
                   primary_key=True)
    __tablename__ = 'email_whitelist_qac'
    __mapper_args__ = {
        'polymorphic_identity': 'email_whitelist_qac'
    }

    # QACModule configuration
    __qac_id = __('Email Whitelist')
    __description = __('Only allows users with a certain email address '
                       '(for example a university issued address) to'
                       'submit. Not that this is only useful, when '
                       'email verification is also enabled.')

    def __init__(self, **kwargs):
        super(EMailWhitelistQAC, self).__init__(**kwargs)
        email_list = QACTextParameter(text='*@*.uni-frankfurt.de, '
                                           '*@uni-frankfurt.de, '
                                           '*@*.ou.nl, *@ou.nl, ')
        email_list.name = __('Email Whitelist')
        email_list.description = __('A comma separated list of email '
                                    'addresses which are allowed to '
                                    'submit. Wildcard expressions '
                                    'like *@uni-frankfurt.de are '
                                    'supported. (The example matches '
                                    'all email addresses that end in '
                                    '"@uni-frankfurt.de")')
        self.parameters.append(email_list)

    @staticmethod
    @deprecated(version='2.0', reason='Use EmailWhitelistQAC class constructor directly.')
    def new() -> 'EMailWhitelistQAC':
        return EMailWhitelistQAC()

    @staticmethod
    def parse_email_list(text: str) -> List[Pattern]:
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

    def set_config_value(self, param_id: str, value: Any):
        """
        Overridden to implement syntax checking when updating the email list
        For a full documentation of the method see model/qac/QACModule
        """
        super(EMailWhitelistQAC, self).set_config_value(param_id, value)
        try:
            whitelist = self.get_parameter_by_name('Email Whitelist')
            EMailWhitelistQAC.parse_email_list(whitelist)
        except Exception as e:
            reason = _('Unknown error.')
            if len(e.args) > 0:
                reason = e.args[0]
            return _("The submitted pattern contains errors: ") + reason

    def render_questionnaire_template(self, previous_errors: List[str]) -> str:
        return render_template('EmailQAC.html', error=previous_errors)

    def control(self) -> Optional[List[str]]:
        if 'email' not in request.form or not request.form['email']:
            return [_('Please enter your email address.')]
        email = request.form['email']
        whitelist = self.get_parameter_by_name('Email Whitelist').text
        regexes = EMailWhitelistQAC.parse_email_list(whitelist)

        if all((m is None for m in (r.match(email) for r in regexes))):
            return [_('You are not allowed to participate in this survey.')]
