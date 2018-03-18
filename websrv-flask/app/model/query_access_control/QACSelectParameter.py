from typing import Iterator, List

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataString import DataString, I18n
from model.query_access_control.QACParameter import QACParameter


class QACSelectParameter(QACParameter):
    """
    A QACParameter which models an HTML select input with internationalized
    labels.
    
    This class is implemented in Python, but not yet supported by the frontend,
    so it is untested.
    
    A QACSelectParameter provides multiple choices to the user which can be
    selected. All selected choices are stored in QACSelectParameter.values.
    
    Every choice and value is an I18n object (see framework/odm/DataString.py),
    which means it contains a msgid (identifying the string) and a text ( a 
    translated version of the string) value.
    
    An user may select multiple choices when QACSelectParameter.allow_multi
    is True.
    """

    exposed_properties = {
        "choices",
        "values"
    }

    @staticmethod
    def new(allow_multi: bool=False) -> "QACSelectParameter":
        """
        Factory method for QACSelectParameter to create a new instance with
        default values. By default, allow_multi is False.
        :param allow_multi: bool Whether multiple choices should be allowed
        :return: QACSelectParameter The newly created QACSelectParameter
        """
        the_new_param = QACSelectParameter()
        the_new_param.allow_multi = allow_multi
        return the_new_param

    @property
    def choices(self) -> Iterator[I18n]:
        """
        Getter for QACSelectParameter.choices
        :return: Iterator[I18n] QACSelectParameter.choices
        """
        return (I18n(msgid) for msgid in self._choices)

    @choices.setter
    def choices(self, values: List[I18n]) -> None:
        """
        Setter for QACSelectParameter.choices, type checks choices and raises
        TypeError if check fails.
        :param values: List[I18n] A list of internationalized choices th user
                                  may select from
        :return: None
        """
        if not all([type(v) is I18n for v in values]):
            raise TypeError

        self._choices = [v.msgid for v in values]

    @property
    def values(self) -> Iterator[I18n]:
        """
        Getter for QACSelectParameter.values
        :return: Iterator[I18n] The list of selected choices
        """
        return (I18n(msgid) for msgid in self._values)

    @values.setter
    def values(self, values: List[I18n]) -> None:
        """
        Setter for QACSelectParameter.values, type checks values and raises
        TypeError if check fails. Also enforces QACSelectParameter.allow_multi
        and raises ValueError if too many choices are passed.
        :param values: List[I18n] The new selected values for the Parameter
        :return: None
        """
        if not self.allow_multi and len(values) > 1:
            raise ValueError("Only one choice is allowed")

        if not all([type(v) == I18n for v in values]):  # arg is list of (name, label)
            raise TypeError

        values = [v.msgid for v in values]
        self._values = values

    def set_values(self, values: List[str]) -> None:
        """
        Setter for QACSelectParameter.values to set from msgid directly without
        passing a full I18n object. Type checks values and raises
        TypeError if check fails. Also enforces QACSelectParameter.allow_multi
        and raises ValueError if too many choices are passed.
        :param values: List[str] The new selected values for the Parameter
        :return: None
        """
        if not self.allow_multi and len(values) > 1:
            raise ValueError("Only one choice is allowed")

        if not all([type(v) == str for v in values]):  # arg is list of (name, label)
            raise TypeError

        self._values = values


QACSelectParameter.name = DataString(QACSelectParameter, "name")
QACSelectParameter.description = DataString(QACSelectParameter, "description")
QACSelectParameter._choices = DataAttribute(QACSelectParameter, "_choices",
                                            serialize=False)
QACSelectParameter._values = DataAttribute(QACSelectParameter, "_values",
                                           serialize=False)
QACSelectParameter.allow_multi = DataAttribute(QACSelectParameter,
                                               "allow_multi")
