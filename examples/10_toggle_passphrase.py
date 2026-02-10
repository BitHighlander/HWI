#!/usr/bin/env python3
"""Toggle BIP39 passphrase protection on the KeepKey.

This enables or disables passphrase protection. The device will prompt
for on-device confirmation.

WARNING: Toggling passphrase changes which wallet is active. Make sure
you understand the implications before proceeding.

Usage:
    python examples/10_toggle_passphrase.py
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import enumerate as hwi_enumerate, toggle_passphrase

from keepkey_helpers import add_common_args, find_keepkey, keepkey_session, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    args = parser.parse_args()

    chain = resolve_chain(args.chain)

    # Show current state
    dev = find_keepkey(password=args.passphrase, chain=chain, expert=True)
    if dev is None:
        print("No KeepKey device found.")
        sys.exit(1)

    current = dev.get("passphrase_protection", "unknown")
    print(f"Current passphrase protection: {current}")
    print("Toggling passphrase protection... Please confirm on device.\n")

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        result = toggle_passphrase(client)
        print("Result:")
        print(json.dumps(result, indent=2))

    # Show new state
    dev_after = find_keepkey(password=args.passphrase, chain=chain, expert=True)
    if dev_after:
        new_state = dev_after.get("passphrase_protection", "unknown")
        print(f"\nPassphrase protection is now: {new_state}")


if __name__ == "__main__":
    main()
