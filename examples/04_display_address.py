#!/usr/bin/env python3
"""Display a Bitcoin address on the KeepKey screen for verification.

This triggers an on-device confirmation showing the address so you can
verify it matches what your wallet software shows.

Usage:
    python examples/04_display_address.py
    python examples/04_display_address.py --path "m/84'/0'/0'/0/0"
    python examples/04_display_address.py --addr-type legacy --path "m/44'/0'/0'/0/0"
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import displayaddress
from hwilib.common import AddressType

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain

ADDR_TYPE_MAP = {
    "legacy": AddressType.LEGACY,
    "wit": AddressType.WIT,
    "sh_wit": AddressType.SH_WIT,
    "tap": AddressType.TAP,
}

DEFAULT_PATHS = {
    "legacy": "m/44'/0'/0'/0/0",
    "sh_wit": "m/49'/0'/0'/0/0",
    "wit": "m/84'/0'/0'/0/0",
    "tap": "m/86'/0'/0'/0/0",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument(
        "--addr-type",
        choices=["legacy", "wit", "sh_wit", "tap"],
        default="wit",
        help="Address type (default: wit / native segwit)",
    )
    parser.add_argument(
        "--path",
        default=None,
        help="Derivation path (default: standard path for address type)",
    )
    args = parser.parse_args()

    chain = resolve_chain(args.chain)
    addr_type = ADDR_TYPE_MAP[args.addr_type]
    path = args.path or DEFAULT_PATHS[args.addr_type]

    print(f"Requesting address display on KeepKey...")
    print(f"  Address type: {args.addr_type}")
    print(f"  Path: {path}")
    print(f"  Please confirm on device.\n")

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        result = displayaddress(client, path=path, addr_type=addr_type)
        print("Address:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
