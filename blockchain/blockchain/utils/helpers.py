import json

import jsonpickle
from cryptography.hazmat.primitives import hashes


class BlockchainUtils:
    @staticmethod
    def hash(data):
        data_string = json.dumps(data)
        data_bytes = data_string.encode("utf-8")

        data_hash = hashes.Hash(hashes.SHA256())
        data_hash.update(data_bytes)
        data_hash_value = data_hash.finalize()

        return data_hash_value

    @staticmethod
    def encode(obj):
        return jsonpickle.encode(obj, unpicklable=True)

    @staticmethod
    def decode(encoded_obj):
        # CAUTION: Never deserialize data that you can not 100% trust
        return jsonpickle.decode(encoded_obj)  # nosec
