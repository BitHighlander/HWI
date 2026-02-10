#!/usr/bin/env python3
"""Interactive PIN entry workflow for the KeepKey.

This demonstrates the PIN prompt/send cycle:
1. Send prompt_pin to the device (device shows scrambled PIN matrix)
2. User reads the matrix and enters the PIN positions
3. Send the PIN to the device

The KeepKey displays a 3x3 matrix of dots. Each position corresponds
to a digit 1-9. The matrix is randomized each time, so you must read
the positions from the device screen.

Usage:
    python examples/11_pin_workflow.py
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import prompt_pin, send_pin

from keepkey_helpers import add_common_args, keepkey_session, resolve_chain

PIN_MATRIX_HELP = """
KeepKey PIN Matrix Layout:
The device shows a 3x3 grid. Enter the positions of your PIN digits
using this keypad mapping:

    7 | 8 | 9
    ---------
    4 | 5 | 6
    ---------
    1 | 2 | 3

Look at your KeepKey screen to see where each number appears,
then type the corresponding position numbers.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    args = parser.parse_args()

    chain = resolve_chain(args.chain)

    with keepkey_session(password=args.passphrase, chain=chain, expert=args.expert) as client:
        # Step 1: Prompt for PIN
        print("Requesting PIN entry from KeepKey...")
        print("The device should now display the PIN matrix.\n")

        result = prompt_pin(client)
        print(f"prompt_pin result: {json.dumps(result, indent=2)}\n")

        if not result.get("success", False):
            print("Failed to initiate PIN prompt.")
            sys.exit(1)

        # Step 2: Get PIN from user
        print(PIN_MATRIX_HELP)
        pin = input("Enter PIN (using position numbers from the matrix): ").strip()

        if not pin:
            print("No PIN entered. Aborting.")
            sys.exit(1)

        # Step 3: Send PIN
        result = send_pin(client, pin=pin)
        print(f"\nsend_pin result: {json.dumps(result, indent=2)}")

        if result.get("success", False):
            print("PIN accepted.")
        else:
            print("PIN rejected or error occurred.")


if __name__ == "__main__":
    main()
