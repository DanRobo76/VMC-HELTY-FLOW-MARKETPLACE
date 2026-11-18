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

import yaml

from .const import NOME_MASTER, NOME_RE
from .trasforma import (
    adatta_link_repository,
    adatta_versione,
    package_per_vmc,
    per_vmc,
    script_cambio_ip_per_vmc,
    script_cambio_nome_per_vmc,
)

_LOGGER = logging.getLogger(__name__)

_SORGENTI = Path(__file__).parent / "package"
FILE_MARCATORE = ".vmc_master_integrazione.json"
CARTELLA_BACKUP = "vmc_master_backup"
# Sottocartella di CARTELLA_BACKUP per i file del package modificati a mano
SUFFISSO_MODIFICATI = "modificati"

# Prima riga «host:» del package: e' l'IP della VMC (sensori TCP)
_RE_HOST = re.compile(r"^\s+host:\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", re.MULTILINE)

# Parti del package che Home Assistant sa ricaricare senza riavvio: chiave -> servizio.
# «shell_command» non ha un servizio di ricarica: un suo cambio chiede il riavvio.
SERVIZI_RICARICA = {
    "automation": "automation.reload",
    "command_line": "command_line.reload",
    "homeassistant": "homeassistant.reload_core_config",
    "input_boolean": "input_boolean.reload",
    "input_datetime": "input_datetime.reload",
    "input_number": "input_number.reload",
    "input_select": "input_select.reload",
    "input_text": "input_text.reload",
    "script": "script.reload",
    "template": "template.reload",
    "timer": "timer.reload",
}
# Sensori della chiave «sensor:» che si ricaricano: piattaforma -> servizio.
# I sensori TCP e la chiave «recorder:» vogliono il riavvio.
SERVIZI_RICARICA_SENSORI = {
    "command_line": "command_line.reload",
    "rest": "rest.reload",
    "template": "template.reload",
}

_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


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


def genera_file(nome: str, ip: str, versione: str) -> dict[str, str]:
    """Contenuto di tutti i file del package della VMC indicata."""
    yaml_master = _leggi(_SORGENTI / "vmc_master.yaml")
    automazione = _leggi(_SORGENTI / "vmc_master_automazione.txt")
    # Gli script .sh vanno sempre scritti con fine riga LF (come dopo «rimuovi caratteri di ritorno»)
    script_ip = _leggi(_SORGENTI / "vmc_master_script_cambio_ip.sh").replace("\r\n", "\n")
    script_nome = _leggi(_SORGENTI / "vmc_master_script_cambio_nome.sh").replace("\r\n", "\n")
    return {
        f"vmc_{nome}.yaml": adatta_link_repository(
            adatta_versione(package_per_vmc(yaml_master, nome, ip), versione)
        ),
        f"vmc_{nome}_automazione.yaml": automazione_come_package(
            adatta_link_repository(per_vmc(automazione, nome, ip)), nome
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


def nome_manuale_con_ip(config_dir: str, ip: str) -> str | None:
    """Nome della VMC installata a mano (release 8.6.0) che usa questo IP, se c'e'."""
    radice = Path(config_dir) / "packages" / "vmc_helty_flow"
    if not radice.is_dir():
        return None
    for cartella in sorted(radice.iterdir()):
        nome = cartella.name
        if (
            NOME_RE.fullmatch(nome)
            and installazione_manuale(config_dir, nome)
            and ip_nel_package(config_dir, nome) == ip
        ):
            return nome
    return None


def leggi_marcatore(config_dir: str, nome: str) -> dict:
    percorso = cartella_vmc(config_dir, nome) / FILE_MARCATORE
    try:
        return json.loads(_leggi(percorso))
    except (OSError, ValueError):
        return {}


def _cartella_backup(config_dir: str, nome: str, tipo: str = "") -> Path:
    data_ora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    parti = [nome, tipo, data_ora] if tipo else [nome, data_ora]
    return Path(config_dir) / CARTELLA_BACKUP / "_".join(parti)


def _rimetti_ip(testo: str, ip: str, ip_scritto: str) -> str:
    """Testo con l'IP originale al posto di quello scritto dal campo «Cambia IP VMC»."""
    return re.sub(rf"(?<![0-9.]){re.escape(ip)}(?![0-9])", ip_scritto, testo)


def modificato_a_mano(testo: str, md5_scritto: object, ip: str, ip_scritto: object) -> bool:
    """True se il file non e' piu' quello scritto dall'integrazione (md5 del marcatore).

    Non conta come modifica l'IP cambiato dal campo «Cambia IP VMC» della scheda: lo script
    sostituisce l'IP in tutto il file, quindi rimettendo quello vecchio torna l'md5 scritto.
    Senza md5 nel marcatore non si puo' sapere: il file si aggiorna come sempre.
    """
    if not isinstance(md5_scritto, str) or _md5(testo) == md5_scritto:
        return False
    if isinstance(ip_scritto, str) and ip_scritto and ip != ip_scritto:
        if _md5(_rimetti_ip(testo, ip, ip_scritto)) == md5_scritto:
            return False
    return True


def sposta_in_backup(config_dir: str, nome: str) -> Path | None:
    """Sposta la cartella della VMC fuori da «packages» (non viene piu' caricata)."""
    cartella = cartella_vmc(config_dir, nome)
    if not cartella.is_dir():
        return None
    destinazione = _cartella_backup(config_dir, nome)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(cartella), str(destinazione))
    _LOGGER.info("Cartella %s spostata in %s", cartella, destinazione)
    return destinazione


def _per_piattaforma(sensori: object) -> dict[object, list] | None:
    if sensori is None:
        return {}
    if not isinstance(sensori, list) or not all(isinstance(s, dict) for s in sensori):
        return None
    gruppi: dict[object, list] = {}
    for sensore in sensori:
        gruppi.setdefault(sensore.get("platform"), []).append(sensore)
    return gruppi


def _ricariche_sensori(prima: object, dopo: object) -> set[str] | None:
    gruppi_prima, gruppi_dopo = _per_piattaforma(prima), _per_piattaforma(dopo)
    if gruppi_prima is None or gruppi_dopo is None:
        return None
    servizi: set[str] = set()
    for piattaforma in gruppi_prima.keys() | gruppi_dopo.keys():
        if gruppi_prima.get(piattaforma) == gruppi_dopo.get(piattaforma):
            continue
        if piattaforma not in SERVIZI_RICARICA_SENSORI:
            return None
        servizi.add(SERVIZI_RICARICA_SENSORI[piattaforma])
    return servizi


def _solo_esclusioni_tolte(prima: object, dopo: object, nuovo: str) -> bool:
    """«recorder:» cambiato solo perche' dall'elenco delle entita' escluse sono uscite
    entita' che il package non definisce piu' (per esempio la Finestra Prima Installazione
    VMC): non c'e' niente da applicare, quindi non serve il riavvio."""
    if not isinstance(prima, dict) or not isinstance(dopo, dict):
        return False
    escl_prima, escl_dopo = prima.get("exclude"), dopo.get("exclude")
    if not isinstance(escl_prima, dict) or not isinstance(escl_dopo, dict):
        return False
    entita_prima = escl_prima.get("entities") or []
    entita_dopo = escl_dopo.get("entities") or []
    if not isinstance(entita_prima, list) or not isinstance(entita_dopo, list):
        return False
    tolte = [e for e in entita_prima if e not in entita_dopo]
    if [e for e in entita_prima if e in entita_dopo] != entita_dopo:
        return False  # entita' aggiunte o riordinate
    if {k: v for k, v in prima.items() if k != "exclude"} != {
        k: v for k, v in dopo.items() if k != "exclude"
    }:
        return False
    if {k: v for k, v in escl_prima.items() if k != "entities"} != {
        k: v for k, v in escl_dopo.items() if k != "entities"
    }:
        return False
    # le entita' tolte non devono comparire da nessun'altra parte del nuovo package
    return all(isinstance(e, str) and e.split(".", 1)[-1] not in nuovo for e in tolte)


def ricariche_necessarie(vecchio: str, nuovo: str) -> set[str] | None:
    """Servizi che applicano le modifiche di un file del package senza riavvio.

    Si confronta il contenuto YAML chiave per chiave, quindi i commenti non contano.
    None vuol dire che serve il riavvio (per esempio IP cambiato nei sensori TCP).
    """
    try:
        prima = yaml.load(vecchio, Loader=_LOADER) or {}
        dopo = yaml.load(nuovo, Loader=_LOADER) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(prima, dict) or not isinstance(dopo, dict):
        return None
    servizi: set[str] = set()
    for chiave in prima.keys() | dopo.keys():
        if prima.get(chiave) == dopo.get(chiave):
            continue
        if chiave in SERVIZI_RICARICA:
            servizi.add(SERVIZI_RICARICA[chiave])
        elif chiave == "recorder" and _solo_esclusioni_tolte(
            prima.get(chiave), dopo.get(chiave), nuovo
        ):
            continue
        elif chiave == "sensor":
            sensori = _ricariche_sensori(prima.get(chiave), dopo.get(chiave))
            if sensori is None:
                return None
            servizi |= sensori
        else:
            return None
    return servizi


@dataclass
class EsitoInstallazione:
    """Cosa e' cambiato su disco e come renderlo attivo."""

    file_scritti: list[str] = field(default_factory=list)
    backup: Path | None = None
    # File modificati a mano dopo l'ultima scrittura: la loro copia e' in «backup_modificati»
    file_modificati: list[str] = field(default_factory=list)
    backup_modificati: Path | None = None
    # File nuovi o parti che Home Assistant non sa ricaricare
    riavvio_necessario: bool = False
    # Servizi che ricaricano le parti cambiate, se il riavvio non serve
    ricariche: set[str] = field(default_factory=set)


def _salva_modificati(config_dir: str, nome: str, modificati: dict[str, str]) -> Path:
    """Copia i file modificati a mano fuori da «packages» (cosi' non vengono caricati)."""
    destinazione = _cartella_backup(config_dir, nome, SUFFISSO_MODIFICATI)
    destinazione.mkdir(parents=True, exist_ok=True)
    for nome_file, testo in modificati.items():
        _scrivi(destinazione / nome_file, testo)
    _LOGGER.warning(
        "VMC %s: file modificati a mano %s, copia salvata in %s",
        nome,
        ", ".join(modificati),
        destinazione,
    )
    return destinazione


def installa(config_dir: str, nome: str, ip: str, versione: str) -> EsitoInstallazione:
    """Scrive solo i file che sono cambiati; un'installazione manuale va prima in backup.

    Un file modificato a mano dopo l'ultima scrittura (md5 diverso da quello del
    marcatore) viene copiato in /config/vmc_master_backup prima di essere riscritto.
    """
    esito = EsitoInstallazione()
    if installazione_manuale(config_dir, nome):
        esito.backup = sposta_in_backup(config_dir, nome)
    cartella = cartella_vmc(config_dir, nome)
    cartella.mkdir(parents=True, exist_ok=True)
    nuovi = genera_file(nome, ip, versione)
    marcatore = leggi_marcatore(config_dir, nome)
    md5_scritti = marcatore.get("md5")
    if not isinstance(md5_scritti, dict):
        md5_scritti = {}
    vecchi = {
        nome_file: _leggi(cartella / nome_file)
        for nome_file in nuovi
        if (cartella / nome_file).is_file()
    }
    modificati = {
        nome_file: vecchio
        for nome_file, vecchio in vecchi.items()
        if vecchio != nuovi[nome_file]
        and modificato_a_mano(vecchio, md5_scritti.get(nome_file), ip, marcatore.get("ip"))
    }
    if modificati:
        esito.backup_modificati = _salva_modificati(config_dir, nome, modificati)
        esito.file_modificati = list(modificati)
    for nome_file, testo in nuovi.items():
        percorso = cartella / nome_file
        vecchio = vecchi.get(nome_file)
        if vecchio == testo:
            continue
        _scrivi(percorso, testo)
        esito.file_scritti.append(nome_file)
        if nome_file.endswith(".sh"):
            percorso.chmod(0o755)
            if vecchio is not None:
                continue  # gli script si leggono a ogni esecuzione: niente riavvio
        servizi = None if vecchio is None else ricariche_necessarie(vecchio, testo)
        if servizi is None:
            esito.riavvio_necessario = True
        else:
            esito.ricariche |= servizi
    marcatore = {
        "versione": versione,
        "nome": nome,
        "ip": ip,
        "master": nome == NOME_MASTER,
        "md5": {nome_file: _md5(testo) for nome_file, testo in nuovi.items()},
    }
    _scrivi(cartella / FILE_MARCATORE, json.dumps(marcatore, indent=2, ensure_ascii=False) + "\n")
    if esito.riavvio_necessario:
        esito.ricariche.clear()  # il riavvio carica gia' tutto
    if esito.file_scritti:
        _LOGGER.info("VMC %s: file aggiornati %s", nome, ", ".join(esito.file_scritti))
    return esito
