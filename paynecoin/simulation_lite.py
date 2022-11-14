"""In this file, I provide some sample code to get you started."""
from blockchain import Blockchain
from utils import (
    generate_keys,
    create_transaction,
    is_from_sender,
    public_key_to_string,
)

if __name__ == "__main__":

    # Start out with our private and public keys for You, Alice, and Bob
    key_dict = {}
    for name in ["You", "Alice", "Bob"]:
        private_key, public_key = generate_keys()
        key_dict[name] = {"private_key": private_key, "public_key": public_key}

    # Create our initial transaction by sending 100 tokens to yourself.
    transaction0 = create_transaction(
        private_key=key_dict["You"]["private_key"],
        public_key=public_key_to_string(key_dict["You"]["public_key"]),
        receiver=public_key_to_string(key_dict["You"]["public_key"]),
        amount=100,  # Start with 100 tokens. This is our (fixed) money supply
    )
    assert is_from_sender(transaction0)
    print(f"Transaction 0: {transaction0}")
    print(f"Transaction 0 is valid: {is_from_sender(transaction0)}")

    private_ledger = Blockchain(starting_transactions=[transaction0])
    block0_hash = Blockchain.hash(private_ledger.chain[0])
    print(f"Block 0 hash: {block0_hash}")
