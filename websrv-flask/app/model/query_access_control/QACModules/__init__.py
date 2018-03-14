from enum import Enum

from model.query_access_control.QACModules.EMailVerificationQAC import \
    EMailVerificationQAC
from model.query_access_control.QACModules.EMailWhitelistQAC import \
    EMailWhitelistQAC
from model.query_access_control.QACModules.EMailBlacklistQAC import \
    EMailBlacklistQAC
from model.query_access_control.QACModules.PasswordQAC import PasswordQAC
from model.query_access_control.QACModules.TOSQAC import TOSQAC

from framework.internationalization import _


class QAC(Enum):
    TOS = (TOSQAC, _("TOS"))
    PASSWORD = (PasswordQAC, _("PASSWORD"))
    EMAIL_VERIFICATION = (EMailVerificationQAC, _("EMAIL_VERIFICATION"))
    EMAIL_BLACKLIST = (EMailBlacklistQAC, _("EMAIL_BLACKLIST"))
    EMAIL_WHITELIST = (EMailWhitelistQAC, _("EMAIL_WHITELIST"))
