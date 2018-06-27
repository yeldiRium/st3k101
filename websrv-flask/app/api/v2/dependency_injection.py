from api.v2 import api
from model.SQLAlchemy import db

__author__ = "Noah Hummel"


class DependencyInjectionException(Exception):
    pass


class ResourceBroker(object):
    _model_resource_map = dict()

    @classmethod
    def add_resource_for(cls, resource, model, id_naming_convention=None):
        cls._model_resource_map[model] = {
            'resource': resource,
            'id_naming_convention': id_naming_convention
        }

    @classmethod
    def url_for(cls, obj: db.Model):
        config_key = 0
        for k in cls._model_resource_map:
            if isinstance(obj, k):
                config_key = k

        model = obj.__class__
        config = cls._model_resource_map.get(config_key, None)
        if not config:
            raise DependencyInjectionException('No resource for {}'.format(model))
        resource = config['resource']
        url_kwargs = dict()
        if config['id_naming_convention']:
            url_kwargs[config['id_naming_convention']] = obj.id
        return api.url_for(resource, **url_kwargs)
