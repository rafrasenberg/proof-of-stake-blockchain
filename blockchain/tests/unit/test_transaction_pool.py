from blockchain.transaction.transaction_pool import TransactionPool


def test_transaction_pool(transaction):
    pool = TransactionPool()
    assert not pool.transaction_exists(transaction)
    pool.add_transaction(transaction)
    assert pool.transaction_exists(transaction)
