from abc import abstractmethod
from typing import Dict, Any, List

from flask.json import jsonify

from model.SQLAlchemy import db


class View(object):

    @staticmethod
    @abstractmethod
    def render(obj: db.Model) -> Dict[Any, Any]:
        """
        :param obj: A SQLAlchemy model instance to render.
        :return: The object as a serializable dict.
        """
        return NotImplemented

    @classmethod
    def jsonify(cls, obj: db.Model) -> str:
        if not isinstance(obj, db.Model):
            return jsonify(cls.expand(obj))
        return jsonify(cls.render(obj))

    @classmethod
    def expand(cls, objs: List[db.Model]) -> List[Dict[Any, Any]]:
        return [cls.render(obj) for obj in objs]
