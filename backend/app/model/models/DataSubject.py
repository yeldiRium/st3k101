__author__ = "Noah Hummel"


from typing import List

from model import db
from model.models.Party import Party
from auth.roles import Role


class DataSubject(Party):
    id = db.Column(db.Integer, db.ForeignKey(Party.id), primary_key=True)

    # polymorphic config
    __tablename__ = 'data_subject'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    email = db.Column(db.String(120))
    lti_user_id = db.Column(db.String(256))
    moodle_username = db.Column(db.String(120))  # TODO: use ext_user_username if available
    source = db.Column(db.String(120), default="Standalone")  # TODO: use tool_consumer_instance_guid

    @property
    def roles(self) -> List[Role]:
        return [Role.Unprivileged]

    @staticmethod
    def get_or_create(email: str=None, lti_user_id: str=None) -> "DataSubject":

        if email is not None:
            subject = DataSubject.query.filter_by(email=email).first()
            if subject is None:
                subject = DataSubject(email=email)
                db.session.add(subject)
        elif lti_user_id is not None:
            subject = DataSubject.query.filter_by(lti_user_id=lti_user_id).first()
            if subject is None:
                subject = DataSubject(lti_user_id=lti_user_id)
                db.session.add(subject)
        else:
            raise ValueError("No identifying feature provided! Provide email, oder lti_user_id.")
        return subject
