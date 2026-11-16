"""Collegamento al Wi-Fi di casa di una VMC nuova, senza l'App Air Guard.

Usa il motore della Finestra Prima Installazione VMC della release 8.6.0
(motore_installa_vmc.py, identico al programma del package) e la stessa cartella
interna, cosi' un ripristino lasciato a meta' dal package viene completato qui.
Le funzioni sono bloccanti: si chiamano con hass.async_add_executor_job.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from . import motore_installa_vmc as motore

# Stessa cartella della Finestra Prima Installazione VMC (identity.json, restore.json, ...)
CARTELLA_MOTORE = ".vmc_master_installa_vmc"

# Una sola procedura alla volta: il Wi-Fi del server e' uno solo
_BLOCCO = threading.Lock()

Failure = motore.Failure
LED_HINT = motore.LED_HINT


class _Stato(motore.Status):
    """Stato del motore che avvisa anche la finestra (barra di avanzamento)."""

    def __init__(self, root: Path, avanzamento: Callable[[int], None] | None) -> None:
        super().__init__(root)
        self._avanzamento = avanzamento

    def emit(self, stage, progress=0, message="", **values):  # noqa: D102
        super().emit(stage, progress, message, **values)
        if self._avanzamento is not None:
            self._avanzamento(int(progress or 0))


def cartella(config_dir: str) -> Path:
    return Path(config_dir) / CARTELLA_MOTORE


def _motore(config_dir: str, avanzamento: Callable[[int], None] | None) -> motore.Engine:
    radice = cartella(config_dir)
    radice.mkdir(mode=0o700, parents=True, exist_ok=True)
    engine = motore.Engine(radice)
    engine.status = _Stato(radice, avanzamento)
    return engine


def esegui(
    config_dir: str,
    azione: str,
    dati: dict[str, Any] | None = None,
    avanzamento: Callable[[int], None] | None = None,
) -> dict[str, Any]:
    """Esegue un'azione del motore come il worker della 8.6.0 (dispatch) e restituisce
    lo stato finale. Gli errori del motore escono come Failure (codice + messaggio)."""
    if not _BLOCCO.acquire(blocking=False):
        raise Failure("in_corso", "Una procedura è già in corso. Attendi il risultato.")
    try:
        engine = _motore(config_dir, avanzamento)
        if azione == "scan":
            engine.scan()
        elif azione == "configure":
            if (engine.root / "restore.json").exists():
                engine.restore()
            engine.run(dati or {})
        elif azione == "verify":
            engine.verify(dati or {})
        elif azione == "recover":
            engine.recover()
        else:
            raise Failure("invalid_action", "Operazione non valida.")
        return dict(engine.status.data)
    except Failure:
        raise
    except Exception as errore:  # stesso messaggio del worker della 8.6.0
        raise Failure(
            "communication_error",
            "Errore di comunicazione. Verifica la raggiungibilità della VMC e del Supervisor.",
        ) from errore
    finally:
        _BLOCCO.release()


def stato(config_dir: str) -> dict[str, Any]:
    """Stato, ultima VMC collegata (configured_*) e reti trovate (vmc_networks, wifi_networks)."""
    return motore.read_status(cartella(config_dir))


def ultima_vmc(config_dir: str) -> dict[str, Any]:
    """Ultima VMC collegata dal motore: ap_ssid, ip, name, mac (vuoto se nessuna)."""
    return motore.read_identity(cartella(config_dir))


def ripristino_in_sospeso(config_dir: str) -> bool:
    """True se il Wi-Fi del server e' rimasto sulla rete di una VMC (riavvio a meta' procedura)."""
    return (cartella(config_dir) / "restore.json").exists()


def rete_del_server(config_dir: str) -> str:
    """Rete Wi-Fi a cui e' collegato ora il server ("" se nessuna o Supervisor assente)."""
    try:
        info = motore.Supervisor().info()
    except Failure:
        return ""
    for interfaccia in motore.interfaces(info):
        if interfaccia.get("type") == "wireless" and interfaccia.get("connected"):
            return (interfaccia.get("wifi") or {}).get("ssid", "")
    return ""
