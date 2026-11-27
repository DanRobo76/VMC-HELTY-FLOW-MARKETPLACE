"""Stato della VMC: collegamento, nome, versione, IP inserito, velocita' letta, LED, portata,
ricambi d'aria e tasti del telecomando (sensori binari).

Le risposte grezze della VMC arrivano dai sensori «memorizzati» (ultima lettura valida):
``VMGO,00002,00000,...`` (VMGH?) per lo stato della ventola, ``VMNM Master`` (VMNM?) per il
nome.
"""

from __future__ import annotations

import re
from collections.abc import Callable

from ..compat import fl, it, rnd, testo
from ..lettore import Lettore
from ..risultato import come_stato, come_stato_numerico
from ..versione import VERSIONE_INTEGRAZIONE
from . import modello

# Valori che i modelli del package trattano come «nessuna lettura»
_NON_VALIDI = ("sconosciuto", "unknown", "", None, "unavailable", "Non disponibile")
_ND = "Non disponibile"
_NON_CALCOLABILE = "[Non Calcolabile]"
_SEPARATORE = " · "

# Voci lette da piu' modelli
_MEMORIZZATA = "sensor.status_ventola_memorizzata"
_INTERFACCIA = "sensor.status_ventola_lettura_codice_interpretato_interfaccia"
_REGISTRATA = "sensor.velocita_registrata"
_LED_PANNELLO = "sensor.status_led_pannello_lettura_codice_interpretato"
_SENSORI = "sensor.status_sensori_lettura_codice_interpretato"
_PORTATA = "sensor.status_portata_ventola_lettura_codice_interpretato"
_VOLUME = "input_number.volume_da_inserire"
_MESE_FREE = "sensor.status_mese_corrente_freeheating_o_freecooling"
_ALERT_FREE = "sensor.alert_monitoraggio_free_heating_o_free_cooling"


# --- Come Home Assistant scrive lo stato di un sensore modello: regole comuni in ..risultato


def _come_stato(reso: str) -> str:
    """Stato mostrato da Home Assistant per un modello che rende ``reso``."""
    return come_stato(reso)


def _come_stato_numerico(reso: str) -> str:
    """Come ``_come_stato`` per un sensore con unita' di misura (stato numerico)."""
    return come_stato_numerico(reso)


def _binario(condizione: bool) -> str:
    return "on" if condizione else "off"


# --- Versione e IP ---------------------------------------------------------------------------


@modello("sensor.versione_corrente")
def versione_corrente(L: Lettore) -> str:
    return f"v.{VERSIONE_INTEGRAZIONE}"


_RE_IP = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
)
_RE_SENSORE_IP = re.compile(r"^sensor\.vmc_[a-z]+_ip$")


def _ip_altre_vmc(L: Lettore) -> list[str]:
    """Stati dei sensori IP delle altre VMC.

    Nel package: ``states.sensor | rejectattr('attributes.restored', 'eq', true)
    | selectattr('entity_id', 'search', '^sensor\\.vmc_[a-z]+_ip$')`` senza il sensore IP di
    questa VMC.
    """
    proprio = L.entity_id("sensor.ip")
    return [
        str(s.state)
        for s in L.elenca("sensor")
        if s.attributes.get("restored") is not True
        and _RE_SENSORE_IP.search(s.entity_id)
        and s.entity_id != proprio
    ]


@modello("sensor.ip")
def ip(L: Lettore) -> str:
    """IP configurato della VMC (nel package scritto come testo fisso all'installazione)."""
    return L.ip.strip()


@modello("sensor.verifica_ip_inserito")
def verifica_ip_inserito(L: Lettore) -> str:
    ip = L.v("input_text.ip_insert").strip()
    esito = L.v("input_text.ip_insert_esito")
    ottetti = [it(x, 0) for x in ip.split(".") + ["", ""]]
    in_uso = any(stato.strip() == ip for stato in _ip_altre_vmc(L))
    if ip == "":
        return "Nessun IP"
    if (
        not _RE_IP.match(ip)
        or ottetti[0] in (0, 127)
        or ottetti[0] >= 224
        or ottetti[:2] == [169, 254]
    ):
        return "IP non Valido"
    if ip == L.v("sensor.ip").strip():
        return "IP già impostato"
    if in_uso:
        return "IP già in uso"
    if esito == "non_risponde " + ip:
        return "VMC non risponde"
    if esito == "altro_dispositivo " + ip:
        return "Non è una VMC"
    if esito == "nome_diverso " + ip:
        return "Nome VMC diverso"
    if esito != "ok " + ip:
        return "Verifica VMC in corso"
    return ip


# --- Collegamento e nome ---------------------------------------------------------------------


def _icona_status_ip_interfaccia(L: Lettore) -> str:
    return "mdi:fan-alert" if L.v("sensor.status_ip") == "OFF-Line" else "mdi:fan-chevron-down"


@modello("sensor.status_ip_interfaccia", icona=_icona_status_ip_interfaccia)
def status_ip_interfaccia(L: Lettore) -> str:
    return "OFF-Line" if L.v("sensor.status_ip") in ("OFF-Line",) else "ON-Line"


@modello("sensor.nome_status")
def nome_status(L: Lettore) -> str:
    """Nome della VMC dalla risposta ``VMNM <nome>``."""
    nome = L.v("sensor.nome_memorizzata")
    if nome in _NON_VALIDI:
        return _ND
    parti = nome.split(" ", 1)
    if len(parti) >= 2:
        return _come_stato(parti[1].strip())
    return _ND


# --- Risposta VMGH?: velocita', sensori, LED del pannello, portata ---------------------------

_CODICI_VELOCITA = {
    "00000": "Velocità 0",
    "00001": "Velocità 1",
    "00002": "Velocità 2",
    "00003": "Velocità 3",
    "00004": "Velocità 4",
    "00005": "Iperventilazione",
    "00006": "Notturna",
}
_CODICE_FREE = "00007"
_CODICI = {**_CODICI_VELOCITA, _CODICE_FREE: "Free Cooling"}
_CODICI_SENSORI = {"00003": "Spenti", "00001": "Accesi", "00002": "Spenti", "00000": "Accesi"}
_PORTATE = {
    "00000": "-",
    "00001": "10",
    "00002": "17",
    "00003": "26",
    "00004": "37",
    "00005": "42",
    "00006": "10",
    "00007": "26",
}


def _componenti(L: Lettore) -> list[str] | None:
    """Campi dell'ultima risposta VMGH? valida, None se non c'e' una lettura."""
    memorizzata = L.v(_MEMORIZZATA)
    if memorizzata in _NON_VALIDI:
        return None
    return memorizzata.split(",")


@modello("sensor.status_ventola_lettura_codice")
def status_ventola_lettura_codice(L: Lettore) -> str:
    componenti = _componenti(L)
    if componenti is None or len(componenti) <= 1:
        return _ND
    return componenti[1] if componenti[1] in _CODICI else _ND


@modello("sensor.status_ventola_lettura_codice_interpretato")
def status_ventola_lettura_codice_interpretato(L: Lettore) -> str:
    componenti = _componenti(L)
    if componenti is None or len(componenti) <= 1:
        return _ND
    return _CODICI.get(componenti[1], _ND)


def _nome_free_interfaccia(L: Lettore) -> str:
    """Nome del codice 00007 nello Status Ventilazione dell'interfaccia (mese corrente)."""
    free_h_c = L.v(_ALERT_FREE)
    if L.is_v(_MESE_FREE, "Free Heating") and free_h_c != _NON_CALCOLABILE:
        return "Free Heating"
    if L.is_v(_MESE_FREE, "Free Cooling") and free_h_c != _NON_CALCOLABILE:
        return "Free Cooling"
    if L.is_v(_MESE_FREE, "Disabilitata") or free_h_c == _NON_CALCOLABILE:
        return "Free Cool./Heat."
    return "Free Cooling"


@modello(_INTERFACCIA)
def status_ventola_lettura_codice_interpretato_interfaccia(L: Lettore) -> str:
    nome_free = _nome_free_interfaccia(L)
    componenti = _componenti(L)
    if componenti is None or len(componenti) <= 1:
        return _ND
    codice = componenti[1]
    if codice == _CODICE_FREE:
        return nome_free
    return _CODICI_VELOCITA.get(codice, _ND)


@modello(_SENSORI)
def status_sensori_lettura_codice_interpretato(L: Lettore) -> str:
    componenti = _componenti(L)
    if componenti is None or len(componenti) <= 4:
        return _ND
    return _CODICI_SENSORI.get(componenti[4], _ND)


@modello(_LED_PANNELLO)
def status_led_pannello_lettura_codice_interpretato(L: Lettore) -> str:
    componenti = _componenti(L)
    if componenti is None or len(componenti) <= 14:
        return _ND
    if componenti[14] == "00000":
        return "Spento"
    if componenti[14] == "00032":
        return "Verificare Filtro"
    return "Acceso"


@modello(_PORTATA)
def status_portata_ventola_lettura_codice_interpretato(L: Lettore) -> str:
    componenti = _componenti(L)
    if componenti is None:
        return _ND
    if len(componenti) <= 1:
        return "-"
    return _PORTATE.get(componenti[1], _ND)


# --- Velocita' registrata (da ripristinare) e tasti del telecomando --------------------------

# [schema della spia, chiavi provate, nome fisso (solo per gli avvisi Free)]: «{}» e' la chiave
_TUTTE = ("0", "1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")
_ALLERTE: tuple[tuple[str, tuple[str, ...], str | None], ...] = (
    ("input_boolean.spia_velocita_{}_congelamento", _TUTTE, None),
    ("input_boolean.spia_velocita_{}_delta_temp_verifica_soglia_valore", _TUTTE, None),
    ("input_boolean.spia_velocita_{}_co2_o_voc", ("0",), None),
    ("input_boolean.spia_co2_o_voc_partenza_ritorno_velocita_0", ("0",), None),
    ("input_boolean.spia_velocita_{}_un_solo_avvio", _TUTTE, None),
    ("input_boolean.spia_velocita_1_co2_o_voc_pdr", ("0",), None),
    (
        "input_boolean.spia_velocita_{}_un_solo_avvio_per_programmazione_freecooling",
        ("freecooling",),
        "Free Cooling",
    ),
    (
        "input_boolean.spia_velocita_{}_un_solo_avvio_per_programmazione_freeheating",
        ("freecooling",),
        "Free Heating",
    ),
    ("input_boolean.spia_umidita_velocita_{}", _TUTTE, None),
    ("input_boolean.spia_velocita_{}", _TUTTE, None),
)


def _chiave_attuale(attuale: str) -> str:
    """Chiave della velocita' attuale nello schema delle spie."""
    if attuale.startswith("Free"):
        return "freecooling"
    if attuale == "Notturna":
        return "notturna"
    if attuale == "Iperventilazione":
        return "iperventilazione"
    return attuale.replace("Velocità ", "")


@modello(_REGISTRATA)
def velocita_registrata(L: Lettore) -> str:
    """Velocita' interrotte da un'allerta, da ripristinare (``Nessuna`` se non ce ne sono)."""
    mese_free = L.v(_MESE_FREE)
    nome_free = (
        mese_free
        if mese_free in ("Free Heating", "Free Cooling") and L.v(_ALERT_FREE) != _NON_CALCOLABILE
        else "Free Heat./Cool."
    )
    nomi = {
        "0": "Velocità 0",
        "1": "Velocità 1",
        "2": "Velocità 2",
        "3": "Velocità 3",
        "4": "Velocità 4",
        "notturna": "Notturna",
        "iperventilazione": "Iperventilazione",
        "freecooling": nome_free,
    }
    annullata = L.is_v("timer.countdown_free_heating_annullamento", "active") or L.is_v(
        "timer.countdown_free_cooling_annullamento", "active"
    )
    attuale = L.v(_INTERFACCIA)
    chiave_attuale = _chiave_attuale(attuale)
    righe: list[str] = []
    viste: list[str] = []
    for schema, chiavi, nome_fisso in _ALLERTE:
        for k in chiavi:
            if (
                L.is_v(schema.replace("{}", k), "on")
                and k != chiave_attuale
                and k not in viste
                and not (nome_fisso is not None and annullata)
            ):
                righe.append(nome_fisso if nome_fisso is not None else nomi[k])
                viste.append(k)
    if righe and attuale != _ND:
        return _SEPARATORE.join(righe)[:255].strip()
    return "Nessuna"


def _tasto_velocita(chiave: str, nome: str, icona_libera: str) -> None:
    """Registra il tasto del telecomando di una velocita' (acceso se e' quella attuale o se
    e' da ripristinare; icona «restore» solo se e' da ripristinare e non e' l'attuale)."""

    def attuale(L: Lettore) -> bool:
        return L.v(_INTERFACCIA) == nome

    def registrata(L: Lettore) -> bool:
        return nome in L.v(_REGISTRATA).split(_SEPARATORE)

    def icona(L: Lettore) -> str:
        return icona_libera if attuale(L) or not registrata(L) else "mdi:restore"

    def stato(L: Lettore) -> str:
        return _binario(attuale(L) or registrata(L))

    modello(chiave, icona=icona)(stato)


for _chiave, _nome, _icona in (
    ("binary_sensor.tasto_velocita_0", "Velocità 0", "mdi:numeric-0-box"),
    ("binary_sensor.tasto_velocita_1", "Velocità 1", "mdi:numeric-1-box"),
    ("binary_sensor.tasto_velocita_2", "Velocità 2", "mdi:numeric-2-box"),
    ("binary_sensor.tasto_velocita_3", "Velocità 3", "mdi:numeric-3-box"),
    ("binary_sensor.tasto_velocita_4", "Velocità 4", "mdi:numeric-4-box"),
    ("binary_sensor.tasto_notturna", "Notturna", "mdi:weather-night"),
    ("binary_sensor.tasto_iperventilazione", "Iperventilazione", "mdi:wind-power"),
):
    _tasto_velocita(_chiave, _nome, _icona)


def _tasto_uguale(
    chiave: str,
    voce: str,
    valori: tuple[str, ...],
    icona: Callable[[Lettore], str] | None = None,
) -> None:
    """Registra un tasto acceso quando la voce letta vale uno dei valori."""

    def stato(L: Lettore) -> str:
        return _binario(L.v(voce) in valori)

    modello(chiave, icona=icona)(stato)


def _icona_tasto_led_pannello_on(L: Lettore) -> str:
    return "mdi:air-filter" if L.v(_LED_PANNELLO) == "Verificare Filtro" else "mdi:led-on"


_tasto_uguale("binary_sensor.tasto_sensori_on", _SENSORI, ("Accesi",))
_tasto_uguale("binary_sensor.tasto_sensori_off", _SENSORI, ("Spenti",))
_tasto_uguale(
    "binary_sensor.tasto_led_pannello_on",
    _LED_PANNELLO,
    ("Acceso", "Verificare Filtro"),
    _icona_tasto_led_pannello_on,
)
_tasto_uguale("binary_sensor.tasto_led_pannello_off", _LED_PANNELLO, ("Spento",))


# --- LED dell'interfaccia --------------------------------------------------------------------

# spie «un solo avvio per programmazione» del Free Heating e del Free Cooling
_SPIA_UN_SOLO_AVVIO_FREE = (
    "input_boolean.spia_velocita_freecooling_un_solo_avvio_per_programmazione_{}"
)


@modello("sensor.stato_led_interfaccia")
def stato_led_interfaccia(L: Lettore) -> str:
    """Colore del LED della scheda: grigio (VMC non in linea), giallo, giallo lento, rosso,
    blu, bianco."""
    velocita = L.v(_INTERFACCIA)
    if L.v("sensor.status_ip_interfaccia") != "ON-Line" or velocita in _NON_VALIDI:
        return "grigio"
    congelamento = L.is_v("input_boolean.congelamento_verifica_soglia_valore_spia", "on") or L.is_v(
        "sensor.congelamento_verifica_soglia", "Si"
    )
    delta = L.is_v("input_boolean.delta_temp_verifica_soglia_valore_spia", "on")
    pdr = (
        L.is_v("input_boolean.opzioni_accendi_spegni_vmc_vs_pdr", "on")
        and L.v("sensor.punto_di_rugiada_verifica_confronto") == "Se ne sconsiglia l'impiego"
    )
    free = L.v("sensor.alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi")
    free_bloccata = (
        "Arrestato" in free
        or L.is_v(_SPIA_UN_SOLO_AVVIO_FREE.format("freeheating"), "on")
        or L.is_v(_SPIA_UN_SOLO_AVVIO_FREE.format("freecooling"), "on")
    )
    if velocita == "Velocità 0":
        if congelamento or delta or pdr or free_bloccata:
            return "giallo"
        if L.is_v("sensor.alert_monitoraggio_totale", "Allerta"):
            return "giallo lento"
        return "bianco"
    if delta or congelamento:
        return "giallo"
    if L.is_v("input_boolean.spia_co2_o_voc", "on"):
        return "rosso"
    if L.is_v("input_boolean.umidita_verifica_soglia_valore_spia", "on"):
        return "blu"
    return "bianco"


# --- Tempo di ricambio e aria scambiata ------------------------------------------------------


def _unita(numero: int, singolare: str, plurale: str) -> str:
    return f"{numero} {singolare if numero == 1 else plurale}"


def _durata_ricambio(tempo_sec: int) -> str:
    """Durata del Tempo ricambio aria: ``2 ore, 5 minuti e 3 secondi``."""
    ore = tempo_sec // 3600
    minuti = (tempo_sec % 3600) // 60
    secondi = tempo_sec % 60
    parte_minuti = _unita(minuti, "minuto", "minuti") if minuti > 0 else ""
    parte_secondi = _unita(secondi, "secondo", "secondi") if secondi > 0 else ""
    if ore > 0:
        return (
            _unita(ore, "ora", "ore")
            + (", " if minuti > 0 or secondi > 0 else "")
            + parte_minuti
            + (" e " if secondi > 0 and minuti > 0 else "")
            + parte_secondi
        )
    if minuti > 0:
        return parte_minuti + (" e " if secondi > 0 else "") + parte_secondi
    return _unita(secondi, "secondo", "secondi")


@modello("sensor.status_calcolo_portata_ventola")
def status_calcolo_portata_ventola(L: Lettore) -> str:
    """Tempo per ricambiare tutto il volume della casa alla portata attuale."""
    portata_str = L.v(_PORTATA)
    volume_str = L.v(_VOLUME)
    if portata_str in _NON_VALIDI or volume_str in _NON_VALIDI:
        return _ND
    portata = fl(portata_str, 0)
    volume = fl(volume_str, 0)
    if portata <= 0 or volume <= 0:
        return "-"
    return _durata_ricambio(rnd((volume / portata) * 3600, 0))


_ARIA_SCAMBIATA = (
    "input_number.aria_scambiata_v1",
    "input_number.aria_scambiata_v2",
    "input_number.aria_scambiata_v3",
    "input_number.aria_scambiata_v4",
    "input_number.aria_scambiata_iperventilazione",
    "input_number.aria_scambiata_notte",
    "input_number.aria_scambiata_freecooling",
)


@modello("sensor.status_calcolo_aria_scambiata_totale")
def status_calcolo_aria_scambiata_totale(L: Lettore) -> str:
    """Somma dell'aria scambiata oggi alle varie velocita' [m³]."""
    valori = [fl(L.v(voce), 0) for voce in _ARIA_SCAMBIATA]
    totale = valori[0]
    for valore in valori[1:]:
        totale = totale + valore
    return _come_stato_numerico(testo(rnd(totale, 3)))


@modello("sensor.cicli_ricambio_aria")
def cicli_ricambio_aria(L: Lettore) -> str:
    """Ricambi d'aria completi di oggi (aria scambiata / volume)."""
    volume = fl(L.v(_VOLUME), 1)
    aria_totale = fl(L.v("sensor.status_calcolo_aria_scambiata_totale"), 0)
    if volume > 0:
        return _come_stato_numerico(testo(rnd(aria_totale / volume, 2)))
    return "0"


_INVALIDI_MANCANTE = ("unknown", "unavailable", "", "none", None, _ND)


def _durata_mancante(tempo_sec: int) -> str:
    """Durata del Tempo mancante: ``2 ore e 5 minuti`` (senza secondi se ci sono minuti)."""
    ore = tempo_sec // 3600
    minuti = (tempo_sec % 3600) // 60
    secondi = tempo_sec % 60
    if ore == 0 and minuti == 0:
        return _unita(secondi, "secondo", "secondi")
    if ore == 0:
        return _unita(minuti, "minuto", "minuti")
    if minuti == 0:
        return _unita(ore, "ora", "ore")
    return f"{_unita(ore, 'ora', 'ore')} e {_unita(minuti, 'minuto', 'minuti')}"


@modello("sensor.tempo_mancante_ricambio")
def tempo_mancante_ricambio(L: Lettore) -> str:
    """Tempo che manca per ricambiare il volume residuo (tutto dopo un reset)."""
    portata_str = L.v(_PORTATA)
    volume_str = L.v(_VOLUME)
    ricambiato_str = L.v("input_number.aria_scambiata_ricomincio")
    reset = L.v("input_text.tempo_mancante_reset") == "reset"
    if (
        portata_str in _INVALIDI_MANCANTE
        or volume_str in _INVALIDI_MANCANTE
        or ricambiato_str in _INVALIDI_MANCANTE
    ):
        return _ND
    portata = fl(portata_str, 0)
    volume = fl(volume_str, 0)
    ricambiato = fl(ricambiato_str, 0)
    residuo = volume - ricambiato
    if residuo < 0:
        residuo = 0
    if portata <= 0 or volume <= 0:
        return "-"
    if reset or residuo == 0:
        tempo_sec_float = (volume / portata) * 3600
    else:
        tempo_sec_float = (residuo / portata) * 3600
    return _durata_mancante(it(rnd(tempo_sec_float, 0), 0))
