from typing import List, Dict

from flask import g

from framework.odm.DataAttribute import DataAttribute
from framework.odm.DataObject import DataObject


class I15dString(DataObject):
    """
    A internationalized string, which may have multiple instances, one for every language in 
    framework.internationalization.languages.Language
    """

    readable_by_anonymous = True

    @staticmethod
    def new(text:str=None):
        the_new_string = I15dString()
        the_new_string.locales = dict({})
        the_new_string.default_locale = g._locale
        if text is not None and type(text) is str:
            the_new_string.set_locale(text)
        return the_new_string

    def get(self):
        if g._locale in self.get_locales():
            return self.locales[g._locale]
        else:
            return self.get_default_text()

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
