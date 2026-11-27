"""Lettura dei valori per i modelli dei sensori e per il motore.

Ogni modello del package usava ``states('sensor.vmc_<nome>_x')``, ``is_state(...)`` e
``now()``. Qui le stesse letture passano da un ``Lettore``:

- ``v("sensor.x")`` legge una voce della VMC (la chiave e' l'entity_id del package senza
  ``vmc_<nome>_``), qualunque cosa sia diventata nella nativa (entita' o parte interna);
- ``s("sensor.qualsiasi")`` legge un entity_id completo, per esempio un sensore scelto
  dall'utente; se l'entity_id e' della VMC passa da ``v``;
- i risultati sono stringhe, come ``states()``: ``unknown`` se il valore non c'e'.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

SCONOSCIUTO = "unknown"


class Lettore:
    """Letture con la stessa semantica di ``states()`` e ``is_state()`` dei modelli."""

    def __init__(
        self,
        nome: str,
        proprio: Callable[[str], str | None],
        esterno: Callable[[str], str | None],
        adesso: Callable[[], datetime],
        attributo_proprio: Callable[[str, str], Any],
        attributo_esterno: Callable[[str, str], Any],
        *,
        ip: str = "",
        elenca: Callable[[str], list[Any]] | None = None,
        memoria: dict[str, Any] | None = None,
    ) -> None:
        """``ip``: indirizzo configurato della VMC; ``elenca(dominio)``: stati di Home
        Assistant di un dominio (come ``states.sensor``), con entity_id, state e attributes;
        ``memoria``: ultimo risultato di ogni modello, da un calcolo all'altro (lo stato di un
        template cambia solo se il risultato cambia: vedere risultato.uguali)."""
        self.nome = nome
        self.ip = ip
        self.memoria: dict[str, Any] = {} if memoria is None else memoria
        self._elenca = elenca
        self._prefisso = f"vmc_{nome}_"
        self._proprio = proprio
        self._esterno = esterno
        self._adesso = adesso
        self._attributo_proprio = attributo_proprio
        self._attributo_esterno = attributo_esterno

    def chiave(self, entity_id: str) -> str | None:
        """Chiave della voce della VMC per un entity_id del package, None se non e' della VMC."""
        dominio, _, oggetto = entity_id.partition(".")
        if oggetto.startswith(self._prefisso):
            return f"{dominio}.{oggetto[len(self._prefisso):]}"
        return None

    def entity_id(self, chiave: str) -> str:
        """entity_id del package per una chiave della VMC."""
        dominio, _, oggetto = chiave.partition(".")
        return f"{dominio}.{self._prefisso}{oggetto}"

    def v(self, chiave: str) -> str:
        valore = self._proprio(chiave)
        return SCONOSCIUTO if valore is None else valore

    def s(self, entity_id: Any) -> str:
        """Come ``states(x)``: accetta anche valori non stringa (diventano 'unknown')."""
        if not isinstance(entity_id, str):
            return SCONOSCIUTO
        chiave = self.chiave(entity_id)
        if chiave is not None:
            return self.v(chiave)
        valore = self._esterno(entity_id.lower())
        return SCONOSCIUTO if valore is None else valore

    def is_v(self, chiave: str, valore: str | list[str]) -> bool:
        stato = self._proprio(chiave)
        if stato is None:
            return False
        if isinstance(valore, list):
            return stato in valore
        return stato == valore

    def attr_v(self, chiave: str, nome: str) -> Any:
        """Come ``state_attr()`` per una voce della VMC."""
        return self._attributo_proprio(chiave, nome)

    def attr(self, entity_id: Any, nome: str) -> Any:
        """Come ``state_attr(x, nome)``: None se l'entita' o l'attributo non c'e'."""
        if not isinstance(entity_id, str):
            return None
        chiave = self.chiave(entity_id)
        if chiave is not None:
            return self.attr_v(chiave, nome)
        return self._attributo_esterno(entity_id.lower(), nome)

    def now(self) -> datetime:
        return self._adesso()

    def elenca(self, dominio: str) -> list[Any]:
        """Come ``states.<dominio>``: gli stati di Home Assistant di un dominio."""
        return [] if self._elenca is None else list(self._elenca(dominio))
