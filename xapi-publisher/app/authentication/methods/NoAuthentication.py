from typing import Optional

import requests
from requests import RequestException

from authentication.methods import AuthenticationMethod

__author__ = "Noah Hummel"


class NoAuthentication(AuthenticationMethod):
    required_parameters = {}
    __headers = {
        'Content-Type': 'application/json',
        'X-Experience-API-Version': '1.0.0',
        'User-Agent': 'st3k101/xapi-publisher'
    }

    def create_session(self) -> dict:
        pass

    @staticmethod
    def transmit_statement(destination: str, statement: str, session_state: dict) -> Optional[int]:
        try:
            response = requests.post(destination, data=statement, headers=NoAuthentication.__headers)
            return response.status_code
        except RequestException as e:
            print(e)
