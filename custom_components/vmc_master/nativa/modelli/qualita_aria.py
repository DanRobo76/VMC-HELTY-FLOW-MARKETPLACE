"""Qualita' dell'aria: CO2, VOC, soglie di Congelamento, Delta Temp. e Umidita', comfort e muffa."""

from __future__ import annotations

from ..compat import fl, is_number, rnd, testo
from ..lettore import Lettore
from . import modello

# valori di «states()» che i modelli del package trattano come «non disponibile»
_NON_VALIDI = ("sconosciuto", "unknown", "", None, "unavailable", "Non disponibile")
# valori dell'entita' scelta (CO2 Int. Selezionata) per cui si usa la sonda della VMC
_SCELTA_NON_DISPONIBILE = ("unknown", "unavailable", "-100", "Non disponibile")


def _sensori_non_disponibili(L: Lettore) -> bool:
    """La VMC non ha mandato le letture delle sonde (``sensori_memorizzata``)."""
    return L.v("sensor.sensori_memorizzata") in _NON_VALIDI


# ---------------------------------------------------------------------------
# CO2 e VOC
# ---------------------------------------------------------------------------


@modello("sensor.co2_interna_selezionata")
def co2_interna_selezionata(L: Lettore) -> str:
    """CO2 dell'entita' scelta dall'utente: 0 per «-», -100 se non e' un numero.

    Il sensore ha un'unita' di misura: Home Assistant legge il testo come numero, che
    resta scritto uguale («600.0» per il valore letto, «0» e «-100» per gli altri casi).
    """
    entity_id = L.v("input_select.selected_co2_internal_entity")
    if entity_id and L.s(entity_id) not in _NON_VALIDI:
        if L.s(entity_id) == "-":
            return "0"
        # «| float» senza predefinito: is_number garantisce che la conversione riesca
        return testo(float(L.s(entity_id))) if is_number(L.s(entity_id)) else "-100"
    return "-100"


@modello("sensor.co2_status")
def co2_status(L: Lettore) -> str:
    """CO2 interna con l'Offset; senza entita' scelta disponibile, la sonda della VMC senza Offset."""
    co2_int = L.v("sensor.co2_interna_selezionata")
    if co2_int in _SCELTA_NON_DISPONIBILE:
        vmc = fl(L.v("sensor.co2_status_senza_offset"), None)
        if vmc is not None and vmc > 0:
            return testo(rnd(vmc, 0))
        if co2_int == "-100":
            return "-"
        return "Non disponibile"
    co2_float = fl(co2_int, 0)
    con_offset = rnd(co2_float + fl(L.v("input_number.offset_co2"), 0), 0)
    if con_offset == 0:
        return "-"
    if con_offset > 0:
        return testo(con_offset)
    if con_offset < 0:
        return "-"
    return "Non disponibile"


def _sonda_vmc(L: Lettore, indice: int, offset: str | None = None) -> str:
    """Valore di una sonda letto da ``sensori_memorizzata`` (campo ``indice``), con l'Offset se c'e'.

    L'Offset si somma sempre al valore letto: con la sonda assente (00000) e un Offset
    positivo si vede il valore dell'Offset.
    """
    dati = L.v("sensor.sensori_memorizzata")
    if dati in _NON_VALIDI:
        return "Non disponibile"
    componenti = dati.split(",")
    if len(componenti) > indice:
        valore = fl(componenti[indice], 0)
        if offset is not None:
            valore = valore + fl(L.v(offset), 0)
        if valore > 0:
            return testo(rnd(valore, 0))
        return "-"
    return "Non disponibile"


@modello("sensor.co2_status_senza_offset")
def co2_status_senza_offset(L: Lettore) -> str:
    return _sonda_vmc(L, 4)


@modello("sensor.voc_status")
def voc_status(L: Lettore) -> str:
    return _sonda_vmc(L, 11, "input_number.offset_voc")


@modello("sensor.voc_status_senza_offset")
def voc_status_senza_offset(L: Lettore) -> str:
    return _sonda_vmc(L, 11)


def _grafico(chiave: str) -> None:
    """Registra «<chiave>_grafico»: lo stesso valore, disponibile solo quando e' un numero.

    Il sensore ha un'unita' di misura, quindi Home Assistant legge il testo come numero:
    i sensori di partenza danno solo interi scritti senza zeri davanti, che restano uguali.
    """

    def disponibile(L: Lettore) -> bool:
        return is_number(L.v(chiave))

    def stato(L: Lettore) -> str:
        return L.v(chiave)

    modello(f"{chiave}_grafico", disponibile=disponibile)(stato)


for _chiave in (
    "sensor.co2_status",
    "sensor.voc_status",
    "sensor.co2_status_senza_offset",
    "sensor.voc_status_senza_offset",
):
    _grafico(_chiave)


def _livello_concentrazione(L: Lettore, chiave: str, fasce: tuple[tuple[float, bool, str], ...]) -> str:
    """Livello di concentrazione del valore di ``chiave``.

    ``fasce``: (limite alto, limite compreso, testo), in ordine; ogni fascia parte (esclusa)
    dal limite della precedente, la prima da 0. Oltre l'ultima: «Pessima Concentrazione».
    """
    grezzo = L.v(chiave)
    if _sensori_non_disponibili(L):
        return "Non disponibile"
    if grezzo == "-":
        return "-"
    valore = fl(grezzo, None)
    if valore is None:
        return "[Non Disponibile]"
    if valore <= 0:
        return "-"
    basso: float = 0
    for alto, compreso, etichetta in fasce:
        if valore > basso and (valore <= alto if compreso else valore < alto):
            return etichetta
        basso = alto
    return "Pessima Concentrazione"


_FASCE_CO2 = (
    (800, True, "Bassa Concentrazione"),
    (1000, True, "Moderata Concentrazione"),
    (1400, False, "Alta Concentrazione"),
)
_FASCE_VOC = (
    (300, True, "Bassa Concentrazione"),
    (600, True, "Moderata Concentrazione"),
)


@modello("sensor.co2_status_verifica_soglia")
def co2_status_verifica_soglia(L: Lettore) -> str:
    return _livello_concentrazione(L, "sensor.co2_status", _FASCE_CO2)


@modello("sensor.voc_status_verifica_soglia")
def voc_status_verifica_soglia(L: Lettore) -> str:
    return _livello_concentrazione(L, "sensor.voc_status", _FASCE_VOC)


# ---------------------------------------------------------------------------
# Umidita'
# ---------------------------------------------------------------------------


def _fascia_umidita(umidita: float, limite: float) -> int | None:
    """0 secchezza (1-35), 1 normale (35-limite), 2 muffe (limite-100), None fuori scala."""
    if umidita >= 1 and umidita <= 35:
        return 0
    if umidita > 35 and umidita < limite:
        return 1
    if umidita >= limite and umidita <= 100:
        return 2
    return None


def _limite_umidita(L: Lettore) -> float:
    """Soglia «Avvio VMC per Umidita' ≥» (65 se non e' un numero)."""
    return fl(L.v("input_number.umidita_avvio"), 65)


_MESSAGGI_UMIDITA = (
    "POSSIBILE SECCHEZZA, DISIDRATAZIONE. SI CONSIGLIA DI UMIDIFICARE L'AMBIENTE.",
    "SITUAZIONE NORMALE.",
    "POTREBBE VERIFICARSI UNA PROLIFERAZIONE DI MUFFE E BATTERI. SI CONSIGLIA DI DEUMIDIFICARE L'AMBIENTE.",
)
_STATI_UMIDITA = ("Possibile Secchezza, Disidratazione", "Normale", "Possibile Muffe, Batteri")


@modello("sensor.umidita_interna_status_verifica_soglia_valore")
def umidita_interna_status_verifica_soglia_valore(L: Lettore) -> str:
    umidita = L.v("sensor.umidita_interna_status")
    limite = _limite_umidita(L)
    if umidita in _NON_VALIDI:
        return "[Non Calcolabile]"
    valore = fl(umidita, None)
    if valore is None:
        return "[Non Calcolabile]"
    fascia = _fascia_umidita(valore, limite)
    if fascia is None:
        return "[Non Calcolabile]"
    return f"UMIDITÀ AL {testo(valore)}%. {_MESSAGGI_UMIDITA[fascia]}"


@modello("sensor.umidita_interna_status_verifica_soglia")
def umidita_interna_status_verifica_soglia(L: Lettore) -> str:
    if _sensori_non_disponibili(L):
        return "Non disponibile"
    umidita = L.v("sensor.umidita_interna_status")
    limite = _limite_umidita(L)
    if umidita in ("unknown", "unavailable", "[Non Calcolabile]"):
        return "[Non Calcolabile]"
    valore = fl(umidita, None)
    if valore is None:
        return "[Non Calcolabile]"
    fascia = _fascia_umidita(valore, limite)
    return "[Non Calcolabile]" if fascia is None else _STATI_UMIDITA[fascia]


# ---------------------------------------------------------------------------
# Congelamento e Delta Temp.
# ---------------------------------------------------------------------------


def _gelo(temperatura: float | None) -> bool:
    """Temperatura esterna di congelamento (≤ -18 °C)."""
    return temperatura is not None and temperatura <= -18


def _quasi_gelo(temperatura: float | None) -> bool:
    """Temperatura esterna vicina al congelamento (tra -18 esclusa e -15 compresa)."""
    return temperatura is not None and temperatura > -18 and temperatura <= -15


def _temperatura(L: Lettore, chiave: str) -> float | None:
    return fl(L.v(chiave), None)


@modello("sensor.congelamento_verifica_soglia")
def congelamento_verifica_soglia(L: Lettore) -> str:
    """Congelamento: con uno dei due sensori (con o senza Offset) mancante si usa l'altro."""
    if _sensori_non_disponibili(L):
        return "Non disponibile"
    esterna = _temperatura(L, "sensor.temp_esterna_status")
    esterna_vmc = _temperatura(L, "sensor.temp_esterna_status_senza_offset")
    if esterna is None and esterna_vmc is None:
        return "[Non Disponibile]"
    if _gelo(esterna) or _gelo(esterna_vmc):
        return "Si"
    if _quasi_gelo(esterna) or _quasi_gelo(esterna_vmc):
        return "[No ma Prossimo]"
    return "No"


def _differenza(interna: float | None, esterna: float | None) -> float | None:
    """Interna meno esterna arrotondata a un decimale; None se manca una delle due."""
    if interna is not None and esterna is not None:
        return rnd(interna - esterna, 1)
    return None


@modello("sensor.delta_temp_verifica_soglia")
def delta_temp_verifica_soglia(L: Lettore) -> str:
    """Delta Temp. > 23 °C: con una delle due coppie (con o senza Offset) mancante si usa l'altra."""
    if _sensori_non_disponibili(L):
        return "Non disponibile"
    esterna = _temperatura(L, "sensor.temp_esterna_status")
    interna = _temperatura(L, "sensor.temp_interna_status")
    esterna_vmc = _temperatura(L, "sensor.temp_esterna_status_senza_offset")
    interna_vmc = _temperatura(L, "sensor.temp_interna_status_senza_offset")
    delta = _differenza(interna, esterna)
    delta_vmc = _differenza(interna_vmc, esterna_vmc)
    if delta is None and delta_vmc is None:
        return "[Non Disponibile]"
    if _gelo(esterna) or _gelo(esterna_vmc):
        return "-"
    if (delta is not None and delta > 23) or (delta_vmc is not None and delta_vmc > 23):
        return "Si"
    if (delta is not None and delta >= 20 and delta <= 23) or (
        delta_vmc is not None and delta_vmc >= 20 and delta_vmc <= 23
    ):
        return "[No ma Prossimo]"
    return "No"


# ---------------------------------------------------------------------------
# Indice di Benessere (dal Punto di Rugiada)
# ---------------------------------------------------------------------------

_LINEETTA = "\u2013"  # trattino medio (en dash), come nel package
_BENESSERE = (
    (29, _LINEETTA),
    (25, "Molto fastidioso, Liv. 2"),
    (22, "Molto fastidioso, Liv. 1"),
    (19, "Fastidioso"),
    (16, "Accettabile"),
    (13, "Confortevole, Liv. 2"),
    (10, "Confortevole, Liv. 1"),
    (7, "Secco"),
)


@modello("sensor.calcolo_confort_interno")
def calcolo_confort_interno(L: Lettore) -> str:
    """Indice di Benessere: il Punto di Rugiada non numerico passa com'e' («[...]», non disponibile)."""
    if _sensori_non_disponibili(L):
        return "Non disponibile"
    punto_rugiada = L.v("sensor.punto_di_rugiada_interno").strip()
    if punto_rugiada in _NON_VALIDI or punto_rugiada.startswith("["):
        return punto_rugiada
    valore = fl(punto_rugiada, None)
    if valore is None:
        return "[Non Calcolabile]"
    for soglia, etichetta in _BENESSERE:
        if valore >= soglia:
            return etichetta
    return _LINEETTA


# ---------------------------------------------------------------------------
# Rischio Muffa (medie di 4, 8 e 12 settimane) e Andamento
# ---------------------------------------------------------------------------

_E = 2.718281828459045
_MUFFA_ESTREME = "Rischio assente (condizioni estreme)"
# nei testi dei livelli il package usa spazi stretti non separabili (U+202F) e il
# trattino medio (U+2013): si scrivono come codici per non confonderli con gli spazi
_MUFFA_LIVELLI = (
    "Liv.\u202f0: nessuna crescita di muffa",
    "Liv.\u202f1: crescita possibile in\u202f>\u202f8\u202fSettimane",
    "Liv.\u202f2: crescita possibile in\u202f4\u20138\u202fSettimane",
    "Liv.\u202f3: crescita possibile in\u202f<\u202f4\u202fSettimane",
)


def _mediana(minimo: float, valore: float, massimo: float) -> float:
    """``([minimo, valore, massimo] | sort)[1]``: il valore tenuto tra minimo e massimo."""
    return sorted([minimo, valore, massimo])[1]


def _rischio_muffa(L: Lettore, settimane: int) -> str:
    """Rischio Muffa dalle medie di temperatura e umidita' interne delle ultime ``settimane``."""
    temp = fl(L.v(f"sensor.temp_interna_media_{settimane}w"), None)
    hum = fl(L.v(f"sensor.hum_interna_media_{settimane}w"), None)
    if temp is None or hum is None:
        return "[Non Calcolabile]"
    # le curve si calcolano prima del controllo sulla temperatura, come nel package
    c1 = _mediana(72, (20 * (_E ** (-0.15 * temp)) + 73), 100)
    c2 = _mediana(79, (17 * (_E ** (-0.11 * temp)) + 80), 100)
    c3 = _mediana(84, (15 * (_E ** (-0.10 * temp)) + 85), 100)
    if temp < 0 or temp > 50:
        return _MUFFA_ESTREME
    if hum <= c1:
        return _MUFFA_LIVELLI[0]
    if hum <= c2:
        return _MUFFA_LIVELLI[1]
    if hum <= c3:
        return _MUFFA_LIVELLI[2]
    return _MUFFA_LIVELLI[3]


@modello("sensor.calcolo_rischio_muffa_4w")
def calcolo_rischio_muffa_4w(L: Lettore) -> str:
    return _rischio_muffa(L, 4)


@modello("sensor.calcolo_rischio_muffa_8w")
def calcolo_rischio_muffa_8w(L: Lettore) -> str:
    return _rischio_muffa(L, 8)


@modello("sensor.calcolo_rischio_muffa_12w")
def calcolo_rischio_muffa_12w(L: Lettore) -> str:
    return _rischio_muffa(L, 12)


# livello numerico di ogni testo del Rischio Muffa
_LIVELLO_MUFFA = {_MUFFA_ESTREME: 0, **{testo_: n for n, testo_ in enumerate(_MUFFA_LIVELLI)}}

_STABILE = "Stabile a Liv. {}"
_OSCILLAZIONE = "Stabile a Liv. {} con Oscillazione"
_PEGGIORAMENTO = "Peggioramento - Rischio Aumentato a Liv. {}"
_MIGLIORAMENTO = "Miglioramento - Rischio Diminuito a Liv. {}"


@modello("sensor.trend_muffa")
def trend_muffa(L: Lettore) -> str:
    s12 = _LIVELLO_MUFFA.get(L.v("sensor.calcolo_rischio_muffa_12w"))
    s8 = _LIVELLO_MUFFA.get(L.v("sensor.calcolo_rischio_muffa_8w"))
    s4 = _LIVELLO_MUFFA.get(L.v("sensor.calcolo_rischio_muffa_4w"))
    if s12 is None or s8 is None or s4 is None:
        return "[Non Calcolabile]"
    if s4 == s12 and s4 != s8:
        return _OSCILLAZIONE.format(s4)
    if s4 > s8:
        return _PEGGIORAMENTO.format(s4)
    if s4 < s8:
        return _MIGLIORAMENTO.format(s4)
    return _STABILE.format(s4)


# livello di ogni testo dell'Andamento, come la tabella del package (che non ha
# «Peggioramento ... Liv. 0» ne' «Miglioramento ... Liv. 3», impossibili)
_LIVELLO_TREND = {
    **{_STABILE.format(n): n for n in range(4)},
    **{_OSCILLAZIONE.format(n): n for n in range(4)},
    **{_PEGGIORAMENTO.format(n): n for n in range(1, 4)},
    **{_MIGLIORAMENTO.format(n): n for n in range(3)},
}


@modello("sensor.trend_muffa_level")
def trend_muffa_level(L: Lettore) -> str:
    txt = L.v("sensor.trend_muffa")
    if txt in (*_NON_VALIDI, "[Non Calcolabile]"):
        return "[Non Calcolabile]"
    return testo(_LIVELLO_TREND.get(txt, "[Non Calcolabile]"))


@modello("sensor.trend_muffa_level_numeric")
def trend_muffa_level_numeric(L: Lettore) -> str:
    """Livello come numero decimale.

    Il package scrive «None» quando il livello non e' un numero: il sensore ha
    ``state_class`` e Home Assistant mostra allora «unknown».
    """
    valore = fl(L.v("sensor.trend_muffa_level"), None)
    return testo(valore) if valore is not None else "unknown"
