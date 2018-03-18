from typing import Optional

from framework.odm.DataObject import DataObject
from framework.odm.DataAttribute import DataAttribute


class DataClient(DataObject):
    """
    A DataObject representing a DataClient.
    DataClients edit and publish Surveys and collect data on them.
    DataClients sign up to the platform and are then able to use either
    the web interface or the REST-like API.
    
    We store email in plain text and password hashed and salted.
    """
    has_owner = False

    @property
    def locale(self) -> Optional[str]:
        """
        Getter for DataClient.locale
        :return: Optional[str] The locale of the DatClient
        """
        if self.locale_name is None:
            return None
        return self.locale_name

    @locale.setter
    def locale(self, value: str) -> None:
        """
        Setter for DataClient.locale
        :param value: str The new locale for the DataClient
        :return: None
        """
        self.locale_name = value


DataClient.email = DataAttribute(DataClient, "email")
DataClient.verified = DataAttribute(DataClient, "verified", serialize=False)
DataClient.password_salt = DataAttribute(DataClient, "password_salt",
                                         serialize=False)
DataClient.password_hash = DataAttribute(DataClient, "password_hash",
                                         serialize=False)
DataClient.locale_name = DataAttribute(DataClient, "locale_name")
