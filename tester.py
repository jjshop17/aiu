from web3 import Web3
from eth_account import Account
import json
import time

# 🔹 Daftar Jaringan EVM & RPC
CHAINS = {
    "Ethereum": {"rpc": "https://rpc.ankr.com/eth", "chain_id": 1, "symbol": "ETH"},
    "BSC": {"rpc": "https://rpc.ankr.com/bsc", "chain_id": 56, "symbol": "BNB"},
}

# 🔹 Daftar Token ERC-20 & BEP-20
TOKENS = {
    "Ethereum": {
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        "UNI": "0xCFFddED873554F362Ac02f8Fb1F02E5Ada10516f",
        "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DdAE9",
        "SHIB": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
        "PEPE": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
    },
    "BSC": {
        "USDT": "0x55d398326f99059fF775485246999027B3197955",
        "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
        "DAI": "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3",
        "BUSD": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
        "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
        "CAKE": "0x0E09FaBB73Bd3Ade0A17ECC321fD13a19e81cE82",
        "DOGE": "0xba2ae424d960c26247dd6c32edc70b295c744c43",
        "BABYDOGE": "0xc748673057861a797275cd8a068abb95a902e8de",
        "FLOKI": "0xfb5b838b6cfeedc2873ab27866079ac55363d37e",
        "PEPE": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
    }
}

# 🔹 Alamat tujuan untuk menerima dana
TARGET_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# 🔹 Fungsi membuat banyak wallet baru
def generate_wallets(n):
    wallets = []
    for _ in range(n):
        account = Account.create()
        wallets.append({"address": account.address, "private_key": account.key.hex()})
    return wallets

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

# 🔹 Cek saldo token ERC-20 & BEP-20
def get_token_balance(web3, token_address, wallet_address):
    try:
        token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=[
            {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}
        ])
        balance = token_contract.functions.balanceOf(wallet_address).call()
        return balance / (10 ** 18)
    except:
        return 0

# 🔹 Cek saldo & simpan hanya yang ada saldonya
def process_wallets(wallets):
    wallets_with_balance = []

    for wallet in wallets:
        print(f"🔍 Checking Wallet: {wallet['address']}")
        has_balance = False
        wallet_data = {"address": wallet["address"], "private_key": wallet["private_key"], "balances": {}}

        for chain in CHAINS.keys():
            web3 = connect_chain(chain)
            balance = get_balance(web3, wallet["address"])
            if balance > 0.01:
                has_balance = True
                wallet_data["balances"][chain] = balance

        for chain, tokens in TOKENS.items():
            web3 = connect_chain(chain)
            for token_name, token_address in tokens.items():
                token_balance = get_token_balance(web3, token_address, wallet["address"])
                if token_balance > 0:
                    has_balance = True
                    wallet_data["balances"][token_name] = token_balance

        if has_balance:
            wallets_with_balance.append(wallet_data)

    with open("wallets_with_balance.json", "w") as f:
        json.dump(wallets_with_balance, f, indent=4)

    print("✅ Wallets with balance saved to wallets_with_balance.json")

# 🔹 Generate 100 Wallet Baru
wallets = generate_wallets(100)

# 🔹 Simpan Wallet ke File JSON
with open("wallets.json", "w") as f:
    json.dump(wallets, f, indent=4)

print("✅ 100 Wallet baru telah dibuat dan disimpan di wallets.json")

# 🔹 Cek saldo & simpan yang ada saldo
time.sleep(2)
process_wallets(wallets)
