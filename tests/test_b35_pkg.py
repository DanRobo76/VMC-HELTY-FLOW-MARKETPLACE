"""Prove della 9.0.0b35 (fetta «pkg»): rilievi dell'audit 1:1 della b34 C2-1, C2-2, C2-3, C2-4.

Prove statiche sul testo e sulla struttura YAML, rese dei template con il motore di Home Assistant e corse vere degli
script «Aggiorna Elenco» in Home Assistant (input_select, input_text e script veri; notifiche registrate)."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import entity_sources
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from homeassistant.util import yaml as hay
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_fire_time_changed

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"
SCRIPT_ELENCO = ("temperatura_esterna", "temperatura_interna", "umidita_esterna", "umidita_interna", "co2_interna",
                 "notifica_dispositivo", "media_player")
# script con l'entita' meteo: attributo, selezione, ultima scelta, voce «Aggiorna…», id della notifica,
# sensore «selezionata»
METEO = {
    "temperatura_esterna": ("temperature", "vmc_master_selected_temp_external_entity",
                            "vmc_master_last_temp_external_entity", "Aggiorna Elenco Entità Temperatura Esterna",
                            "vmc_master_aggiorna_entita_temperatura_esterna",
                            "sensor.vmc_master_temperatura_esterna_selezionata"),
    "umidita_esterna": ("humidity", "vmc_master_selected_humidity_external_entity",
                        "vmc_master_last_humidity_external_entity", "Aggiorna Elenco Entità Umidità Esterna",
                        "vmc_master_aggiorna_entita_umidita_esterna", "sensor.vmc_master_umidita_esterna_selezionata"),
}
DEVICE_CLASS = {"temperatura_esterna": "temperature", "umidita_esterna": "humidity"}
METEO_PROVA = "weather.prova"
ALTRO_METEO = "weather.altra"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


def _script(pacchetto: dict[str, Any], nome: str) -> dict[str, Any]:
    return pacchetto["script"][f"vmc_master_aggiorna_elenco_entita_{nome}"]


def _opzioni(pacchetto: dict[str, Any], nome: str) -> str:
    passo = _script(pacchetto, nome)["sequence"][0]
    assert passo["action"] == "input_select.set_options", nome
    return passo["data"]["options"]


def _stato_sensore(pacchetto: dict[str, Any], entita: str) -> str:
    for blocco in pacchetto["template"]:
        for sensore in blocco.get("sensor", []) or []:
            if sensore.get("default_entity_id") == entita:
                return str(sensore["state"])
    raise AssertionError(entita)


# ------------------------------------------------------------------------------------------------------------ C2-2
def _imposta_meteo(hass: HomeAssistant, attributo: str, caso: str) -> None:
    """caso: «disponibile» (con l'attributo), «unavailable» (senza: HA toglie gli attributi del meteo),
    «assente»."""
    hass.states.async_set(ALTRO_METEO, "sunny", {attributo: 30})
    if caso == "disponibile":
        hass.states.async_set(METEO_PROVA, "cloudy", {attributo: 12.5, "friendly_name": "Prova"})
    elif caso == "unavailable":
        hass.states.async_set(METEO_PROVA, "unavailable", {"friendly_name": "Prova", "restored": True})
    else:
        hass.states.async_remove(METEO_PROVA)


@pytest.mark.parametrize("nome", METEO)
async def test_c2_2_opzioni_tengono_il_meteo_memorizzato(hass: HomeAssistant, nome: str) -> None:
    """C2-2: l'entita' meteo memorizzata in last_* resta tra le opzioni anche se non e' disponibile (senza
    l'attributo temperature/humidity), purche' esista ancora in HA; mai doppia; nessuna aggiunta se last_* e' vuoto,
    «Aggiorna Elenco…» o un'entita' che non c'e' piu'."""
    pacchetto = _pacchetto()
    attributo, _, ultimo, voce, _, _ = METEO[nome]
    modello = Template(_opzioni(pacchetto, nome), hass)
    hass.states.async_set("sensor.sonda_prova", "20", {"device_class": DEVICE_CLASS[nome]})
    hass.states.async_set("sensor.sonda_spenta", "unavailable", {"device_class": DEVICE_CLASS[nome]})

    def rendi(caso: str, ultima: str) -> list[str]:
        _imposta_meteo(hass, attributo, caso)
        hass.states.async_set(f"input_text.{ultimo}", ultima)
        opzioni = modello.async_render()
        assert isinstance(opzioni, list), (caso, ultima)
        assert len(opzioni) == len(set(opzioni)), (caso, ultima, opzioni)
        assert opzioni[0] == voce and ALTRO_METEO in opzioni, (caso, ultima, opzioni)
        # un sensore non disponibile tiene la device_class: resta nell'elenco (come negli altri 5 script)
        assert "sensor.sonda_spenta" in opzioni, (caso, ultima, opzioni)
        return opzioni

    assert rendi("disponibile", METEO_PROVA).count(METEO_PROVA) == 1
    assert rendi("disponibile", "").count(METEO_PROVA) == 1
    # b34: assente, la selezione tornava su «Aggiorna…»
    assert rendi("unavailable", METEO_PROVA).count(METEO_PROVA) == 1
    assert METEO_PROVA not in rendi("assente", METEO_PROVA)
    for ultima in ("", voce, "unknown", "Non disponibile", "weather.non_esiste"):
        assert METEO_PROVA not in rendi("unavailable", ultima), ultima
        assert "weather.non_esiste" not in rendi("unavailable", ultima), ultima
    # un sensore memorizzato non viene aggiunto una seconda volta
    assert rendi("unavailable", "sensor.sonda_spenta").count("sensor.sonda_spenta") == 1


async def _prepara_elenco(hass: HomeAssistant, nome: str, selezione_oggetto: str, ultimo_oggetto: str
                          ) -> dict[str, list[ServiceCall]]:
    """Script «Aggiorna Elenco» vero, con input_select e input_text veri; notifiche e update_entity registrati."""
    pacchetto = _pacchetto()
    assert await async_setup_component(
        hass, "input_select", {"input_select": {selezione_oggetto: pacchetto["input_select"][selezione_oggetto]}})
    assert await async_setup_component(
        hass, "input_text", {"input_text": {ultimo_oggetto: pacchetto["input_text"][ultimo_oggetto]}})
    chiamate: dict[str, list[ServiceCall]] = {"create": [], "dismiss": [], "update_entity": []}

    def registra(dominio: str, servizio: str) -> None:
        async def _registra(call: ServiceCall) -> None:
            chiamate[servizio].append(call)

        hass.services.async_register(dominio, servizio, _registra)

    registra("persistent_notification", "create")
    registra("persistent_notification", "dismiss")
    registra("homeassistant", "update_entity")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set("input_boolean.vmc_master_notifica_status_vmc", "on")
    hass.states.async_set("sensor.vmc_master_nome_status", "VMC Prova")
    nome_script = f"vmc_master_aggiorna_elenco_entita_{nome}"
    assert await async_setup_component(hass, "script", {"script": {nome_script: _script(pacchetto, nome)}})
    await hass.async_block_till_done()
    return chiamate


async def _scegli(hass: HomeAssistant, selezione: str, opzioni: list[str], scelta: str) -> None:
    await hass.services.async_call("input_select", "set_options", {"entity_id": selezione, "options": opzioni},
                                   blocking=True)
    await hass.services.async_call("input_select", "select_option", {"entity_id": selezione, "option": scelta},
                                   blocking=True)


async def _lancia(hass: HomeAssistant, nome: str) -> None:
    script = f"script.vmc_master_aggiorna_elenco_entita_{nome}"
    await hass.services.async_call("script", "turn_on", {"entity_id": script}, blocking=True)
    await hass.async_block_till_done()
    for _ in range(4):  # pause dello script: 2 s + 3 s
        async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=10))
        await hass.async_block_till_done()
    assert hass.states.get(script).state == "off", nome


# caso del meteo, selezione prima dell'aggiornamento, ultima scelta, selezione attesa dopo, notifica attesa
CASI_SCRIPT = {
    "disponibile": ("disponibile", METEO_PROVA, METEO_PROVA, METEO_PROVA, False),
    "unavailable": ("unavailable", METEO_PROVA, METEO_PROVA, METEO_PROVA, False),
    # selezione gia' su «Aggiorna Elenco…» (lasciata cosi' dalla b34): il meteo memorizzato torna subito
    "unavailable_da_aggiorna": ("unavailable", "VOCE", METEO_PROVA, METEO_PROVA, False),
    "assente": ("assente", METEO_PROVA, METEO_PROVA, "VOCE", True),
    "ultima_vuota": ("unavailable", "VOCE", "", "VOCE", True),
    "ultima_aggiorna": ("unavailable", "VOCE", "VOCE", "VOCE", True),
}


@pytest.mark.parametrize("caso", CASI_SCRIPT)
@pytest.mark.parametrize("nome", METEO)
async def test_c2_2_script_vero_meteo_non_disponibile(hass: HomeAssistant, nome: str, caso: str) -> None:
    """C2-2: corsa vera dello script. Meteo non disponibile ma presente in HA: la selezione resta sul meteo e la
    notifica «Aggiornare Manualmente l'Entità» non parte; meteo assente da HA o nessuna scelta memorizzata: come
    prima (selezione su «Aggiorna Elenco…», notifica, last_* invariato)."""
    attributo, selezione_oggetto, ultimo_oggetto, voce, notifica, _ = METEO[nome]
    selezione, ultimo = f"input_select.{selezione_oggetto}", f"input_text.{ultimo_oggetto}"
    meteo, prima, ultima, attesa = (voce if v == "VOCE" else v for v in CASI_SCRIPT[caso][:4])
    con_notifica = CASI_SCRIPT[caso][4]
    chiamate = await _prepara_elenco(hass, nome, selezione_oggetto, ultimo_oggetto)
    hass.states.async_set("sensor.sonda_prova", "20", {"device_class": DEVICE_CLASS[nome]})
    _imposta_meteo(hass, attributo, "disponibile")
    await _scegli(hass, selezione, [voce, METEO_PROVA, ALTRO_METEO, "sensor.sonda_prova"], prima)
    await hass.services.async_call("input_text", "set_value", {"entity_id": ultimo, "value": ultima}, blocking=True)
    _imposta_meteo(hass, attributo, meteo)

    await _lancia(hass, nome)

    assert hass.states.get(selezione).state == attesa, caso
    assert hass.states.get(ultimo).state == ultima, caso  # la memoria non cambia mai
    create = [c for c in chiamate["create"] if c.data.get("notification_id") == notifica]
    assert bool(create) is con_notifica, caso
    if con_notifica:
        assert create[0].data["message"].startswith("Aggiornare Manualmente l'Entità"), caso
    else:
        assert any(c.data.get("notification_id") == notifica for c in chiamate["dismiss"]), caso


@pytest.mark.parametrize("nome", METEO)
async def test_c2_2_il_valore_torna_da_solo(hass: HomeAssistant, nome: str) -> None:
    """C2-2: dopo l'aggiornamento dell'elenco con il meteo non disponibile, il sensore «…_selezionata» vale -100
    (la A2 usa la sonda della VMC o resta «Non disponibile»); quando il meteo torna il valore torna da solo, senza
    un nuovo aggiornamento dell'elenco."""
    attributo, selezione_oggetto, ultimo_oggetto, voce, _, selezionata = METEO[nome]
    selezione, ultimo = f"input_select.{selezione_oggetto}", f"input_text.{ultimo_oggetto}"
    await _prepara_elenco(hass, nome, selezione_oggetto, ultimo_oggetto)
    _imposta_meteo(hass, attributo, "disponibile")
    await _scegli(hass, selezione, [voce, METEO_PROVA], METEO_PROVA)
    await hass.services.async_call("input_text", "set_value", {"entity_id": ultimo, "value": METEO_PROVA},
                                   blocking=True)
    _imposta_meteo(hass, attributo, "unavailable")
    await _lancia(hass, nome)
    stato = Template(_stato_sensore(_pacchetto(), selezionata), hass)
    assert hass.states.get(selezione).state == METEO_PROVA
    assert stato.async_render() == -100
    _imposta_meteo(hass, attributo, "disponibile")
    await hass.async_block_till_done()
    assert hass.states.get(selezione).state == METEO_PROVA
    assert stato.async_render() == 12.5


def test_c2_2_commenti_aggiornati() -> None:
    """C2-2: i commenti sulla scrittura di last_* non dicono piu' che il meteo non pronto torna solo al prossimo
    aggiornamento dell'elenco; i due script del meteo spiegano che l'entita' meteo memorizzata resta nell'elenco."""
    testo = _testo("vmc_master.yaml")
    assert "per esempio meteo non ancora pronto all'avvio" not in testo
    assert testo.count("il prossimo aggiornamento dell'elenco la ripristina") == len(SCRIPT_ELENCO)
    pacchetto = _pacchetto()
    for nome in METEO:
        assert "states.weather | map(attribute='entity_id')" in _piatto(_opzioni(pacchetto, nome)), nome
        assert METEO[nome][2] in _opzioni(pacchetto, nome), nome


# ------------------------------------------------------------------------------------------------------------ C2-1
async def test_c2_1_delta_pdr_uguale_al_set(hass: HomeAssistant) -> None:
    """C2-1: con Δ PdR uguale al SET (valori a 2 decimali) la logica dice «Se ne sconsiglia l'impiego» (Foglio F6:
    superato con Δ PdR ≥ SET) e il testo dice «UGUALE»; 0,01 sotto: «Si può impiegare» e «MINORE»; 0,01 sopra:
    «Se ne sconsiglia» e «MAGGIORE». Su una griglia di SET da -10 a 10 e di PdR interni."""
    pacchetto = _pacchetto()
    logica = Template(_stato_sensore(pacchetto, "sensor.vmc_master_punto_di_rugiada_verifica_confronto"), hass)
    testo = Template(_stato_sensore(pacchetto, "sensor.vmc_master_punto_di_rugiada_verifica_confronto_valore"), hass)
    hass.states.async_set("sensor.vmc_master_sensori_memorizzata", "1")
    hass.states.async_set("sensor.vmc_master_punto_di_rugiada_interno_esterno_non_calcolabile", "Calcolabile")

    def rendi(pdri: float, pdre: float, soglia: float) -> tuple[str, str]:
        hass.states.async_set("sensor.vmc_master_punto_di_rugiada_interno", str(pdri))
        hass.states.async_set("sensor.vmc_master_punto_di_rugiada_esterno", str(pdre))
        hass.states.async_set("input_number.vmc_master_offset_verifica_impiego_vmc", str(soglia))
        return (_piatto(logica.async_render(parse_result=False)), _piatto(testo.async_render(parse_result=False)))

    assert rendi(6.03, 8.03, 2.0) == (
        "Se ne sconsiglia l'impiego",
        "Δ PUNTO DI RUGIADA RILEVATO 2.0 °C, UGUALE AL VALORE IMPOSTATO (2.0 °C).")
    diversi = []
    for decimi in range(-100, 101, 5):
        soglia = decimi / 10
        for centesimi in range(-1517, 3000, 97):
            pdri = centesimi / 100
            for scarto, atteso, parola in ((0, "Se ne sconsiglia l'impiego", "UGUALE"),
                                           (-0.01, "Si può impiegare", "MINORE"),
                                           (0.01, "Se ne sconsiglia l'impiego", "MAGGIORE")):
                pdre = round(pdri + soglia + scarto, 2)
                stato, frase = rendi(pdri, pdre, soglia)
                if stato != atteso or f"°C, {parola} DEL" not in frase and f"°C, {parola} AL" not in frase:
                    diversi.append((pdri, pdre, soglia, stato, frase))
    assert not diversi, diversi[:5]


def test_c2_1_differenza_arrotondata_in_entrambi() -> None:
    """C2-1: i due sensori confrontano la differenza arrotondata a 2 decimali."""
    pacchetto = _pacchetto()
    logica = _piatto(_stato_sensore(pacchetto, "sensor.vmc_master_punto_di_rugiada_verifica_confronto"))
    testo = _piatto(_stato_sensore(pacchetto, "sensor.vmc_master_punto_di_rugiada_verifica_confronto_valore"))
    assert "{% if ((PdRe_val - PdRi_val) | round(2)) < Delta %}" in logica
    assert "{% set diff_esatta = (PdRe_val - PdRi_val) | round(2) %}" in testo
    assert "{% if diff_esatta < Delta %}" in testo and "{% elif diff_esatta == Delta %}" in testo


# ------------------------------------------------------------------------------------------------------------ C2-4
def _dispositivi_omonimi(hass: HomeAssistant, nomi: tuple[str, ...]) -> None:
    """Dispositivi Mobile App veri nei registri (device_tracker con il dispositivo), come li crea l'app."""
    dispositivi, entita = dr.async_get(hass), er.async_get(hass)
    for i, nome in enumerate(nomi):
        voce = MockConfigEntry(domain="mobile_app", title=nome, entry_id=f"app{i}")
        voce.add_to_hass(hass)
        dispositivo = dispositivi.async_get_or_create(config_entry_id=voce.entry_id,
                                                      identifiers={("mobile_app", f"id{i}")}, name=nome)
        registrata = entita.async_get_or_create("device_tracker", "mobile_app", f"id{i}", config_entry=voce,
                                                device_id=dispositivo.id)
        entity_sources(hass)[registrata.entity_id] = {"domain": "mobile_app", "config_entry": voce.entry_id}


async def test_c2_4_opzioni_senza_doppi(hass: HomeAssistant) -> None:
    """C2-4: due dispositivi Mobile App con lo stesso nome danno una sola opzione (set_options rifiuta i doppi)."""
    _dispositivi_omonimi(hass, ("iPhone di prova", "iPhone di prova", "Pixel"))
    opzioni = Template(_opzioni(_pacchetto(), "notifica_dispositivo"), hass).async_render()
    assert opzioni == ["Aggiorna Elenco Dispositivi per Invio Notifica", "iphone_di_prova", "pixel"]


async def test_c2_4_script_vero_non_si_ferma(hass: HomeAssistant) -> None:
    """C2-4: corsa vera dello script con due dispositivi omonimi: l'elenco si aggiorna, la scelta memorizzata torna
    e lo script arriva in fondo (prima set_options alzava duplicate_options e lo script si fermava al primo passo)."""
    selezione_oggetto, ultimo_oggetto = "vmc_master_selected_notification_device", "vmc_master_last_notification_device"
    chiamate = await _prepara_elenco(hass, "notifica_dispositivo", selezione_oggetto, ultimo_oggetto)
    _dispositivi_omonimi(hass, ("iPhone di prova", "iPhone di prova"))
    await hass.services.async_call("input_text", "set_value",
                                   {"entity_id": f"input_text.{ultimo_oggetto}", "value": "iphone_di_prova"},
                                   blocking=True)
    await _lancia(hass, "notifica_dispositivo")
    stato = hass.states.get(f"input_select.{selezione_oggetto}")
    assert stato.attributes["options"] == ["Aggiorna Elenco Dispositivi per Invio Notifica", "iphone_di_prova"]
    assert stato.state == "iphone_di_prova"
    assert not chiamate["create"] and chiamate["update_entity"]


@pytest.mark.parametrize("nome", SCRIPT_ELENCO)
def test_c2_4_unique_in_tutti_gli_elenchi(nome: str) -> None:
    """C2-4: tutti e 7 i template delle opzioni tolgono i doppi prima di passarli a set_options."""
    assert "| unique | list" in _piatto(_opzioni(_pacchetto(), nome)), nome


# ------------------------------------------------------------------------------------------------------------ C2-3
ECCEZIONI_140 = ("(anche l'avvio a Velocità 1 per Inquinanti durante un'allerta Lim. Δ Punto di Rugiada già in "
                 "corso prima del riavvio e la Velocità 0 già mantenuta dall'Umidità possono riprendere prima)")


def test_c2_3_eccezioni_del_riavvio_scritte() -> None:
    """C2-3: la descrizione del Riallineamento e la Nota Avvio di HA della scheda scrivono anche le eccezioni dei
    trigger 155/157 (Velocità 1 per Inquinanti durante un'allerta Lim. Δ PdR, memoria un_solo_avvio) e del trigger
    umidita_velocita_0 (Velocità 0 mantenuta dall'Umidità), che il codice continua ad avere."""
    automazioni = _pacchetto()["automation"]
    riallineamento = next(a for a in automazioni if a["id"] == "vmc_master_riallineamento_allerte_al_riavvio")
    descrizione = _piatto(riallineamento["description"])
    assert ("dopo altri 40 s Lim. Δ Punto di Rugiada, Free Cool./Heat., Calendario e Umidità " + ECCEZIONI_140
            + ".") in descrizione
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    i = scheda.index("<strong>Nota Avvio di Home Assistant</strong>")
    nota = _piatto(scheda[i: scheda.index("<br>", i)])
    assert ("dopo 140 secondi Lim. Δ Punto di Rugiada, Free Cool./Heat., Calendario e Umidità " + ECCEZIONI_140
            + ".") in nota
    automazione = _testo("vmc_master_automazione.txt")
    fase = "states('input_number.vmc_master_fase_riallineamento_al_riavvio') | float(0) >= 4 or "
    assert automazione.count(fase + "(states('input_boolean.vmc_master_spia_velocita_0_un_solo_avvio') == 'on'") == 4
    umidita = "states('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0') == 'on')"
    assert automazione.count(fase + umidita) == 2
