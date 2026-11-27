"""I 10 sensori con memoria in Python contro i template a trigger del Package.

- Letture memorizzate: i template a trigger veri girano in Home Assistant e ricevono
  le stesse letture del modello Python (cambi di stato, interruzioni, valori strani);
  stato e attributo devono coincidere a ogni passo. Il trigger di avvio si confronta
  rendendo il template con le stesse variabili.
- Medie e giorni di dati: i template rendono una risposta di recorder.get_statistics
  inventata (ore mancanti, ore senza media, bordi dei 28/56/84 giorni) a un'ora fissa.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
import os
import random

import pytest

from custom_components.vmc_master.nativa import memoria
from custom_components.vmc_master.nativa.memoria import (
    GIORNI_DATI,
    MEDIE,
    TRIGGER_AVVIO,
    TRIGGER_STATO,
    calcola_medie,
    come_stato,
    lettura_prima_dell_interruzione,
    memorizzata,
)
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component

from .confronto import GREZZI_VMGH, GREZZI_VMGI, NOME, package

GIRI = int(os.environ.get("VMC_GIRI", "400"))
SEME = int(os.environ.get("VMC_SEME", "20261125"))

LETTURE = {
    "status_ventola": GREZZI_VMGH,
    "sensori": GREZZI_VMGI,
    "nome": ["VMNM Master", "VMNM Sala", "VMNM 12"],
}
STRANI = [
    "unavailable",
    "unknown",
    "",
    " ",
    "None",
    "123",
    "1.50",
    "+3",
    "007",
    "True",
    "1,2",
    "[1]",
    "'testo'",
    "VMGO",
    "VMGO,00002\r\n",
    " VMNM Master ",
]


def _blocchi_memorizzati() -> dict[str, dict]:
    """lettura (status_ventola, sensori, nome) -> blocco a trigger del Package."""
    uscita = {}
    for blocco in package()["template"]:
        if "triggers" not in blocco:
            continue
        for conf in blocco.get("sensor", []) or []:
            eid = conf["default_entity_id"]
            if eid.endswith("_memorizzata"):
                lettura = eid.removeprefix(f"sensor.vmc_{NOME}_").removesuffix("_memorizzata")
                uscita[lettura] = blocco
    return uscita


def _stato(risultato) -> str | None:
    """Come un sensore template trasforma il risultato in stato (None = unknown)."""
    return None if risultato is None else str(risultato)


def test_come_stato() -> None:
    """Interpretazione del testo come Home Assistant (numeri, None, booleani, testi)."""
    assert come_stato("VMNM Master") == "VMNM Master"
    assert come_stato("1.50") == "1.5"
    assert come_stato("+3") == "3"
    assert come_stato("007") == "007"
    assert come_stato("1e5") == "1e5"
    assert come_stato("None") is None
    assert come_stato("True") == "True"
    assert come_stato("1,2") == "1,2"
    assert come_stato("'testo'") == "'testo'"
    assert come_stato("...") == "Ellipsis"
    assert come_stato("") == ""
    assert come_stato(".") == "."


async def test_come_stato_uguale_a_home_assistant(hass: HomeAssistant) -> None:
    """Per ogni testo di prova, lo stesso risultato del motore dei template."""
    for testo in [*STRANI, "1e5", "...", ".", "-0", "0.0", "00", "-", "b'x'", "{1: 2}", "1j", "3.", ".5"]:
        risultato = Template("{{ v }}", hass).async_render({"v": testo}, parse_result=True)
        if testo.strip() != testo:
            continue  # il motore toglie gli spazi prima: qui conta solo l'interpretazione
        assert come_stato(testo) == _stato(risultato), testo


@pytest.mark.parametrize("lettura", ["status_ventola", "sensori", "nome"])
async def test_memorizzate_uguali_ai_trigger(hass: HomeAssistant, freezer, lettura: str) -> None:
    """Stesse letture al template a trigger vero e al modello: stesso stato e attributo."""
    rng = random.Random(f"{SEME}-{lettura}")
    freezer.move_to("2026-11-25 10:00:00+00:00")
    sorgente = f"sensor.vmc_{NOME}_{lettura}"
    memorizzato = f"sensor.vmc_{NOME}_{lettura}_memorizzata"
    hass.states.async_set(sorgente, "unknown")
    blocco = _blocchi_memorizzati()[lettura]
    assert await async_setup_component(hass, "template", {"template": [blocco]})
    await hass.async_block_till_done()
    assert hass.states.get(memorizzato).state == "unknown"

    # Modello: stato del sensore memorizzato e suo last_changed.
    ricordata, cambiata = "unknown", hass.states.get(memorizzato).last_changed
    attributo: str | None = None
    precedente = "unknown"
    valori = LETTURE[lettura] + STRANI
    for giro in range(GIRI):
        freezer.tick(timedelta(seconds=rng.choice([1, 5, 5, 5, 30, 1227])))
        nuova = rng.choice(valori + [precedente] * 3)
        hass.states.async_set(sorgente, nuova)
        await hass.async_block_till_done()
        if nuova != precedente and nuova not in ("unavailable", "unknown"):
            testo = memorizzata(TRIGGER_STATO, nuova, nuova, ricordata)
            if lettura == "status_ventola":
                attributo = lettura_prima_dell_interruzione(
                    TRIGGER_STATO, precedente, ricordata, cambiata
                )
            stato = come_stato(testo)
            stato = "unknown" if stato is None else stato
            if stato != ricordata:
                ricordata, cambiata = stato, hass.states.get(memorizzato).last_changed
        precedente = nuova
        reale = hass.states.get(memorizzato)
        assert reale.state == ricordata, (giro, nuova)
        if lettura == "status_ventola" and attributo is not None:
            assert come_stato(attributo) == _stato(
                reale.attributes.get("lettura_prima_dell_interruzione")
            ) or (attributo == "" and reale.attributes.get("lettura_prima_dell_interruzione") == ""), (
                giro,
                attributo,
                reale.attributes,
            )
        assert reale.last_changed == cambiata, giro


@pytest.mark.parametrize("lettura", ["status_ventola", "sensori", "nome"])
async def test_memorizzate_avvio_uguale_al_template(hass: HomeAssistant, lettura: str) -> None:
    """Trigger di avvio: il template reso con le stesse variabili dà lo stesso risultato."""
    rng = random.Random(f"{SEME}-avvio-{lettura}")
    conf = _blocchi_memorizzati()[lettura]["sensor"][0]
    stato_tpl = Template(conf["state"], hass)
    attributo_tpl = (
        Template(conf["attributes"]["lettura_prima_dell_interruzione"], hass)
        if lettura == "status_ventola"
        else None
    )
    sorgente = f"sensor.vmc_{NOME}_{lettura}"
    valori = LETTURE[lettura] + STRANI
    for giro in range(GIRI):
        ora = rng.choice(valori)
        ricordata = rng.choice(valori)
        cambiata = datetime(2026, 11, 25, 9, 0, rng.randrange(60), rng.randrange(10**6), tzinfo=UTC)
        hass.states.async_set(sorgente, ora)
        this = State(f"{sorgente}_memorizzata", ricordata or "unknown", last_changed=cambiata)
        ricordata = this.state
        variabili = {"trigger": {"platform": TRIGGER_AVVIO, "event": "start"}, "this": this}
        atteso = _stato(stato_tpl.async_render(variabili, parse_result=True))
        assert come_stato(memorizzata(TRIGGER_AVVIO, None, ora, ricordata)) == atteso, (giro, ora, ricordata)
        if attributo_tpl is not None:
            atteso = attributo_tpl.async_render(variabili, parse_result=True)
            calcolato = lettura_prima_dell_interruzione(TRIGGER_AVVIO, None, ricordata, cambiata)
            assert (come_stato(calcolato) if calcolato else "") == (
                _stato(atteso) if atteso != "" else ""
            ), (giro, ricordata, calcolato, atteso)


def _risposta(rng: random.Random, adesso: datetime) -> dict:
    """Una risposta di recorder.get_statistics inventata, con casi ai bordi."""
    statistiche = {}
    for statistica in ("temp_interna_numeric", "hum_interna_numeric"):
        if rng.random() < 0.1:
            continue  # statistica assente
        ore = rng.choice([0, 1, 5, 24 * 3, 24 * 27, 24 * 28 + 1, 24 * 56 + 1, 24 * 84, 24 * 90])
        ultima = adesso.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
        righe = []
        for i in range(ore, 0, -1):
            if rng.random() < 0.05:
                continue  # ora mancante
            inizio = ultima - timedelta(hours=i - 1)
            riga = {"start": inizio.isoformat(), "end": (inizio + timedelta(hours=1)).isoformat()}
            if rng.random() > 0.03:
                base = 21 if statistica.startswith("temp") else 55
                riga["mean"] = round(base + rng.uniform(-8, 8), rng.choice([0, 1, 3, 9]))
            righe.append(riga)
        statistiche[f"sensor.vmc_{NOME}_{statistica}"] = righe
    return {"statistics": statistiche}


async def test_medie_uguali_ai_template(hass: HomeAssistant, freezer) -> None:
    """Le 6 medie e i giorni di dati: stesso stato dei template per risposte inventate."""
    rng = random.Random(f"{SEME}-medie")
    blocco = next(
        b for b in package()["template"] if any(t.get("trigger") == "time_pattern" for t in b.get("triggers", []))
    )
    template = {c["default_entity_id"].removeprefix(f"sensor.vmc_{NOME}_"): Template(c["state"], hass) for c in blocco["sensor"]}
    assert sorted(template) == sorted(
        [k.removeprefix("sensor.") for k, _, _ in MEDIE] + ["rischio_muffa_giorni_dati"]
    )
    giri = max(GIRI // 4, 50)
    visti: dict[str, set] = {chiave: set() for chiave in template}
    for giro in range(giri):
        adesso = datetime(2026, 11, 25, rng.randrange(24), 5, rng.randrange(60), rng.randrange(10**6), tzinfo=UTC)
        freezer.move_to(adesso)
        caso = rng.random()
        if caso < 0.05:
            variabili: dict = {}  # azione non riuscita: stat non definita
            risposta = None
        elif caso < 0.08:
            variabili = {"stat": {"altro": 1}}
            risposta = {"altro": 1}
        else:
            risposta = _risposta(rng, adesso)
            variabili = {"stat": risposta}
        calcolati = calcola_medie(risposta, adesso, NOME)
        for chiave, tpl in template.items():
            atteso = _stato(tpl.async_render(variabili, parse_result=True))
            valore = calcolati[f"sensor.{chiave}"]
            assert _stato(valore) == atteso, (giro, chiave, valore, atteso)
            visti[chiave].add("nessuno" if valore is None else type(valore).__name__)
        assert calcolati[GIORNI_DATI] is not None
    # Ogni sensore è passato sia da «nessun dato» sia da un valore calcolato.
    for chiave, tipi in visti.items():
        attesi = {"int", "float"} if chiave == "rischio_muffa_giorni_dati" else {"nessuno", "float"}
        assert attesi <= tipi, (chiave, tipi)


def test_costanti_medie() -> None:
    """84 giorni di statistiche, medie su 28, 56 e 84 giorni."""
    assert memoria.GIORNI_STATISTICHE == 84
    assert sorted({g for _, _, g in MEDIE}) == [28, 56, 84]
