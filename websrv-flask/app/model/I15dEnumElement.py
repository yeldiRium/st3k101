from typing import Dict

from framework.internationalization.languages import Language
from framework.odm.DataAttribute import DataAttribute
from model.I15dString import I15dString


class I15dEnumElement(I15dString):

    exposed_properties = {
        "label"
    }

    @staticmethod
    def define(name: str, locales: Dict[Language, str]):
        the_element = I15dEnumElement.one_from_query({"name": name})
        if the_element is not None:
            return
        the_element.locales = {l.name: txt for l, txt in locales.items()}

    @staticmethod
    def by_name(name: str):
        the_element = I15dEnumElement.one_from_query({"name": name})
        if the_element is None:
            the_element = I15dEnumElement()
            the_element.name = name
        return the_element

    @property
    def label(self):
        return self.get()


I15dEnumElement.name = DataAttribute(I15dEnumElement, "name")
