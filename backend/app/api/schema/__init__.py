from marshmallow import Schema, fields

from api.utils.ResourceBroker import ResourceBroker

__author__ = "Noah Hummel"


class RESTFulSchema(Schema):
    """A serialisation schema for resources."""

    id = fields.Int(dump_only=True)
    """int: An integer uniquely identifying the resource."""

    href = fields.Method('build_href', dump_only=True)
    """str: The API URL where the resource can be fetched."""

    def build_href(self, obj) -> str:
        """Generates a URL pointing to the API resource where an object can be
        fetched.

        Args:
            obj(Model): The object whose URL should be generated.

        Returns:
            The URL from which the object may be fetched.

        Raises:
            DependencyInjectionError: The object's class has not registered an
                API resource with the ResourceBroker.
        """
        return ResourceBroker.url_for(obj)
