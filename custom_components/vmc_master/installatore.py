"""Installa e aggiorna il package di ogni VMC in /config/packages/vmc_helty_flow/<nome>.

I file sono generati da quelli della release 8.6.0 contenuti nella cartella «package»
dell'integrazione, con le stesse trasformazioni degli script Clona e Cambia IP
(vedere trasforma.py). L'automazione principale, che nella release 8.6.0 si incollava
a mano, diventa il file vmc_<nome>_automazione.yaml dello stesso package.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .const import NOME_MASTER
from .trasforma import (
    package_per_vmc,
    per_vmc,
    script_cambio_ip_per_vmc,
    script_cambio_nome_per_vmc,
)

_LOGGER = logging.getLogger(__name__)

_SORGENTI = Path(__file__).parent / "package"
FILE_MARCATORE = ".vmc_master_integrazione.json"
CARTELLA_BACKUP = "vmc_master_backup"

# Prima riga «host:» del package: e' l'IP della VMC (sensori TCP)
_RE_HOST = re.compile(r"^\s+host:\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", re.MULTILINE)


def _leggi(percorso: Path) -> str:
    # newline="" mantiene CRLF e LF esattamente come nei file originali
    with open(percorso, encoding="utf-8", newline="") as file:
        return file.read()


def _scrivi(percorso: Path, testo: str) -> None:
    with open(percorso, "w", encoding="utf-8", newline="") as file:
        file.write(testo)


def _md5(testo: str) -> str:
    return hashlib.md5(testo.encode("utf-8")).hexdigest()


def cartella_vmc(config_dir: str, nome: str) -> Path:
    return Path(config_dir) / "packages" / "vmc_helty_flow" / nome


def automazione_come_package(testo: str, nome: str) -> str:
    """L'automazione incollata a mano diventa un elemento della lista «automation:».

    Il testo resta identico: ogni riga e' solo spostata di 4 spazi a destra.
    L'id serve a Home Assistant per conservare le tracce (trace) dell'automazione.
    """
    a_capo = "\r\n" if "\r\n" in testo else "\n"
    righe = testo.splitlines(keepends=True)
    # Anche le righe di soli spazi vanno spostate: nei blocchi di testo (|, >) gli spazi contano
    corpo = "".join(r if r in ("\n", "\r\n") else "    " + r for r in righe)
    if not corpo.endswith(("\n", "\r\n")):
        corpo += a_capo
    return (
        f"# AUTOMAZIONE VMC {nome.upper()}: GENERATA DALL'INTEGRAZIONE VMC MASTER, NON MODIFICARE{a_capo}"
        f"automation:{a_capo}"
        f"  - id: automazione_vmc_{nome}{a_capo}"
        f"{corpo}"
    )


def genera_file(nome: str, ip: str) -> dict[str, str]:
    """Contenuto di tutti i file del package della VMC indicata."""
    yaml_master = _leggi(_SORGENTI / "vmc_master.yaml")
    automazione = _leggi(_SORGENTI / "vmc_master_automazione.txt")
    # Gli script .sh vanno sempre scritti con fine riga LF (come dopo «rimuovi caratteri di ritorno»)
    script_ip = _leggi(_SORGENTI / "vmc_master_script_cambio_ip.sh").replace("\r\n", "\n")
    script_nome = _leggi(_SORGENTI / "vmc_master_script_cambio_nome.sh").replace("\r\n", "\n")
    return {
        f"vmc_{nome}.yaml": package_per_vmc(yaml_master, nome, ip),
        f"vmc_{nome}_automazione.yaml": automazione_come_package(
            per_vmc(automazione, nome, ip), nome
        ),
        f"vmc_{nome}_script_cambio_ip.sh": script_cambio_ip_per_vmc(script_ip, nome, ip),
        f"vmc_{nome}_script_cambio_nome.sh": script_cambio_nome_per_vmc(script_nome, nome, ip),
    }


def ip_nel_package(config_dir: str, nome: str) -> str | None:
    """IP scritto nel package (puo' essere cambiato dal campo «Cambia IP VMC» della scheda)."""
    percorso = cartella_vmc(config_dir, nome) / f"vmc_{nome}.yaml"
    if not percorso.is_file():
        return None
    trovato = _RE_HOST.search(_leggi(percorso))
    return trovato.group(1) if trovato else None


def installazione_manuale(config_dir: str, nome: str) -> bool:
    """True se la cartella della VMC esiste ma non e' stata creata dall'integrazione."""
    cartella = cartella_vmc(config_dir, nome)
    return cartella.is_dir() and any(cartella.iterdir()) and not (cartella / FILE_MARCATORE).is_file()


def leggi_marcatore(config_dir: str, nome: str) -> dict:
    percorso = cartella_vmc(config_dir, nome) / FILE_MARCATORE
    try:
        return json.loads(_leggi(percorso))
    except (OSError, ValueError):
        return {}


def sposta_in_backup(config_dir: str, nome: str) -> Path | None:
    """Sposta la cartella della VMC fuori da «packages» (non viene piu' caricata)."""
    cartella = cartella_vmc(config_dir, nome)
    if not cartella.is_dir():
        return None
    destinazione = (
        Path(config_dir)
        / CARTELLA_BACKUP
        / f"{nome}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    )
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(cartella), str(destinazione))
    _LOGGER.info("Cartella %s spostata in %s", cartella, destinazione)
    return destinazione


@dataclass
class EsitoInstallazione:
    """Cosa e' cambiato su disco."""

    file_scritti: list[str] = field(default_factory=list)
    backup: Path | None = None

    @property
    def riavvio_necessario(self) -> bool:
        return bool(self.file_scritti)


def installa(config_dir: str, nome: str, ip: str, versione: str) -> EsitoInstallazione:
    """Scrive solo i file che sono cambiati; un'installazione manuale va prima in backup."""
    esito = EsitoInstallazione()
    if installazione_manuale(config_dir, nome):
        esito.backup = sposta_in_backup(config_dir, nome)
    cartella = cartella_vmc(config_dir, nome)
    cartella.mkdir(parents=True, exist_ok=True)
    nuovi = genera_file(nome, ip)
    for nome_file, testo in nuovi.items():
        percorso = cartella / nome_file
        if percorso.is_file() and _leggi(percorso) == testo:
            continue
        _scrivi(percorso, testo)
        if nome_file.endswith(".sh"):
            percorso.chmod(0o755)
        esito.file_scritti.append(nome_file)
    marcatore = {
        "versione": versione,
        "nome": nome,
        "ip": ip,
        "master": nome == NOME_MASTER,
        "md5": {nome_file: _md5(testo) for nome_file, testo in nuovi.items()},
    }
    _scrivi(cartella / FILE_MARCATORE, json.dumps(marcatore, indent=2, ensure_ascii=False) + "\n")
    if esito.file_scritti:
        _LOGGER.info("VMC %s: file aggiornati %s", nome, ", ".join(esito.file_scritti))
    return esito
