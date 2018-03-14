from itertools import takewhile

from flask import g

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from model.DataSubject import DataSubject
from model.I15dString import I15dString
from model.QuestionResult import QuestionResult
from model.QuestionStatistic import QuestionStatistic


class Question(DataObject):

    readable_by_anonymous = True

    @staticmethod
    def create_question(text: str):
        question = Question()
        question.text = I15dString.new(text)
        question.dirty = False

        question_statistic = QuestionStatistic()
        question_statistic.question = question
        question.statistic = question_statistic

        return question

    def remove_question_result(self, question_result: QuestionResult):
        """
        
        :param question_result: 
        :return: 
        """
        self.results.remove(question_result)
        question_result.remove()

    def add_question_result(
            self, answer_value: int,
            subject_email: str,
            needs_verification:bool=True,
            verification_token:str="") -> bool:
        """
        
        :param answer_value: 
        :param subject_email: 
        :param needs_verification: 
        :param verification_token: 
        :return: bool Indicating whether the answer count has increased or not
        """

        self.dirty = True
        data_subject = DataSubject.get_or_create(subject_email)
        previous_results = self.get_results_by_subject(data_subject)
        verified_results = list(filter(lambda x: x.verified, previous_results))
        unverified_results = list(filter(lambda x: not x.verified,
                                         previous_results))
        # create after getting previous results as new result would be in
        # previous results otherwise
        new_result = QuestionResult.new(self, data_subject, answer_value,
                                        needs_verification, verification_token)
        self.results.add(new_result)

        if len(previous_results) == 0:  # first result by this DataSubject
            return True

        elif len(previous_results) == 1:
            previous_result = previous_results[0]
            if not previous_result.verified or not needs_verification:
                # verification disabled, new result is instantly verified
                # replace old result by new result
                self.remove_question_result(previous_result)

        elif len(previous_results) == 2:
            # one result is verified, the other one isn't, find out which
            verified_result = verified_results[0]
            unverified_result = unverified_results[0]

            # cancel pending unverified result
            self.remove_question_result(unverified_result)

            if not needs_verification:
                # remove previous verified result, so that the new result
                # replaces it
                self.remove_question_result(verified_result)

        return False

    def update_text(self, text):
        self.text.set_locale(text)

    def get_results_by_subject(self, data_subject:DataSubject):
        results_by_subject = QuestionResult.many_from_query({
            "data_subject": data_subject.uuid,
            "question": self.uuid
        })
        return results_by_subject


# These are here to prevent circular dependencies in QuestionStatistic and
# QuestionResult modules
QuestionStatistic.question = DataPointer(QuestionStatistic, "question",
                                         Question)
QuestionResult.question = DataPointer(QuestionResult, "question", Question)

Question.text = DataPointer(Question, "text", I15dString, cascading_delete=True)
Question.statistic = DataPointer(Question, "statistic", QuestionStatistic,
                                 cascading_delete=True, serialize=False)
Question.results = DataPointerSet(Question, "results", QuestionResult,
                                  cascading_delete=True, serialize=False,
                                  no_acl=True)
Question.dirty = DataAttribute(Question, "dirty", serialize=False, no_acl=True)
