import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from web3 import Web3

# Inisialisasi Web3 (Testnet Monad)
web3 = Web3(Web3.HTTPProvider("https://monad-testnet.rpc-url"))
private_key = "PRIVATE_KEY_ANDA"
account = web3.eth.account.from_key(private_key)
wallet_address = account.address

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def visit_and_interact(url, interactions):
    driver.get(url)
    time.sleep(5)  # Tunggu halaman dimuat
    for action in interactions:
        elem = driver.find_element(By.XPATH, action["xpath"])
        if action["action"] == "click":
            elem.click()
        elif action["action"] == "send_keys":
            elem.send_keys(action["value"])
        time.sleep(2)

def stake_mon(amount):
    staking_contract_address = "0xSTAKING_CONTRACT_ADDRESS"
    staking_abi = [...]  # Gantilah dengan ABI kontrak staking
    contract = web3.eth.contract(address=staking_contract_address, abi=staking_abi)
    
    amount_wei = web3.to_wei(amount, 'ether')
    tx = contract.functions.stake(amount_wei).build_transaction({
        'from': wallet_address,
        'gas': 200000,
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Staking Transaction Hash:", web3.to_hex(tx_hash))

# Task 1: AICraft - Join Whitelist
def aicraft_task():
    visit_and_interact(
        "https://aicraft.fun/",
        [
            {"xpath": "//button[contains(text(), 'Join Whitelist')]", "action": "click"},
            {"xpath": "//input[@placeholder='Enter Monad Address']", "action": "send_keys", "value": wallet_address},
            {"xpath": "//a[contains(@href, 'fizen')]", "action": "click"},
        ]
    )

# Task 2: Ambient - Swap MON > USDC > WETH
def ambient_task():
    visit_and_interact(
        "https://monad.ambient.finance/",
        [
            {"xpath": "//input[@type='number']", "action": "send_keys", "value": "1"},
            {"xpath": "//button[contains(text(), 'Swap')]","action": "click"},
        ]
    )

# Task 3: Apriori - Claim Faucet & Stake
def apriori_task():
    visit_and_interact(
        "https://stake.apr.io/",
        [
            {"xpath": "//button[contains(text(), 'Claim Faucet')]", "action": "click"},
            {"xpath": "//input[@type='number']", "action": "send_keys", "value": "0.2"},
            {"xpath": "//button[contains(text(), 'Stake')]", "action": "click"},
        ]
    )
    stake_mon(0.2)  # Staking 0.2 MON

# Task 4: Bean - Swap and Add Liquidity
def bean_task():
    visit_and_interact(
        "https://perp.bean.exchange/#/trade",
        [
            {"xpath": "//input[@type='number']", "action": "send_keys", "value": "1"},
            {"xpath": "//button[contains(text(), 'Swap')]", "action": "click"},
            {"xpath": "//button[contains(text(), 'Add Liquidity')]", "action": "click"},
        ]
    )

# Task 5: Bima - Claim Faucet and Deposit Vault
def bima_task():
    visit_and_interact(
        "https://bima.money/vaults",
        [
            {"xpath": "//button[contains(text(), 'Claim Faucet')]", "action": "click"},
            {"xpath": "//input[@placeholder='Deposit Amount']", "action": "send_keys", "value": "0.2"},
            {"xpath": "//button[contains(text(), 'Deposit Vault')]", "action": "click"},
        ]
    )

# Task 6: Blazpay - Swap and Add Liquidity
def blazpay_task():
    visit_and_interact(
        "https://www.defi.blazpay.com/",
        [
            {"xpath": "//button[contains(text(), 'Swap')]", "action": "click"},
            {"xpath": "//button[contains(text(), 'Add Liquidity')]", "action": "click"},
        ]
    )

# Task 7: Caddy - Join Whitelist
def caddy_task():
    visit_and_interact(
        "https://caddy.finance/",
        [
            {"xpath": "//button[contains(text(), 'Join Whitelist')]", "action": "click"},
        ]
    )

# Task 8: Curvance - Claim Faucet and Deposit
def curvance_task():
    visit_and_interact(
        "https://monad.curvance.com/monad",
        [
            {"xpath": "//button[contains(text(), 'Claim All Faucet')]", "action": "click"},
            {"xpath": "//button[contains(text(), 'Get CVE')]", "action": "click"},
            {"xpath": "//button[contains(text(), 'Deposit')]", "action": "click"},
        ]
    )

# Schedule Tasks
def schedule_tasks():
    schedule.every().day.at("10:00").do(aicraft_task)
    schedule.every().day.at("10:30").do(ambient_task)
    schedule.every().day.at("11:00").do(apriori_task)
    schedule.every().day.at("11:30").do(bean_task)
    schedule.every().day.at("12:00").do(bima_task)
    schedule.every().day.at("12:30").do(blazpay_task)
    schedule.every().day.at("13:00").do(caddy_task)
    schedule.every().day.at("13:30").do(curvance_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start Task Scheduler
schedule_tasks()
