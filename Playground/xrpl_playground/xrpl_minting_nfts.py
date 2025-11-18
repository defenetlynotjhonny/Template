import json
import os
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from xrpl.models.transactions import NFTokenMint
from xrpl.utils import get_nftoken_id, str_to_hex
from dotenv import load_dotenv


load_dotenv()
# 1. --- Connect to the Testnet Client ---
# We'll use the public Testnet server.
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# 2. --- Set Up Your Minter Wallet ---
#    !!! PASTE YOUR TESTNET SEED HERE !!!
#    (The one starting with 's...')
MINTER_WALLET_SEED = os.environ.get("SEED_PHRASE_1")


minter_wallet = Wallet.from_seed(seed=MINTER_WALLET_SEED)
print(f"nUsing Minter Wallet: {minter_wallet.classic_address}")

# 3. --- Define NFT Parameters ---
# This is the placeholder link for testing.
metadata_uri = "https://my-testnet-placeholder.com/nft/1"

# Convert the URI to hex for the transaction
metadata_uri_hex = str_to_hex(metadata_uri)
print(f"Using Placeholder URI: {metadata_uri}")

# This is an arbitrary number for your "collection".
# You can set it to 0 if you don't have one.
collection_taxon = 1

# 4. --- Construct the NFTokenMint Transaction ---
print(f"Preparing to mint NFT for collection taxon {collection_taxon}...")

nft_mint_tx = NFTokenMint(
    account=minter_wallet.classic_address,
    uri=metadata_uri_hex,
    nftoken_taxon=collection_taxon
)

# 5. --- Sign, Submit, and Wait for Validation ---
print("nSubmitting NFTokenMint transaction and waiting for validation...")

try:
    response = submit_and_wait(nft_mint_tx, client, minter_wallet)
    
    # 6. --- Check Result and Get NFTokenID ---
    # Check the final transaction result code
    result_code = response.result["meta"]["TransactionResult"]
    
    if result_code == "tesSUCCESS":
        print("n--- MINT SUCCESSFUL! ---")
        
        # Helper function to find the NFTokenID in the transaction metadata
        nft_id = get_nftoken_id(response.result["meta"])
        print(f"nYour new NFTokenID is:n{nft_id}")
        
    else:
        print(f"n--- MINT FAILED ---")
        print(f"Transaction failed with result code: {result_code}")

    print(f"nTransaction Hash: {response.result['hash']}")
    print(f"Validated in Ledger Index: {response.result['ledger_index']}")

except Exception as e:
    print(f"nAn error occurred during submission: {e}")