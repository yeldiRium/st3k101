from flask import g
from memcache import Client

__author__ = "Noah Hummel, Hannes Leutloff"


def get_memcache() -> Client:
    """
    Factory method for memcache.Client.
    Instantiates only one memcached client per request.
    :return: Client The memcached client
    """

    mc = getattr(g, '_memcache_client', None)
    if mc is None:
        mc = g._memcache_client = Client(['memcached'],
                                         debug=g._config['DEBUG'])

    return mc
