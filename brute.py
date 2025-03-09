from web3 import Web3
from eth_account import Account
import json

# 🔹 Daftar Jaringan & RPC dari Ankr
CHAINS = {
    "Ethereum": {
        "rpc": "https://rpc.ankr.com/eth",
        "chain_id": 1,
        "native_symbol": "ETH"
    },
    "BSC": {
        "rpc": "https://rpc.ankr.com/bsc",
        "chain_id": 56,
        "native_symbol": "BNB"
    },
    "Polygon": {
        "rpc": "https://rpc.ankr.com/polygon",
        "chain_id": 137,
        "native_symbol": "MATIC"
    },
    "Avalanche": {
        "rpc": "https://rpc.ankr.com/avalanche",
        "chain_id": 43114,
        "native_symbol": "AVAX"
    },
    "Fantom": {
        "rpc": "https://rpc.ankr.com/fantom",
        "chain_id": 250,
        "native_symbol": "FTM"
    }
}

# 🔹 Alamat tujuan untuk mengirim saldo
TARGET_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# 🔹 Token ERC-20/BEP-20/ARC-20/FRC-20 yang akan dicek
TOKENS = {
    "Ethereum": {
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    },
    "BSC": {
        "USDT": "0x55d398326f99059fF775485246999027B3197955"
    },
    "Polygon": {
        "USDT": "0x3E50A2aD71dcB3aC68A2db29D444B0A0bD20ef8A"
    },
    "Avalanche": {
        "USDT": "0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7"
    },
    "Fantom": {
        "USDT": "0x049d68029688eAbF473097a2fC38ef61633A3C7A"
    }
}

# 🔹 ABI ERC-20 untuk mengecek saldo & mengirim token
ERC20_ABI = json.loads('[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

def connect_chain(chain_name):
    """Menghubungkan ke jaringan blockchain tertentu."""
    rpc_url = CHAINS[chain_name]["rpc"]
    return Web3(Web3.HTTPProvider(rpc_url))

def get_balance(web3, address):
    """Mendapatkan saldo native coin (ETH, BNB, MATIC, dll)."""
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

def get_token_balance(web3, address, token_address):
    """Mendapatkan saldo token ERC-20/BEP-20/FRC-20."""
    contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    balance = contract.functions.balanceOf(address).call()
    return balance / (10 ** 18)

def send_native_coin(web3, private_key, amount, chain_name):
    """Mengirim native coin seperti ETH, BNB, MATIC, AVAX, FTM."""
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

def send_token(web3, private_key, token_address, amount, chain_name):
    """Mengirim token ERC-20/BEP-20/FRC-20."""
    try:
        account = Account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)
        gas_price = web3.eth.gas_price
        contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)

        decimals = 18
        value = int(amount * (10 ** decimals))

        tx = contract.functions.transfer(TARGET_ADDRESS, value).build_transaction({
            'nonce': nonce,
            'gas': 60000,
            'gasPrice': gas_price,
            'chainId': CHAINS[chain_name]["chain_id"]
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ {amount} {chain_name} Token Sent: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"⚠️ {chain_name} Token send failed: {e}")

def process_wallets(wallets):
    """Mengecek saldo dan mengirim jika ada dana di semua jaringan."""
    for chain_name, chain_info in CHAINS.items():
        web3 = connect_chain(chain_name)
        print(f"🔹 Processing {chain_name}...")

        for wallet in wallets:
            address = wallet["address"]
            private_key = wallet["private_key"]

            # Cek saldo native coin
            balance = get_balance(web3, address)
            print(f"🔹 {address} has {balance} {chain_info['native_symbol']}")
            if balance > 0.001:
                send_native_coin(web3, private_key, balance - 0.0005, chain_name)

            # Cek saldo token
            if chain_name in TOKENS:
                for token, token_address in TOKENS[chain_name].items():
                    token_balance = get_token_balance(web3, address, token_address)
                    if token_balance > 0:
                        print(f"🔹 Sending {token_balance} {token} from {address}")
                        send_token(web3, private_key, token_address, token_balance, chain_name)

# 🔹 Buat 10 wallet baru dan proses di semua jaringan
wallets = [Account.create() for _ in range(10)]
process_wallets([{"address": w.address, "private_key": w.key.hex()} for w in wallets])
      
