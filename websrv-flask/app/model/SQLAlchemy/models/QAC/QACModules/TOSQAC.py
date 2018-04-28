from typing import List

from deprecated import deprecated
from flask import render_template, request

from framework.internationalization import __, _
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACI15dTextParameter import QACI15dTextParameter
from model.SQLAlchemy.models.QAC.QACModule import QACModule

__author__ = "Noah Hummel"


class TOSQAC(QACModule):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_module.id'),
                   primary_key=True)
    __tablename__ = 'tos_qac'
    __mapper_args__ = {
        'polymorphic_identity': 'tos_qac'
    }

    # QACModule configuration
    __qac_id = __('Terms of Service')
    __description = __('Displays an internationalized terms of '
                       'service text to the user when they '
                       'submit a survey. The user has to agree'
                       'to the terms of service before a survey '
                       'may be submitted.')

    def __init__(self, **kwargs):
        super(TOSQAC, self).__init__(**kwargs)
        tos_text = QACI15dTextParameter()
        tos_text.name = __('ToS Text')
        tos_text.description = __('The text that is displayed '
                                  'to the user as the terms of '
                                  'service.')
        self.parameters.append(tos_text)

    @staticmethod
    @deprecated(version='2.0', reason='Use TOSQAC class constructor directly.')
    def new() -> 'TOSQAC':
        return TOSQAC()

    def render_questionnaire_template(self, previous_errors: List[str]) -> str:
        tos_text_parameter = self.get_parameter_by_name('ToS Text')
        return render_template(
            'TOSQAC.html',
            error=previous_errors,
            agb_agreement_text=tos_text_parameter.text
        )

    def control(self) -> List[str]:
        if 'tos' not in request.form or not request.form['tos']:
            return [_('Please accept the terms of service.')]
