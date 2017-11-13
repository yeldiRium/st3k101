from flask import request


def get_client_ip():
    """
    Returns the client's IP address. Also takes into account that this app will be behind a proxy,
    because it will be deployed with docker. It does this by checking the X-Forwarded-For http header attribute
    which is set by in-between proxies.
    :return: str The client's IP
    """
    return request.headers.get('X-Forwarded-For', request.remote_addr)