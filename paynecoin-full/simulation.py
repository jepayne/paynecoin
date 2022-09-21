"""
Before running this, spawn 5 nodes in a terminal: bash payne_nodes.sh init 5
The spawned nodes will be on 5001, 5002, 5003, 5004, 5005 by default with uuids
alice, bob, carol, dave, and eve respectively.
"""

import os
import subprocess
import requests
import secrets
from random import randrange
from hashlib import sha256
import random


def req_endpoint(endpoint, port=5001, data=None):
    """Send a request to a specific endpoint on a specific port"""
    # Check valid request
    get_reqs = ["/nodes/resolve", "/chain", "/mine", "/wallets"]
    post_reqs = ["/nodes/register", "/transaction"]
    if endpoint not in get_reqs + post_reqs:
        print("invalid request")
        return -1
    # Determine request address and method
    base_url = f"http://127.0.0.1:{port}"
    url = f"{base_url}{endpoint}"
    is_post = any(kwd in endpoint for kwd in post_reqs)
    if is_post:
        if data is None:
            print("POST requests required data")
            return -1
        else:
            req = requests.post(url, json=data)
    else:
        req = requests.get(url)
    return req.json()


def simulate_transaction(sender, recipient, amount):
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    return transaction


def get_balances(uuids):
    balances = {}
    wallets = req_endpoint("/wallets")
    for uuid in uuids:
        if uuid in wallets.keys():
            balances[uuid] = wallets[uuid]["balance"]
        else:
            balances[uuid] = 0
    return balances


# 5 miners with their 5 wallets at ports 5001, 5002, 5003, 5004, 5005
nodes_uuids = ["alice", "bob", "carol", "dave", "eve"]
ports = list(range(5001, 5001 + len(nodes_uuids)))

# nodes_dict is the mapping of node uuid (person's name) to port
nodes_dict = dict(zip(nodes_uuids, ports))

# Register nodes. This makes each miner's blockchain aware of the other miners
nodes_register_body = {"nodes": [f"http://127.0.0.1:{port}" for port in ports]}
for port in ports:
    req_endpoint("/nodes/register", port=port, data=nodes_register_body)

balances = {uuid: [] for uuid in nodes_uuids}
nperiods = 10

print(f"Simulating {nperiods} periods of transactions between {nodes_uuids}")

# Note that this blockchain implementation does not screen for negative balances
for t in range(nperiods):
    # Randomly make a transaction
    current_balances = get_balances(nodes_uuids)
    sender = random.choice(nodes_uuids)
    if current_balances[sender] == 0:  # Randomly-chosen sender has no money
        sender = max(
            current_balances, key=current_balances.get
        )  # Choose sender with most money
    # Choose recipient who is not the sender
    recipient = random.choice([n for n in nodes_uuids if n != sender])
    # Send a random percentage of sender's tokens to recipient
    amount = random.random() * current_balances[sender]
    transaction = simulate_transaction(sender, recipient, amount)
    # Broadcast transaction to all nodes
    for port in ports:
        req_endpoint(
            "/transaction",
            port=port,
            data=transaction,
        )
    # Randomly select a miner. This is similar but not equivalent to all miners
    # mining at the same time, with one randomly winning
    miner = random.choice(nodes_uuids)
    print(f"Miner: {miner} for period {t+1}")
    req_endpoint("/mine", port=nodes_dict.get(miner))

    # Broadcast the new block to all nodes and update their wallets
    for node_port in nodes_dict.values():
        req_endpoint("/nodes/resolve", port=node_port)

    # Update balances post-transaction and post-mining reward
    current_balances = req_endpoint("/wallets", port=5001)
    for uuid in nodes_uuids:
        if uuid in current_balances.keys():
            balances[uuid].append(current_balances[uuid]["balance"])
        else:
            balances[uuid].append(0)

print("Balance history is:")
print(balances)

# Plot balances over time for each user

# Plot total money supply

# Plot cpu usage
