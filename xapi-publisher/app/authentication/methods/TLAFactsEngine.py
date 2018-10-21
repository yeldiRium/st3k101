from typing import Optional

import requests
from requests import RequestException

from authentication.methods.AuthenticationMethod import AuthenticationMethod

__author__ = "Noah Hummel"


class TLAFactsEngine(AuthenticationMethod):
    required_parameters = {
        'username': str,
        'password': str
    }

    @staticmethod
    def create_session(parameters: dict) -> dict:
        return {
            'username': parameters['username'],
            'password': parameters['password']
        }

    @staticmethod
    def transmit_statement(destination: str, statement: str, session_state: dict) -> Optional[int]:
        headers = {
            'Content-Type': 'application/json',
            'X-Experience-API-Version': '1.0.0',
            'User-Agent': 'xapi-publisher/TLAFactsEngineSession'
        }
        try:
            username = session_state['username']
            password = session_state['password']
            response = requests.post(
                destination,
                data=statement,
                headers=headers,
                auth=(username, password)
            )
            return response.status_code
        except RequestException:
            return None
