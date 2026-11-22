"""Prove della b37: l'Offset si somma sempre al valore letto dall'entità scelta (tutti i sensori «_status» con Offset).

Segnalazione: VMC senza sonda CO₂/VOC (la risposta Sensori Ambientali, VMGI?, ha i campi 4 e 11 a 00000: la sonda
della VMC sensor.vmc_master_co2_status_senza_offset mostra «-» e il sensore «CO₂ Int. Selezionata» lo passa come 0).
Con la sonda della VMC scelta come «Entità CO₂ Interna» e un Offset CO₂, fino alla b35 la CO₂ diventava il valore
dell'Offset (+900 -> 900 ppm, con l'allerta Inquinanti); la b36 (commit 0a6b741) aveva aggiunto un controllo del valore
letto ≤ 0 prima dell'Offset in sensor.vmc_master_co2_status e nel gemello sensor.vmc_master_voc_status, e restava «-».
Regola del proprietario: la sonda della VMC SENZA Offset si usa solo quando va in down un'entità scelta diversa dalla
VMC; altrimenti l'Offset si somma sempre al valore letto. La b37 toglie i due controlli: la logica torna quella della
b35.

Prove per tutti i sensori che sommano un Offset (Temperatura Ext. e Int., Umidità Ext. e Int., CO₂ e VOC):
a) entità scelta = sonda della VMC (voce «_senza_offset» degli elenchi «Aggiorna Elenco»; i VOC hanno solo la sonda
   della VMC) con una lettura vera: valore letto + Offset;
b) entità scelta = un sensore (o un meteo) esterno con un numero: valore letto + Offset;
c) entità esterna non disponibile o non numerica: sonda della VMC SENZA Offset (l'Umidità Ext. non ha una sonda della
   VMC: «Non disponibile»);
d) sonda della VMC scelta e assente (CO₂ e VOC a 00000): un Offset positivo dà il valore dell'Offset, con livelli,
   allerte e «_grafico» che seguono; Offset 0 o negativo: «-» (con l'Offset positivo fallisce sulla b36, passa dopo);
e) controllo statico: nessun sensore «_status» con Offset confronta il valore letto con 0 prima di sommare l'Offset
   (fallisce sulla b36, passa dopo).

Rese con il motore di Home Assistant: i blocchi template veri del Package (sensore memorizzato a trigger, sensori
selezionati, segni delle temperature, sensori con e senza Offset, livelli, allerte e «_grafico») caricati con
l'integrazione template; gli elenchi delle entità sono resi dai modelli veri degli script «Aggiorna Elenco»."""

from __future__ import annotations

import copy
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, NamedTuple

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from homeassistant.util import yaml as hay
from jinja2 import Environment, nodes

RADICE = Path(__file__).resolve().parents[1]
PKG = RADICE / "custom_components" / "vmc_master" / "package"
SENSORI = "sensor.vmc_master_sensori"
MEMORIZZATA = "sensor.vmc_master_sensori_memorizzata"
PREFISSO_OFFSET = "input_number.vmc_master_offset_"


class Famiglia(NamedTuple):
    status: str               # sensore con Offset
    sonda: str | None         # sonda della VMC senza Offset (None: la VMC non ha questa sonda)
    selezionata: str | None   # sensore «Selezionata» che legge l'entità scelta (None: si legge solo la VMC)
    scelta: str | None        # input_select dell'entità scelta
    script: str | None        # script «Aggiorna Elenco» che scrive le opzioni dell'input_select
    offset: str               # input_number dell'Offset


FAMIGLIE = {
    "temp_esterna": Famiglia(
        "sensor.vmc_master_temp_esterna_status", "sensor.vmc_master_temp_esterna_status_senza_offset",
        "sensor.vmc_master_temperatura_esterna_selezionata", "input_select.vmc_master_selected_temp_external_entity",
        "vmc_master_aggiorna_elenco_entita_temperatura_esterna", "input_number.vmc_master_offset_temp_esterna"),
    "temp_interna": Famiglia(
        "sensor.vmc_master_temp_interna_status", "sensor.vmc_master_temp_interna_status_senza_offset",
        "sensor.vmc_master_temperatura_interna_selezionata", "input_select.vmc_master_selected_temp_internal_entity",
        "vmc_master_aggiorna_elenco_entita_temperatura_interna", "input_number.vmc_master_offset_temp_interna"),
    "umidita_esterna": Famiglia(
        "sensor.vmc_master_umidita_esterna_status", None,
        "sensor.vmc_master_umidita_esterna_selezionata", "input_select.vmc_master_selected_humidity_external_entity",
        "vmc_master_aggiorna_elenco_entita_umidita_esterna", "input_number.vmc_master_offset_umidita_esterna"),
    "umidita_interna": Famiglia(
        "sensor.vmc_master_umidita_interna_status", "sensor.vmc_master_umidita_interna_status_senza_offset",
        "sensor.vmc_master_umidita_interna_selezionata", "input_select.vmc_master_selected_humidity_internal_entity",
        "vmc_master_aggiorna_elenco_entita_umidita_interna", "input_number.vmc_master_offset_umidita_interna"),
    "co2": Famiglia(
        "sensor.vmc_master_co2_status", "sensor.vmc_master_co2_status_senza_offset",
        "sensor.vmc_master_co2_interna_selezionata", "input_select.vmc_master_selected_co2_internal_entity",
        "vmc_master_aggiorna_elenco_entita_co2_interna", "input_number.vmc_master_offset_co2"),
    "voc": Famiglia(
        "sensor.vmc_master_voc_status", "sensor.vmc_master_voc_status_senza_offset",
        None, None, None, "input_number.vmc_master_offset_voc"),
}
CON_SCELTA = [nome for nome, f in FAMIGLIE.items() if f.scelta]
CO2, VOC = FAMIGLIE["co2"], FAMIGLIE["voc"]
LIVELLO_CO2 = "sensor.vmc_master_co2_status_verifica_soglia"
LIVELLO_VOC = "sensor.vmc_master_voc_status_verifica_soglia"
ALLERTA_CO2 = "sensor.vmc_master_alert_monitoraggio_co2"
ALLERTA_VOC = "sensor.vmc_master_alert_monitoraggio_voc"
STATUS = [f.status for f in FAMIGLIE.values()]
SONDE = [f.sonda for f in FAMIGLIE.values() if f.sonda]
# sensori da cui parte il caricamento: i sensori con e senza Offset, i livelli e le allerte di CO₂ e VOC (le loro
# dipendenze, selezionati, segni delle temperature e sensore memorizzato, si aggiungono da sole) e i «_grafico»
RADICI = [*STATUS, *SONDE, LIVELLO_CO2, LIVELLO_VOC, ALLERTA_CO2, ALLERTA_VOC]
# lettura della VMC data da _vmgi() senza argomenti, come la mostrano le sonde senza Offset
LETTURA_VMC = {"temp_esterna": "10.0", "temp_interna": "21.0", "umidita_interna": "50.0", "co2": "600", "voc": "50"}
TEMPERATURA = {"device_class": "temperature", "unit_of_measurement": "°C"}
UMIDITA = {"device_class": "humidity", "unit_of_measurement": "%"}
ANIDRIDE = {"device_class": "carbon_dioxide", "unit_of_measurement": "ppm"}
METEO = {"temperature": 8.4, "humidity": 70}


@lru_cache(maxsize=1)
def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _vmgi(co2: int = 600, voc: int = 50, ti: int = 210, te: int = 100, rh: int = 500) -> str:
    return (f"VMGI,{ti:05d},{te:05d},{rh:05d},{co2:05d},00000,00000,00000,00000,00000,00000,{voc:05d},"
            "00000,00000,00000")


def _dipendenze(sensore: dict[str, Any]) -> list[str]:
    return re.findall(r"sensor\.vmc_master_\w+", " ".join(str(sensore.get(k, "")) for k in ("state", "availability")))


def _blocchi() -> list[dict[str, Any]]:
    """Blocchi template veri del Package: RADICI con le loro dipendenze (sensore memorizzato col suo trigger) e tutti
    i «_grafico» (senza le loro dipendenze: quelli di altri sensori restano non disponibili)."""
    blocchi = _pacchetto()["template"]
    sensori = {s["default_entity_id"]: s for b in blocchi for s in b.get("sensor", []) or []}
    da_caricare: set[str] = set()
    coda = list(RADICI)
    while coda:
        eid = coda.pop()
        if eid in sensori and eid not in da_caricare:
            da_caricare.add(eid)
            coda += _dipendenze(sensori[eid])
    risultato = []
    for blocco in blocchi:
        scelti = [s for s in blocco.get("sensor", []) or []
                  if s["default_entity_id"] in da_caricare or s["default_entity_id"].endswith("_grafico")]
        if scelti:
            nuovo = {"sensor": scelti}
            if "triggers" in blocco:
                nuovo["triggers"] = blocco["triggers"]
            risultato.append(copy.deepcopy(nuovo))
    return risultato


async def _avvia(hass: HomeAssistant, scelte: dict[str, str] | None = None,
                 offset: dict[str, float] | None = None) -> None:
    """Entità scelte (di base la sonda della VMC; l'Umidità Ext. non ne ha una) e Offset (di base 0), poi i blocchi."""
    for nome, famiglia in FAMIGLIE.items():
        if famiglia.scelta:
            hass.states.async_set(famiglia.scelta, (scelte or {}).get(nome, famiglia.sonda or "sensor.nessuna"))
        hass.states.async_set(famiglia.offset, str((offset or {}).get(nome, 0)))
    assert await async_setup_component(hass, "template", {"template": _blocchi()})
    await hass.async_block_till_done()
    caricati = [f.selezionata for f in FAMIGLIE.values() if f.selezionata] + [
        "sensor.vmc_master_temp_esterna_positivo_negativo", "sensor.vmc_master_temp_interna_positivo_negativo",
        MEMORIZZATA, *(f"{e}_grafico" for e in STATUS + SONDE)]
    assert [e for e in caricati if hass.states.get(e) is None] == []


async def _lettura(hass: HomeAssistant, valore: str) -> None:
    hass.states.async_set(SENSORI, valore)
    await hass.async_block_till_done()


async def _imposta(hass: HomeAssistant, entita: str, stato: str | None,
                   attributi: dict[str, Any] | None = None) -> None:
    """Stato di un'entità (None: entità tolta da Home Assistant)."""
    if stato is None:
        hass.states.async_remove(entita)
    else:
        hass.states.async_set(entita, stato, attributi or {})
    await hass.async_block_till_done()


def _stati(hass: HomeAssistant, *entita: str) -> list[str]:
    return [hass.states.get(e).state for e in entita]


def _opzioni(hass: HomeAssistant, famiglia: Famiglia) -> list[str]:
    """Opzioni dell'input_select rese dal modello vero dello script «Aggiorna Elenco» con le entità presenti."""
    passo = _pacchetto()["script"][famiglia.script]["sequence"][0]
    assert passo["action"] == "input_select.set_options"
    assert passo["target"]["entity_id"] == famiglia.scelta
    return Template(passo["data"]["options"], hass).async_render()


def _grafico(stato: str) -> str:
    """Il «_grafico» segue il sensore quando è un numero, altrimenti non è disponibile (buco nel grafico)."""
    try:
        float(stato)
    except ValueError:
        return "unavailable"
    return stato


# ------------------------------------------------------------------------------- a) sonda della VMC scelta, letta
async def test_elenchi_delle_entita_con_la_sonda_della_vmc(hass: HomeAssistant) -> None:
    """La sonda della VMC senza Offset è una voce degli elenchi «Aggiorna Elenco» di Temperatura Ext. e Int., Umidità
    Int. e CO₂ (sceglierla è il caso della segnalazione); l'elenco dell'Umidità Ext. non ha una sonda della VMC."""
    await _avvia(hass)
    for nome in CON_SCELTA:
        famiglia = FAMIGLIE[nome]
        opzioni = _opzioni(hass, famiglia)
        if famiglia.sonda:
            assert famiglia.sonda in opzioni, nome
        else:
            assert [o for o in opzioni if o.endswith("_senza_offset")] == [], nome


SONDA_VMC = [  # famiglia, Offset positivo e valore atteso, Offset negativo e valore atteso
    ("temp_esterna", 1.5, "11.5", -2.5, "7.5"),
    ("temp_interna", 1.5, "22.5", -1.5, "19.5"),
    ("umidita_interna", 5, "55.0", -5, "45.0"),
    ("co2", 50, "650", -100, "500"),
    ("voc", 20, "70", -10, "40"),
]


@pytest.mark.parametrize(("nome", "piu", "atteso_piu", "meno", "atteso_meno"), SONDA_VMC,
                         ids=[c[0] for c in SONDA_VMC])
async def test_sonda_della_vmc_scelta_offset_sommato(hass: HomeAssistant, nome: str, piu: float, atteso_piu: str,
                                                     meno: float, atteso_meno: str) -> None:
    """a) Entità scelta = sonda della VMC (i VOC hanno solo quella) con una lettura vera: valore letto + Offset, sia
    positivo sia negativo; con l'Offset 0 il valore letto. La sonda senza Offset resta la lettura, il «_grafico» del
    sensore con Offset lo segue."""
    famiglia = FAMIGLIE[nome]
    await _avvia(hass)
    if famiglia.scelta:
        assert hass.states.get(famiglia.scelta).state == famiglia.sonda
    await _lettura(hass, _vmgi())
    for offset, atteso in ((0, LETTURA_VMC[nome]), (piu, atteso_piu), (meno, atteso_meno)):
        await _imposta(hass, famiglia.offset, str(offset))
        assert _stati(hass, famiglia.status, f"{famiglia.status}_grafico", famiglia.sonda) == [
            atteso, atteso, LETTURA_VMC[nome]], offset


# --------------------------------------------------------------------------------------- b) entità esterna con numero
ESTERNE = [  # famiglia, entità scelta, stato, attributi, Offset, valore atteso
    ("temp_esterna", "sensor.temp_esterna_prova", "12.3", TEMPERATURA, 1.5, "13.8"),
    ("temp_esterna", "weather.casa", "sunny", METEO, -0.4, "8.0"),
    ("temp_interna", "sensor.temp_interna_prova", "19.8", TEMPERATURA, -0.8, "19.0"),
    ("umidita_esterna", "sensor.umidita_esterna_prova", "60", UMIDITA, 5, "65.0"),
    ("umidita_esterna", "weather.casa", "sunny", METEO, 5, "75.0"),
    ("umidita_interna", "sensor.umidita_interna_prova", "45.5", UMIDITA, 4.5, "50.0"),
    ("co2", "sensor.co2_prova", "700", ANIDRIDE, 50, "750"),
]


@pytest.mark.parametrize(("nome", "entita", "stato", "attributi", "offset", "atteso"), ESTERNE,
                         ids=[f"{c[0]}-{c[1].split('.')[0]}" for c in ESTERNE])
async def test_entita_esterna_offset_sommato(hass: HomeAssistant, nome: str, entita: str, stato: str,
                                             attributi: dict[str, Any], offset: float, atteso: str) -> None:
    """b) Entità scelta = un sensore (o per l'esterno un meteo) di Home Assistant con un numero, voce dell'elenco
    «Aggiorna Elenco»: valore letto + Offset, anche sulla VMC senza sonda CO₂/VOC (la sonda della VMC non conta)."""
    famiglia = FAMIGLIE[nome]
    hass.states.async_set(entita, stato, attributi)
    await _avvia(hass, scelte={nome: entita}, offset={nome: offset})
    assert entita in _opzioni(hass, famiglia)
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, famiglia.status, f"{famiglia.status}_grafico") == [atteso, atteso]


# ------------------------------------------------------------------------------ c) entità esterna non disponibile
def _guasti(entita: str, attributi: dict[str, Any]) -> list[tuple[str | None, dict[str, Any]]]:
    """Stati di un'entità scelta che non dà un numero: non disponibile, sconosciuta, non numerica, tolta (None)."""
    if entita.startswith("weather."):
        return [("unavailable", {}), ("sunny", {}), (None, {})]
    return [("unavailable", attributi), ("unknown", attributi), ("non numerico", attributi), (None, {})]


NON_DISPONIBILI = [  # famiglia, entità scelta, stato e attributi validi, Offset, atteso con il numero, atteso guasta
    ("temp_esterna", "sensor.temp_esterna_prova", "30", TEMPERATURA, 1.5, "31.5", "10.0"),
    ("temp_esterna", "weather.casa", "sunny", METEO, 1.5, "9.9", "10.0"),
    ("temp_interna", "sensor.temp_interna_prova", "30", TEMPERATURA, 1.5, "31.5", "21.0"),
    ("umidita_esterna", "sensor.umidita_esterna_prova", "30", UMIDITA, 5, "35.0", "Non disponibile"),
    ("umidita_esterna", "weather.casa", "sunny", METEO, 5, "75.0", "Non disponibile"),
    ("umidita_interna", "sensor.umidita_interna_prova", "30", UMIDITA, 5, "35.0", "50.0"),
    ("co2", "sensor.co2_prova", "700", ANIDRIDE, 900, "1600", "600"),
]


@pytest.mark.parametrize(("nome", "entita", "stato", "attributi", "offset", "atteso", "atteso_guasta"),
                         NON_DISPONIBILI, ids=[f"{c[0]}-{c[1].split('.')[0]}" for c in NON_DISPONIBILI])
async def test_entita_esterna_non_disponibile_sonda_della_vmc_senza_offset(
        hass: HomeAssistant, nome: str, entita: str, stato: str, attributi: dict[str, Any], offset: float,
        atteso: str, atteso_guasta: str) -> None:
    """c) Entità scelta diversa dalla VMC che va in down (non disponibile, sconosciuta, non numerica o tolta; il meteo
    anche senza l'attributo): si usa la sonda della VMC SENZA Offset (l'Umidità Ext. non ha una sonda della VMC:
    «Non disponibile»); quando l'entità torna con un numero l'Offset si somma di nuovo."""
    famiglia = FAMIGLIE[nome]
    hass.states.async_set(entita, stato, attributi)
    await _avvia(hass, scelte={nome: entita}, offset={nome: offset})
    await _lettura(hass, _vmgi())
    assert _stati(hass, famiglia.status, f"{famiglia.status}_grafico") == [atteso, atteso]
    for guasto, attributi_guasto in _guasti(entita, attributi):
        await _imposta(hass, entita, guasto, attributi_guasto)
        assert _stati(hass, famiglia.status, f"{famiglia.status}_grafico") == [
            atteso_guasta, _grafico(atteso_guasta)], guasto
        await _imposta(hass, entita, stato, attributi)
        assert _stati(hass, famiglia.status) == [atteso], guasto


async def test_co2_esterna_non_disponibile_e_sonda_della_vmc_assente(hass: HomeAssistant) -> None:
    """c) Entità CO₂ esterna in down sulla VMC senza sonda CO₂: la sonda della VMC senza Offset è «-», quindi la CO₂ è
    «-» anche con l'Offset +900 (l'Offset non si somma alla sonda di riserva), grafico non disponibile, livello «-» e
    nessuna allerta."""
    hass.states.async_set("sensor.co2_prova", "700", ANIDRIDE)
    await _avvia(hass, scelte={"co2": "sensor.co2_prova"}, offset={"co2": 900})
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, CO2.status, LIVELLO_CO2, ALLERTA_CO2) == ["1600", "Pessima Concentrazione", "Allerta"]
    await _imposta(hass, "sensor.co2_prova", "unavailable", ANIDRIDE)
    assert _stati(hass, CO2.status, f"{CO2.status}_grafico", CO2.sonda, LIVELLO_CO2, ALLERTA_CO2) == [
        "-", "unavailable", "-", "-", "Nessuna Allerta"]


# ------------------------------------------------------------------- d) sonda della VMC scelta e assente (00000)
CO2_ASSENTE = [  # Offset CO₂, CO₂, livello, allerta
    (50, "50", "Bassa Concentrazione", "Nessuna Allerta"),
    (900, "900", "Moderata Concentrazione", "Allerta"),
    (0, "-", "-", "Nessuna Allerta"),
    (-50, "-", "-", "Nessuna Allerta"),
]
VOC_ASSENTE = [  # Offset VOC, VOC, livello, allerta
    (20, "20", "Bassa Concentrazione", "Nessuna Allerta"),
    (400, "400", "Moderata Concentrazione", "Allerta"),
    (0, "-", "-", "Nessuna Allerta"),
    (-20, "-", "-", "Nessuna Allerta"),
]


@pytest.mark.parametrize(("offset", "atteso", "livello", "allerta"), CO2_ASSENTE,
                         ids=[f"offset{c[0]:+d}" for c in CO2_ASSENTE])
async def test_co2_sonda_della_vmc_assente_offset(hass: HomeAssistant, offset: int, atteso: str, livello: str,
                                                  allerta: str) -> None:
    """d) La segnalazione: sonda della VMC scelta come «Entità CO₂ Interna» su una VMC senza sonda (CO₂ a 00000, «-»
    passato come 0 dal sensore «CO₂ Int. Selezionata»). L'Offset si somma al valore letto: +50 -> 50 ppm, +900 ->
    900 ppm con «Moderata Concentrazione» e allerta; Offset 0 o negativo -> «-». Il «_grafico» con Offset segue la
    CO₂, la sonda senza Offset resta «-» col suo grafico non disponibile."""
    await _avvia(hass, offset={"co2": offset})
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, CO2.selezionata, CO2.sonda, f"{CO2.sonda}_grafico") == ["0", "-", "unavailable"]
    assert _stati(hass, CO2.status, f"{CO2.status}_grafico", LIVELLO_CO2, ALLERTA_CO2) == [
        atteso, _grafico(atteso), livello, allerta]


@pytest.mark.parametrize(("offset", "atteso", "livello", "allerta"), VOC_ASSENTE,
                         ids=[f"offset{c[0]:+d}" for c in VOC_ASSENTE])
async def test_voc_sonda_della_vmc_assente_offset(hass: HomeAssistant, offset: int, atteso: str, livello: str,
                                                  allerta: str) -> None:
    """d) Gemello VOC (solo la sonda della VMC, VOC a 00000): +20 -> 20 ppb, +400 -> 400 ppb con «Moderata
    Concentrazione» e allerta; Offset 0 o negativo -> «-». Il «_grafico» con Offset segue i VOC, la sonda senza Offset
    resta «-» col suo grafico non disponibile."""
    await _avvia(hass, offset={"voc": offset})
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, VOC.sonda, f"{VOC.sonda}_grafico") == ["-", "unavailable"]
    assert _stati(hass, VOC.status, f"{VOC.status}_grafico", LIVELLO_VOC, ALLERTA_VOC) == [
        atteso, _grafico(atteso), livello, allerta]


async def test_offset_cambiato_e_sonda_della_vmc_che_torna(hass: HomeAssistant) -> None:
    """d) VMC senza sonda, Offset cambiati a sensori già avviati: 0 -> «-»; +900 ppm e +400 ppb -> 900 e 400 con le
    allerte; una lettura con la sonda (600 ppm, 50 ppb) -> 1500 e 450; di nuovo senza sonda -> 900 e 400; Offset
    tolti -> «-» e nessuna allerta."""
    await _avvia(hass)
    entita = [CO2.status, VOC.status, f"{CO2.status}_grafico", f"{VOC.status}_grafico", ALLERTA_CO2, ALLERTA_VOC]
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, *entita) == ["-", "-", "unavailable", "unavailable", "Nessuna Allerta", "Nessuna Allerta"]
    await _imposta(hass, CO2.offset, "900.0")
    await _imposta(hass, VOC.offset, "400.0")
    assert _stati(hass, *entita) == ["900", "400", "900", "400", "Allerta", "Allerta"]
    await _lettura(hass, _vmgi(co2=600, voc=50))
    assert _stati(hass, *entita) == ["1500", "450", "1500", "450", "Allerta", "Allerta"]
    assert _stati(hass, LIVELLO_CO2, LIVELLO_VOC) == ["Pessima Concentrazione", "Moderata Concentrazione"]
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, *entita) == ["900", "400", "900", "400", "Allerta", "Allerta"]
    await _imposta(hass, CO2.offset, "0.0")
    await _imposta(hass, VOC.offset, "0.0")
    assert _stati(hass, *entita) == ["-", "-", "unavailable", "unavailable", "Nessuna Allerta", "Nessuna Allerta"]


# ------------------------------------------------------------------------------------------- e) controllo statico
_CONVERSIONI = {"float", "int", "round", "abs"}
_CONFRONTI = {"lt", "lteq", "gt", "gteq", "eq", "ne"}


def _nucleo(nodo: nodes.Node) -> nodes.Node:
    """Il valore sotto le conversioni numeriche: «x | float(0)», «float(x, 0)», «x | round(1)» -> x."""
    while True:
        if isinstance(nodo, nodes.Filter) and nodo.name in _CONVERSIONI and nodo.node is not None:
            nodo = nodo.node
        elif (isinstance(nodo, nodes.Call) and isinstance(nodo.node, nodes.Name)
              and nodo.node.name in ("float", "int") and nodo.args):
            nodo = nodo.args[0]
        else:
            return nodo


def _zero_o_meno(nodo: nodes.Node) -> bool:
    segno = 1
    if isinstance(nodo, nodes.Neg):
        segno, nodo = -1, nodo.node
    return (isinstance(nodo, nodes.Const) and isinstance(nodo.value, (int, float))
            and not isinstance(nodo.value, bool) and segno * nodo.value <= 0)


def _controlli_prima_dell_offset(modello: str) -> tuple[list[nodes.Node], list[str]]:
    """Valori letti a cui il modello somma l'Offset (anche risalendo le variabili da cui vengono) e confronti di questi
    valori con 0 o con un numero negativo (righe del modello)."""
    albero = Environment(extensions=["jinja2.ext.loopcontrols", "jinja2.ext.do"]).parse(modello)
    assegnazioni = [(a.target.name, a.node) for a in albero.find_all(nodes.Assign) if isinstance(a.target, nodes.Name)]
    con_offset: set[str] = set()

    def ha_offset(nodo: nodes.Node) -> bool:
        return any((isinstance(n, nodes.Const) and isinstance(n.value, str) and n.value.startswith(PREFISSO_OFFSET))
                   or (isinstance(n, nodes.Name) and n.name in con_offset) for n in (nodo, *nodo.find_all(nodes.Node)))

    while nuovi := {nome for nome, valore in assegnazioni if ha_offset(valore)} - con_offset:
        con_offset |= nuovi
    letti: list[nodes.Node] = []
    for somma in albero.find_all((nodes.Add, nodes.Sub)):
        for lato, altro in ((somma.left, somma.right), (somma.right, somma.left)):
            if ha_offset(altro) and not ha_offset(lato) and _nucleo(lato) not in letti:
                letti.append(_nucleo(lato))
    for valore_letto in letti:  # la lista cresce mentre si risale
        if isinstance(valore_letto, nodes.Name):
            letti += [_nucleo(v) for n, v in assegnazioni
                      if n == valore_letto.name and not ha_offset(v) and _nucleo(v) not in letti]
    righe = modello.splitlines()
    errori = []
    for confronto in albero.find_all(nodes.Compare):
        termini = [confronto.expr, *(o.expr for o in confronto.ops)]
        for sinistra, operatore, destra in zip(termini, confronto.ops, termini[1:]):
            if operatore.op in _CONFRONTI and ((_nucleo(sinistra) in letti and _zero_o_meno(destra))
                                               or (_nucleo(destra) in letti and _zero_o_meno(sinistra))):
                errori.append(righe[confronto.lineno - 1].strip())
    return letti, errori


def test_nessun_controllo_del_valore_letto_prima_dell_offset() -> None:
    """e) Classe del difetto della b36: nessun sensore «_status» che somma un input_number.vmc_master_offset_* confronta
    il valore letto (o la variabile da cui viene) con 0 prima di sommare l'Offset; si confronta solo il valore con
    l'Offset. I sensori controllati sono esattamente i 6 con Offset e in ognuno il controllo trova il valore letto.
    Le due condizioni della b36 (co2_status e voc_status) non ci sono più."""
    controllati = {}
    for blocco in _pacchetto()["template"]:
        for sensore in blocco.get("sensor", []) or []:
            modello = str(sensore.get("state", ""))
            if sensore["default_entity_id"].endswith("_status") and PREFISSO_OFFSET in modello:
                controllati[sensore["default_entity_id"]] = _controlli_prima_dell_offset(modello)
    assert sorted(controllati) == sorted(STATUS)
    assert [e for e, (letti, _) in controllati.items() if not letti] == []
    assert {e: errori for e, (_, errori) in controllati.items() if errori} == {}
    pacchetto = _testo("vmc_master.yaml")
    assert "co2_float <= 0 or" not in pacchetto
    assert "float(componenti[11], 0) > 0" not in pacchetto
