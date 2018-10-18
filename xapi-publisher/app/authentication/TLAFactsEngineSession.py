from requests import Response

from authentication.AuthenticatedXApiSession import AuthenticatedXApiSession

__author__ = "Noah Hummel"


class TLAFactsEngineSession(AuthenticatedXApiSession):
    authentication_parameters = {
        'username': str,
        'password': str
    }

    def before_requests(self) -> None:
        pass

    def request(self, statement: str) -> Response:
        pass

    def after_requests(self) -> None:
        pass