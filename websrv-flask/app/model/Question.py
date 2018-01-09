from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject
from framework.odm.DataPointer import DataPointer
from framework.odm.DataPointerSet import DataPointerSet
from model.QuestionResult import QuestionResult
from model.QuestionStatistic import QuestionStatistic


class Question(DataObject):
    def add_question_result(self, question_result: QuestionResult):
        self.results.add(question_result)


# These are here to prevent circular dependencies in QuestionStatistic and
# QuestionResult modules
QuestionStatistic.question = DataPointer(QuestionStatistic, "question", Question)
QuestionResult.question = DataPointer(QuestionResult, "question", Question)

Question.text = DataAttribute(Question, "text")
Question.statistic = DataPointer(Question, "statistic", QuestionStatistic)
Question.results = DataPointerSet(Question, "results", QuestionResult)
