"""Shared certificate verification for HTTP monitoring clients."""

import argparse
import ssl


def add_tls_arguments(parser: argparse.ArgumentParser) -> None:
    """Keep the legacy verification flag and support private CA bundles."""
    parser.add_argument("--verify-ssl", action="store_true", default=True, help=argparse.SUPPRESS)
    parser.add_argument("--ca-file", help="PEM CA bundle; defaults to system trust")


def tls_verification(ca_file: str | None = None) -> bool | ssl.SSLContext:
    """Verify both trust and hostname, including when a private CA is supplied."""
    return ssl.create_default_context(cafile=ca_file) if ca_file else True
