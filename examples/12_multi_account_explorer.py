#!/usr/bin/env python3
"""Explore multiple accounts on the KeepKey.

Iterates through accounts 0-4, showing xpubs and descriptors for each.
This is useful for understanding how passphrase affects account derivation:
the same device with different passphrases will show entirely different
account fingerprints and keys.

Usage:
    python examples/12_multi_account_explorer.py
    python examples/12_multi_account_explorer.py --max-accounts 10
    python examples/12_multi_account_explorer.py --passphrase "my secret"
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import getdescriptors, getmasterxpub, getxpub
from hwilib.common import AddressType

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument(
        "--max-accounts",
        type=int,
        default=5,
        help="Number of accounts to explore (default: 5)",
    )
    args = parser.parse_args()

    chain = resolve_chain(args.chain)

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        print(f"Exploring accounts 0-{args.max_accounts - 1}")
        if args.passphrase:
            print(f"  Using passphrase: {'*' * len(args.passphrase)}")
        print()

        for account in range(args.max_accounts):
            print(f"{'=' * 60}")
            print(f"Account {account}")
            print(f"{'=' * 60}")

            # Get master xpub for native segwit (most common)
            try:
                xpub_result = getmasterxpub(client, addrtype=AddressType.WIT, account=account)
                print(f"  Native SegWit xpub: {xpub_result['xpub']}")
            except Exception as e:
                print(f"  Error getting xpub: {e}")
                continue

            # Get account-level xpub at BIP84 path
            path = f"m/84'/0'/{account}'"
            try:
                account_xpub = getxpub(client, path=path, expert=args.expert)
                print(f"  Account xpub ({path}): {account_xpub['xpub']}")
            except Exception as e:
                print(f"  Error getting account xpub: {e}")

            # Get descriptors
            try:
                descriptors = getdescriptors(client, account=account)
                receive = descriptors.get("receive", [])
                if receive:
                    print(f"  Receive descriptors ({len(receive)}):")
                    for desc in receive:
                        print(f"    {desc}")
            except Exception as e:
                print(f"  Error getting descriptors: {e}")

            print()


if __name__ == "__main__":
    main()
