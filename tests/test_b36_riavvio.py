"""Prove della b36, verifica dei riavvii di Home Assistant con il simulatore (21-11-2026).

- E1: la Spia Comando non eseguito del Calendario si spegneva a ogni riavvio (initial: false). Con la porta 5001 muta
  all'ingresso nella Fascia, a fine Fascia o allo spegnimento del Calendario durante la Fascia, un riavvio di Home
  Assistant faceva perdere il comando in sospeso (VMC a Velocità 0 per tutta la Fascia, oppure rimasta alla velocità
  della Fascia). Ora la spia viene ripristinata come la Spia Black-Out del Calendario: il trigger
  «calendario_ritorno_comando» ha già la guardia del riallineamento (fase 0 o >= 4) e aspetta la velocità leggibile,
  quindi il comando viene ripetuto a riallineamento finito, salvo se nel frattempo la velocità è cambiata.
- E4: il trigger «Spia Avvisi On» non aveva la guardia del riallineamento: un riavvio durante i suoi 5 s di attesa
  lasciava la Spia Avvisi spenta per tutta l'allerta (un template già vero all'avvio non scatta). Ora ha la stessa
  guardia degli altri trigger, nelle 4 copie (trigger, «Evento ancora valido», Countdown Attese ON e OFF).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
CNE = "vmc_master_spia_calendario_comando_non_eseguito"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
GUARDIA = (f"(states('{FASE}') | float(0) == 0 or states('{FASE}') | float(0) >= 4)")
ID_AVVISI = "Spia Avvisi On"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _norm(testo: str) -> str:
    return " ".join(testo.split())


def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


# ------------------------------------------------------------------------------------------------------------- E1
def test_e1_spia_comando_non_eseguito_ripristinata_al_riavvio() -> None:
    spia = _pacchetto()["input_boolean"][CNE]
    assert "initial" not in spia
    assert spia == {"name": "Spia Comando non eseguito all'interno del Calendario", "icon": "mdi:memory"}
    riga = next(r for r in _testo("vmc_master.yaml").splitlines() if r.startswith(f"  {CNE}:"))
    assert "SI SPEGNE AL RIAVVIO" not in riga
    assert "RESTA ACCESA ANCHE DOPO UN RIAVVIO DI HOME ASSISTANT" in riga
    # come la Spia Black-Out del Calendario, anch'essa senza initial
    assert "initial" not in _pacchetto()["input_boolean"]["vmc_master_spia_calendario_black_out"]


def test_e1_ritorno_del_comando_aspetta_il_riallineamento_e_la_lettura() -> None:
    """Il comando ripetuto dopo il riavvio parte solo a riallineamento finito (fase 0 o >= 4) e con la velocità
    della VMC leggibile: la spia ripristinata non fa nulla durante le fasi 1-3."""
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == "calendario_ritorno_comando"]
    modello = _norm(trigger["value_template"])
    assert f"states('input_boolean.{CNE}') == 'on'" in modello
    assert "states('sensor.vmc_master_status_ventola') not in ['unavailable', 'unknown', '']" in modello
    assert _norm(GUARDIA) in modello


def test_e1_nessun_testo_dice_che_la_spia_si_spegne_al_riavvio() -> None:
    radice = PKG.parent.parent.parent
    for file in (PKG / "vmc_master.yaml", PKG / "vmc_master_automazione.txt",
                 PKG / "vmc_master_scheda_manuale_interfaccia.txt", radice / "README.md", radice / ".github" / "README.md"):
        testo = file.read_text(encoding="utf-8").upper()
        assert "SI SPEGNE AL RIAVVIO" not in testo, file


# ------------------------------------------------------------------------------------------------------------- E4
def _trigger_avvisi() -> dict[str, Any]:
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == ID_AVVISI]
    return trigger


def test_e4_trigger_spia_avvisi_on_con_la_guardia() -> None:
    trigger = _trigger_avvisi()
    assert _norm(trigger["value_template"]).endswith(f") and {_norm(GUARDIA)} }}}}")
    assert trigger["for"] == {"seconds": "{{ states('input_number.vmc_master_attesa_avvisi') | int(5) }}"}


def test_e4_copie_identiche_al_trigger() -> None:
    """Copia 1:1 nella condizione «Evento ancora valido» e nelle copie ON e OFF del Countdown Attese."""
    corpo = _norm(_trigger_avvisi()["value_template"])
    aut = _testo("vmc_master_automazione.txt")
    inizio = aut.index(f"{{%- elif trigger.id == '{ID_AVVISI}' -%}}")
    copia = aut[inizio:aut.index("{%- elif", inizio + 10)].split("-%}", 1)[1]
    assert _norm(copia) == corpo
    countdown = next(a for a in _pacchetto()["automation"] if any(
        str(t.get("id", "")).endswith(f"|{ID_AVVISI}") for t in a.get("triggers", a.get("trigger", []))))
    copie = {t["id"]: t["value_template"] for t in countdown.get("triggers", countdown.get("trigger", []))
             if str(t.get("id", "")).endswith(f"|{ID_AVVISI}")}
    assert sorted(copie) == [f"OFF|avvisi|avvisi|{ID_AVVISI}", f"ON|avvisi|avvisi|{ID_AVVISI}"]
    assert _norm(copie[f"ON|avvisi|avvisi|{ID_AVVISI}"]) == corpo
    off = _norm(copie[f"OFF|avvisi|avvisi|{ID_AVVISI}"])
    assert off.startswith("{%- set vmc_master_esito -%} " + corpo + " {%- endset -%}")


@pytest.mark.parametrize(("fase", "atteso"), [("0", "True"), ("1", "False"), ("2", "False"), ("3", "False"),
                                              ("4", "True")])
async def test_e4_spia_avvisi_on_aspetta_il_riallineamento(hass, fase: str, atteso: str) -> None:
    from homeassistant.helpers.template import Template

    hass.states.async_set("sensor.vmc_master_alert_monitoraggio_totale", "Allerta")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set("sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia", "Velocità 0")
    for v in ("0", "1", "2", "3", "4", "notturna", "freecooling", "iperventilazione"):
        hass.states.async_set(f"input_boolean.vmc_master_spia_velocita_{v}", "off")
    hass.states.async_set(FASE, fase)
    esito = Template(_trigger_avvisi()["value_template"], hass).async_render(parse_result=False).strip()
    assert esito == atteso
