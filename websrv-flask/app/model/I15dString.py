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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.locales is None:  # init dict
            self.locales = dict({})

    def add_locale(self, locale: str, text: str) -> None:
        """
        Add a localized instance of this string for the given locale.
        :param locale: str The short code for the locale.
        :param text: str The localized instance of the string
        :return: None
        """
        new_locales = self.locales
        new_locales[locale] = text
        self.locales = new_locales

    def get_locales(self) -> List[str]:
        """
        :return: list of available locales 
        """
        return [HTTP_LANGUAGE_TAGS[name]["native"] for name in
                self.locales.keys()]

    def get(self, locale: str = None) -> str:
        """
        Return the localized version of the string for the requested locale.
        If the requested locale doesn't exist, it falls back to the
        BABEL_DEFAULT_LOCALE set in flask.cfg. If even the BABEL_DEFAULT_LOCALE
        doesn't exist, it raises LocaleNotFoundException. If no locale is
        passed, it uses g._locale, which is automatically set before each
        request.
        :param locale: str The requested locale, optional
        :return: str The i15d version of the string 
        """

        # use current auto detected locale if no other locale is requested
        if locale is None:
            locale = g._locale

        if locale == "zxx":
            some_locale = next((v for v in self.locales.values()))
            return re.sub(r'[^\s]', "☃", some_locale)

        if locale not in self.locales:  # requested locale not found
            print(
                "Requested locale \"{}\" not found. Falling back to default "
                "locale.".format(
                    locale), file=sys.stderr)
            locale = HTTP_LANGUAGE_TAGS[g._config["BABEL_DEFAULT_LOCALE"]][
                "native"]  # try default locale
            if locale not in self.locales:  # give up, we can't just show any language to the user
                error_message = "Locale {} not found for string. Available " \
                                "locales are: {}".format(
                    locale, self.get_locales())
                raise LocaleNotFoundException(error_message)

        return self.locales[locale]


I15dString.locales = DataAttribute(I15dString,
                                   "locales")  # type: Dict[str, str]
