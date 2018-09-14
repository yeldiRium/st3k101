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

    email = db.Column(db.String(120), nullable=False)
    lti_user_id = db.Column(db.String(256))

    @property
    def roles(self) -> List[Role]:
        return [Role.Unprivileged]

    @staticmethod
    def get_or_create(email: str) -> "DataSubject":
        subject = DataSubject.query.filter_by(email=email).first()
        if subject is None:
            subject = DataSubject(email=email)
            db.session.add(subject)
        return subject
