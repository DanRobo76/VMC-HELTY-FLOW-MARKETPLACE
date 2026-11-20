"""Prove della 9.0.0b34, Calendario e Countdown (rilievi B1-1, B1-3, B1-4, B1-5, B1-6, B1-7 della verifica profonda
della b33).

B1-1: il ciclo «ripeti finche' la VMC conferma» del Calendario non finiva se la VMC risponde al ping ma la porta 5001
non risponde (velocita' letta sempre quella di prima, nessun OFF-Line): l'automazione principale (in coda) restava
ferma. Ora tutti i cicli del Calendario (360 negli script di Fascia, 14 nei rami «Off») escono anche quando la lettura
della velocita' (sensore TCP, «unavailable» a ogni lettura fallita) manca da quanto dura la rilevazione del Black-Out.
Nessun tempo nuovo: si usa la stessa attesa della rilevazione del Black-Out."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
FASCE = ("vmc_master_calendario_fascia_1_on", "vmc_master_calendario_fascia_2_on")
TCP = "sensor.vmc_master_status_ventola"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
ATTESA = "input_number.vmc_master_attesa_blackout_rilevazione"
LETTURA_PERSA = (f"(is_state('{TCP}', 'unavailable') and (now() - states.{TCP}.last_changed).total_seconds() >= "
                 f"states('{ATTESA}') | int(32))")


def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _cicli(nodo: Any) -> Iterator[dict[str, Any]]:
    if isinstance(nodo, dict):
        if "repeat" in nodo:
            yield nodo["repeat"]
        for valore in nodo.values():
            yield from _cicli(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _cicli(valore)


def _cicli_calendario() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """I cicli degli script di Fascia e quelli dei rami «Off» (1°/2° giorno Off) dell'automazione."""
    script = _pacchetto()["script"]
    fasce = [c for nome in FASCE for c in _cicli(script[nome]["sequence"])]
    rami = [r for b in _automazione()["actions"] if "choose" in b for r in b["choose"]]
    off = [c for r in rami
           if isinstance(r["conditions"][0].get("id"), str) and r["conditions"][0]["id"].endswith(" Off")
           and r["conditions"][0]["id"][:2] in ("1°", "2°")
           for c in _cicli(r["sequence"])]
    return fasce, off


# ------------------------------------------------------------------------------------------------------------ B1-1
def test_b1_1_tutti_i_cicli_del_calendario_escono_con_la_lettura_persa() -> None:
    fasce, off = _cicli_calendario()
    assert len(fasce) == 360 and len(off) == 14
    for ciclo in fasce + off:
        (fine,) = ciclo["until"]
        assert fine["value_template"].endswith(f" or {LETTURA_PERSA} }}}}"), fine["value_template"][-200:]
        assert "lettura della velocità persa per il tempo di rilevazione del Black-Out" in fine["alias"]
    # nessun altro ciclo ha la nuova uscita: 360 nel package, 14 nell'automazione, in tutto 374
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    automazione = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    assert pacchetto.count(LETTURA_PERSA) == 360
    assert automazione.count(LETTURA_PERSA) == 14


def test_b1_1_il_sensore_letto_e_quello_tcp() -> None:
    """La condizione legge il sensore TCP della porta 5001 (che da HA 2026.x diventa «unavailable» a ogni lettura
    fallita), non la sua copia «memorizzata» che conserva l'ultimo valore."""
    tcp = next(s for s in _pacchetto()["sensor"] if s.get("name") == "vmc_master_status_ventola")
    assert tcp["platform"] == "tcp" and tcp["port"] == 5001 and tcp["payload"] == "VMGH?"


def _until_fascia() -> str:
    fasce, _ = _cicli_calendario()
    return next(c["until"][0]["value_template"] for c in fasce
                if c["sequence"][0]["action"] == "shell_command.vmc_master_velocita_2")


@pytest.mark.parametrize(
    ("stato_tcp", "secondi_fa", "attesa", "atteso"),
    [
        (None, 0, "32.0", "False"),  # sensore TCP inesistente: nessun errore
        ("0102", 100, "32.0", "False"),  # lettura valida
        ("unavailable", 10, "32.0", "False"),  # lettura persa da poco (disturbo): si continua a ripetere
        ("unavailable", 40, "32.0", "True"),  # lettura persa da almeno 32 s: il ciclo finisce
        ("unavailable", 40, "60.0", "False"),  # stessa attesa della rilevazione del Black-Out
        ("unavailable", 40, "unknown", "True"),  # attesa non disponibile: riserva 32 s
        ("unknown", 40, "32.0", "False"),
    ],
)
async def test_b1_1_uscita_dal_ciclo(hass, stato_tcp, secondi_fa, attesa, atteso) -> None:
    from homeassistant.helpers.template import Template

    hass.states.async_set(LETTURA, "Velocità 0")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set(ATTESA, attesa)
    if stato_tcp is not None:
        hass.states.async_set(TCP, stato_tcp, timestamp=time.time() - secondi_fa)
    reso = Template(_until_fascia(), hass).async_render({"vel_prima_del_comando": "Velocità 0"}, parse_result=False)
    assert reso == atteso
