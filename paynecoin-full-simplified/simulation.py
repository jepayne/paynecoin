#%%

"""In this file, I provide some sample code to get you started."""
from blockchain import Blockchain
from utils import (
    generate_keys,
    create_transaction,
    public_key_to_string,
)
from copy import deepcopy
import multiprocessing as mp
from functools import partial

# This could be a class method of the Blockchain class
def mine(chain, miner):
    """Mine a block for a given miner"""
    # Create a block to mine. chain.current_transactions will be in there
    block_to_mine = chain.new_block()
    # Add the mining reward
    reward = create_transaction(
        private_key=None, public_key="0", receiver=miner, amount=1
    )
    block_to_mine["transactions"].append(reward)
    # This updates the nonce in block_to_mine to solve the mining puzzle
    chain.proof_of_work(block_to_mine)
    return block_to_mine


# Start out with our private and public keys for You, Alice, and Bob
key_dict = {}
names = ["You", "Alice", "Bob"]
for name in names:
    private_key, public_key = generate_keys()
    key_dict[name] = {"private_key": private_key, "public_key": public_key}

starting_transactions = [
    create_transaction(
        private_key=None,
        public_key=0,
        receiver=public_key_to_string(key_dict["You"]["public_key"]),
        amount=10,  # Start with 10 tokens
    )
]

# Create a copy of the blockchain for each person
# Note that deepcopy is necessary here
ledgers = {}
for name in names:
    ledgers[name] = Blockchain(starting_transactions=deepcopy(starting_transactions))

# Add a transaction to each node
new_tx = create_transaction(
    private_key=None,
    public_key=public_key_to_string(key_dict["You"]["public_key"]),
    receiver=public_key_to_string(key_dict["Alice"]["public_key"]),
    amount=2,
)
for name in names:
    ledgers[name].add_transaction(deepcopy(new_tx))

# In parallel, have each node try to mine a block
# From StackOverflow: worker function takes in an int
# With imap_unordered, the first result is the first task to finish
p = mp.Pool(4)
for result in p.imap_unordered(worker, range(20), chunksize=1):
    if result == 0:
        print("terminating")
        p.terminate()
        break
print("done")
# new_block = mine(ledger, public_key_to_string(key_dict["Bob"]["public_key"]))
# ledger.chain.append(new_block)
# print(ledger.get_balances())

# %%
