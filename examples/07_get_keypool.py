#!/usr/bin/env python3
"""Get keypool descriptors for Bitcoin Core import.

Generates descriptors suitable for `importmulti` or `importdescriptors` in
Bitcoin Core.

Usage:
    python examples/07_get_keypool.py
    python examples/07_get_keypool.py --start 0 --end 100
    python examples/07_get_keypool.py --all
    python examples/07_get_keypool.py --addr-type legacy
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import getkeypool
from hwilib.common import AddressType

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain

ADDR_TYPE_MAP = {
    "legacy": AddressType.LEGACY,
    "wit": AddressType.WIT,
    "sh_wit": AddressType.SH_WIT,
    "tap": AddressType.TAP,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--start", type=int, default=0, help="Keypool start index (default: 0)")
    parser.add_argument("--end", type=int, default=999, help="Keypool end index (default: 999)")
    parser.add_argument("--account", type=int, default=0, help="Account number (default: 0)")
    parser.add_argument(
        "--addr-type",
        choices=["legacy", "wit", "sh_wit", "tap"],
        default="wit",
        help="Address type (default: wit / native segwit)",
    )
    parser.add_argument("--all", action="store_true", help="Get keypool for all address types")
    parser.add_argument("--internal", action="store_true", help="Get change (internal) keypool")
    args = parser.parse_args()

    chain = resolve_chain(args.chain)
    addr_type = ADDR_TYPE_MAP[args.addr_type]

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        result = getkeypool(
            client,
            path="",
            start=args.start,
            end=args.end,
            internal=args.internal,
            keypool=True,
            account=args.account,
            addr_type=addr_type,
            addr_all=args.all,
        )
        print(f"Keypool ({args.start}-{args.end}):")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
