from zoodb import *
from debug import *

import time
import auth_client

def transfer(sender, token, recipient, zoobars):
    if not auth_client.check_token(sender, token):
        raise ValueError()

    bankdb = bank_setup()
    senderp = bankdb.query(Bank).get(sender)
    recipientp = bankdb.query(Bank).get(recipient)

    sender_balance = senderp.zoobars - zoobars
    recipient_balance = recipientp.zoobars + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    senderp.zoobars = sender_balance
    recipientp.zoobars = recipient_balance
    bankdb.commit()

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()


def balance(username):
    db = bank_setup()
    bank = db.query(Bank).get(username)
    return bank.zoobars


def get_log(username):
    db = transfer_setup()
    transfers = db.query(Transfer).filter(or_(Transfer.sender==username,
                                              Transfer.recipient==username)).all()
    return [{'time': t.time,
             'sender': t.sender,
             'recipient': t.recipient,
             'amount': t.amount} for t in transfers]


def add_user(username):
    db = bank_setup()

    user = Bank()
    user.username = username
    db.add(user)
    db.commit()
