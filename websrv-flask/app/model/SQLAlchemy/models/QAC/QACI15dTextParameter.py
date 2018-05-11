from deprecated import deprecated
from flask import g

from framework.internationalization import _
from framework.internationalization.babel_languages import BabelLanguage
from model.SQLAlchemy import db, translation_hybrid, MUTABLE_HSTORE
from model.SQLAlchemy.models.QAC.QACParamter import QACParameter

__author__ = "Noah Hummel"


class QACI15dTextParameter(QACParameter):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_parameter.id'),
                   primary_key=True)
    original_language = db.Column(db.Enum(BabelLanguage), nullable=False)
    __tablename__ = 'qac_i15d_text_parameter'
    __mapper_args__ = {
        'polymorphic_identity': 'qac_i15d_text_parameter',
    }

    # translatable columns
    text_translations = db.Column(MUTABLE_HSTORE)
    __text = translation_hybrid(text_translations)

    def __init__(self, text: str=None, **kwargs):
        if text is None:
            text = _("This is a placeholder text, replace it to your liking.")
        super(QACI15dTextParameter, self).__init__(text=text, **kwargs)
        if 'original_language' not in kwargs:
            self.original_language = g._language

    @staticmethod
    @deprecated(version='2.0', reason='Use class constructor directly.')
    def new(text: str=None) -> 'QACI15dTextParameter':
        return QACI15dTextParameter(text=text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        """
        Safe setter for QACI15dTextParameter.text.
        Raises TypeError if text is not a string.
        :param text: The text to set.
        """
        if type(text) is not str:
            raise TypeError
        self.__text = text

    @deprecated(version='2.0', reason='Use QACI15dTextParameter.text attribute directly.')
    def set_text(self, text: str):
        self.text = text
