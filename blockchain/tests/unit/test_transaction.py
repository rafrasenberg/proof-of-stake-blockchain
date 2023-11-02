def test_transaction(transaction):
    tx_dict = transaction.to_dict()

    assert tx_dict["id"]
    assert tx_dict["timestamp"]
    assert tx_dict["amount"] == 1


def test_transaction_sign(transaction, wallet_signature):
    transaction.sign(wallet_signature)
    tx_dict = transaction.to_dict()

    assert tx_dict["id"]
    assert tx_dict["timestamp"]
    assert not tx_dict["signature"] == ""
