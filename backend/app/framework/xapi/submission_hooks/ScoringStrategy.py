from abc import abstractmethod

__author__ = "Noah Hummel"


class ScoringStrategy(object):
    """
    An abstract base class for scoring know survey items.
    A list of known survey items can be found in framework/xapi/knownItems.
    For a given SurveyBase, this class describes how to calculate a score it.
    """

    @staticmethod
    @abstractmethod
    def score_item(submission_data: dict) -> float:
        """
        Given a certain SurveyBase and the submitted data, this method should
        return a score for the entire item. See api/schemas/Submission for
        information on what data will be present in `submission_data`.
        `submission_data` will only contain the known item in question.
        :param submission_data: {dict} The validated submission data.
        :return: {float} A score for the known item.
        """
        raise NotImplementedError
