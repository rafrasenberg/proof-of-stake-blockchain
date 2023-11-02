import pytest

from blockchain.transaction.transaction import Transaction
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet


@pytest.fixture(scope="function")
def transaction():
    sender = "sender"
    receiver = "receiver"
    amount = 1
    type = "transfer"
    return Transaction(sender, receiver, amount, type)


@pytest.fixture(scope="function")
def transaction_from_wallet():
    receiver = "receiver"
    amount = 1
    type = "transfer"
    wallet = Wallet()
    transaction = wallet.create_transaction(receiver, amount, type)
    return {"transaction": transaction, "wallet": wallet}


@pytest.fixture(scope="function")
def transaction_pool(transaction_from_wallet):
    tx = transaction_from_wallet["transaction"]
    pool = TransactionPool()
    if not pool.transaction_exists(tx):
        pool.add_transaction(tx)
    return {"pool": pool, "transaction_from_wallet": transaction_from_wallet}


@pytest.fixture(scope="function")
def block(transaction_pool):
    pool = TransactionPool()
    if not pool.transaction_exists(transaction):
        pool.add_transaction(transaction)
    return pool


@pytest.fixture(scope="function")
def wallet_signature(transaction):
    wallet = Wallet()
    return wallet.sign(transaction.to_dict())
