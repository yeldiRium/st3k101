from abc import abstractmethod

from requests import Response
from typing import Dict, Any

__author__ = "Noah Hummel"


class AuthenticatedXApiSession(object):
    """Abstract base class for an authenticated HTTP session with a single xAPI endpoint."""
    @property
    @abstractmethod
    def authentication_parameters(self) -> Dict[str, type]:
        """
        :return: A dictionary describing the required parameters for this authentication method.
        """
        pass

    @abstractmethod
    def before_requests(self) -> None:
        """
        Called before the first request is made. Configure anything that needs to be configured and can be re-used for
        multiple requests here.
        """
        pass

    @abstractmethod
    def request(self, statement: str) -> Response:
        """
        Sends the xAPI statement to self.receiver.
        :param statement: The serialized xAPI statement.
        :return: Teh response object.
        """
        pass

    @abstractmethod
    def after_requests(self) -> None:
        """Called after the requests were made. Tear down anything not needed anymore here."""
        pass


    @property
    def receiver(self) -> str:
        """
        :return: The URL of the receiving xAPI endpoint.
        """
        return self.__receiver

    @property
    def parameters(self) -> Dict[str, Any]:
        """
        :return: The parameters provided for the authentication method (read: credentials).
        """
        return self.__parameters

    def __init__(self, receiver: str, **parameters: Dict[str, Any]):
        """
        Raises ValueError if the parameters do not match the ones specified in self.authentication_parameters.
        :param parameters: The parameters required for this authentication method as described in
        self.authentication_parameters
        """
        self.__receiver = receiver
        parameters = dict()
        self.validate_parameters(parameters)
        self.__parameters = parameters

    def validate_parameters(self, parameters: Dict[str, Any]) -> None:
        required_parameters = set(self.authentication_parameters.keys())
        for parameter_name, parameter_value in parameters.items():
            expected_type = getattr(self.authentication_parameters, parameter_name, None)
            actual_type = type(parameter_value)
            if expected_type is None:
                raise ValueError('Unexpected authentication parameter "{}".'.format(parameter_name))
            if actual_type != expected_type:
                raise ValueError('Type mismatch for parameter "{}". Expected "{}", git "{}"'.format(
                    parameter_name, expected_type, actual_type))
            required_parameters.discard(parameter_name)
        if len(required_parameters) != 0:
            raise ValueError("Missing parameters: {}".format(required_parameters))
