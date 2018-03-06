from typing import List, Dict

import sys
import re
from flask import g

from framework.exceptions import LocaleNotFoundException
from framework.internationalization import HTTP_LANGUAGE_TAGS
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject


class I15dString(DataObject):
    """
    A internationalized string, which may have multiple instances, one for every language in 
    framework.internationalization.languages.Language
    """

    readable_by_anonymous = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.locales is None:  # init dict
            self.locales = dict({})
        if self.default_locale is None:
            self.default_locale = g._locale

    def set_locale(self, text: str, locale: str = None) -> None:
        """
        Add a localized instance of this string for the given locale.
        :param locale: str The short code for the locale.
        :param text: str The localized instance of the string
        :return: None
        """
        if locale is None:
            locale = g._locale

        new_locales = self.locales
        new_locales[locale] = text
        self.locales = new_locales

    def get_locales(self) -> List[str]:
        """
        :return: list of available locales 
        """
        return list(self.locales.keys())

    def get_default_text(self) -> str:
        return self.locales[self.default_locale]


I15dString.locales = DataAttribute(I15dString,
                                   "locales")  # type: Dict[str, str]
I15dString.default_locale = DataAttribute(I15dString,
                                          "default_locale")  # type: str
