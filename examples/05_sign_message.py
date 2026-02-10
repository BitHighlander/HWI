#!/usr/bin/env python3
"""Sign a message with a key on the KeepKey.

The device will display the message for confirmation before signing.

Usage:
    python examples/05_sign_message.py
    python examples/05_sign_message.py --message "Proof of ownership"
    python examples/05_sign_message.py --path "m/44'/0'/0'/0/0" --message "Hello"
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import signmessage

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument(
        "--message",
        default="Hello from KeepKey via HWI!",
        help='Message to sign (default: "Hello from KeepKey via HWI!")',
    )
    parser.add_argument(
        "--path",
        default="m/84'/0'/0'/0/0",
        help="Derivation path for signing key (default: m/84'/0'/0'/0/0)",
    )
    args = parser.parse_args()

    chain = resolve_chain(args.chain)

    print(f"Signing message with KeepKey...")
    print(f"  Message: {args.message}")
    print(f"  Path: {args.path}")
    print(f"  Please confirm on device.\n")

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        result = signmessage(client, message=args.message, path=args.path)
        print("Signature:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
