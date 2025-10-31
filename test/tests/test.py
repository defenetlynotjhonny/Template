import requests
import xumm
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()



def get_account_info(account_address: str) -> dict:

    load_dotenv()
    project_origin = os.getenv("MY_PROJECT_ORIGIN")


    # Define the API endpoint and parameters origin mandatory
    base_url = f"https://api.xrpscan.com/api/v1/account/{account_address}"
    params = {
        'origin': project_origin
    }
    
    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # This will show an error like 401 or 403 if auth fails
        print(f"HTTP error occurred: {http_err}") 
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    
    return {}

if __name__ == "__main__":

    secret = os.getenv("XAMAN_SECRET")
    key = os.getenv("XAMAN_KEY")

    sdk = xumm.XummSdk(key, secret)

    print("Xumm SDK initialized successfully.")
    print(sdk.ping())  
    print("\n")
    account = "r3e9LPrquap5VynDSJpfDQuCtnLm45KWci"
    account_data = get_account_info(account)
    
    if account_data:
        print(f"--- Successfully fetched data for {account} ---")
        print("\n")
        pprint(account_data,indent=4)
