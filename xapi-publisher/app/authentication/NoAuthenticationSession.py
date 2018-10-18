import requests
from requests import Response

from authentication.AuthenticatedXApiSession import AuthenticatedXApiSession

__author__ = "Noah Hummel"


class NoAuthenticationSession(AuthenticatedXApiSession):
    authentication_parameters = {}

    def before_requests(self) -> None:
        self.headers = {
        'Content-Type': 'application/json',
        'X-Experience-API-Version': '1.0.0',
        'User-Agent': 'st3k101/2.0'
    }

    def request(self, statement: str) -> Response:
        return requests.post(self.receiver, data=statement, headers=self.headers,
                             timeout=5)

    def after_requests(self) -> None:
        pass
