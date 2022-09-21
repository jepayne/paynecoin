from hashlib import sha256
import json
from time import time
from urllib.parse import urlparse
import requests


class Blockchain:
    def __init__(self, starting_transactions):
        """Initialize the blockchain.

        :param starting_transactions: A list of transactions to start the blockchain with"""
        self.current_transactions = starting_transactions
        self.chain = []
        # Spawn the genesis block
        self.new_block(previous_hash="1")

    def add_transaction(self, tx: dict) -> int:
        """
        Adds a transaction to the list of transactions
        :param tx: The transaction dict
        :return: The index of the Block that will hold this transaction
        """
        # TODO: Verify that the transaction is validly signed

        # end TODO

        # Verify that the sender has enough funds to send this amount
        balances = self.get_balances()
        sender = tx["sender"]
        receiver = tx["receiver"]
        amount = tx["amount"]
        if (sender not in balances.keys()) or (amount > balances[sender]):
            raise ValueError("Not enough money to send")
        else:
            self.current_transactions.append(tx)
        return self.last_block["index"] + 1

    def get_balances(self):
        """Generate a dict of balances for each public key
        :return: A dict of balances"""
        balances = {}
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
            if balance < 0:
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

            # If this blockchain implemented proof of work, we would need to check
            # that here for each block

            # TODO: check that transactions are all validly signed in this block

            # end TODO

            last_block = block
            current_index += 1

        return True

    def new_block(self, previous_hash):
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

        self.chain.append(block)
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

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work (PoW) algorithm:
            - Find a number p' such that hash(pp') contains leading 5 zeroes
            - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last block
        :return: <int>
        """

        last_proof = last_block["proof"]

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f"{last_proof}{proof}".encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"
