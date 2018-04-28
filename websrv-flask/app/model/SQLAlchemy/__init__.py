from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_utils import TranslationHybrid
from sqlalchemy.dialects.postgresql import HSTORE as postgresql_HSTORE

from app import app, get_locale


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(app, metadata=metadata)


# Internationalization from sqlalchemy_utils

translation_hybrid = TranslationHybrid(
    current_locale=get_locale,
    default_locale=app.config['BABEL_DEFAULT_LOCALE']
)

HSTORE = postgresql_HSTORE
