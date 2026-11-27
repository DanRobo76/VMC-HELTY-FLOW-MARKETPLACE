"""VMC finte in ascolto sulla porta 5001, una per indirizzo, con l'orologio vero.

Sono le VMC finte del simulatore (``strumenti/simulatore/fakevmc.py``, classe ``FakeVMC``:
stesse risposte a VMGH? e VMGI?, stessi comandi VMWH con la latenza del cambio di
velocità) messe dietro un vero server TCP: qui Home Assistant gira davvero, con i sensori
``tcp`` e i comandi di shell ``nc`` del package di oggi, o con il ``ClientVMC``
dell'integrazione nativa, e parla con la porta 5001 come con una VMC vera.

``fakevmc`` importa ``vclock`` (l'orologio virtuale del simulatore, che cambia
``time.time`` per tutto il processo): qui al suo posto c'è un modulo con il solo ``_V``,
aggiornato con l'orologio vero prima di ogni comando.
"""

from __future__ import annotations

import asyncio
import importlib
import sys
import time
import types
from dataclasses import dataclass, field
from pathlib import Path

SIMULATORE = Path(__file__).resolve().parents[1] / "simulatore"
PORTA = 5001


def _classe_vmc_finta() -> type:
    """La classe ``FakeVMC`` del simulatore, senza il suo orologio virtuale."""
    if "vclock" not in sys.modules:
        orologio = types.ModuleType("vclock")
        orologio._V = [time.monotonic()]  # type: ignore[attr-defined]
        sys.modules["vclock"] = orologio
    if str(SIMULATORE) not in sys.path:
        sys.path.insert(0, str(SIMULATORE))
    return importlib.import_module("fakevmc").FakeVMC


def risposta_lan(ip: str) -> str:
    """Risposta a VMSL? come quella della VMC vera: rete (32), password (32), IP (15),
    porta (5), gateway (15), maschera (15) e modalità, senza «VMSL » davanti."""
    gateway = ".".join([*ip.split(".")[:3], "1"])
    return (
        "CasaProva".ljust(32)
        + "parolasegreta123".ljust(32)
        + ip.ljust(15)
        + "5001".ljust(5)
        + gateway.ljust(15)
        + "255.255.255.0".ljust(15)
        + "1"
    )


@dataclass
class VMCFinta:
    """Una VMC finta: nome (risposta a VMNM?), indirizzo e stato del simulatore."""

    nome: str
    ip: str
    stato: object = field(init=False)
    richieste: list[tuple[float, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.stato = _classe_vmc_finta()()
        self.stato.latency = 0.3

    def rispondi(self, richiesta: str) -> str:
        """La risposta della VMC a una richiesta (lettura o comando)."""
        sys.modules["vclock"]._V[0] = time.monotonic()  # type: ignore[attr-defined]
        self.richieste.append((time.time(), richiesta.strip()))
        testo = richiesta.strip()
        if testo.startswith("VMGH"):
            return self.stato.status_str()
        if testo.startswith("VMGI"):
            return self.stato.sensori_str()
        if testo.startswith("VMNM?"):
            return f"VMNM {self.nome}"
        if testo.startswith("VMSL"):
            return risposta_lan(self.ip)
        if testo.startswith("VMWH"):
            return "OK" if self.stato.command(testo[4:11]) else ""
        if testo.startswith("VMNM "):
            self.nome = testo[5:].strip()
            return "OK"
        return ""


class VMCFinte:
    """I server TCP delle VMC finte (uno per VMC, tutti sulla porta 5001)."""

    def __init__(self, vmc: list[VMCFinta], porta: int = PORTA) -> None:
        self.vmc = {v.ip: v for v in vmc}
        self.porta = porta
        self.porte: dict[str, int] = {}
        self._server: list[asyncio.Server] = []

    async def avvia(self) -> None:
        ciclo = asyncio.get_running_loop()
        for vmc in self.vmc.values():
            vmc.stato.loop = ciclo
            server = await asyncio.start_server(
                lambda r, w, v=vmc: self._servi(v, r, w), vmc.ip, self.porta
            )
            self._server.append(server)
            self.porte[vmc.ip] = server.sockets[0].getsockname()[1]

    async def _servi(
        self,
        vmc: VMCFinta,
        lettore: asyncio.StreamReader,
        scrittore: asyncio.StreamWriter,
    ) -> None:
        try:
            dati = await asyncio.wait_for(lettore.read(256), 5)
            risposta = vmc.rispondi(dati.decode(errors="replace"))
            if risposta:
                scrittore.write(risposta.encode())
                await scrittore.drain()
        except (OSError, TimeoutError):
            pass
        finally:
            scrittore.close()

    async def ferma(self) -> None:
        for server in self._server:
            server.close()
            await server.wait_closed()
        self._server.clear()
