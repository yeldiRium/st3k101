from abc import abstractmethod
from typing import Dict

from model.SQLAlchemy import db, MUTABLE_HSTORE, translation_hybrid
from model.SQLAlchemy.v2_models.SurveyBase import SurveyBase
from utils import check_color

__author__ = "Noah Hummel"


class Dimension(SurveyBase):
    id = db.Column(db.Integer, db.ForeignKey(SurveyBase.id), primary_key=True)

    __tablename__ = 'dimension'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # foreign keys
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))

    # relationships
    questions = db.relationship(
        'Question',
        backref='dimension',
        cascade='all, delete-orphan',
        foreign_keys=['question.id']
    )

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def name_translations(self) -> Dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def color(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def text_color(self) -> str:
        raise NotImplementedError

    @property
    def original_language(self) -> str:
        return self.questionnaire.original_language


class ConcreteDimension(Dimension):
    id = db.Column(db.Integer, db.ForeignKey(Dimension.id), primary_key=True)

    __tablename__ = 'concrete_dimension'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    # columns
    color = db.Column(db.String(7), nullable=False, default='#aeaeae')
    text_color = db.Column(db.String(7), nullable=False, default='#000000')
    name_translations = db.Column(MUTABLE_HSTORE)
    name = translation_hybrid(name_translations)

    def set_color(self, color: str):
        """
        Setter for QuestionGroup.color, checks if color is valid.
        :param color: A html-style color hex i.e. #00fa23
        """
        check_color(color)
        self.color = color

    def set_text_color(self, color: str):
        """
        Setter for QuestionGroup.text_color, checks if color is valid.
        :param color: A html-style color hex i.e. #00fa24
        """
        check_color(color)
        self.text_color = color


class ShadowDimension(Dimension):
    id = db.Column(db.Integer, db.ForeignKey(Dimension.id), primary_key=True)

    __tablename__ = 'shadow_dimension'
    __mapper_args__ = {'polymorphic_identity': __tablename__}

    _referenced_object_id = db.Column(db.Integer,
                                      db.ForeignKey(ConcreteDimension.id))
    _referenced_object = db.relationship(ConcreteDimension,
                                         foreign_keys=[_referenced_object_id],
                                         backref='copies')

    @property
    def name(self) -> str:
        return self._referenced_object.name

    @property
    def name_translations(self) -> Dict[str, str]:
        return self._referenced_object.name_translations

    @property
    def color(self) -> str:
        return self._referenced_object.color

    @property
    def text_color(self) -> str:
        return self._referenced_object.text_color
