from enum import Enum

class XApiActivities(Enum):
    Question = {
        "type": "http://adlnet.gov/expapi/activities/question",
        "description": {
            "en-US": "This is a question that is part of a survey at st3k101."
        }
    }

    Dimension = {
        "id": "http://fantasy.land/dimension",
        "description": {
            "en-US": "This is a particular scale of a survey, it usually contains multiple questions."
        }
    }

    Questionnaire = {
        "id": "http://id.tincanapi.com/activitytype/survey",
        "description": {
            "en-US": "This is a survey hosted at st3k101."
        }
    }
