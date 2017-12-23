from framework.odm.PersistentObject import PersistentObject, \
    PersistentAttribute, \
    PersistentReference, \
    PersistentReferenceSet
from model.QuestionResult import QuestionResult
from model.QuestionStatistic import QuestionStatistic


class Question(PersistentObject):
    def add_question_result(self, question_result: QuestionResult):
        self.results.add(question_result)


# These are here to prevent circular dependencies in QuestionStatistic and
# QuestionResult modules
QuestionStatistic.question = PersistentReference(QuestionStatistic, "question",
                                                 Question)
QuestionResult.question = PersistentReference(QuestionResult, "question",
                                              Question)

Question.text = PersistentAttribute(Question, "text")
Question.statistic = PersistentReference(Question, "statistic",
                                         QuestionStatistic)
Question.results = PersistentReferenceSet(Question, "results",
                                          QuestionResult)
