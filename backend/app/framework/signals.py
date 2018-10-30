from blinker import Namespace

__author__ = "Noah Hummel"
app_signals = Namespace()
property_updated = app_signals.signal('property_updated')
translation_hybrid_updated = app_signals.signal('translation_hybrid_updated')
item_added = app_signals.signal('item_added')
item_removed = app_signals.signal('item_removed')
questionnaire_removed = app_signals.signal('questionnaire_removed')
SIG_LOGGED_IN = app_signals.signal('logged_in')
SIG_LTI_LAUNCH = app_signals.signal('lti_launch')
SIG_QUESTION_ANSWERED = app_signals.signal('question_answered')
SIG_ANSWER_VERIFIED = app_signals.signal('answer_verified')
SIG_REFERENCE_ID_UPDATED = app_signals.signal('reference_id_updated')
SIG_QUESTIONNAIRE_PUBLISHED = app_signals.signal('questionnaire_published')
SIG_QUESTIONNAIRE_UNPUBLISHED = app_signals.signal('questionnaire_unpublished')
SIG_SURVEY_CONCLUDED = app_signals.signal('survey_concluded')