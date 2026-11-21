"""Prove della b36, verifica B delle allerte con Black-Out e ritorno della corrente (Umidità, Free, Calendario, velocità
dell'utente).

- BO-1: dopo il ritorno della corrente la VMC (che riparte a Velocità 1) aspetta 32 s il ripristino della velocità
  memorizzata dal Black-Out (Priorità 7, spie input_boolean.vmc_master_spia_velocita_*), ma la «Velocità Registrata» e i
  tasti della tastiera non la mostravano: la memoria del Black-Out non era tra le memorie lette dal sensore. Ora c'è
  (ultima riga, Priorità 7): la velocità da ripristinare compare come Velocità Registrata e il suo tasto si illumina con
  l'icona mdi:restore finché il ripristino non la conferma. Durante il Black-Out (VMC OFF-Line, ultima lettura uguale
  alla memoria) e con la VMC che riparte già alla velocità di prima non cambia nulla.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
SUFFISSI = ("0", "1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")
BLACK_OUT = [f"input_boolean.vmc_master_spia_velocita_{s}" for s in SUFFISSI]
LETTURA_I = "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia"
SPIA_U0 = "input_boolean.vmc_master_spia_umidita_velocita_0"
FREE_H = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating"
MESE = "sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling"


@lru_cache
def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _modello(eid: str, chiave: str = "state") -> str:
    for blocco in _pacchetto()["template"]:
        for tipo in ("sensor", "binary_sensor"):
            for ent in blocco.get(tipo, []) or []:
                if ent.get("default_entity_id") == eid:
                    return ent[chiave]
    raise AssertionError(eid)


def _registrata(hass: HomeAssistant, letta: str, accese: list[str], mese: str = "Disabilitata") -> str:
    tutte = BLACK_OUT + [SPIA_U0, FREE_H]
    for e in tutte:
        hass.states.async_set(e, "on" if e in accese else "off")
    hass.states.async_set(LETTURA_I, letta)
    hass.states.async_set(MESE, mese)
    hass.states.async_set("sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling", "Nessuna Allerta")
    return str(Template(_modello("sensor.vmc_master_velocita_registrata"), hass).async_render({})).strip()


@pytest.mark.parametrize(
    ("letta", "accese", "attesa"),
    [
        # ritorno della corrente: la VMC riparte a Velocità 1, il Black-Out ha memorizzato la Velocità 2
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_2"], "Velocità 2"),
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_notturna"], "Notturna"),
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_iperventilazione"], "Iperventilazione"),
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_freecooling"], "Free Heat./Cool."),
        # Umidità partita da Velocità 0 (memoria 0) e Black-Out a Velocità 2: le 2 velocità da ripristinare, in ordine di priorità
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_2", SPIA_U0], "Velocità 0 · Velocità 2"),
        # durante il Black-Out (ultima lettura = memoria) o con la VMC già alla velocità di prima: nessuna differenza
        ("Velocità 2", ["input_boolean.vmc_master_spia_velocita_2"], "Nessuna"),
        ("Velocità 0", ["input_boolean.vmc_master_spia_velocita_0"], "Nessuna"),
        # Black-Out a Velocità 0 con la VMC che riparte a Velocità 1
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_0"], "Velocità 0"),
        # velocità non leggibile: nessuna
        ("Non disponibile", ["input_boolean.vmc_master_spia_velocita_2"], "Nessuna"),
        # memoria Free (sospesa) e Black-Out a Velocità 0 con la VMC a Velocità 1 (Umidità, Nota 3): entrambe
        ("Velocità 1", ["input_boolean.vmc_master_spia_velocita_0", FREE_H], "Free Heating · Velocità 0"),
    ],
)
async def test_bo_1_velocita_registrata_mostra_la_memoria_del_black_out(hass: HomeAssistant, letta: str,
                                                                       accese: list[str], attesa: str) -> None:
    assert _registrata(hass, letta, accese) == attesa


async def test_bo_1_tasto_della_velocita_da_ripristinare(hass: HomeAssistant) -> None:
    """Il tasto della velocità memorizzata dal Black-Out si illumina con l'icona mdi:restore (template dei tasti invariati)."""
    reg = _registrata(hass, "Velocità 1", ["input_boolean.vmc_master_spia_velocita_3"])
    hass.states.async_set("sensor.vmc_master_velocita_registrata", reg)
    stato = Template(_modello("binary_sensor.vmc_master_tasto_velocita_3"), hass).async_render({})
    icona = Template(_modello("binary_sensor.vmc_master_tasto_velocita_3", "icon"), hass).async_render({})
    assert stato is True and str(icona).strip() == "mdi:restore"
    attivo = Template(_modello("binary_sensor.vmc_master_tasto_velocita_1", "icon"), hass).async_render({})
    assert str(attivo).strip() == "mdi:numeric-1-box"


def test_bo_1_riga_black_out_ultima_e_file_crlf() -> None:
    dati = (PKG / "vmc_master.yaml").read_bytes()
    assert dati.count(b"\r\n") == dati.count(b"\n")
    testo = dati.decode("utf-8").replace("\r\n", "\n")
    modello = _modello("sensor.vmc_master_velocita_registrata")
    righe = [r.strip() for r in modello.split("\n") if r.strip().startswith("['")]
    assert righe[-1] == "['Black-Out', 'input_boolean.vmc_master_spia_velocita_{}', nomi.keys() | list]"
    assert righe[-2].startswith("['Umidità', ") and righe[-2].endswith(",")
    assert "['Black-Out', 'input_boolean.vmc_master_spia_velocita_{}', nomi.keys() | list]" in testo
