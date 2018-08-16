from zoodb import *
from debug import *

import hashlib
import random
import os
import pbkdf2


def newtoken(db, cred):
    hashinput = "%s%.10f" % (cred.password_hash, random.random())
    cred.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return cred.token


def login(username, password):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if not cred:
        return None

    hash = pbkdf2.PBKDF2(password, cred.password_salt).hexread(Cred.PASSWORD_HASH_SIZE)
    if cred.password_hash == hash:
        return newtoken(db, cred)
    else:
        return None


def register(username, password):
    cred_db = cred_setup()
    cred = cred_db.query(Cred).get(username)
    if cred:
        return None

    newcred = Cred()
    newcred.username = username
    newcred.password_salt = os.urandom(Cred.SALT_SIZE)
    newcred.password_hash = pbkdf2.PBKDF2(password, newcred.password_salt).hexread(Cred.PASSWORD_HASH_SIZE)
    cred_db.add(newcred)
    cred_db.commit()

    person_db = person_setup()
    newperson = Person()
    newperson.username = username
    person_db.add(newperson)
    person_db.commit()

    return newtoken(cred_db, newcred)


def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False

