from framework.xapi.submission_hooks.ScoringStrategy import ScoringStrategy
from model.models.SurveyBase import SurveyBase

__author__ = "Noah Hummel"


class EFLAScore(ScoringStrategy):
    score_min = 0
    score_max = 10

    def score_item(self, the_item: SurveyBase):
        # TODO: calculate EFLA score for questionnaire
        return self.score_max
