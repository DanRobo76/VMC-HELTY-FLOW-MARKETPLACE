"""Prove della b36, velocità scelta dall'utente dopo il ritorno della corrente e prima del ripristino (Foglio A23).

Dopo un Black-Out, al ritorno della corrente la VMC aspetta 32 s (più gli eventuali cicli) prima del ripristino della
velocità memorizzata dal Black-Out (spie input_boolean.vmc_master_spia_velocita_*). Prima, una velocità scelta
dall'utente in quell'attesa (Telecomando, scheda o App) veniva sovrascritta dal ripristino e le allerte in corso non la
memorizzavano (a fine allerta la VMC andava alla memoria vecchia). Ora, in testa agli 8 rami «Black-Out Off», se la
velocità letta è cambiata dopo la riaccensione della VMC (meno di 20 s prima del ritorno ON-Line o dopo) e non è la
Velocità 1 (con cui la VMC può ripartire da sola), la scelta resta: nessun comando, le spie del Black-Out si spengono
subito come dopo un ripristino eseguito e le allerte in corso la trattano come una scelta fatta durante l'allerta.
La VMC che riparte da sola non è una scelta: alla Velocità 1 (modello base) o alla velocità di prima (la lettura non
cambia: l'ultima lettura prima del Black-Out è di almeno 32 s prima del ritorno ON-Line).
"""

from __future__ import annotations

import time
from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import BLACK_OUT, FASE, IP, LETTURA, LETTURA_I, PKG, _ramo, _spente
from tests.test_b36_allerte import _esegui, _stato

RAMI = {"0": "Black-Out Off Vel. 0", "1": "Black-Out Off Vel. 1", "2": "Black-Out Off Vel. 2",
        "3": "Black-Out Off Vel. 3", "4": "Black-Out Off Vel. 4", "notturna": "Black-Out Off Notturna",
        "iperventilazione": "Black-Out Off Iperventilazione", "freecooling": "Black-Out Off Free Cool./Heat."}
COMANDO = {"0": "vmc_master_velocita_0", "1": "vmc_master_velocita_1", "2": "vmc_master_velocita_2",
           "3": "vmc_master_velocita_3", "4": "vmc_master_velocita_4", "notturna": "vmc_master_notturna",
           "iperventilazione": "vmc_master_iperventilazione", "freecooling": "vmc_master_freecooling"}
CONDIZIONE = (
    "{%- set vel = states.sensor.vmc_master_status_ventola_lettura_codice_interpretato -%}\n"
    "{%- set rete = states.sensor.vmc_master_status_ip_interfaccia -%}\n"
    "{%- set fase = states.input_number.vmc_master_fase_riallineamento_al_riavvio -%}\n"
    "{{ vel is not none and rete is not none\n"
    "   and vel.state not in ['Velocità 1', 'Non disponibile', 'unknown', 'unavailable', '']\n"
    "   and as_timestamp(vel.last_changed) > as_timestamp(rete.last_changed) - 20\n"
    "   and (fase is none or as_timestamp(vel.last_changed) > as_timestamp(fase.last_changed)) }}"
)
CONDIZIONE_INQ = (
    "{{ is_state('input_boolean.vmc_master_spia_co2_o_voc', 'on')\n"
    "   and (is_state('sensor.vmc_master_alert_monitoraggio_co2', 'Allerta')\n"
    "        or is_state('sensor.vmc_master_alert_monitoraggio_voc', 'Allerta')) }}"
)
STOP = "Velocità scelta dall'utente dopo il ritorno della corrente mantenuta (nessun ripristino)"
SPIA_CO2 = "input_boolean.vmc_master_spia_co2_o_voc"
PARTENZA = "input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0"
V1_CO2 = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc"
V1_PDR = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr"
SPIA_GELO = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
FREE_C = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling"
FREE_H = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating"
MEMORIE_INQ = [f"input_boolean.vmc_master_spia_velocita_{s}_co2_o_voc" for s in COMANDO]
CO2 = "sensor.vmc_master_alert_monitoraggio_co2"
VOC = "sensor.vmc_master_alert_monitoraggio_voc"
MEMORIE_PDR = [f"input_boolean.vmc_master_spia_velocita_{s}_un_solo_avvio" for s in COMANDO]
BLACK_OUT_RILEVATO = "binary_sensor.vmc_master_black_out_rilevato"


def _passo(memoria: str) -> dict[str, Any]:
    return _ramo(RAMI[memoria])["sequence"][0]


@pytest.mark.parametrize("memoria", list(RAMI))
def test_blocco_della_scelta_in_testa_agli_8_rami(memoria: str) -> None:
    """Primo passo di ogni ramo «Black-Out Off», uguale negli 8 rami: condizione, spie del Black-Out spente, stop;
    nessun comando, nessuna attesa nuova (tempi fissi). Il resto del ramo (ripristino di prima) non cambia."""
    passo = _passo(memoria)
    assert set(passo) == {"alias", "if", "then"}
    (condizione,) = passo["if"]
    assert condizione["condition"] == "template"
    assert " ".join(condizione["value_template"].split()) == " ".join(CONDIZIONE.split())
    inquinanti, spegni, stop = passo["then"]
    assert set(inquinanti) == {"alias", "if", "then"}
    (cond_inq,) = inquinanti["if"]
    assert " ".join(cond_inq["value_template"].split()) == " ".join(CONDIZIONE_INQ.split())
    azzera, velocita_0 = inquinanti["then"]
    assert azzera["action"] == "input_boolean.turn_off" and sorted(azzera["target"]["entity_id"]) == sorted(MEMORIE_INQ)
    (cond_v0,) = velocita_0["if"]
    testo_v0 = " ".join(cond_v0["value_template"].split())
    assert "lettura_codice_interpretato', 'Velocità 0')" in testo_v0
    assert all(f"is_state('{e}', 'off')" in testo_v0 for e in MEMORIE_PDR + [FREE_C, FREE_H])
    (accendi,) = velocita_0["then"]
    assert accendi["action"] == "input_boolean.turn_on" and sorted(accendi["target"]["entity_id"]) == sorted(
        [V1_PDR, PARTENZA, V1_CO2])
    assert spegni["action"] == "input_boolean.turn_off" and sorted(spegni["target"]["entity_id"]) == sorted(BLACK_OUT)
    assert stop == {"stop": STOP}
    assert passo == _passo("2")
    assert "vel_prima_del_comando" in _ramo(RAMI[memoria])["sequence"][1]["variables"]
    testo = str(passo)
    for parola in ("delay", "wait_template", "timeout", "'for'", "shell_command", "repeat"):
        assert parola not in testo, parola


def test_file_automazione_lf_e_8_blocchi() -> None:
    dati = (PKG / "vmc_master_automazione.txt").read_bytes()
    assert b"\r" not in dati
    assert dati.decode("utf-8").count(f"- stop: {STOP}\n") == 8


async def test_blocco_valido_per_home_assistant(hass: HomeAssistant) -> None:
    for memoria in RAMI:
        cv.SCRIPT_SCHEMA(_ramo(RAMI[memoria])["sequence"])


def _prepara(hass: HomeAssistant, memoria: str, letta: str, cambiata: float, **altri: str) -> dict[str, str]:
    """VMC di nuovo ON-Line da 32 s (inizio dell'attesa del ripristino), velocità letta cambiata «cambiata» secondi fa
    (o rimasta quella di prima del Black-Out, 120 s fa); spia del Black-Out della velocità «memoria» accesa."""
    adesso = time.time()
    hass.states.async_set(FASE, "0", timestamp=adesso - 3600)  # riallineamento al riavvio finito da tempo
    hass.states.async_set(IP, "ON-Line", timestamp=adesso - 32)
    hass.states.async_set(LETTURA, letta, timestamp=adesso - cambiata)
    stati = {LETTURA_I: letta, FASE: "0", BLACK_OUT_RILEVATO: "off", **_spente(BLACK_OUT),
             f"input_boolean.vmc_master_spia_velocita_{memoria}": "on", SPIA_CO2: "off", PARTENZA: "off", V1_CO2: "off",
             V1_PDR: "off", SPIA_GELO: "off", FREE_C: "off", FREE_H: "off", **_spente(MEMORIE_PDR),
             "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr": "off",
             "sensor.vmc_master_punto_di_rugiada_verifica_confronto": "Si può impiegare"}
    stati.update(altri)
    return stati


async def _ripristino(hass: HomeAssistant, memoria: str, letta: str, cambiata: float, attesa: float = 1.0,
                      **altri: str) -> list[str]:
    stati = _prepara(hass, memoria, letta, cambiata, **altri)
    return await _esegui(hass, _ramo(RAMI[memoria])["sequence"], stati, attesa=attesa)


@pytest.mark.parametrize("memoria", list(RAMI))
@pytest.mark.parametrize(("letta", "cambiata"), [("Velocità 4", 22.0), ("Velocità 0", 10.0), ("Notturna", 1.0),
                                                 ("Velocità 3", 45.0)])
async def test_scelta_prima_del_ripristino_resta(hass: HomeAssistant, memoria: str, letta: str, cambiata: float) -> None:
    """Velocità scelta dopo il ritorno ON-Line (o fino a 20 s prima, prima lettura con la VMC già riaccesa): nessun
    comando e spie del Black-Out spente subito (niente attesa di 12 s del ripristino)."""
    if letta == {"0": "Velocità 0", "3": "Velocità 3", "4": "Velocità 4", "notturna": "Notturna"}.get(memoria):
        pytest.skip("stessa velocità della memoria: vedi test_stessa_velocita_di_prima_del_black_out")
    comandi = await _ripristino(hass, memoria, letta, cambiata, attesa=0.5)
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)


@pytest.mark.parametrize("memoria", [m for m in RAMI if m != "1"])
async def test_ripartenza_a_velocita_1_non_e_una_scelta(hass: HomeAssistant, memoria: str) -> None:
    """Modello base: la VMC riparte da sola a Velocità 1 (lettura cambiata dopo il ritorno): il ripristino avviene come
    prima (anche una Velocità 1 scelta dall'utente non si distingue: il ripristino avviene)."""
    comandi = await _ripristino(hass, memoria, "Velocità 1", 25.0)
    attesi = {"0": "vmc_master_velocita_0"}
    assert comandi[:1] == [attesi.get(memoria, COMANDO[memoria])]


@pytest.mark.parametrize("memoria", [m for m in RAMI if m not in ("0", "1")])
async def test_ripartenza_alla_velocita_di_prima_non_e_una_scelta(hass: HomeAssistant, memoria: str) -> None:
    """Modello R: la VMC riparte alla velocità letta prima del Black-Out, la lettura non cambia (ultimo cambio prima
    del Black-Out, almeno 32 s prima del ritorno ON-Line): il ripristino avviene come prima, anche se la velocità di
    prima non è quella della memoria (per esempio Black-Out mentre un'allerta finiva)."""
    comandi = await _ripristino(hass, memoria, "Velocità 3" if memoria != "3" else "Velocità 2", 120.0)
    assert comandi[:1] == [COMANDO[memoria]]
    comandi = await _ripristino(hass, memoria, "Velocità 3" if memoria != "3" else "Velocità 2", 52.5)
    assert comandi[:1] == [COMANDO[memoria]]


@pytest.mark.parametrize("memoria", ["2", "3", "4", "notturna", "iperventilazione", "freecooling"])
async def test_stessa_velocita_di_prima_del_black_out(hass: HomeAssistant, memoria: str) -> None:
    """L'utente sceglie la velocità di prima del Black-Out (con il modello base, ripartito a Velocità 1): la VMC è già
    alla velocità da ripristinare, nessun comando, spie spente (come dopo il ripristino)."""
    letta = {"2": "Velocità 2", "3": "Velocità 3", "4": "Velocità 4", "notturna": "Notturna",
             "iperventilazione": "Iperventilazione", "freecooling": "Free Cooling"}[memoria]
    comandi = await _ripristino(hass, memoria, letta, 15.0, attesa=0.5)
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)


async def test_velocita_illeggibile_ripristino_come_prima(hass: HomeAssistant) -> None:
    comandi = await _ripristino(hass, "2", "Non disponibile", 10.0)
    assert comandi[:1] == ["vmc_master_velocita_2"]


async def test_inquinanti_partenza_0_scelta_resta(hass: HomeAssistant) -> None:
    """Black-Out a Velocità 1 con gli Inquinanti partiti da Velocità 0 (memoria Velocità 0): la VMC riparte a
    Velocità 1, l'utente sceglie la Velocità 4 -> resta (le spie si spengono e gli Inquinanti la memorizzano con la loro
    regola); senza scelta il ripristino di prima (Velocità 1 degli Inquinanti)."""
    altri = {SPIA_CO2: "on", PARTENZA: "on", V1_PDR: "on", V1_CO2: "on"}
    assert await _ripristino(hass, "0", "Velocità 4", 18.0, attesa=0.5, **altri) == []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)
    assert (await _ripristino(hass, "0", "Velocità 1", 120.0, **altri))[:1] == ["vmc_master_velocita_1"]


async def test_free_con_inquinanti_scelta_resta(hass: HomeAssistant) -> None:
    altri = {SPIA_CO2: "on", V1_CO2: "on", FREE_H: "on"}
    assert await _ripristino(hass, "freecooling", "Velocità 2", 12.0, attesa=0.5, **altri) == []
    assert (await _ripristino(hass, "freecooling", "Velocità 1", 25.0, **altri))[:1] == ["vmc_master_velocita_1"]


@pytest.mark.parametrize("allerta", [CO2, VOC])
@pytest.mark.parametrize(("letta", "cambiata"), [("Velocità 4", 18.0), ("Velocità 0", 12.0)])
async def test_inquinanti_in_corso_memoria_vecchia_azzerata(hass: HomeAssistant, allerta: str, letta: str,
                                                           cambiata: float) -> None:
    """Inquinanti in corso con la memoria di prima del Black-Out (Velocità 2): con la scelta le memorie della velocità
    degli Inquinanti si azzerano, così all'avvio dell'allerta (8 s dopo lo spegnimento delle spie del Black-Out) la
    scelta non viene sostituita dalla Velocità 2 e viene memorizzata con le regole degli Inquinanti (la Velocità 0
    riparte a Velocità 1 con il ritorno a Velocità 0). Le altre spie degli Inquinanti non cambiano."""
    altri = {SPIA_CO2: "on", PARTENZA: "off", **_spente(MEMORIE_INQ), "input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on",
             CO2: "Normale", VOC: "Normale", allerta: "Allerta"}
    assert await _ripristino(hass, "2", letta, cambiata, attesa=0.5, **altri) == []
    accese = [V1_CO2] if letta == "Velocità 0" else []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT + [m for m in MEMORIE_INQ if m not in accese])
    assert all(_stato(hass, e) == "on" for e in accese)
    attesa_partenza = "on" if letta == "Velocità 0" else "off"
    assert _stato(hass, SPIA_CO2) == "on" and _stato(hass, PARTENZA) == attesa_partenza
    assert _stato(hass, V1_PDR) == attesa_partenza


async def test_inquinanti_in_corso_velocita_0_con_pdr(hass: HomeAssistant) -> None:
    """Velocità 0 scelta con gli Inquinanti in corso ma con il PdR su una velocità: le memorie degli Inquinanti si
    azzerano e basta (all'avvio dell'allerta vale la regola del PdR)."""
    altri = {SPIA_CO2: "on", **_spente(MEMORIE_INQ), "input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on",
             CO2: "Allerta", VOC: "Normale", "input_boolean.vmc_master_spia_velocita_3_un_solo_avvio": "on"}
    assert await _ripristino(hass, "2", "Velocità 0", 12.0, attesa=0.5, **altri) == []
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT + MEMORIE_INQ + [PARTENZA, V1_PDR])


async def test_inquinanti_finiti_memoria_non_cambia(hass: HomeAssistant) -> None:
    """Spia degli Inquinanti accesa ma nessuna allerta in corso (finita durante il Black-Out): la memoria resta."""
    altri = {SPIA_CO2: "on", **_spente(MEMORIE_INQ), "input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on",
             CO2: "Normale", VOC: "Normale"}
    assert await _ripristino(hass, "2", "Velocità 4", 18.0, attesa=0.5, **altri) == []
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_2_co2_o_voc") == "on"
    assert all(_stato(hass, e) == "off" for e in BLACK_OUT)


async def test_inquinanti_in_corso_senza_scelta_ripristino_come_prima(hass: HomeAssistant) -> None:
    altri = {SPIA_CO2: "on", **_spente(MEMORIE_INQ), "input_boolean.vmc_master_spia_velocita_2_co2_o_voc": "on",
             CO2: "Allerta", VOC: "Normale"}
    assert (await _ripristino(hass, "2", "Velocità 1", 25.0, **altri))[:1] == ["vmc_master_velocita_2"]
    assert _stato(hass, "input_boolean.vmc_master_spia_velocita_2_co2_o_voc") == "on"
