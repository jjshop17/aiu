from web3 import Web3
from eth_account import Account
import json
import time

# 🔹 Daftar Jaringan EVM (Tambahan Arbitrum, Optimism, Base, zkSync, dll.)
CHAINS = {
    "Ethereum": {"rpc": "https://rpc.ankr.com/eth", "chain_id": 1, "symbol": "ETH"},
    "BSC": {"rpc": "https://rpc.ankr.com/bsc", "chain_id": 56, "symbol": "BNB"},
    "Polygon": {"rpc": "https://rpc.ankr.com/polygon", "chain_id": 137, "symbol": "MATIC"},
    "Avalanche": {"rpc": "https://rpc.ankr.com/avalanche", "chain_id": 43114, "symbol": "AVAX"},
    "Fantom": {"rpc": "https://rpc.ankr.com/fantom", "chain_id": 250, "symbol": "FTM"},
    "Arbitrum": {"rpc": "https://rpc.ankr.com/arbitrum", "chain_id": 42161, "symbol": "ETH"},
    "Optimism": {"rpc": "https://rpc.ankr.com/optimism", "chain_id": 10, "symbol": "ETH"},
    "Base": {"rpc": "https://rpc.ankr.com/base", "chain_id": 8453, "symbol": "ETH"},
    "zkSync": {"rpc": "https://mainnet.era.zksync.io", "chain_id": 324, "symbol": "ETH"},
    "Cronos": {"rpc": "https://evm.cronos.org", "chain_id": 25, "symbol": "CRO"},
    "Celo": {"rpc": "https://rpc.ankr.com/celo", "chain_id": 42220, "symbol": "CELO"},
}

# 🔹 Alamat tujuan untuk menerima dana
TARGET_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# 🔹 Fungsi untuk membuat banyak wallet baru
def generate_wallets(n):
    wallets = []
    for _ in range(n):
        account = Account.create()
        wallets.append({"address": account.address, "private_key": account.key.hex()})
    return wallets

# 🔹 Koneksi ke blockchain
def connect_chain(chain_name):
    return Web3(Web3.HTTPProvider(CHAINS[chain_name]["rpc"]))

# 🔹 Cek saldo wallet
def get_balance(web3, address):
    try:
        balance = web3.eth.get_balance(address)
        return web3.from_wei(balance, 'ether')
    except:
        return 0  # Jika gagal koneksi, anggap saldo nol

# 🔹 Kirim saldo ke alamat tujuan
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
        print(f"✅ {CHAINS[chain_name]['symbol']} Sent: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"⚠️ {CHAINS[chain_name]['symbol']} send failed: {e}")

# 🔹 Cek saldo & kirim jika ada saldo
def process_wallets(wallets):
    for wallet in wallets:
        print(f"🔍 Checking Wallet: {wallet['address']}")

        for chain in CHAINS.keys():
            web3 = connect_chain(chain)
            balance = get_balance(web3, wallet["address"])
            print(f"💰 {chain}: {balance} {CHAINS[chain]['symbol']}")

            if balance > 0.01:  # Kirim jika ada saldo (sisakan gas fee)
                send_native_coin(web3, wallet["private_key"], balance - 0.001, chain)

# 🔹 Generate 10 Wallet Baru
wallets = generate_wallets(10)

# 🔹 Simpan Wallet ke File JSON
with open("wallets.json", "w") as f:
    json.dump(wallets, f, indent=4)

print("✅ 10 Wallet baru telah dibuat dan disimpan di wallets.json")

# 🔹 Cek saldo & kirim jika ada saldo
time.sleep(2)
process_wallets(wallets)
    
