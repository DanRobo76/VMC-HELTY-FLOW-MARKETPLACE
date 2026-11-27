"""Inventario esatto di come il motore tocca ogni aiutante del package (fase 4).

Gli aiutanti sono le 342 voci «da aiutante» del package (dopo ``rimuovi_sezioni_solo_master``):
input_boolean, input_number, input_text, input_select, input_datetime, timer, script e
shell_command. Per ognuna l'inventario conta, sulle configurazioni di automazioni e script
validate da Home Assistant (le stesse che legge il traduttore, ``traduci.py``):

- le letture nei modelli (``states()``, ``is_state()``, ``state_attr()`` con l'attributo,
  ``states.dominio.oggetto``, ``expand()`` e le altre funzioni), per posizione del modello
  (trigger, condizione, attesa, variabili, dati e bersagli dei servizi...) e per come il
  valore letto viene usato (``| float``, ``== 'on'``, scritto nel testo...);
- i trigger di stato di cui è il soggetto (con from/to/not_from/not_to/for/attribute) e i
  trigger a modello che la leggono;
- le condizioni di stato e a modello che la leggono;
- i servizi chiamati su di lei, con il nome esatto e le chiavi dei dati;
- dove il suo entity_id compare come costante fuori da una lettura diretta (liste,
  variabili, confronti, dati dei servizi): i posti che un cambio di nome deve conoscere.

A parte elenca: ogni entity_id o nome di servizio COSTRUITO durante l'esecuzione, ogni uso
del contesto e degli istanti (``context``, ``last_changed``...), i trigger a evento e ciò
che riguarda i timer.

I modelli si leggono dall'albero di Jinja (lo stesso ambiente del traduttore), non dal
testo dello YAML; solo il testo fuori dai ``{{ }}`` e le costanti si cercano con
un'espressione regolare, perché sono testo.

Uso::

    /home/user/hat/bin/python tests/nativa/motore/inventario_aiutanti.py           # totali
    /home/user/hat/bin/python tests/nativa/motore/inventario_aiutanti.py --scrivi  # e i CSV

I CSV (``inventario_aiutanti*.csv``) stanno accanto a questo file;
``test_aiutanti_inventario.py`` controlla che siano aggiornati.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import time, timedelta
from pathlib import Path
from typing import Any

if (
    __name__ == "__main__"
):  # eseguito come programma: la radice del progetto nel percorso
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    import tests.conftest  # noqa: F401  (Home Assistant prima del plugin dei test)

import yaml
from homeassistant.components.automation.config import (
    async_validate_config_item as valida_automazione,
)
from homeassistant.components.script.config import (
    async_validate_config_item as valida_script,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.script_variables import ScriptVariables
from homeassistant.helpers.template import Template
from homeassistant.util import slugify
from jinja2 import nodes

from custom_components.vmc_master.trasforma import rimuovi_sezioni_solo_master
from tests.nativa.motore.traduci import PACKAGE, _Caricatore, leggi_package
from tests.nativa.motore.traduci_jinja import AMBIENTE

QUI = Path(__file__).resolve().parent
FASE1 = QUI / "aiutanti_fase1.csv"
"""Le 342 righe «da aiutante» dell'inventario approvato della fase 1 (entita.csv)."""

DOMINI_AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_text",
    "input_select",
    "input_datetime",
    "timer",
)
DOMINI_SIMILI = (*DOMINI_AIUTANTI, "script", "shell_command")

# Funzioni dei modelli che ricevono un entity_id (quelle che il package usa davvero le
# controlla ``_Visita._chiamata``: una funzione nuova che legge gli stati ferma tutto).
FUNZIONI_STATO = {
    "states": "states()",
    "is_state": "is_state()",
    "state_attr": "state_attr()",
    "is_state_attr": "is_state_attr()",
    "has_value": "has_value()",
    "expand": "expand()",
    "device_name": "device_name()",
    "entity_name": "entity_name()",
}
FUNZIONI_NOTE = FUNZIONI_STATO.keys() | {
    "now",
    "utcnow",
    "as_timestamp",
    "as_datetime",
    "strptime",
    "namespace",
    "timedelta",
    "integration_entities",
}
# Nomi di filtri e test che leggono gli stati se passati a map/select/reject...
FILTRI_STATO = {
    "states",
    "is_state",
    "state_attr",
    "is_state_attr",
    "has_value",
    "expand",
}
ISTANTI = {"last_changed", "last_updated", "last_reported", "last_triggered"}
RADICI = {"trigger", "this", "repeat", "wait", "context"}

_ID = re.compile(r"(?<![A-Za-z0-9_.])([a-z_]+)\.([a-z0-9_]+)")
_NOME = re.compile(r"(?<![A-Za-z0-9_.])((?:automazione_)?vmc_master[a-z0-9_]*)")
_MASTER = re.compile("master", re.IGNORECASE)

BINARI = {
    nodes.Add: "+",
    nodes.Sub: "-",
    nodes.Mul: "*",
    nodes.Div: "/",
    nodes.FloorDiv: "//",
    nodes.Mod: "%",
    nodes.Pow: "**",
}
CONFRONTI = {
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "gteq": ">=",
    "lt": "<",
    "lteq": "<=",
    "in": "in",
    "notin": "not in",
}


class Sconosciuto(Exception):
    """Una forma che l'inventario non conosce: meglio fermarsi che contare male."""


# --- il package ---------------------------------------------------------------------------


def leggi_sezioni() -> dict[str, Any]:
    """Tutte le sezioni di vmc_master.yaml (senza le sezioni solo del master)."""
    return yaml.load(
        rimuovi_sezioni_solo_master((PACKAGE / "vmc_master.yaml").read_text("utf-8")),
        Loader=_Caricatore,
    )


def leggi_fase1() -> dict[str, dict[str, str]]:
    """entity_id di oggi -> riga dell'inventario della fase 1 (colonna «Domani» compresa)."""
    righe = csv.DictReader(io.StringIO(FASE1.read_text("utf-8")), delimiter=";")
    return {riga["Entità oggi"]: riga for riga in righe}


def catalogo(sezioni: Mapping[str, Any]) -> dict[str, str]:
    """entity_id -> tipo di oggi per tutte le entità che il package definisce."""
    uscita: dict[str, str] = {}
    for dominio in DOMINI_SIMILI:
        for oggetto in sezioni.get(dominio) or {}:
            uscita[f"{dominio}.{oggetto}"] = dominio
    for blocco in sezioni.get("template") or []:
        for dominio in ("sensor", "binary_sensor"):
            for conf in blocco.get(dominio) or []:
                uscita[conf["default_entity_id"]] = f"template {dominio}"
    for conf in sezioni.get("sensor") or []:
        uscita[f"sensor.{conf['name']}"] = f"sensor {conf['platform']}"
    for voce in sezioni.get("command_line") or []:
        for dominio, conf in voce.items():
            uscita[f"{dominio}.{conf['name']}"] = f"command_line {dominio}"
    return uscita


# --- il testo di un'espressione di Jinja ---------------------------------------------------


def testo(nodo: nodes.Node | None) -> str:
    """Un'espressione di Jinja riscritta come testo (per gli elenchi)."""
    if nodo is None:
        return ""
    if isinstance(nodo, nodes.Const):
        return repr(nodo.value)
    if isinstance(nodo, nodes.TemplateData):
        return repr(nodo.data)
    if isinstance(nodo, nodes.Name):
        return nodo.name
    if isinstance(nodo, nodes.NSRef):
        return f"{nodo.name}.{nodo.attr}"
    if isinstance(nodo, nodes.Getattr):
        return f"{testo(nodo.node)}.{nodo.attr}"
    if isinstance(nodo, nodes.Getitem):
        return f"{testo(nodo.node)}[{testo(nodo.arg)}]"
    if isinstance(nodo, nodes.Slice):
        parti = [testo(nodo.start), testo(nodo.stop)]
        if nodo.step is not None:
            parti.append(testo(nodo.step))
        return ":".join(parti)
    if isinstance(nodo, (nodes.Call, nodes.Filter, nodes.Test)):
        argomenti = [testo(a) for a in nodo.args]
        argomenti += [f"{k.key}={testo(k.value)}" for k in nodo.kwargs]
        dentro = ", ".join(argomenti)
        if isinstance(nodo, nodes.Call):
            return f"{testo(nodo.node)}({dentro})"
        if isinstance(nodo, nodes.Filter):
            base = testo(nodo.node) if nodo.node is not None else ""
            return f"{base} | {nodo.name}" + (f"({dentro})" if dentro else "")
        return f"{testo(nodo.node)} is {nodo.name}" + (f"({dentro})" if dentro else "")
    if isinstance(nodo, nodes.List):
        return "[" + ", ".join(testo(v) for v in nodo.items) + "]"
    if isinstance(nodo, nodes.Tuple):
        return "(" + ", ".join(testo(v) for v in nodo.items) + ")"
    if isinstance(nodo, nodes.Dict):
        return (
            "{"
            + ", ".join(f"{testo(p.key)}: {testo(p.value)}" for p in nodo.items)
            + "}"
        )
    if isinstance(nodo, nodes.CondExpr):
        altrimenti = f" else {testo(nodo.expr2)}" if nodo.expr2 is not None else ""
        return f"({testo(nodo.expr1)} if {testo(nodo.test)}{altrimenti})"
    if isinstance(nodo, nodes.And):
        return f"({testo(nodo.left)} and {testo(nodo.right)})"
    if isinstance(nodo, nodes.Or):
        return f"({testo(nodo.left)} or {testo(nodo.right)})"
    if isinstance(nodo, nodes.Not):
        return f"not {testo(nodo.node)}"
    if isinstance(nodo, nodes.Neg):
        return f"-{testo(nodo.node)}"
    if isinstance(nodo, nodes.Pos):
        return f"+{testo(nodo.node)}"
    if type(nodo) in BINARI:
        return f"({testo(nodo.left)} {BINARI[type(nodo)]} {testo(nodo.right)})"
    if isinstance(nodo, nodes.Concat):
        return " ~ ".join(testo(v) for v in nodo.nodes)
    if isinstance(nodo, nodes.Compare):
        parti = [testo(nodo.expr)]
        for operando in nodo.ops:
            parti += [CONFRONTI[operando.op], testo(operando.expr)]
        return " ".join(parti)
    raise Sconosciuto(f"espressione {type(nodo).__name__}")


def _corto(riga: str, massimo: int = 300) -> str:
    riga = " ".join(riga.split())
    return riga if len(riga) <= massimo else riga[: massimo - 3] + "..."


# --- l'analisi di un modello ----------------------------------------------------------------


@dataclass
class Analisi:
    """Ciò che un modello legge e costruisce (una volta per testo distinto)."""

    # (entity_id, tipo di lettura, dettaglio, uso del valore)
    letture: list[tuple[str, str, str, str]] = field(default_factory=list)
    # (entity_id, dove compare la costante)
    costanti: list[tuple[str, str]] = field(default_factory=list)
    # (classe, tipo, testo dell'espressione): classe «uso» (un entity_id non costante
    # dove si legge), «costruzione» (un testo composto con un pezzo di nome), «elenco»
    # (entità trovate scorrendo gli stati)
    dinamici: list[tuple[str, str, str]] = field(default_factory=list)
    # nomi composti: (testo, prefisso, suffisso, valori possibili del pezzo o None)
    costruiti: list[tuple[str, str, str, tuple[str, ...] | None]] = field(
        default_factory=list
    )
    # (tipo, testo dell'espressione, entity_id o "")
    contesto: list[tuple[str, str, str]] = field(default_factory=list)
    # catene che partono da trigger/this/repeat/wait/context
    radici: Counter[str] = field(default_factory=Counter)
    funzioni: Counter[str] = field(default_factory=Counter)
    filtri: Counter[str] = field(default_factory=Counter)
    # testi con «master» che non sono un entity_id del package: (classe, testo)
    testi: list[tuple[str, str]] = field(default_factory=list)


class Analizzatore:
    """Legge l'albero di Jinja di un modello."""

    def __init__(self, entita: Mapping[str, str]) -> None:
        self.entita = entita
        self.oggetti = {e.split(".", 1)[1] for e in entita}
        self._fatte: dict[str, Analisi] = {}

    def analizza(self, sorgente: str) -> Analisi:
        sorgente = sorgente.strip()  # come Template.__init__
        if (fatta := self._fatte.get(sorgente)) is None:
            fatta = self._fatte[sorgente] = _Visita(self, AMBIENTE.parse(sorgente)).a
        return fatta

    # --- le costanti (anche quelle delle configurazioni, fuori dai modelli) ----------------

    def classifica(self, valore: str) -> tuple[str, list[str]]:
        """La classe di un testo e gli entity_id del package che contiene.

        ``id``: è un entity_id del package; ``testo con id``: lo contiene; ``frammento``:
        contiene un pezzo di entity_id (dominio.vmc_master_...) che non è un'entità;
        ``nome``: il nome senza dominio di un'entità o di un servizio (vmc_master_...);
        ``frammento di nome``: l'inizio di uno o più nomi; ``nome non di entità``: un
        nome con vmc_master che non è di un'entità (per esempio l'id di una notifica);
        ``prosa``: «Master» in un testo per l'utente; ``altro``: niente che riguardi i
        nomi.
        """
        if valore in self.entita:
            return "id", [valore]
        if not _MASTER.search(valore):
            return "altro", []
        valore = valore.replace("\\.", ".")  # un'espressione regolare: timer\.vmc_...
        trovati, frammenti = [], False
        resto = valore
        for trovato in _ID.finditer(valore):
            intero = trovato.group(0)
            if not _MASTER.search(intero):
                continue
            if intero in self.entita:
                trovati.append(intero)
            else:
                frammenti = True
            resto = resto.replace(intero, " ")
        if frammenti:
            return "frammento", trovati
        if trovati:
            return "testo con id", trovati
        nomi = _NOME.findall(resto)
        if nomi:
            if all(nome in self.oggetti for nome in nomi):
                return "nome", []
            if any(o.startswith(nome) for nome in nomi for o in self.oggetti):
                return "frammento di nome", []
            return "nome non di entità", []
        return "prosa", []


class _Visita:
    """Una passata sull'albero di un modello."""

    def __init__(self, analizzatore: Analizzatore, albero: nodes.Template) -> None:
        self.x = analizzatore
        self.a = Analisi()
        self._genitori: dict[int, nodes.Node] = {}
        self._consumati: set[int] = set()  # costanti già contate come lettura
        self._catene: set[int] = set()  # nodi interni di una catena già contata
        self._assegnati = {
            nodo.name
            for nodo in albero.find_all(nodes.Name)
            if nodo.ctx in ("store", "param")
        }
        if ombre := self._assegnati & (FUNZIONI_NOTE | {"states"}):
            raise Sconosciuto(f"funzioni globali riassegnate nel modello: {ombre}")
        # variabile -> le entità che le sono state assegnate come oggetto di stato
        # (``{% set fase = states.input_number.x %}``, anche in una lista): servono per
        # attribuire ``fase.last_changed`` all'entità
        self._variabili: dict[str, set[str]] = defaultdict(set)
        for assegna in albero.find_all(nodes.Assign):
            if not isinstance(assegna.target, nodes.Name):
                continue
            valori = (
                assegna.node.items
                if isinstance(assegna.node, (nodes.List, nodes.Tuple))
                else [assegna.node]
            )
            for valore in valori:
                if (entita := _oggetto_di_stato(valore)) is not None:
                    self._variabili[assegna.target.name].add(entita)
        self._parenti(albero)
        self._visita(albero)

    def _parenti(self, nodo: nodes.Node) -> None:
        for figlio in nodo.iter_child_nodes():
            self._genitori[id(figlio)] = nodo
            self._parenti(figlio)

    def _genitore(self, nodo: nodes.Node) -> nodes.Node | None:
        genitore = self._genitori.get(id(nodo))
        # Operand, Keyword e Pair non contano: si guarda chi li contiene
        if isinstance(genitore, (nodes.Operand, nodes.Keyword, nodes.Pair)):
            return self._genitori.get(id(genitore))
        return genitore

    # --- la visita ------------------------------------------------------------------------

    def _visita(self, nodo: nodes.Node) -> None:
        if isinstance(nodo, nodes.Call):
            self._chiamata(nodo)
        elif isinstance(nodo, (nodes.Getattr, nodes.Getitem)):
            self._catena(nodo)
        elif isinstance(nodo, nodes.Name):
            self._nome(nodo)
        elif isinstance(nodo, nodes.Filter):
            self._filtro(nodo)
        elif isinstance(nodo, nodes.Test):
            if nodo.name in FILTRI_STATO:
                raise Sconosciuto(f"test {nodo.name}")
        elif isinstance(nodo, nodes.Const):
            self._costante(nodo)
        elif isinstance(nodo, nodes.TemplateData):
            self._dati(nodo)
        if type(nodo) in (nodes.Concat, nodes.Add, nodes.Mod):
            segni = {nodes.Concat: "~", nodes.Add: "+", nodes.Mod: "%"}
            self._costruzione(nodo, segni[type(nodo)])
        for figlio in nodo.iter_child_nodes():
            self._visita(figlio)

    def _chiamata(self, nodo: nodes.Call) -> None:
        if nodo.dyn_args is not None or nodo.dyn_kwargs is not None:
            raise Sconosciuto("*args o **kwargs")
        funzione = nodo.node
        if isinstance(funzione, nodes.Getattr):
            if funzione.attr in ("format", "replace", "join"):
                self._costruzione(nodo, f".{funzione.attr}()")
            return
        if not isinstance(funzione, nodes.Name):
            raise Sconosciuto(f"chiamata di {type(funzione).__name__}")
        nome = funzione.name
        self.a.funzioni[nome] += 1
        if nome in self._assegnati:
            return  # una variabile del modello chiamata come funzione
        if nome not in FUNZIONI_NOTE:
            raise Sconosciuto(f"funzione {nome}")
        if nome == "integration_entities":
            self.a.dinamici.append(
                (
                    "elenco",
                    "entità di un'integrazione (integration_entities)",
                    testo(nodo),
                )
            )
            return
        if nome not in FUNZIONI_STATO:
            return
        tipo = FUNZIONI_STATO[nome]
        if nome == "expand":
            for argomento in nodo.args:
                self._soggetto(nodo, argomento, tipo, "")
            return
        if not nodo.args:
            raise Sconosciuto(f"{nome} senza argomenti")
        dettaglio = ""
        if nome in ("state_attr", "is_state_attr"):
            attributo = nodo.args[1]
            dettaglio = (
                attributo.value
                if isinstance(attributo, nodes.Const)
                else f"<{testo(attributo)}>"
            )
            if isinstance(attributo, nodes.Const):
                self._consumati.add(id(attributo))
                if attributo.value in ISTANTI:
                    soggetto = nodo.args[0]
                    self.a.contesto.append(
                        (
                            attributo.value,
                            testo(nodo),
                            soggetto.value if isinstance(soggetto, nodes.Const) else "",
                        )
                    )
        elif nome == "is_state":
            dettaglio = testo(nodo.args[1])
        elif nome == "states" and (len(nodo.args) > 1 or nodo.kwargs):
            dettaglio = ", ".join(
                [testo(a) for a in nodo.args[1:]]
                + [f"{k.key}={testo(k.value)}" for k in nodo.kwargs]
            )
        self._soggetto(nodo, nodo.args[0], tipo, dettaglio)

    def _soggetto(
        self, lettura: nodes.Node, soggetto: nodes.Node, tipo: str, dettaglio: str
    ) -> None:
        """L'entità letta: una costante (lettura diretta) o un'espressione (dinamica)."""
        if isinstance(soggetto, nodes.Const) and isinstance(soggetto.value, str):
            self._consumati.add(id(soggetto))
            self.a.letture.append((soggetto.value, tipo, dettaglio, self._uso(lettura)))
            return
        if isinstance(soggetto, (nodes.List, nodes.Tuple)) and all(
            isinstance(v, nodes.Const) and isinstance(v.value, str)
            for v in soggetto.items
        ):
            for voce in soggetto.items:
                self._consumati.add(id(voce))
                self.a.letture.append((voce.value, tipo, dettaglio, self._uso(lettura)))
            return
        self.a.dinamici.append(
            ("uso", f"{tipo} con entity_id non costante", testo(lettura))
        )

    def _catena(self, nodo: nodes.Getattr | nodes.Getitem) -> None:
        """``a.b.c`` e ``a['b']``: contata una volta, dal nodo più esterno."""
        if id(nodo) in self._catene:
            return
        parti: list[str] = []
        corrente: nodes.Node = nodo
        while isinstance(corrente, (nodes.Getattr, nodes.Getitem)):
            self._catene.add(id(corrente))
            if isinstance(corrente, nodes.Getattr):
                parti.append(corrente.attr)
            elif isinstance(corrente.arg, nodes.Const) and isinstance(
                corrente.arg.value, str
            ):
                parti.append(corrente.arg.value)
                self._consumati.add(id(corrente.arg))
            else:
                parti.append(f"[{testo(corrente.arg)}]")
            corrente = corrente.node
        parti.reverse()
        radice = corrente.name if isinstance(corrente, nodes.Name) else None
        intera = testo(nodo)
        entita = ""
        if radice == "states" and "states" not in self._assegnati:
            self._consumati.add(id(corrente))
            if parti[0].startswith("["):
                self.a.dinamici.append(
                    ("uso", "states[...] con entity_id non costante", intera)
                )
            elif "." in parti[0]:  # states['dominio.oggetto']
                entita = parti[0]
                self._lettura_oggetto(nodo, entita, "states[...]", parti[1:])
            elif len(parti) == 1:
                self.a.dinamici.append(
                    ("elenco", "tutte le entità di un dominio", intera)
                )
            elif parti[1].startswith("["):
                self.a.dinamici.append(
                    ("uso", "states.dominio[...] non costante", intera)
                )
            else:
                entita = f"{parti[0]}.{parti[1]}"
                self._lettura_oggetto(nodo, entita, "states.dominio.oggetto", parti[2:])
        elif radice in RADICI and radice not in self._assegnati:
            self.a.radici[intera] += 1
        soggetti = [entita] if entita else sorted(self._variabili.get(radice or "", ()))
        for parte in parti:
            if parte in ISTANTI or parte == "context":
                for soggetto in soggetti or [""]:
                    self.a.contesto.append((parte, intera, soggetto))
        if radice == "context" and radice not in self._assegnati:
            self.a.contesto.append(("context", intera, ""))

    def _lettura_oggetto(
        self, nodo: nodes.Node, entita: str, tipo: str, resto: list[str]
    ) -> None:
        self.a.letture.append(
            (entita, tipo, ".".join(resto) or "(oggetto)", self._uso(nodo))
        )

    def _nome(self, nodo: nodes.Name) -> None:
        if nodo.ctx != "load" or nodo.name in self._assegnati:
            return
        genitore = self._genitori.get(id(nodo))
        if nodo.name == "states":
            if isinstance(genitore, nodes.Call) and genitore.node is nodo:
                return
            if id(nodo) in self._consumati:
                return
            self.a.dinamici.append(
                ("elenco", "tutte le entità (states)", testo(genitore))
            )
        elif nodo.name in RADICI:
            if (
                isinstance(genitore, (nodes.Getattr, nodes.Getitem))
                and genitore.node is nodo
            ):
                return  # contata dalla catena
            self.a.radici[nodo.name] += 1
            if nodo.name == "context":
                self.a.contesto.append(("context", testo(genitore), ""))

    def _filtro(self, nodo: nodes.Filter) -> None:
        self.a.filtri[nodo.name] += 1
        if nodo.name in FILTRI_STATO:
            raise Sconosciuto(f"filtro {nodo.name}")
        if nodo.name in ("format", "replace", "regex_replace", "join"):
            self._costruzione(nodo, f"| {nodo.name}")
        if nodo.name in ("map", "select", "reject", "selectattr", "rejectattr"):
            for argomento in nodo.args:
                if (
                    isinstance(argomento, nodes.Const)
                    and argomento.value in FILTRI_STATO
                ):
                    self.a.dinamici.append(
                        (
                            "elenco",
                            f"| {nodo.name}('{argomento.value}') su un elenco",
                            testo(nodo),
                        )
                    )
                self._attributo_per_nome(nodo, argomento)
            for chiave in nodo.kwargs:
                self._attributo_per_nome(nodo, chiave.value)
        elif nodo.name in ("sort", "groupby", "unique", "min", "max", "sum"):
            for chiave in nodo.kwargs:
                self._attributo_per_nome(nodo, chiave.value)

    def _attributo_per_nome(self, filtro: nodes.Filter, nodo: nodes.Node) -> None:
        """``map(attribute='last_changed')``, ``selectattr('context.user_id', ...)``."""
        if not (isinstance(nodo, nodes.Const) and isinstance(nodo.value, str)):
            return
        base = filtro.node
        while isinstance(base, nodes.Filter):
            base = base.node
        soggetti = (
            sorted(self._variabili.get(base.name, ()))
            if isinstance(base, nodes.Name)
            else []
        )
        for parte in nodo.value.split("."):
            if parte in ISTANTI or parte == "context":
                for soggetto in soggetti or [""]:
                    self.a.contesto.append((parte, testo(filtro), soggetto))

    def _costante(self, nodo: nodes.Const) -> None:
        if not isinstance(nodo.value, str) or id(nodo) in self._consumati:
            return
        classe, trovati = self.x.classifica(nodo.value)
        if classe == "altro":
            return
        dove = self._dove_costante(nodo)
        for entita in trovati:
            self.a.costanti.append(
                (entita, dove if classe == "id" else f"{dove}, dentro un testo")
            )
        if classe != "id":
            self.a.testi.append((classe, nodo.value))

    def _dati(self, nodo: nodes.TemplateData) -> None:
        classe, trovati = self.x.classifica(nodo.data)
        if classe == "altro":
            return
        for entita in trovati:
            self.a.costanti.append((entita, "testo del modello fuori da {{ }}"))
        if classe != "id":
            self.a.testi.append((classe, nodo.data))
        if classe == "prosa":
            return
        genitore = self._genitori.get(id(nodo))
        if isinstance(genitore, nodes.Output) and len(genitore.nodes) > 1:
            pezzi = [
                n.data
                if isinstance(n, nodes.TemplateData)
                else "{{ " + testo(n) + " }}"
                for n in genitore.nodes
            ]
            intero = _corto("".join(pezzi))
            self.a.dinamici.append(
                ("costruzione", f"testo del modello con espressioni ({classe})", intero)
            )
            if nodo is genitore.nodes[0] or not isinstance(
                genitore.nodes[genitore.nodes.index(nodo) - 1], nodes.TemplateData
            ):
                self._costruito(intero, genitore.nodes[genitore.nodes.index(nodo) :])

    def _costruzione(self, nodo: nodes.Node, operatore: str) -> None:
        """Un testo composto durante la resa: conta se un suo pezzo è un pezzo di nome."""
        genitore = self._genitori.get(id(nodo))
        if type(genitore) is type(nodo) and type(nodo) in (nodes.Concat, nodes.Add):
            return  # contata dal nodo più esterno
        classi = set()
        for costante in nodo.find_all(nodes.Const):
            if isinstance(costante.value, str) and not self._soggetto_di_lettura(
                costante
            ):
                classi.add(self.x.classifica(costante.value)[0])
        nomi = classi & {"id", "frammento", "nome", "frammento di nome", "testo con id"}
        if not nomi:
            return
        intero = testo(nodo)
        self.a.dinamici.append(
            (
                "costruzione",
                f"testo composto con {operatore} ({', '.join(sorted(nomi))})",
                intero,
            )
        )
        if isinstance(nodo, nodes.Concat):
            self._costruito(intero, nodo.nodes)
        elif (
            isinstance(nodo, nodes.Filter)
            and nodo.name == "replace"
            and nodo.args
            and isinstance(nodo.args[0], nodes.Const)
        ):
            # ``x | replace('timer.vmc_master_lettura_', '')``: toglie un prefisso
            self.a.costruiti.append((intero, nodo.args[0].value, "", None))

    def _soggetto_di_lettura(self, costante: nodes.Const) -> bool:
        """La costante è l'entity_id di una lettura diretta (già contata come lettura)."""
        genitore = self._genitori.get(id(costante))
        return (
            isinstance(genitore, nodes.Call)
            and isinstance(genitore.node, nodes.Name)
            and genitore.node.name in FUNZIONI_STATO
            and bool(genitore.args)
            and genitore.args[0] is costante
        )

    def _costruito(self, intero: str, parti: list[nodes.Node]) -> None:
        """Un nome composto da un inizio costante e un pezzo calcolato: l'inizio, la
        fine e, se il pezzo è scelto fra costanti, i suoi valori possibili."""
        testi = [
            p.value
            if isinstance(p, nodes.Const) and isinstance(p.value, str)
            else p.data
            if isinstance(p, nodes.TemplateData)
            else None
            for p in parti
        ]
        if testi[0] is None or not testi[0].strip():
            return
        prefisso = testi[0].split()[-1]
        if self.x.classifica(prefisso)[0] not in ("frammento", "frammento di nome"):
            return
        calcolati = [p for p, t in zip(parti, testi, strict=True) if t is None]
        suffisso, valori = "", None
        if len(calcolati) == 1 and testi[1] is None:
            if len(parti) > 2 and testi[2] is not None and testi[2].strip():
                suffisso = testi[2].split()[0]
            valori = self._valori(calcolati[0])
        self.a.costruiti.append((intero, prefisso, suffisso, valori))

    @staticmethod
    def _valori(nodo: nodes.Node) -> tuple[str, ...] | None:
        """I valori possibili di ``{...}[x]`` o ``[...][x]`` con soli testi costanti."""
        if not isinstance(nodo, nodes.Getitem):
            return None
        base = nodo.node
        if isinstance(base, nodes.Dict):
            voci = [p.value for p in base.items]
        elif isinstance(base, (nodes.List, nodes.Tuple)):
            voci = list(base.items)
        else:
            return None
        if all(isinstance(v, nodes.Const) and isinstance(v.value, str) for v in voci):
            return tuple(v.value for v in voci)
        return None

    # --- come si usa un valore ---------------------------------------------------------------

    def _uso(self, nodo: nodes.Node) -> str:
        """Chi consuma il valore letto (il nodo che lo contiene)."""
        genitore = self._genitore(nodo)
        if isinstance(genitore, nodes.Filter) and genitore.node is nodo:
            return f"| {genitore.name}"
        if isinstance(genitore, nodes.Filter):
            return f"argomento di | {genitore.name}"
        if isinstance(genitore, nodes.Compare):
            return self._confronto(genitore, nodo)
        if isinstance(genitore, nodes.Getattr):
            nonno = self._genitore(genitore)
            if isinstance(nonno, nodes.Call) and nonno.node is genitore:
                argomenti = ", ".join(testo(a) for a in nonno.args)
                return f".{genitore.attr}({argomenti})"
            return f".{genitore.attr}"
        if isinstance(genitore, nodes.Getitem):
            return f"[{testo(genitore.arg)}]"
        if isinstance(genitore, nodes.Call):
            return f"argomento di {testo(genitore.node)}()"
        if isinstance(genitore, nodes.Output):
            return "scritto {{ }}"
        if isinstance(genitore, nodes.Test):
            return f"is {genitore.name}"
        if isinstance(genitore, (nodes.Concat, nodes.Add)):
            return "unito a un testo"
        if isinstance(genitore, (nodes.And, nodes.Or, nodes.Not)):
            return "vero o falso"
        if isinstance(genitore, (nodes.If, nodes.CondExpr)):
            if genitore.test is nodo:
                return "vero o falso"
            return "ramo di un if"
        if isinstance(genitore, nodes.Assign):
            return "assegnato a una variabile"
        if isinstance(genitore, (nodes.List, nodes.Tuple, nodes.Dict)):
            return "in una lista o dizionario"
        if isinstance(genitore, nodes.For):
            return "scorso da un for"
        if type(genitore) in BINARI or isinstance(genitore, (nodes.Neg, nodes.Pos)):
            return "in un calcolo"
        raise Sconosciuto(f"uso in {type(genitore).__name__}")

    def _confronto(self, confronto: nodes.Compare, nodo: nodes.Node) -> str:
        if confronto.expr is nodo:
            parti = [
                f"{CONFRONTI[operando.op]} {self._altro_lato(operando.expr)}"
                for operando in confronto.ops
            ]
            return " ".join(parti)
        for operando in confronto.ops:
            if operando.expr is nodo:
                lato = self._altro_lato(confronto.expr)
                return f"{lato} {CONFRONTI[operando.op]} <stato>"
        raise Sconosciuto("confronto")

    @staticmethod
    def _altro_lato(nodo: nodes.Node) -> str:
        if isinstance(nodo, nodes.Const):
            return repr(nodo.value)
        if isinstance(nodo, (nodes.List, nodes.Tuple)) and all(
            isinstance(v, nodes.Const) for v in nodo.items
        ):
            return testo(nodo)
        return "<espressione>"

    def _dove_costante(self, nodo: nodes.Const) -> str:
        genitore = self._genitore(nodo)
        if isinstance(genitore, (nodes.List, nodes.Tuple)):
            return "in una lista"
        if isinstance(genitore, nodes.Dict):
            return "in un dizionario"
        if isinstance(genitore, nodes.Compare):
            altro = genitore.ops[0].expr if genitore.expr is nodo else genitore.expr
            return f"confrontata con {_corto(testo(altro), 60)}"
        if isinstance(genitore, nodes.Assign):
            return "assegnata a una variabile"
        if isinstance(genitore, nodes.CondExpr):
            return "ramo di un if"
        if isinstance(genitore, nodes.Output):
            return "scritta {{ }}"
        if isinstance(genitore, (nodes.Concat, nodes.Add)):
            return "unita a un testo"
        if isinstance(genitore, nodes.Call):
            return f"argomento di {_corto(testo(genitore.node), 40)}()"
        if isinstance(genitore, nodes.Filter):
            return f"argomento di | {genitore.name}"
        return type(genitore).__name__


def _oggetto_di_stato(nodo: nodes.Node) -> str | None:
    """``states.dominio.oggetto`` (l'oggetto intero, senza attributi): l'entity_id."""
    if (
        isinstance(nodo, nodes.Getattr)
        and isinstance(nodo.node, nodes.Getattr)
        and isinstance(nodo.node.node, nodes.Name)
        and nodo.node.node.name == "states"
    ):
        return f"{nodo.node.attr}.{nodo.attr}"
    return None


# --- l'inventario ---------------------------------------------------------------------------


@dataclass
class Inventario:
    """I fatti raccolti sulle configurazioni validate."""

    entita: dict[str, str]
    analizzatore: Analizzatore
    # (entity_id, posizione, tipo, dettaglio, uso)
    letture: Counter[tuple[str, str, str, str, str]] = field(default_factory=Counter)
    # entity_id -> i trigger, le condizioni e le attese a modello che la leggono
    trigger_modello: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    condizioni_modello: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    attese_modello: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    # (entity_id, filtri del trigger)
    trigger_stato: Counter[tuple[str, str]] = field(default_factory=Counter)
    trigger_ora: Counter[str] = field(default_factory=Counter)
    condizioni_stato: Counter[tuple[str, str]] = field(default_factory=Counter)
    # (entity_id, servizio, dettaglio dei dati, da dove viene l'entity_id)
    scritture: Counter[tuple[str, str, str, str]] = field(default_factory=Counter)
    # (entity_id, posizione, dove compare)
    costanti: Counter[tuple[str, str, str]] = field(default_factory=Counter)
    # (classe, tipo, posizione, testo, luogo)
    dinamici: list[tuple[str, str, str, str, str]] = field(default_factory=list)
    # (testo, prefisso, suffisso, valori possibili o None) -> quante volte
    costruiti: Counter[tuple[str, str, str, tuple[str, ...] | None]] = field(
        default_factory=Counter
    )
    # (tipo, posizione, testo, entity_id, luogo)
    contesto: list[tuple[str, str, str, str, str]] = field(default_factory=list)
    # (automazione, indice, id, tipi di evento, dati, contesto)
    eventi: list[tuple[str, int, str, str, str, str]] = field(default_factory=list)
    radici: Counter[tuple[str, str]] = field(default_factory=Counter)
    trigger: Counter[str] = field(default_factory=Counter)
    condizioni: Counter[str] = field(default_factory=Counter)
    azioni: Counter[str] = field(default_factory=Counter)
    servizi: Counter[str] = field(default_factory=Counter)
    modelli: Counter[str] = field(default_factory=Counter)  # per posizione
    posti: Counter[str] = field(default_factory=Counter)  # testo -> in quanti posti
    funzioni: Counter[str] = field(default_factory=Counter)
    filtri: Counter[str] = field(default_factory=Counter)
    testi: Counter[tuple[str, str]] = field(default_factory=Counter)
    timer: dict[str, dict[str, Any]] = field(default_factory=dict)

    # --- i modelli --------------------------------------------------------------------------

    def modello(self, modello: Template, posizione: str, luogo: str) -> None:
        """Conta ciò che legge un modello che sta in ``posizione``."""
        if modello.is_static:
            self.testo(modello.template, posizione)
            return
        self.modelli[posizione] += 1
        self.posti[modello.template.strip()] += 1
        a = self.analizzatore.analizza(modello.template)
        for entita, tipo, dettaglio, uso in a.letture:
            self.letture[entita, posizione, tipo, dettaglio, uso] += 1
            if posizione == "trigger":
                self.trigger_modello[entita].add(luogo)
            elif posizione == "condizione":
                self.condizioni_modello[entita].add(luogo)
            elif posizione == "attesa":
                self.attese_modello[entita].add(luogo)
        for entita, dove in a.costanti:
            self.costanti[entita, posizione, dove] += 1
        for classe, tipo, espressione in a.dinamici:
            self.dinamici.append((classe, tipo, posizione, espressione, luogo))
        self.costruiti.update(a.costruiti)
        for tipo, espressione, entita in a.contesto:
            self.contesto.append((tipo, posizione, espressione, entita, luogo))
        for catena, quante in a.radici.items():
            self.radici[catena, posizione] += quante
        self.funzioni.update(a.funzioni)
        self.filtri.update(a.filtri)
        for classe, valore in a.testi:
            self.testi[classe, valore] += 1

    def testo(self, valore: str, posizione: str) -> None:
        """Un testo costante di una configurazione (non un modello)."""
        classe, trovati = self.analizzatore.classifica(valore)
        if classe == "altro":
            return
        for entita in trovati:
            self.costanti[entita, posizione, "costante nella configurazione"] += 1
        if classe != "id":
            self.testi[classe, valore] += 1

    def valore(self, valore: Any, posizione: str, luogo: str) -> None:
        """Tutti i modelli e i testi dentro un valore validato."""
        if isinstance(valore, Template):
            self.modello(valore, posizione, luogo)
        elif isinstance(valore, ScriptVariables):
            self.valore(valore.as_dict(), posizione, luogo)
        elif isinstance(valore, str):
            self.testo(valore, posizione)
        elif isinstance(valore, Mapping):
            for chiave, sotto in valore.items():
                self.valore(chiave, posizione, f"{luogo}.{chiave}")
                self.valore(sotto, posizione, f"{luogo}.{chiave}")
        elif isinstance(valore, (list, tuple)):
            for indice, sotto in enumerate(valore):
                self.valore(sotto, posizione, f"{luogo}[{indice}]")
        elif not (
            valore is None or isinstance(valore, (bool, int, float, timedelta, time))
        ):
            raise Sconosciuto(f"valore {type(valore).__name__} in {luogo}")

    # --- i trigger ---------------------------------------------------------------------------

    def trigger_di(self, trigger: Mapping[str, Any], nome: str, indice: int) -> None:
        trigger = dict(trigger)
        piattaforma = trigger.pop("platform")
        luogo = f"{nome} > trigger {indice}"
        self.trigger[piattaforma] += 1
        identita = str(trigger.pop("id", ""))
        trigger.pop("alias", None)
        if trigger.pop("enabled", True) is not True:
            raise Sconosciuto(f"trigger spento: {luogo}")
        if trigger.pop("variables", None):
            raise Sconosciuto(f"trigger con variables: {luogo}")
        if piattaforma == "state":
            chiavi = ("from", "to", "not_from", "not_to", "for", "attribute")
            filtri = _filtri(trigger, chiavi)
            self.valore(trigger.get("for"), "trigger (for)", luogo)
            for entita in trigger.pop("entity_id"):
                self.trigger_stato[entita, filtri] += 1
            for chiave in chiavi:
                trigger.pop(chiave, None)
        elif piattaforma == "template":
            self.modello(trigger.pop("value_template"), "trigger", luogo)
            durata = trigger.pop("for", None)
            self.valore(durata, "trigger (for)", luogo)
            self.trigger[
                "template con for" if durata is not None else "template senza for"
            ] += 1
        elif piattaforma == "event":
            tipi = [t.template for t in trigger.pop("event_type")]
            dati = trigger.pop("event_data", {})
            contesto = trigger.pop("context", {})
            self.valore(dati, "trigger (evento)", luogo)
            self.eventi.append(
                (
                    nome,
                    indice,
                    identita,
                    ", ".join(tipi),
                    _piatto(dati),
                    _piatto(contesto),
                )
            )
        elif piattaforma == "time":
            for quando in trigger.pop("at"):
                if isinstance(quando, str):
                    self.trigger_ora[quando] += 1
                elif not isinstance(quando, time):
                    raise Sconosciuto(f"trigger time at {quando!r}")
        elif piattaforma == "time_pattern":
            for chiave in ("hours", "minutes", "seconds"):
                trigger.pop(chiave, None)
        elif piattaforma == "homeassistant":
            trigger.pop("event")
        else:
            raise Sconosciuto(f"trigger {piattaforma}")
        if trigger:
            raise Sconosciuto(f"trigger {piattaforma} con {sorted(trigger)}: {luogo}")

    # --- le condizioni ---------------------------------------------------------------------

    def condizione(self, config: Mapping[str, Any], luogo: str) -> None:
        tipo = config["condition"]
        self.condizioni[tipo] += 1
        noti = {"condition", "alias", "enabled"}
        if tipo == "template":
            self.modello(config["value_template"], "condizione", luogo)
            noti |= {"value_template"}
        elif tipo in ("and", "or", "not"):
            for indice, sotto in enumerate(config["conditions"]):
                self.condizione(sotto, f"{luogo} > {tipo} {indice}")
            noti |= {"conditions"}
        elif tipo == "state":
            filtri = _filtri(config, ("state", "for", "attribute", "match"))
            self.valore(config.get("for"), "condizione (for)", luogo)
            for entita in config["entity_id"]:
                self.condizioni_stato[entita, filtri] += 1
            noti |= {"entity_id", "state", "for", "attribute", "match"}
        elif tipo == "trigger":
            noti |= {"id"}
        else:
            raise Sconosciuto(f"condizione {tipo}: {luogo}")
        if altre := set(config) - noti:
            raise Sconosciuto(f"condizione {tipo} con {sorted(altre)}: {luogo}")

    # --- le azioni -------------------------------------------------------------------------

    def sequenza(self, azioni: Iterable[Mapping[str, Any]], luogo: str) -> None:
        for indice, azione in enumerate(azioni):
            self.azione(azione, f"{luogo} > {indice}")

    def azione(self, azione: Mapping[str, Any], luogo: str) -> None:
        azione = dict(azione)
        if azione.pop("enabled", True) is not True:
            raise Sconosciuto(f"azione spenta: {luogo}")
        for chiave in ("alias", "continue_on_error", "metadata"):
            azione.pop(chiave, None)
        if "delay" in azione:
            self.azioni["delay"] += 1
            self.valore(azione.pop("delay"), "pausa", luogo)
        elif "wait_template" in azione:
            self.azioni["wait_template"] += 1
            self.modello(azione.pop("wait_template"), "attesa", luogo)
            self.valore(azione.pop("timeout", None), "attesa (timeout)", luogo)
            azione.pop("continue_on_timeout", None)
        elif "condition" in azione:
            self.azioni["condition"] += 1
            self.condizione(azione, luogo)
            azione.clear()
        elif "repeat" in azione:
            ripeti = dict(azione.pop("repeat"))
            self.sequenza(ripeti.pop("sequence"), f"{luogo} repeat")
            for chiave in ("until", "while"):
                if chiave in ripeti:
                    self.azioni[f"repeat {chiave}"] += 1
                    for indice, sotto in enumerate(ripeti.pop(chiave)):
                        self.condizione(sotto, f"{luogo} repeat {chiave} {indice}")
            for chiave in ("count", "for_each"):
                if chiave in ripeti:
                    self.azioni[f"repeat {chiave}"] += 1
                    self.valore(ripeti.pop(chiave), f"ripetizione ({chiave})", luogo)
            if ripeti:
                raise Sconosciuto(f"repeat con {sorted(ripeti)}: {luogo}")
        elif "choose" in azione:
            self.azioni["choose"] += 1
            for indice, scelta in enumerate(azione.pop("choose")):
                for posto, sotto in enumerate(scelta["conditions"]):
                    self.condizione(
                        sotto, f"{luogo} choose {indice} condizione {posto}"
                    )
                self.sequenza(scelta["sequence"], f"{luogo} choose {indice}")
            if (predefinito := azione.pop("default", None)) is not None:
                self.sequenza(predefinito, f"{luogo} default")
        elif "if" in azione:
            self.azioni["if"] += 1
            for posto, sotto in enumerate(azione.pop("if")):
                self.condizione(sotto, f"{luogo} if condizione {posto}")
            self.sequenza(azione.pop("then"), f"{luogo} then")
            if (altrimenti := azione.pop("else", None)) is not None:
                self.sequenza(altrimenti, f"{luogo} else")
        elif "variables" in azione:
            self.azioni["variables"] += 1
            self.valore(azione.pop("variables"), "variabili", luogo)
        elif "action" in azione:
            self.azioni["action"] += 1
            self.chiamata(azione, luogo)
        elif "stop" in azione:
            self.azioni["stop"] += 1
            self.valore(azione.pop("stop"), "stop", luogo)
            azione.pop("error", None)
        elif "sequence" in azione:
            self.azioni["sequence"] += 1
            self.sequenza(azione.pop("sequence"), f"{luogo} sequence")
        if azione:
            raise Sconosciuto(f"azione con {sorted(azione)}: {luogo}")

    def chiamata(self, azione: dict[str, Any], luogo: str) -> None:
        """Una chiamata di servizio: il nome, i bersagli, i dati."""
        nome = azione.pop("action")
        dati = azione.pop("data", {})
        bersaglio = azione.pop("target", {})
        azione.pop("response_variable", None)
        if isinstance(nome, Template):
            self.modello(nome, "nome del servizio", luogo)
            self.dinamici.append(
                (
                    "uso",
                    f"nome del servizio: {self._origine(nome)}",
                    "nome del servizio",
                    _corto(nome.template),
                    luogo,
                )
            )
            servizio = "<modello>"
        else:
            servizio = nome
        self.servizi[servizio] += 1
        if not isinstance(dati, Mapping) or not isinstance(bersaglio, Mapping):
            raise Sconosciuto(f"dati o bersaglio non dizionario: {luogo}")
        if altre := set(bersaglio) - {"entity_id"}:
            raise Sconosciuto(f"bersaglio con {sorted(altre)}: {luogo}")
        dettaglio = _dettaglio_dati(dati)
        origini = [
            ("target.entity_id", bersaglio.get("entity_id")),
            ("entity_id", azione.pop("entity_id", None)),
            ("data.entity_id", dati.get("entity_id")),
        ]
        for origine, valore in origini:
            if valore is None:
                continue
            for voce in valore if isinstance(valore, (list, tuple)) else [valore]:
                if isinstance(voce, Template) and not voce.is_static:
                    self.modello(voce, "bersaglio del servizio", luogo)
                    self.dinamici.append(
                        (
                            "uso",
                            f"bersaglio di {servizio} [{dettaglio}]: "
                            + self._origine(voce),
                            "bersaglio del servizio",
                            _corto(voce.template),
                            luogo,
                        )
                    )
                    continue
                testo_voce = voce.template if isinstance(voce, Template) else voce
                for entita in [e.strip() for e in testo_voce.split(",")]:
                    self.scritture[entita, servizio, dettaglio, origine] += 1
        dominio, _, oggetto = servizio.partition(".")
        if dominio == "shell_command" or (
            dominio == "script" and f"script.{oggetto}" in self.entita
        ):
            # chiamata diretta: il servizio È la voce
            diretta = f"{dominio}.<nome> (chiamata diretta)"
            self.scritture[servizio, diretta, dettaglio, "nome"] += 1
        # i modelli e i testi dei dati (entity_id a parte, già contato)
        for chiave, valore in dati.items():
            if chiave != "entity_id":
                self.valore(valore, "dati del servizio", f"{luogo} dati.{chiave}")

    def _origine(self, modello: Template) -> str:
        """Da dove viene il nome che un modello rende (per un bersaglio o un servizio)."""
        a = self.analizzatore.analizza(modello.template)
        if a.costruiti and a.costanti:
            return "scelta fra entity_id costanti e un nome composto"
        if a.costruiti:
            return "nome composto (inizio costante + pezzo calcolato)"
        if a.costanti:
            return "scelta fra entity_id costanti"
        if a.letture:
            return "nome letto dallo stato di un'altra entità"
        return "nome in una variabile"

    # --- automazioni e script -------------------------------------------------------------

    def automazione(self, config: Mapping[str, Any], posto: int) -> None:
        nome = f"automazione «{config.get('alias') or f'automation {posto}'}»"
        for indice, trigger in enumerate(config["triggers"]):
            self.trigger_di(trigger, nome, indice)
        for indice, condizione in enumerate(config.get("conditions") or []):
            self.condizione(condizione, f"{nome} > condizione {indice}")
        if config.get("variables"):
            self.valore(config["variables"], "variabili", f"{nome} > variabili")
        if config.get("trigger_variables"):
            raise Sconosciuto(f"{nome}: trigger_variables")
        self.sequenza(config["actions"], nome)

    def script(self, chiave: str, config: Mapping[str, Any]) -> None:
        nome = f"script {chiave}"
        if config.get("variables"):
            self.valore(config["variables"], "variabili", f"{nome} > variabili")
        self.sequenza(config["sequence"], nome)


def _filtri(config: Mapping[str, Any], chiavi: tuple[str, ...]) -> str:
    parti = []
    for chiave in chiavi:
        if chiave not in config or config[chiave] is None:
            continue
        valore = config[chiave]
        if chiave == "match" and valore == "all":
            continue
        if isinstance(valore, (Template, Mapping)):
            valore = f"modello {_corto(_piatto(valore), 90)}"
        elif isinstance(valore, timedelta):
            valore = f"{valore.total_seconds():g} s"
        elif isinstance(valore, list):
            valore = "|".join(str(v) for v in valore)
        parti.append(f"{chiave}={valore}")
    return ", ".join(parti) or "(qualsiasi cambio)"


def _piatto(valore: Any) -> str:
    """Un dizionario validato come testo breve (i modelli con il loro testo)."""
    if isinstance(valore, Template):
        return valore.template
    if isinstance(valore, Mapping):
        return "{" + ", ".join(f"{k}: {_piatto(v)}" for k, v in valore.items()) + "}"
    if isinstance(valore, (list, tuple)):
        return "[" + ", ".join(_piatto(v) for v in valore) + "]"
    return str(valore)


def _dettaglio_dati(dati: Mapping[str, Any]) -> str:
    """Le chiavi dei dati di una chiamata (entity_id a parte): costante o modello."""
    parti = []
    for chiave in sorted(dati):
        if chiave == "entity_id":
            continue
        valore = dati[chiave]
        if isinstance(valore, Template) and not valore.is_static:
            parti.append(f"{chiave}=<modello>")
        elif isinstance(valore, (Mapping, list)):
            parti.append(f"{chiave}=<struttura>")
        else:
            parti.append(f"{chiave}=<costante>")
    return ", ".join(parti) or "(senza dati)"


async def inventario(hass: HomeAssistant) -> Inventario:
    """L'inventario del package, dalle configurazioni validate da Home Assistant."""
    sezioni = leggi_sezioni()
    entita = catalogo(sezioni)
    inv = Inventario(entita, Analizzatore(entita))
    inv.timer = {f"timer.{k}": dict(v or {}) for k, v in sezioni["timer"].items()}
    automazioni, script = leggi_package()
    for posto, config in enumerate(automazioni):
        # l'entità dell'automazione prende il nome dall'alias
        entita[f"automation.{slugify(config['alias'])}"] = "automation"
    for posto, config in enumerate(automazioni):
        validata = await valida_automazione(hass, "automation", config)
        if validata is None or getattr(validata, "validation_status", "ok") != "ok":
            raise Sconosciuto(f"automazione non valida: {config.get('alias')}")
        inv.automazione(validata, posto)
    for chiave, config in script.items():
        validato = await valida_script(hass, chiave, config)
        if validato is None or getattr(validato, "validation_status", "ok") != "ok":
            raise Sconosciuto(f"script non valido: {chiave}")
        inv.script(chiave, validato)
    return inv


# --- le uscite ------------------------------------------------------------------------------

AZIONI = "azioni"
GRUPPI = {
    "trigger": "trigger",
    "trigger (for)": "trigger (for)",
    "condizione": "condizione",
    "attesa": "attesa",
}
"""Posizione di un modello -> gruppo; tutte le altre posizioni sono «azioni» (variabili,
dati, bersagli e nomi dei servizi, ripetizioni)."""


def classe_domani(domani: str) -> str:
    """Il dominio di domani («interna» per lo stato del motore)."""
    return domani.split(".", 1)[0] if "." in domani else "interna"


def candidati(
    inv: Inventario, prefisso: str, suffisso: str, valori: tuple[str, ...] | None
) -> tuple[list[str], bool]:
    """Le entità che un nome composto può indicare, e se l'elenco è esatto.

    Esatto quando il pezzo calcolato è scelto fra costanti (``{...}[x]``, ``[...][x]``);
    altrimenti sono tutte le entità del package con quell'inizio e quella fine.
    """
    if valori is not None:
        return [f"{prefisso}{valore}{suffisso}" for valore in valori], True
    minimo = len(prefisso) + len(suffisso)
    return (
        sorted(
            e
            for e in inv.entita
            if e.startswith(prefisso) and e.endswith(suffisso) and len(e) > minimo
        ),
        False,
    )


def _conta(voci: Mapping[str, int] | Counter[str]) -> str:
    """``nome=3; altro=1`` in ordine di nome."""
    return "; ".join(f"{nome}={quante}" for nome, quante in sorted(voci.items()))


def _csv(colonne: list[str], righe: Iterable[Mapping[str, Any]]) -> str:
    uscita = io.StringIO()
    scrittore = csv.DictWriter(
        uscita, fieldnames=colonne, delimiter=";", lineterminator="\n"
    )
    scrittore.writeheader()
    scrittore.writerows(righe)
    return uscita.getvalue()


@dataclass
class Scheda:
    """I conti di un'entità."""

    letture: Counter[str] = field(default_factory=Counter)  # per tipo
    gruppi: Counter[str] = field(default_factory=Counter)  # per gruppo di posizione
    attributi: Counter[str] = field(default_factory=Counter)
    oggetto: Counter[str] = field(default_factory=Counter)  # states.d.o: cosa si legge
    usi: Counter[str] = field(default_factory=Counter)
    valori: Counter[str] = field(default_factory=Counter)  # is_state(.., valore)
    trigger_stato: Counter[str] = field(default_factory=Counter)
    condizioni_stato: Counter[str] = field(default_factory=Counter)
    servizi: Counter[str] = field(default_factory=Counter)
    dati: Counter[str] = field(default_factory=Counter)
    costanti: Counter[str] = field(default_factory=Counter)
    istanti: Counter[str] = field(default_factory=Counter)
    composti: int = 0
    eventi: int = 0

    @property
    def toccata(self) -> bool:
        return bool(
            self.letture
            or self.trigger_stato
            or self.condizioni_stato
            or self.servizi
            or self.costanti
            or self.composti
            or self.eventi
        )


def schede(inv: Inventario) -> dict[str, Scheda]:
    """I conti per entità (anche quelle che non sono aiutanti)."""
    uscita: dict[str, Scheda] = defaultdict(Scheda)
    for (entita, posizione, tipo, dettaglio, uso), quante in inv.letture.items():
        scheda = uscita[entita]
        scheda.letture[tipo] += quante
        scheda.gruppi[GRUPPI.get(posizione, AZIONI)] += quante
        if tipo in ("state_attr()", "is_state_attr()"):
            scheda.attributi[dettaglio] += quante
        elif tipo in ("states.dominio.oggetto", "states[...]"):
            scheda.oggetto[dettaglio] += quante
        elif tipo == "is_state()":
            scheda.valori[dettaglio] += quante
        if tipo != "is_state()":
            scheda.usi[f"{tipo} {uso}"] += quante
    for (entita, filtri), quante in inv.trigger_stato.items():
        uscita[entita].trigger_stato[filtri] += quante
    for (entita, filtri), quante in inv.condizioni_stato.items():
        uscita[entita].condizioni_stato[filtri] += quante
    for (entita, servizio, dettaglio, _origine), quante in inv.scritture.items():
        uscita[entita].servizi[servizio] += quante
        uscita[entita].dati[f"{servizio} [{dettaglio}]"] += quante
    for (entita, posizione, dove), quante in inv.costanti.items():
        uscita[entita].costanti[f"{posizione}: {dove}"] += quante
    for tipo, _posizione, _testo, entita, _luogo in inv.contesto:
        if entita:
            uscita[entita].istanti[tipo] += 1
    for (_testo, prefisso, suffisso, valori), quante in inv.costruiti.items():
        for entita in candidati(inv, prefisso, suffisso, valori)[0]:
            uscita[entita].composti += quante
    for _nome, _indice, _id, tipi, dati, _contesto in inv.eventi:
        if tipi == "call_service":
            dominio = re.search(r"domain: (\w+)", dati)
            servizio = re.search(r"service: (\w+)", dati)
            if dominio and servizio:
                uscita[f"{dominio.group(1)}.{servizio.group(1)}"].eventi += 1
    return uscita


COLONNE_ENTITA = [
    "entita",
    "tipo_oggi",
    "domani",
    "uso_nella_scheda",
    "dopo_un_riavvio",
    "letture",
    "states()",
    "is_state()",
    "state_attr()",
    "attributi_letti",
    "states.dominio.oggetto",
    "oggetto_cosa_si_legge",
    "altre_funzioni",
    "letture_nei_trigger",
    "letture_nei_for_dei_trigger",
    "letture_nelle_condizioni",
    "letture_nelle_attese",
    "letture_nelle_azioni",
    "trigger_di_stato",
    "trigger_di_stato_filtri",
    "trigger_a_modello_che_la_leggono",
    "attese_che_la_leggono",
    "condizioni_di_stato",
    "condizioni_di_stato_filtri",
    "condizioni_a_modello_che_la_leggono",
    "servizi_chiamati",
    "servizi",
    "servizi_con_i_dati",
    "id_costante_altrove",
    "id_costante_dove",
    "nomi_composti_che_possono_indicarla",
    "trigger_a_evento_che_la_guardano",
    "valori_di_is_state",
    "usi_del_valore",
    "istanti_letti",
]


def righe_entita(
    inv: Inventario, fase1: Mapping[str, Mapping[str, str]]
) -> list[dict[str, Any]]:
    """Una riga per ognuna delle 342 voci «da aiutante», nell'ordine della fase 1."""
    tutte = schede(inv)
    righe = []
    for entita, riga in fase1.items():
        s = tutte.get(entita, Scheda())
        altre = {
            tipo: quante
            for tipo, quante in s.letture.items()
            if tipo
            not in ("states()", "is_state()", "state_attr()", "states.dominio.oggetto")
        }
        righe.append(
            {
                "entita": entita,
                "tipo_oggi": riga["Tipo oggi"],
                "domani": riga["Domani"],
                "uso_nella_scheda": riga["Uso nella scheda"],
                "dopo_un_riavvio": riga["Dopo un riavvio"],
                "letture": sum(s.letture.values()),
                "states()": s.letture["states()"],
                "is_state()": s.letture["is_state()"],
                "state_attr()": s.letture["state_attr()"],
                "attributi_letti": _conta(s.attributi),
                "states.dominio.oggetto": s.letture["states.dominio.oggetto"],
                "oggetto_cosa_si_legge": _conta(s.oggetto),
                "altre_funzioni": _conta(altre),
                "letture_nei_trigger": s.gruppi["trigger"],
                "letture_nei_for_dei_trigger": s.gruppi["trigger (for)"],
                "letture_nelle_condizioni": s.gruppi["condizione"],
                "letture_nelle_attese": s.gruppi["attesa"],
                "letture_nelle_azioni": s.gruppi[AZIONI],
                "trigger_di_stato": sum(s.trigger_stato.values()),
                "trigger_di_stato_filtri": _conta(s.trigger_stato),
                "trigger_a_modello_che_la_leggono": len(
                    inv.trigger_modello.get(entita, ())
                ),
                "attese_che_la_leggono": len(inv.attese_modello.get(entita, ())),
                "condizioni_di_stato": sum(s.condizioni_stato.values()),
                "condizioni_di_stato_filtri": _conta(s.condizioni_stato),
                "condizioni_a_modello_che_la_leggono": len(
                    inv.condizioni_modello.get(entita, ())
                ),
                "servizi_chiamati": sum(s.servizi.values()),
                "servizi": _conta(s.servizi),
                "servizi_con_i_dati": _conta(s.dati),
                "id_costante_altrove": sum(s.costanti.values()),
                "id_costante_dove": _conta(s.costanti),
                "nomi_composti_che_possono_indicarla": s.composti,
                "trigger_a_evento_che_la_guardano": s.eventi,
                "valori_di_is_state": _conta(s.valori),
                "usi_del_valore": _conta(s.usi),
                "istanti_letti": _conta(s.istanti),
            }
        )
    return righe


def righe_dinamici(
    inv: Inventario, fase1: Mapping[str, Mapping[str, str]]
) -> list[dict[str, Any]]:
    """Una riga per ogni caso dinamico distinto, con tutti i luoghi."""
    luoghi: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    for classe, tipo, posizione, espressione, luogo in inv.dinamici:
        luoghi[classe, tipo, posizione, espressione].append(luogo)
    composti = {
        espressione: (prefisso, suffisso, valori)
        for (espressione, prefisso, suffisso, valori) in inv.costruiti
    }
    righe = []
    for (classe, tipo, posizione, espressione), dove in sorted(luoghi.items()):
        riga = {
            "classe": classe,
            "tipo": tipo,
            "posizione": posizione,
            "espressione": espressione,
            "occorrenze": len(dove),
            "entita_possibili": "",
            "elenco_esatto": "",
            "domani_delle_possibili": "",
            "luoghi": " | ".join(dove),
        }
        if espressione in composti:
            possibili, esatto = candidati(inv, *composti[espressione])
            domani = Counter(
                classe_domani(fase1[e]["Domani"]) if e in fase1 else "NON ESISTE"
                for e in possibili
            )
            riga["entita_possibili"] = len(possibili)
            riga["elenco_esatto"] = (
                "sì" if esatto else "no (stesso inizio e stessa fine)"
            )
            riga["domani_delle_possibili"] = _conta(domani)
        righe.append(riga)
    return righe


COLONNE_DINAMICI = [
    "classe",
    "tipo",
    "posizione",
    "espressione",
    "occorrenze",
    "entita_possibili",
    "elenco_esatto",
    "domani_delle_possibili",
    "luoghi",
]
COLONNE_CONTESTO = [
    "tipo",
    "posizione",
    "espressione",
    "entita",
    "occorrenze",
    "luoghi",
]
COLONNE_EVENTI = [
    "automazione",
    "trigger",
    "id",
    "evento",
    "dati_evento",
    "contesto",
    "dominio",
    "servizio",
    "entita_guardata",
]


def righe_contesto(inv: Inventario) -> list[dict[str, Any]]:
    luoghi: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    for tipo, posizione, espressione, entita, luogo in inv.contesto:
        luoghi[tipo, posizione, espressione, entita].append(luogo)
    return [
        {
            "tipo": tipo,
            "posizione": posizione,
            "espressione": espressione,
            "entita": entita,
            "occorrenze": len(dove),
            "luoghi": " | ".join(dove),
        }
        for (tipo, posizione, espressione, entita), dove in sorted(luoghi.items())
    ]


def righe_eventi(inv: Inventario) -> list[dict[str, Any]]:
    righe = []
    for nome, indice, identita, tipi, dati, contesto in inv.eventi:
        dominio = re.search(r"domain: (\w+)", dati)
        servizio = re.search(r"service: (\w+)", dati)
        entita = re.search(r"entity_id: ([\w.]+)", dati)
        righe.append(
            {
                "automazione": nome,
                "trigger": indice,
                "id": identita,
                "evento": tipi,
                "dati_evento": dati,
                "contesto": contesto,
                "dominio": dominio.group(1) if dominio else "",
                "servizio": servizio.group(1) if servizio else "",
                "entita_guardata": entita.group(1) if entita else "(nessuna: tutte)",
            }
        )
    return righe


def totali(inv: Inventario, fase1: Mapping[str, Mapping[str, str]]) -> str:
    """I totali dell'inventario, come testo."""
    tutte = schede(inv)
    r: list[str] = []

    def titolo(testo_titolo: str) -> None:
        r.extend(["", testo_titolo, "-" * len(testo_titolo)])

    def tabella(voci: Mapping[Any, int], rientro: str = "  ") -> None:
        for nome, quante in sorted(voci.items(), key=lambda v: (-v[1], str(v[0]))):
            r.append(f"{rientro}{quante:>6}  {nome}")

    r.append("INVENTARIO DEGLI AIUTANTI DEL PACKAGE (fase 4) - totali")
    titolo("Le voci")
    tipi = Counter(
        (riga["Tipo oggi"], classe_domani(riga["Domani"])) for riga in fase1.values()
    )
    r.append(f"  {len(fase1)} voci «da aiutante» (oggi -> domani):")
    tabella({f"{oggi} -> {domani}": n for (oggi, domani), n in tipi.items()})
    mai = sorted(e for e in fase1 if not tutte.get(e, Scheda()).toccata)
    r.append(f"  mai toccate da automazioni e script: {len(mai)}")
    for entita in mai:
        r.append(f"          {entita} -> {fase1[entita]['Domani']}")

    titolo("Automazioni e script validati")
    r.append(f"  trigger: {sum(n for k, n in inv.trigger.items() if ' ' not in k)}")
    tabella(inv.trigger)
    r.append(f"  condizioni: {sum(inv.condizioni.values())}")
    tabella(inv.condizioni)
    r.append(f"  azioni: {sum(inv.azioni.values())}")
    tabella(inv.azioni)
    r.append(
        f"  modelli: {sum(inv.modelli.values())} in tutto, {len(inv.posti)} testi distinti"
    )
    tabella(inv.modelli)
    r.append("  funzioni chiamate nei modelli:")
    tabella(inv.funzioni)

    titolo("Letture nei modelli (entity_id costante)")
    per_tipo: Counter[str] = Counter()
    per_posizione: Counter[str] = Counter()
    per_dominio: Counter[str] = Counter()
    for (entita, posizione, tipo, _dettaglio, _uso), quante in inv.letture.items():
        per_tipo[tipo] += quante
        per_posizione[posizione] += quante
        chi = (
            f"aiutanti: {fase1[entita]['Tipo oggi']}"
            if entita in fase1
            else f"altre entità del package: {inv.entita[entita]}"
            if entita in inv.entita
            else f"fuori dal package: {entita}"
        )
        per_dominio[chi] += quante
    r.append(f"  totale: {sum(per_tipo.values())}")
    r.append("  per tipo di lettura:")
    tabella(per_tipo, "    ")
    r.append("  per posizione del modello:")
    tabella(per_posizione, "    ")
    r.append("  per entità letta:")
    tabella(per_dominio, "    ")

    titolo("Per tipo di oggi e dominio di domani")
    gruppi: dict[tuple[str, str], list[str]] = defaultdict(list)
    for entita, riga in fase1.items():
        gruppi[riga["Tipo oggi"], classe_domani(riga["Domani"])].append(entita)
    for (oggi, domani), entita_gruppo in sorted(gruppi.items()):
        r.append(f"  {oggi} -> {domani}: {len(entita_gruppo)} voci")
        somma = Scheda()
        con: Counter[str] = Counter()
        trigger_modello: set[str] = set()
        condizioni_modello: set[str] = set()
        attese: set[str] = set()
        for entita in entita_gruppo:
            s = tutte.get(entita, Scheda())
            for campo in (
                "letture", "gruppi", "attributi", "oggetto", "valori", "trigger_stato",
                "condizioni_stato", "servizi", "dati", "costanti", "istanti", "usi",
            ):  # fmt: skip
                getattr(somma, campo).update(getattr(s, campo))
            somma.composti += s.composti
            somma.eventi += s.eventi
            con["lette in un modello"] += bool(s.letture)
            con["soggetto di un trigger di stato"] += bool(s.trigger_stato)
            con["lette da un trigger a modello"] += bool(
                inv.trigger_modello.get(entita)
            )
            con["in un trigger (di stato o a modello)"] += bool(
                s.trigger_stato or inv.trigger_modello.get(entita)
            )
            con["lette da un'attesa (wait_template)"] += bool(
                inv.attese_modello.get(entita)
            )
            con["in una condizione di stato"] += bool(s.condizioni_stato)
            con["lette da una condizione a modello"] += bool(
                inv.condizioni_modello.get(entita)
            )
            con["scritte da un servizio"] += bool(s.servizi)
            con["id costante altrove"] += bool(s.costanti)
            con["indicabili da un nome composto"] += bool(s.composti)
            con["mai toccate"] += not s.toccata
            trigger_modello |= inv.trigger_modello.get(entita, set())
            condizioni_modello |= inv.condizioni_modello.get(entita, set())
            attese |= inv.attese_modello.get(entita, set())
        r.append("    voci:")
        for nome, quante in con.items():
            r.append(f"      {quante:>6}  {nome}")
        r.append(
            f"    letture: {sum(somma.letture.values())}  ({_conta(somma.letture)})"
        )
        r.append(f"      per posizione: {_conta(somma.gruppi)}")
        if somma.attributi:
            r.append(f"      attributi (state_attr): {_conta(somma.attributi)}")
        if somma.oggetto:
            r.append(f"      states.dominio.oggetto: {_conta(somma.oggetto)}")
        if somma.valori:
            r.append(f"      valori di is_state: {_conta(somma.valori)}")
        if somma.usi:
            r.append("      usi del valore letto:")
            tabella(somma.usi, "        ")
        r.append(
            f"    trigger di stato: {sum(somma.trigger_stato.values())}"
            + (f"  ({_conta(somma.trigger_stato)})" if somma.trigger_stato else "")
        )
        r.append(f"    trigger a modello che le leggono: {len(trigger_modello)}")
        r.append(f"    attese che le leggono: {len(attese)}")
        r.append(
            f"    condizioni di stato: {sum(somma.condizioni_stato.values())}"
            + (
                f"  ({_conta(somma.condizioni_stato)})"
                if somma.condizioni_stato
                else ""
            )
        )
        r.append(f"    condizioni a modello che le leggono: {len(condizioni_modello)}")
        r.append(f"    servizi chiamati: {sum(somma.servizi.values())}")
        etichette: Counter[str] = Counter()
        for nome, quante in somma.dati.items():
            # le chiamate dirette hanno il nome della voce: si contano insieme
            etichette[re.sub(r"^(script|shell_command)\.vmc_\w+ ", "", nome)] += quante
        tabella(etichette, "      ")
        if somma.costanti:
            r.append(f"    id costante altrove: {sum(somma.costanti.values())}")
            tabella(somma.costanti, "      ")
        if somma.composti:
            r.append(f"    nomi composti che possono indicarle: {somma.composti}")
        if somma.eventi:
            r.append(f"    trigger a evento che le guardano: {somma.eventi}")
        if somma.istanti:
            r.append(f"    istanti letti: {_conta(somma.istanti)}")

    titolo("Servizi chiamati (tutte le chiamate, anche fuori dagli aiutanti)")
    servizi: Counter[str] = Counter()
    for nome, quante in inv.servizi.items():
        dominio, _, oggetto = nome.partition(".")
        diretta = dominio == "shell_command" or f"script.{oggetto}" in inv.entita
        servizi[f"{dominio}.<nome> (chiamata diretta)" if diretta else nome] += quante
    r.append(f"  chiamate: {sum(servizi.values())}")
    tabella(servizi)
    r.append(
        "  entità colpite (entity_id costante), per servizio e dominio dell'entità:"
    )
    colpite: Counter[str] = Counter()
    for (entita, servizio, _dettaglio, origine), quante in inv.scritture.items():
        if origine == "nome":
            continue
        colpite[f"{servizio} su {entita.split('.', 1)[0]} ({origine})"] += quante
    tabella(colpite, "    ")

    titolo("Entity_id e nomi di servizio dinamici")
    classi = Counter(d[0] for d in inv.dinamici)
    r.append(
        "  «uso»: un nome non costante dove si legge o si scrive; «costruzione»: il testo"
    )
    r.append(
        "  composto che lo forma (gli stessi casi visti da dentro: non si sommano agli"
    )
    r.append("  usi); «elenco»: entità trovate scorrendo gli stati.")
    for classe in ("uso", "costruzione", "elenco"):
        distinti = len({d[1:4] for d in inv.dinamici if d[0] == classe})
        r.append(f"  {classe}: {classi[classe]} occorrenze, {distinti} casi distinti")
        tabella(Counter(d[1] for d in inv.dinamici if d[0] == classe), "    ")
    r.append("  nomi composti (inizio costante + pezzo calcolato), per inizio:")
    per_inizio: dict[tuple[str, str], list[Any]] = {}
    for (_espressione, prefisso, suffisso, valori), quante in inv.costruiti.items():
        possibili, esatto = candidati(inv, prefisso, suffisso, valori)
        voce = per_inizio.setdefault((prefisso, suffisso), [0, set(), True])
        voce[0] += quante
        voce[1] |= set(possibili)
        voce[2] = voce[2] and esatto
    for (prefisso, suffisso), (quante, possibili, esatto) in sorted(per_inizio.items()):
        domani = Counter(
            classe_domani(fase1[e]["Domani"]) if e in fase1 else "NON ESISTE"
            for e in possibili
        )
        r.append(
            f"    {quante:>4}  {prefisso}…{suffisso}: {len(possibili)} entità possibili "
            f"({'elenco esatto' if esatto else 'stesso inizio e fine'}); domani: {_conta(domani)}"
        )
    r.append("  testi con «master» che non sono un entity_id intero, per classe:")
    tabella(Counter(classe for classe, _valore in inv.testi.elements()), "    ")
    r.append("  catene da trigger/this/repeat/wait/context:")
    catene: Counter[str] = Counter()
    for (catena, _posizione), quante in inv.radici.items():
        catene[catena] += quante
    tabella(catene, "    ")

    titolo("Contesto e istanti")
    tipi_contesto = Counter(c[0] for c in inv.contesto)
    r.append(f"  usi: {sum(tipi_contesto.values())}  ({_conta(tipi_contesto)})")
    forme: Counter[str] = Counter()
    soggetti: Counter[str] = Counter()
    for tipo, posizione, espressione, entita, _luogo in inv.contesto:
        forma = re.sub(
            r"^states\.\w+\.\w+\.", "states.<dominio>.<oggetto>.", espressione
        )
        forme[f"{tipo} in {posizione}: {_corto(forma, 80)}"] += 1
        soggetti[f"{tipo}: {entita or '(da trigger o da una variabile)'}"] += 1
    tabella(forme, "    ")
    r.append("  per entità:")
    tabella(soggetti, "    ")
    for nome in ("context", "this"):
        usi = sum(
            n for (catena, _p), n in inv.radici.items() if catena.split(".")[0] == nome
        )
        r.append(f"  variabile «{nome}»: {usi} usi")

    titolo("Trigger a evento")
    r.append(f"  {len(inv.eventi)} trigger a evento:")
    tabella(Counter(f"{e[3]} {e[4]}" for e in inv.eventi), "    ")
    tabella(Counter(f"{e[0]}: {e[3]}" for e in inv.eventi), "    ")

    titolo("Timer")
    r.append(f"  timer definiti: {len(inv.timer)}")
    r.append(
        f"    con duration: {sum('duration' in t for t in inv.timer.values())}; "
        f"con restore: {sum(bool(t.get('restore')) for t in inv.timer.values())}"
    )
    eventi_timer = [e for e in inv.eventi if e[3].startswith("timer.")]
    r.append(f"  trigger sugli eventi dei timer: {len(eventi_timer)}")
    for e in eventi_timer:
        r.append(f"    {e[0]} > trigger {e[1]}: {e[3]} dati {e[4]}")
    attributi: Counter[str] = Counter()
    stati: Counter[str] = Counter()
    servizi_timer: Counter[str] = Counter()
    for (entita, _posizione, tipo, dettaglio, _uso), quante in inv.letture.items():
        if entita.startswith("timer."):
            if tipo == "state_attr()":
                attributi[dettaglio] += quante
            elif tipo == "is_state()":
                stati[dettaglio] += quante
    for (entita, servizio, dettaglio, _origine), quante in inv.scritture.items():
        if servizio.startswith("timer."):
            servizi_timer[f"{servizio} [{dettaglio}]"] += quante
    r.append(
        f"  attributi letti con entity_id costante: {_conta(attributi) or 'nessuno'}"
    )
    r.append(
        f"  stati confrontati con is_state (costante): {_conta(stati) or 'nessuno'}"
    )
    r.append("  servizi con entity_id costante:")
    tabella(servizi_timer, "    ")
    r.append("  letture e servizi con il nome del timer non costante:")
    for classe, tipo, _posizione, espressione, _luogo in inv.dinamici:
        if classe == "uso" and "timer" in f"{tipo} {espressione}":
            r.append(f"    {tipo}: {_corto(espressione, 100)}")
    return "\n".join(r) + "\n"


def uscite(inv: Inventario) -> dict[str, str]:
    """I file dell'inventario (nome -> testo)."""
    fase1 = leggi_fase1()
    if set(fase1) != {e for e, tipo in inv.entita.items() if tipo in DOMINI_SIMILI}:
        raise Sconosciuto("le voci della fase 1 non sono quelle del package")
    return {
        "inventario_aiutanti.csv": _csv(COLONNE_ENTITA, righe_entita(inv, fase1)),
        "inventario_aiutanti_dinamici.csv": _csv(
            COLONNE_DINAMICI, righe_dinamici(inv, fase1)
        ),
        "inventario_aiutanti_contesto.csv": _csv(COLONNE_CONTESTO, righe_contesto(inv)),
        "inventario_aiutanti_eventi.csv": _csv(COLONNE_EVENTI, righe_eventi(inv)),
        "inventario_aiutanti_totali.txt": totali(inv, fase1),
    }


def _principale() -> None:
    import asyncio

    from pytest_homeassistant_custom_component.common import async_test_home_assistant

    async def corsa() -> Inventario:
        async with async_test_home_assistant() as hass:
            inv = await inventario(hass)
            await hass.async_stop(force=True)
        return inv

    testi = uscite(asyncio.run(corsa()))
    if "--scrivi" in sys.argv:
        for nome, contenuto in testi.items():
            (QUI / nome).write_text(contenuto, encoding="utf-8")
            print(f"scritto {QUI / nome}", file=sys.stderr)
    print(testi["inventario_aiutanti_totali.txt"])


if __name__ == "__main__":
    _principale()
