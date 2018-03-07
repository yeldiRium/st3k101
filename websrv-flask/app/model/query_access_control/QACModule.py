from abc import abstractmethod
from typing import Any, Optional, List

from framework.odm.DataObject import DataObject
from framework.odm.DataString import DataString, I18n
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from framework.internationalization import _
from model.query_access_control.QACCheckboxParameter import QACCheckboxParameter
from model.query_access_control.QACParameter import QACParameter
from model.query_access_control.QACSelectParameter import QACSelectParameter
from model.query_access_control.QACTextParameter import QACTextParameter, \
    QACI15dTextParameter


class QACModule(DataObject):

    readable_by_anonymous = True

    def set_config_value(self, param_uuid: str, value: Any) -> Optional[str]:
        """
        Sets a QACParameter of the QACModule.
        :param param_uuid: str The DataObject uuid of the parameter to set
        :param value: Any The value (as given by the user in http serialized
        form) to set the parameter to
        :returns: Optional[str] An error message, if the config param couldn't
        be set for some reason
        """
        updated = False

        for param in self.parameters:  # type: QACParameter
            if param.uuid != param_uuid:
                continue

            type_of_param = type(param)
            try:
                if type_of_param is QACCheckboxParameter:
                    param: QACCheckboxParameter
                    param.value = value
                    updated = True

                elif type_of_param is QACSelectParameter:
                    param: QACSelectParameter
                    value: List[str]  # list of msgids
                    try:
                        param.set_values(value)
                        updated = True
                    except ValueError as e:
                        return e.args[0]

                elif type_of_param in (QACTextParameter, QACI15dTextParameter):
                    param: QACTextParameter
                    value: str
                    param.text = value
                    updated = True

                else:
                    raise NotImplementedError("Some developer's been lazy af")
            except TypeError:
                return _("Wrong type for QACParameter")
            except NotImplementedError as e:
                raise e

            if not updated:
                return _("QACParameter not found.")

    @abstractmethod
    def render_questionnaire_template(self, previous_errors: List[I18n]) \
            -> str:
        """
        :param previous_errors: List[QACError] A list of errors that occurred
        during a previous execution of QACModule.control(). Used for displaying
        hints to the user when redisplaying the survey after a submission
        failure due to control() failing.
        :return: str A piece of html that is embedded into the questionnaire
        form that the user sees to present additional data and / or challenges
        to the user before submission.
        """
        raise NotImplementedError()

    def control(self) -> List[I18n]:
        """
        Tests the flask request parameters against the persisted config params.
        Returns a list of all found errors in user-readable form, so that they
        can be displayed as an error message.
        An empty list means there was no error.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def new() -> "QACModule":
        """
        :return: A new instance of le QAC, avec les defaults
        """
        raise NotImplementedError()


QACModule.name = DataString(QACModule, "name")
QACModule.description = DataString(QACModule, "description")
QACModule.parameters = MixedDataPointerSet(QACModule, "parameters")
