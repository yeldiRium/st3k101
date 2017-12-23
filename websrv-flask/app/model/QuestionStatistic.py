from framework.odm.PersistentObject import PersistentObject, PersistentAttribute, PersistentReference


class QuestionStatisticHasNoQuestionException(Exception):
    pass


class QuestionStatistic(PersistentObject):
    def update(self):
        if self.question is None:
            raise QuestionStatisticHasNoQuestionException()
        print("updating statistic!")


QuestionStatistic.smallest = PersistentAttribute(QuestionStatistic, "smallest")
QuestionStatistic.biggest = PersistentAttribute(QuestionStatistic, "biggest")
QuestionStatistic.q1 = PersistentAttribute(QuestionStatistic, "q1")
QuestionStatistic.q2 = PersistentAttribute(QuestionStatistic, "q2")
QuestionStatistic.q3 = PersistentAttribute(QuestionStatistic, "q3")
