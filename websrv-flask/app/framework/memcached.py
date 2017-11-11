from flask import g
from memcache import Client


def get_memcache():
    """
    Instantiates only one memcached client per request.
    :return: The memcached client
    """

    mc = getattr(g, '_memcache_client', None)
    if mc is None:
        mc = g._memcache_client = Client(['memcached'], debug=g._config['DEBUG'])
    return mc
