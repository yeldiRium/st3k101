from typing import Optional, List

from deprecated import deprecated

from framework.internationalization import __
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACModule import QACModule

__author__ = "Noah Hummel"


class EMailVerificationQAC(QACModule):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_module.id'),
                   primary_key=True)
    __tablename__ = 'email_verification_qac'
    __mapper_args__ = {
        'polymorphic_identity': 'email_verification_qac'
    }

    # QACModule configuration
    __qac_id = __('Email Verification')
    __description = __('Sends an email to the user after they submit. In order '
                       'to make their answers count. This ensures that the '
                       'user has access to the provided email account. '
                       'Note that if this is disabled, users may submit '
                       'multiple times.')

    @staticmethod
    @deprecated(version='2.0', reason='Use EMailVerificationQAC class constructor directly.')
    def new() -> 'EMailVerificationQAC':
        return EMailVerificationQAC()

    def render_questionnaire_template(self, previous_errors: List[str]) -> str:
        return ''

    def control(self) -> Optional[List[str]]:
        pass
