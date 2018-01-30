from abc import abstractmethod
from typing import Dict, Any, Optional

from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from model.I15dString import I15dString


class QACModule(DataObject):
    exposed_properties = {
        "name",
        "description"
    }

    @property
    def name(self) -> str:
        """
        :return: str The name of the module, localized.
        """
        return self.i15d_name.get()

    @property
    def description(self):
        """
        :return: str A description of the module, localized.
        """
        return self.i15d_description.get()

    @abstractmethod
    def set_config_value(self, param_uuid: str, value: Any) -> Optional[str]:
        """
        Sets a QACParameter of the QACModule.
        :param param_uuid: str The DataObject uuid of the parameter to set
        :param value: Any The value (as given by the user in http serialized
        form) to set the parameter to
        :returns: Optional[str] An error message, if the config param couldn't
        be set for some reason
        """
        pass

    def control(self) -> Dict[str, str]:
        """
        Tests the flask request parameters against the persisted config params.
        Returns a dictionary with all found errors of the form param_uuid ->
        message.
        An empty dictionary means there was no error.
        """
        raise NotImplementedError()


QACModule.i15d_name = DataPointer(QACModule, "i15d_name", I15dString,
                                  serialize=False)
QACModule.i15d_description = DataPointer(QACModule, "i15d_module", I15dString,
                                         serialize=False)
QACModule.parameters = MixedDataPointerSet(QACModule, "parameters")
