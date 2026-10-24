"""
ScanCLI — CLI layer.

Fase 0 ini sengaja di buat SERIAL (satu port lewat, tunggu, satu port
berikutnya) supaya konsepnya jelas. Di Fase 1, loop `for` di `run_scan()`
inilah yang akan kita ganti dengan ThreadPoolExecutor.
"""

import argparse

from scancli.scanner import scan_port

# Whether port harus daftar literal — sengaja "monitoring pribadi latihan".
DEFAULT_PORTS = "22,80,443"


def parse_ports(spec: str) -> list[int]:
    """
    Mengubah string daftar port menjadi list int.

    Mendukung dua gaya (biar latihan nanti scan 1-1024 mudah):
      "22,80,443"  -> [22, 80, 443]
      "1-3"        -> [1, 2, 3]
    """
    ports: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return ports


def run_scan(host: str, ports: list[int], timeout: float) -> list[tuple[int, str]]:
    """Scan serial, satu per satu. Kembalikan hanya port yang TERBUKA."""
    print(f"Scanning {host} ({len(ports)} ports)...")
    open_ports: list[tuple[int, str]] = []
    for port in ports:
        banner = scan_port(host, port, timeout)
        if banner is not None:
            open_ports.append((port, banner))
            label = f"{banner[:60]}" if banner else "(open, no banner)"
            print(f"{host}:{port:<6} OPEN   {label}")
        else:
            print(f"{host}:{port:<6} closed")
    return open_ports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scancli",
        description="An educational TCP port scanner & banner grabber.",
        epilog="Only scan hosts you own or are allowed to test!",
    )
    parser.add_argument(
        "-t", "--target", required=True,
        help="hostname or IP to scan (e.g. 127.0.0.1)",
    )
    parser.add_argument(
        "-p", "--ports", default=DEFAULT_PORTS,
        help=f"ports to check, e.g. '22,80,443' or '1-1024' (default: {DEFAULT_PORTS})",
    )
    parser.add_argument(
        "--timeout", type=float, default=2.0,
        help="seconds to wait per port (default: 2.0)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    ports = parse_ports(args.ports)
    open_ports = run_scan(args.target, ports, args.timeout)

    # Rangkuman kecil di bawah — kebiasaan UX CLI yang bagus.
    print("-" * 40)
    print(f"{len(open_ports)} open / {len(ports) - len(open_ports)} closed")
