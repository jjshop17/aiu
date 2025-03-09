import requests
from web3 import Web3

# Konfigurasi Ankr RPC
ANKR_RPC_URL = "https://rpc.ankr.com/eth"
web3 = Web3(Web3.HTTPProvider(ANKR_RPC_URL))

# Fungsi untuk generate wallet dari vanity-eth.tk
def generate_wallet():
    url = "https://vanity-eth.tk/generate"
    response = requests.get(url)

    if response.status_code == 200:
        wallet = response.json()
        print(f"Address: {wallet['address']}")
        print(f"Private Key: {wallet['private']}")
        return wallet
    else:
        print("Gagal membuat wallet!")
        return None

# Fungsi untuk cek saldo ETH menggunakan Ankr
def check_balance_ankr(address):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    response = requests.post(ANKR_RPC_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        balance_wei = int(data["result"], 16)
        balance_eth = Web3.from_wei(balance_wei, 'ether')
        print(f"Saldo: {balance_eth} ETH")
        return balance_eth
    else:
        print("Gagal mengambil saldo!")
        return None

# Eksekusi
wallet = generate_wallet()
if wallet:
    check_balance_ankr(wallet["address"])
  
