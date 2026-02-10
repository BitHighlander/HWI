#!/usr/bin/env python3
"""Shared helpers for KeepKey CLI examples.

Provides device discovery, client management, and common argparse setup
for all example scripts.
"""
import argparse
import os
import sys
from contextlib import contextmanager
from typing import Any, Dict, Optional

# Ensure hwilib is importable from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hwilib.commands import enumerate as hwi_enumerate, get_client
from hwilib.common import AddressType, Chain

CHAIN_MAP = {
    "main": Chain.MAIN,
    "test": Chain.TEST,
    "regtest": Chain.REGTEST,
    "signet": Chain.SIGNET,
}


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments shared by all example scripts."""
    parser.add_argument(
        "--passphrase",
        default="",
        help="BIP39 passphrase (default: empty)",
    )
    parser.add_argument(
        "--chain",
        choices=["main", "test", "regtest", "signet"],
        default="main",
        help="Bitcoin network (default: main)",
    )
    parser.add_argument(
        "--expert",
        action="store_true",
        help="Enable expert mode for additional output",
    )


def resolve_chain(chain_str: str) -> Chain:
    """Convert chain string argument to Chain enum."""
    return CHAIN_MAP[chain_str]


def find_keepkey(
    password: str = "",
    chain: Chain = Chain.MAIN,
    expert: bool = False,
) -> Optional[Dict[str, Any]]:
    """Find the first connected KeepKey device.

    Returns the device dict from enumerate() or None if no KeepKey found.
    """
    devices = hwi_enumerate(password=password or None, expert=expert, chain=chain)
    for dev in devices:
        if dev.get("type") == "keepkey":
            return dev
    return None


def get_keepkey_client(
    password: str = "",
    chain: Chain = Chain.MAIN,
    expert: bool = False,
):
    """Get an HWI client for the first connected KeepKey.

    Returns a HardwareWalletClient or raises RuntimeError.
    """
    dev = find_keepkey(password=password, chain=chain, expert=expert)
    if dev is None:
        raise RuntimeError("No KeepKey device found. Is it connected and unlocked?")

    client = get_client(
        device_type=dev["type"],
        device_path=dev["path"],
        password=password or None,
        expert=expert,
        chain=chain,
    )
    if client is None:
        raise RuntimeError(
            f"Failed to open client for KeepKey at {dev['path']}. "
            "Check that the device is unlocked and not in use by another application."
        )
    return client


@contextmanager
def keepkey_session(
    password: str = "",
    chain: Chain = Chain.MAIN,
    expert: bool = False,
):
    """Context manager that yields a KeepKey HWI client and ensures cleanup.

    Usage:
        with keepkey_session(password="", chain=Chain.MAIN) as client:
            result = getmasterxpub(client)
    """
    client = get_keepkey_client(password=password, chain=chain, expert=expert)
    try:
        yield client
    finally:
        try:
            client.close()
        except Exception:
            pass
