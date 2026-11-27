"""Valori in piu' per i modelli del Calendario (accensione e spegnimento nelle Fasce).

I sensori di stato del Calendario escono da «Disabilitata» solo quando, nel giorno di oggi,
accensione < spegnimento < accensione 2 < spegnimento 2 (confronti tra testi) e il
Calendario comanda la VMC. Con i soli 5 orari del banco (piu' unknown/unavailable) quattro
valori in ordine crescente capitano di rado: piu' orari diversi rendono il caso frequente.
Ci sono anche valori non orari, per provare ``[0:5]`` e gli spazi tolti alla fine:
un testo vuoto, uno con uno spazio al quinto carattere e uno piu' corto di 5 caratteri.
Nessuno ha due «:» con numeri non validi, perche' il banco sceglie l'ora vicino agli
orari con due «:».
"""

from __future__ import annotations

_GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")

_ORARI = {
    "01:15:00",
    "05:59:30",
    "06:30:30",
    "07:00:00",
    "08:20:00",
    "10:05:00",
    "12:00:30",
    "13:30:00",
    "15:45:00",
    "17:10:00",
    "19:00:00",
    "20:30:00",
    "22:15:00",
    "",
    "9:30 PM",
    "7:05",
}

EXTRA: dict[str, set[str]] = {
    f"input_datetime.vmc_master_{voce}_{giorno}{fascia}": _ORARI
    for voce in ("accensione", "spegnimento")
    for giorno in _GIORNI
    for fascia in ("", "_2")
}
