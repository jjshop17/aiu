from web3 import Web3
import secrets

# Koneksi ke Ankr Ethereum Mainnet RPC
ANKR_RPC_URL = "https://rpc.ankr.com/eth"
web3 = Web3(Web3.HTTPProvider(ANKR_RPC_URL))

# Fungsi untuk membuat wallet baru
def generate_wallet():
    private_key = "0x" + secrets.token_hex(32)  # Generate private key
    acct = web3.eth.account.from_key(private_key)  # Buat akun dari private key
    print(f"✅ Address: {acct.address}")
    print(f"🔑 Private Key: {private_key}")
    return acct.address, private_key

# Fungsi untuk cek saldo
def check_balance(address):
    balance_wei = web3.eth.get_balance(address)
    balance_eth = web3.from_wei(balance_wei, 'ether')
    print(f"💰 Saldo {address}: {balance_eth} ETH")
    return balance_eth

# Jalankan skrip
address, private_key = generate_wallet()
check_balance(address)
