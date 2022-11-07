#%%

"""In this file, I provide some sample code to get you started."""
from blockchain import Blockchain
from utils import (
    generate_keys,
    create_transaction,
    public_key_to_string,
)

"""
What do we need to do here?

Instantiate set of users with addresses and balances
    Not sure I need this! Current blockchain keeps track of balances, so adding blocks may be enough
    Maybe adding blocks needs a user to be specified, and the user's balance is updated
Instantiate set of blockchains, one for each user
Way for updates (new blocks) to propogate to other chains
    self.valid_chain(self.chain + [new_block])
Way for blockchains to accept / reject blocks
    See above
Propogation of transactions
    Probably have to do this synchronously



How do I do this asynchronously?
"""

# This could be a class method of the Blockchain class
def mine(chain, miner):
    """Mine a block for a given miner"""
    # Create a block to mine. chain.current_transactions will be in there
    block_to_mine = chain.new_block()
    # Add the mining reward
    reward = create_transaction(private_key=None, public_key="0", receiver=miner, amount=1)
    block_to_mine["transactions"].append(reward)
    # This updates the nonce in block_to_mine to solve the mining puzzle
    chain.proof_of_work(block_to_mine)
    return block_to_mine


# Start out with our private and public keys for You, Alice, and Bob
key_dict = {}
for name in ["You", "Alice", "Bob"]:
    private_key, public_key = generate_keys()
    key_dict[name] = {"private_key": private_key, "public_key": public_key}

# # Create our initial transaction by sending 100 tokens to yourself.
# transaction0 = create_transaction(
#     private_key=None,
#     public_key=None,
#     receiver=public_key_to_string(key_dict["You"]["public_key"]),
#     amount=100,  # Start with 100 tokens
# )

ledger = Blockchain(starting_transactions=[])
new_tx = create_transaction(
        private_key=None,
        public_key=public_key_to_string(key_dict["You"]["public_key"]),
        receiver=public_key_to_string(key_dict["Alice"]["public_key"]),
        amount=0,
    )
ledger.add_transaction(new_tx)
new_block = mine(ledger, public_key_to_string(key_dict["You"]["public_key"]))
ledger.chain.append(new_block)
print(ledger.get_balances())

# %%
