import os
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountInfo
from xrpl.utils import drops_to_xrp
from xrpl import XRPLException

from dotenv import load_dotenv


load_dotenv()

seed_1 = os.environ.get("SEED_PHRASE_1")
seed_2 = os.environ.get("SEED_PHRASE_2")
seed_3 = os.environ.get("SEED_PHRASE_3")
URL = os.environ.get("TESTNET_URL")

SEED_PHRASES = [
    os.environ.get("SEED_PHRASE_1"),
    os.environ.get("SEED_PHRASE_2"),
    os.environ.get("SEED_PHRASE_3"),
]


wallet_1 = generate_faucet_wallet(JsonRpcClient(URL))
wallet_2 = generate_faucet_wallet(JsonRpcClient(URL))
wallet_3 = generate_faucet_wallet(JsonRpcClient(URL))

WALLETS = [wallet_1, wallet_2, wallet_3]


print("Generated Wallets:")
print("-------------------")
print(f"Wallet 1 Address: {wallet_1.classic_address}, Seed: {wallet_1.seed}")
print(f"Wallet 2 Address: {wallet_2.classic_address}, Seed: {wallet_2.seed}")
print(f"Wallet 3 Address: {wallet_3.classic_address}, Seed: {wallet_3.seed}")


print(WALLETS)