from web3 import Web3
from eth_account import Account

# ============================================================
# 1. Connect to Flare Coston2 Testnet
# ============================================================

RPC_URL = "https://coston2-api.flare.network/ext/C/rpc"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    print("❌ Failed to connect to Flare Coston2")
    exit()
print("✔ Connected to Flare Coston2 Testnet\n")

# ============================================================
# 2. Generate a new wallet
# ============================================================

acct = Account.create()
my_address = acct.address
my_private_key = acct.key.hex()

print("=== NEW WALLET GENERATED ===")
print(f"Address:     {my_address}")
print(f"Private Key: {my_private_key}  (SAVE THIS!)\n")

# ============================================================
# 3. Function to check balance
# ============================================================
# NOTE : Faucet available at https://faucet.flare.network
def get_balance(address):
    balance_wei = web3.eth.get_balance(address)
    return web3.from_wei(balance_wei, "ether")

# ============================================================
# 4. Check balance of the new wallet
# ============================================================

print("=== BALANCE OF NEW WALLET ===")
my_balance = get_balance(my_address)
print(f"{my_address} → {my_balance} C2FLR (should be 0 until faucet)\n")

# ============================================================
# 5. Check balance of a random address
# ============================================================

random_address = "0xc1250F0A96A075f93231cED19E572a15894562ed"

print("=== BALANCE OF RANDOM ADDRESS ===")
random_balance = get_balance(random_address)
print(f"{random_address} → {random_balance} C2FLR\n")

# ============================================================
# 6. (Optional) Example: Send a transaction
# ============================================================
# NOTE: Uncomment this only after funding the wallet with C2FLR
#       from https://faucet.flare.network

"""
tx = {
    "to": "0xAnotherAddressHere",
    "value": web3.to_wei(0.001, "ether"),
    "gas": 21000,
    "gasPrice": web3.to_wei("25", "gwei"),
    "nonce": web3.eth.get_transaction_count(my_address),
}

signed = web3.eth.account.sign_transaction(tx, my_private_key)
tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
print(f"Transaction sent! Hash: {tx_hash.hex()}")
"""
# ============================================================

print("Done.")
