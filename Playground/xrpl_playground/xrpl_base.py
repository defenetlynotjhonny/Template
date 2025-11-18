from xrpl.clients import JsonRpcClient
from xrpl.models import requests
from xrpl.wallet import Wallet
from pprint import pprint
import os
from dotenv import load_dotenv
# Import all necessary models and helpers
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.transaction import submit_and_wait
from xrpl.models.transactions import (
    Payment, TrustSet, OfferCreate, NFTokenMint
)
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.utils import xrp_to_drops, str_to_hex
from xrpl.models.transactions.nftoken_mint import NFTokenMintFlag

class XrplQueryClient:
    """
    Handles all READ-ONLY requests to the XRP Ledger.
    This class does not hold any private keys.
    """
    def __init__(self, url: str):
        self.client = JsonRpcClient(url)

    def get_server_info(self):
        return self.client.request(requests.ServerInfo()).result

    def get_server_state(self):
        return self.client.request(requests.ServerState()).result

    def get_ledger(self, ledger_index="validated"):
        return self.client.request(requests.Ledger(
            ledger_index=ledger_index, 
            transactions=True, 
            expand=True
        )).result

    def get_ledger_closed(self):
        return self.client.request(requests.LedgerClosed()).result

    def get_ledger_current(self):
        return self.client.request(requests.LedgerCurrent()).result

    def account_info(self, account: str):
        return self.client.request(requests.AccountInfo(account=account)).result

    def account_currencies(self, account: str):
        return self.client.request(requests.AccountCurrencies(account=account)).result

    def account_lines(self, account: str, peer: str = None):
        return self.client.request(requests.AccountLines(account=account, peer=peer)).result

    def account_nfts(self, account: str):
        return self.client.request(requests.AccountNFTs(account=account)).result

    def account_channels(self, account: str):
        # Note: ChannelAuthorize is a transaction type. 
        # For querying channels, you'd use account_objects
        # or a specific method if available (e.g., PaymentChannel)
        # This is likely an error in the original. 
        # Let's use the correct request:
        return self.client.request(requests.AccountObjects(
            account=account, 
            type="payment_channel"
        )).result

    def account_objects(self, account: str, type: str = None):
        return self.client.request(requests.AccountObjects(account=account, type=type)).result

    def account_offers(self, account: str):
        return self.client.request(requests.AccountOffers(account=account)).result

    def book_offers(self, taker_gets, taker_pays, limit=10):
        return self.client.request(requests.BookOffers(
            taker_gets=taker_gets, 
            taker_pays=taker_pays, 
            limit=limit
        )).result

    def nft_info(self, nft_id):
        # Note: NFTInfo is deprecated. Use NFTokenInfo
        return self.client.request(requests.NFTokenInfo(nft_id=nft_id)).result

    def nft_buy_offers(self, nft_id):
        return self.client.request(requests.NFTBuyOffers(nft_id=nft_id)).result

    def nft_sell_offers(self, nft_id):
        return self.client.request(requests.NFTSellOffers(nft_id=nft_id)).result

    def ripple_path_find(self, source_account, destination_account, destination_amount):
        return self.client.request(requests.RipplePathFind(
            source_account=source_account,
            destination_account=destination_account,
            destination_amount=destination_amount
        )).result

    def path_find(self, subcommand="create", **kwargs):
        return self.client.request(requests.PathFind(subcommand=subcommand, **kwargs)).result

    def ledger_data(self, limit=10, marker=None):
        return self.client.request(requests.LedgerData(limit=limit, marker=marker)).result

    def manifest(self, public_key):
        return self.client.request(requests.Manifest(public_key=public_key)).result
    




class XrplTransactionClient:
    """
    Handles all WRITE operations (transactions) to the XRP Ledger.
    It securely holds a Wallet object to sign transactions.
    """
    def __init__(self, client: JsonRpcClient, wallet: Wallet):
        self.client = client
        self.wallet = wallet
        self.account = wallet.classic_address # Get the address from the wallet

    def send_xrp(self, destination: str, amount_xrp: float, destination_tag: int = None):
        """
        Constructs, signs, and submits an XRP Payment.
        [Ref: Section III.A. Payment (XRP), cite: 2072-2101]
        """
        print(f"Preparing to send {amount_xrp} XRP to {destination}...")
        
        payment_tx = Payment(
            account=self.account,
            amount=xrp_to_drops(amount_xrp),
            destination=destination,
            destination_tag=destination_tag
        )
        
        # This uses the "submit_and_wait" pattern from your docs
        # It automatically autofills fees, signs, submits, and verifies.
        # [Ref: Section II.D, cite: 2030-2041]
        try:
            response = submit_and_wait(payment_tx, self.client, self.wallet)
            return response.result
        except Exception as e:
            print(f"Error submitting transaction: {e}")
            return None

    def set_trust_line(self, issuer: str, currency: str, limit: str):
        """
        Constructs, signs, and submits a TrustSet transaction.
        [Ref: Section III.B. TrustSet (Creating a Trust Line), cite: 2145-2179]
        """
        print(f"Preparing to set Trust Line for {currency}.{issuer}...")
        
        trust_limit = IssuedCurrencyAmount(
            currency=currency,
            issuer=issuer,
            value=limit
        )
        
        trust_set_tx = TrustSet(
            account=self.account,
            limit_amount=trust_limit
        )
        
        try:
            response = submit_and_wait(trust_set_tx, self.client, self.wallet)
            return response.result
        except Exception as e:
            print(f"Error submitting transaction: {e}")
            return None

    def mint_nft(self, uri: str, taxon: int = 0, flags: int = NFTokenMintFlag.TF_TRANSFERABLE):
        """
        Constructs, signs, and submits an NFTokenMint transaction.
        [Ref: Section III.D. NFTokenMint (Minting an NFT), cite: 2223-2260]
        """
        print(f"Preparing to mint NFT with URI: {uri}...")
        
        mint_tx = NFTokenMint(
            account=self.account,
            uri=str_to_hex(uri),
            nftoken_taxon=taxon,
            flags=flags
        )
        
        try:
            response = submit_and_wait(mint_tx, self.client, self.wallet)
            return response.result
        except Exception as e:
            print(f"Error submitting transaction: {e}")
            return None

if __name__ == "__main__":
    load_dotenv()

    RPC_URL = os.getenv("XRPL_RPC_URL", "https://s.altnet.rippletest.net:51234")
    ACCOUNT_ADDRESS = os.getenv("wallet_1")
    WALLET_SEED = os.getenv("SEED_PHRASE_1")
    NFT_ID = "00000000955CF0E765491900ECA6C630CCCE9566A407F9264DB3191000BBB976"
    MANIFEST_PUB_KEY = os.getenv("XRPL_MANIFEST_PUB_KEY")

    query_client = XrplQueryClient(RPC_URL)

    pprint(query_client.get_server_info())
    pprint(query_client.get_server_state())
    pprint(query_client.get_ledger())
    pprint(query_client.get_ledger_closed())
    pprint(query_client.get_ledger_current())

    if ACCOUNT_ADDRESS:
        pprint(query_client.account_info(ACCOUNT_ADDRESS))
        pprint(query_client.account_currencies(ACCOUNT_ADDRESS))
        pprint(query_client.account_lines(ACCOUNT_ADDRESS))
        pprint(query_client.account_nfts(ACCOUNT_ADDRESS))
        pprint(query_client.account_channels(ACCOUNT_ADDRESS))
        pprint(query_client.account_objects(ACCOUNT_ADDRESS))
        pprint(query_client.account_offers(ACCOUNT_ADDRESS))

    pprint(query_client.ledger_data(limit=5))

    if NFT_ID:
        pprint(query_client.nft_info(NFT_ID))
        pprint(query_client.nft_buy_offers(NFT_ID))
        pprint(query_client.nft_sell_offers(NFT_ID))

    if MANIFEST_PUB_KEY:
        pprint(query_client.manifest(MANIFEST_PUB_KEY))

    if WALLET_SEED:
        wallet = Wallet(seed=WALLET_SEED, sequence=0)
        tx_client = XrplTransactionClient(JsonRpcClient(RPC_URL), wallet)
        print(f"Loaded wallet account: {tx_client.account}")