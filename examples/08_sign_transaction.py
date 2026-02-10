#!/usr/bin/env python3
"""Sign a PSBT (Partially Signed Bitcoin Transaction) with the KeepKey.

Accepts a PSBT as a base64 string or from a file. The device will display
the transaction details for confirmation before signing.

Usage:
    python examples/08_sign_transaction.py --psbt "cHNidP8BAH..."
    python examples/08_sign_transaction.py --psbt-file tx.psbt
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import signtx

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--psbt", help="PSBT as base64 string")
    group.add_argument("--psbt-file", help="Path to file containing PSBT (base64)")
    args = parser.parse_args()

    if args.psbt_file:
        with open(args.psbt_file, "r") as f:
            psbt = f.read().strip()
    else:
        psbt = args.psbt

    chain = resolve_chain(args.chain)

    print("Sending PSBT to KeepKey for signing...")
    print("  Please confirm the transaction on device.\n")

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        result = signtx(client, psbt=psbt)
        signed = result.get("signed", False)
        print(f"Signed: {signed}")
        if signed:
            print(f"\nSigned PSBT:")
            print(result["psbt"])
        else:
            print("\nPSBT was not modified (signing may have failed or been cancelled).")
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
