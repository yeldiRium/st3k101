from typing import Optional

from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class DataClient(DataObject):
    has_owner = False

    @property
    def locale(self) -> Optional[str]:
        if self.locale_name is None:
            return None
        return self.locale_name

    @locale.setter
    def locale(self, value: str):
        self.locale_name = value


DataClient.email = DataAttribute(DataClient, "email")
DataClient.verified = DataAttribute(DataClient, "verified", serialize=False)
DataClient.password_salt = DataAttribute(DataClient, "password_salt",
                                         serialize=False)
DataClient.password_hash = DataAttribute(DataClient, "password_hash",
                                         serialize=False)
DataClient.locale_name = DataAttribute(DataClient,
                                       "locale_name")  # Language.name of the preferred locale
