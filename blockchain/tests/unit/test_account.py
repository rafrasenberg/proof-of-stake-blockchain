import pytest

from blockchain.blockchain import Blockchain
from blockchain.transaction.account_model import AccountModel
from blockchain.transaction.transaction_pool import TransactionPool
from blockchain.transaction.wallet import Wallet
from blockchain.utils.helpers import BlockchainUtils


def test_account_model():
    wallet = Wallet()
    public_key_string = wallet.public_key_string()
    account_model = AccountModel()

    account_model.add_account(public_key_string)
    assert account_model.balances[public_key_string] == 0
    account_model.update_balance(public_key_string, 5)
    assert account_model.balances[public_key_string] == 5


def test_account_model_with_blockchain():
    blockchain = Blockchain()
    pool = TransactionPool()

    john = Wallet()
    jane = Wallet()
    exchange = Wallet()
    forger = Wallet()

    # John buys 10 tokens from exchange
    exchange_transaction = exchange.create_transaction(
        john.public_key_string(), 10, "EXCHANGE"
    )

    if not pool.transaction_exists(exchange_transaction):
        pool.add_transaction(exchange_transaction)

    # Add to blockchain
    covered_transaction = blockchain.get_covered_transaction_set(pool.transactions)
    last_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hex()
    block_count = blockchain.blocks[-1].block_count + 1
    block_one = forger.create_block(covered_transaction, last_hash, block_count)
    blockchain.add_block(block_one)
    pool.remove_from_pool(block_one.transactions)

    # John sends 5 tokens to Jane
    transaction = john.create_transaction(jane.public_key_string(), 5, "TRANSFER")

    if not pool.transaction_exists(transaction):
        pool.add_transaction(transaction)

    # Add to blockchain
    covered_transaction = blockchain.get_covered_transaction_set(pool.transactions)
    last_hash = BlockchainUtils.hash(blockchain.blocks[-1].payload()).hex()
    block_count = blockchain.blocks[-1].block_count + 1
    block_two = forger.create_block(covered_transaction, last_hash, block_count)
    blockchain.add_block(block_two)
    pool.remove_from_pool(block_one.transactions)

    blockchain_representation = blockchain.to_dict()

    assert blockchain_representation["blocks"][0]["last_hash"] == "genesis_hash"
    assert blockchain_representation["blocks"][1]["transactions"][0]["amount"] == 10
    with pytest.raises(IndexError):
        # Make sure transactions are not duplicate in new block (remove_from_pool)
        assert blockchain_representation["blocks"][2]["transactions"][1]
    assert blockchain_representation["blocks"][2]["transactions"][0]["amount"] == 5
