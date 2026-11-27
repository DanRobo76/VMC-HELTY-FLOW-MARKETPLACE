"""Temperature, umidita', punto di rugiada e umidita' assoluta, interne ed esterne.

I sensori vengono a coppie (esterno/interno) e a famiglie (``_grafico``,
``_senza_offset``): ogni famiglia ha una funzione comune con parametri, e ogni sensore
del package e' una funzione di una riga che la chiama con i suoi.

Ogni funzione rende il testo del modello del package; poi il testo diventa lo stato come
in Home Assistant:
- Home Assistant interpreta il risultato (``21.30`` diventa il numero 21.3, ``None``
  nessun valore); i sensori con unita' di misura lo vogliono numerico (altrimenti
  ``unknown``); i numeri decimali si scrivono con al piu' 15 cifre significative;
- un errore del modello (divisione per zero, numero fuori scala, ``int`` impossibile)
  rende il sensore ``unavailable``;
- lo stato cambia solo se il nuovo risultato e' diverso (``!=``) dal precedente: dopo
  ``100.0`` un risultato ``100`` lascia scritto ``100.0`` (e cosi' ``-0.0`` e ``0.0``,
  ``-100`` e ``-100.0``). Per questo si ricorda, per ogni VMC, l'ultimo risultato di ogni
  sensore (``L.memoria``).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from functools import wraps
from typing import Any

from ..compat import fl, is_number, rnd, testo
from ..lettore import Lettore
from ..risultato import ERRORE, interpreta, stato_numerico, stato_testo, uguali
from . import MEMORIA_PROPRIA, modello

ND = "Non disponibile"
NC = "[Non Calcolabile]"
ND_PARENTESI = "[Non Disponibile]"

# stati di «sensori memorizzata» (la lettura grezza delle sonde) che valgono «non disponibile»
_STATI_MEMORIZZATA = ("sconosciuto", "unknown", "", None, "unavailable", "Non disponibile")
# stati di un sensore scelto (o della sonda) che valgono «non disponibile»
_STATI_SCELTO = ("unknown", "unavailable", "-100", "Non disponibile")

_MEMORIZZATA = "sensor.sensori_memorizzata"

# le parti di «sensori memorizzata»: VMGI,<temp. interna>,<temp. esterna>,<umidita'>,...
_INDICE_TEMP = {"interna": 1, "esterna": 2}
_INDICE_UMIDITA = 3


# --- come Home Assistant trasforma il testo reso in stato ---------------------------------
# (regole comuni in ..risultato)


class _ErroreModello(Exception):
    """Il modello del package andrebbe in errore (TemplateError): il sensore e' ``unavailable``."""


# Ultimo risultato e ultimo stato di ogni sensore: L.memoria[chiave] = (risultato, stato),
# una memoria per VMC che dura da un calcolo all'altro. Come Home Assistant, lo stato cambia
# solo con un risultato diverso dal precedente. Un sensore con «availability» non rende lo
# stato mentre non e' disponibile, quindi lo confronta con l'ultimo risultato reso da
# disponibile: il calcolo infatti non chiama la funzione dello stato quando ``disponibile``
# e' falso. Si segue Home Assistant da un calcolo all'altro, non i risultati intermedi che
# Home Assistant rende dentro un giro, a ogni ingresso cambiato.


def _sensore(
    chiave: str, stato_da: Callable[[Any], str], **opzioni: Any
) -> Callable[[Callable[[Lettore], str]], Callable[[Lettore], str]]:
    """Registra il modello ``chiave``: la funzione rende il testo, ``stato_da`` ne fa lo stato."""

    def registra(funzione: Callable[[Lettore], str]) -> Callable[[Lettore], str]:
        @wraps(funzione)
        def stato(L: Lettore) -> str:
            try:
                risultato = interpreta(funzione(L))
            except (_ErroreModello, ArithmeticError):
                risultato = ERRORE
            precedente = L.memoria.get(chiave)
            if precedente is not None and uguali(precedente[0], risultato):
                return precedente[1]
            # i sensori con «availability» (i grafici) non vanno mai in errore
            nuovo = "unavailable" if risultato is ERRORE else stato_da(risultato)
            L.memoria[chiave] = (risultato, nuovo)
            return nuovo

        MEMORIA_PROPRIA.add(chiave)
        return modello(chiave, **opzioni)(stato)

    return registra


def _testo(chiave: str, **opzioni: Any) -> Callable[[Callable[[Lettore], str]], Callable[[Lettore], str]]:
    """Sensore senza unita' di misura."""
    return _sensore(chiave, stato_testo, **opzioni)


def _numerico(chiave: str, **opzioni: Any) -> Callable[[Callable[[Lettore], str]], Callable[[Lettore], str]]:
    """Sensore con unita' di misura (o classe): lo stato e' un numero oppure ``unknown``."""
    return _sensore(chiave, stato_numerico, **opzioni)


def _int_modello(valore: str) -> int:
    """``int(x)`` del modello su un testo di sole cifre; se non si puo' il modello va in errore."""
    try:
        return int(valore, 10)
    except ValueError:
        try:
            return int(float(valore))
        except (ValueError, OverflowError) as errore:
            raise _ErroreModello(valore) from errore


def _log(valore: float) -> float:
    """``log(x)`` del modello (base e, come Home Assistant)."""
    return math.log(float(valore), math.e)


# --- sensori scelti dall'utente -----------------------------------------------------------


def _scelto_esterno(L: Lettore, chiave_scelta: str, attributo: str) -> str:
    """Sensore esterno scelto: un sensore numerico oppure l'attributo di un'entita' meteo."""
    entity_id = L.v(chiave_scelta)
    if entity_id.startswith("sensor."):
        stato = L.s(entity_id)
        return stato if is_number(stato) else "-100"
    if entity_id.startswith("weather."):
        valore = L.attr(entity_id, attributo)
        return testo(valore) if valore is not None else "-100"
    return "-100"


def _scelto_interno(L: Lettore, chiave_scelta: str) -> str:
    """Sensore interno scelto: il suo stato se e' un numero, altrimenti -100."""
    entity_id = L.v(chiave_scelta)
    if entity_id and is_number(L.s(entity_id)):
        return L.s(entity_id)
    return "-100"


@_numerico("sensor.temperatura_esterna_selezionata")
def temperatura_esterna_selezionata(L: Lettore) -> str:
    return _scelto_esterno(L, "input_select.selected_temp_external_entity", "temperature")


@_numerico("sensor.temperatura_interna_selezionata")
def temperatura_interna_selezionata(L: Lettore) -> str:
    return _scelto_interno(L, "input_select.selected_temp_internal_entity")


@_numerico("sensor.umidita_esterna_selezionata")
def umidita_esterna_selezionata(L: Lettore) -> str:
    return _scelto_esterno(L, "input_select.selected_humidity_external_entity", "humidity")


@_numerico("sensor.umidita_interna_selezionata")
def umidita_interna_selezionata(L: Lettore) -> str:
    return _scelto_interno(L, "input_select.selected_humidity_internal_entity")


# --- sonde della VMC: segno e temperatura senza Offset, umidita' senza Offset ---------------


def _segno(L: Lettore, lato: str) -> str:
    """Segno della temperatura: la parte della sonda comincia con 1 se e' negativa."""
    memorizzata = L.v(_MEMORIZZATA)
    if memorizzata in _STATI_MEMORIZZATA:
        return ND
    componenti = memorizzata.split(",")
    indice = _INDICE_TEMP[lato]
    if len(componenti) > indice:
        # una parte vuota non ha prima cifra (nel modello e' «undefined», diverso da '1')
        prima_cifra = componenti[indice][:1]
        return "negativo" if prima_cifra == "1" else "positivo"
    return ND


def _temp_senza_offset(L: Lettore, lato: str) -> str:
    """Temperatura della sonda della VMC in decimi, con il segno letto a parte."""
    memorizzata = L.v(_MEMORIZZATA)
    segno = L.v(f"sensor.temp_{lato}_positivo_negativo")
    if memorizzata not in _STATI_SCELTO and segno in ("positivo", "negativo"):
        componenti = memorizzata.split(",")
        indice = _INDICE_TEMP[lato]
        if len(componenti) > indice:
            grezza = componenti[indice]
            cifre_ok = grezza.isdigit() or (grezza.startswith("1") and grezza[1:].isdigit())
            # un solo carattere con segno negativo non ha cifre dopo l'1: non disponibile
            if cifre_ok and not (segno == "negativo" and len(grezza) < 2):
                if segno == "negativo":
                    valore = -(float(_int_modello(grezza[1:]) / 10))
                else:
                    valore = float(_int_modello(grezza) / 10)
                return testo(rnd(valore, 1))
            return ND
        return ND
    return ND


@_testo("sensor.temp_esterna_positivo_negativo")
def temp_esterna_positivo_negativo(L: Lettore) -> str:
    return _segno(L, "esterna")


@_testo("sensor.temp_interna_positivo_negativo")
def temp_interna_positivo_negativo(L: Lettore) -> str:
    return _segno(L, "interna")


@_testo("sensor.temp_esterna_status_senza_offset")
def temp_esterna_status_senza_offset(L: Lettore) -> str:
    return _temp_senza_offset(L, "esterna")


@_testo("sensor.temp_interna_status_senza_offset")
def temp_interna_status_senza_offset(L: Lettore) -> str:
    return _temp_senza_offset(L, "interna")


@_testo("sensor.umidita_interna_status_senza_offset")
def umidita_interna_status_senza_offset(L: Lettore) -> str:
    memorizzata = L.v(_MEMORIZZATA)
    if memorizzata in _STATI_SCELTO:
        return ND
    componenti = memorizzata.split(",")
    if len(componenti) > _INDICE_UMIDITA:
        umidita = fl(componenti[_INDICE_UMIDITA], 0) / 10
        if umidita > 100:
            return "100"
        if umidita <= 0:
            return NC
        return testo(rnd(umidita, 1))
    return ND


# --- temperatura e umidita' con Offset ----------------------------------------------------


def _sonda_vmc(L: Lettore, chiave_senza_offset: str) -> str:
    """Sensore scelto non disponibile: si usa la sonda della VMC, senza Offset."""
    vmc = fl(L.v(chiave_senza_offset), None)
    return testo(rnd(vmc, 1)) if vmc is not None else ND


def _temp_status(L: Lettore, lato: str) -> str:
    """Temperatura del sensore scelto piu' l'Offset (o la sonda della VMC)."""
    scelta = L.v(f"sensor.temperatura_{lato}_selezionata")
    if scelta in _STATI_SCELTO:
        return _sonda_vmc(L, f"sensor.temp_{lato}_status_senza_offset")
    valore = fl(scelta, None)
    if valore is None:
        return NC
    return testo(rnd(valore + fl(L.v(f"input_number.offset_temp_{lato}"), 0), 1))


@_testo("sensor.temp_esterna_status")
def temp_esterna_status(L: Lettore) -> str:
    return _temp_status(L, "esterna")


@_testo("sensor.temp_interna_status")
def temp_interna_status(L: Lettore) -> str:
    return _temp_status(L, "interna")


@_testo("sensor.umidita_esterna_status")
def umidita_esterna_status(L: Lettore) -> str:
    """Umidita' esterna scelta piu' l'Offset (non c'e' una sonda esterna di riserva)."""
    if L.v("sensor.umidita_esterna_selezionata") in _STATI_SCELTO:
        return ND
    umidita = L.v("sensor.umidita_esterna_selezionata")
    if fl(umidita, None) is None:
        return NC
    relativa = fl(umidita, 0) + fl(L.v("input_number.offset_umidita_esterna"), 0)
    if relativa > 0 and relativa <= 100:
        return testo(rnd(relativa, 1))
    if relativa <= 0:
        return NC
    return "100"


@_testo("sensor.umidita_interna_status")
def umidita_interna_status(L: Lettore) -> str:
    """Umidita' interna scelta piu' l'Offset (o la sonda della VMC)."""
    umidita = L.v("sensor.umidita_interna_selezionata")
    offset = fl(L.v("input_number.offset_umidita_interna"), 0)
    if L.v("sensor.umidita_interna_selezionata") in _STATI_SCELTO:
        return _sonda_vmc(L, "sensor.umidita_interna_status_senza_offset")
    valore = fl(umidita, None)
    if valore is None:
        return NC
    relativa = valore + offset
    if relativa > 100:
        return "100"
    if relativa <= 0:
        return NC
    return testo(rnd(relativa, 1))


# --- punto di rugiada ---------------------------------------------------------------------


def _punto_di_rugiada(L: Lettore, lato: str, stati_memorizzata: tuple[str | None, ...]) -> str:
    """Punto di rugiada (formula di Magnus) da temperatura e umidita' con Offset."""
    if L.v(_MEMORIZZATA) in stati_memorizzata:
        return ND
    rh = fl(L.v(f"sensor.umidita_{lato}_status"), None)
    tc = fl(L.v(f"sensor.temp_{lato}_status"), None)
    if rh is None or tc is None:
        return ND_PARENTESI
    es = 6.11 * 10 ** ((7.5 * tc) / (237.7 + tc))
    e = (es * rh) / 100
    if rh > 0 and rh <= 100 and e > 0:
        dp = (-430.22 + 237.7 * _log(e)) / (-_log(e) + 19.08)
        return testo(rnd(dp, 2))
    return NC


@_testo("sensor.punto_di_rugiada_interno")
def punto_di_rugiada_interno(L: Lettore) -> str:
    # qui il package considera non disponibili solo 'unknown' e 'unavailable'
    return _punto_di_rugiada(L, "interna", ("unknown", "unavailable"))


@_testo("sensor.punto_di_rugiada_esterno")
def punto_di_rugiada_esterno(L: Lettore) -> str:
    return _punto_di_rugiada(L, "esterna", _STATI_MEMORIZZATA)


@_testo("sensor.punto_di_rugiada_interno_esterno_non_calcolabile")
def punto_di_rugiada_interno_esterno_non_calcolabile(L: Lettore) -> str:
    if L.v(_MEMORIZZATA) in _STATI_MEMORIZZATA:
        return ND
    interno = L.v("sensor.punto_di_rugiada_interno")
    esterno = L.v("sensor.punto_di_rugiada_esterno")
    if interno == NC or esterno == NC:
        return NC
    if interno in (ND, ND_PARENTESI) or esterno in (ND, ND_PARENTESI):
        return ND
    return "Si può impiegare"


def _delta_rugiada(interno: float, esterno: float) -> float:
    """Δ punto di rugiada [Ext-Int] arrotondato a 2 decimali, come i due punti di rugiada."""
    return rnd(esterno - interno, 2)


@_testo("sensor.punto_di_rugiada_valore")
def punto_di_rugiada_valore(L: Lettore) -> str:
    if L.v(_MEMORIZZATA) in _STATI_MEMORIZZATA:
        return ND
    interno_testo = L.v("sensor.punto_di_rugiada_interno")
    esterno_testo = L.v("sensor.punto_di_rugiada_esterno")
    calcolabilita = L.v("sensor.punto_di_rugiada_interno_esterno_non_calcolabile")
    if calcolabilita == ND:
        return ND
    if calcolabilita == NC:
        return NC
    if calcolabilita != "Si può impiegare":
        return NC
    if interno_testo == ND or esterno_testo == ND:
        return ND
    if interno_testo == NC or esterno_testo == NC:
        return NC
    interno = fl(interno_testo, None)
    esterno = fl(esterno_testo, None)
    if interno is None or esterno is None:
        return NC
    return testo(_delta_rugiada(interno, esterno))


@_testo("sensor.punto_di_rugiada_verifica_confronto")
def punto_di_rugiada_verifica_confronto(L: Lettore) -> str:
    """Si consiglia la VMC se il Δ punto di rugiada e' sotto il limite impostato."""
    if L.v(_MEMORIZZATA) in _STATI_MEMORIZZATA:
        return ND
    interno_testo = L.v("sensor.punto_di_rugiada_interno")
    esterno_testo = L.v("sensor.punto_di_rugiada_esterno")
    limite = fl(L.v("input_number.offset_verifica_impiego_vmc"), None)
    if L.v("sensor.punto_di_rugiada_interno_esterno_non_calcolabile") == NC:
        return NC
    interno = fl(interno_testo, None)
    esterno = fl(esterno_testo, None)
    if interno is None or esterno is None or limite is None:
        return ND_PARENTESI
    if _delta_rugiada(interno, esterno) < limite:
        return "Si può impiegare"
    return "Se ne sconsiglia l'impiego"


@_testo("sensor.punto_di_rugiada_verifica_confronto_valore")
def punto_di_rugiada_verifica_confronto_valore(L: Lettore) -> str:
    """Il Δ punto di rugiada rilevato, confrontato a parole con il limite impostato."""
    if L.v(_MEMORIZZATA) in _STATI_MEMORIZZATA:
        return ND
    interno_testo = L.v("sensor.punto_di_rugiada_interno")
    esterno_testo = L.v("sensor.punto_di_rugiada_esterno")
    if L.v("sensor.punto_di_rugiada_interno_esterno_non_calcolabile") == NC:
        return NC
    if interno_testo == ND or esterno_testo == ND:
        return ND
    if interno_testo == NC or esterno_testo == NC:
        return NC
    interno = fl(interno_testo, None)
    esterno = fl(esterno_testo, None)
    if interno is None or esterno is None:
        return NC
    limite = fl(L.v("input_number.offset_verifica_impiego_vmc"), None)
    if limite is None:
        return NC
    delta = _delta_rugiada(interno, esterno)
    if delta < limite:
        confronto = "MINORE DEL"
    elif delta == limite:
        confronto = "UGUALE AL"
    else:
        confronto = "MAGGIORE DEL"
    return (
        f"Δ PUNTO DI RUGIADA RILEVATO {testo(rnd(delta, 2))} °C, "
        f"{confronto} VALORE IMPOSTATO ({testo(limite)} °C)."
    )


# --- umidita' assoluta ----------------------------------------------------------------------


def _umidita_assoluta(L: Lettore, lato: str) -> str:
    """Umidita' assoluta in g/m³ da umidita' relativa (%) e temperatura (°C)."""
    if L.v(_MEMORIZZATA) in _STATI_MEMORIZZATA:
        return ND
    h_testo = L.v(f"sensor.umidita_{lato}_status")
    t_testo = L.v(f"sensor.temp_{lato}_status")
    if h_testo == ND or t_testo == ND:
        return ND
    if h_testo == NC or t_testo == NC:
        return NC
    h = fl(h_testo, None)
    t = fl(t_testo, None)
    if h is None or t is None or h <= 0:
        return NC
    # come nel modello: e**x (non exp(x)), per avere lo stesso numero
    return testo(rnd((h * 6.112 * 2.1674 * math.e ** ((17.67 * t) / (t + 243.5))) / (t + 273.15), 2))


@_testo("sensor.umidita_assoluta_interna")
def umidita_assoluta_interna(L: Lettore) -> str:
    return _umidita_assoluta(L, "interna")


@_testo("sensor.umidita_assoluta_esterna")
def umidita_assoluta_esterna(L: Lettore) -> str:
    return _umidita_assoluta(L, "esterna")


# --- grafici e valori numerici: sensori con unita' di misura ---------------------------------


def _grafico(sorgente: str) -> None:
    """Registra il grafico di ``sorgente``: il suo valore come numero, disponibile solo se lo e'."""

    def disponibile(L: Lettore) -> bool:
        return is_number(L.v(sorgente))

    @_numerico(f"{sorgente}_grafico", disponibile=disponibile)
    def stato(L: Lettore) -> str:
        return L.v(sorgente)


for _sorgente in (
    "sensor.temp_esterna_status",
    "sensor.temp_interna_status",
    "sensor.umidita_esterna_status",
    "sensor.umidita_interna_status",
    "sensor.punto_di_rugiada_esterno",
    "sensor.punto_di_rugiada_interno",
    "sensor.punto_di_rugiada_valore",
    "sensor.umidita_assoluta_esterna",
    "sensor.umidita_assoluta_interna",
    "sensor.temp_esterna_status_senza_offset",
    "sensor.temp_interna_status_senza_offset",
    "sensor.umidita_interna_status_senza_offset",
):
    _grafico(_sorgente)


def _numerico_da(L: Lettore, chiave: str) -> str:
    """Il valore del sensore come numero; se non lo e', nessun valore (``None``)."""
    valore = fl(L.v(chiave), None)
    return testo(valore) if valore is not None else testo(None)


@_numerico("sensor.temp_interna_numeric")
def temp_interna_numeric(L: Lettore) -> str:
    return _numerico_da(L, "sensor.temp_interna_status")


@_numerico("sensor.hum_interna_numeric")
def hum_interna_numeric(L: Lettore) -> str:
    return _numerico_da(L, "sensor.umidita_interna_status")
