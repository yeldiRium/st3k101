from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataAttribute import DataAttribute
from model.DataClient import DataClient
from model.DataSubject import DataSubject


class QuestionResult(DataObject):

    readable_by_anonymous = True

    @staticmethod
    def new(question, data_subject:DataSubject, answer_value:int,
            needs_verification:bool=True, verification_token:str=""):
        owner = DataClient(question.owner_uuid)
        new_result = QuestionResult(owner=owner)
        new_result.data_subject = data_subject
        new_result.question = question
        new_result.submission_attempt_count = 0
        new_result.verified = not needs_verification
        new_result.verification_token = verification_token
        new_result.answer_value = answer_value
        return new_result

    def verify(self):
        # first remove previous verified results from  question
        question = self.question

        previous_results = question.get_results_by_subject(self.data_subject)
        verified_results = list(filter(lambda x: x.verified, previous_results))

        for result in verified_results:
            question.remove_question_result(result)

        # now verify self
        self.verified = True
        self.verification_token = "Already verified"

        # update answer count on questionnaire if needed
        if len(verified_results) == 0:
            question.questionnaire.answer_count += 1


QuestionResult.verified = DataAttribute(QuestionResult, "verified", no_acl=True)
QuestionResult.verification_token = DataAttribute(QuestionResult,
                                                  "verification_token",
                                                  serialize=False, no_acl=True)
QuestionResult.submission_attempt_count = DataAttribute(
    QuestionResult, "submission_attempt_count")
QuestionResult.data_subject = DataPointer(QuestionResult, "data_subject",
                                          DataSubject)
QuestionResult.answer_value = DataAttribute(QuestionResult, "answer_value")
