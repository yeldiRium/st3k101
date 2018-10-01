from framework.xapi.submission_hooks import AverageQuestionsInDimension
from framework.xapi.submission_hooks.scoring_strategies.EFLAScore import EFLAScore

__author__ = "Noah Hummel"

hooks = {
    'regex:lernstrategien_wild_schiefele--(?!.*--).*': {
        'score_min': 0,
        'score_max': 5,
        'scoring_strategy': AverageQuestionsInDimension
    },
    'efla': {
        'score_min': 0,
        'score_max': 10,
        'scoring_strategy': EFLAScore
    }
}
