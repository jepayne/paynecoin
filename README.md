# `paynecoin` (PYN) <!-- omit in toc -->

This repository contains the code for running 2 toy blockchains that allows you to record transactions. One is `paynecoin-lite`, a local private ledger, and the other is `paynecoin-full`, a decentralized distributed ledger. Both are made-up cryptocurrencies and are only for educational purposes.

#### Note

All instructions in this repository assume you have access to a Unix machine (macOS or Linux).

- [1. Installation](#1-installation)
  - [1.1. Poetry](#11-poetry)
  - [1.2. Windows Support](#12-windows-support)
- [2. Running the paynecoin-lite blockchain](#2-running-paynecoin-lite)
- [3. Running the paynecoin-full blockchain](#3-running-paynecoin-full)

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

Everything going forward will assume that you are working from a shell where the python executable has the correct dependencies installed (this is the case if you activate the poetry shell as described below).

## 1.1. Poetry

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

## 1.2. Windows support

Forthcoming

# 2. Running paynecoin-lite

Look at the [paynecoin-lite readme](/paynecoin-lite/README.md) for motivation, homework 2 questions, and example code.

For a very quick start, navigate to the paynecoin-lite subfolder (e.g. `cd ~/paynecoin/paynecoin-lite`) and run the following in your (poetry) shell:
```sh
python simulation.py
```

# 3. Running paynecoin-full

Look at the [paynecoin-full readme](/paynecoin-full/README.md) for motivation, homework 3 questions, and example code.

For a very quick start, navigate to the paynecoin-full subfolder (e.g. `cd ~/paynecoin/paynecoin-full`) and run the following in your (poetry) shell:
```sh
bash paynecoin_nodes.sh init 5
python simulation.py
bash paynecoin_nodes.sh kill
```
