This subfolder provides code related to homework 3, simulating a decentralized transparent ledger.
For a very quick start, run the following in your (poetry) shell from this directory:
```sh
bash paynecoin_nodes.sh init 5
python simulation.py
bash paynecoin_nodes.sh kill
```

- [1. Initializing nodes](#1-initializing-nodes)
  - [1.1. Manual node initialization](#11-manual-node-initialization)
  - [1.2. Bulk node initialization](#12-bulk-node-initialization)
- [2. Interacting with the blockchain](#2-interacting-with-the-blockchain)
  - [2.1. Simulating transactions](#21-simulating-transactions)
  - [2.2. Low-level details](#22-low-level-details)
- [3. Exercises](#3-exercises)
  - [3.1. Proof of work versus proof of stake](#31-proof-of-work-versus-proof-of-stake)
  - [3.2. Blockchain vulnerabilities](#32-blockchain-vulnerabilities)
- [4. Sample code](#4-sample-code)
- [5. Additional materials](#4-additional-materials)

# 1. Initializing nodes

Nodes are virtual representations of the agents that will be interacting with the blockchain. First they have to be initialized, at which point they will be assigned a port in the local host (e.g. `http://localhost:5001/`). Think of each node as a separate individual with their own copy of the blockchain. The API constructed here is simply a structured way for the nodes to communicate updates with each other.

## 1.1. Manual node initialization

Initialize a node in the development server with
```sh
python paynecoin/api.py
```
This initializes a node in the default port, `5001`.
You can initialize additional nodes in other ports by using the `-p <port>` option. For example,
```sh
python paynecoin/api.py -p 5002
```

Each node is assigned an automatically-generated node UUID. However, you can specify a custom UUID for the node using the `-u <uuid>` option. For example,
```sh
python paynecoin/api.py p 5002 -u bob
```
Whenever a node mines a block, the reward will be associated to this node UUID.

## 1.2. Bulk node initialization

There is a simple auxiliary shell script that makes it easier to initialize and terminate nodes in bulk.
The script is in [`paynecoin_nodes.sh`](paynecoin_nodes.sh).
- **Initialize** a sequence of nodes associated to ports `5001, ..., 5000+(i)` by running
```sh
bash payne_nodes.sh init [i]
```
where `[i]` is an optional integer; if none is specified, the program will initialize a single node in port `5001`.
For example, you can initialize three nodes associated to ports `5001`, `5002`, and `5003` by running
```sh
bash tests/payne_nodes.sh init 3
```
- **List** the jobs associated to the running nodes using `bash paynecoin_nodes.sh list`.
- **Kill**  all the initialized nodes using `bash paynecoin_nodes.sh kill`

When using bulk node initialization, the first 10 nodes will be given uuids "alice", "bob", "carol", "dave", "eve", "frank", "george", "harry", "iris", and "james".

### Note <!-- omit in toc -->

Node instances are simply Python processes, which can be managed with the usual Unix tools. For example, you can list the processes running the nodes with
```sh
ps ax | grep api.py | grep -v grep
```
You can kill these processes using, for example,
```sh
kill $(ps ax | grep api.py | grep -v grep | awk '{print $1}')
```

# 2. Interacting with the blockchain

## 2.1 Simulating transactions

The script [`simulation.py`](simulation.py) contains some functions and code to easily manage the blockchain using Python.
Take a look at this file and the functions within to mine blocks, post transactions and check the blockchain.

## 2.2 Low-level details

This implementation serves the blockchain as an API with which we can interact using HTTP requests (i.e. ```GET``` and ```POST```). Each node (i.e., individual running a copy of the blockchain) you have initialized is tied to a specific URL. You can retrieve data from a particular node using ```GET``` requests to that URL, and send data using ```POST``` requests to that URL. Under the hood, the provided simulation script is using this interface.
An easy way to manage these requests interactively is to use a tool like [Postman](https://www.postman.com/downloads/).

<table>
<thead>
  <tr>
    <th>request</th>
    <th>method</th>
    <th>description</th>
    <th>request body</th>
    <th>request body example</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><pre>/nodes/register</pre></td>
    <td><pre>POST</pre><br></td>
    <td>register a list of new nodes in the form of URLs</td>
    <td>JSON list of URLs</td>
    <td><pre>{<br>    "nodes": [<br>        "http://localhost:5000",<br>        "http://localhost:5001"<br>    ]<br>}</pre></td>
  </tr>
   <tr>
    <td><pre>/nodes/register</pre></td>
    <td><pre>GET</pre><br></td>
    <td>list registered nodes</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/nodes/resolve</pre></td>
    <td><pre>GET</pre><br></td>
    <td>implement consensus algorithm to resolve conflicts</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/chain</pre></td>
    <td><pre>GET</pre><br></td>
    <td>return full blockchain</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/mine</pre></td>
    <td><pre>GET</pre><br></td>
    <td>mine a new block</td>
    <td>NA</td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/transaction</pre></td>
    <td><pre>POST</pre><br></td>
    <td>register a new transaction</td>
    <td>JSON list of transaction parameters</td>
    <td><pre>{<br>    "sender": "alvaro",<br>    "recipient": "jonathan",<br>    "amount": 42<br>}</pre></td>
  </tr>
  <tr>
    <td><pre>/wallets</pre></td>
    <td><pre>GET</pre><br></td>
    <td>get all wallets</td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td><pre>/wallets/{uuid}</pre></td>
    <td><pre>GET</pre><br></td>
    <td>get wallet of {uuid}</td>
    <td></td>
    <td></td>
  </tr>
</tbody>
</table>

# 3. Exercises

You will be asked to answer a subset of these on homework 3.

# 3.1. Proof of work versus proof of stake

1. Simulate proof of work for a blockchain of length at least 100 involving transactions with at least 5 nodes (hint: [simulation.py](simulation.py) does almost exactly this). Plot the time taken to mine each block as well as balances of each individual over time. Also plot the total money supply over time.
2. Simulate another blockchain of the same length and with the same number of nodes, but use proof of stake rather than proof of work to decide which node gets to mine a block at each step. Plot the time taken to mine each block, and compare this with the plot from the previous exercise.

# 3.2. Blockchain vulnerabilities

1. As this code exists, there are no checks against an individual spending more than their balance. What would need to change in the code to fix this? (No code necessary)
2. This blockchain does not provide encryption. What would an 'attack' based on the lack of encryption look like? What would need to change to provide encryption? (No code necessary)

# 4. Sample code

See [simulation.py](simulation.py).

# 5. Additional materials

These videos were put together by Alvaro Carril to help students use last year's code. Although a few details have changed, most of what is said is very relevant. These can be a resource if the existing example code and documentation are insufficient.

- Lecture on installation: [video link](https://princeton.zoom.us/rec/share/I1__5keDJzAoVYfEirM7bEnDpNjPLNf39UjZRKUZKD-Df-YkqvmMf8delS3K9X9p.PYAh47XNeIk37Hof?startTime=1633476809000)
- Lecture on interacting with the blockchain API: [video link](https://princeton.zoom.us/rec/share/MizzD2wezrg6DhsX0FCxNYDPgROO-cuV47b_sPBfLA5xOl78jmueRLdZO_9AWkDq.rVKjI1nxkx9X9f7m?startTime=1634577401000)
- Lecture on bulk node initialization: [video link](https://princeton.zoom.us/rec/share/IcwncgJhD7JSt_DwlwI6dqB0WrHqp6UpxoSfKC9p2iBufvenmYDENDoWENkiAqQn.gj58kJ9l5uip7izX)
- Lecture on Wallet class and keeping track of money in the blockchain: [video link](https://princeton.zoom.us/rec/share/U1ku3gC7EbunUtu-qMR_taEEbha1FxVO_1gXckH-LEJqqV6sFyytm849t_fwBZKs.yBZk6hki-HF_Wroy)
- Lecture on simulating transactions: [video link](https://princeton.zoom.us/rec/share/c07Sm4ucX3VTJbL_exEMCPJnIOqaCoNriQMmSga2VJllNnTQ4zS80ffJt6D7pD3t.V8dVboGu-9lRcgLV)

