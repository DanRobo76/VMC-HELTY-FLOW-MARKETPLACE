"""La rete del banco: uno spazio di rete tutto suo (``unshare -n``) con gli indirizzi delle
VMC finte e un ``ping`` finto.

Il banco gira in un nuovo spazio dei nomi di rete: dentro c'è solo l'interfaccia di
loopback, a cui si aggiungono gli indirizzi delle VMC (192.168.1.x, come in una casa).
Home Assistant, le VMC finte e il browser vedono solo questa rete: nessuna porta degli
altri processi del calcolatore, nessuna uscita verso internet (il sensore della versione su
GitHub risponde «Errore Connessione» subito), e tutto sparisce alla fine del processo.

Il package di oggi controlla la VMC con ``ping`` (sensore ``status_ip``), che qui non c'è:
il ``ping`` finto risponde come quello vero quando la VMC finta accetta la connessione
sulla porta 5001 (accesa), e tace quando non risponde.
"""

from __future__ import annotations

import fcntl
import os
import socket
import struct
import subprocess
import sys
from pathlib import Path

VARIABILE = "VMC_BANCO_RETE"
"""Variabile d'ambiente che segna il processo già nello spazio di rete del banco."""

SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914
SIOCSIFADDR = 0x8916
IFF_UP = 0x1

PING_FINTO = """\
#!/usr/bin/env python3
# ping finto del banco (rete.py): risponde se la VMC accetta la connessione sulla porta 5001
import socket, sys
indirizzo = sys.argv[-1]
try:
    socket.create_connection((indirizzo, 5001), timeout=1).close()
except OSError:
    print(f"PING {indirizzo} ({indirizzo}) 56(84) bytes of data.")
    sys.exit(1)
print(f"PING {indirizzo} ({indirizzo}) 56(84) bytes of data.")
for n in (1, 2, 3):
    print(f"64 bytes from {indirizzo}: icmp_seq={n} ttl=64 time=0.05 ms")
"""


def nello_spazio_del_banco() -> bool:
    return os.environ.get(VARIABILE) == "1"


def rilancia_nello_spazio_del_banco() -> int:
    """Rilancia questo stesso comando dentro un nuovo spazio dei nomi di rete."""
    ambiente = {**os.environ, VARIABILE: "1"}
    # nessun proxy: dentro lo spazio del banco non c'è rete verso fuori
    for chiave in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
        ambiente.pop(chiave, None)
    comando = ["unshare", "-n", sys.executable, *sys.argv]
    return subprocess.call(comando, env=ambiente)


def prepara_indirizzi(indirizzi: list[str]) -> None:
    """Accende l'interfaccia di loopback e le aggiunge gli indirizzi delle VMC."""
    presa = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        richiesta = struct.pack("16sH14s", b"lo", 0, b"")
        bandiere = struct.unpack(
            "16sH14s", fcntl.ioctl(presa, SIOCGIFFLAGS, richiesta)
        )[1]
        fcntl.ioctl(
            presa, SIOCSIFFLAGS, struct.pack("16sH14s", b"lo", bandiere | IFF_UP, b"")
        )
        for numero, indirizzo in enumerate(indirizzi, start=1):
            richiesta = struct.pack(
                "16sH2s4s8s",
                f"lo:{numero}".encode(),
                socket.AF_INET,
                b"\x00" * 2,
                socket.inet_aton(indirizzo),
                b"\x00" * 8,
            )
            fcntl.ioctl(presa, SIOCSIFADDR, richiesta)
    finally:
        presa.close()


def prepara_ping(cartella: Path) -> Path:
    """Scrive il ``ping`` finto in ``cartella`` e restituisce la cartella (da mettere in
    testa al PATH di Home Assistant)."""
    cartella.mkdir(parents=True, exist_ok=True)
    ping = cartella / "ping"
    ping.write_text(PING_FINTO, encoding="utf-8")
    ping.chmod(0o755)
    return cartella
