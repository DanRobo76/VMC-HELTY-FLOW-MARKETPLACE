"""Prove della b36, fetta «tastiera»: durante un'allerta la finestra Telecomando mostra ancora la velocità attiva e la
Velocità Registrata.

Ogni tasto di velocità con la scritta Alert ha due varianti: quella normale (binary_sensor del tasto, illuminata con
l'icona del tasto o con l'icona ↺ della velocità da ripristinare) e quella «alert» (sensor Alert Avvio Interfaccia,
scritta sotto il tasto). Prima la variante alert prendeva il posto del tasto per tutta l'allerta, anche quando il tasto
era acceso: con «Alert Free» e la Velocità Registrata Free Heating il tasto Free Heating mostrava solo la scritta.
Ora, dove compare la variante alert, si vede la variante normale se il binary_sensor del tasto è acceso: la scritta
resta sotto i tasti spenti; fuori dalle allerte non cambia niente.

Tasti Free: in ogni combinazione di mese programmato, monitoraggio Free, Alert Avvio e sensori di temperatura si vede
esattamente un tasto Free (in una delle sue due varianti), quello del nome Free della Velocità Registrata (nome_free):
Free Heating o Free Cooling nel mese programmato, Free Cool./Heat. («Free Heat./Cool.») negli altri mesi o con il
monitoraggio Free «[Non Calcolabile]». Prima, nel mese programmato con una temperatura «[Non Calcolabile]», non si vedeva
nessun tasto Free.

Le condizioni di visibilità della scheda (state, and, or) sono valutate come fa il frontend di Home Assistant.
"""

from __future__ import annotations

import itertools
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import jinja2
import pytest
from homeassistant.util import yaml as hay

RADICE = Path(__file__).parent.parent
PKG = RADICE / "custom_components" / "vmc_master" / "package"
SCHEDA = PKG / "vmc_master_scheda_manuale_interfaccia.txt"

ALERT = "sensor.vmc_master_alert_avvio_interfaccia"
MESE = "sensor.vmc_master_status_mese_corrente_freeheating_o_freecooling"
FREE = "sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi"
MON = "sensor.vmc_master_alert_monitoraggio_free_heating_o_free_cooling"
NC = "[Non Calcolabile]"
T_EST = "sensor.vmc_master_temp_esterna_status"
T_INT = "sensor.vmc_master_temp_interna_status"
TASTO = "binary_sensor.vmc_master_tasto_"
STATI_ALERT = ("Nessuna", "Alert", "Alert Δ Temp.", "Alert Free")

# tasto: (scritte che può mostrare, voce 22 e sensore Alert Avvio Interfaccia; mesi in cui il tasto c'è)
TUTTI_I_MESI = ("Free Heating", "Free Cooling", "Disabilitata")
ATTESI = {
    "velocita_1": ({"Alert"}, TUTTI_I_MESI),
    "velocita_2": ({"Alert", "Alert Δ Temp."}, TUTTI_I_MESI),
    "velocita_3": ({"Alert", "Alert Δ Temp."}, TUTTI_I_MESI),
    "velocita_4": ({"Alert", "Alert Δ Temp."}, TUTTI_I_MESI),
    "notturna": ({"Alert", "Alert Δ Temp."}, TUTTI_I_MESI),
    "iperventilazione": ({"Alert", "Alert Δ Temp."}, TUTTI_I_MESI),
    "free_heating": ({"Alert", "Alert Δ Temp.", "Alert Free"}, ("Free Heating",)),
    "free_cooling": ({"Alert", "Alert Δ Temp.", "Alert Free"}, ("Free Cooling",)),
    "free_cool_heat": ({"Alert", "Alert Δ Temp."}, ("Disabilitata",)),
}
MONITORAGGIO = {
    "Free Heating": ("Nessuna Allerta Free Heating Programmato",
                     "Nessuna Allerta Free Heating Programmato, Presenza di Inquinanti",
                     "Allerta Free Heating Programmato (Raffrescamento Arrestato)",
                     "Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)",
                     "[Non Calcolabile]"),
    "Free Cooling": ("Nessuna Allerta Free Cooling Programmato",
                     "Nessuna Allerta Free Cooling Programmato, Presenza di Inquinanti",
                     "Allerta Free Cooling Programmato (Riscaldamento Arrestato)",
                     "Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)",
                     "[Non Calcolabile]"),
    "Disabilitata": ("Nessuna Allerta", "Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento)"),
}
# nome Free della Velocità Registrata -> tasto Free
TASTO_DEL_NOME = {"Free Heating": "free_heating", "Free Cooling": "free_cooling", "Free Heat./Cool.": "free_cool_heat"}
NOMI_FREE = {"Free Heating", "Free Cooling", "Free Cool./Heat."}


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


@lru_cache
def _testo(percorso: Path) -> str:
    return percorso.read_bytes().decode("utf-8")


def _lista(valore: Any) -> list[str]:
    return [str(v) for v in (valore if isinstance(valore, list) else [valore])]


def _vale(condizione: dict[str, Any], stati: dict[str, str]) -> bool:
    """Una condizione di visibilità, come il frontend: state/state_not su una o più stringhe, and, or."""
    tipo = condizione["condition"]
    if tipo == "and":
        return all(_vale(c, stati) for c in condizione["conditions"])
    if tipo == "or":
        return any(_vale(c, stati) for c in condizione["conditions"])
    assert tipo == "state", condizione
    stato = stati.get(condizione["entity"], "unavailable")
    if "state" in condizione:
        return stato in _lista(condizione["state"])
    return stato not in _lista(condizione["state_not"])


def _visibile(card: dict[str, Any], stati: dict[str, str]) -> bool:
    return all(_vale(c, stati) for c in card.get("visibility", []))


@lru_cache
def _modello_nome_free() -> jinja2.Template:
    """Le due righe di sensor.vmc_master_velocita_registrata che danno il nome della velocità Free."""
    pacchetto = _testo(PKG / "vmc_master.yaml")
    righe = [re.search(r"\{%- set mese_free = .*?-%\}", pacchetto).group(0),
             re.search(r"\{%- set nome_free = .*?-%\}", pacchetto).group(0)]
    assert MON in righe[1] and MESE in righe[0]
    return jinja2.Environment().from_string("".join(righe) + "{{ nome_free }}")


@lru_cache
def _nome_free(mese: str, monitoraggio: str) -> str:
    stati = {MESE: mese, MON: monitoraggio}
    return _modello_nome_free().render(states=lambda entita: stati.get(entita, "unavailable"))


def _stati(s: str, mese: str, avvisi: str, tasto: str, acceso: str) -> dict[str, str]:
    """Stati coerenti: con il monitoraggio Free «[Non Calcolabile]» la Temperatura Esterna non è un numero."""
    return {ALERT: s, MESE: mese, FREE: avvisi, MON: NC if avvisi == NC else "Nessuna Allerta",
            T_EST: NC if avvisi == NC else "10.0", T_INT: "21.0", f"{TASTO}{tasto}": acceso}


def _liste_di_card(nodo: Any):
    if isinstance(nodo, dict):
        for chiave, valore in nodo.items():
            if chiave == "cards" and isinstance(valore, list):
                yield valore
            yield from _liste_di_card(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _liste_di_card(valore)


@lru_cache
def _tastiera() -> tuple[dict[str, Any], ...]:
    """L'unica griglia di tasti della scheda (quella con il tasto Velocità 0)."""
    griglie = [
        lista for lista in _liste_di_card(hay.load_yaml(str(SCHEDA)))
        if any(isinstance(c, dict) and c.get("entity") == f"{TASTO}velocita_0" for c in lista)
    ]
    assert len(griglie) == 1
    return tuple(griglie[0])


def _coppie() -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    """tasto -> (variante normale, variante alert): la variante alert segue sempre la sua variante normale."""
    tasti = _tastiera()
    coppie = {}
    for i, card in enumerate(tasti):
        if card.get("entity") != ALERT:
            continue
        normale = tasti[i - 1]
        assert normale["entity"].startswith(TASTO), normale
        assert normale["name"] == card["name"] and normale["tap_action"] == card["tap_action"], card["name"]
        assert normale["state_color"] is True and normale["show_state"] is False and card["show_state"] is True
        coppie[normale["entity"].removeprefix(TASTO)] = (normale, card)
    return coppie


def test_una_sola_tastiera_e_tutte_le_varianti_alert() -> None:
    assert _testo(SCHEDA).count(f"entity: {TASTO}velocita_0\r\n") == 1
    assert set(_coppie()) == set(ATTESI)
    # Velocità 0, Sensori e Led Pannello non hanno la scritta Alert
    for nome in ("velocita_0", "sensori_on", "sensori_off", "led_pannello_on", "led_pannello_off"):
        assert sum(c.get("entity") == f"{TASTO}{nome}" for c in _tastiera()) == 1, nome


@pytest.mark.parametrize("tasto", sorted(ATTESI))
def test_scritte_del_tasto(tasto: str) -> None:
    """Le scritte che compaiono sotto il tasto sono quelle della tabella della voce 22."""
    scritte, mesi = ATTESI[tasto]
    _, alert = _coppie()[tasto]
    viste = {
        s for s, mese in itertools.product(STATI_ALERT, mesi)
        for avvisi in MONITORAGGIO[mese] if avvisi != NC
        if _visibile(alert, _stati(s, mese, avvisi, tasto, "off"))
    }
    assert viste == scritte


@pytest.mark.parametrize("tasto", sorted(ATTESI))
def test_durante_le_allerte_il_tasto_acceso_resta_acceso(tasto: str) -> None:
    """Con il tasto acceso (velocità attiva o Velocità Registrata) si vede la variante normale, con il tasto spento
    la scritta Alert; mai le due varianti insieme; fuori dalle allerte del tasto si vede la variante normale, acceso o
    spento. Un tasto Free c'è solo se è quello del nome Free della Velocità Registrata."""
    scritte, _ = ATTESI[tasto]
    normale, alert = _coppie()[tasto]
    for mese in TUTTI_I_MESI:
        for s, avvisi in itertools.product(STATI_ALERT, MONITORAGGIO[mese]):
            stati = _stati(s, mese, avvisi, tasto, "on")
            presente = not tasto.startswith("free_") or TASTO_DEL_NOME[_nome_free(mese, stati[MON])] == tasto
            for acceso in ("on", "off", "unavailable"):
                stati = _stati(s, mese, avvisi, tasto, acceso)
                visto = (_visibile(normale, stati), _visibile(alert, stati))
                if not presente:
                    atteso = (False, False)
                elif s in scritte:
                    atteso = (True, False) if acceso == "on" else (False, True)
                else:
                    atteso = (True, False)
                assert visto == atteso, (mese, s, avvisi, acceso)


TEMPERATURE = ("10.0", NC, "Non disponibile", "unavailable")
MESI = ("Free Heating", "Free Cooling", "Disabilitata", "Non disponibile", "unavailable", "unknown")
MONITORAGGI = ("Nessuna Allerta", "Allerta Free Heating Programmato (Raffrescamento in atto)",
               "Allerta Free Cooling Programmato (Riscaldamento in atto)", "Allerta Raffrescamento in atto",
               "Riscaldamento in atto", NC, "Non disponibile", "unavailable")
AVVISI = tuple(dict.fromkeys(a for valori in MONITORAGGIO.values() for a in valori)) + ("Non disponibile", "unavailable")


def test_esattamente_un_tasto_free() -> None:
    """In ogni combinazione (anche non coerente) di mese, monitoraggio Free, avvisi Free, Alert Avvio, temperature e
    tasti Free accesi o spenti si vede un solo tasto Free, quello del nome Free della Velocità Registrata."""
    free = [c for c in _tastiera() if c.get("name") in NOMI_FREE]
    assert len(free) == 6
    nomi = {"free_heating": "Free Heating", "free_cooling": "Free Cooling", "free_cool_heat": "Free Cool./Heat."}
    for mese, monitoraggio, avvisi, s, t_est, t_int, acceso in itertools.product(
        MESI, MONITORAGGI, AVVISI, STATI_ALERT, TEMPERATURE, TEMPERATURE, ("on", "off")
    ):
        stati = {MESE: mese, MON: monitoraggio, FREE: avvisi, ALERT: s, T_EST: t_est, T_INT: t_int}
        stati.update({f"{TASTO}{t}": acceso for t in nomi})
        visti = [c["name"] for c in free if _visibile(c, stati)]
        assert visti == [nomi[TASTO_DEL_NOME[_nome_free(mese, monitoraggio)]]], (stati, visti)


def test_caso_della_segnalazione() -> None:
    """Velocità 1 con «Alert Free» e Velocità Registrata Free Heating: accesi Velocità 1 e Free Heating (↺)."""
    stati = {ALERT: "Alert Free", MESE: "Free Heating", MON: "Nessuna Allerta",
             FREE: "Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)",
             T_EST: "10.0", T_INT: "21.0", f"{TASTO}velocita_1": "on", f"{TASTO}free_heating": "on"}
    visibili = [c for c in _tastiera() if _visibile(c, stati)]
    accesi = [c["entity"].removeprefix(TASTO) for c in visibili if c.get("entity", "").startswith(TASTO)]
    assert {"velocita_1", "free_heating"} <= set(accesi)
    assert [c["name"] for c in visibili if c.get("entity") == ALERT] == []
    # la stessa allerta con la Velocità Registrata diversa da Free: sotto il tasto Free resta la scritta
    stati[f"{TASTO}free_heating"] = "off"
    visibili = [c for c in _tastiera() if _visibile(c, stati)]
    assert [c["name"] for c in visibili if c.get("entity") == ALERT] == ["Free Heating"]


def test_caso_temperatura_non_calcolabile() -> None:
    """Mese Free Heating con la Temperatura Esterna «[Non Calcolabile]»: si vede il tasto Free Cool./Heat., come il nome
    «Free Heat./Cool.» della Velocità Registrata."""
    stati = {ALERT: "Nessuna", MESE: "Free Heating", MON: NC, FREE: NC, T_EST: NC, T_INT: "21.0"}
    assert _nome_free("Free Heating", NC) == "Free Heat./Cool."
    assert [c["name"] for c in _tastiera() if c.get("name") in NOMI_FREE and _visibile(c, stati)] == ["Free Cool./Heat."]


def test_fini_riga_e_yaml() -> None:
    grezzo = SCHEDA.read_bytes()
    assert grezzo.count(b"\r\n") == grezzo.count(b"\n")
    assert _tastiera()


# ------------------------------------------------------------------------------------------------------ testi
def _voce(numero: int) -> str:
    scheda = _testo(SCHEDA)
    inizio = scheda.index(f"<summary><b>{numero} ")
    return _norm(scheda[inizio: scheda.index("<summary><b>", inizio + 1)])


def test_testi_della_scheda() -> None:
    assert ("Il tasto della velocità attiva e quello della velocità da ripristinare (icona ↺) restano illuminati "
            "anche durante l'allerta: la scritta compare solo sotto i tasti spenti.") in _voce(22)
    assert ("Nella finestra Telecomando il tasto della velocità attiva è illuminato, quello della velocità da "
            "ripristinare è illuminato con l'icona ↺, anche durante un'allerta (la scritta Alert compare solo sotto i "
            "tasti spenti);") in _voce(17)


@pytest.mark.parametrize("nome", ["README.md", ".github/README.md"])
def test_readme(nome: str) -> None:
    testo = (RADICE / nome).read_text(encoding="utf-8")
    assert testo.count("Nella finestra Telecomando il tasto della velocità attiva è illuminato e quello della velocità "
                       "da ripristinare è illuminato con l'icona ↺, anche durante un'allerta (le scritte «Alert» "
                       "compaiono solo sotto i tasti spenti).") == 1
    assert testo.count("In the Telecomando window the button of the active speed is lit and the button of the speed to "
                       "restore is lit with the ↺ icon, also during an alert (the «Alert» labels appear only under the "
                       "unlit buttons).") == 1
    if nome == ".github/README.md":
        assert testo.count("«Alert Free» sotto i tasti spenti avvisano") == 1
        assert testo.count("«Alert Free» labels under the unlit buttons warn") == 1
