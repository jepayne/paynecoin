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


def mine(miner: str, chain: Blockchain) -> dict:
    """
    Mine a block for a given miner.

    Gives a mining reward to the miner and provides the proof of work

    :param miner: The miner's public key
    :param chain: The blockchain
    :return: The mined block
    """
    # Create a block to mine. chain.current_transactions will be included
    block_to_mine = chain.new_block()
    # Add the mining reward
    reward = create_transaction(
        private_key=None, public_key="0", receiver=miner, amount=1
    )
    block_to_mine["transactions"].append(reward)
    # This updates the nonce in block_to_mine to solve the mining puzzle
    chain.proof_of_work(block_to_mine)
    return block_to_mine


# A wrapper for the mine function with only one argument
def parallel_mine(iter):
    return mine(*iter)


if __name__ == "__main__":
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
        ledgers[name] = Blockchain(
            starting_transactions=deepcopy(starting_transactions)
        )

    # Add a transaction to each node's list of current transactions
    new_tx = create_transaction(
        private_key=None,
        public_key=public_key_to_string(key_dict["You"]["public_key"]),
        receiver=public_key_to_string(key_dict["Alice"]["public_key"]),
        amount=2,
    )
    for name in names:
        ledgers[name].add_transaction(deepcopy(new_tx))

    # In parallel, have each node try to mine a block
    # With imap_unordered, the first result is the first task to finish
    # So here, new_block is the block mined by the fastest miner
    p = mp.Pool(len(names))  # Set up the number of parallel tasks to run
    for new_block in p.imap_unordered(
        parallel_mine,  # Function to run in parallel
        zip(  # Arguments to the function
            [public_key_to_string(key_dict[name]["public_key"]) for name in names],
            [ledgers[name] for name in names],
        ),
        chunksize=1,
    ):
        if new_block:  # Triggers when the first task is finished
            print("A block has been mined")  # You can delete this line
            p.terminate()
            break
    print(new_block)  # Note the extra mining reward from '0' to the miner

    # Add the new block to each node
    for name in names:
        ledgers[name].chain.append(new_block)

    # Print the balances of each node's blockchain, which will all be the same
    for name in names:
        print(name, ledgers[name].get_balances())
