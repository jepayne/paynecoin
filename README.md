# `paynecoin` (PYN) <!-- omit in toc -->

This repository contains the code for simulating a blockchain. This is a fictional cryptocurrency and is only for educational purposes.


- [1. Installation](#1-installation)
  - [1.1. Conda](#11-conda)
  - [1.2. Poetry](#12-poetry)
- [2. Running a centralized blockchain](#2-running-a-centralized-blockchain)
  - [2.1. Motivation](#21-motivation)
  - [2.2. Exercises](#22-exercises)
    - [2.2.1. Blockchain simulation](#221-blockchain-simulation)
    - [2.2.2. Proof of work](#222-proof-of-work)
  - [2.3. Sample code](#23-sample-code)
- [3. Running a decentralized blockchain](#3-running-a-decentralized-blockchain)
  - [3.1. Exercises](#31-exercises)
    - [3.1.1. Proof of work versus proof of stake](#311-proof-of-work-versus-proof-of-stake)
    - [3.1.2. Blockchain vulnerabilities](#312-blockchain-vulnerabilities)
  - [3.2. Sample code](#32-sample-code)
- [4. Stablecoins](#4-stablecoins)

# 1. Installation

Simply clone this repository to your machine to install.
For example, you can clone this repository to your home directory by running
```sh
cd ~
git clone git@github.com:jepayne/paynecoin.git # SSH (recommended), or
git clone https://github.com/jepayne/paynecoin.git # HTTPS
```
This will download the `paynecoin` folder to your home directory. This is a python project, so you will also need to have a python executable with the proper dependencies installed.

You will need a working Python 3.5+ installation. I assume you already have one working, but if not, I recommend installing [Anaconda](https://www.anaconda.com/products/individual).

If you already know how to manage your Python environments and packages, you can skip the following subsection. Just make sure you install the dependencies listed in [`pyproject.toml`](pyproject.toml) (i.e., using conda or pip with a virtual environment).

Everything going forward will assume that you are working from a shell where the python executable has the correct dependencies installed (for example, this is the case if you activate the poetry shell as described below, or if you have activated a conda environment that has the appropriate dependencies installed).

## 1.1. Conda

If you have an [Anaconda](https://www.anaconda.com/products/individual) python installation, you can create an environment, activate the environment, install the dependencies listed in [`pyproject.toml`](pyproject.toml), and then you will be able to run everything without a hitch.

## 1.2. Poetry

[Poetry](https://python-poetry.org/) is one way to easily manage packages and environments.
1. Follow the [installation instructions](https://python-poetry.org/docs/#installation) to set Poetry up in your machine. You can verify that the installation was successful by running the following command in a terminal without any errors:
```sh
poetry --version
```
2. Navigate to the local copy of this repository and install the defined dependencies for this project. For example, if you cloned the project to your home directory, run
```sh
cd ~/paynecoin
poetry install
```
3. activate the project's Python virtual environment by spawning a new shell:
```sh
poetry shell
```

# 2. Running a centralized blockchain

## 2.1. Motivation

You've decided to create some digital currency (tokens) for you and your friends to use. You want to create and run a public ledger so that all parties knows how many tokens everyone has. Your friends will send you transactions, and you will keep a record of them in a blockchain. You want this ledger to address the following concerns:
1. A friend could hack into your computer and modify a past transaction in your blockchain
2. A friend could try to spend more tokens than they have
3. A friend could try to spend someone else's tokens

Right now, the provided code in this folder only addresses the first two concerns. Homework 2 is about modifying the code to address concern 3 via encryption.
We recommend using the cryptography package (https://cryptography.io/en/latest/), as it supports a wide range of cryptographic algorithms, is actively supported, and has a wide user base.

Note that this is NOT a decentralized ledger - you and you alone can exclude friends from being able to make payments as you see fit.

## 2.2. Exercises:
For all of the following, you will find the functions in utils.py and example code in simulation_lite.py to be useful. We do not claim that this code is free of bugs. Feel free to change any part of the code in order to complete the exercises. You will be asked to complete a subset of these on homework 2.

### 2.2.1. Blockchain simulation
1. Suppose you have 2 friends, Alice and Bob. Generate public/private key pairs for each of them. Create a blockchain that starts with you owning 100 tokens and has 5 or more blocks, each with at least 2 transactions between you, Alice, and Bob. Call this your 'sample blockchain.' Call the valid_chain() method and check that this returns True.
2. In what way does this code address concern 1? Provide an example where you modify some block of your sample blockchain and call the valid_chain() method. What happens?
3. In what way does this code address concern 2? Add a large transaction to an additional block of your original sample blockchain, then call the valid_chain() method. What happens?
4. Modify the code to address concern 3 - that is, suppose that your friends send you transactions with a signature. Places that need modification are marked with a TODO comment (see both blockchain.py and utils.py). Re-create your sample blockchain using your modified code. What happens if a friend tries to spend someone else's tokens? Note that you will have to switch between strings and bytes using .encode() and .decode(), as in the example code, since the provided hash algorithm can only accept strings and encryption signatures are bytes.

### 2.2.2. Proof of work
1. Find a nonce (an integer) so that the hash of str(nonce) + "The quick brown fox jumps over the lazy dog" has at least 5 leading zeros. You will find the hash method of the Blockchain class to be useful. Explain why we can't use an optimization algorithm to find such a nonce.
2. In your sample blockchain, adjust the nonce of each block so that the hash of the block has at least 5 leading zeros. Adjust the "previous_hash" of each block accordingly. You will find the proof_of_work and valid_proof methods of the Blockchain class to be useful. How does this relate to Proof of Work as discussed in class?

## 2.3. Sample code
See [simulation_lite.py](paynecoin/simulation_lite.py).

# 3. Running a decentralized blockchain

Here, you decide to allow others the opportunity to add transactions to the public ledger.

# 3.1. Exercises

You will be asked to answer a subset of these on homework 3.

# 3.1.1. Proof of work versus proof of stake

1. Simulate proof of work for a blockchain of length at least 100 involving transactions with at least 5 nodes (hint: [simulation_full.py](paynecoin/simulation_full.py) is a great starting point). Plot the time taken to mine each block as well as balances of each individual over time. Also plot the total money supply over time.
2. Simulate another blockchain of the same length and with the same number of nodes, but use proof of stake rather than proof of work to decide which node gets to mine a block at each step. Plot the time taken to mine each block, and compare this with the plot from the previous exercise.

# 3.1.2. Blockchain vulnerabilities

1. As this code exists, there are no checks against an individual spending more than their balance. What would need to change in the code to fix this? (No code necessary)
2. This blockchain does not provide encryption. What would an 'attack' based on the lack of encryption look like? What would need to change to provide encryption? (No code necessary)

## 3.2. Sample code
See [simulation_full.py](simulation_full.py).

# 4. Stablecoins

This is an exercise on stablecoins that may be included on the homework.

Consider a cryptocurrency which initially has a fixed mining reward of \$1.
Throughout this question, use the following specification of money demand. Let real money demand be denoted by
$$
\begin{align*}
    \gamma_t &= A e^{\mu t} e^{-\frac{1}{2}\sigma^2} \epsilon_t,
\end{align*}
$$
where $\log(\epsilon_t)$ is a normally distributed random variable with mean $0$ and variance $\sigma^2$. Under this specification, money demand grows at rate $\mu$ with i.i.d. normal shocks around the mean growth rate. The mean is $\mathbb{E}[\gamma_t] = A e^{\mu t}$. Let money supply be denoted by $M_t$. Then, we have that the price level can be derived from money market clearing,
$$
\begin{align*}
    \gamma_t ={}& \frac{M_t}{P_t} \\
    \implies \quad P_t ={}& \frac{M_t}{\gamma_t}.
\end{align*}
$$
For all simulations consider discrete time with 100 periods.

1. Simulate demand with trend growth and i.i.d. fluctuations (hint: set simple/sensible values for unknown parameters). Simulate money supply (hint: you don't need to simulate blockchain transactions). Compute and plot prices for each period.
2. Can you set a fixed mining reward such that the price is stable in trends? Explain. What is your answer if you can set an arbitrary schedule for reward in each period? Implement and plot a solution that stabilizes price in trend.
3. Suppose that we know the demand shock $\epsilon_t$ one period in advance. Now set a  mining reward schedule to eliminate all volatility in the price, plotting your result. Briefly explain.
4. Suppose that we don't know $\epsilon_t$ in advance but it is mean reverting. To what extent can the price be stabilized? Discuss what can go wrong with this approach.
