from blinker import Namespace


__author__ = "Noah Hummel"

app_signals = Namespace()

property_updated = app_signals.signal('property_updated')
translation_hybrid_updated = app_signals.signal('translation_hybrid_updated')
item_added = app_signals.signal('item_added')
item_removed = app_signals.signal('item_removed')
questionnaire_removed = app_signals.signal('questionnaire_removed')

SIG_LOGGED_IN = app_signals.signal('logged_in')
