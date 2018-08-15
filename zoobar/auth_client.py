from debug import *
from zoodb import *
import rpclib

def _connect():
    return rpclib.client_connect('/authsvc/sock')


def login(username, password):
    with _connect() as c:
        return c.call('login', username=username, password=password)


def register(username, password):
    with _connect() as c:
        return c.call('register', username=username, password=password)


def check_token(username, token):
    with _connect() as c:
        return c.call('check_token', username=username, token=token)

