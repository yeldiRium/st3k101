from enum import Enum


class XApiVerbs(Enum):

    LoggedIn = {
        "id": "https://brindlewaye.com/xAPITerms/verbs/loggedin",
        "display": {
            "en-US": "Indicates someone logged in at st3k101."
        }
    }

    Asked = {
        "id": "http://adlnet.gov/expapi/verbs/asked",
        "display": {
            "en-US": "Indicates the DataClient asked a survey question, i.e. someone accessed a survey."
        }
    }

    Answered = {
        "id": "http://adlnet.gov/expapi/verbs/answered",
        "display": {
            "en-US": "Indicates the DataSubject answered something."
        }
    }

    PublishedSurvey = {
        "id": "http://fantasy.land/published",
        "display": {
            "en-US": "Indicates the DataClient published a survey."
        }
    }

    RetractedSurvey = {
        "id": "http://activitystrea.ms/schema/1.0/retract",
        "display": {
            "en-US": "Indicates the DataClient retracted a previously published a survey."
        }
    }

    ConcludedSurvey = {
        "id": "http://activitystrea.ms/schema/1.0/archive",
        "display": {
            "en-US": "Indicates the DataClient has concluded and archived their survey at st3k101."
        }
    }

    ChangedReferenceId = {
        "id": "http://activitystrea.ms/schema/1.0/update",
        "display": {
            "en-US": "Indicates the DataClient updated the reference id."
        }
    }

    AccessedDashboard = {
        "id": "http://activitystrea.ms/schema/1.0/access",
        "display": {
            "en-US": "Indicates the learner accessed the st3k101 dashboard."
        }
    }

    Voided = {
        "id": "http://adlnet.gov/expapi/verbs/voided",
        "display": {
             "en-US": "Indicates that the object in this statement is no longer valid."
        }
    }
