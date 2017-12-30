import math

from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReference


class QuestionStatisticHasNoQuestionException(Exception):
    pass


class QuestionStatistic(PersistentObject):
    def update(self):
        if self.question is None:
            raise QuestionStatisticHasNoQuestionException()

        result_list = list(self.question.results)
        list.sort(result_list, key=lambda x: x.answer_value)

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

    def median(self, values):
        """
        values has to be sorted
        """
        if len(values) % 2 == 0:
            return (int(values[int(len(values) / 2) - 1].answer_value) + int(values[int(len(values) / 2)].answer_value)) / 2
        else:
            return int(values[math.floor(len(values) / 2)].answer_value)


QuestionStatistic.smallest = PersistentAttribute(QuestionStatistic, "smallest")
QuestionStatistic.biggest = PersistentAttribute(QuestionStatistic, "biggest")
QuestionStatistic.q1 = PersistentAttribute(QuestionStatistic, "q1")
QuestionStatistic.q2 = PersistentAttribute(QuestionStatistic, "q2")
QuestionStatistic.q3 = PersistentAttribute(QuestionStatistic, "q3")
