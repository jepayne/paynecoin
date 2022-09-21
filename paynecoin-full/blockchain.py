from hashlib import sha256
import json
from time import time
from urllib.parse import urlparse
import requests


class Wallets:
    def __init__(self):
        self.wallets = {}

    def wallets_get(self, uuid):
        if uuid is not None:
            try:
                return self.wallets[uuid]
            except KeyError:
                return None
        else:
            return self.wallets

    def wallet_create(self, uuid):
        transactions = []
        wallet = {"transactions": transactions, "balance": sum(transactions)}
        self.wallets[uuid] = wallet
        return self.wallets

    def wallet_update(self, uuid, amount=0):
        try:
            wallet = self.wallets[uuid]
        except KeyError:
            self.wallet_create(uuid)
            wallet = self.wallets[uuid]
        wallet["transactions"].append(amount)
        wallet["balance"] = sum(wallet["transactions"])
        return wallet


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Spawn the genesis block
        self.new_block(previous_hash="1", proof=100)

    def add_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError("Invalid URL")

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f"{last_block}")
            print(f"{block}")
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block["previous_hash"] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbors = self.nodes
        winning_neighbor = None
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbors:
            chain_response = requests.get(f"http://{node}/chain")
            if chain_response.status_code == 200:
                length = chain_response.json()["length"]
                chain = chain_response.json()["chain"]

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
                    winning_neighbor = node

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True, winning_neighbor

        return False, winning_neighbor

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "total_transactions": sum(
                [x.get("amount") for x in self.current_transactions]
            ),
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount,
            }
        )

        # TODO: I think there should not be a +1 here
        return self.last_block["index"] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a Block
        :param block: Block
        """

        # NOTE: dict must be sorted to avoid inconsistent hashes
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
