import math
from typing import List

from framework.exceptions import QuestionStatisticHasNoQuestionException
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject


class QuestionStatistic(DataObject):
    """
    A DataObject representing statistical data generated from QuestionResults of
    a particular Question. Each Question has exactly one QuestionStatistic.
    Used to draw the visualizations in the DataClient's dashboard.
    """

    def update(self):
        """
        Updates the statistics taking into account all QuestionResults of 
        self.question that are verified.
        :return: None
        """
        if self.question is None:
            raise QuestionStatisticHasNoQuestionException()

        result_list = list(filter(lambda x: x.verified,
                                  list(self.question.results)))
        list.sort(result_list, key=lambda x: x.answer_value)

        self.smallest = None
        self.biggest = None

        for result in result_list:
            if self.smallest is None or result.answer_value < self.smallest:
                self.smallest = result.answer_value
            if self.biggest is None or result.answer_value > self.biggest:
                self.biggest = result.answer_value

        result_list_length = len(result_list)
        self.q2 = self.median(result_list)
        if result_list_length % 2 == 0:
            self.q1 = self.median(result_list[0:int(result_list_length / 2)])
            self.q3 = self.median(result_list[int(result_list_length / 2):])

        if result_list_length % 4 == 1:
            if result_list_length == 1:
                self.q1 = int(result_list[0].answer_value)
                self.q3 = int(result_list[0].answer_value)
            else:
                n = int((result_list_length - 1) / 4)
                self.q1 = 0.25 * int(result_list[n - 1].answer_value) + 0.75 * int(result_list[n].answer_value)
                self.q3 = 0.75 * int(result_list[3*n].answer_value) + 0.25 * int(result_list[3*n + 1].answer_value)
        if result_list_length % 4 == 3:
            n = int((result_list_length - 3) / 4)
            self.q1 = 0.25 * int(result_list[n].answer_value) + 0.75 * int(result_list[n + 1].answer_value)
            self.q3 = 0.75 * int(result_list[3*n + 1].answer_value) + 0.25 * int(result_list[3*n + 2].answer_value)

    def median(self, values: List[int]) -> int:
        """
        Returns the median value of all QuestionResults
        """
        list.sort(values, key=lambda x: x.answer_value)
        if len(values) % 2 == 0:
            return (values[int(len(values) / 2) - 1].answer_value) + int(values[int(len(values) / 2)].answer_value) // 2
        else:
            return int(values[int(math.floor(len(values) / 2))].answer_value)


QuestionStatistic.smallest = DataAttribute(QuestionStatistic, "smallest")
QuestionStatistic.biggest = DataAttribute(QuestionStatistic, "biggest")
QuestionStatistic.q1 = DataAttribute(QuestionStatistic, "q1")
QuestionStatistic.q2 = DataAttribute(QuestionStatistic, "q2")
QuestionStatistic.q3 = DataAttribute(QuestionStatistic, "q3")
