"""Prove della 9.0.0b39: i cicli di conferma escono se la velocità della VMC non si legge da 32 s con una Fascia del
Calendario in corso.

Durante una Fascia il Black-Out rilevato non si accende mai (i suoi 11 casi chiedono le 14 spie del Calendario spente):
un ciclo di conferma di un'allerta (PdR, Inquinanti, Congelamento, Δ Temp., Free, interruttori) con la VMC OFF-Line o con
la porta 5001 muta girava finché la VMC non tornava, con la coda dell'automazione ferma e il comando vecchio mandato al
ritorno. Scelta del proprietario (21-11-2026): l'uscita dei 32 s del Foglio A27 N.B. vale per tutti i cicli che possono
girare in una Fascia. La b39 la mette in tutta la classe: i 134 cicli che possono partire anche in Fascia e i 58 fuori
Fascia (ripristino dopo il Black-Out e Umidità) dove una Fascia può iniziare mentre il ciclo gira. La condizione chiede
una Fascia in corso: fuori Fascia è sempre falsa e i cicli restano quelli della b38 (ferma il Black-Out rilevato).
I cicli del Calendario hanno già la loro uscita (b34-b36) e non cambiano."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.util import yaml as hay

from custom_components.vmc_master import trasforma

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"
GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")
SPIE_FASCIA = tuple(f"input_boolean.vmc_master_spia_calendario_{g}_{n}" for g in GIORNI for n in (1, 2))
FASCIA = " or ".join(f"is_state('{s}', 'on')" for s in SPIE_FASCIA)
LETTURA_PERSA_IN_FASCIA = (
    "(is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - "
    "states.sensor.vmc_master_status_ventola.last_changed).total_seconds() >= "
    "states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32) and (" + FASCIA + "))")
LETTURA_PERSA = (
    "(is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - "
    "states.sensor.vmc_master_status_ventola.last_changed).total_seconds() >= "
    "states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32))")
BLACK_OUT = "is_state('binary_sensor.vmc_master_black_out_rilevato', 'on')"
COMANDO = re.compile(r"^shell_command\.vmc_master_(velocita_[0-4]|notturna|freecooling|iperventilazione|\{\{.*\}\})$")
CALENDARIO = re.compile(r"[Cc]alendario|^[12]° \w+ Off$")


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


_CACHE: dict[str, Any] = {}


def _automazione() -> dict[str, Any]:
    if "a" not in _CACHE:
        _CACHE["a"] = hay.parse_yaml(_testo("vmc_master_automazione.txt"))
    return _CACHE["a"]


def _nodi(nodo: Any) -> Iterator[Any]:
    yield nodo
    if isinstance(nodo, dict):
        for v in nodo.values():
            yield from _nodi(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _nodi(v)


def _ha_comando(sequenza: Any) -> bool:
    return any(isinstance(n, dict) and isinstance(n.get("action"), str) and COMANDO.match(n["action"].strip())
               for n in _nodi(sequenza))


def _cicli() -> Iterator[tuple[str, str]]:
    """(id dei trigger del ramo, testo dell'until) per ogni ciclo dell'automazione che manda un comando alla VMC."""
    for blocco in _automazione()["actions"]:
        for ramo in (blocco.get("choose") or []) if isinstance(blocco, dict) else []:
            ids = [str(i) for n in _nodi(ramo.get("conditions", [])) if isinstance(n, dict)
                   and n.get("condition") == "trigger" for i in (n["id"] if isinstance(n["id"], list) else [n["id"]])]
            for n in _nodi(ramo):
                if isinstance(n, dict) and isinstance(n.get("repeat"), dict) and _ha_comando(n["repeat"]["sequence"]):
                    fine = n["repeat"]["until"]
                    assert isinstance(fine, list) and len(fine) == 1
                    yield ",".join(ids), str(fine[0]["value_template"])


# ------------------------------------------------------------------ versioni
def test_versioni_b39() -> None:
    """L'automazione e il manifest cambiano nella b39 (la VER. di un file cambia solo quando cambia il file)."""
    trovata = re.search(r"AUTOMAZIONE VMC HELTY FLOW PLUS RELEASE \[VER\. 9\.0\.0b(\d+)\]",
                        _testo("vmc_master_automazione.txt")[:1000])
    assert trovata and int(trovata.group(1)) >= 39
    manifest = json.loads((PKG.parent / "manifest.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"9\.0\.0b(\d+)", manifest["version"]) and int(manifest["version"].split("b")[1]) >= 39


# ------------------------------------------------------------------ classe: tutti i cicli
def test_ogni_ciclo_esce_anche_con_la_lettura_persa() -> None:
    """Tutti i 210 cicli di conferma dell'automazione hanno un'uscita per la velocità non leggibile da 32 s: i 18 del
    Calendario senza condizioni (b34-b36), gli altri 192 solo con una Fascia in corso, subito dopo il Black-Out."""
    cicli = list(_cicli())
    assert len(cicli) == 210
    calendario = [(i, t) for i, t in cicli if any(CALENDARIO.search(x) for x in i.split(","))]
    altri = [(i, t) for i, t in cicli if (i, t) not in calendario]
    assert (len(calendario), len(altri)) == (18, 192)
    for ids, testo in calendario:
        assert LETTURA_PERSA in testo and LETTURA_PERSA_IN_FASCIA not in testo, ids
    for ids, testo in altri:
        assert testo.count(BLACK_OUT + " or " + LETTURA_PERSA_IN_FASCIA) == 1, ids
        assert testo.rstrip().endswith(LETTURA_PERSA_IN_FASCIA + " }}"), ids  # ultima uscita, in OR con le altre


def test_le_spie_della_fascia_sono_quelle_che_spengono_il_black_out() -> None:
    """Le 14 spie della condizione sono esattamente quelle che tutti gli 11 casi del Black-Out rilevato chiedono spente:
    con una di loro accesa il Black-Out non si accende e serve l'uscita della b39; con tutte spente la ferma il
    Black-Out e la condizione nuova è falsa (fuori Fascia nulla cambia)."""
    yaml = trasforma.rimuovi_sezioni_solo_master(_testo("vmc_master.yaml").replace("\r\n", "\n"))
    sensori = [s for blocco in hay.parse_yaml(yaml)["template"] for s in blocco.get("binary_sensor", [])]
    (black_out,) = [s for s in sensori if s.get("unique_id") == "vmc_master_black_out_rilevato"]
    casi = re.split(r"\{%-? set t\d+ = ", str(black_out["state"]))[1:]
    assert len(casi) == 11
    for caso in casi:
        spente = set(re.findall(r"states\('(input_boolean\.vmc_master_spia_calendario_\w+?_[12])'\)\s*==\s*'off'", caso))
        assert spente == set(SPIE_FASCIA)


# ------------------------------------------------------------------ comportamento della condizione
async def test_uscita_solo_in_fascia_e_dopo_32_secondi(hass: HomeAssistant, freezer) -> None:
    """La condizione nuova (valutata con il motore dei template di Home Assistant su un until vero dell'automazione):
    vera solo con la velocità non leggibile da almeno 32 s E una Fascia in corso; con 31 s, fuori Fascia o con la
    velocità leggibile è falsa e il ciclo continua come nella b38."""
    ids, testo = next((i, t) for i, t in _cicli() if i.startswith("PdR Vel. 1->"))
    fine = Template(testo, hass)
    hass.states.async_set("input_number.vmc_master_attesa_blackout_rilevazione", "32")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set("sensor.vmc_master_status_ventola_lettura_codice_interpretato", "Velocità 1")
    for spia in SPIE_FASCIA:
        hass.states.async_set(spia, "off")

    def esce(vel_prima: str = "Velocità 1") -> bool:
        return result_as_boolean(fine.async_render({"vel_prima_del_comando": vel_prima}))

    hass.states.async_set("sensor.vmc_master_status_ventola", "VMGH,1,0")
    assert esce() is False
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=31))
    assert esce() is False
    freezer.tick(timedelta(seconds=30))  # 61 s senza lettura, ma fuori Fascia: lo ferma solo il Black-Out (b38)
    assert esce() is False
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_mercoledi_2", "on")
    assert esce() is True
    hass.states.async_set("sensor.vmc_master_status_ventola", "VMGH,1,0")  # lettura tornata: il ciclo continua
    assert esce() is False
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=31))
    assert esce() is False
    freezer.tick(timedelta(seconds=1))
    assert esce() is True


@pytest.mark.parametrize("spia", SPIE_FASCIA)
async def test_ogni_spia_della_fascia_apre_l_uscita(hass: HomeAssistant, freezer, spia: str) -> None:
    """Ognuna delle 14 spie da sola basta (l'uscita vale per tutte e due le Fasce di tutti i giorni)."""
    _, testo = next((i, t) for i, t in _cicli() if i.startswith("Delta Temp.") or "delta" in i.lower())
    fine = Template(testo, hass)
    hass.states.async_set("input_number.vmc_master_attesa_blackout_rilevazione", "32")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set("sensor.vmc_master_status_ventola_lettura_codice_interpretato", "Non disponibile")
    for s in SPIE_FASCIA:
        hass.states.async_set(s, "on" if s == spia else "off")
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=32))
    assert result_as_boolean(fine.async_render({"vel_prima_del_comando": "Velocità 2"})) is True
