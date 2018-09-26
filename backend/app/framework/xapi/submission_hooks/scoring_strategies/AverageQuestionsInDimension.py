from framework.xapi.submission_hooks.ScoringStrategy import ScoringStrategy

__author__ = "Noah Hummel"


class AverageQuestionsInDimension(ScoringStrategy):
    score_min = 0
    score_max = 7

    @staticmethod
    def score_item(submission_data: dict) -> float:
        total = 0
        counter = 0
        for question in submission_data['questions']:
            total += question['value']
            counter += 1

        return total / counter
