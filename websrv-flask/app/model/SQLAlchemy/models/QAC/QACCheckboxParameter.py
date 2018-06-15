from deprecated import deprecated

from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACParamter import QACParameter

__author__ = "Noah Hummel"


class QACCheckboxParameter(QACParameter):
    # polymorphism configuration
    id = db.Column(db.Integer, db.ForeignKey('qac_parameter.id'),
                   primary_key=True)
    __tablename__ = 'qac_checkbox_parameter'
    __mapper_args__ = {
        'polymorphic_identity': 'qac_checkbox_parameter'
    }

    __value = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    @deprecated(version='2.0', reason='Use QACCheckboxParameter class constructor directly.')
    def new(value: bool=False):
        return QACCheckboxParameter(value=value)

    @property
    def value(self) -> bool:
        return self.__value

    @value.setter
    def value(self, value: bool):
        """
        Safe setter for QACCheckboxParameter.value.
        Raises TypeError if value is not a bool.
        :param value: The value to set.
        """
        if type(value) is not bool:
            raise TypeError
        self.__value = value
