#!/usr/bin/env python3
"""Enumerate all connected hardware wallets and highlight KeepKey devices.

Usage:
    python examples/01_enumerate_devices.py
    python examples/01_enumerate_devices.py --expert
    python examples/01_enumerate_devices.py --chain test
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import enumerate as hwi_enumerate

from keepkey_helpers import add_common_args, resolve_chain


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    args = parser.parse_args()

    chain = resolve_chain(args.chain)
    devices = hwi_enumerate(password=args.passphrase or None, expert=args.expert, chain=chain)

    if not devices:
        print("No hardware wallets detected.")
        print("Make sure your device is connected and unlocked.")
        sys.exit(1)

    print(f"Found {len(devices)} device(s):\n")
    for i, dev in enumerate(devices):
        is_keepkey = dev.get("type") == "keepkey"
        marker = " <<< KeepKey" if is_keepkey else ""
        print(f"--- Device {i + 1}{marker} ---")
        print(json.dumps(dev, indent=2))
        print()


if __name__ == "__main__":
    main()
