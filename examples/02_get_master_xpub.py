#!/usr/bin/env python3
"""Get the master extended public key (xpub) from a KeepKey.

Shows the master xpub for different address types and accounts.

Usage:
    python examples/02_get_master_xpub.py
    python examples/02_get_master_xpub.py --passphrase "my secret"
    python examples/02_get_master_xpub.py --account 1
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import getmasterxpub
from hwilib.common import AddressType

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--account", type=int, default=0, help="Account number (default: 0)")
    args = parser.parse_args()

    chain = resolve_chain(args.chain)
    addr_types = [
        ("Legacy (P2PKH)", AddressType.LEGACY),
        ("Nested SegWit (P2SH-P2WPKH)", AddressType.SH_WIT),
        ("Native SegWit (P2WPKH)", AddressType.WIT),
    ]

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        print(f"Master xpubs for account {args.account}:\n")
        for label, addrtype in addr_types:
            result = getmasterxpub(client, addrtype=addrtype, account=args.account)
            print(f"  {label}:")
            print(f"    {result['xpub']}\n")


if __name__ == "__main__":
    main()
