from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataAttribute import DataAttribute
from model.DataClient import DataClient
from model.DataSubject import DataSubject


class QuestionResult(DataObject):
    """
    A DataObject representing an answer to a particular Question by a Data-
    Subject.
    """

    # allow reading data from QuestionResult even when no user is logged in
    readable_by_anonymous = True

    @staticmethod
    def new(question, data_subject:DataSubject, answer_value:int,
            needs_verification:bool=True, verification_token:str="") \
            -> "QuestionResult":
        """
        Factory method for QuestionResult
        :param question: Question The Question that this results refers to.
        :param data_subject: DataSubject The DataSubject who has given the 
        answer.
        :param answer_value: int The value of the answer.
        :param needs_verification: bool Whether this result still needs to be 
        verified in order to be counted.
        :param verification_token: str A random token used to verify the Data-
        Subects email address if needed.
        :return: QuestionResult The newly created QuestionResult
        """
        owner = DataClient(question.owner_uuid)
        new_result = QuestionResult(owner=owner)
        new_result.data_subject = data_subject
        new_result.question = question
        new_result.submission_attempt_count = 0
        new_result.verified = not needs_verification
        new_result.verification_token = verification_token
        new_result.answer_value = answer_value
        return new_result

    def verify(self) -> bool:
        """
        Used to verify a QuestionResult to make it count into the statistic.
        :return: bool Indicating whether the answer count for the corresponding
        question increased
        """
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
            return True

        return False


QuestionResult.verified = DataAttribute(QuestionResult, "verified", no_acl=True)
QuestionResult.verification_token = DataAttribute(QuestionResult,
                                                  "verification_token",
                                                  serialize=False, no_acl=True)
QuestionResult.submission_attempt_count = DataAttribute(
    QuestionResult, "submission_attempt_count")
QuestionResult.data_subject = DataPointer(QuestionResult, "data_subject",
                                          DataSubject)
QuestionResult.answer_value = DataAttribute(QuestionResult, "answer_value")
