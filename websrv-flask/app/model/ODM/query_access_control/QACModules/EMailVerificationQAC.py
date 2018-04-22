from typing import List

from framework.odm.DataString import I18n, DataString
from framework.odm.MixedDataPointerSet import MixedDataPointerSet
from model.ODM.query_access_control.QACModule import QACModule

__author__ = "Noah Hummel, Hannes Leutloff"


class EMailVerificationQAC(QACModule):
    """
    A dummy QACModule which causes the SurveyFrontend to mark responses 
    submitted to Questionnaires as unverified.
    
    DataSubjects may then verify their responses by following a link sent out
    to them via email. The link contains a verification token, which is used to
    relate the responses back to the DataSubject without saving the email
    address.
    
    For a full documentation of the methods see model/qac/QACModule
    
    For a better understanding of how email verification works, see 
    api/SurveyFrontend.py
    """

    @staticmethod
    def new() -> "EMailVerificationQAC":

        the_new_qac = EMailVerificationQAC()
        the_new_qac.name = I18n("Email Verification")
        the_new_qac.description = I18n("When submitting a survey, users have "
                                       "to enter their email address. "
                                       "For their answers to be counted, users "
                                       "have to verify their email address by "
                                       "clicking on a link that is sent out "
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
