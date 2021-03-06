from flask import g

from framework.internationalization.babel_languages import BabelLanguage

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
    moodle_username = db.Column(db.String(120))
    source = db.Column(db.String(120), default="Standalone")
    launch_language = db.Column(db.Enum(BabelLanguage))

    @property
    def language(self) -> BabelLanguage:
        if self.launch_language is not None:
            return self.launch_language
        return g._config['LANGUAGE']

    @property
    def roles(self) -> List[Role]:
        return [Role.Unprivileged]

    @staticmethod
    def get_or_create(email: str=None, lti_user_id: str=None, tool_consumer: str=None) -> "DataSubject":

        if email is not None:
            subject = DataSubject.query.filter_by(email=email).first()
            if subject is None:
                subject = DataSubject(email=email)
                db.session.add(subject)
        elif lti_user_id is not None:
            subject = DataSubject.query.filter_by(lti_user_id=lti_user_id, source=tool_consumer).first()
            if subject is None:
                subject = DataSubject(lti_user_id=lti_user_id, source=tool_consumer)
                db.session.add(subject)
        else:
            raise ValueError("No identifying feature provided! Provide email, oder lti_user_id.")
        return subject

    def __str__(self) -> str:
        lti_id_or_username = self.moodle_username if self.moodle_username else self.lti_user_id
        identifier = self.email if self.email else "LTI:{}@{}".format(lti_id_or_username, self.source)
        return "<DataSubject: {identifier}>".format(identifier=identifier)
