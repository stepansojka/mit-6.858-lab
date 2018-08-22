from debug import *
from zoodb import *
import rpclib

def _connect():
    return rpclib.client_connect('/banksvc/sock')


def transfer(sender, token, recipient, zoobars):
    with _connect() as c:
        return c.call('transfer', sender=sender, token=token, recipient=recipient, zoobars=zoobars)


def balance(username):
    with _connect() as c:
        return c.call('balance', username=username)


def add_user(username):
    with _connect() as c:
        return c.call('add_user', username=username)


def get_log(username):
    with _connect() as c:
        return c.call('get_log', username=username)

