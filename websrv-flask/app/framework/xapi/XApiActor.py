from abc import abstractmethod
from hashlib import sha1
import json

from XApiItem import XApiItem


class XApiActor(XApiItem):

    def __init__(self, name: str):
        """
        :param name: The name of the actor as string.
        """
        self.__name = name

    def get_name(self) -> str:
        """
        Returns the name of the Actor as string.
        """
        return self.__name

    @abstractmethod
    def get_identifier(self) -> dict:
        """
        Returns an identifier for the Actor.
        According to xAPI, this can be

            "mbox", "mbox_sha1sum", "openid" or "account"

        See subclasses.
        """
        raise NotImplementedError

    def as_dict(self) -> dict:
        return {
            "objectType": "Agent",
            "name": self.get_name(),
            **self.get_identifier()
        }

class XApiMboxActor(XApiActor):

    def __init__(self, name: str, email: str):
        super(XApiMboxActor, self).__init__(name)
        self.__email = email

    def get_email(self):
        return self.__email

    def get_identifier(self) -> dict:
        return {
            "mbox": "mailto:{}".format(self.get_email())
        }

class XApiMboxSha1sumActor(XApiMboxActor):

    def get_identifier(self) -> dict:
        hasher = sha1()
        hasher.update(self.get_email().encode("utf-8"))
        return {
            "mbox_sha1sum": hasher.hexdigest()
        }

class XApiOpenIdActor(XApiActor):

    def __init__(self, name: str, open_id: str):
        super(XApiOpenIdActor, self).__init__(name)
        self.__open_id = open_id

    def get_identifier(self) -> dict:
        return {
            "openid": self.__open_id
        }

class XApiAccountActor(XApiActor):

    def __init__(self, name: str, username: str, service_provider: str):
        """
        :param name: The name of the Actor.
        :param username: The username/id of the Actor at the given service_provider.
        :param service_provider: URL to the service where the Actor has an account.
        """
        super(XApiAccountActor, self).__init__(name)
        self.__username = username
        self.__service_provider = self.format_provider_url(service_provider)

    @staticmethod
    def format_provider_url(service_provider: str) -> str:
        if not service_provider.startswith("http://"):
            if not service_provider.startswith("https://"):
                return "http://{}".format(service_provider)
        return service_provider

    def get_identifier(self) -> dict:
        return {
            "account": {
                "name": self.__username,
                "homePage": self.__service_provider
            }
        }
