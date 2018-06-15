from auth.roles import Role

__author__ = "Noah Hummel"


from flask import g

from model.SQLAlchemy import db
from model.SQLAlchemy.models.Party import Party
from framework.internationalization.babel_languages import BabelLanguage


class DataClient(Party):
    id = db.Column(db.Integer, db.ForeignKey(Party.id), primary_key=True)

    # polymorphic config
    __tablename__ = 'data_client'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    language = db.Column(db.Enum(BabelLanguage), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    _roles = db.Column(db.ARRAY(db.Integer))

    def __init__(self, **kwargs):
        super(DataClient, self).__init__(**kwargs)
        if 'language' not in kwargs:
            self.language = g._language
        self._roles = [Role.User.value]

    @property
    def roles(self):
        return [Role(r) for r in self._roles]

    def add_role(self, role: Role):
        self._roles.append(role.value)

    def revoke_role(self, role: Role):
        self._roles.remove(role.value)
