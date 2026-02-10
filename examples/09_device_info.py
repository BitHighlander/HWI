#!/usr/bin/env python3
"""Display detailed device information from the KeepKey.

Uses expert-mode enumeration to show firmware version, device ID, label,
PIN status, passphrase status, and other KeepKey-specific fields.

Usage:
    python examples/09_device_info.py
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import enumerate as hwi_enumerate

from keepkey_helpers import add_common_args, resolve_chain


DISPLAY_FIELDS = [
    ("type", "Device Type"),
    ("model", "Model"),
    ("label", "Label"),
    ("path", "Device Path"),
    ("fingerprint", "Master Fingerprint"),
    ("needs_pin_sent", "Needs PIN"),
    ("needs_passphrase_sent", "Needs Passphrase"),
    ("fw_version", "Firmware Version"),
    ("device_id", "Device ID"),
    ("initialized", "Initialized"),
    ("passphrase_protection", "Passphrase Protection"),
    ("pin_protection", "PIN Protection"),
    ("firmware_variant", "Firmware Variant"),
    ("firmware_hash", "Firmware Hash"),
    ("passphrase_cached", "Passphrase Cached"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    args = parser.parse_args()

    chain = resolve_chain(args.chain)
    # Always use expert mode to get full device info
    devices = hwi_enumerate(password=args.passphrase or None, expert=True, chain=chain)

    keepkeys = [d for d in devices if d.get("type") == "keepkey"]
    if not keepkeys:
        print("No KeepKey device found.")
        sys.exit(1)

    for i, dev in enumerate(keepkeys):
        print(f"=== KeepKey {i + 1} ===\n")
        for field, label in DISPLAY_FIELDS:
            if field in dev:
                print(f"  {label:25s}: {dev[field]}")
        print()

        # Show any extra fields not in the display list
        known_fields = {f[0] for f in DISPLAY_FIELDS}
        extra = {k: v for k, v in dev.items() if k not in known_fields}
        if extra:
            print("  Additional fields:")
            print(json.dumps(extra, indent=4))
            print()

    print("Full JSON:")
    print(json.dumps(keepkeys, indent=2))


if __name__ == "__main__":
    main()
