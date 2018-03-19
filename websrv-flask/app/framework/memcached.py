from flask import g
from bmemcached import Client

__author__ = "Noah Hummel, Hannes Leutloff"


def get_memcache() -> Client:
    """
    Factory method for bmemcached.Client.
    Instantiates only one memcached client per request.
    :return: Client The memcached client
    """

    mc = getattr(g, '_memcache_client', None)
    if mc is None:
        mc = g._memcache_client = Client(
            ['memcached:11211'],
            g._config["MEMCACHED_USERNAME"],
            g._config["MEMCACHED_PASSWORD"]
        )
    return mc
