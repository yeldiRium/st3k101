from enum import Enum

from model.query_access_control.QACModules.EMailWhitelistQAC import \
    EMailWhitelistQAC
from model.query_access_control.QACModules.EMailBlacklistQAC import \
    EMailBlacklistQAC
from model.query_access_control.QACModules.PasswordQAC import PasswordQAC
from model.query_access_control.QACModules.TOSQAC import TOSQAC


class QAC(Enum):
    TOS = TOSQAC
    PASSWORD = PasswordQAC
    EMAIL_BLACKLIST = EMailBlacklistQAC
    EMAIL_WHITELIST = EMailWhitelistQAC
