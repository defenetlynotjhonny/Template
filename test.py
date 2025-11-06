import ssl
import certifi
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountTx, Ledger, Tx
from pprint import pprint

# --- Use the JSON-RPC URL (HTTPS) ---
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

# --- Test Data ---
# A public Testnet address to check
TARGET_ADDRESS = "rPT1Sjq2YGrBMTcg4Ztkg2oUA8R7CJ9Tnw"
# A known validated transaction hash on the Testnet
TRANSACTION_HASH = "4363B51152431527A3A919A36F9732709280B427F29B1246C613110E4878519B"


def get_latest_ledger(client: JsonRpcClient):
    """
    Fetches the latest validated ledger information.
    """
    print("\n--- 1. Fetching Latest Ledger Info ---")
    request = Ledger(
        ledger_index="validated",
        transactions=True  # Set to True if you want all tx hashes
    )
    
    try:
        response = client.request(request)
        print("--- Response (Ledger): ---")
        pprint(response.result, indent=4)
    except Exception as e:
        print(f"Error fetching ledger: {e}")


def get_transaction_by_hash(client: JsonRpcClient, tx_hash: str):
    """
    Fetches a specific transaction by its unique hash.
    """
    print(f"\n--- 2. Fetching Transaction by Hash: {tx_hash} ---")
    request = Tx(transaction=tx_hash)
    
    try:
        response = client.request(request)
        print("--- Response (Transaction): ---")
        pprint(response.result, indent=4)
    except Exception as e:
        print(f"Error fetching transaction: {e}")


def get_account_transactions(client: JsonRpcClient, account: str):
    """
    Fetches the most recent transactions for a specific account.
    """
    print(f"\n--- 3. Fetching Transactions for Account: {account} ---")
    request = AccountTx(
        account=account,
        limit=5  # Get the 5 most recent transactions
    )
    
    try:
        response = client.request(request)
        print("--- Response (Account Transactions): ---")
        pprint(response.result, indent=4)
    except Exception as e:
        print(f"Error fetching account transactions: {e}")


def main():
    """
    Runs all the example functions.
    """
    print(f"--- Connecting to {JSON_RPC_URL}... ---")
    client = JsonRpcClient(JSON_RPC_URL)
    
    # Run the examples
    get_latest_ledger(client)
    get_transaction_by_hash(client, TRANSACTION_HASH)
    get_account_transactions(client, TARGET_ADDRESS)


if __name__ == "__main__":
    print("--- Script started... ---")
    main()
    print("--- Script finished. ---")
