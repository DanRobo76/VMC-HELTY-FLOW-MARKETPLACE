"""I 10 sensori con memoria del Package, calcolati in Python.

Nel Package sono sensori template «a trigger», che ricordano un valore tra un
evento e l'altro:

- le tre letture memorizzate (stato ventola, sensori, nome): l'ultima lettura
  valida della VMC, che resta anche quando la VMC non risponde;
- le medie di temperatura e umidità interne delle ultime 4, 8 e 12 settimane e i
  giorni di dati disponibili, calcolati all'avvio e ogni ora al minuto 5 dalle
  statistiche orarie a lungo termine di Home Assistant.

Qui ci sono i calcoli, uguali ai template; quando e come si ripetono lo decidono
le entità native (avvio, cambio della lettura, minuto 5 di ogni ora).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta
from typing import Any

from .compat import rnd
from .risultato import interpreta, scrivi

# Valori che il template considera «nessuna lettura» per la lettura attuale e per quella ricordata.
_NON_VALIDI_ORA = ("unknown", "unavailable", "")
_NON_VALIDI_MEMORIA = ("unknown", "unavailable", "", "None")
_INTERRUZIONE = ("unavailable", "unknown", "")

TRIGGER_STATO = "state"
TRIGGER_AVVIO = "homeassistant"

# Statistiche lette e giorni delle tre medie.
STATISTICA_TEMPERATURA = "temp_interna_numeric"
STATISTICA_UMIDITA = "hum_interna_numeric"
GIORNI_STATISTICHE = 84
MEDIE: tuple[tuple[str, str, int], ...] = (
    ("sensor.temp_interna_media_4w", STATISTICA_TEMPERATURA, 28),
    ("sensor.hum_interna_media_4w", STATISTICA_UMIDITA, 28),
    ("sensor.temp_interna_media_8w", STATISTICA_TEMPERATURA, 56),
    ("sensor.hum_interna_media_8w", STATISTICA_UMIDITA, 56),
    ("sensor.temp_interna_media_12w", STATISTICA_TEMPERATURA, 84),
    ("sensor.hum_interna_media_12w", STATISTICA_UMIDITA, 84),
)
GIORNI_DATI = "sensor.rischio_muffa_giorni_dati"
# I 10 sensori nell'ordine del Package (i blocchi a trigger e i sensori di ogni blocco):
# l'ordine in cui oggi scrivono quando scattano insieme (avvio).
IN_ORDINE: tuple[str, ...] = (
    "sensor.status_ventola_memorizzata",
    "sensor.sensori_memorizzata",
    "sensor.nome_memorizzata",
    *(chiave for chiave, _, _ in MEDIE),
    GIORNI_DATI,
)


def come_stato(testo: str) -> str | None:
    """Lo stato che Home Assistant mostra per il testo prodotto da un template di sensore.

    Regole comuni in risultato.py; qui «nessun valore» resta None (stato «unknown»).
    """
    valore = interpreta(testo)
    return None if valore is None else scrivi(valore)


def memorizzata(piattaforma: str, nuova: str | None, ora: str, ricordata: str) -> str:
    """Ultima lettura valida (template di status_ventola/sensori/nome_memorizzata).

    ``piattaforma``: TRIGGER_STATO quando la lettura cambia verso un valore che non
    è unknown/unavailable (``nuova`` è il nuovo valore), TRIGGER_AVVIO all'avvio di
    Home Assistant. ``ora`` è la lettura attuale, ``ricordata`` lo stato del sensore
    memorizzato prima di questo calcolo. Il risultato è già senza spazi in testa e
    in coda, come ogni risultato di template.
    """
    if piattaforma == TRIGGER_STATO:
        valore = nuova
    elif ora in _NON_VALIDI_ORA and ricordata not in _NON_VALIDI_MEMORIA:
        valore = ricordata
    else:
        valore = ora
    return str(valore).strip()


def lettura_prima_dell_interruzione(
    piattaforma: str,
    da: str | None,
    ricordata: str,
    cambiata: datetime | None,
) -> str:
    """Attributo «lettura_prima_dell_interruzione» di status_ventola_memorizzata.

    Dopo un'interruzione (avvio, oppure lettura che torna da unavailable/unknown/«»)
    vale «codice|ora»: il codice della lettura ricordata e l'ora (timestamp con un
    decimale) in cui era iniziata; altrimenti «». ``da`` è lo stato precedente della
    lettura (None se non c'era), ``cambiata`` il last_changed del sensore memorizzato.
    """
    prima = str(ricordata).split(",")
    interruzione = piattaforma != TRIGGER_STATO or da is None or da in _INTERRUZIONE
    if interruzione and len(prima) > 1:
        istante = cambiata.timestamp() if cambiata is not None else 0
        return f"{prima[1]}|{rnd(istante, 1)}"
    return ""


def righe_statistiche(risultato: Any, statistica: str) -> list[Mapping[str, Any]]:
    """Le righe di una statistica dalla risposta di recorder.get_statistics (o [])."""
    if not isinstance(risultato, Mapping):
        return []
    statistiche = risultato.get("statistics")
    if not isinstance(statistiche, Mapping):
        return []
    righe = statistiche.get(statistica, [])
    return list(righe) if isinstance(righe, Iterable) else []


def media(
    righe: Iterable[Mapping[str, Any]], adesso: datetime, giorni: int
) -> float | None:
    """Media delle medie orarie degli ultimi ``giorni`` (due decimali), o None senza dati.

    Come il template: confronta l'inizio di ogni ora come testo ISO in UTC con
    l'istante di ``giorni`` fa (secondi interi) e salta le ore senza media.
    """
    inizio = (adesso - timedelta(days=giorni)).replace(microsecond=0).isoformat()
    valori = [
        riga["mean"] for riga in righe if riga["start"] >= inizio and "mean" in riga
    ]
    if not valori:
        return None
    return rnd(sum(valori) / len(valori), 2)


def giorni_di_dati(righe: list[Mapping[str, Any]], adesso: datetime) -> float | int:
    """Giorni dalla prima ora con statistiche, da 0 a 84 (un decimale)."""
    if not righe:
        return 0
    primo = datetime.fromisoformat(righe[0]["start"])
    return min(rnd((adesso - primo).total_seconds() / 86400, 1), GIORNI_STATISTICHE)


def calcola_medie(
    risultato: Any, adesso: datetime, nome: str
) -> dict[str, float | int | None]:
    """I 7 valori (6 medie e giorni di dati) dalla risposta di recorder.get_statistics.

    ``risultato`` è None se la lettura delle statistiche non è riuscita; ``adesso`` è
    l'ora in UTC; ``nome`` il nome della VMC (le statistiche sono di sensor.vmc_<nome>_...).
    """
    uscita: dict[str, float | int | None] = {}
    righe = {
        statistica: righe_statistiche(risultato, f"sensor.vmc_{nome}_{statistica}")
        for statistica in (STATISTICA_TEMPERATURA, STATISTICA_UMIDITA)
    }
    for chiave, statistica, giorni in MEDIE:
        uscita[chiave] = media(righe[statistica], adesso, giorni)
    uscita[GIORNI_DATI] = giorni_di_dati(righe[STATISTICA_UMIDITA], adesso)
    return uscita
