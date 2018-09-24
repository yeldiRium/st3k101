from enum import Enum

class XApiActivities(Enum):
    Question = {
        "type": "http://adlnet.gov/expapi/activities/question",
        "description": {
            "en-US": "This is a question that is part of a survey at st3k101."
        }
    }

    Dimension = {
        "type": "http://fantasy.land/dimension",
        "description": {
            "en-US": "This is a particular scale of a survey, it usually contains multiple questions."
        }
    }

    Questionnaire = {
        "type": "http://id.tincanapi.com/activitytype/survey",
        "description": {
            "en-US": "This is a survey hosted at st3k101."
        }
    }

    Login = {
        "type": "http://activitystrea.ms/schema/1.0/page",
        "description": {
            "en-US": "This is the log in page of the st3k101 survey tool."
        }
    }
