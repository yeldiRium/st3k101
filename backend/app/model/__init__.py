from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy_utils import TranslationHybrid
from sqlalchemy.dialects.postgresql import HSTORE as postgresql_HSTORE
from sqlalchemy.ext.mutable import MutableDict

from app import app, get_locale


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention)
db: SQLAlchemy = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

# Internationalization from sqlalchemy_utils

def default_locale(obj: db.Model) -> str:
    """
    Determines a default locale for a given persistent object.
    """
    if hasattr(obj, 'original_language'):
        return obj.original_language.name
    elif hasattr(obj, 'default_language'):
        return obj.default_language.name
    return app.config['LANGUAGE']


translation_hybrid = TranslationHybrid(
    current_locale=get_locale,
    default_locale=default_locale
)

HSTORE = postgresql_HSTORE
MUTABLE_HSTORE = MutableDict.as_mutable(HSTORE)
