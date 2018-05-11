from deprecated import deprecated

from model.ODM.QuestionGroup import check_color
from model.SQLAlchemy import db, translation_hybrid, MUTABLE_HSTORE
from flask import g

from model.SQLAlchemy.models.DataClient import DataClient
from model.SQLAlchemy.models.Question import Question

__author__ = "Noah Hummel"


class QuestionGroup(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(7), nullable=False, default='#aeaeae')
    text_color = db.Column(db.String(7), nullable=False, default='#000000')

    # translatable columns
    name_translations = db.Column(MUTABLE_HSTORE)
    name = translation_hybrid(name_translations)

    # relationships
    questions = db.relationship('Question', backref='question_group',
                                cascade='all, delete-orphan')

    # foreign keys
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))

    def __init__(self, **kwargs):
        super(QuestionGroup, self).__init__(**kwargs)
        if 'color' not in kwargs:
            self.color = g._config['QUESTIONGROUP_DEFAULT_COLOR']
        if 'text_color' not in kwargs:
            self.text_color = g._config['QUESTIONGROUP_DEFAULT_TEXTCOLOR']

    @staticmethod
    @deprecated(version='2.0', reason='Use QuestionGroup() constructor directly')
    def create_question_group(name: str) -> 'QuestionGroup':
        """
        Factory method for QuestionGroup to create a new instance with default
        values.
        :param name: The name of the new QuestionGroup.
        :return: The newly created QuestionGroup instance.
        """
        return QuestionGroup(name=name)

    @deprecated(version='2.0', reason='Use Question() constructor directly and pass question_group')
    def add_new_question(self, text: str) -> Question:
        """
        Adds a new Question to the QuestionGroup.
        :param text: The text for the new Question.
        :return: The newly created Question instance.
        """
        return Question(text, question_group=self)

    @deprecated(version='2.0', reason='Will be implemented by db triggers in the future')
    def remove_question(self, question: Question):
        """
        Removes a Question from the QuestionGroup.
        :param question: The Question to remove.
        """
        # TODO: implement via cascading delete
        self.questions.remove(question)
        db.session.delete(question)

    @deprecated(version='2.0', reason='Use question_group.name attribute directly')
    def set_name(self, name: str):
        self.name = name

    def set_color(self, color: str):
        """
        Setter for QuestionGroup.color, checks if color is valid.
        :param color: A html-style color hex i.e. #00fa23
        """
        check_color(color)  # TODO: refactor: move check_color to utils package
        self.color = color

    def set_text_color(self, color: str):
        """
        Setter for QuestionGroup.text_color, checks if color is valid.
        :param color: A html-style color hex i.e. #00fa24
        """
        check_color(color)
        self.text_color = color

    @property
    def owner(self) -> DataClient:
        return self.questionnaire.owner

    @property
    def original_language(self) -> str:
        return self.questionnaire.original_language
