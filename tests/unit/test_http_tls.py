# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Verify actual TLS trust and hostname checks with locally generated keys."""

import datetime as dt
import ssl
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch

import httpx
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from nagios_plugins.services.http_tls import tls_verification
from nagios_plugins.services.tls import days_remaining, fetch_server_cert


@pytest.fixture
def tls_server(tmp_path: Path) -> Iterator[tuple[int, str]]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = dt.datetime.now(dt.UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - dt.timedelta(minutes=1))
        .not_valid_after(now + dt.timedelta(days=1))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
        .sign(key, hashes.SHA256())
    )
    cert_path = tmp_path / "cert.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path = tmp_path / "key.pem"
    key_path.touch(mode=0o600)
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"trusted")

        def log_message(self, format: str, *args: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_path, key_path)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server.server_port, str(cert_path)
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_default_trust_rejects_unknown_certificate(tls_server: tuple[int, str]) -> None:
    port, _ = tls_server
    with (
        httpx.Client(verify=tls_verification(), trust_env=False) as client,
        pytest.raises(httpx.ConnectError, match="CERTIFICATE_VERIFY_FAILED"),
    ):
        client.get(f"https://localhost:{port}")


def test_explicit_ca_allows_matching_hostname(tls_server: tuple[int, str]) -> None:
    port, ca_file = tls_server
    with httpx.Client(verify=tls_verification(ca_file), trust_env=False) as client:
        response = client.get(f"https://localhost:{port}")
    assert response.status_code == 200
    assert response.text == "trusted"


def test_explicit_ca_still_rejects_wrong_hostname(tls_server: tuple[int, str]) -> None:
    port, ca_file = tls_server
    with (
        httpx.Client(verify=tls_verification(ca_file), trust_env=False) as client,
        pytest.raises(httpx.ConnectError, match="CERTIFICATE_VERIFY_FAILED"),
    ):
        client.get(f"https://127.0.0.1:{port}")


def test_verified_peer_certificate_metadata(tls_server: tuple[int, str]) -> None:
    port, ca_file = tls_server
    context = ssl.create_default_context(cafile=ca_file)
    with patch("ssl.create_default_context", return_value=context):
        info = fetch_server_cert("localhost", port)
    assert info.san_count == 1
    assert "localhost" in info.subject
    assert "localhost" in info.issuer
    assert days_remaining(info, now=info.not_after - dt.timedelta(days=5)) == 5
    assert days_remaining(info, now=info.not_after + dt.timedelta(days=1)) == 0
