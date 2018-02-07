from enum import Enum

from model.query_access_control.QACModules.MailListQAC import MailListQAC
from model.query_access_control.QACModules.IPRangeQAC import IPRangeQAC
from model.query_access_control.QACModules.TOSQAC import TOSQAC


class QAC(Enum):
    TOS = TOSQAC
    IP_RANGE = IPRangeQAC
    MAIL_LIST = MailListQAC

