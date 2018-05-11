from flask import g

from model.SQLAlchemy import db
from framework.internationalization.babel_languages import BabelLanguage, babel_languages

from deprecated import deprecated

__author__ = "Noah Hummel"


class DataClient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    language = db.Column(db.Enum(BabelLanguage), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)

    # relationships
    surveys = db.relationship('Survey', backref='data_client', lazy=True,
                              cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(DataClient, self).__init__(**kwargs)
        if 'language' not in kwargs:
            self.language = g._language

    @property
    @deprecated(version='2.0', reason='Attribute has been renamed to "language"')
    def locale(self) -> str:
        """
        Legacy shim for DataClient.locale
        DataClient.locale will be renamed to DataClient.language
        in version 2.0
        :return: Language identifier i.e. "en", "en_gb", see
                 framework/internationalization/babel_languages
        """
        return self.language

    @locale.setter
    @deprecated(version='2.0', reason='Attribute has been renamed to "language"')
    def locale(self, new_locale: str):
        """
        Legacy shim for DataClient.locale
        DataClient.locale will be renamed to DataClient.language
        in version 2.0
        """
        if new_locale not in babel_languages:
            raise ValueError
        self.language = BabelLanguage[new_locale]
