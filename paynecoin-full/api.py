import requests
from flask import Flask, jsonify, request
from blockchain import Blockchain
from blockchain import Wallets
from uuid import uuid4

MINING_REWARD = 1

# Instantiate the Node
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Instantiate the Blockchain and Wallets
blockchain = Blockchain()
wallets = Wallets()


@app.route("/mine", methods=["GET"])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    sender = "0"
    amount = MINING_REWARD
    blockchain.new_transaction(
        sender=sender,
        recipient=node_uuid,
        amount=amount,
    )
    wallets.wallet_update(node_uuid, amount)

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200


@app.route("/wallets", methods=["GET"])
def full_wallets():
    response = wallets.wallets
    return jsonify(response), 200


@app.route("/wallets/<uuid>", methods=["GET"], strict_slashes=False)
def route_wallets_get(uuid):
    response = wallets.wallets_get(uuid=uuid)
    return jsonify(response)


@app.route(
    "/wallets/new/", methods=["GET"], defaults={"uuid": None}, strict_slashes=False
)
@app.route("/wallets/new/<uuid>", methods=["GET"], strict_slashes=False)
def route_wallets_new(uuid):
    uuid = uuid if uuid is not None else str(uuid4().hex)
    response = wallets.wallet_create(uuid=uuid)
    return jsonify(response)


@app.route("/wallets/update/<uuid>", methods=["GET"])
def route_wallets_update(uuid):
    response = {
        "message": "Wallet updated",
        "uuid": uuid,
        "wallet": wallets.wallet_update(uuid),
    }
    return jsonify(response)


@app.route("/transaction", methods=["POST"])
def new_transaction():
    values = request.get_json()
    print(values)

    # Check that the required fields are in the POSTed data
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # Create a new Transaction
    index = blockchain.new_transaction(
        values["sender"], values["recipient"], values["amount"]
    )

    # Update wallets
    wallets.wallet_update(values["sender"], -values["amount"])
    wallets.wallet_update(values["recipient"], values["amount"])

    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201


@app.route("/chain", methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()

    nodes = values.get("nodes")
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        "message": "New nodes have been added",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route("/nodes/register", methods=["GET"])
def register_nodes_get():
    response = list(blockchain.nodes)
    return jsonify(response), 201


@app.route("/nodes/resolve", methods=["GET"])
def consensus():
    # Update longest chain
    replaced, neighbor = blockchain.resolve_conflicts()
    # If a longer chain was found, update wallets with that node's transactions
    if replaced:
        response = {"message": "Our chain was replaced", "new_chain": blockchain.chain}
        updated_wallets = requests.get(f"http://{neighbor}/wallets").json()
        wallets.wallets = updated_wallets.copy()

    else:
        response = {"message": "Our chain is authoritative", "chain": blockchain.chain}

    return jsonify(response), 200


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    parser.add_argument(
        "-u", "--uuid", default=None, type=str, help="unique identifier for node"
    )
    args = parser.parse_args()
    port = args.port
    # Generate a globally unique address for this node if none is specified
    node_uuid = args.uuid if args.uuid is not None else str(uuid4().hex)

    app.run(host="0.0.0.0", port=port)
