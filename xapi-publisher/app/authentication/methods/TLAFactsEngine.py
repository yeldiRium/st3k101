from typing import Optional

import requests
from requests import RequestException

from authentication.methods.AuthenticationMethod import AuthenticationMethod

__author__ = "Noah Hummel"


class TLAFactsEngine(AuthenticationMethod):
    required_parameters = {
        'authentication_endpoint': str,
        'username': str,
        'password': str
    }

    @staticmethod
    def create_session(parameters: dict) -> dict:
        endpoint = parameters['authentication_endpoint']
        username = parameters['username']
        password = parameters['password']
        response = requests.post(endpoint, auth=(username, password))
        jwt = response.json()['token']  # TODO: wait for endpoint to be fixed.
        return {
            'headers': {
                'Content-Type': 'application/json',
                'X-Experience-API-Version': '1.0.0',
                'User-Agent': 'xapi-publisher/TLAFactsEngineSession',
                'Authorization': 'Bearer {}'.format(jwt)
            }
        }

    @staticmethod
    def transmit_statement(destination: str, statement: str, session_state: dict) -> Optional[int]:
        headers = session_state['headers']
        try:
            response = requests.post(destination, data=statement, headers=headers)
            return response.status_code
        except RequestException:
            return None
