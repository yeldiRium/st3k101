from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString
from model.ODM.query_access_control.QACParameter import QACParameter

__author__ = "Noah Hummel, Hannes Leutloff"


class QACCheckboxParameter(QACParameter):
    """
    A QACParameter which models an HTML checkbox input.
    """

    exposed_properties = {
        "value"
    }

    @staticmethod
    def new(value:bool=False) \
            -> "QACCheckboxParameter":
        """
        Factory method for QACCheckboxParameter for creating a new instance
        with QACCheckboxParameter.value set to False by default.
        :param value: bool The QACCheckboxParameter.value of the new instance
        :return: QACCheckboxParameter The newly created Parameter
        """
        the_new_param = QACCheckboxParameter()
        the_new_param._value = value
        return the_new_param

    @property
    def value(self) -> bool:
        """
        Getter for QACCheckboxParameter.value
        :return: bool QACCheckboxParameter.value
        """
        return self._value

    @value.setter
    def value(self, le_value: bool) -> None:
        """
        Setter for QACCheckboxParameter.value, type checks le_value to make
        sure input is valid, raises TypeError if check fails.
        :param le_value: bool The new QACCheckboxParameter.value
        :return: None
        """
        if type(le_value) is not bool:
            raise TypeError

        self._value = le_value


QACCheckboxParameter.name = DataString(QACCheckboxParameter, "name")
QACCheckboxParameter.description = DataString(QACCheckboxParameter,
                                              "description")
QACCheckboxParameter._value = DataAttribute(QACCheckboxParameter, "_value",
                                            serialize=False)
