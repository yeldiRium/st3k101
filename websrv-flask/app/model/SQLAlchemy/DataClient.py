from model.SQLAlchemy import db
from framework.internationalization.babel_languages import BabelLanguage


class DataClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    language = db.Column(db.Enum(BabelLanguage), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
