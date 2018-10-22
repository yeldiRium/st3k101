from typing import Type, Dict

from authentication.methods.AuthenticationMethod import AuthenticationMethod
from authentication.methods.NoAuthentication import NoAuthentication
from authentication.methods.TLAFactsEngine import TLAFactsEngine

__author__ = "Noah Hummel"

__available_methods = {
    "NoAuthentication": NoAuthentication,
    "TLAFactsEngine": TLAFactsEngine
}


class UnknownAuthenticationMethod(Exception):
    pass


def get_authentication_handler(method_name: str) -> Type[AuthenticationMethod]:
    if method_name not in __available_methods:
        raise UnknownAuthenticationMethod
    return __available_methods[method_name]


def get_available_authentication_methods() -> Dict[str, dict]:
    return {
        name: {
            key: str(required_type)
            for key, required_type in method.required_parameters.items()
        }
        for name, method in __available_methods
    }
