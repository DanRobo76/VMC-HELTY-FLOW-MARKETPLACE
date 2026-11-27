"""Mappa dei nomi della fase 4: dagli aiutanti del package alle entità native.

Il traduttore la riceve come parametro facoltativo (``traduci.traduzione(...,
rinomina=...)``): senza, il codice generato resta quello di sempre. Con la mappa, ogni
testo costante che il traduttore scrive nel codice (modelli, trigger, condizioni,
bersagli e dati dei servizi) passa da ``Rinomina.testo`` e ogni nome di servizio costante
da ``Rinomina.servizio``.

Tre casi per un nome ``dominio.oggetto`` dentro un testo:

- è un'entità della mappa: prende il nome di domani;
- è l'inizio di più entità della mappa (un nome che il package compone a pezzi, come
  ``'input_boolean.vmc_master_spia_' ~ velocita``): cambia solo il dominio, e solo se
  tutte le entità che cominciano così vanno nello stesso dominio e tengono il loro
  oggetto; altrimenti la traduzione si ferma (``NomeAmbiguo``): quel nome va deciso
  mentre il motore gira, non quando si traduce;
- non è nella mappa: resta com'è.

Un'entità intera è sempre presa per sé stessa, anche se è l'inizio di un'altra
(``..._avvisi`` e ``..._avvisi_spia``): i nomi composti del package partono tutti da un
pezzo che non è un'entità (``inventario_aiutanti_dinamici.csv``).
"""

from __future__ import annotations

import csv
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

FASE_1 = Path(__file__).with_name("aiutanti_fase1.csv")

# Un nome «dominio.oggetto» (anche solo l'inizio dell'oggetto) dentro un testo.
_NOME = re.compile(r"(?<![A-Za-z0-9_.])([a-z_]+)\.([a-z0-9_]*)")


class NomeAmbiguo(Exception):
    """Un pezzo di nome che comincia entità con destini diversi."""


@dataclass
class Rinomina:
    """Entità di oggi -> entità di domani, servizio di oggi -> servizio di domani."""

    entita: Mapping[str, str]
    servizi: Mapping[str, str] = field(default_factory=dict)
    # i pezzi di nome cambiati durante la traduzione (di oggi -> di domani)
    frammenti: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._domini = {nome.split(".", 1)[0] for nome in self.entita}

    def servizio(self, nome: str) -> str:
        """Il servizio di domani (lo stesso, se la mappa non lo cambia)."""
        return self.servizi.get(nome, nome)

    def testo(self, valore: str) -> str:
        """``valore`` con ogni nome della mappa cambiato."""
        return _NOME.sub(self._nome, valore)

    def _nome(self, trovato: re.Match[str]) -> str:
        nome, dominio, oggetto = trovato.group(0, 1, 2)
        if dominio not in self._domini or nome in self.servizi:
            return nome
        if nome in self.entita:
            return self.entita[nome]
        domani = set()
        for vecchia, nuova in self.entita.items():
            if not vecchia.startswith(nome):
                continue
            dominio_nuovo, oggetto_nuovo = nuova.split(".", 1)
            if oggetto_nuovo != vecchia.split(".", 1)[1]:
                raise NomeAmbiguo(f"{nome!r}: {vecchia} cambia oggetto ({nuova})")
            domani.add(dominio_nuovo)
        if not domani:
            return nome
        if len(domani) > 1:
            raise NomeAmbiguo(f"{nome!r} comincia entità di {sorted(domani)}")
        nuovo = f"{domani.pop()}.{oggetto}"
        self.frammenti[nome] = nuovo
        return nuovo

    def indietro(self, valore: str) -> str:
        """``valore`` con i nomi di oggi al posto di quelli di domani: per confrontare
        due registri, o il codice tradotto con e senza la mappa."""
        entita = {nuova: vecchia for vecchia, nuova in self.entita.items()}
        frammenti = {nuovo: vecchio for vecchio, nuovo in self.frammenti.items()}
        servizi = {nuovo: vecchio for vecchio, nuovo in self.servizi.items()}

        def nome(trovato: re.Match[str]) -> str:
            testo = trovato.group(0)
            for mappa in (entita, servizi, frammenti):
                if testo in mappa:
                    return mappa[testo]
            return testo

        return _NOME.sub(nome, valore)


def da_fase_1(
    tipi: Iterable[str],
    servizi: Mapping[str, str],
    interna: str | None = None,
) -> Rinomina:
    """La mappa per i ``tipi`` di aiutante dalla colonna «Domani» della fase 1.

    Un aiutante «interno» (che domani non è un'entità mostrata) va nel dominio
    ``interna`` con lo stesso oggetto; senza ``interna`` resta fuori dalla mappa.
    """
    voluti = set(tipi)
    entita: dict[str, str] = {}
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        for riga in csv.DictReader(flusso, delimiter=";"):
            if riga["Tipo oggi"] not in voluti:
                continue
            oggi, domani = riga["Entità oggi"], riga["Domani"]
            if domani.startswith("interna"):
                if interna is None:
                    continue
                domani = f"{interna}.{oggi.split('.', 1)[1]}"
            entita[oggi] = domani
    return Rinomina(entita, dict(servizi))
