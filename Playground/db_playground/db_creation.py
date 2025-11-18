#!/usr/bin/env python3
"""
Create a SQLite database that stores XRPL Testnet wallets (address + signing secrets).

Usage:
    python create_xrpl_testnet_wallet_db.py wallets.db 10

This will:
  - create/open wallets.db
  - create a `xrpl_wallets` table (if it doesn't exist)
  - generate 10 XRPL *Testnet* wallets via the Testnet faucet
  - store address, seed, public key, private key in the database
"""

import sys
import sqlite3
from pathlib import Path
from typing import Optional

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet

# Testnet JSON-RPC endpoint (Ripple-operated)
JSON_RPC_TESTNET_URL = "https://s.altnet.rippletest.net:51234"

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS xrpl_wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT,
    address TEXT UNIQUE NOT NULL,
    seed TEXT NOT NULL,
    public_key TEXT NOT NULL,
    private_key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def get_connection(db_path: str) -> sqlite3.Connection:
    """Open a SQLite connection and ensure foreign keys are enabled."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create the xrpl_wallets table if it doesn't exist."""
    conn.execute(DB_SCHEMA)
    conn.commit()


def insert_wallet(
    conn: sqlite3.Connection,
    address: str,
    seed: str,
    public_key: str,
    private_key: str,
    label: Optional[str] = None,
) -> None:
    """Insert a single wallet into the database."""
    conn.execute(
        """
        INSERT INTO xrpl_wallets (label, address, seed, public_key, private_key)
        VALUES (?, ?, ?, ?, ?);
        """,
        (label, address, seed, public_key, private_key),
    )
    conn.commit()


def generate_and_store_wallets(
    conn: sqlite3.Connection,
    client: JsonRpcClient,
    count: int,
    label_prefix: Optional[str] = "wallet",
) -> None:
    """
    Generate `count` XRPL Testnet wallets and store them in the database.

    Uses xrpl-py's `generate_faucet_wallet(client)`, which:
      - calls the Testnet faucet
      - creates a funded Testnet account
      - returns a Wallet with:
          * classic_address / address
          * seed
          * public_key
          * private_key
    """
    for i in range(1, count + 1):
        # Create & fund wallet on XRPL Testnet via faucet
        wallet: Wallet = generate_faucet_wallet(client)

        label = f"{label_prefix}_{i}" if label_prefix else None

        insert_wallet(
            conn=conn,
            address=wallet.classic_address,
            seed=wallet.seed,
            public_key=wallet.public_key,
            private_key=wallet.private_key,
            label=label,
        )

        print(f"[+] Stored TESTNET wallet {i}: {wallet.classic_address}")


def parse_args(argv):
    if len(argv) < 3:
        print(
            "Usage: python create_xrpl_testnet_wallet_db.py <db_path> <num_wallets> [label_prefix]",
            file=sys.stderr,
        )
        sys.exit(1)

    db_path = argv[1]
    try:
        num_wallets = int(argv[2])
    except ValueError:
        print("Error: <num_wallets> must be an integer.", file=sys.stderr)
        sys.exit(1)

    label_prefix = argv[3] if len(argv) >= 4 else "wallet"
    return db_path, num_wallets, label_prefix


def main():
    db_path, num_wallets, label_prefix = parse_args(sys.argv)

    # Ensure directory exists
    db_file = Path(db_path)
    if db_file.parent and not db_file.parent.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"[*] Using database: {db_path}")
    conn = get_connection(db_path)

    # XRPL Testnet client
    client = JsonRpcClient(JSON_RPC_TESTNET_URL)

    try:
        init_db(conn)
        print("[*] Initialized xrpl_wallets table (if not already present).")
        print("[*] Creating funded TESTNET wallets via faucet...")
        generate_and_store_wallets(conn, client, num_wallets, label_prefix)
        print("[*] Done.")
    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    main()
