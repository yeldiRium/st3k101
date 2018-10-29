from typing import List, Dict, Any

from flask import g
from marshmallow import fields, missing, post_dump

from api.schema import RESTFulSchema
from api.schema.DataClient import DataClientSchema
from api.schema.fields import enum_field
from framework.internationalization.babel_languages import BabelLanguage
from model.models.SurveyBase import SurveyBase
from auth.session import current_user

__author__ = "Noah Hummel"


class SurveyBaseSchema(RESTFulSchema):
    """A serialisation schema for the :class:`SurveyBase` model.

    This schema provides common fields used in all SurveyBase descendants.
    If the schema is used to serialise a SurveyBase which is not owned by the
    current_user, the following fields are stripped:

        - shadow
        - incoming_reference_count
        - owned_incoming_references
        - reference_to
        - owners
    """
    original_language = enum_field(BabelLanguage, dump_only=True)
    """dict(str, str): The language the SurveyBase was created in.
    For a list of all available languages, see :class:`BabelLanguage`.
    For more information on how this attribute is serialised, see `enum_field`.
    """

    reference_id = fields.String()
    """str: The xAPI activity ID used when constructing xAPI statements 
    concerning the SurveyBase. This does not __not__ contain the owner prefix 
    included in the final xAPI statement."""

    template = fields.Boolean()
    """bool: A flag indicating whether the SurveyBase is a template."""

    current_language = fields.Method('get_current_language', dump_only=True)
    """dict(str, str): The language the SurveyBase representation is currently 
    in. For a list of all available languages, see :class:`BabelLanguage`. 
    For more information on how this attribute is serialised, see 
    ``enum_field``."""

    available_languages = fields.List(enum_field(BabelLanguage), dump_only=True)
    """list(dict(str, str)): All languages for which translations of the
    SurveyBase are available. For a list of all available languages, see 
    :class:`BabelLanguage`. For more information on how this attribute is 
    serialized, see ``enum_field``."""

    shadow = fields.Boolean(dump_only=True)
    """bool: A flag indicating whether the SurveyBase is a copy of a 
    template."""

    reference_to = fields.Method('build_reference_to', dump_only=True)
    """dict(str, str): If the SurveyBase is a copy, this is the template
    serialised using the :class:`RESTFulSchema`."""

    owners = fields.Nested(DataClientSchema(only=("id", "href")), many=True,
                           dump_only=True)
    """list(dict): A list of DataClients, serialized using the 
    :class:`DataClientSchema`, who are owners of the SurveyBase."""

    owned_incoming_references = fields.Method(
        'build_owned_incoming_references',
        dump_only=True
    )
    """list: If the SurveyBase is a template, this is a list of SurveyBases 
    copying the SurveyBase. This attribute is serialised using the 
    :class:`RESTFulSchema`."""

    incoming_reference_count = fields.Method(
        'build_incoming_reference_count',
        dump_only=True
    )
    """int: If the SurveyBase is a template, this is the number of copies that 
    exist of the SurveyBase."""

    __private__ = [
        'shadow',
        'incoming_reference_count',
        'owned_incoming_references',
        'reference_to',
        'owners'
    ]

    def get_current_language(self, obj: SurveyBase) -> Dict[str, str]:
        """Helper method for serialising current_language.

        Args:
            obj: The SurveyBase which is being serialised at the moment.

        Returns:
            A dictionary resembling the way :function:`enum_field` serialises
            enum items. For example::

                {
                    'item_id': 'AF',
                    'value': 'Afrikaans'
                }
        """
        current_language = g._language
        if current_language not in obj.available_languages:
            current_language = obj.original_language
        # TODO(strangedev@posteo.net):
        #   use enum_field for this, move logic to SurveyBase class
        return {
            'item_id': current_language.name,
            'value': current_language.value
        }

    def build_reference_to(self, obj: SurveyBase) -> Dict[str, str]:
        """Helper method for serialising reference_to.

        Args:
            obj: The SurveyBase which is being serialised at the moment.

        Returns:
            A dictionary containing the serialised SurveyBase. The SurveyBase
            is not fully serialised, only id and href are included,
            for example::

                {
                    'id': 420,
                    'href': '/api/resource/for/surveybase/420'
                }

        Raises:
            DependencyInjectionError: The SurveyBase class did not register an
                API resource with the :class:`ResourceBroker`.
        """
        if not obj.shadow:
            return missing
        return RESTFulSchema().dump(obj.concrete)

    def build_owned_incoming_references(self, obj: SurveyBase) \
            -> List[Dict[str, str]]:
        """Helper method to serialise owned_incoming_references.

        Args:
            obj: The SurveyBase which is being serialised at the moment.

        Returns:
            A list of serialised SurveyBase objects which are copies of the
            SurveyBase. The SurveyBase objects are not fully serialised, only
            id and href are included. For example::

                [
                    { 'id': 420, 'href': '/api/resource/for/surveybase/420'},
                    { 'id': 1337, 'href': '/api/resource/for/surveybase/1337'}
                ]

        Raises:
            DependencyInjectionError: The SurveyBase class did not register an
                API resource with the :class:`ResourceBroker`.
        """
        accessible_copies = list(filter(
            lambda q: q.accessible_by(current_user()),
            obj.copies  # FIXME: scales linearly with the number of SurveyBases
        ))
        return RESTFulSchema(many=True).dump(accessible_copies)

    def build_incoming_reference_count(self, obj: SurveyBase) -> int:
        """Helper method for serialising incoming_reference_count.

        Args:
            obj: The SurveyBase which is being serialised at the moment.

        Returns:
            The number of existing copies of the SurveyBase.
        """
        return len(obj.copies)

    @classmethod
    def get_private(cls) -> List[str]:
        """Helper class method for getting a list of private attributes.

        Returns:
            A list of attribute names which should be stripped from the
            serialised SurveyBase when accessed by a non-owner.

        This method is used to determine which attributes should be stripped
        from the serialised SurveyBase, when the SurveyBase is accessed by a
        non-owner. This method exists, since __private__ is a private attribute,
        but sub-classes should have read access to their parent's private
        attributes in order to extend them.
        """
        if hasattr(cls, '__private__'):
            # This check is performed, since sub-classes may not explicitly
            # list their private attributes if they don't have any additional
            # private attributes compared to the super-class.
            return cls.__private__
        return []

    @post_dump(pass_original=True, pass_many=False)
    def strip_private_fields(self, data: Dict[str, Any],
                             original_data: SurveyBase = None) \
            -> Dict[str, Any]:
        """Post-serialisation hook for stripping private attributes.

        Args:
            data: The serialised SurveyBase as a dictionary.
            original_data: The SurveyBase which was serialised.

        Returns:
            The serialised SurveyBase with stripped private attributes, if
            the current_user is not an owner of the SurveyBase.
            The unmodified serialised SurveyBase otherwise.

        This method is executed by marshmallow after serialisation of a
        SurveyBase. If the current_user is not an owner of the SurveyBase,
        attributes listed in __private__ are stripped from the serialised
        SurveyBase.
        """
        def _strip(d):
            for k in self.get_private():
                if k in d:
                    del d[k]
            return d

        if isinstance(original_data, list):
            for od in original_data:
                if od.id == data['id']:
                    original_data = od
                    break

        if not original_data.modifiable_by(current_user()):
            return _strip(data)
