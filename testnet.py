import requests

# Alamat wallet tujuan
WALLET_ADDRESS = "0x25fa9C6d6bc937d415aD2Bc13F0ca2c01F6E1037"

# URL Faucet Alchemy (Gunakan API dari Alchemy)
FAUCET_URL = "https://faucet.alchemy.com/api/faucet"

# Data untuk permintaan faucet
data = {
    "recipient": WALLET_ADDRESS
}

headers = {
    "Content-Type": "application/json"
}

# Kirim permintaan ke faucet
response = requests.post(FAUCET_URL, json=data, headers=headers)

if response.status_code == 200:
    print(f"✅ Berhasil mengajukan permintaan faucet! Cek wallet {WALLET_ADDRESS} dalam beberapa menit.")
else:
    print(f"❌ Gagal mendapatkan ETH Sepolia: {response.text}")
  
