from typing import List

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from model.query_access_control.QACModule import QACModule


class EMailVerificationQAC(QACModule):

    @staticmethod
    def new() -> "EMailVerificationQAC":

        the_new_qac = EMailVerificationQAC()
        the_new_qac.name = I18n("EMAIL_VERIFICATION")
        the_new_qac.description = I18n("When submitting a survey, users have"
                                       "to enter their email address."
                                       "For their answers to be counted, users"
                                       "have to verify their email address by"
                                       "clicking on a link that is sent out"
                                       "to them.")
        the_new_qac.parameters = {}
        return the_new_qac

    def control(self) -> List[I18n]:
        return []

    def render_questionnaire_template(self, previous_errors: List[I18n]) -> str:
        return ""


EMailVerificationQAC.name = DataString(EMailVerificationQAC, "name")
EMailVerificationQAC.description = DataString(EMailVerificationQAC,
                                              "description")
EMailVerificationQAC.parameters = MixedDataPointerSet(EMailVerificationQAC,
                                                      "parameters")
