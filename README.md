# EthWalletMoneyGenerator

This Python script generates Ethereum wallet addresses along with their corresponding mnemonic phrases and private keys. It utilizes randomization techniques to ensure security and uniqueness. Additionally, it checks whether the generated addresses already exist in a SQLite database and logs the results.

## Prerequisites
- Python 3.x
- Required Python libraries: `sqlite3`, `ecdsa`, `hashlib`, `bip32utils`, `colorama`

## Setup
1. Install the required Python libraries using pip:
`pip install sqlite3 ecdsa bip32utils colorama` 
2. Ensure you have a SQLite database set up to store addresses.
3. Customize the script as necessary, modifying database paths and result file names.

## Usage
1. Run the script using Python:
`python wallet_address_generator.py`
2. The script will continuously generate Ethereum wallet addresses, check their existence in the database, and log the results in a specified file (`result.txt` by default).

## How it Works
- The script generates a mnemonic phrase, which is a human-readable representation of a random sequence of bytes.
- From the mnemonic phrase, it derives a seed, which is used to generate a hierarchical deterministic (HD) wallet.
- The HD wallet is traversed to obtain a private key and corresponding Ethereum wallet address.
- The address is checked against the database to ensure uniqueness.
- Results are logged in a file for further analysis.

## Disclaimer
YOU MUST HAVE YOUR DB

This script is intended for educational purposes only. Use it responsibly and at your own risk.


