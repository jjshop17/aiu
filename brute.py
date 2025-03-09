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

# 🔹 Daftar Token ERC-20/BEP-20/ARC-20/FRC-20
TOKENS = {
    "Ethereum": {
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    },
    "BSC": {
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
        "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "DAI": "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
        "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
        "WBNB": "0xbb4CdB9Cbd36B01bD1cBaEBF2De08d9173bc095c"
    },
    "Polygon": {
        "USDT": "0x3E50A2aD71dcB3aC68A2db29D444B0A0bD20ef8A",
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        "WMATIC": "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0"
    },
    "Avalanche": {
        "USDT": "0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7",
        "USDC": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
        "DAI": "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70",
        "WAVAX": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"
    },
    "Fantom": {
        "USDT": "0x049d68029688eAbF473097a2fC38ef61633A3C7A",
        "USDC": "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",
        "DAI": "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E",
        "WFTM": "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83"
    }
}

# 🔹 ABI ERC-20
ERC20_ABI = json.loads('[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

def connect_chain(chain_name):
    return Web3(Web3.HTTPProvider(CHAINS[chain_name]["rpc"]))

def get_balance(web3, address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

def get_token_balance(web3, address, token_address):
    contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    balance = contract.functions.balanceOf(address).call()
    return balance / (10 ** 18)

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

def send_token(web3, private_key, token_address, amount, chain_name):
    try:
        account = Account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)
        gas_price = web3.eth.gas_price
        contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
        value = int(amount * (10 ** 18))

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

# 🔹 Jalankan untuk 10 wallet
wallets = [Account.create() for _ in range(10)]
process_wallets([{"address": w.address, "private_key": w.key.hex()} for w in wallets])
