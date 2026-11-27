"""Free Cooling e Free Heating: stato, mesi, allerte e tasti."""

from __future__ import annotations

from collections.abc import Callable

from ..compat import fl
from ..lettore import Lettore
from . import modello

# valori che i modelli del package trattano come «non disponibile»
_STATI = ("sconosciuto", "unknown", "", None, "unavailable", "Non disponibile")
_MESI = (
    "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre",
)
_INQUINANTI = ", Presenza di Inquinanti"
_SENZA_TEMPERATURE = ("Non disponibile", "[Non Calcolabile]")
# il modello del package va in errore: Home Assistant rende il sensore non disponibile
_ERRORE = "unavailable"

# testi di allerta che il sensore «disabilitato» riconosce (OK)
_AVVISI_DISABILITATO = frozenset(
    {
        "Allerta Free Heating Programmato (Raffrescamento Arrestato)",
        "Allerta Free Heating Programmato (Raffrescamento in atto)",
        "Allerta Free Heating Programmato (Raffrescamento in atto, Presenza di Inquinanti)",
        "Allerta Free Heating Programmato (Raffrescamento Arrestato, Presenza di Inquinanti)",
        "Allerta Free Cooling Programmato (Riscaldamento in atto)",
        "Allerta Free Cooling Programmato (Riscaldamento Arrestato)",
        "Allerta Free Cooling Programmato (Riscaldamento Arrestato, Presenza di Inquinanti)",
        "Allerta Free Cooling Programmato (Riscaldamento in atto, Presenza di Inquinanti)",
        "Allerta Raffrescamento in atto",
        "Allerta Riscaldamento in atto",
        "Allerta Riscaldamento in atto, Presenza di Inquinanti",
        "Allerta Raffrescamento in atto, Presenza di Inquinanti",
        "Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento)",
        "Non Avviare in Velocità Free Heating Programmato (Allerta Raffrescamento, Presenza di Inquinanti)",
        "Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento)",
        "Non Avviare in Velocità Free Cooling Programmato (Allerta Riscaldamento, Presenza di Inquinanti)",
        "Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento)",
        "Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento)",
        "Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento, Presenza di Inquinanti)",
        "Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento, Presenza di Inquinanti)",
    }
)


def _non_disponibile(L: Lettore) -> bool:
    """Lettura grezza dei sensori della VMC assente: tutti i modelli del gruppo danno «Non disponibile»."""
    return L.v("sensor.sensori_memorizzata") in _STATI


# ---------------------------------------------------------------------------------------
# Fasce dei mesi
# ---------------------------------------------------------------------------------------


def _intervallo(mese1: str, mese2: str) -> list[str] | None:
    """Mesi della fascia da ``mese1`` a ``mese2`` compresi, con l'anno che comincia da ``mese1``.

    Nel package: ``mesi[mesi.index(input1):mesi.index(input2)+1]``, con la lista dei mesi
    che comincia da ``input1``. Se ``mese1`` non e' un mese la fascia resta non definita e
    nessun mese ci «sta»: lista vuota. Se ``mese2`` non e' un mese ``index`` va in errore:
    None.
    """
    if mese1 not in _MESI:
        return []
    if mese2 not in _MESI:
        return None
    inizio = _MESI.index(mese1)
    giro = _MESI[inizio:] + _MESI[:inizio]
    return list(giro[: giro.index(mese2) + 1])


def _status_fascia(L: Lettore, tipo: str) -> str:
    """Stato della fascia Free Cooling o Free Heating (``tipo``: freecooling / freeheating)."""
    if _non_disponibile(L):
        return "Non disponibile"
    mese1 = L.v(f"sensor.mese_1_fascia_{tipo}")
    mese2 = L.v(f"sensor.mese_2_fascia_{tipo}")
    check = L.v("sensor.status_check_freeheating_freecooling")
    mese_corrente = _MESI[L.now().month - 1]
    if mese1 in _STATI or mese2 in _STATI or check in _STATI:
        return "Non disponibile"
    intervallo = _intervallo(mese1, mese2)
    if intervallo is None:
        return _ERRORE
    if check == "OK":
        return "OK" if mese_corrente in intervallo else "-"
    return "NOT OK"


@modello("sensor.status_freecooling")
def status_freecooling(L: Lettore) -> str:
    return _status_fascia(L, "freecooling")


@modello("sensor.status_freeheating")
def status_freeheating(L: Lettore) -> str:
    return _status_fascia(L, "freeheating")


def _numero_mese(mese: str, primo: str) -> int:
    """Posizione di ``mese`` (1-12) nell'anno che comincia da ``primo``; 0 se non e' un mese."""
    if mese not in _MESI:
        return 0
    return (_MESI.index(mese) - _MESI.index(primo)) % 12 + 1


@modello("sensor.status_check_freeheating_freecooling")
def status_check_freeheating_freecooling(L: Lettore) -> str:
    """Le due fasce (Free Heating poi Free Cooling) devono seguirsi in ordine nell'anno."""
    if _non_disponibile(L):
        return "Non disponibile"
    mesi = [
        L.v("sensor.mese_1_fascia_freeheating"),
        L.v("sensor.mese_2_fascia_freeheating"),
        L.v("sensor.mese_1_fascia_freecooling"),
        L.v("sensor.mese_2_fascia_freecooling"),
    ]
    if any(m in _STATI for m in mesi):
        return "Non disponibile"
    if mesi[0] not in _MESI:
        # numeri non definiti nel package: il primo confronto (!=) e' falso
        return "NOT OK"
    n1, n2, n3, n4 = (_numero_mese(m, mesi[0]) for m in mesi)
    # nel package anche n1 != n2 != n3 != n4, gia' compresi nei «<»
    if n1 < n2 < n3 < n4:
        return "OK"
    return "NOT OK"


@modello("sensor.status_mese_corrente_freeheating_o_freecooling")
def status_mese_corrente_freeheating_o_freecooling(L: Lettore) -> str:
    if _non_disponibile(L):
        return "Non disponibile"
    heating = L.v("sensor.status_freeheating")
    cooling = L.v("sensor.status_freecooling")
    if heating in _STATI or cooling in _STATI:
        return "Non disponibile"
    if heating == "OK" and L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_freeheating") == "on":
        return "Free Heating"
    if cooling == "OK" and L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_freecooling") == "on":
        return "Free Cooling"
    return "Disabilitata"


# ---------------------------------------------------------------------------------------
# Allerte
# ---------------------------------------------------------------------------------------


def _temperature(L: Lettore) -> tuple[float, float] | str:
    """Temperature interna ed esterna come numeri, o il testo da mostrare se non si possono usare."""
    interna = L.v("sensor.temp_interna_status")
    esterna = L.v("sensor.temp_esterna_status")
    if interna in _SENZA_TEMPERATURE or esterna in _SENZA_TEMPERATURE:
        return "[Non Calcolabile]"
    t_int = fl(interna, None)
    t_est = fl(esterna, None)
    if t_int is None or t_est is None:
        return "[Non Calcolabile]"
    return t_int, t_est


@modello("sensor.alert_monitoraggio_free_heating_o_free_cooling")
def alert_monitoraggio_free_heating_o_free_cooling(L: Lettore) -> str:
    if _non_disponibile(L):
        return "Non disponibile"
    tipologia = L.v("sensor.status_mese_corrente_freeheating_o_freecooling")
    velocita = L.v("sensor.status_ventola_lettura_codice_interpretato")
    if tipologia == "Non disponibile" or velocita == "Non disponibile":
        return "Non disponibile"
    temperature = _temperature(L)
    if isinstance(temperature, str):
        return temperature
    t_int, t_est = temperature
    if velocita != "Free Cooling":
        return "Nessuna Allerta"
    heating_on = L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_freeheating") == "on"
    cooling_on = L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_freecooling") == "on"
    if tipologia == "Free Heating" and t_int > t_est:
        if heating_on:
            return "Allerta Free Heating Programmato (Raffrescamento in atto)"
        return "Allerta Raffrescamento in atto"
    if tipologia == "Free Cooling" and t_est > t_int:
        if cooling_on:
            return "Allerta Free Cooling Programmato (Riscaldamento in atto)"
        return "Allerta Riscaldamento in atto"
    if tipologia == "Disabilitata" and t_int > t_est:
        return "Raffrescamento in atto"
    if tipologia == "Disabilitata" and t_est > t_int:
        return "Riscaldamento in atto"
    return "Nessuna Allerta"


def _avviso_programmato(
    velocita: str,
    spia: str,
    maggiore: bool,
    minore_uguale: bool,
    inquinanti: str,
    programma: str,
    effetto: str,
) -> str | None:
    """Avviso di una fascia programmata (Free Heating o Free Cooling) con l'automazione accesa.

    ``maggiore``: la velocita' Free porterebbe la casa nella direzione sbagliata (interna >
    esterna per il Free Heating: raffrescherebbe; esterna > interna per il Free Cooling:
    riscalderebbe); ``minore_uguale``: il confronto opposto (con un NaN sono falsi entrambi).
    ``programma``: «Free Heating Programmato» / «Free Cooling Programmato»;
    ``effetto``: «Raffrescamento» / «Riscaldamento». None se nessun ramo del package vale.
    """
    in_free = velocita == "Free Cooling"
    if maggiore and spia == "on":
        stato = "in atto" if in_free else "Arrestato"
        return f"Allerta {programma} ({effetto} {stato}{inquinanti})"
    if maggiore and spia == "off":
        if in_free:
            return f"Allerta {programma} ({effetto} in atto{inquinanti})"
        return f"Non Avviare in Velocità {programma} (Allerta {effetto}{inquinanti})"
    if minore_uguale:
        return f"Nessuna Allerta {programma}{inquinanti}"
    return None


@modello("sensor.alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi")
def alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi(L: Lettore) -> str:
    """Avviso per l'interfaccia: fascia programmata, velocita', temperature e inquinanti."""
    if _non_disponibile(L):
        return "Non disponibile"
    tipologia = L.v("sensor.status_mese_corrente_freeheating_o_freecooling")
    velocita = L.v("sensor.status_ventola_lettura_codice_interpretato")
    if tipologia == "Non disponibile" or velocita == "Non disponibile":
        return "Non disponibile"
    temperature = _temperature(L)
    if isinstance(temperature, str):
        return temperature
    t_int, t_est = temperature
    allerta = L.v("sensor.alert_monitoraggio_co2") == "Allerta" or L.v("sensor.alert_monitoraggio_voc") == "Allerta"
    # in ogni testo, «, Presenza di Inquinanti» se CO2 o VOC sono in allerta
    inquinanti = _INQUINANTI if allerta else ""
    avviso: str | None = None
    if tipologia == "Free Heating":
        if L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_freeheating") == "on":
            avviso = _avviso_programmato(
                velocita,
                L.v("input_boolean.spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating"),
                t_int > t_est,
                t_int <= t_est,
                inquinanti,
                "Free Heating Programmato",
                "Raffrescamento",
            )
    elif tipologia == "Free Cooling":
        if L.v("input_boolean.opzioni_accendi_spegni_vmc_vs_freecooling") == "on":
            avviso = _avviso_programmato(
                velocita,
                L.v("input_boolean.spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling"),
                t_est > t_int,
                t_est <= t_int,
                inquinanti,
                "Free Cooling Programmato",
                "Riscaldamento",
            )
    elif tipologia == "Disabilitata":
        in_free = velocita == "Free Cooling"
        if t_int > t_est:
            avviso = (
                f"Allerta Raffrescamento in atto{inquinanti}"
                if in_free
                else f"Se Avviata in Velocità Free Cool./Heat. (Allerta Raffrescamento{inquinanti})"
            )
        elif t_est > t_int:
            avviso = (
                f"Allerta Riscaldamento in atto{inquinanti}"
                if in_free
                else f"Se Avviata in Velocità Free Cool./Heat. (Allerta Riscaldamento{inquinanti})"
            )
        elif t_int == t_est:
            avviso = f"Nessuna Allerta{inquinanti}"
    return avviso if avviso is not None else "Nessuna Allerta"


@modello("sensor.alert_monitoraggio_free_heating_o_free_cooling_disabilitato")
def alert_monitoraggio_free_heating_o_free_cooling_disabilitato(L: Lettore) -> str:
    if _non_disponibile(L):
        return "Non disponibile"
    avviso = L.v("sensor.alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi")
    return "OK" if avviso in _AVVISI_DISABILITATO else "NOT OK"


# ---------------------------------------------------------------------------------------
# Tasti del telecomando
# ---------------------------------------------------------------------------------------


def _velocita_free_attiva(L: Lettore) -> bool:
    """La velocita' in corso e' una Free."""
    return L.v("sensor.status_ventola_lettura_codice_interpretato_interfaccia").startswith("Free")


def _free_registrata(L: Lettore) -> bool:
    """Tra le velocita' registrate (separate da « · ») ce n'e' una Free.

    Nel package ``select('match', 'Free')``: il test ``match`` e' ``re.match``, cioe' «comincia con».
    """
    registrate = L.v("sensor.velocita_registrata").split(" · ")
    return any(parte.startswith("Free") for parte in registrate)


def _tasto(L: Lettore) -> str:
    return "on" if _velocita_free_attiva(L) or _free_registrata(L) else "off"


def _icona_tasto(icona_free: str) -> Callable[[Lettore], str]:
    """Icona dei tasti: quella Free, oppure «ripristina» se una Free e' registrata ma non in corso."""

    def icona(L: Lettore) -> str:
        return icona_free if _velocita_free_attiva(L) or not _free_registrata(L) else "mdi:restore"

    return icona


@modello("binary_sensor.tasto_free_cool_heat", icona=_icona_tasto("mdi:sun-snowflake-variant"))
def tasto_free_cool_heat(L: Lettore) -> str:
    return _tasto(L)


@modello("binary_sensor.tasto_free_cooling", icona=_icona_tasto("mdi:snowflake"))
def tasto_free_cooling(L: Lettore) -> str:
    return _tasto(L)


@modello("binary_sensor.tasto_free_heating", icona=_icona_tasto("mdi:weather-sunny"))
def tasto_free_heating(L: Lettore) -> str:
    return _tasto(L)
