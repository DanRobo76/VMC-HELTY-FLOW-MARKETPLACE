"""Le istantanee della casa di prova: tutto quello che il banco confronta.

Due tipi:

- **con Home Assistant acceso** (``istantanea_viva``): stato e attributi di ogni entità,
  registro delle entità e dei dispositivi, voci di configurazione, riparazioni, notifiche,
  plancia e risorse delle plance (le stesse richieste websocket del frontend);
- **con Home Assistant fermo** (``istantanea_ferma``): i file (cartelle ``packages``,
  ``www``, ``vmc_master_backup``, ``custom_components``), i file di ``.storage`` che
  contano (fra cui ``core.restore_state``: gli ultimi valori salvati alla fermata) e il
  registro storico SQLite (``states_meta``, righe per entità, ``statistics_meta``).
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any

from ha import ClientHA, ErroreHA

FILE_STORAGE = (
    "core.restore_state",
    "core.entity_registry",
    "core.device_registry",
    "core.config_entries",
    "lovelace",
    "lovelace_resources",
    "lovelace_dashboards",
    "repairs.issue_registry",
    "core.config",
)
CARTELLE = ("packages", "www", "vmc_master_backup", "custom_components")


async def notifiche(client: ClientHA) -> dict[str, Any]:
    """Le notifiche persistenti (campanella), come le riceve il frontend."""
    await client.collega_ws()
    assert client.ws is not None
    numero = next(client._id)
    await client.ws.send_json(
        {"id": numero, "type": "persistent_notification/subscribe"}
    )
    trovate: dict[str, Any] = {}
    fine = time.monotonic() + 10
    while time.monotonic() < fine:
        messaggio = await client.ws.receive_json(timeout=10)
        if messaggio.get("id") != numero:
            continue
        if messaggio.get("type") == "event":
            evento = messaggio["event"]
            if evento.get("type") in ("current", "added", "updated"):
                trovate.update(evento.get("notifications") or {})
            break
    with contextlib.suppress(ErroreHA):
        await client.ws_comando("unsubscribe_events", subscription=numero)
    return trovate


async def istantanea_viva(client: ClientHA, momento: str) -> dict[str, Any]:
    """Tutto quello che si vede con Home Assistant acceso."""
    stati = await client.stati()
    uscita: dict[str, Any] = {
        "momento": momento,
        "ora": time.time(),
        "stati": {s["entity_id"]: s for s in stati},
        "registro": await client.ws_comando("config/entity_registry/list"),
        "dispositivi": await client.ws_comando("config/device_registry/list"),
        "voci": await client.ws_comando("config_entries/get", domain="vmc_master"),
        "riparazioni": (await client.ws_comando("repairs/list_issues"))["issues"],
        "risorse": await client.ws_comando("lovelace/resources"),
        # i servizi delle VMC (comandi di shell e script del package: i nomi che usano
        # le automazioni dell'utente)
        "servizi": {
            voce["domain"]: sorted(s for s in voce["services"] if "vmc_" in s)
            for voce in await client.richiesta("GET", "/api/services")
            if voce["domain"] in ("shell_command", "script", "vmc_master")
        },
    }
    try:
        uscita["plancia"] = await client.ws_comando("lovelace/config")
    except ErroreHA as errore:
        uscita["plancia"] = {"errore": str(errore)}
    uscita["notifiche"] = await notifiche(client)
    return uscita


def _albero(cartella: Path) -> dict[str, dict[str, Any]]:
    """I file di una cartella (percorso relativo -> dimensione e md5)."""
    if not cartella.exists():
        return {}
    uscita: dict[str, dict[str, Any]] = {}
    for radice, cartelle, file in os.walk(cartella):
        cartelle[:] = [c for c in cartelle if c != "__pycache__"]
        for nome in file:
            percorso = Path(radice) / nome
            relativo = percorso.relative_to(cartella).as_posix()
            dati = percorso.read_bytes()
            uscita[relativo] = {
                "byte": len(dati),
                "md5": hashlib.md5(dati).hexdigest(),
            }
    return uscita


def _registro_storico(file_db: Path) -> dict[str, Any]:
    """Dal registro SQLite: ``states_meta`` (entity_id -> metadata_id), righe e istanti
    per metadata_id, ``statistics_meta``."""
    if not file_db.exists():
        return {}
    con = sqlite3.connect(f"file:{file_db}?mode=ro", uri=True)
    try:
        meta = dict(con.execute("SELECT entity_id, metadata_id FROM states_meta"))
        righe = {
            m: {"righe": n, "prima": p, "ultima": u}
            for m, n, p, u in con.execute(
                "SELECT metadata_id, COUNT(*), MIN(last_updated_ts), MAX(last_updated_ts)"
                " FROM states GROUP BY metadata_id"
            )
        }
        statistiche = {
            sid: {"id": i, "sorgente": s, "unita": u}
            for i, sid, s, u in con.execute(
                "SELECT id, statistic_id, source, unit_of_measurement FROM statistics_meta"
            )
        }
        righe_statistiche = dict(
            con.execute(
                "SELECT metadata_id, COUNT(*) FROM statistics GROUP BY metadata_id"
            )
        )
        righe_brevi = dict(
            con.execute(
                "SELECT metadata_id, COUNT(*) FROM statistics_short_term GROUP BY metadata_id"
            )
        )
    finally:
        con.close()
    return {
        "states_meta": meta,
        "righe": {str(k): v for k, v in righe.items()},
        "statistics_meta": statistiche,
        "righe_statistiche": {str(k): v for k, v in righe_statistiche.items()},
        "righe_statistiche_brevi": {str(k): v for k, v in righe_brevi.items()},
    }


def istantanea_ferma(config: Path, momento: str) -> dict[str, Any]:
    """Tutto quello che si legge con Home Assistant fermo."""
    storage: dict[str, Any] = {}
    cartella_storage = config / ".storage"
    for nome in (
        sorted(os.listdir(cartella_storage)) if cartella_storage.exists() else []
    ):
        if nome in FILE_STORAGE or nome.startswith("vmc_master"):
            with contextlib.suppress(ValueError, OSError):
                storage[nome] = json.loads((cartella_storage / nome).read_text("utf-8"))
    return {
        "momento": momento,
        "ora": time.time(),
        "file": {c: _albero(config / c) for c in CARTELLE},
        "configuration_yaml": (config / "configuration.yaml").read_text("utf-8"),
        "storage_presenti": sorted(os.listdir(cartella_storage))
        if cartella_storage.exists()
        else [],
        "storage": storage,
        "registro_storico": _registro_storico(config / "home-assistant_v2.db"),
    }


def istantanea_file(config: Path, momento: str) -> dict[str, Any]:
    """Solo i file (si leggono anche con Home Assistant acceso)."""
    return {
        "momento": momento,
        "ora": time.time(),
        "file": {c: _albero(config / c) for c in CARTELLE},
    }


def salva(uscita: Path, nome: str, dati: dict[str, Any]) -> Path:
    uscita.mkdir(parents=True, exist_ok=True)
    file = uscita / f"{nome}.json"
    file.write_text(
        json.dumps(dati, ensure_ascii=False, indent=1, default=str), "utf-8"
    )
    return file


def leggi(uscita: Path, nome: str) -> dict[str, Any] | None:
    file = uscita / f"{nome}.json"
    if not file.exists():
        return None
    return json.loads(file.read_text("utf-8"))
