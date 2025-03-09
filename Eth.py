from web3 import Web3
import secrets
import time

# Koneksi ke Ankr Ethereum Mainnet RPC
ANKR_RPC_URL = "https://rpc.ankr.com/eth"
web3 = Web3(Web3.HTTPProvider(ANKR_RPC_URL))

# Fungsi untuk membuat wallet baru
def generate_wallet():
    private_key = "0x" + secrets.token_hex(32)  # Generate private key
    acct = web3.eth.account.from_key(private_key)  # Buat akun dari private key
    return acct.address, private_key

# Fungsi untuk cek saldo ETH
def check_balance(address):
    balance_wei = web3.eth.get_balance(address)  # Ambil saldo dalam Wei
    balance_eth = web3.from_wei(balance_wei, 'ether')  # Konversi ke ETH
    return balance_eth

# Looping untuk mencari wallet dengan saldo
wallet_found = False
wallet_count = 0

while not wallet_found:
    wallet_count += 1
    address, private_key = generate_wallet()
    balance = check_balance(address)
    
    print(f"[{wallet_count}] Address: {address} | Saldo: {balance} ETH")
    
    if balance > 0:
        wallet_found = True
        print("\n🎉 Wallet dengan saldo ditemukan!")
        print(f"✅ Address: {address}")
        print(f"🔑 Private Key: {private_key}")
        print(f"💰 Saldo: {balance} ETH")
        break
    
    time.sleep(1)  # Beri jeda 1 detik agar tidak terlalu banyak request ke Ankr

print("\n✅ Skrip selesai.")
