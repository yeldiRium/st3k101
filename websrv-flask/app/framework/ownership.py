from flask import g

from model import db


def owned(obj: db.Model) -> bool:
    if not g._current_user:
        return False
    if not hasattr(obj, 'owner'):
        return False
    return obj.owner == g._current_user
