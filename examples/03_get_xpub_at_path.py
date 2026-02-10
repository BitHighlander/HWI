#!/usr/bin/env python3
"""Get the extended public key (xpub) at a specific derivation path.

Usage:
    python examples/03_get_xpub_at_path.py
    python examples/03_get_xpub_at_path.py --path "m/44'/0'/0'"
    python examples/03_get_xpub_at_path.py --expert
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import getxpub

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain

DEFAULT_PATHS = [
    ("BIP44 Legacy", "m/44'/0'/0'"),
    ("BIP49 Nested SegWit", "m/49'/0'/0'"),
    ("BIP84 Native SegWit", "m/84'/0'/0'"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--path", default=None, help="Custom derivation path (default: show standard paths)")
    args = parser.parse_args()

    chain = resolve_chain(args.chain)
    paths = [("Custom", args.path)] if args.path else DEFAULT_PATHS

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        for label, path in paths:
            print(f"{label} ({path}):")
            result = getxpub(client, path=path, expert=args.expert)
            print(json.dumps(result, indent=2))
            print()


if __name__ == "__main__":
    main()
