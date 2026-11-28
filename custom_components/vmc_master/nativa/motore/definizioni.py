"""Le definizioni delle automazioni e degli script del motore (scritte dal traduttore)."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .esecuzione import Corpo

    Condizione = Callable[[Any, Mapping[str, Any]], bool]


@dataclass(frozen=True, kw_only=True)
class Automazione:
    """Un'automazione del package, come la configurazione validata da Home Assistant."""

    alias: str
    id: str | None
    descrizione: str | None
    modo: str
    massimo: int | None
    avviso_massimo: str
    stato_iniziale: bool | None
    # trigger come configurazioni validate (``platform``...), con ``Modello`` al posto
    # dei Template
    trigger: Sequence[Mapping[str, Any]]
    condizioni: Sequence[Condizione] | None
    corpo: Corpo
    variabili: Mapping[str, Any] | None = None
    variabili_trigger: Mapping[str, Any] | None = None


@dataclass(frozen=True, kw_only=True)
class Script:
    """Uno script del package (``script.<chiave>``)."""

    chiave: str
    alias: str | None
    descrizione: str | None
    icona: str | None
    modo: str
    massimo: int | None
    avviso_massimo: str
    campi: Mapping[str, Any] = field(default_factory=dict)
    corpo: Corpo
    variabili: Mapping[str, Any] | None = None


# I tipi di comando (``Comando.tipo``): cosa faceva lo shell_command del package.
COMANDO_VMC = "vmc"  # printf '<testo>\n' | timeout 5 nc -w 3 <ip> 5001
COMANDO_NOME = "nome"  # bash vmc_<nome>_script_cambio_nome.sh "<nome nuovo>"
COMANDO_NESSUNO = "nessuno"  # toglieva i caratteri di ritorno dai file .sh


@dataclass(frozen=True, kw_only=True)
class Comando:
    """Uno shell_command del package (``shell_command.<nome>``), come comando del motore.

    ``testo``: il comando per la VMC (tipo ``vmc``). ``argomenti``: il modello degli
    argomenti del file .sh, senza il percorso del file (tipo ``nome``), reso con i dati
    della chiamata come lo rendeva ``shell_command``.
    """

    nome: str
    tipo: str
    testo: str = ""
    argomenti: Any = None
