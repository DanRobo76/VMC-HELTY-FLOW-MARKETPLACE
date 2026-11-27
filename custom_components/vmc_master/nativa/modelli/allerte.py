"""Allerte: Black-Out rilevato e sensori di monitoraggio delle allerte."""

from __future__ import annotations

from ..compat import fl, it
from ..lettore import Lettore
from . import modello

# letture non valide (la lista ``stati`` / ``invalidi`` dei modelli del package)
_NON_VALIDI = ("sconosciuto", "unknown", "", None, "unavailable", "Non disponibile")


def _memorizzata_non_valida(L: Lettore) -> bool:
    """``states('sensor.vmc_x_sensori_memorizzata') in stati``: letture dei sensori assenti."""
    return L.v("sensor.sensori_memorizzata") in _NON_VALIDI


def _allerta(L: Lettore, chiave: str, valori: tuple[str, ...]) -> str:
    """Schema comune dei monitoraggi: «Allerta» se la verifica della soglia e' in ``valori``."""
    if _memorizzata_non_valida(L):
        return "Non disponibile"
    return "Allerta" if L.v(chiave) in valori else "Nessuna Allerta"


# ---------------------------------------------------------------------------------------
# Black-Out rilevato
# ---------------------------------------------------------------------------------------

# spie dei tasti di velocita' (input_boolean.vmc_x_spia_velocita_<nome>)
_SPIE_VELOCITA = ("0", "1", "2", "3", "4", "notturna", "freecooling", "iperventilazione")
_GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")
_SPIE_CALENDARIO = tuple(f"spia_calendario_{g}_{n}" for g in _GIORNI for n in (1, 2))
# spie che i casi «Velocità 1» controllano in piu'
_CO2_O_VOC = "spia_co2_o_voc"
_PARTENZA_RITORNO_0 = "spia_co2_o_voc_partenza_ritorno_velocita_0"
_VEL_1_CO2_O_VOC_PDR = "spia_velocita_1_co2_o_voc_pdr"
_VEL_1_CO2_O_VOC = "spia_velocita_1_co2_o_voc"
_UN_SOLO_AVVIO_FC = "spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling"
_UN_SOLO_AVVIO_FH = "spia_velocita_freecooling_un_solo_avvio_per_programmazione_freeheating"


def _spia(L: Lettore, nome: str) -> str:
    return L.v(f"input_boolean.{nome}")


def _base_black_out(L: Lettore, codice: str, spia_del_codice: str) -> bool:
    """Parte comune di ogni condizione: VMC OFF-Line con ``codice`` come ultima velocita'
    letta, spie di velocita' ``off`` (tranne quella del codice) e spie del Calendario ``off``."""
    return (
        L.v("sensor.status_ip_interfaccia") == "OFF-Line"
        and L.v("sensor.status_ventola_lettura_codice_interpretato") == codice
        and all(_spia(L, f"spia_velocita_{s}") == "off" for s in _SPIE_VELOCITA if s != spia_del_codice)
        and all(_spia(L, s) == "off" for s in _SPIE_CALENDARIO)
    )


def condizioni_black_out(L: Lettore) -> dict[str, bool]:
    """Le undici condizioni del modello (t1…t11), messe in OR: una per «Trigger»."""

    def spento(nome: str) -> bool:
        return _spia(L, nome) == "off"

    def acceso(nome: str) -> bool:
        return _spia(L, nome) == "on"

    def v1() -> bool:
        return _base_black_out(L, "Velocità 1", "1")

    return {
        # «Black-Out a Velocità 0»
        "t1": _base_black_out(L, "Velocità 0", "0"),
        # «Black-Out a Velocità 1»
        "t2": v1()
        and spento(_CO2_O_VOC)
        and spento(_PARTENZA_RITORNO_0)
        and spento(_VEL_1_CO2_O_VOC_PDR)
        and spento(_VEL_1_CO2_O_VOC)
        and spento(_UN_SOLO_AVVIO_FC)
        and spento(_UN_SOLO_AVVIO_FH),
        # «Black-Out a Velocità 1 caso [SPIE INQUINANTI ON] e [SPIE FREECOOLING OFF e FREEHEAING OFF]»
        "t3": v1() and acceso(_CO2_O_VOC) and spento(_UN_SOLO_AVVIO_FC) and spento(_UN_SOLO_AVVIO_FH),
        # «Black-Out a Velocità 1 caso [SPIE INQUINANTI ON] e [SPIE FREECOOLING ON o FREEHEAING ON]»
        "t4": v1() and acceso(_CO2_O_VOC) and (acceso(_UN_SOLO_AVVIO_FC) or acceso(_UN_SOLO_AVVIO_FH)),
        # «Black-Out a Velocità 2», «… 3», «… 4», «Notturna», «Iperventilazione»
        "t5": _base_black_out(L, "Velocità 2", "2"),
        "t6": _base_black_out(L, "Velocità 3", "3"),
        "t7": _base_black_out(L, "Velocità 4", "4"),
        "t8": _base_black_out(L, "Notturna", "notturna"),
        "t9": _base_black_out(L, "Iperventilazione", "iperventilazione"),
        # «Black-Out Free Cool./Heat.»
        "t10": _base_black_out(L, "Free Cooling", "freecooling"),
        # «Black-Out a Velocità 1 caso [SPIE INQUINANTI OFF] e
        #  [SPIE FREECOOLING ON o FREEHEATING ON o MEMORIE INQUINANTI ON]»
        "t11": v1()
        and spento(_CO2_O_VOC)
        and (
            acceso(_UN_SOLO_AVVIO_FC)
            or acceso(_UN_SOLO_AVVIO_FH)
            or acceso(_PARTENZA_RITORNO_0)
            or acceso(_VEL_1_CO2_O_VOC_PDR)
            or acceso(_VEL_1_CO2_O_VOC)
        ),
    }


def _icona_black_out_rilevato(L: Lettore) -> str:
    return "mdi:power-plug-off" if L.is_v("binary_sensor.black_out_rilevato", "on") else "mdi:power-plug"


def _ritardo_black_out_rilevato(L: Lettore) -> int:
    """``delay_on``: secondi di attesa prima di dare il Black-Out per rilevato."""
    return it(L.v("input_number.attesa_blackout_rilevazione"), 32)


@modello("binary_sensor.black_out_rilevato", icona=_icona_black_out_rilevato, ritardo_on=_ritardo_black_out_rilevato)
def black_out_rilevato(L: Lettore) -> str:
    """Condizione prima del ritardo: ``{{ t1 or … or t11 }}``."""
    return "on" if any(condizioni_black_out(L).values()) else "off"


# ---------------------------------------------------------------------------------------
# Allerte
# ---------------------------------------------------------------------------------------


@modello("sensor.alert_avvio_interfaccia")
def alert_avvio_interfaccia(L: Lettore) -> str:
    """Allerta mostrata sui tasti di velocita' dell'interfaccia.

    Alert = PdR sfavorevole (interruttore PdR ON) o Congelamento; Alert Δ Temp. = Diff. Temp.
    > 23 °C; Alert Free = mese Free programmato in condizioni sfavorevoli; Nessuna altrimenti.
    """
    vel = L.v("sensor.status_ventola_lettura_codice_interpretato_interfaccia")
    if L.v("sensor.status_ip_interfaccia") != "ON-Line" or vel in _NON_VALIDI:
        return "Nessuna"
    congelamento = L.is_v("input_boolean.congelamento_verifica_soglia_valore_spia", "on") or L.is_v(
        "sensor.congelamento_verifica_soglia", "Si"
    )
    delta = L.is_v("input_boolean.delta_temp_verifica_soglia_valore_spia", "on") or L.is_v(
        "sensor.delta_temp_verifica_soglia", "Si"
    )
    pdr = (
        L.is_v("input_boolean.opzioni_accendi_spegni_vmc_vs_pdr", "on")
        and L.v("sensor.punto_di_rugiada_verifica_confronto") == "Se ne sconsiglia l'impiego"
    )
    free = L.v("sensor.alert_monitoraggio_free_heating_o_free_cooling_allert_interfaccia_avvisi")
    free_alert = free.startswith("Allerta Free") or free.startswith("Non Avviare in Velocità Free")
    if pdr or congelamento:
        return "Alert"
    if delta:
        return "Alert Δ Temp."
    if free_alert:
        return "Alert Free"
    return "Nessuna"


@modello("sensor.alert_monitoraggio_black_out")
def alert_monitoraggio_black_out(L: Lettore) -> str:
    if _memorizzata_non_valida(L):
        return "Non disponibile"
    rilevato = L.v("sensor.status_ip_interfaccia") == "OFF-Line" or any(
        L.is_v(f"input_boolean.spia_velocita_{s}", "on") for s in _SPIE_VELOCITA
    )
    return "Rilevato" if rilevato else "Non Rilevato"


@modello("sensor.alert_monitoraggio_co2")
def alert_monitoraggio_co2(L: Lettore) -> str:
    return _allerta(
        L,
        "sensor.co2_status_verifica_soglia",
        ("Moderata Concentrazione", "Alta Concentrazione", "Pessima Concentrazione"),
    )


@modello("sensor.alert_monitoraggio_congelamento")
def alert_monitoraggio_congelamento(L: Lettore) -> str:
    return _allerta(L, "sensor.congelamento_verifica_soglia", ("Si",))


@modello("sensor.alert_monitoraggio_delta")
def alert_monitoraggio_delta(L: Lettore) -> str:
    return _allerta(L, "sensor.delta_temp_verifica_soglia", ("Si",))


@modello("sensor.alert_monitoraggio_umidita")
def alert_monitoraggio_umidita(L: Lettore) -> str:
    return _allerta(
        L,
        "sensor.umidita_interna_status_verifica_soglia",
        ("Possibile Secchezza, Disidratazione", "Possibile Muffe, Batteri"),
    )


@modello("sensor.alert_monitoraggio_voc")
def alert_monitoraggio_voc(L: Lettore) -> str:
    return _allerta(L, "sensor.voc_status_verifica_soglia", ("Moderata Concentrazione", "Pessima Concentrazione"))


# offset dei sensori (input_number.vmc_x_offset_<nome>)
_OFFSET = ("temp_interna", "temp_esterna", "umidita_interna", "umidita_esterna", "co2", "voc")


@modello("sensor.alert_monitoraggio_offset_tutti_min")
def alert_monitoraggio_offset_tutti_min(L: Lettore) -> str:
    """«NOT OK» se tutti gli offset sono al loro minimo (attributo ``min``, -50 se manca)."""
    if _memorizzata_non_valida(L):
        return "Non disponibile"
    tutti_al_minimo = all(
        fl(L.v(f"input_number.offset_{n}"), 0) == fl(L.attr_v(f"input_number.offset_{n}", "min"), -50)
        for n in _OFFSET
    )
    return "NOT OK" if tutti_al_minimo else "OK"


@modello("sensor.alert_monitoraggio_pdr")
def alert_monitoraggio_pdr(L: Lettore) -> str:
    pdr = L.v("sensor.punto_di_rugiada_verifica_confronto")
    if _memorizzata_non_valida(L):
        return "Non disponibile"
    if pdr == "Se ne sconsiglia l'impiego":
        return "Allerta"
    if pdr in ("[Non Calcolabile]", "[Non Disponibile]"):
        return pdr
    return "Nessuna Allerta"


@modello("sensor.alert_monitoraggio_totale")
def alert_monitoraggio_totale(L: Lettore) -> str:
    if _memorizzata_non_valida(L):
        return "Non disponibile"
    allerta = (
        L.v("sensor.alert_monitoraggio_black_out") == "Rilevato"
        or L.v("sensor.alert_monitoraggio_umidita") == "Allerta"
        or L.v("sensor.umidita_interna_status") == "[Non Calcolabile]"
        or L.v("sensor.umidita_esterna_status") == "[Non Calcolabile]"
        or L.v("sensor.alert_monitoraggio_co2") == "Allerta"
        or L.v("sensor.alert_monitoraggio_voc") == "Allerta"
        or L.v("sensor.alert_monitoraggio_pdr") == "Allerta"
        or L.v("sensor.alert_monitoraggio_congelamento") == "Allerta"
        or L.v("sensor.congelamento_verifica_soglia") == "[No ma Prossimo]"
        or L.v("sensor.alert_monitoraggio_delta") == "Allerta"
        or L.v("sensor.delta_temp_verifica_soglia") == "[No ma Prossimo]"
        or L.v("sensor.alert_monitoraggio_free_heating_o_free_cooling_disabilitato") == "OK"
        or L.v("sensor.alert_monitoraggio_offset_tutti_min") == "NOT OK"
    )
    return "Allerta" if allerta else "Nessuna Allerta"


@modello("sensor.spia_pannello_alert_monitoraggio_totale")
def spia_pannello_alert_monitoraggio_totale(L: Lettore) -> str:
    if _memorizzata_non_valida(L):
        return "Non disponibile"
    monitoraggio = L.v("sensor.alert_monitoraggio_totale")
    spia_avvisi = L.v("input_boolean.opzioni_accendi_spegni_avvisi")
    if monitoraggio == "Nessuna Allerta":
        return "Non Presenti"
    if monitoraggio == "Allerta" and spia_avvisi == "on":
        return "Presenti"
    if monitoraggio == "Allerta" and spia_avvisi == "off":
        return "Presenti ma Disabilitati"
    return ""
