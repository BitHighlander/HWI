#!/usr/bin/env python3
"""Get output descriptors from the KeepKey.

Output descriptors can be imported into Bitcoin Core using `importdescriptors`.

Usage:
    python examples/06_get_descriptors.py
    python examples/06_get_descriptors.py --account 0
    python examples/06_get_descriptors.py --passphrase "my secret" --account 1
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import getdescriptors

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--account", type=int, default=0, help="Account number (default: 0)")
    args = parser.parse_args()

    chain = resolve_chain(args.chain)

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        result = getdescriptors(client, account=args.account)
        print(f"Output descriptors for account {args.account}:\n")

        print("Receive descriptors:")
        for desc in result.get("receive", []):
            print(f"  {desc}")

        print("\nChange (internal) descriptors:")
        for desc in result.get("internal", []):
            print(f"  {desc}")

        print("\nJSON output:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
