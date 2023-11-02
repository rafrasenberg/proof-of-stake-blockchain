from blockchain.block import Block


def test_block(transaction_pool):
    tx_pool = transaction_pool["pool"]
    block = Block(tx_pool.transactions, "last_hash", "forger", 1)
    block_representation = block.to_dict()
    assert block_representation["block_count"]
    assert block_representation["transactions"][0]["sender_public_key"]
    assert block_representation["forger"]
