from abc import abstractmethod
from typing import List, Any, Optional

from deprecated import deprecated

from framework.internationalization import _, __
from model.SQLAlchemy import db
from model.SQLAlchemy.models.QAC.QACCheckboxParameter import QACCheckboxParameter
from model.SQLAlchemy.models.QAC.QACI15dTextParameter import QACI15dTextParameter
from model.SQLAlchemy.models.QAC.QACParamter import QACParameter
from model.SQLAlchemy.models.QAC.QACTextParameter import QACTextParameter
from model.SQLAlchemy.models.OwnershipBase import OwnershipBase

__author__ = "Noah Hummel"


class QACModule(OwnershipBase):
    id = db.Column(db.Integer, db.ForeignKey(OwnershipBase.id), primary_key=True)

    # polymorphism on, this is a base class
    module_type = db.Column(db.String(50))
    __tablename__ = 'qac_module'
    __mapper_args__ = {
        'polymorphic_identity': 'qac_module',
        'polymorphic_on': module_type
    }

    # foreign keys
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))

    parameters = db.relationship(
        'QACParameter',
        backref='qac_module',
        cascade='all, delete-orphan',
        foreign_keys=[QACParameter.qac_module_id]
    )

    # non ORM-related attributes
    _qac_id = __('QACModule')
    _description = __('The base class for all QACModules. '
                      'If you see this in the front end, '
                      'you haven\'t assigned a _description '
                      'to the QACModule.')

    @classmethod
    def get_qac_id(cls):
        return cls._qac_id

    @property
    def qac_id(self) -> str:
        return self.get_qac_id()

    @property
    def name(self) -> str:
        return _(self.qac_id)

    @property
    def description(self) -> str:
        return _(self._description)

    @property
    @deprecated(version='2.0', reason='This property exists as a compatibility '
                                      'shim for the 1.0 API and will likely be '
                                      'removed in the future.')
    def description_msgid(self) -> str:
        return self._description

    def set_config_value(self, param_id: str, value: Any) -> Optional[str]:
        """
        Sets a QACParameter of the QACModule.
        :param param_id: str The primary key "id" of the parameter to set
        :param value: Any The value (as given by the user in http serialized
        form) to set the parameter to
        :returns: Optional[str] An error message, if the config param couldn't
        be set for some reason
        """
        updated = False

        for param in self.parameters:  # type: QACParameter
            if param.id != param_id:
                continue

            try:
                if type(param) is QACCheckboxParameter:
                    param.value = value
                    updated = True

                elif type(param) in (QACTextParameter, QACI15dTextParameter):
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
    def render_questionnaire_template(self, previous_errors: List[str]) \
            -> str:
        """
        :param previous_errors: A list of errors that occurred
        during a previous execution of QACModule.control(). Used for displaying
        hints to the user when re-displaying the survey after a submission
        failure due to control() failing.
        :return: str A piece of html that is embedded into the questionnaire
        form that the user sees to present additional data and / or challenges
        to the user before submission.
        """
        raise NotImplementedError()

    @abstractmethod
    def control(self) -> Optional[List[str]]:
        """
        Tests the flask request parameters against the persisted config params.
        Returns a list of all found errors in user-readable form, so that they
        can be displayed as an error message.
        No return value means there was no error.
        """
        raise NotImplementedError()

    @classmethod
    @deprecated(version='2.0', reason='Use appropriate constructor directly.')
    def new(cls, *args, **kwargs) -> "QACModule":
        """
        :return: A new instance of le QAC, avec les defaults
        """
        return cls(*args, **kwargs)

    def get_parameter_by_name(self, name: str) -> Optional[QACParameter]:
        """
        Returns the QACModules QACParameter by the given name, if it exists.
        :param name: The name of the QACParameter.
        :return: The QACParameter or None if it doesn't exist.
        """
        for parameter in self.parameters:
            if parameter.name_msgid == name:
                return parameter

        return None
