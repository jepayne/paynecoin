# `paynecoin` (PYN) <!-- omit in toc -->

This repository contains the code for running 2 toy blockchains that allows you to record transactions. One is `paynecoin-lite`, a local private ledger, and the other is `paynecoin-full`, a decentralized distributed ledger. Both are made-up cryptocurrencies and are only for educational purposes.

#### Note

All instructions in this repository assume you have access to a Unix machine (macOS or Linux). See [this section](#12-windows-support) if you only have access to a machine with Windows.

- [1. Installation](#1-installation)
  - [1.1. Conda](#11-conda)
  - [1.2. Poetry](#12-poetry)
  - [1.3. Windows Support](#13-windows-support)
    - [1.3.1. Windows Subsystem for Linux](#131-windows-subsystem-for-linux)
    - [1.3.2. Cygwin](#132-cygwin)
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

## 1.3. Windows support

From Windows, everything except the utilities provided by [paynecoin-full/paynecoin_nodes.sh](paynecoin-full/paynecoin_nodes.sh) will work as normal. You can still initialize blockchain nodes manually on Windows (as on Unix systems) by running [paynecoin-full/api.py](paynecoin-full/api.py) with the appropriate command line arguments. Look at [paynecoin-full/README.md](paynecoin-full/README.md) for more details on initializing blockchain nodes.

### 1.3.1. Windows Subsystem for Linux

If you have a Windows machine, one elegant way to run all the code from this repository is to install the [Windows Subsystem for Linux](https://ubuntu.com/wsl) (WSL). This will give you a Unix terminal that has access to files on your Windows machine. You can then install a python executable in the WSL (for example, using the `wget` command to download the Anaconda installation script) and proceed as if you were using Unix. If you are committed to using Windows and plan to do a lot of software development, this is a good tool to be familiar with.

### 1.3.2 Cygwin

Another option is to use [Cygwin](https://www.cygwin.com/). If you choose to go this route, you will need to do the following:

1. Run `sed -i 's/\r//' paynecoin_nodes.sh` from cygwin to change the format of the script. Then, bulk initialization of nodes will work as described elsewhere.
2. Running `ps -W | grep payne | awk '{print $1}' | while read line; do echo $line | xargs kill -f; done;` will kill nodes in bulk (usually, sometimes this is buggy)
3. `netstat -ano | findstr :<port_number>` (find the PIDs of the processes using these ports) and
`taskkill /PID <pid> -f` (kill the processes once you have the PIDs) will work to kill nodes individually.

# 2. Running paynecoin-lite

Look at the [paynecoin-lite readme](/paynecoin-lite/README.md) for motivation, possible homework 2 questions, and example code.

For a very quick start, navigate to the paynecoin-lite subfolder (e.g. `cd ~/paynecoin/paynecoin-lite`) and run the following in your (poetry) shell:
```sh
python simulation.py
```

# 3. Running paynecoin-full

Look at the [paynecoin-full readme](/paynecoin-full/README.md) for motivation, possible homework 3 questions, and example code.

For a very quick start, navigate to the paynecoin-full subfolder (e.g. `cd ~/paynecoin/paynecoin-full`) and run the following in your (poetry) shell:
```sh
bash paynecoin_nodes.sh init 5
python simulation.py
bash paynecoin_nodes.sh kill
```
