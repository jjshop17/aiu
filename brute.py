import json
import time
import random
from web3 import Web3
from eth_account import Account
import requests

# Konfigurasi
ANKR_RPC = {
    "ethereum": "https://rpc.ankr.com/eth",
    "bsc": "https://rpc.ankr.com/bsc",
    "polygon": "https://rpc.ankr.com/polygon",
    "avalanche": "https://rpc.ankr.com/avalanche",
    "fantom": "https://rpc.ankr.com/fantom"
}

STABLECOINS = {
    "USDT": {
        "ethereum": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "bsc": "0x55d398326f99059fF775485246999027B3197955",
        "polygon": "0x3813e82e6f7098b9583FC0F33a962D02018B6803",
        "avalanche": "0x9702230A8eF020A4209e3aB990DC11dD3F1E0e1E",
        "fantom": "0x049d68029688eAbF473097a2fC38ef61633A3C7A"
    },
    "USDC": {
        "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "bsc": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "polygon": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "avalanche": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
        "fantom": "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75"
    },
    "DAI": {
        "ethereum": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "bsc": "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
        "polygon": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        "avalanche": "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70",
        "fantom": "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E"
    }
}

ALAMAT_TUJUAN = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# Fungsi untuk membuat wallet baru
def buat_wallet():
    account = Account.create()
    return account.address, account.key.hex()

# Fungsi untuk mendapatkan saldo ETH/BNB/MATIC/AVAX/FTM
def get_native_balance(w3, address):
    return w3.eth.get_balance(address) / (10 ** 18)

# Fungsi untuk mendapatkan saldo token ERC-20
def get_token_balance(w3, token_address, wallet_address):
    abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
    token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=json.loads(abi))
    balance = token_contract.functions.balanceOf(wallet_address).call()
    return balance / (10 ** 18)

# Fungsi untuk mengirim dana jika ada saldo
def kirim_dana(w3, private_key, amount, token_address=None):
    account = Account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)

    if token_address:
        abi = '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
        token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=json.loads(abi))
        tx = token_contract.functions.transfer(ALAMAT_TUJUAN, int(amount * (10 ** 18))).build_transaction({
            'from': account.address,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce
        })
    else:
        tx = {
            'nonce': nonce,
            'to': ALAMAT_TUJUAN,
            'value': int(amount * (10 ** 18)),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price
        }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)

# Buat banyak wallet
wallets = [buat_wallet() for _ in range(5)]  # Bisa ubah jumlah wallet

# Cek saldo dan transfer jika ada
for chain, rpc in ANKR_RPC.items():
    w3 = Web3(Web3.HTTPProvider(rpc))

    for address, private_key in wallets:
        print(f"\n[+] Cek saldo di {chain} untuk {address}")

        # Cek saldo native (ETH, BNB, MATIC, AVAX, FTM)
        saldo_native = get_native_balance(w3, address)
        print(f"   - Native: {saldo_native} {chain.upper()}")

        if saldo_native > 0.01:  # Jika ada saldo, kirim
            tx_hash = kirim_dana(w3, private_key, saldo_native - 0.005)  # Sisakan fee
            print(f"   - Dikirim! TX: {tx_hash}")

        # Cek saldo token stablecoin
        for token, addrs in STABLECOINS.items():
            if chain in addrs:
                saldo_token = get_token_balance(w3, addrs[chain], address)
                print(f"   - {token}: {saldo_token}")

                if saldo_token > 0:
                    tx_hash = kirim_dana(w3, private_key, saldo_token, addrs[chain])
                    print(f"   - {token} dikirim! TX: {tx_hash}")

        time.sleep(random.randint(1, 3))  # Anti-spam RPC

print("\nSelesai!")
        
