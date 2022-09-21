This subfolder provides code related to homework 2, simulating a centralized transparent ledger.

- [1. Motivation](#1-motivation)
- [2. Exercises](#2-exercises)
  - [2.1. Blockchain simulation](#21-blockchain-simulation)
  - [2.2. Proof of work](#22-proof-of-work)
- [3. Sample code](#3-sample-code)

# 1. Motivation

You've decided to create some digital currency (tokens) for you and your friends to use. You want to create and run a public ledger so that all parties knows how many tokens everyone has. Your friends will send you transactions, and you will keep a record of them in a blockchain. You want this ledger to address the following concerns:
1. A friend could hack into your computer and modify a past transaction in your blockchain
2. A friend could try to spend more tokens than they have
3. A friend could try to spend someone else's tokens

Right now, the provided code in this folder only addresses the first two concerns. Homework 2 is about modifying the code to address concern 3 via encryption.
We recommend using the cryptography package (https://cryptography.io/en/latest/), as it supports a wide range of cryptographic algorithms, is actively supported, and has a wide user base.

Note that this is NOT a decentralized ledger - you and you alone can exclude friends from being able to make payments as you see fit. Later in the class we will investigate how to make a decentralized public ledger.

# 2. Exercises:
For all of the following, you will find the functions in utils.py and example code in simulation.py to be useful. We do not claim that this code is free of bugs. Feel free to change any part of the code in order to complete the exercises. You will be asked to complete a subset of these on homework 2.

## 2.1. Blockchain simulation
1. Suppose you have 2 friends, Alice and Bob. Generate public/private key pairs for each of them. Create a blockchain that starts with you owning 100 tokens and has 5 or more blocks, each with at least 2 transactions between you, Alice, and Bob. Call this your 'sample blockchain.' Call the valid_chain() method and check that this returns True.
2. In what way does this code address concern 1? Provide an example where you modify some block of your sample blockchain and call the valid_chain() method. What happens?
3. In what way does this code address concern 2? Add a large transaction to an additional block of your original sample blockchain, then call the valid_chain() method. What happens?
4. Modify the code to address concern 3 - that is, suppose that your friends send you transactions with a signature. Places that need modification are marked with a TODO comment (see both blockchain.py and utils.py). Re-create your sample blockchain using your modified code. What happens if a friend tries to spend someone else's tokens? Note that you will have to switch between strings and bytes using .encode() and .decode(), as in the example code, since the provided hash algorithm can only accept strings and encryption signatures are bytes.

## 2.2. Proof of work
1. Find a nonce (an integer) so that the hash of str(nonce) + "The quick brown fox jumps over the lazy dog" has at least 5 leading zeros. You will find the hash method of the Blockchain class to be useful. Explain why we can't use an optimization algorithm to find such a nonce.
2. In your sample blockchain, adjust the nonce of each block so that the hash of the block has at least 5 leading zeros. Adjust the "previous_hash" of each block accordingly. You will find the proof_of_work and valid_proof methods of the Blockchain class to be useful. How does this relate to Proof of Work as discussed in class?

# 3. Sample code
See [simulation.py](simulation.py).
