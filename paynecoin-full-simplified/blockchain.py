from hashlib import sha256
import json
from time import time
from urllib.parse import urlparse


class Blockchain:
    def __init__(self, starting_transactions):
        """Initialize the blockchain.

        :param starting_transactions: A list of transactions to start the blockchain with"""
        self.current_transactions = starting_transactions
        self.chain = []
        # Spawn the genesis block
        self.chain.append(self.new_block(previous_hash="1"))

    def add_transaction(self, tx: dict) -> int:
        """
        Adds a transaction to the list of transactions
        :param tx: The transaction dict
        :return: The index of the Block that will hold this transaction
        """

        # Verify that the sender has enough funds to send this amount
        balances = self.get_balances()
        sender = tx["sender"]
        receiver = tx["receiver"]
        amount = tx["amount"]
        # sender == "0" specifies the mining reward
        if (amount > balances.get(sender, 0)) and (sender != "0"):
            raise ValueError("Not enough money to send")
        else:
            self.current_transactions.append(tx)
        return

    def get_balances(self):
        """Generate a dict of balances for each public key
        :return: A dict of balances"""
        # Put in the mining reward as an address
        balances = {"0": 0}
        # Start with whatever was received in the genesis block
        for tx in self.chain[0]["transactions"]:
            receiver = tx["receiver"]
            if receiver in balances.keys():
                balances[receiver] += tx["amount"]
            else:
                balances[receiver] = tx["amount"]
        # Cycle through subsequent blocks and add or subtract amounts
        for block in self.chain[1:]:
            for tx in block["transactions"]:
                sender = tx["sender"]
                receiver = tx["receiver"]
                amount = tx["amount"]
                balances[sender] -= amount
                if receiver in balances.keys():
                    balances[receiver] += amount
                else:
                    balances[receiver] = amount
        # Cycle through current pending transactions and add or subtract amounts
        for tx in self.current_transactions:
            sender = tx["sender"]
            receiver = tx["receiver"]
            amount = tx["amount"]
            balances[sender] -= amount
            if receiver in balances.keys():
                balances[receiver] += amount
            else:
                balances[receiver] = amount
        return balances

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        # Check that balances are positive
        balances = self.get_balances()
        for sender, balance in balances.items():
            # Skip the mining reward balance
            if (balance < 0) & (sender != "0"):
                return False

        # Cycle through each block in the chain and check conditions
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]

            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block["previous_hash"] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(block):
                return False

            last_block = block
            current_index += 1

        return True

    def new_block(self, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            "nonce": 0,
            "index": len(self.chain),
            "timestamp": time(),
            "transactions": self.current_transactions,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a Block (or any dictionary)
        :param block: Dict
        """
        # Note: recent versions of python use ordered dicts, so the
        # sort_keys=True parameter is not needed
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def proof_of_work(self, block):
        """
        Simple Proof of Work (PoW) algorithm:
        Adjust the nonce such that the hash of a block with that nonce contains leading 5 zeroes

        :param last_block: <dict> last block
        :return: <int>
        """

        nonce = 0
        block["nonce"] = nonce
        while self.valid_proof(block) is False:
            nonce += 1
            block["nonce"] = nonce
        # If we hit this point, we have found a valid nonce and saved it in block.
        return

    @staticmethod
    def valid_proof(block):
        """
        Validates the proof
        :param block <dict> Block to check
        :return: <bool> True if correct, False if not.
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        guess_hash = sha256(block_string).hexdigest()
        return guess_hash[:3] == "000"
