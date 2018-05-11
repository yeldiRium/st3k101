from typing import Optional, List, Any

from deprecated import deprecated
from flask import render_template, request

from framework.internationalization import __, _
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from model.SQLAlchemy.models.QAC.QACModules.EMailWhitelistQAC import EMailWhitelistQAC
from model.SQLAlchemy.models.QAC.QACTextParameter import QACTextParameter

__author__ = "Noah Hummel"


class EMailBlacklistQAC(QACModule):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_module.id'),
                   primary_key=True)
    __tablename__ = 'email_blacklist_qac'
    __mapper_args__ = {
        'polymorphic_identity': 'email_blacklist_qac'
    }

    # QACModule configuration
    _qac_id = __('Email Blacklist')
    _description = __('Blocks users with a certain email address from '
                       'submitting. Not that this is only useful when '
                       'email verification is also enabled.')

    def __init__(self, **kwargs):
        super(EMailBlacklistQAC, self).__init__(**kwargs)
        blacklist = QACTextParameter(text='*@em.uni-frankfurt.de')
        blacklist.name = __('Email Blacklist')
        blacklist.description = __('A comma separated list of email '
                                   'addresses which are not allowed '
                                   'to submit. Wildcard expressions '
                                   'like *@em.uni-frankfurt.de '
                                   'are supported. (The example '
                                   'matches any email address ending '
                                   'with "@em.uni-frankfurt.de".)')
        self.parameters.append(blacklist)

    @staticmethod
    @deprecated(version='2.0', reason='Use EMailBlacklistQAC class constructor directly.')
    def new() -> 'EMailBlacklistQAC':
        return EMailBlacklistQAC()

    def set_config_value(self, param_id: str, value: Any):
        """
        Overridden to implement syntax checking when updating the email list
        For a full documentation of the method see model/qac/QACModule
        """
        super(EMailBlacklistQAC, self).set_config_value(param_id, value)
        blacklist = self.get_parameter_by_name('Email Blacklist').text
        try:
            EMailWhitelistQAC.parse_email_list(blacklist)
        except Exception as e:
            reason = _("Unknown error")
            if len(e.args) > 0:
                reason = e.args[0]
            return _("The submitted pattern contains errors: ") + reason

    def render_questionnaire_template(self, previous_errors: List[str]) -> str:
        return render_template('EmailQAC.html', error=previous_errors)

    def control(self) -> Optional[List[str]]:
        if 'email' not in request.form or not request.form['email']:
            return [_('Please enter your email address.')]
        email = request.form['email']
        blacklist = self.get_parameter_by_name('Email Blacklist').text
        regexes = EMailWhitelistQAC.parse_email_list(blacklist)

        if any((m is not None for m in (r.match(email) for r in regexes))):
            return [_('You are not allowed to participate in this survey.')]
