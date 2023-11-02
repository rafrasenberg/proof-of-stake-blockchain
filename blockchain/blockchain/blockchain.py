import logging

from blockchain.block import Block
from blockchain.pos.proof_of_stake import ProofOfStake
from blockchain.transaction.account_model import AccountModel
from blockchain.utils.helpers import BlockchainUtils


class Blockchain:
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = AccountModel()
        self.pos = ProofOfStake()

    def add_block(self, block):
        self.execute_transactions(block.transactions)
        self.blocks.append(block)

    def to_dict(self):
        data = {}
        blocks_readable = []
        for block in self.blocks:
            blocks_readable.append(block.to_dict())
        data["blocks"] = blocks_readable
        return data

    def block_count_valid(self, block):
        if self.blocks[-1].block_count == block.block_count - 1:
            return True
        return False

    def last_block_hash_valid(self, block):
        last_block_chain_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()
        ).hex()
        if last_block_chain_block_hash == block.last_hash:
            return True
        return False

    def get_covered_transaction_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                logging.error("Transaction is not covered by sender")
        return covered_transactions

    def transaction_covered(self, transaction):
        # Assume the exchange always has the amount of tokens
        if transaction.type == "EXCHANGE":
            return True
        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance >= transaction.amount:
            return True
        return False

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):
        if transaction.type == "STAKE":
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.account_model.update_balance(sender, -amount)
        else:
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            amount = transaction.amount
            self.account_model.update_balance(sender, -amount)
            self.account_model.update_balance(receiver, amount)

    def next_forger(self):
        last_block_hash = BlockchainUtils.hash(self.blocks[-1].payload()).hex()
        next_forger = self.pos.forger(last_block_hash)
        return next_forger

    def create_block(self, transactions_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transaction_set(transactions_from_pool)
        self.execute_transactions(covered_transactions)
        new_block = forger_wallet.create_block(
            covered_transactions,
            BlockchainUtils.hash(self.blocks[-1].payload()).hex(),
            len(self.blocks),
        )
        self.blocks.append(new_block)
        return new_block

    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False

    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.last_hash)
        proposed_block_forger = block.forger
        if forger_public_key == proposed_block_forger:
            return True
        return False

    def transactions_valid(self, transactions):
        covered_transactions = self.get_covered_transaction_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        return False
