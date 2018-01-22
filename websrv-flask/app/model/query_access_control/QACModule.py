from typing import Dict
from typing import List

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject


class QACModule(DataObject):
    def get_name(self) -> str:
        """
        Statically returns the name of the module.
        """
        raise NotImplementedError()

    def get_survey_template(self, errors: Dict[str, str]) -> str:
        """
        Returns an html-snippet that expects to be embedded in a form.
        """
        raise NotImplementedError()

    def get_required_config_fields(self) -> List[str]:
        """
        Returns a static list of config filed names.
        """
        raise NotImplementedError()

    def get_config(self) -> Dict[str, str]:
        """
        Returns the persisted config values.
        """
        return self.config

    def set_config_value(self, key: str, value):
        """
        Sets a value in the persisted config dict. Only works, if the key
        is contained in the output of get_required_config_fields.
        """
        if key in self.get_required_config_fields():
            self.config[key] = value

    def control(self) -> Dict[str, str]:
        """
        Tests the flask request parameters against the persisted config params.
        Returns a dictionary with all found errors of the form key -> message.
        An empty dictionary means there was no error.
        """
        raise NotImplementedError()

QACModule.config = DataAttribute(QACModule, "config")
