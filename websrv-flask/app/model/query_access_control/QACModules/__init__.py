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
    PASSWORD = (PasswordQAC, _("Password"))
    EMAIL_VERIFICATION = (EMailVerificationQAC, _("Email Verification"))
    EMAIL_BLACKLIST = (EMailBlacklistQAC, _("Email Blacklist"))
    EMAIL_WHITELIST = (EMailWhitelistQAC, _("Email Whitelist"))
