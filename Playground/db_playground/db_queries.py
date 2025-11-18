#!/usr/bin/env python3
"""
Load XRPL wallet records from a SQLite DB and rebuild them as objects.

Usage example:

    loader = WalletLoader("wallets.db")
    wallet_obj = loader.get_wallet_by_id(1)

    print(wallet_obj.address)
    print(wallet_obj.xrpl_wallet)  # XRPL Wallet usable for signing
"""

import sqlite3
import os
import xrpl
from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient


class WalletRecord:
    """
    Represents a wallet loaded from the database.
    Contains:
        - DB fields (address, seed, keys)
        - An xrpl-py Wallet object for signing
    """

    def __init__(self, row):
        self.id = row["id"]
        self.label = row["label"]
        self.address = row["address"]
        self.seed = row["seed"]
        self.public_key = row["public_key"]
        self.private_key = row["private_key"]
        self.created_at = row["created_at"]

        # Re create usable XRPL Wallet object
        self.xrpl_wallet = Wallet(
        seed=self.seed,
        public_key=self.public_key,
        private_key=self.private_key,
)


    def __repr__(self):
        return (
            f"WalletRecord(id={self.id}, address={self.address}, "
            f"label={self.label}, created_at={self.created_at})"
        )


class WalletLoader:
    """Handles loading wallets from the SQLite database."""

    def __init__(self, db_filename="wallets.db"):
        # DB is in the same directory as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_filename)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # return dict-like rows

    def get_wallet_by_id(self, wallet_id: int) -> WalletRecord:
        cur = self.conn.execute(
            "SELECT * FROM xrpl_wallets WHERE id = ?;", (wallet_id,)
        )
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No wallet found with id {wallet_id}")
        return WalletRecord(row)

    def get_wallet_by_address(self, address: str) -> WalletRecord:
        cur = self.conn.execute(
            "SELECT * FROM xrpl_wallets WHERE address = ?;", (address,)
        )
        row = cur.fetchone()
        if not row:
            raise ValueError(f"No wallet found with address {address}")
        return WalletRecord(row)

    def list_wallets(self):
        cur = self.conn.execute("SELECT * FROM xrpl_wallets ORDER BY id;")
        return [WalletRecord(row) for row in cur.fetchall()]

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    loader = WalletLoader("db_xrpl.db")

    print("Listing wallets in DB...")
    wallets = loader.list_wallets()
    for w in wallets:
        print(w)

    print("\nLoading wallet with ID 1...")
    wallet = loader.get_wallet_by_id(1)
    wallet1 = loader.get_wallet_by_id(2)
    print(wallet)
    print("XRPL signing object:", wallet.xrpl_wallet)
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
    payment = xrpl.models.transactions.Payment(
        account=wallet.address,
        amount=xrpl.utils.xrp_to_drops(int(10)),
        destination=wallet1.address,
    )
    response = xrpl.transaction.submit_and_wait(payment, client, wallet.xrpl_wallet)
    print(response)

