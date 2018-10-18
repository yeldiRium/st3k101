from enum import Enum

from authentication.NoAuthenticationSession import NoAuthenticationSession
from authentication.TLAFactsEngineSession import TLAFactsEngineSession

__author__ = "Noah Hummel"


class AuthenticationMethods(Enum):
    """
    An enum list all available authentication mechanisms.
    It's values map to the appropriate session handler class.
    """
    NoAuthentication = NoAuthenticationSession
    TLAFactsEngineAuthentication = TLAFactsEngineSession
