import copy
import time
import uuid


class Transaction:
    def __init__(self, sender_public_key, receiver_public_key, amount, type):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ""

    def to_dict(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    def payload(self):
        dict_respresentation = copy.deepcopy(self.to_dict())
        dict_respresentation["signature"] = ""
        return dict_respresentation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        return False
