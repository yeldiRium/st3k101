import os
from typing import Tuple, List

import argon2

from auth.roles import Role

__author__ = "Noah Hummel"


from flask import g

from model import db
from model.models.Party import Party
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
    verification_token = db.Column(db.String(128))
    _roles = db.Column(db.ARRAY(db.Integer))

    def __init__(self, **kwargs):
        super(DataClient, self).__init__(**kwargs)
        if 'language' not in kwargs:
            self.language = g._language
        self._roles = [Role.User.value]
        if 'verified' not in kwargs:
            self.verified = False
            self.verification_token = os.urandom(64).hex()

    @property
    def roles(self):
        return [Role(r) for r in self._roles]

    def add_role(self, role: Role):
        if role not in self._roles:
            self._roles.append(role.value)

    def revoke_role(self, role: Role):
        if role in self._roles:
            self._roles.remove(role.value)

    def update_roles(self, roles: List[Role]):
        self._roles = [role.value for role in roles]

    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        password_salt = os.urandom(g._config['AUTH_SALT_LENGTH']).hex()
        password_hash = argon2.argon2_hash(password, password_salt).hex()
        return password_salt, password_hash

    @property
    def password(self):
        return self.password_salt, self.password_hash

    @password.setter
    def password(self, password):
        pw_salt, pw_hash = self.hash_password(password)
        self.password_salt = pw_salt
        self.password_hash = pw_hash

    def __str__(self) -> str:
        highest_role = sorted(self.roles)[0].name
        return "<{role}: {email}>".format(role=highest_role, email=self.email)
