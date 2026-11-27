"""Calendario: accensione e spegnimento della VMC nelle Fasce, velocita' e mesi delle Fasce."""

from __future__ import annotations

from ..lettore import Lettore
from . import modello

# now().weekday(): 0 = lunedi' ... 6 = domenica (nomi delle voci del package)
_GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")
# la lista «stati» dei modelli; il none della lista non e' mai uguale a un testo di states()
_NON_VALIDI = ("sconosciuto", "unknown", "", "unavailable", "Non disponibile")


def _fasce_valide(L: Lettore, giorno: str) -> bool:
    """Le due Fasce del giorno sono in ordine e il Calendario comanda la VMC.

    Stessi confronti (tra testi, come nel modello) e stesso ordine del package: in
    pratica accensione < spegnimento < accensione 2 < spegnimento 2.
    """
    a1 = L.v(f"input_datetime.accensione_{giorno}")
    s1 = L.v(f"input_datetime.spegnimento_{giorno}")
    a2 = L.v(f"input_datetime.accensione_{giorno}_2")
    s2 = L.v(f"input_datetime.spegnimento_{giorno}_2")
    return (
        a1 < s1
        and a1 != s1
        and a2 < s2
        and a2 != s2
        and a1 < a2
        and s1 < s2
        and a1 != a2
        and s1 != s2
        and s1 != a2
        and a2 > s1
        and L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_calendario") == "on"
    )


def _stato_calendario(L: Lettore, orario: str | None = None) -> str:
    """Stato dei sensori di accensione/spegnimento programmati (Fascia 1 e 2).

    ``orario``: None per i sensori che mostrano solo il giorno; per quelli «_interfaccia»
    la voce di cui si mostrano ore e minuti, con ``{giorno}`` al posto del giorno
    (per esempio ``"input_datetime.accensione_{giorno}_2"``).
    """
    if L.v("sensor.sensori_memorizzata") in _NON_VALIDI:
        return "Non disponibile"
    giorno = _GIORNI[L.now().weekday()]
    if not _fasce_valide(L, giorno):
        return "Disabilitata"
    nome = giorno.capitalize()
    if orario is None:
        return nome
    # «Lunedi, {{ states(x)[0:5] }}»: Home Assistant toglie gli spazi alla fine del testo
    return f"{nome}, {L.v(orario.format(giorno=giorno))[0:5]}".strip()


@modello("sensor.status_accensione_vmc_tramite_calendario")
def status_accensione_vmc_tramite_calendario(L: Lettore) -> str:
    return _stato_calendario(L)


@modello("sensor.status_accensione_vmc_tramite_calendario_2")
def status_accensione_vmc_tramite_calendario_2(L: Lettore) -> str:
    return _stato_calendario(L)


@modello("sensor.status_spegnimento_vmc_tramite_calendario")
def status_spegnimento_vmc_tramite_calendario(L: Lettore) -> str:
    return _stato_calendario(L)


@modello("sensor.status_spegnimento_vmc_tramite_calendario_2")
def status_spegnimento_vmc_tramite_calendario_2(L: Lettore) -> str:
    return _stato_calendario(L)


@modello("sensor.status_accensione_vmc_tramite_calendario_interfaccia")
def status_accensione_vmc_tramite_calendario_interfaccia(L: Lettore) -> str:
    return _stato_calendario(L, "input_datetime.accensione_{giorno}")


@modello("sensor.status_accensione_vmc_tramite_calendario_2_interfaccia")
def status_accensione_vmc_tramite_calendario_2_interfaccia(L: Lettore) -> str:
    return _stato_calendario(L, "input_datetime.accensione_{giorno}_2")


@modello("sensor.status_spegnimento_vmc_tramite_calendario_interfaccia")
def status_spegnimento_vmc_tramite_calendario_interfaccia(L: Lettore) -> str:
    return _stato_calendario(L, "input_datetime.spegnimento_{giorno}")


@modello("sensor.status_spegnimento_vmc_tramite_calendario_2_interfaccia")
def status_spegnimento_vmc_tramite_calendario_2_interfaccia(L: Lettore) -> str:
    return _stato_calendario(L, "input_datetime.spegnimento_{giorno}_2")


def _selezione(L: Lettore, chiave: str) -> str:
    """``{{ states(x) | default('') }}``: states() da' sempre un testo, il default non serve mai."""
    return L.v(chiave)


@modello("sensor.speed_1_fascia_calendario")
def speed_1_fascia_calendario(L: Lettore) -> str:
    return _selezione(L, "input_select.speed_1_fascia_calendario")


@modello("sensor.speed_2_fascia_calendario")
def speed_2_fascia_calendario(L: Lettore) -> str:
    return _selezione(L, "input_select.speed_2_fascia_calendario")


@modello("sensor.mese_1_fascia_freecooling")
def mese_1_fascia_freecooling(L: Lettore) -> str:
    return _selezione(L, "input_select.mese_1_fascia_freecooling")


@modello("sensor.mese_1_fascia_freeheating")
def mese_1_fascia_freeheating(L: Lettore) -> str:
    return _selezione(L, "input_select.mese_1_fascia_freeheating")


@modello("sensor.mese_2_fascia_freecooling")
def mese_2_fascia_freecooling(L: Lettore) -> str:
    return _selezione(L, "input_select.mese_2_fascia_freecooling")


@modello("sensor.mese_2_fascia_freeheating")
def mese_2_fascia_freeheating(L: Lettore) -> str:
    return _selezione(L, "input_select.mese_2_fascia_freeheating")
