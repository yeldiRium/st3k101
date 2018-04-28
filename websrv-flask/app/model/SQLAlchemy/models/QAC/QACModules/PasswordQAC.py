from typing import List

from deprecated import deprecated
from flask import render_template, request

from framework.internationalization import __, _
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACModule import QACModule
from model.SQLAlchemy.models.QAC.QACTextParameter import QACTextParameter

__author__ = "Noah Hummel"


class PasswordQAC(QACModule):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_module.id'),
                   primary_key=True)
    __tablename__ = 'password_qac'
    __mapper_args__ = {
        'polymorphic_identity': 'password_qac'
    }

    # QACModule configuration
    __qac_id = __('Password')
    __description = __('Prompts the user to enter a password '
                       'before they may submit their answers.')

    def __init__(self, **kwargs):
        super(PasswordQAC, self).__init__(**kwargs)
        password = QACTextParameter(text='gandalf1')
        password.name = __('Password')
        password.description = __('The password the user has to enter before '
                                  'submitting.')
        self.parameters.append(password)

    @staticmethod
    @deprecated(version='2.0', reason='Use PasswordQAC class constructor directly.')
    def new() -> 'PasswordQAC':
        return PasswordQAC()

    def render_questionnaire_template(self, previous_errors: List[str]) -> str:
        return render_template('PasswordQAC.html', error=previous_errors)

    def control(self) -> List[str]:
        if 'preshared_passphrase' not in request.form:
            return [_('Please enter a password.')]

        password = self.get_parameter_by_name('Password').text

        if password != request.form['preshared_passphrase']:
            return [_('The entered password is not correct.')]
