"""
ScanCLI — Fase 0: TCP Connect Scanner (versi paling sederhana)

=== APA YANG KITA BELAJAR DI FASE INI ===

1. **TCP handshake**: memanggil `socket.connect()` membuat Python melakukan
   three-way handshake (SYN -> SYN-ACK -> ACK) untuk kita. Kalau handshake
   selesai, port *terbuka*; kalau ditolak (`ConnectionRefusedError`), port
   *tertutup*; kalau tidak pernah dibalas (`socket.timeout`), paket mungkin
   di-*drop* firewall -> kita anggap *tidak terjangkau*.

2. **Timeout itu wajib**: tanpa `settimeout()`, scanner bisa berhenti
   selamanya di satu port yang di-firewall. 2 detik adalah kompromi umum.

3. **Banner grabbing**: beberapa layanan (SSH, FTP, SMTP) menyapa dulu
   begitu koneksi dibuka — contoh: `SSH-2.0-OpenSSH_9.6`. String ini
   tentang *fingerprinting* di Fase 2 nanti. HTTP tidak menyapa dulu;
   dia menunggu kita mengirim request — makanya hasilnya banner kosong.
"""

import socket  # modul bawaan Python untuk semua komunikasi jaringan


def scan_port(host: str, port: int, timeout: float = 2.0) -> str | None:
    """
    Mencoba membuka satu koneksi TCP ke `host:port`.

    Return:
      str  -> port TERBUKA, dan layanan mengirim banner (mis. "SSH-2.0-...")
      ""   -> port TERBUKA, tapi tidak menyapa dulu (mis. HTTP)
      None -> port tertutup / tidak terjangkau (refused, filtered, dsb.)
    """
    # AF_INET  = keluarga alamat IPv4
    # SOCK_STREAM = tipe stream berbasis TCP (kalau SOCK_DGRAM, itu UDP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)  # jangan menunggu selamanya
    try:
        # INI titik pentingnya: connect() yang menjalankan TCP handshake.
        sock.connect((host, port))
        try:
            # Banner = data pertama yang dikirim layanan (maks 1024 byte
            # sudah cukup untuk string perkenalan).
            banner = sock.recv(1024).decode(errors="replace").strip()
        except (socket.timeout, ConnectionError):
            # Port terbuka tapi layanannya diam — normal untuk HTTP.
            banner = ""
        return banner
    except (ConnectionRefusedError, socket.timeout, OSError):
        # Refused  = mesin menjawab dengan RST (port tertutup)
        # Timeout  = tidak ada jawaban sama sekali (maybe firewall drop)
        # OSError  = menangkap sisa kasus jaringan lain (DNS gagal, dsb.)
        return None
    finally:
        # Selalu tutup socket, apa pun hasilnya — kalau lupa, OS akan
        # menumpuk socket "zombie" sampai garbage collector lewat.
        sock.close()
