"""Test kecil untuk Fase 0 — menjalankan scanner di localhost sendiri (aman)."""

import socket
import threading

from scancli.scanner import scan_port


def test_open_port_detected():
    # Buka port *asli* di localhost supaya scanner punya target yang jatuh.
    # port 0 = "kasih nomor port bebas", lalu kita tanya port-nya.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]

    # Thread di sini supaya koneksi dari scanner tidak menggantung forever.
    threading.Thread(target=server.accept, daemon=True).start()

    assert scan_port("127.0.0.1", port, timeout=2) is not None
    server.close()


def test_closed_port():
    # Pakai port yang sudah kita tutup sendiri => pasti refused -> None.
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()

    assert scan_port("127.0.0.1", port, timeout=2) is None
