"""Prove della b40.

free_v0 (decisioni 1, 2 e 3 del proprietario, 23-11-2026; possibili difetti FX-D1, FX-D2 e FX-D2b della famiglia FX del
simulatore, b39): Free Cool./Heat. sospesa (Spia Free Heating o Free Cooling «un solo avvio per programmazione» accesa,
VMC ferma in attesa della ripresa) e Velocità 0 scelta dall'utente.
- Decisione 1 (FX-D1): con un'allerta Δ Temp. in corso (VMC a Velocità 1) la Velocità 0 scelta resta e annulla la ripresa
  in Free, come con gli Inquinanti: nel ramo Δ ON, opzione «Velocità 0», per la scelta memorizzata (trigger
  spia_velocita_0_delta_temp, non per l'avvio dell'allerta con la VMC già ferma) e nel passo di fine Δ per la scelta
  fatta negli ultimi Secondi (C3-1, Foglio D6).
- Decisioni 2 e 3 (FX-D2, FX-D2b): con l'allerta Umidità in corso, la Free sospesa e [Set Velocità Umidità di Avvio]
  diversa da Velocità 0, la Velocità 0 scelta riporta la VMC alla Velocità 1 [Nota 3] (Foglio A21, A27), con l'Umidità
  partita a Free già sospesa (memoria Free) o prima della sospensione (memoria Free), e con l'Umidità partita da
  Velocità 0 con la Velocità di avvio Free Cool./Heat.: trigger «Umidità ON Vel. 0» (con le sue 3 copie) e primo passo
  del suo ramo.
- Regola del 24-11-2026 (coordinatore, gemella della decisione 1 nella fine Inquinanti, C3-2): nell'attesa di 8 s della
  fine Inquinanti con la Free sospesa, la Velocità 0 scelta e non ancora memorizzata resta e annulla la ripresa in Free;
  non vale per gli Inquinanti partiti da ferma o riavviati da Velocità 0, per la Velocità 0 già memorizzata e con
  l'allerta Umidità in corso.
La verifica dinamica (HA vero, VMC simulata) è nel simulatore: famiglia FX, classe di 112 scenari (tasto Velocità 0 con
la VMC in Free) e scenari mirati in /home/user/sim/simulatore-b36/b40/free_v0/."""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import (
    FREE_C,
    FREE_H,
    LETTURA,
    SPIA_U0,
    _copia_guardia,
    _copie_countdown,
    _imposta,
    _norm,
    _ramo,
    _rami,
    _render,
    _stati_fine_delta,
    _testo,
    _trigger,
)
from tests.test_b36_allerte import (
    MEMORIE_CO2,
    PARTENZA,
    SET_UMIDITA,
    SPIA_CO2,
    SPIA_U0_MANTENUTA,
    SPIA_U_FREE,
    SPIA_UMIDITA,
    _esegui,
    _passi_fine_inquinanti,
    _stati_fine_inquinanti,
    _stato,
)

ALLERTA_UMIDITA = "sensor.vmc_master_alert_monitoraggio_umidita"
BLACK_OUT_RILEVATO = "binary_sensor.vmc_master_black_out_rilevato"

# ------------------------------------------------------------------------------------------------ free_v0
FREE_V0_CLAUSOLA = (
    f"( (states('{FREE_C}') == 'off' and states('{FREE_H}') == 'off') or "
    f"(states('{ALLERTA_UMIDITA}') == 'Allerta' and states('{SET_UMIDITA}') != 'Velocità 0' and "
    f"(states('{SPIA_U_FREE}') == 'on' or states('{SPIA_U0}') == 'on')) )"
)
FREE_V0_SOSPESA = f"(is_state('{FREE_C}', 'on') or is_state('{FREE_H}', 'on'))"


def _free_v0_opzione_delta_velocita_0() -> dict[str, Any]:
    """Opzione «Velocità 0» del ramo Δ ON (trigger delta_temp_ON e le 8 memorie della velocità scelta)."""
    (ramo,) = [r for r in _rami() if "'delta_temp_ON'" in str(r["conditions"]) or "['delta_temp_ON']" in str(r["conditions"])]
    (scelta,) = [p for p in ramo["sequence"] if "choose" in p and str(p.get("alias", "")).startswith("Attivazione Velocità Spia Δ")]
    opzione = scelta["choose"][0]
    assert "spia_velocita_0_delta_temp" in str(opzione["conditions"])
    return opzione


def test_free_v0_umidita_v0_condizione_in_tutte_le_copie() -> None:
    """Decisioni 2-3: la condizione delle spie Free del trigger «Umidità ON Vel. 0» (prima le chiedeva spente) è la
    stessa nel trigger, nella copia «Evento ancora valido» e nelle 2 copie del Countdown Attese (ON uguale, OFF che la
    contiene)."""
    modello = _norm(_trigger("umidita_velocita_0")["value_template"])
    assert modello.count(_norm(FREE_V0_CLAUSOLA)) == 1
    assert _norm(_copia_guardia("umidita_velocita_0")) == modello
    accesa, spenta = _copie_countdown("umidita_velocita_0")
    assert _norm(accesa) == modello
    assert modello in _norm(spenta)
    # 2 copie nell'automazione (trigger e guardia) e 2 nel package (Countdown ON e OFF), nessun'altra
    assert _norm(_testo("vmc_master_automazione.txt")).count(_norm(FREE_V0_CLAUSOLA)) == 2
    assert _norm(_testo("vmc_master.yaml")).count(_norm(FREE_V0_CLAUSOLA)) == 2


@pytest.mark.parametrize(
    ("stati", "atteso"),
    [
        # Free non sospesa: come prima, qualunque sia l'Umidità
        ({FREE_C: "off", FREE_H: "off", ALLERTA_UMIDITA: "Nessuna Allerta"}, True),
        ({FREE_C: "off", FREE_H: "off", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Velocità 0"}, True),
        # Free sospesa, Umidità in corso con la memoria Free (FX-D2, FX-D2b) o partita da Velocità 0 (Set Free)
        ({FREE_C: "on", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Velocità 2", SPIA_U_FREE: "on"}, True),
        ({FREE_H: "on", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Free Cool./Heat.", SPIA_U0: "on"}, True),
        # Set Velocità 0 (A21: la VMC resta ferma), nessuna memoria Free o Velocità 0, Umidità non in corso
        ({FREE_C: "on", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Velocità 0", SPIA_U_FREE: "on"}, False),
        ({FREE_H: "on", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Velocità 2"}, False),
        ({FREE_C: "on", ALLERTA_UMIDITA: "Nessuna Allerta", SET_UMIDITA: "Velocità 2", SPIA_U_FREE: "on"}, False),
    ],
)
async def test_free_v0_umidita_v0_condizione_free_sospesa(hass: HomeAssistant, stati: dict[str, str], atteso: bool) -> None:
    base = {FREE_C: "off", FREE_H: "off", ALLERTA_UMIDITA: "Allerta", SET_UMIDITA: "Velocità 2", SPIA_U_FREE: "off",
            SPIA_U0: "off"}
    for entita, stato in {**base, **stati}.items():
        hass.states.async_set(entita, stato)
    assert _render(hass, "{{ " + FREE_V0_CLAUSOLA + " }}") is atteso


def _free_v0_stati_umidita(**altri: str) -> dict[str, str]:
    stati = {LETTURA: "Velocità 0", BLACK_OUT_RILEVATO: "off", FREE_C: "off", FREE_H: "off", SET_UMIDITA: "Velocità 2",
             SPIA_U0: "off", SPIA_U0_MANTENUTA: "off", SPIA_U_FREE: "off"}
    stati.update(altri)
    return stati


@pytest.mark.parametrize(
    "altri",
    [
        {FREE_H: "on", SPIA_U_FREE: "on"},  # FX-D2 / FX-D2b, Free Heating
        {FREE_C: "on", SPIA_U_FREE: "on", SET_UMIDITA: "Free Cool./Heat."},  # Free Cooling, Set Free
        {FREE_C: "on", SPIA_U0: "on", SET_UMIDITA: "Free Cool./Heat."},  # Umidità partita da Velocità 0 (U3 darebbe V1)
    ],
)
async def test_free_v0_umidita_v0_con_free_sospesa_torna_a_velocita_1(hass: HomeAssistant, altri: dict[str, str]) -> None:
    """Decisioni 2-3: primo passo del ramo «Umidità ON Vel. 0»: con la Free sospesa la VMC torna alla Velocità 1 [Nota 3];
    le memorie dell'Umidità non cambiano (niente Velocità 0 mantenuta) e la ripresa Free resta in attesa."""
    stati = _free_v0_stati_umidita(**altri)
    comandi = await _esegui(hass, _ramo("umidita_velocita_0")["sequence"], stati,
                            variabili={"trigger": {"id": "umidita_velocita_0"}})
    assert comandi == ["vmc_master_velocita_1"]
    for entita in (FREE_C, FREE_H, SPIA_U0, SPIA_U0_MANTENUTA, SPIA_U_FREE):
        assert _stato(hass, entita) == stati[entita], entita


async def test_free_v0_umidita_v0_senza_free_sospesa_come_prima(hass: HomeAssistant) -> None:
    """Senza Free sospesa il passo non vale: l'Umidità partita da Velocità 0 rimanda la velocità di avvio (correzione U3);
    con il Set Velocità 0 il passo non vale nemmeno con la Free sospesa (nessuna Velocità 1)."""
    comandi = await _esegui(hass, _ramo("umidita_velocita_0")["sequence"], _free_v0_stati_umidita(**{SPIA_U0: "on"}),
                            variabili={"trigger": {"id": "umidita_velocita_0"}})
    assert comandi == ["vmc_master_velocita_2"]
    comandi = await _esegui(hass, _ramo("umidita_velocita_0")["sequence"],
                            _free_v0_stati_umidita(**{FREE_C: "on", SPIA_U_FREE: "on", SET_UMIDITA: "Velocità 0"}),
                            variabili={"trigger": {"id": "umidita_velocita_0", "from_state": None}})
    assert "vmc_master_velocita_1" not in comandi


def test_free_v0_umidita_v0_passo_prima_della_u3() -> None:
    """Il passo della Free sospesa è il primo del ramo e finisce con «stop» (la U3 e la Velocità 0 mantenuta non
    partono); la condizione è quella delle copie del trigger."""
    passo, u3 = _ramo("umidita_velocita_0")["sequence"]
    assert "Free Cool./Heat. sospesa" in passo["alias"] and "(correzione U3)" in u3["alias"]
    assert passo["if"][0]["value_template"] == (
        "{{ " + FREE_V0_SOSPESA + f" and states('{SET_UMIDITA}') != 'Velocità 0' }}}}")
    variabili, ciclo, fermo = passo["then"]
    assert ciclo["repeat"]["sequence"][0]["action"] == "shell_command.vmc_master_velocita_1"
    assert "== 'Velocità 1'" in ciclo["repeat"]["until"][0]["value_template"]
    assert set(fermo) == {"stop"}


@pytest.mark.parametrize(
    ("trigger_id", "free", "spenta"),
    [
        ("spia_velocita_0_delta_temp", FREE_C, True),  # FX-D1: scelta memorizzata durante il Δ
        ("spia_velocita_0_delta_temp", FREE_H, True),
        ("delta_temp_ON", FREE_C, False),  # avvio del Δ con la VMC ferma per la Free sospesa: la ripresa resta
        ("delta_temp_ON", FREE_H, False),
        ("spia_velocita_0_delta_temp|umidita", FREE_C, False),  # Umidità in corso: la ripresa resta (24-11-2026)
        ("spia_velocita_0_delta_temp|umidita", FREE_H, False),
    ],
)
async def test_free_v0_delta_velocita_0_annulla_la_ripresa(hass: HomeAssistant, trigger_id: str, free: str,
                                                           spenta: bool) -> None:
    """Decisione 1: opzione «Velocità 0» del ramo Δ ON: la Velocità 0 scelta durante il Δ con la Free sospesa spegne le 2
    spie Free (ripresa annullata); all'avvio dell'allerta con la VMC già ferma la ripresa resta in attesa; con
    un'allerta Umidità in corso la ripresa resta e a fine Δ la VMC torna a Velocità 1 [Nota 3] (regola del 24-11-2026)."""
    opzione = _free_v0_opzione_delta_velocita_0()
    trigger_id, _, umidita = trigger_id.partition("|")
    stati = {LETTURA: "Velocità 0", BLACK_OUT_RILEVATO: "off", FREE_C: "off", FREE_H: "off", free: "on",
             SPIA_UMIDITA: "on" if umidita else "off"}
    await _esegui(hass, opzione["sequence"], stati, attesa=0.5, variabili={"trigger": {"id": trigger_id}})
    assert _stato(hass, free) == ("off" if spenta else "on")


@pytest.mark.parametrize(
    ("letta", "free", "ripresa", "comando", "umidita"),
    [
        ("Velocità 0", FREE_C, "off", None, "off"),  # scelta negli ultimi Secondi: resta e annulla la ripresa
        ("Velocità 0", FREE_H, "off", None, "off"),
        ("Velocità 3", FREE_H, "on", None, "off"),  # altre velocità: resta, la ripresa la annulla il trigger dei 20 s
        ("Velocità 1", FREE_C, "on", "vmc_master_velocita_2", "off"),  # nessuna scelta: ripristino come prima
        ("Velocità 0", FREE_C, "on", None, "on"),  # Umidità in corso: la ripresa resta, Velocità 1 dal ramo Umidità
        ("Velocità 0", FREE_H, "on", None, "on"),
    ],
)
async def test_free_v0_fine_delta_velocita_0_annulla_la_ripresa(hass: HomeAssistant, letta: str, free: str, ripresa: str,
                                                                comando: str | None, umidita: str) -> None:
    """Decisione 1, passo di fine Δ (C3-1, Foglio D6): la Velocità 0 scelta quando non è ancora memorizzata resta e, con
    la Free sospesa, annulla la ripresa, come la Velocità 0 memorizzata durante l'allerta; non con un'allerta Umidità in
    corso (regola del 24-11-2026): la ripresa resta e la Velocità 1 [Nota 3] la manda il ramo «Umidità ON Vel. 0»."""
    comandi = await _esegui(hass, _ramo("delta_temp_OFF")["sequence"],
                            _stati_fine_delta(**{LETTURA: letta, FREE_C: "off", FREE_H: "off", free: "on",
                                                 SPIA_UMIDITA: umidita}), attesa=0.5)
    assert comandi[:1] == ([comando] if comando else [])
    assert _stato(hass, free) == ripresa


async def test_free_v0_rami_validi_e_alias_chiari(hass: HomeAssistant) -> None:
    """I 3 rami cambiati sono validi per Home Assistant; gli alias nuovi sono in italiano chiaro (senza entity_id)."""
    for tid in ("umidita_velocita_0", "delta_temp_OFF"):
        cv.SCRIPT_SCHEMA(_ramo(tid)["sequence"])
    cv.SCRIPT_SCHEMA(_free_v0_opzione_delta_velocita_0()["sequence"])
    alias = [_ramo("umidita_velocita_0")["sequence"][0]["alias"], _ramo("umidita_velocita_0")["alias"],
             _free_v0_opzione_delta_velocita_0()["sequence"][0]["alias"], _trigger("umidita_velocita_0")["alias"]]
    alias += [p["alias"] for p in _ramo("delta_temp_OFF")["sequence"][2]["then"] if "alias" in p]
    nuovi = [a for a in alias if "23-11-2026" in a or "Free Cool./Heat. sospesa" in a]
    assert len(nuovi) == 5, alias
    for a in nuovi:
        assert "input_boolean" not in a and "vmc_master" not in a and "master" not in a, a


# ------------------------------------------------------------------------------------------------ free_v0, fine Inquinanti
INQ_0 = "input_boolean.vmc_master_spia_velocita_0_co2_o_voc"
INQ_1 = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc"
INQ_FREE = "input_boolean.vmc_master_spia_velocita_freecooling_co2_o_voc"
FREE_V0_FINE_INQUINANTI = (
    "vel_fine_inquinanti == 'Velocità 0' and " + FREE_V0_SOSPESA + f" and is_state('{SPIA_UMIDITA}', 'off') and "
    f"is_state('{PARTENZA}', 'off') and is_state('{INQ_0}', 'off')")


@pytest.mark.parametrize(
    ("memorie", "letta", "free", "ripresa"),
    [
        ({INQ_1: "on"}, "Velocità 0", FREE_C, "off"),  # Inquinanti con la Free già sospesa: la Velocità 0 resta
        ({INQ_1: "on"}, "Velocità 0", FREE_H, "off"),
        ({INQ_FREE: "on"}, "Velocità 0", FREE_H, "off"),  # Free sospesa durante gli Inquinanti partiti in Free
        ({INQ_1: "on", PARTENZA: "on"}, "Velocità 0", FREE_C, "on"),  # riavviati da Velocità 0: non è una scelta
        ({INQ_1: "on", SPIA_UMIDITA: "on"}, "Velocità 0", FREE_C, "on"),  # Umidità in corso: Velocità 1 [Nota 3]
        ({INQ_1: "on"}, "Velocità 3", FREE_C, "on"),  # altre velocità: la ripresa la annulla il trigger dei 20 s
        ({INQ_1: "on"}, "Velocità 1", FREE_H, "on"),  # nessuna scelta: ripresa in attesa
    ],
)
async def test_free_v0_fine_inquinanti_velocita_0_annulla_la_ripresa(hass: HomeAssistant, memorie: dict[str, str],
                                                                     letta: str, free: str, ripresa: str) -> None:
    """Regola del 24-11-2026 (C3-2, Foglio E6 e A29): la Velocità 0 scelta nell'attesa della fine Inquinanti con la Free
    sospesa resta (nessun comando, memorie Inquinanti spente) e annulla la ripresa in Free (spie Free spente)."""
    stati = _stati_fine_inquinanti(**{**memorie, LETTURA: letta, free: "on"})
    comandi = await _esegui(hass, _ramo("inquinanti_co2_voc_off")["sequence"], stati)
    assert _stato(hass, free) == ripresa
    if ripresa == "off":
        assert comandi == []
        assert all(_stato(hass, e) == "off" for e in (SPIA_CO2, PARTENZA, *MEMORIE_CO2))
        assert _stato(hass, FREE_C if free == FREE_H else FREE_H) == "off"


async def test_free_v0_fine_inquinanti_velocita_0_memorizzata_come_prima(hass: HomeAssistant) -> None:
    """La Velocità 0 già memorizzata durante l'allerta non passa dalla regola nuova: ripristino a Velocità 0 di prima."""
    variabili, protezione, _ = _passi_fine_inquinanti()
    stati = _stati_fine_inquinanti(**{INQ_0: "on", LETTURA: "Velocità 0", FREE_C: "on"})
    _imposta(hass, stati)
    ripristino = _render(hass, variabili["variables"]["vel_ripristino_inquinanti"])
    assert ripristino == "Velocità 0"
    assert _render(hass, protezione["if"][0]["value_template"],
                   {"vel_ripristino_inquinanti": ripristino, "vel_fine_inquinanti": "Velocità 0"}) is False


async def test_free_v0_fine_inquinanti_passo_nella_protezione(hass: HomeAssistant) -> None:
    """Il passo nuovo è nella protezione C3-2, dopo lo spegnimento delle memorie e prima dello «stop»; la condizione
    della protezione contiene la stessa clausola; il ramo è valido e l'alias è in italiano chiaro."""
    _, protezione, _ = _passi_fine_inquinanti()
    assert "(" + FREE_V0_FINE_INQUINANTI + ")" in protezione["if"][0]["value_template"]
    passo = protezione["then"][-2]
    assert "stop" in protezione["then"][-1]
    assert passo["if"][0]["value_template"] == "{{ " + FREE_V0_FINE_INQUINANTI + " }}"
    assert passo["then"] == [{"data": {}, "target": {"entity_id": [FREE_C, FREE_H]}, "action": "input_boolean.turn_off"}]
    assert not any("shell_command" in str(p) for p in protezione["then"])
    cv.SCRIPT_SCHEMA(_ramo("inquinanti_co2_voc_off")["sequence"])
    for a in (passo["alias"], protezione["alias"]):
        assert "24-11-2026" in a and "input_boolean" not in a and "vmc_master" not in a and "master" not in a, a


def test_free_v0_delta_velocita_0_esclusa_con_l_umidita() -> None:
    """Le 2 copie del Δ (opzione «Velocità 0» del Δ ON e passo C3-1) hanno l'esclusione «Umidità in corso» con la stessa
    definizione della fine Inquinanti (Spia Umidità accesa); gli alias la dicono senza entity_id."""
    umidita = f"is_state('{SPIA_UMIDITA}', 'off')"
    passo_on = _free_v0_opzione_delta_velocita_0()["sequence"][0]
    (passo_fine,) = [p for p in _ramo("delta_temp_OFF")["sequence"][2]["then"] if "vel_fine_delta == 'Velocità 0'" in str(p)]
    assert passo_on["if"][0]["value_template"] == (
        "{{ trigger.id == 'spia_velocita_0_delta_temp' and " + FREE_V0_SOSPESA + f" and {umidita} }}}}")
    assert passo_fine["if"][0]["value_template"] == (
        "{{ vel_fine_delta == 'Velocità 0' and " + FREE_V0_SOSPESA + f" and {umidita} }}}}")
    assert umidita in FREE_V0_FINE_INQUINANTI
    for a in (passo_on["alias"], passo_fine["alias"]):
        assert "Umidità in corso" in a and "24-11-2026" in a and "[Nota 3]" in a and "vmc_master" not in a, a


# ------------------------------------------------------------------------------------------------ free_v0, Velocità 0 negli Inquinanti
def _free_v0_inquinanti_v0_scelta() -> list[dict[str, Any]]:
    """Ramo spia_velocita_0_inquinanti_co2_voc, opzione della Free sospesa (memoria Inquinanti accesa, Velocità 0 e una
    spia Free accesa), ramo «else»: la Velocità 0 scelta dall'utente dopo l'avvio dell'allerta."""
    opzione = _ramo("spia_velocita_0_inquinanti_co2_voc")["sequence"][0]["choose"][2]
    assert "Spia un solo Avvio FreeCooling o Heating ON" in opzione["alias"] and "Almeno una Spia" in opzione["alias"]
    return opzione["sequence"][0]["else"]


@pytest.mark.parametrize(
    ("free", "umidita", "ripresa"),
    [
        (FREE_C, "off", "off"),  # come prima: la Velocità 0 scelta annulla la ripresa (riferimento della decisione 1)
        (FREE_H, "off", "off"),
        (FREE_C, "on", "on"),  # Umidità in corso: la ripresa resta, Velocità 1 [Nota 3] a fine Inquinanti
        (FREE_H, "on", "on"),
    ],
)
async def test_free_v0_inquinanti_velocita_0_con_l_umidita(hass: HomeAssistant, free: str, umidita: str,
                                                           ripresa: str) -> None:
    """Regola del 24-11-2026 (ultima copia gemella): la Velocità 0 scelta durante gli Inquinanti con la Free sospesa
    riavvia la VMC a Velocità 1 come prima; le spie Free si spengono solo senza un'allerta Umidità in corso."""
    stati = {LETTURA: "Velocità 0", BLACK_OUT_RILEVATO: "off", FREE_C: "off", FREE_H: "off", free: "on",
             SPIA_UMIDITA: umidita, INQ_1: "on", SPIA_CO2: "on", PARTENZA: "off"}
    comandi = await _esegui(hass, _free_v0_inquinanti_v0_scelta(), stati, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_1"]
    assert _stato(hass, free) == ripresa
    assert _stato(hass, PARTENZA) == "on" and _stato(hass, INQ_1) == "on"


def test_free_v0_inquinanti_velocita_0_passo_nuovo() -> None:
    """Le spie Free non sono più nell'elenco spento dal ciclo della Velocità 1: le spegne il passo nuovo prima del ciclo,
    con la condizione «Umidità non in corso» delle altre copie."""
    passi = _free_v0_inquinanti_v0_scelta()
    passo = passi[0]
    assert passo["if"][0]["value_template"] == f"{{{{ is_state('{SPIA_UMIDITA}', 'off') }}}}"
    assert passo["then"] == [{"action": "input_boolean.turn_off", "target": {"entity_id": [FREE_C, FREE_H]}}]
    (ciclo,) = [p for p in passi if "repeat" in p]
    assert FREE_C not in str(ciclo) and FREE_H not in str(ciclo)
    assert f"is_state('{SPIA_UMIDITA}', 'off')" in FREE_V0_FINE_INQUINANTI
    a = passo["alias"]
    assert "Umidità in corso" in a and "24-11-2026" in a and "[Nota 3]" in a and "vmc_master" not in a, a
    cv.SCRIPT_SCHEMA(_ramo("spia_velocita_0_inquinanti_co2_voc")["sequence"])
