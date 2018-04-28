"""
This module lists all subclasses of QACModule that should be available to
the DataClients to enable on their Questionnaires.
"""

from enum import Enum

from model.SQLAlchemy.models.QAC.QACModules import EMailBlacklistQAC
from model.SQLAlchemy.models.QAC.QACModules.EMailVerificationQAC import EMailVerificationQAC
from model.SQLAlchemy.models.QAC.QACModules.EMailWhitelistQAC import EMailWhitelistQAC
from model.SQLAlchemy.models.QAC.QACModules.PasswordQAC import PasswordQAC
from model.SQLAlchemy.models.QAC.QACModules.TOSQAC import TOSQAC

__author__ = "Noah Hummel"


class QAC(Enum):
    """
    Format: NAME = QACModuleSubclass
    """
    TOS = TOSQAC
    PASSWORD = PasswordQAC
    EMAIL_VERIFICATION = EMailVerificationQAC
    EMAIL_BLACKLIST = EMailBlacklistQAC
    EMAIL_WHITELIST = EMailWhitelistQAC
