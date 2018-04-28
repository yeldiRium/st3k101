from deprecated import deprecated

from framework.internationalization import _
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACParamter import QACParameter

__author__ = "Noah Hummel"


class QACTextParameter(QACParameter):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_parameter.id'),
                   primary_key=True)
    __tablename__ = 'qac_text_parameter'
    __mapper_args__ = {
        'polymorphic_identity': 'qac_text_parameter',
    }

    # columns
    __text = db.Column(db.String(1000), nullable=False, default='')

    def __init__(self, text: str=None, **kwargs):
        super(QACTextParameter, self).__init__(text=text, **kwargs)
        if text is None:
            self.text = _("This is a placeholder text, replace it to your "
                          "liking.")

    @staticmethod
    @deprecated(version='2.0', reason='Use the class constructor directly.')
    def new(text: str=None):
        return QACTextParameter(text=text)

    @deprecated(version='2.0', reason='Use QACTextParameter.text attribute directly.')
    def set_text(self, text: str):
        self.text = text

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str):
        """
        Safe setter for QACTextParameter.text, type checks and ensures that
        string fits into the database column.
        Raises TypeError when type check fails.
        Raises ValueError when string is too long.
        :param text: The text to set.
        """
        if type(text) is not str:
            raise TypeError
        if len(text) > 1000:
            raise ValueError
        self.__text = text
