from http import client
import os
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountInfo
from xrpl.utils import drops_to_xrp, xrp_to_drops
from xrpl import XRPLException
from xrpl.models.transactions import Payment, Transaction
from xrpl.transaction import submit_and_wait

from dotenv import load_dotenv


load_dotenv()
client = JsonRpcClient(os.environ.get("TESTNET_URL"))
URL = os.environ.get("TESTNET_URL")
adress_1 = os.environ.get("wallet_1")
adress_2 = os.environ.get("wallet_2")
adress_3 = os.environ.get("wallet_3")


# This string is a seed
seed_1 = os.environ.get("SEED_PHRASE_1")
seed_2 = os.environ.get("SEED_PHRASE_2")
seed_3 = os.environ.get("SEED_PHRASE_3")

# Create the wallet from the seed
wallet_1 = Wallet.from_seed(seed_1)
wallet_2 = Wallet.from_seed(seed_2)
wallet_3 = Wallet.from_seed(seed_3)



WALLETS = [wallet_1, wallet_2, wallet_3]
print("Loaded Wallets from .env:")
print("-------------------------")

account_info_wallet_1 = client.request(AccountInfo(account=adress_1))
account_info_wallet_2 = client.request(AccountInfo(account=adress_2))
account_info_wallet_3 = client.request(AccountInfo(account=adress_3))


print(account_info_wallet_1)
print("-------------------------")
print(account_info_wallet_2)
print("-------------------------")
print(account_info_wallet_3)
print("-------------------------")
print(f"Wallet 1 Address: {wallet_1}, Balance: {drops_to_xrp(account_info_wallet_1.result['account_data']['Balance'])} XRP")
print(f"Wallet 2 Address: {wallet_2}, Balance: {drops_to_xrp(account_info_wallet_2.result['account_data']['Balance'])} XRP")
print(f"Wallet 3 Address: {wallet_3}, Balance: {drops_to_xrp(account_info_wallet_3.result['account_data']['Balance'])} XRP")

payment_amount = 1
payment_amount = xrp_to_drops(payment_amount) 

payment_tx = Payment(
    account=wallet_1.classic_address,
    destination=wallet_2.classic_address,
    amount=payment_amount
)

print("Prepared Payment Transaction:")
print(payment_tx)   
print("-------------------------")
print("Payment Transaction is valid.")
response = submit_and_wait(transaction=payment_tx, client=client,wallet=wallet_1) 
print("Payment Transaction Response:")
print(response)
print("-------------------------")
print(response.result)