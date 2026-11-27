"""Le tabelle native sono quelle del package e coprono tutti i modelli portati."""

from __future__ import annotations

from custom_components.vmc_master.nativa import tabelle
from custom_components.vmc_master.nativa.memoria import GIORNI_DATI, MEDIE
from custom_components.vmc_master.nativa.modelli import MODELLI

from .genera_tabelle import contenuto


def test_tabelle_aggiornate() -> None:
    """tabelle.py è esattamente quello che scrive il generatore dal package della b42."""
    with open(tabelle.__file__, encoding="utf-8") as file:
        assert file.read() == contenuto(), "rigenerare con: python -m tests.nativa.genera_tabelle"


def test_conteggi() -> None:
    """136 sensori (120 modelli, 10 con memoria, 4 letture, ping, versione) e 273 helper."""
    tipi: dict[str, int] = {}
    for voce in tabelle.SENSORI.values():
        tipi[voce["tipo"]] = tipi.get(voce["tipo"], 0) + 1
    assert tipi == {"modello": 120, "memoria": 10, "lettura": 4, "ping": 1, "versione": 1}
    domini: dict[str, int] = {}
    for chiave in tabelle.IMPOSTAZIONI:
        dominio = chiave.split(".")[0]
        domini[dominio] = domini.get(dominio, 0) + 1
    assert domini == {
        "input_boolean": 115,
        "input_number": 43,
        "input_select": 15,
        "input_text": 36,
        "input_datetime": 30,
        "timer": 34,
    }


def test_ogni_modello_portato() -> None:
    """Ogni sensore calcolato del package ha il suo modello Python, e solo quelli."""
    modelli = {k for k, v in tabelle.SENSORI.items() if v["tipo"] == "modello"}
    assert set(MODELLI) == modelli


def test_icone_calcolate() -> None:
    """Icona None nella tabella = template di icona = funzione icona nel modello."""
    for chiave, voce in tabelle.SENSORI.items():
        if voce["tipo"] != "modello":
            continue
        calcolata = "icona" in voce and voce["icona"] is None
        assert calcolata == (MODELLI[chiave].icona is not None), chiave


def test_memoria() -> None:
    """I 10 sensori con memoria sono le 3 letture memorizzate, le 6 medie e i giorni di dati."""
    memoria = {k for k, v in tabelle.SENSORI.items() if v["tipo"] == "memoria"}
    attese = {f"sensor.{n}_memorizzata" for n in ("status_ventola", "sensori", "nome")}
    attese |= {k for k, _, _ in MEDIE} | {GIORNI_DATI}
    assert memoria == attese


def test_domani() -> None:
    """DOMANI: la colonna «Domani» della fase 1 per le 342 voci del package (aiutanti,
    script e shell_command): 172 impostazioni visibili, 34 timer come sensori, 25
    pulsanti, 108 interne e 3 tolte (b46: il campo dell'IP, il suo esito e il comando che
    scriveva l'IP)."""
    coppie: dict[tuple[str, str], int] = {}
    for chiave, dominio in tabelle.DOMANI.items():
        coppia = (chiave.split(".")[0], dominio)
        coppie[coppia] = coppie.get(coppia, 0) + 1
    assert coppie == {
        ("input_boolean", "binary_sensor"): 77,
        ("input_boolean", "interna"): 1,
        ("input_boolean", "switch"): 37,
        ("input_datetime", "time"): 30,
        ("input_number", "interna"): 32,
        ("input_number", "number"): 10,
        ("input_number", "sensor"): 1,
        ("input_select", "select"): 14,
        ("input_select", "sensor"): 1,
        ("input_text", "interna"): 34,
        ("input_text", "sensor"): 1,
        ("input_text", "text"): 1,
        ("input_text", "tolta"): 2,
        ("script", "button"): 13,
        ("script", "interna"): 38,
        ("shell_command", "button"): 12,
        ("shell_command", "interna"): 3,
        ("shell_command", "tolta"): 1,
        ("timer", "sensor"): 34,
    }
    assert set(tabelle.IMPOSTAZIONI) <= set(tabelle.DOMANI)


def test_pulsanti() -> None:
    """25 pulsanti (fase 4): i 13 script e i 12 comandi di shell che la scheda chiama,
    ognuno con l'oggetto dello script o del comando di oggi."""
    tipi: dict[str, int] = {}
    for voce in tabelle.PULSANTI.values():
        tipi[voce["tipo"]] = tipi.get(voce["tipo"], 0) + 1
    assert tipi == {"script": 13, "comando": 12}
    assert all(
        voce["nome"].startswith("VMC {Nome} - ") for voce in tabelle.PULSANTI.values()
    )
