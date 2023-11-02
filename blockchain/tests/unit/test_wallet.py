from blockchain.transaction.wallet import Wallet


def test_wallet_signature(transaction):
    wallet = Wallet()
    signature = wallet.sign(transaction.to_dict())
    assert int(signature, 16)


def test_wallet_signature_not_valid_with_to_dict(transaction):
    wallet = Wallet()
    signature = wallet.sign(transaction.to_dict())
    assert Wallet.signature_valid(
        transaction.to_dict(), signature, wallet.public_key_string()
    )

    transaction.sign(signature)
    assert Wallet.signature_valid(
        transaction.payload(), signature, wallet.public_key_string()
    )
    assert not Wallet.signature_valid(
        transaction.to_dict(), signature, wallet.public_key_string()
    )


def test_public_key_string():
    wallet = Wallet()
    public_key = wallet.public_key_string()
    assert "PUBLIC KEY" in public_key


def test_wallet_create_transaction(transaction_from_wallet):
    tx = transaction_from_wallet["transaction"]
    wallet = transaction_from_wallet["wallet"]

    tx_dict = tx.to_dict()

    assert "PUBLIC KEY" in tx_dict["sender_public_key"]
    assert tx_dict["receiver_public_key"]

    tx_payload = tx.payload()

    assert tx_payload["signature"] == ""
    assert Wallet.signature_valid(
        tx.payload(), tx.signature, wallet.public_key_string()
    )

    fraudulent_wallet = Wallet()

    assert not Wallet.signature_valid(
        tx.payload(),
        tx.signature,
        fraudulent_wallet.public_key_string(),
    )


def test_wallet_create_block(transaction_pool):
    pool = transaction_pool["pool"]
    wallet = transaction_pool["transaction_from_wallet"]["wallet"]

    fraudulent_wallet = Wallet()

    block = wallet.create_block(pool.transactions, "last_hash", 1)

    block_readable = block.to_dict()

    assert "PUBLIC KEY" in block_readable["transactions"][0]["sender_public_key"]
    assert block_readable["forger"]
    assert block_readable["block_count"]

    assert Wallet.signature_valid(
        block.payload(), block.signature, wallet.public_key_string()
    )
    assert not Wallet.signature_valid(
        block.payload(), block.signature, fraudulent_wallet.public_key_string()
    )
