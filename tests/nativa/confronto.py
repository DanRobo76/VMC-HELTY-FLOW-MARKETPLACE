"""Strumenti per confrontare i modelli portati in Python con i modelli del package.

I modelli del package girano nel vero Home Assistant (integrazione template), con gli
stessi valori in ingresso dati alle funzioni Python: lo stato, l'icona, la disponibilita'
e gli attributi devono uscire identici.
"""

from __future__ import annotations

import json
import random
import re
import sys
import types
from functools import lru_cache
from pathlib import Path

from homeassistant.util.yaml.loader import parse_yaml

from . import extra

RADICE = Path(__file__).resolve().parents[2]
NOME = "master"
IP = "192.168.1.50"

RE_ID = re.compile(
    r"\b(input_boolean|input_number|input_select|input_text|input_datetime|timer|script|sensor|binary_sensor|automation)\.([a-z0-9_]+)\b"
)


def _installatore():
    if "vmc_master" not in sys.modules:
        pacchetto = types.ModuleType("vmc_master")
        pacchetto.__path__ = [str(RADICE / "custom_components" / "vmc_master")]
        sys.modules["vmc_master"] = pacchetto
    from vmc_master import installatore  # noqa: PLC0415

    return installatore


def versione_del_manifest() -> str:
    """La versione dell'integrazione (manifest.json): l'integrazione ibrida installa il
    package con questa (sensore «Package Ver.») e il modello in Python la legge da li'."""
    manifest = RADICE / "custom_components" / "vmc_master" / "manifest.json"
    return str(json.loads(manifest.read_text(encoding="utf-8"))["version"])


@lru_cache(maxsize=2)
def file_package(versione: str | None = None) -> dict[str, str]:
    """I file del package come li installa l'integrazione, con ``versione`` nel sensore
    «Package Ver.» (senza: quella del manifest.json, come l'integrazione ibrida)."""
    return _installatore().genera_file(NOME, IP, versione or versione_del_manifest())


@lru_cache(maxsize=2)
def package(versione: str | None = None) -> dict:
    return parse_yaml(file_package(versione)[f"vmc_{NOME}.yaml"])


@lru_cache(maxsize=1)
def modelli() -> dict[str, dict]:
    """entity_id -> {'dominio', 'conf', 'blocco'} per ogni sensore modello del package."""
    uscita: dict[str, dict] = {}
    for blocco in package()["template"]:
        for dominio in ("sensor", "binary_sensor"):
            for conf in blocco.get(dominio, []) or []:
                uscita[conf["default_entity_id"]] = {"dominio": dominio, "conf": conf, "blocco": blocco}
    return uscita


def testi_modello(conf: dict) -> list[str]:
    testi: list[str] = []

    def raccogli(valore):
        if isinstance(valore, str):
            testi.append(valore)
        elif isinstance(valore, dict):
            for v in valore.values():
                raccogli(v)
        elif isinstance(valore, list):
            for v in valore:
                raccogli(v)

    raccogli(conf)
    return testi


@lru_cache(maxsize=1)
def ingressi() -> list[str]:
    """entity_id letti dai modelli che non sono a loro volta sensori modello."""
    nomi = set(modelli())
    trovati: set[str] = set()
    for dati in modelli().values():
        for t in testi_modello(dati["conf"]):
            for d, o in RE_ID.findall(t):
                eid = f"{d}.{o}"
                if not o.startswith(f"vmc_{NOME}_"):
                    continue
                if o.endswith("_"):
                    # famiglia scritta con un modello: 'input_boolean.vmc_x_spia_' ~ nome
                    conf = package().get(d, {}) or {}
                    trovati.update(f"{d}.{k}" for k in conf if k.startswith(o))
                elif eid not in nomi:
                    trovati.add(eid)
    # i sensori modello con trigger si provano a parte: qui sono ingressi come gli altri
    con_trigger = {e for e, d in modelli().items() if "triggers" in d["blocco"]}
    return sorted((trovati - nomi) | con_trigger | extra.INGRESSI)


@lru_cache(maxsize=1)
def _testo_tutto() -> str:
    f = file_package()
    return f[f"vmc_{NOME}.yaml"] + f[f"vmc_{NOME}_automazione.yaml"]


def _letterali(eid: str) -> set[str]:
    """Valori confrontati con eid nel package (==, !=, in [...], is_state)."""
    testo = _testo_tutto()
    e = re.escape(eid)
    valori: set[str] = set()
    for m in re.finditer(rf"states\(\s*['\"]{e}['\"]\s*\)\s*(?:\|\s*(?:trim|lower|string)\s*)*(==|!=)\s*['\"]([^'\"]*)['\"]", testo):
        valori.add(m.group(2))
    for m in re.finditer(rf"states\(\s*['\"]{e}['\"]\s*\)\s*(?:\|\s*(?:trim|lower|string)\s*)*(?:not\s+)?in\s*\[([^\]]*)\]", testo):
        valori.update(re.findall(r"['\"]([^'\"]*)['\"]", m.group(1)))
    for m in re.finditer(rf"is_state\(\s*['\"]{e}['\"]\s*,\s*(\[[^\]]*\]|['\"][^'\"]*['\"])", testo):
        valori.update(re.findall(r"['\"]([^'\"]*)['\"]", m.group(1)))
    return valori


NUMERI = ["0", "1", "-5.5", "3", "8", "12.5", "21.3", "35", "50", "65.4", "80", "100", "600", "1250", "2500"]
GREZZI_VMGH = [f"VMGO,{v:05d},00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000" for v in range(8)]
GREZZI_VMGI = [
    "VMGI,00210,00100,00500,00600,00000,00000,00000,00000,00000,00000,00050,00000,00000,00000",
    "VMGI,00185,65486,00720,01250,00000,00000,00000,00000,00000,00000,00300,00000,00000,00000",
    "VMGI,00250,00320,00350,00450,00000,00000,00000,00000,00000,00000,00020,00000,00000,00000",
]
ESTERNI = ["sensor.esterno_uno", "sensor.esterno_due", "weather.casa"]


def attributi_fissi(eid: str) -> dict:
    """Attributi che le voci del package hanno sempre (min/max/passo, opzioni)."""
    dominio, _, oggetto = eid.partition(".")
    sezione = package().get(dominio)
    conf = sezione.get(oggetto) if isinstance(sezione, dict) else None
    if not isinstance(conf, dict):
        return {}
    if dominio == "input_number":
        return {"min": float(conf.get("min", 0)), "max": float(conf.get("max", 100)), "step": float(conf.get("step", 1))}
    if dominio == "input_select":
        return {"options": list(conf.get("options", []))}
    return {}


def attributi_esterni(rng: random.Random, eid: str) -> dict:
    if eid.startswith("weather."):
        return {
            "temperature": rng.choice([None, -3.5, 0, 12, 21.4, 33]),
            "humidity": rng.choice([None, 15, 48, 77.5, 100]),
        }
    return {}


@lru_cache(maxsize=None)
def candidati(eid: str) -> tuple[str, ...]:
    dominio, _, oggetto = eid.partition(".")
    valori = set(_letterali(eid))
    conf = package().get(dominio, {}) or {}
    c = conf.get(oggetto) if isinstance(conf, dict) else None
    if dominio == "input_boolean":
        valori |= {"on", "off"}
    elif dominio == "input_number" and isinstance(c, dict):
        mn, mx = float(c.get("min", 0)), float(c.get("max", 100))
        passo = float(c.get("step", 1))
        for x in (mn, mx, (mn + mx) / 2, mn + passo, mx - passo):
            x = max(mn, min(mx, x))
            valori.add(str(float(round(x / passo) * passo)) if passo else str(x))
        valori |= {n for n in NUMERI if mn <= float(n) <= mx}
    elif dominio == "input_select" and isinstance(c, dict):
        valori |= {str(o) for o in c.get("options", [])}
        if oggetto.startswith(f"vmc_{NOME}_selected_") and oggetto.endswith("_entity"):
            valori |= set(ESTERNI)
    elif dominio == "input_text":
        valori |= {"", "abc"}
        if "ip" in oggetto:
            valori |= {"192.168.1.50", "192.168.1.60", "10.0.0.7"}
    elif dominio == "input_datetime" and isinstance(c, dict):
        valori |= {"00:00:00", "06:30:00", "12:00:00", "18:45:00", "23:59:00"}
    elif dominio == "timer":
        valori |= {"idle", "active", "paused"}
    elif dominio in ("sensor", "binary_sensor"):
        if oggetto in (f"vmc_{NOME}_status_ventola", f"vmc_{NOME}_status_ventola_memorizzata"):
            valori |= set(GREZZI_VMGH)
        elif oggetto in (f"vmc_{NOME}_sensori", f"vmc_{NOME}_sensori_memorizzata"):
            valori |= set(GREZZI_VMGI)
        elif oggetto == f"vmc_{NOME}_status_ip":
            valori |= {"ON-Line", "OFF-Line"}
        elif oggetto in (f"vmc_{NOME}_nome", f"vmc_{NOME}_nome_memorizzata"):
            valori |= {"VMNM Master", "VMNM Sala", ""}
        elif oggetto == f"vmc_{NOME}_lan":
            valori |= {"VMSL,192,168,1,160", ""}
        elif dominio == "binary_sensor":
            valori |= {"on", "off"}
        else:
            valori |= set(NUMERI[:8])
    valori |= {"unknown", "unavailable"}
    valori |= extra.EXTRA.get(eid, set())
    return tuple(sorted(valori))


def campione(rng: random.Random, base: dict[str, str], quanti: int) -> dict[str, str]:
    """Copia di base con 'quanti' ingressi cambiati a caso tra i loro candidati."""
    nuovo = dict(base)
    for eid in rng.sample(sorted(base), min(quanti, len(base))):
        nuovo[eid] = rng.choice(candidati(eid))
    return nuovo


def base_iniziale(rng: random.Random) -> dict[str, str]:
    stati = {}
    for eid in ingressi():
        c = [v for v in candidati(eid) if v not in ("unknown", "unavailable")] or list(candidati(eid))
        stati[eid] = rng.choice(c)
    for eid in ESTERNI:
        stati[eid] = rng.choice(NUMERI + ["sunny", "rainy", "unknown"]) if eid.startswith("weather.") else rng.choice(NUMERI)
    return stati
