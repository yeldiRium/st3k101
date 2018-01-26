from typing import Optional

from framework.internationalization.languages import Language
from framework.odm.DataObject import DataObject
from framework.odm.DataPointerSet import DataPointerSet
from framework.odm.DataAttribute import DataAttribute
from model.Survey import Survey


class DataClient(DataObject):
    has_owner = False

    @property
    def locale(self) -> Optional[Language]:
        if self.locale_name is None:
            return None
        return Language[self.locale_name]

    @locale.setter
    def locale(self, value: Language):
        self.locale_name = value.name

DataClient.email = DataAttribute(DataClient, "email")
DataClient.activated = DataAttribute(DataClient, "activated", serialize=False)
DataClient.password_salt = DataAttribute(DataClient, "password_salt", serialize=False)
DataClient.password_hash = DataAttribute(DataClient, "password_hash", serialize=False)
DataClient.locale_name = DataAttribute(DataClient, "locale_name")  # Language.name of the preferred locale
DataClient.surveys = DataPointerSet(DataClient, "surveys", Survey)
