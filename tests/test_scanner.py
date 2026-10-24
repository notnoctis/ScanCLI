"""Test Fase 0 — pakai `unittest` bawaan Python (project ini stdlib only).

Jalankan dengan:  python3 -m unittest discover -s tests -v
"""

import socket
import threading
import unittest

from scancli.scanner import scan_port


class TestScanner(unittest.TestCase):
    def test_open_port_detected(self):
        # Buka port *asli* di localhost supaya scanner punya target yang jalan.
        # port 0 = "kasih nomor port bebas", lalu kita tanya port-nya.
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]

        # Thread supaya koneksi dari scanner tidak menggantung forever.
        # Kembalikan juga socket yang di-accept, `done` berfungsi sebagai
        # wadah agar bisa kita tutup — KEDUA sisi koneksi harus ditutup,
        # kalau tidak, Python protes lewat ResourceWarning.
        done: list[socket.socket] = []
        threading.Thread(target=lambda: done.append(server.accept()[0]), daemon=True).start()

        self.assertIsNotNone(scan_port("127.0.0.1", port, timeout=2))
        for s in done:
            s.close()
        server.close()

    def test_closed_port(self):
        # Pakai port yang sudah kita tutup sendiri => pasti refused -> None.
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
        probe.close()

        self.assertIsNone(scan_port("127.0.0.1", port, timeout=2))


if __name__ == "__main__":
    unittest.main()
