from web3 import Web3
from eth_account import Account
import json
import time

# 🔹 Daftar Jaringan EVM & RPC
CHAINS = {
    "Ethereum": {"rpc": "https://rpc.ankr.com/eth", "chain_id": 1, "symbol": "ETH"},
    "BSC": {"rpc": "https://rpc.ankr.com/bsc", "chain_id": 56, "symbol": "BNB"},
    "Polygon": {"rpc": "https://rpc.ankr.com/polygon", "chain_id": 137, "symbol": "MATIC"},
    "Avalanche": {"rpc": "https://rpc.ankr.com/avalanche", "chain_id": 43114, "symbol": "AVAX"},
    "Fantom": {"rpc": "https://rpc.ankr.com/fantom", "chain_id": 250, "symbol": "FTM"},
    "Arbitrum": {"rpc": "https://rpc.ankr.com/arbitrum", "chain_id": 42161, "symbol": "ETH"},
    "Optimism": {"rpc": "https://rpc.ankr.com/optimism", "chain_id": 10, "symbol": "ETH"},
    "Base": {"rpc": "https://mainnet.base.org", "chain_id": 8453, "symbol": "ETH"},
}

# 🔹 Daftar Token ERC-20 & BEP-20 di berbagai jaringan
TOKENS = {
    "Ethereum": {
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        "SHIB": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
    },
    "BSC": {
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
        "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "DAI": "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
        "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
        "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "DOGE": "0xba2ae424d960c26247dd6c32edc70b295c744c43",
        "FLOKI": "0xfb5b838b6cfeedc2873ab27866079ac55363d37e",
    },
    "Polygon": {
        "USDT": "0x9fB83c0635De2E815fd1c21b3a292277540C2e8d",
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        "WMATIC": "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0",
    },
    "Avalanche": {
        "USDT": "0xc7198437980c041c805A1EDcbA50c1Ce5db95118",
        "USDC": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
        "DAI": "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70",
        "WAVAX": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
    },
    "Fantom": {
        "USDT": "0x049d68029688eAbF473097a2fC38ef61633A3C7A",
        "USDC": "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",
        "DAI": "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E",
        "WFTM": "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83",
    },
}

# 🔹 Alamat tujuan untuk menerima dana
TARGET_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# 🔹 Koneksi ke blockchain
def connect_chain(chain_name):
    return Web3(Web3.HTTPProvider(CHAINS[chain_name]["rpc"]))

# 🔹 Cek saldo native coin
def get_balance(web3, address):
    try:
        balance = web3.eth.get_balance(address)
        return web3.from_wei(balance, 'ether')
    except:
        return 0

# 🔹 Cek saldo token ERC-20
def get_token_balance(web3, token_address, wallet_address):
    try:
        token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=[
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf",
             "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}
        ])
        balance = token_contract.functions.balanceOf(wallet_address).call()
        return balance / (10 ** 18)
    except:
        return 0

# 🔹 Simpan wallet yang memiliki saldo
def save_wallet(wallet_data):
    try:
        with open("wallets_with_balance.json", "r") as f:
            wallets = json.load(f)
    except:
        wallets = []

    wallets.append(wallet_data)

    with open("wallets_with_balance.json", "w") as f:
        json.dump(wallets, f, indent=4)

# 🔹 Buat 20 wallet & cek saldo langsung
for i in range(20):
    account = Account.create()
    wallet = {"address": account.address, "private_key": account.key.hex(), "balances": {}}
    print(f"🔹 Wallet {i+1} Created: {wallet['address']}")

    has_balance = False

    # Cek saldo native di semua jaringan
    for chain in CHAINS.keys():
        web3 = connect_chain(chain)
        balance = get_balance(web3, wallet["address"])
        if balance > 0.01:
            has_balance = True
            wallet["balances"][chain] = balance

    # Cek saldo token di semua jaringan
    for chain, tokens in TOKENS.items():
        web3 = connect_chain(chain)
        for token_name, token_address in tokens.items():
            token_balance = get_token_balance(web3, token_address, wallet["address"])
            if token_balance > 0:
                has_balance = True
                wallet["balances"][token_name] = token_balance

    # Simpan hanya jika ada saldo
    if has_balance:
        save_wallet(wallet)
        print(f"✅ Wallet {i+1} has balance, saved!")
    else:
        print(f"❌ Wallet {i+1} is empty, discarded.")
