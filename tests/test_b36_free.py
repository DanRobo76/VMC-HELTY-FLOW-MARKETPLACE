"""Prove della b36, fetta «ripresa Free»: difetto trovato dal simulatore con HA vero (gia' nella b35).

Free Cooling/Heating sospesa (ripresa in attesa), allerta Umidita' accesa (VMC a Velocita' 1, nota 3), Inquinanti e PdR
che finiscono quasi insieme: a fine Inquinanti la VMC resta a Velocita' 1 (nota 3, automatica) e il ripristino di fine
PdR («Rip. Free Cool./Heat. No PdR») prendeva quella Velocita' 1 per una velocita' scelta dall'utente e non ancora
memorizzata: spegneva anche le spie della ripresa Free, la ripresa si perdeva e a fine Umidita' la VMC restava a
Velocita' 1 invece di tornare a Velocita' 0 e poi in Free.

Foglio Logiche 21-11-2026: righe 15 e 19 (Free sospesa: con l'allerta Umidita' Velocita' 1 [NOTA 3]), F6 (a fine PdR
ripristino della velocita'), NOTA 2 N.B. (solo un'altra velocita' scelta annulla la ripresa), NOTA 3 N.B. (ad allerta
terminata ripresa automatica), A21 N.B. (con la sospensione Free l'Umidita' parte comunque a Velocita' 1 [NOTA 3]; con
[Set Velocita' Umidita' di Avvio] su Velocita' 0 la VMC resta ferma, quindi la Velocita' 1 e' una scelta dell'utente).

Ora con l'Umidita' accesa, il Set diverso da Velocita' 0 e la Free sospesa la Velocita' 1 e' gia' la velocita' di fine
allerta: la VMC resta a Velocita' 1, si spengono solo le memorie PdR e la ripresa Free resta in attesa. Con il Set a
Velocita' 0, senza Umidita', senza la Free sospesa o con un'altra velocita' tutto come prima.
"""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import (
    ALLERTA_UMIDITA,
    FREE_C,
    FREE_H,
    LETTURA,
    MEMORIE_PDR,
    SPIA_U0,
    SPIA_UMIDITA,
    _automazione,
    _copia_guardia,
    _copie_countdown,
    _norm,
    _ramo,
    _spente,
    _testo,
    _trigger,
)
from tests.test_b36_allerte import SET_UMIDITA, _esegui, _stato

TID = "Rip. Free Cool./Heat. No PdR"
MEMORIA_PDR_FREE = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio"
FERMO_NOTA_3 = "Velocità 1 dell'allerta Umidità con la Free sospesa mantenuta [Nota 3]: la ripresa Free resta in attesa"
FERMO_UTENTE = "Velocità scelta dall'utente durante l'allerta PdR mantenuta"


def _stati(**altri: str) -> dict[str, str]:
    """Fine PdR con la memoria PdR Free: Free Cooling sospesa, Umidita' in corso con il Set a Velocita' 2, VMC a
    Velocita' 1 (nota 3)."""
    stati = {SPIA_UMIDITA: "on", SPIA_U0: "off", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Velocità 2",
             **_spente(MEMORIE_PDR), MEMORIA_PDR_FREE: "on", FREE_C: "on", FREE_H: "off", LETTURA: "Velocità 1",
             "binary_sensor.vmc_master_black_out_rilevato": "off"}
    stati.update(altri)
    return stati


def _passi() -> list[dict[str, Any]]:
    return _ramo(TID)["sequence"]


def test_passo_nuovo_prima_della_protezione_della_scelta_dell_utente() -> None:
    """Il passo sta dopo la memoria della velocita' prima del comando e subito prima della protezione «velocita'
    scelta dall'utente»; non manda comandi e non spegne nulla (le memorie PdR le ha gia' spente il ciclo)."""
    passi = _passi()
    (k,) = [k for k, p in enumerate(passi) if p.get("then") == [{"stop": FERMO_NOTA_3}]]
    assert "vel_prima_del_comando" in passi[k - 1].get("variables", {})
    assert passi[k + 1]["then"][-1] == {"stop": FERMO_UTENTE}
    condizione = _norm(passi[k]["if"][0]["value_template"])
    for parte in ("vel_prima_del_comando == 'Velocità 1'",
                  "states('input_boolean.vmc_master_umidita_verifica_soglia_valore_spia') == 'on'",
                  "states('input_select.vmc_master_speed_umidita') != 'Velocità 0'",
                  f"states('{FREE_C}') == 'on' or states('{FREE_H}') == 'on'"):
        assert parte in condizione, parte
    cv.SCRIPT_SCHEMA(passi)


def test_trigger_e_copie_non_cambiano() -> None:
    """Cambia solo il ramo: il trigger (con «for») e le sue copie nella guardia e nel Countdown restano identici."""
    modello = _norm(_trigger(TID)["value_template"])
    assert _norm(_copia_guardia(TID)) == modello
    accesa, spenta = _copie_countdown(TID)
    assert _norm(accesa) == modello
    assert modello in _norm(spenta)


@pytest.mark.parametrize(("free", "valore_set"), [
    ({FREE_C: "on"}, "Velocità 2"),
    ({FREE_C: "off", FREE_H: "on"}, "Velocità 2"),  # Free Heating sospesa
    ({FREE_C: "on"}, "Velocità 1"),
    ({FREE_C: "on"}, "Free Cool./Heat."),
    ({FREE_C: "on"}, "Iperventilazione"),
])
async def test_velocita_1_della_nota_3_resta_e_la_ripresa_free_resta_in_attesa(
        hass: HomeAssistant, free: dict[str, str], valore_set: str) -> None:
    """Il caso del simulatore (B4|U|-|SAME): nessun comando, memorie PdR spente, spie della ripresa Free accese."""
    comandi = await _esegui(hass, _passi(), _stati(**free, **{SET_UMIDITA: valore_set}), attesa=0.5)
    assert comandi == []
    assert all(_stato(hass, e) == "off" for e in MEMORIE_PDR)
    for entita, valore in free.items():
        assert _stato(hass, entita) == valore, entita


async def test_umidita_appena_rientrata_ma_ancora_accesa_vale_lo_stesso(hass: HomeAssistant) -> None:
    """Umidita' rientrata ma allerta ancora accesa (i 28 s della fine): la Velocita' 1 e' ancora quella della nota 3
    (la VMC non era partita da Velocita' 0, quindi non vale il controllo in testa al ramo)."""
    comandi = await _esegui(hass, _passi(), _stati(**{ALLERTA_UMIDITA: "Nessuna Allerta"}), attesa=0.5)
    assert comandi == []
    assert _stato(hass, FREE_C) == "on"


@pytest.mark.parametrize("altri", [
    {SET_UMIDITA: "Velocità 0"},  # Set 0: l'Umidita' non da' mai la Velocita' 1, e' una scelta dell'utente (ce550e1)
    {SPIA_UMIDITA: "off", ALLERTA_UMIDITA: "Nessuna Allerta"},  # senza Umidita'
    {FREE_C: "off"},  # Free non sospesa
    {LETTURA: "Velocità 2"},  # un'altra velocita' scelta dall'utente
    {LETTURA: "Notturna"},
])
async def test_altrimenti_la_scelta_dell_utente_vince_come_prima(hass: HomeAssistant, altri: dict[str, str]) -> None:
    comandi = await _esegui(hass, _passi(), _stati(**altri), attesa=0.5)
    assert comandi == []
    assert _stato(hass, FREE_C) == "off" and _stato(hass, FREE_H) == "off"
    assert all(_stato(hass, e) == "off" for e in MEMORIE_PDR)


@pytest.mark.parametrize(("letta", "comando"), [("Velocità 0", "vmc_master_velocita_0")])
async def test_vmc_ferma_ripristino_come_prima(hass: HomeAssistant, letta: str, comando: str) -> None:
    """Con la VMC a Velocita' 0 (PdR finito dopo la fine degli Inquinanti) il ripristino manda ancora la Velocita' 0."""
    comandi = await _esegui(hass, _passi(), _stati(**{LETTURA: letta}), attesa=0.5)
    assert comandi[:1] == [comando]
    assert _stato(hass, FREE_C) == "on"


async def test_free_non_sospesa_vmc_ferma_riparte_in_free_come_prima(hass: HomeAssistant) -> None:
    comandi = await _esegui(hass, _passi(), _stati(**{FREE_C: "off", LETTURA: "Velocità 0"}), attesa=0.5)
    assert comandi[:1] == ["vmc_master_freecooling"]


def test_nessun_tempo_nuovo_nel_ramo() -> None:
    """Il passo nuovo non aggiunge attese: le stesse delay/wait/for/timeout del ramo della b36 (354efe3)."""
    testo = _testo("vmc_master_automazione.txt")
    inizio = testo.index(f"            id: {TID}\n        sequence:")
    fine = testo.index("            id: Rip. Iperventilazione No PdR\n        sequence:")
    ramo = testo[inizio:fine]
    assert ramo.count("delay:") == 2
    assert "wait_" not in ramo and "timeout" not in ramo and "for:" not in ramo
    assert len(_automazione()["triggers"]) > 0
