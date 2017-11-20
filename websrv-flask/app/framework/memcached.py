from flask import g
from bmemcached import Client


def get_memcache():
    """
    Instantiates only one memcached client per request.
    :return: The memcached client
    """

    mc = getattr(g, '_memcache_client', None)
    if mc is None:
        mc = g._memcache_client = Client(
            ['memcached:11211'],
            g._config["MEMCACHED_USERNAME"],
            g._config["MEMCACHED_PASSWORD"]
        )
    return mc
