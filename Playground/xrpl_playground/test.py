import json
from pprint import pprint
import time
from xrpl.clients import JsonRpcClient
from xrpl.models import requests
from xrpl.models.requests import AccountObjectType

def print_and_save(name, result, file_handle):
    header = f"\n--- {name} ---\n"
    formatted_json = json.dumps(result, indent=4)
    
    print(header)
    pprint(formatted_json)
    
    file_handle.write(header)
    file_handle.write(formatted_json)
    file_handle.write("\n")

client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
account_address = "rNcmpNiUjUjrWhod2Vr1fgQPtZm9QyPVRV"
output_file = "xrpl_api_explorer_minimal.txt"

print(f"Starting API exploration for {account_address} on Testnet.")
print(f"All results will be saved to {output_file}")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"XRPL API Exploration Results for {account_address}\n")
    f.write(f"Timestamp: {time.ctime()}\n")

    # --- Server Info Methods ---
    print_and_save("ServerInfo", client.request(requests.ServerInfo()).result, f)
    print_and_save("ServerState", client.request(requests.ServerState()).result, f)
    print_and_save("Ping", client.request(requests.Ping()).result, f)
    print_and_save("Random", client.request(requests.Random()).result, f)

    # --- Ledger Methods ---
    print_and_save("LedgerCurrent", client.request(requests.LedgerCurrent()).result, f)
    print_and_save("LedgerClosed", client.request(requests.LedgerClosed()).result, f)
    
    current_ledger_index = client.request(requests.LedgerCurrent()).result["ledger_current_index"]
    
    ledger_request = requests.Ledger(ledger_index=current_ledger_index, transactions=True, expand=False)
    print_and_save("Ledger (Current)", client.request(ledger_request).result, f)

    ledger_data_request = requests.LedgerData(ledger_index=current_ledger_index, limit=5)
    print_and_save("LedgerData (Limit 5)", client.request(ledger_data_request).result, f)


    # --- Account Methods ---
    print_and_save("AccountInfo", client.request(requests.AccountInfo(account=account_address)).result, f)
    print_and_save("AccountCurrencies", client.request(requests.AccountCurrencies(account=account_address)).result, f)
    print_and_save("AccountChannels", client.request(requests.AccountChannels(account=account_address)).result, f)
    print_and_save("AccountLines", client.request(requests.AccountLines(account=account_address)).result, f)
    print_and_save("AccountNFTs", client.request(requests.AccountNFTs(account=account_address)).result, f)
    
    acc_objects_request = requests.AccountObjects(
        account=account_address, 
        type=AccountObjectType.STATE
    )
    print_and_save("AccountObjects (Type: State)", client.request(acc_objects_request).result, f)
    
    print_and_save("AccountOffers", client.request(requests.AccountOffers(account=account_address)).result, f)
    
    acc_tx_request = requests.AccountTx(account=account_address, limit=5)
    acc_tx_response = client.request(acc_tx_request).result
    print_and_save("AccountTx (Limit 5)", acc_tx_response, f)

    print_and_save("GatewayBalances", client.request(requests.GatewayBalances(account=account_address)).result, f)
    
    print_and_save("NFTsByIssuer", client.request(requests.NFTsByIssuer(issuer=account_address)).result, f)

print(f"\nDone. All results saved to {output_file}")