"""Sensori calcolati della VMC: i modelli (template) del package portati in Python.

Ogni modello si registra con ``@modello("sensor.x")``: la chiave e' l'entity_id del package
senza ``vmc_<nome>_``. La funzione riceve un ``Lettore`` e restituisce lo stato come lo
mostrava Home Assistant (testo; ``on``/``off`` per i sensori binari).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from ..lettore import Lettore
from ..risultato import interpreta, uguali

Funzione = Callable[[Lettore], str]


@dataclass(frozen=True)
class Modello:
    chiave: str
    stato: Funzione
    icona: Funzione | None = None
    disponibile: Callable[[Lettore], bool] | None = None
    attributi: dict[str, Funzione] = field(default_factory=dict)
    # sensore binario con «delay_on»: secondi per cui la condizione deve restare vera
    ritardo_on: Callable[[Lettore], int] | None = None


MODELLI: dict[str, Modello] = {}
# chiavi dei modelli che ricordano da soli il loro ultimo risultato (L.memoria)
MEMORIA_PROPRIA: set[str] = set()


class _StatoErrore(str):
    """Stato di un modello andato in errore: vale «unavailable», ma si riconosce (``is``)."""


_ERRORE_STATO = _StatoErrore("unavailable")


def modello(
    chiave: str,
    *,
    icona: Funzione | None = None,
    disponibile: Callable[[Lettore], bool] | None = None,
    ritardo_on: Callable[[Lettore], int] | None = None,
) -> Callable[[Funzione], Funzione]:
    def registra(funzione: Funzione) -> Funzione:
        if chiave in MODELLI:
            raise ValueError(f"modello registrato due volte: {chiave}")
        MODELLI[chiave] = Modello(chiave, funzione, icona, disponibile, ritardo_on=ritardo_on)
        return funzione

    return registra


class Calcolo:
    """Stati dei modelli calcolati al bisogno, una volta per giro, nell'ordine delle dipendenze."""

    def __init__(self, ingressi: Callable[[str], str | None]) -> None:
        self._ingressi = ingressi
        self._fatti: dict[str, str] = {}
        self._in_corso: set[str] = set()
        self.lettore: Lettore | None = None

    def valore(self, chiave: str) -> str | None:
        m = MODELLI.get(chiave)
        if m is None or m.ritardo_on is not None:
            # i sensori con «delay_on» si leggono come sono: il ritardo lo tiene l'entita'
            return self._ingressi(chiave)
        if chiave not in self._fatti:
            if chiave in self._in_corso:
                raise RuntimeError(f"dipendenza circolare: {chiave}")
            self._in_corso.add(chiave)
            try:
                if not self._disponibile(m):
                    # non reso: l'ultimo risultato ricordato resta quello di quando era disponibile
                    self._fatti[chiave] = "unavailable"
                else:
                    self._fatti[chiave] = self._ricorda(chiave, self._stato(m))
            finally:
                self._in_corso.discard(chiave)
        return self._fatti[chiave]

    def _ricorda(self, chiave: str, nuovo: str) -> str:
        """Come Home Assistant: lo stato cambia solo se il risultato e' diverso (``!=``).

        Dopo ``100.0`` un risultato ``100`` lascia scritto ``100.0``. I modelli che ricordano
        da soli il loro risultato (MEMORIA_PROPRIA) restituiscono gia' lo stato giusto.
        """
        if chiave in MEMORIA_PROPRIA:
            return nuovo
        assert self.lettore is not None
        memoria = self.lettore.memoria
        if nuovo is _ERRORE_STATO:
            memoria.pop(chiave, None)  # un errore e' diverso da ogni risultato
            return "unavailable"
        precedente = memoria.get(chiave)
        if precedente is not None and precedente != nuovo and uguali(interpreta(precedente), interpreta(nuovo)):
            return precedente
        memoria[chiave] = nuovo
        return nuovo

    def _disponibile(self, m: Modello) -> bool:
        """Template di disponibilita': se va in errore, Home Assistant tiene il sensore disponibile."""
        assert self.lettore is not None
        if m.disponibile is None:
            return True
        try:
            return m.disponibile(self.lettore)
        except RuntimeError:
            raise
        except Exception:  # noqa: BLE001
            return True

    def _stato(self, m: Modello) -> str:
        """Template di stato: se va in errore, Home Assistant mostra il sensore non disponibile."""
        assert self.lettore is not None
        try:
            return m.stato(self.lettore)
        except RuntimeError:
            raise  # dipendenza circolare: errore di programmazione, non un caso del template
        except Exception:  # noqa: BLE001
            return _ERRORE_STATO

    def icona(self, chiave: str) -> str | None:
        """Icona calcolata; se il template dell'icona va in errore l'icona manca (None)."""
        m = MODELLI[chiave]
        assert self.lettore is not None and m.icona is not None
        try:
            return m.icona(self.lettore)
        except RuntimeError:
            raise
        except Exception:  # noqa: BLE001
            return None

    def condizione(self, chiave: str) -> str:
        """Per un sensore con «delay_on»: la condizione prima del ritardo (on/off)."""
        stato = self._stato(MODELLI[chiave])
        return "unavailable" if stato is _ERRORE_STATO else stato


from . import allerte, calendario, clima, free, qualita_aria, stato_vmc  # noqa: E402,F401  (registrano i modelli)
