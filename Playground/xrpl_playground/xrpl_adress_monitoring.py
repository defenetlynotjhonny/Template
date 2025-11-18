import json
import os
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountInfo
from xrpl.models.transactions import AccountSet, AccountSetAsfFlag
from xrpl.transaction import submit_and_wait
from xrpl.wallet import Wallet
from dotenv import load_dotenv

def get_account_info(address: str, client: JsonRpcClient):
    print(f"\nChecking flags for {address}...")
    try:
        request = AccountInfo(account=address, ledger_index="validated")
        response = client.request(request)
        if response.is_successful():
            return response.result["account_flags"]
        print(f"Error: {response.result['error_message']}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def main():
    load_dotenv()
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
    
    try:
        seed = os.environ["SEED_PHRASE_1"]
        wallet = Wallet.from_secret(seed)
    except KeyError:
        print("Error: SEED_PHRASE_1 not found in .env file.")
        return

    address = wallet.classic_address
    
    flags_before = get_account_info(address, client)
    if flags_before:
        print(json.dumps(flags_before, indent=2))

    print("\nSending AccountSet to TURN ON 'ASF_REQUIRE_DEST'...")
    try:
        set_tx = AccountSet(
            account=address,
            set_flag=AccountSetAsfFlag.ASF_DEPOSIT_AUTH
        )
        response_set = submit_and_wait(set_tx, client, wallet)
        print(json.dumps(response_set.result, indent=2))
    except Exception as e:
        print(f"Error: {e}")

    flags_after = get_account_info(address, client)
    if flags_after:
        print("Account info:")
        print(json.dumps(flags_after, indent=2))

    print("\nSending AccountSet to TURN OFF 'ASF_REQUIRE_DEST'...")
    try:
        clear_tx = AccountSet(
            account=address,
            clear_flag=AccountSetAsfFlag.ASF_REQUIRE_DEST
        )
        response_clear = submit_and_wait(clear_tx, client, wallet)
        print(json.dumps(response_clear.result, indent=2))
    except Exception as e:
        print(f"Error: {e}")

    flags_final = get_account_info(address, client)
    if flags_final:
        print(json.dumps(flags_final, indent=2))

if __name__ == "__main__":
    main()