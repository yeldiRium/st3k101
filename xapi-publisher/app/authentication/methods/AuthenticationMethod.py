from abc import abstractmethod
from typing import Optional

__author__ = "Noah Hummel"


class AuthenticationMethod(object):
    @property
    @abstractmethod
    def required_parameters(self) -> dict:
        """
        :return: A dictionary describing the required parameters for this authentication method.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_session(parameters: dict) -> dict:
        """
        Creates a session and returns a dict containing all information
        needed to perform a request with the created session.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def transmit_statement(destination: str, statement: str, session_state: dict) -> Optional[int]:
        """
        Transmits an xAPI statement and returns the status code of the operation.
        :param destination: The xAPI endpoint
        :param statement: The xAPI statement as serialized JSON
        :param session_state: The session information returned by create_session()
        :return: The status code for the request. If 401 is returned, the session is assumed to be stale
        and will be renewed. Return None on network failure.
        """
        raise NotImplementedError
