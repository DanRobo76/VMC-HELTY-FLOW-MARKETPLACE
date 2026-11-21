"""Prove della b36, velocità scelta dall'utente negli ultimi Secondi dell'allerta Umidità (Foglio A21).

Durante l'Umidità una velocità scelta dall'utente viene memorizzata dopo 4 s (memorie umidita_velocita_X) e mantenuta a
fine Umidità. La fine Umidità (trigger spia_umidita_off, 28 s dopo il rientro dell'umidità) non guarda la lettura: una
velocità scelta negli ultimi Secondi, non ancora memorizzata, veniva sovrascritta dal ripristino della memoria vecchia
(stessa classe del PdR A2-1, del Δ Temp. C3-1 e della fine Inquinanti C3-2). Ora, in ognuno degli 8 casi del ripristino
(memoria Velocità 0, 1, 2, 3, 4, Notturna, Free Cooling, Iperventilazione), dopo lo spegnimento della Spia e delle
memorie dell'Umidità e prima del primo comando, una velocità valida diversa da quella data dall'Umidità e da quella del
ripristino resta: nessun comando, il ramo si ferma.

Velocità date dall'Umidità (non sono una scelta dell'utente):
- memoria Velocità 0 (VMC avviata da Velocità 0): la [Set Velocità Umidità di Avvio] (con Free Cool./Heat. la Free
  Cooling e la Velocità 1 delle allerte Free, Nota 3) e la Velocità 0 (scelta dall'utente: a fine Umidità torna a 0);
  con il Set su Velocità 0 la VMC resta ferma e ogni altra velocità è una scelta;
- memoria Free Cooling: la Free Cooling, la Velocità 0 con la Free sospesa (velocità di fine allerta) e la Velocità 1
  data dall'Umidità con la Free sospesa (Nota 3; con il Set su Velocità 0 la Velocità 1 è una scelta);
- memorie Velocità 1-4, Notturna, Iperventilazione (VMC già in moto): la velocità memorizzata.
"""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from tests.test_b35_allerte import FREE_C, FREE_H, LETTURA, PKG, SPIA_U0, SPIA_UMIDITA, _ramo, _spente
from tests.test_b36_allerte import (
    BLACK_OUT_RILEVATO,
    MEMORIE_UMIDITA,
    SET_UMIDITA,
    SPIA_U0_MANTENUTA,
    _esegui,
    _stato,
)

STOP = "Velocità scelta dall'utente durante l'allerta Umidità mantenuta"
VALIDE = ["Velocità 0", "Velocità 1", "Velocità 2", "Velocità 3", "Velocità 4", "Notturna", "Iperventilazione",
          "Free Cooling"]
# caso del ripristino: (alias, memoria Umidità accesa, velocità del ripristino senza Free sospesa, comando)
CASI = {
    "0": ("Velocità 0", SPIA_U0, "Velocità 0", "vmc_master_velocita_0"),
    "1": ("Velocità 1", "input_boolean.vmc_master_spia_umidita_velocita_1", "Velocità 1", "vmc_master_velocita_1"),
    "2": ("Velocità 2", "input_boolean.vmc_master_spia_umidita_velocita_2", "Velocità 2", "vmc_master_velocita_2"),
    "3": ("Velocità 3", "input_boolean.vmc_master_spia_umidita_velocita_3", "Velocità 3", "vmc_master_velocita_3"),
    "4": ("Velocità 4", "input_boolean.vmc_master_spia_umidita_velocita_4", "Velocità 4", "vmc_master_velocita_4"),
    "notturna": ("Velocità Notturna", "input_boolean.vmc_master_spia_umidita_velocita_notturna", "Notturna",
                 "vmc_master_notturna"),
    "freecooling": ("Velocità Free Cooling", "input_boolean.vmc_master_spia_umidita_velocita_freecooling",
                    "Free Cooling", "vmc_master_freecooling"),
    "iperventilazione": ("Velocità Iperventilazione", "input_boolean.vmc_master_spia_umidita_velocita_iperventilazione",
                         "Iperventilazione", "vmc_master_iperventilazione"),
}
GENERICI = ["1", "2", "3", "4", "notturna", "iperventilazione"]


def _sequenza() -> list[dict[str, Any]]:
    return _ramo("spia_umidita_off")["sequence"]


def _caso(chiave: str) -> list[dict[str, Any]]:
    (opzione,) = [o for o in _sequenza()[1]["choose"] if o["alias"] == CASI[chiave][0]]
    return opzione["sequence"]


def _blocco(chiave: str) -> tuple[int, dict[str, Any]]:
    passi = _caso(chiave)
    (k,) = [k for k, p in enumerate(passi) if "vel_prima_del_comando" in p.get("variables", {})]
    return k, passi[k + 1]


# ------------------------------------------------------------------------------------------------ struttura
@pytest.mark.parametrize("chiave", list(CASI))
def test_blocco_dopo_la_lettura_e_prima_del_comando(chiave: str) -> None:
    """Il blocco segue la lettura della velocità (vel_prima_del_comando) e precede il ciclo di comando; le memorie e la
    Spia dell'Umidità sono già spente; il blocco ha solo lo stop: nessun comando, nessuna attesa."""
    passi = _caso(chiave)
    k, blocco = _blocco(chiave)
    assert set(blocco) == {"alias", "if", "then"}
    assert blocco["alias"].startswith("Velocità cambiata dall'utente negli ultimi Secondi dell'allerta Umidità")
    assert "[Foglio Logiche A21]" in blocco["alias"]
    assert blocco["then"] == [{"stop": STOP}]
    assert "repeat" in passi[k + 2]
    spente = [p for p in passi[:k] if p.get("action") == "input_boolean.turn_off" and "target" in p]
    assert spente and set(MEMORIE_UMIDITA) <= set(spente[-1]["target"]["entity_id"])
    assert _sequenza()[0]["target"]["entity_id"] == SPIA_UMIDITA
    testo = str(blocco)
    for parola in ("delay", "wait_template", "timeout", "'for'", "shell_command", "repeat"):
        assert parola not in testo, parola


@pytest.mark.parametrize("chiave", GENERICI)
def test_condizione_dei_6_casi_con_la_vmc_gia_in_moto(chiave: str) -> None:
    (condizione,) = _blocco(chiave)[1]["if"]
    altre = [v for v in VALIDE if v != CASI[chiave][2]]
    attesa = "{{ vel_prima_del_comando in [" + ", ".join(f"'{v}'" for v in altre) + "] }}"
    assert condizione == {"condition": "template", "value_template": attesa}


def test_condizioni_velocita_0_e_free_cooling() -> None:
    (c0,) = _blocco("0")[1]["if"]
    assert c0["value_template"] == (
        "{{ vel_prima_del_comando in ['Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', 'Notturna', "
        "'Iperventilazione', 'Free Cooling'] and vel_prima_del_comando not in (['Free Cooling', 'Velocità 1'] if "
        f"states('{SET_UMIDITA}') == 'Free Cool./Heat.' else [states('{SET_UMIDITA}')]) }}}}")
    (cf,) = _blocco("freecooling")[1]["if"]
    assert cf["value_template"] == (
        "{{ vel_prima_del_comando in ['Velocità 0', 'Velocità 1', 'Velocità 2', 'Velocità 3', 'Velocità 4', "
        "'Notturna', 'Iperventilazione'] and not (vel_prima_del_comando == 'Velocità 0' and "
        f"(states('{FREE_C}') == 'on' or states('{FREE_H}') == 'on')) and not (vel_prima_del_comando == "
        f"'Velocità 1' and states('{SET_UMIDITA}') != 'Velocità 0') }}}}")


def test_file_automazione_lf_e_8_blocchi() -> None:
    dati = (PKG / "vmc_master_automazione.txt").read_bytes()
    assert b"\r" not in dati
    assert dati.decode("utf-8").count(f"- stop: {STOP}\n") == 8


async def test_ramo_valido_per_home_assistant(hass: HomeAssistant) -> None:
    cv.SCRIPT_SCHEMA(_sequenza())


# ------------------------------------------------------------------------------------------------ esecuzione
def _stati(chiave: str, letta: str, **altri: str) -> dict[str, str]:
    stati = {SPIA_UMIDITA: "on", **_spente(MEMORIE_UMIDITA), CASI[chiave][1]: "on", SET_UMIDITA: "Velocità 2",
             LETTURA: letta, FREE_C: "off", FREE_H: "off", BLACK_OUT_RILEVATO: "off"}
    stati.update(altri)
    return stati


async def _fine(hass: HomeAssistant, chiave: str, letta: str, **altri: str) -> list[str]:
    return await _esegui(hass, _sequenza(), _stati(chiave, letta, **altri), attesa=0.5)


def _pulizia_fatta(hass: HomeAssistant) -> bool:
    return all(_stato(hass, e) == "off" for e in (SPIA_UMIDITA, *MEMORIE_UMIDITA))


def _scelte(chiave: str) -> list[str]:
    """Velocità che sono una scelta dell'utente con [Set Velocità Umidità di Avvio] su Velocità 2 e la Free non sospesa."""
    escluse = {"0": ["Velocità 0", "Velocità 2"], "freecooling": ["Free Cooling", "Velocità 1"]}.get(
        chiave, [CASI[chiave][2]])
    return [v for v in VALIDE if v not in escluse]


@pytest.mark.parametrize(("chiave", "letta"), [(c, v) for c in CASI for v in _scelte(c)])
async def test_scelta_non_memorizzata_resta(hass: HomeAssistant, chiave: str, letta: str) -> None:
    """Velocità scelta negli ultimi Secondi dell'Umidità: nessun comando, Spia e memorie dell'Umidità spente."""
    assert await _fine(hass, chiave, letta) == []
    assert _pulizia_fatta(hass)


@pytest.mark.parametrize("chiave", list(CASI))
async def test_senza_scelta_ripristino_come_prima(hass: HomeAssistant, chiave: str) -> None:
    """VMC ancora alla velocità data dall'Umidità (o già a quella del ripristino): il ripristino parte come prima."""
    letta = "Velocità 2" if chiave == "0" else CASI[chiave][2]
    assert (await _fine(hass, chiave, letta))[:1] == [CASI[chiave][3]]
    assert _pulizia_fatta(hass)


@pytest.mark.parametrize("letta", ["Non disponibile", "unknown", ""])
async def test_lettura_non_valida_ripristino_come_prima(hass: HomeAssistant, letta: str) -> None:
    assert (await _fine(hass, "3", letta))[:1] == ["vmc_master_velocita_3"]


# ------------------------------------------------------------------------------------------------ casi del Foglio A21
@pytest.mark.parametrize(
    ("altri", "letta", "comando"),
    [
        ({}, "Velocità 2", "vmc_master_velocita_0"),  # VMC alla Set di avvio: a fine Umidità torna a 0
        ({}, "Velocità 0", "vmc_master_velocita_0"),  # avviata da 0 e scelta Velocità 0: torna a 0
        ({SPIA_U0_MANTENUTA: "on"}, "Velocità 2", "vmc_master_velocita_0"),  # stessa velocità di avvio: nulla cambia
        ({SPIA_U0_MANTENUTA: "on"}, "Velocità 3", None),  # Velocità 0 mantenuta, poi un'altra velocità: resta
        ({SET_UMIDITA: "Notturna"}, "Notturna", "vmc_master_velocita_0"),
        ({SET_UMIDITA: "Notturna"}, "Velocità 2", None),
        ({SET_UMIDITA: "Free Cool./Heat."}, "Free Cooling", "vmc_master_velocita_0"),
        ({SET_UMIDITA: "Free Cool./Heat."}, "Velocità 1", "vmc_master_velocita_0"),  # Velocità 1 delle allerte Free
        ({SET_UMIDITA: "Free Cool./Heat."}, "Velocità 3", None),
        ({SET_UMIDITA: "Velocità 0"}, "Velocità 0", "vmc_master_velocita_0"),  # Set 0: la VMC è rimasta ferma
        ({SET_UMIDITA: "Velocità 0"}, "Velocità 1", None),  # con il Set 0 la Velocità 1 è una scelta
        ({SET_UMIDITA: "Velocità 0"}, "Free Cooling", None),
    ],
)
async def test_a21_umidita_avviata_da_velocita_0(hass: HomeAssistant, altri: dict[str, str], letta: str,
                                                 comando: str | None) -> None:
    comandi = await _fine(hass, "0", letta, **altri)
    assert comandi[:1] == ([comando] if comando else [])
    assert _pulizia_fatta(hass)


@pytest.mark.parametrize(
    ("altri", "letta", "comando", "ripresa"),
    [
        # Free sospesa: Velocità 1 dell'Umidità [Nota 3] -> Velocità 0, la ripresa Free resta in attesa
        ({FREE_C: "on"}, "Velocità 1", "vmc_master_velocita_0", "on"),
        ({FREE_C: "on"}, "Velocità 0", "vmc_master_velocita_0", "on"),
        ({FREE_C: "on"}, "Free Cooling", "vmc_master_velocita_0", "on"),
        ({FREE_H: "on"}, "Velocità 1", "vmc_master_velocita_0", "off"),
        # velocità scelta con la Free sospesa: resta, la ripresa la annulla poi l'annullamento (20 s, Foglio A29)
        ({FREE_C: "on"}, "Velocità 3", None, "on"),
        ({FREE_H: "on"}, "Notturna", None, "off"),
        # Free non sospesa
        ({}, "Free Cooling", "vmc_master_freecooling", "off"),
        ({}, "Velocità 0", None, "off"),
        ({}, "Velocità 1", "vmc_master_freecooling", "off"),
        ({SET_UMIDITA: "Velocità 0"}, "Velocità 1", None, "off"),  # con il Set 0 la Velocità 1 è una scelta
    ],
)
async def test_a21_memoria_free_cooling_e_free_sospesa(hass: HomeAssistant, altri: dict[str, str], letta: str,
                                                       comando: str | None, ripresa: str) -> None:
    comandi = await _fine(hass, "freecooling", letta, **altri)
    assert comandi[:1] == ([comando] if comando else [])
    assert _stato(hass, FREE_C) == ripresa
    assert _pulizia_fatta(hass)


async def test_velocita_0_e_ripresa_free_come_prima(hass: HomeAssistant) -> None:
    """Memoria Velocità 0 con la Free sospesa: l'annullamento della ripresa (regola C4-4) precede il blocco, quindi
    vale anche quando la scelta resta (Set diverso da 0: annullata; Set 0 e Velocità 0 non mantenuta: in attesa)."""
    assert await _fine(hass, "0", "Velocità 3", **{FREE_C: "on"}) == []
    assert _stato(hass, FREE_C) == "off"
    assert await _fine(hass, "0", "Velocità 3", **{FREE_C: "on", SET_UMIDITA: "Velocità 0"}) == []
    assert _stato(hass, FREE_C) == "on"


# ------------------------------------------------------------------------------------------------ testi
def test_descrizione_e_scheda_aggiornate() -> None:
    """Tempo dell'Umidità e 2 righe della tabella del cambio di velocità, nella descrizione e nella scheda (voce 17 e
    tabella HTML); l'uguaglianza dei testi la controlla test_b36_coerenza_testi."""
    descrizione = " ".join((PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8").split())
    scheda = " ".join((PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8").split())
    for testo in (descrizione, scheda):
        assert testo.count("mantenuta a fine Umidità (se l'Umidità finisce prima che sia memorizzata, la Velocità "
                           "scelta resta)") == 1
        assert testo.count("mantenuta a fine Umidità (se l'Umidità finisce prima che sia memorizzata, resta la "
                           "Velocità scelta)") == 2
        assert "mantenuta a fine Umidità;" not in testo
