# ScanCLI

A fast, **educational** TCP port scanner & service banner grabber — written in
pure Python (stdlib only), no nmap required.

> ⚠️ **Ethics & legal:** use only against hosts you own or are explicitly
> permitted to test — your own machine, your own VMs, or
> [scanme.nmap.org](https://scanme.nmap.org), which exists exactly for this
> purpose. Scanning other people's systems without permission is illegal in
> most jurisdictions.

## Install

```bash
pip install -e .
```

## Usage

```bash
scancli -t 127.0.0.1 -p 22,80,443,8000
# or
python -m scancli -t scanme.nmap.org -p 22,80
```

Example output:

```
Scanning 127.0.0.1 (4 ports)...
127.0.0.1:22     OPEN   SSH-2.0-OpenSSH_9.6
127.0.0.1:80     closed
127.0.0.1:443    closed
127.0.0.1:8000   OPEN   (open, no banner)
```

## Learning roadmap

| Phase | What it teaches | Status |
|-------|-----------------|--------|
| 0 | Sockets, TCP connect, timeouts, banner grabbing, argparse | ✅ here |
| 1 | Concurrency with `concurrent.futures` (fast scanning) | ⏳ |
| 2 | Service fingerprinting, JSON output | ⏳ |
| 3 | `asyncio` rewrite, raw-socket SYN scan | ⏳ |

## Project layout

```
scancli/
├── __main__.py      # entry: python -m scancli
├── cli.py           # argument parsing & reporting
└── scanner.py       # socket logic — the learning core
tests/
└── test_scanner.py
```
