"""Prove della b34: Velocità 0 scelta dall'utente durante gli Inquinanti o il Δ Temp. con l'Umidità (avviata da una
velocità diversa da 0) in corso. Se l'Umidità finisce prima dell'altra allerta, alla fine di quest'ultima la VMC torna
a 0 e poi, 28 Secondi dopo, la fine dell'Umidità rimandava la velocità di avvio dell'Umidità: la scelta dell'utente
andava persa (84 esiti della simulazione completa, presenti anche nella b32). Ora la lettura a Velocità 0 con la
Spia Umidità ancora accesa e la memoria «Velocità 0» spenta memorizza la Velocità 0 (mantenuta) anche a Umidità
finita; con l'Umidità avviata da 0 (memoria «Velocità 0» accesa) vale come prima solo durante l'allerta."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
ALLERTA_O_MEMORIA_SPENTA = (
    "(states('sensor.vmc_master_alert_monitoraggio_umidita') == 'Allerta' or "
    "states('input_boolean.vmc_master_spia_umidita_velocita_0') == 'off') and"
)
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
ALLERTA = "sensor.vmc_master_alert_monitoraggio_umidita"
SPIA_U0 = "input_boolean.vmc_master_spia_umidita_velocita_0"
SPIA_UMIDITA = "input_boolean.vmc_master_umidita_verifica_soglia_valore_spia"


def _testo() -> str:
    return (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")


def _trigger() -> dict:
    trovati = [t for t in hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))["triggers"]
               if t.get("id") == "umidita_velocita_0"]
    assert len(trovati) == 1
    return trovati[0]


def _copia_guardia() -> str:
    righe = _testo().split("\n")
    testa = "{%- elif trigger.id == 'umidita_velocita_0' -%}"
    inizio = [k for k, r in enumerate(righe) if r.strip() == testa]
    assert len(inizio) == 1
    rientro = len(righe[inizio[0]]) - len(righe[inizio[0]].lstrip())
    fine = next(k for k in range(inizio[0] + 1, len(righe))
                if len(righe[k]) - len(righe[k].lstrip()) == rientro and re.match(r"\{%-? (elif|else|endif)\b", righe[k].strip()))
    return "\n".join(righe[inizio[0] + 1 : fine])


def test_condizione_nel_trigger_e_nella_guardia() -> None:
    """La nuova condizione è nel trigger e nella sua copia 1:1 della guardia «Evento ancora valido»."""
    assert _trigger()["value_template"].count(ALLERTA_O_MEMORIA_SPENTA) == 1
    assert _copia_guardia().count(ALLERTA_O_MEMORIA_SPENTA) == 1
    # gli altri trigger dell'Umidità con «== 'Allerta'» restano come prima (2 copie: trigger + guardia)
    assert _testo().count(ALLERTA_O_MEMORIA_SPENTA) == 2


def test_ramo_documentato() -> None:
    """L'«altrimenti» del ramo dice che la Velocità 0 resta anche a Umidità finita con la Spia Umidità accesa."""
    assert "vale anche a Umidità finita con la Spia Umidità ancora accesa" in _testo()


def _stati_base(hass: HomeAssistant) -> None:
    """Tutto spento tranne la Spia Umidità e l'interruttore dell'Umidità; VMC ON-Line e a Velocità 0."""
    for riga in set(re.findall(r"states\('(input_boolean\.[a-z0-9_]+)'\) == 'off'", _trigger()["value_template"])):
        hass.states.async_set(riga, "off")
    hass.states.async_set(LETTURA, "Velocità 0")
    hass.states.async_set("input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita", "on")
    hass.states.async_set(SPIA_UMIDITA, "on")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set("sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia", "Velocità 0")
    hass.states.async_set("input_number.vmc_master_fase_riallineamento_al_riavvio", "0")
    hass.states.async_set("input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0", "off")


@pytest.mark.parametrize(
    ("allerta", "memoria_0", "spia_umidita", "lettura", "atteso"),
    [
        ("Allerta", "off", "on", "Velocità 0", True),  # come prima: l'utente preme 0 durante l'Umidità
        ("Allerta", "on", "on", "Velocità 0", True),  # come prima: Umidità avviata da 0 (riparte la velocità di avvio)
        ("Nessuna Allerta", "off", "on", "Velocità 0", True),  # nuovo: Umidità finita, 0 scelto sotto un'altra allerta
        ("Nessuna Allerta", "on", "on", "Velocità 0", False),  # Umidità avviata da 0 e finita: nessuna ripartenza
        ("Nessuna Allerta", "off", "off", "Velocità 0", False),  # Umidità già chiusa
        ("Nessuna Allerta", "off", "on", "Velocità 3", False),  # la VMC non è a 0
    ],
)
async def test_trigger_reso(hass: HomeAssistant, allerta: str, memoria_0: str, spia_umidita: str, lettura: str,
                            atteso: bool) -> None:
    """Il trigger e la sua copia nella guardia danno lo stesso esito, reso con il motore Jinja di Home Assistant."""
    _stati_base(hass)
    hass.states.async_set(ALLERTA, allerta)
    hass.states.async_set(SPIA_U0, memoria_0)
    hass.states.async_set(SPIA_UMIDITA, spia_umidita)
    hass.states.async_set(LETTURA, lettura)
    assert Template(_trigger()["value_template"], hass).async_render() is atteso
    assert Template(_copia_guardia(), hass).async_render() is atteso


async def test_con_inquinanti_accesi_niente(hass: HomeAssistant) -> None:
    """Finché gli Inquinanti sono in corso (Spia Inquinanti accesa) la lettura a 0 non tocca l'Umidità."""
    _stati_base(hass)
    hass.states.async_set(ALLERTA, "Nessuna Allerta")
    hass.states.async_set(SPIA_U0, "off")
    hass.states.async_set("input_boolean.vmc_master_spia_co2_o_voc", "on")
    assert Template(_trigger()["value_template"], hass).async_render() is False

