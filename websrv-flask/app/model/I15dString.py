from typing import List, Dict

import sys
import re
from flask import g

from framework.exceptions import LocaleNotFoundException
from framework.internationalization.languages import Language
from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject


class I15dString(DataObject):
    """
    A internationalized string, which may have multiple instances, one for every language in 
    framework.internationalization.languages.Language
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.locales is None:  # init dict
            self.locales = dict({})

    def add_locale(self, locale: Language, text: str) -> None:
        """
        Add a localized instance of this string for the given locale.
        :param locale: Language The language the given text is in 
        :param text: str The localized instance of the string
        :return: None
        """
        new_locales = self.locales
        new_locales[locale.name] = text
        self.locales = new_locales

    def get_locales(self) -> List[Language]:
        """
        :return: list of available locales 
        """
        return [Language[name] for name in self.locales.keys()]

    def get(self, locale: Language=None) -> str:
        """
        Return the localized version of the string for the requested locale.
        If the requested locale doesn't exist, it falls back to the DEFAULT_LOCALE set in flask.cfg.
        If even the DEFAULT_LOCALE doesn't exist, it raises LocaleNotFoundException.
        If no locale is passed, it uses g._locale, which is automatically set before each request.
        :param locale: Language The requested locale, optional
        :return: str The i15d version of the string 
        """

        if locale is None:  # use current auto detected locale if no other locale is requested
            locale = g._locale

        if locale == Language.ZXX:
            some_locale = next((v for v in self.locales.values()))
            return re.sub(r'[^\s]', "☃", some_locale)

        if locale.name not in self.locales:  # requested locale not found
            print("Requested locale \"{}\" not found. Falling back to default locale.".format(locale), file=sys.stderr)
            locale = Language[g._config["DEFAULT_LOCALE"]]  # try default locale
            if locale.name not in self.locales:  # give up, we can't just show any language to the user
                error_message = "Locale {} not found for string. Available locales are: {}".format(
                    locale.name, self.get_locales())
                raise LocaleNotFoundException(error_message)

        return self.locales[locale.name]

I15dString.locales = DataAttribute(I15dString, "locales")  # type: Dict[str, str]
