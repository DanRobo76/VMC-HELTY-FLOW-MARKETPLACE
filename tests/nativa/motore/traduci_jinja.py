"""Traduzione di un modello Jinja del package in una funzione Python.

Ogni modello diventa ``def mNNNN(c, V) -> str``: ``c`` è il contesto del motore
(``motore/contesto.py``), ``V`` le variabili viste dal modello (una variabile che non c'è
vale indefinito). Il codice usa le funzioni di ``motore/jinja.py`` (filtri, test,
attributi, uscita nel testo) e del contesto (``states``, ``is_state``, ``now``...).

Le regole di Jinja che contano sono tutte qui:

- gli ambiti delle variabili sono quelli del compilatore di Jinja: si usa la sua analisi
  (``jinja2.idtracking``) per sapere, in ogni ambito (il modello, il corpo di un ciclo
  ``for``, il corpo di un ``{% set x %}...{% endset %}``), da dove parte ogni variabile:
  dalle variabili del modello (``resolve``), dalla variabile dell'ambito esterno
  (``alias``, a ogni giro del ciclo) o da nessuna parte (``missing``, poi indefinita);
- ``{{ x }}`` scrive ``testo(x)`` (``str`` dopo ``finalize``), il testo fuori dai
  ``{{ }}`` resta com'è, ``a ~ b`` è ``concat(a, b)``;
- ``x.y`` e ``x[k]`` passano dalla sandbox di Jinja (``attributo``, ``elemento``), le
  chiamate di metodi anche (``chiama``); le funzioni globali del contesto si chiamano
  direttamente;
- i testi che contengono «master» passano da ``c.N`` (il nome di ogni VMC, come
  ``trasforma.rinomina`` sul package): anche i nomi che escono dal modello (variabili
  lette da ``V``, attributi, argomenti per nome, ``ns.attributo``), perché per un'altra
  VMC il package li ha rinominati come le chiavi delle variabili e degli stati; le
  variabili assegnate nel modello restano nomi Python (rinominarle non cambia nulla).
- ogni funzione ha in ``sorgente`` il testo del modello: ``Contesto.testo`` lo mette in
  ``template_cv`` durante la resa, come Home Assistant, per i messaggi d'errore (``float
  got invalid input ... when rendering template '<modello>' ...``).
"""

from __future__ import annotations

import math
import re
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

import jinja2
from jinja2 import nodes
from jinja2.idtracking import (
    VAR_LOAD_ALIAS,
    VAR_LOAD_PARAMETER,
    VAR_LOAD_RESOLVE,
    VAR_LOAD_UNDEFINED,
    Symbols,
)

from custom_components.vmc_master.nativa.motore import jinja as J

# L'ambiente per leggere i modelli: come quello di Home Assistant (stesse estensioni e
# impostazioni predefinite per gli spazi).
AMBIENTE = jinja2.Environment(extensions=["jinja2.ext.loopcontrols", "jinja2.ext.do"])

# Funzioni globali dei modelli che leggono Home Assistant: le dà il contesto.
GLOBALI_CONTESTO = {
    "states",
    "is_state",
    "state_attr",
    "now",
    "utcnow",
    "device_name",
    "entity_name",
    "integration_entities",
    "expand",
}
# Funzioni globali senza Home Assistant: le dà jinja.py.
GLOBALI_JINJA = {
    "strptime": "J.strptime",
    "as_timestamp": "J.as_timestamp",
    "as_datetime": "J.as_datetime",
    "namespace": "J.namespace",
    "timedelta": "J.timedelta",
    # le funzioni globali che in Home Assistant sono anche filtri (stessa funzione: estensioni
    # type_cast e math) e la costante «e» (math.e); le usano i sensori template del package
    "float": "J.f_float",
    "int": "J.f_int",
    "is_number": "J.f_is_number",
    "log": "J.log",
    "e": repr(math.e),
}
GLOBALI = GLOBALI_CONTESTO | set(GLOBALI_JINJA)

_PAROLE_NOME = re.compile("master|Master|MASTER")
OPERATORI = {
    "eq": "==",
    "ne": "!=",
    "gt": ">",
    "gteq": ">=",
    "lt": "<",
    "lteq": "<=",
    "in": "in",
    "notin": "not in",
}
BINARI = {
    nodes.Add: "+",
    nodes.Sub: "-",
    nodes.Mul: "*",
    nodes.Div: "/",
    nodes.FloorDiv: "//",
    nodes.Mod: "%",
    nodes.Pow: "**",
}


class NonTraducibile(Exception):
    """Un costrutto Jinja che il traduttore non conosce."""


# La mappa dei nomi della fase 4 (``rinomina.Rinomina``) durante una traduzione che la
# chiede (``traduci.traduzione(..., rinomina=...)``). Senza, come sempre, ogni testo
# resta quello del package.
RINOMINA: ContextVar[Any] = ContextVar("rinomina", default=None)


# Fase 4: i timer del package nel motore (``traduci.traduzione(..., timer_motore=True)``).
# Con il parametro, le letture che possono riguardare un timer passano dai timer del motore
# (``c.timer``, che lascia a Home Assistant tutto ciò che non è un suo timer); le altre
# letture di Home Assistant che possono riguardare un timer fermano la traduzione. Senza,
# come sempre.
TIMER_MOTORE: ContextVar[bool] = ContextVar("timer_motore", default=False)
# Le letture che i timer del motore sanno fare (funzioni globali, filtri e test): le
# stesse funzioni di Home Assistant per un timer del motore, quelle di Home Assistant per
# il resto.
GLOBALI_TIMER = {"states", "is_state", "state_attr"}
FILTRI_TIMER = {"states", "state_attr"}
TEST_TIMER = {"is_state"}
# Le altre letture degli stati di Home Assistant (estensione «state» dei modelli): con un
# timer del motore darebbero un altro risultato.
ALTRE_LETTURE = {
    "expand",
    "has_value",
    "is_state_attr",
    "closest",
    "distance",
    "state_translated",
    "state_attr_translated",
}


def forse_timer(nodo: nodes.Node | None) -> bool:
    """Il valore di ``nodo`` può essere l'entity_id di un timer? (Home Assistant cerca
    l'entity_id anche in minuscolo.) No solo per i testi fissi di un altro dominio e per
    i nomi composti che cominciano con un dominio diverso da ``timer``."""
    if isinstance(nodo, nodes.Const):
        valore = nodo.value
        if isinstance(valore, str):
            return valore.lower().startswith("timer.")
        if isinstance(valore, (list, tuple)):
            return any(forse_timer(nodes.Const(v)) for v in valore)
        return False
    if isinstance(nodo, (nodes.List, nodes.Tuple)):
        return any(forse_timer(v) for v in nodo.items)
    if isinstance(nodo, nodes.Concat) and nodo.nodes:
        return forse_timer_inizio(nodo.nodes[0])
    if isinstance(nodo, nodes.Add):
        return forse_timer_inizio(nodo.left)
    return True


# Funzioni globali che danno entity_id del registro delle entità (di un'integrazione, di
# un dispositivo...): i timer del motore non ci sono mai.
ELENCHI_REGISTRO = {
    "integration_entities",
    "device_entities",
    "area_entities",
    "label_entities",
    "floor_entities",
}
# Filtri che danno una parte degli elementi che ricevono.
FILTRI_PARTE = {
    "select",
    "reject",
    "selectattr",
    "rejectattr",
    "list",
    "unique",
    "sort",
    "reverse",
}


def forse_timer_tra(nodo: nodes.Node | None, globale: Any) -> bool:
    """Tra gli elementi del valore di ``nodo`` (una lista) può esserci l'entity_id di un
    timer? ``globale(nome)``: il nome è la funzione globale (non una variabile)."""
    if isinstance(nodo, nodes.Const):
        valore = nodo.value
        return isinstance(valore, (list, tuple)) and forse_timer(nodo)
    if isinstance(nodo, (nodes.List, nodes.Tuple)):
        return any(forse_timer(v) for v in nodo.items)
    if (
        isinstance(nodo, nodes.Call)
        and isinstance(nodo.node, nodes.Name)
        and nodo.node.name in ELENCHI_REGISTRO
        and globale(nodo.node.name)
    ):
        return False
    if isinstance(nodo, nodes.Filter) and nodo.name in FILTRI_PARTE:
        return forse_timer_tra(nodo.node, globale)
    return True


def forse_timer_inizio(nodo: nodes.Node) -> bool:
    """Un testo che comincia con il valore di ``nodo`` può essere l'entity_id di un
    timer?"""
    if isinstance(nodo, nodes.Const) and isinstance(nodo.value, str):
        inizio = nodo.value.lower()
        return inizio.startswith("timer.") or "timer.".startswith(inizio)
    if isinstance(nodo, nodes.Concat) and nodo.nodes:
        return forse_timer_inizio(nodo.nodes[0])
    return True


def testo_costante(valore: str) -> str:
    """Un testo del package nel codice: con «master» passa da ``c.N``."""
    if (mappa := RINOMINA.get()) is not None:
        valore = mappa.testo(valore)
    if _PAROLE_NOME.search(valore):
        return f"c.N({valore!r})"
    return repr(valore)


def costante(valore: Any) -> str:
    """Una costante Jinja (anche in liste, tuple, dizionari) nel codice."""
    if isinstance(valore, str):
        return testo_costante(valore)
    if isinstance(valore, tuple):
        return "(" + "".join(costante(v) + ", " for v in valore) + ")"
    if isinstance(valore, list):
        return "[" + ", ".join(costante(v) for v in valore) + "]"
    if isinstance(valore, dict):
        return (
            "{"
            + ", ".join(f"{costante(k)}: {costante(v)}" for k, v in valore.items())
            + "}"
        )
    if valore is None or isinstance(valore, (bool, int, float)):
        return repr(valore)
    raise NonTraducibile(f"costante {valore!r}")


@dataclass
class _Ambito:
    """Un ambito di Jinja (come Frame): i simboli e il nome Python di ogni variabile."""

    simboli: Symbols
    ciclo: bool = False


@dataclass
class Traduttore:
    """Traduce i modelli in funzioni; tiene le funzioni uguali una volta sola."""

    filtri_ha: set[str] = field(default_factory=set)
    test_ha: set[str] = field(default_factory=set)
    globali_ha: set[str] = field(default_factory=set)
    funzioni: dict[str, str] = field(default_factory=dict)  # sorgente -> nome
    codice: list[str] = field(default_factory=list)
    _righe: list[str] = field(default_factory=list)
    _rientro: int = 0
    _contatore: int = 0
    # variabili «resolve» già lette dal modello nel codice (``v_x = V.get('x', ...)``)
    _risolte: set[str] = field(default_factory=set)
    # con TIMER_MOTORE, i modelli che leggono dai timer del motore (``c.timer``): un trigger
    # o un'attesa non li seguono (Home Assistant non vede i timer del motore)
    instradati: set[str] = field(default_factory=set)
    _instradato: bool = False

    # --- interfaccia ---------------------------------------------------------------------

    def funzione(self, sorgente: str) -> str:
        """Il nome della funzione del modello ``sorgente`` (testo come nel package)."""
        testo = sorgente.strip()  # come Template.__init__
        if testo in self.funzioni:
            return self.funzioni[testo]
        nome = f"m{len(self.funzioni) + 1:04d}"
        albero = AMBIENTE.parse(testo)
        self._righe = []
        self._rientro = 0
        self._contatore = 0
        self._risolte = set()
        self._instradato = False
        self._scrivi(f"def {nome}(c, V):")
        self._rientro += 1
        self._scrivi(f"# {_documento(testo)}")
        ambito = _Ambito(Symbols(level=0))
        ambito.simboli.analyze_node(albero)
        self._entra(ambito)
        self._scrivi("_o = []")
        self._blocco(albero.body, ambito, "_o")
        self._scrivi("return ''.join(_o)")
        self._rientro -= 1
        # il testo del modello, per i messaggi d'errore (come ``template_cv``)
        self._righe.append(f"\n\n{nome}.sorgente = {testo!r}")
        self.codice.append("\n".join(self._righe))
        self.funzioni[testo] = nome
        if self._instradato:
            self.instradati.add(nome)
        return nome

    def _al_timer(self, codice: str) -> str:
        """Una lettura dai timer del motore."""
        self._instradato = True
        return codice

    # --- scrittura -----------------------------------------------------------------------

    def _scrivi(self, riga: str) -> None:
        self._righe.append("    " * self._rientro + riga)

    def _temporaneo(self, prefisso: str) -> str:
        self._contatore += 1
        return f"_{prefisso}{self._contatore}"

    # --- ambiti (come CodeGenerator.enter_frame) -----------------------------------------

    def _entra(self, ambito: _Ambito) -> None:
        indefinite = []
        for nome_py, (azione, parametro) in ambito.simboli.loads.items():
            if azione == VAR_LOAD_PARAMETER:
                continue
            if azione == VAR_LOAD_RESOLVE:
                # serve solo se la variabile si assegna (altrimenti si legge al suo posto)
                if _salvato(ambito.simboli, parametro):
                    self._scrivi(f"{_py(nome_py)} = {self._risolvi(parametro)}")
                    self._risolte.add(nome_py)
            elif azione == VAR_LOAD_ALIAS:
                esterna = ambito.simboli.parent and ambito.simboli.parent.find_load(
                    parametro
                )
                if (
                    esterna
                    and esterna[0] == VAR_LOAD_RESOLVE
                    and parametro not in self._risolte
                ):
                    # la variabile esterna non si assegna mai (si legge al suo posto):
                    # il suo valore è sempre quello del modello, come ``resolve``
                    self._scrivi(f"{_py(nome_py)} = {self._risolvi(esterna[1])}")
                else:
                    self._scrivi(f"{_py(nome_py)} = {_py(parametro)}")
            elif azione == VAR_LOAD_UNDEFINED:
                indefinite.append(_py(nome_py))
            else:  # pragma: no cover
                raise NonTraducibile(azione)
        if indefinite:
            self._scrivi(" = ".join(indefinite) + " = J.MANCANTE")

    def _controlla(self, nome: str) -> None:
        """Una funzione globale di Home Assistant che il traduttore non conosce non può
        diventare una variabile del modello."""
        if nome in self.globali_ha and nome not in GLOBALI:
            raise NonTraducibile(f"funzione globale {nome}")

    def _risolvi(self, nome: str) -> str:
        """Come context.resolve_or_missing: variabile del modello o funzione globale.

        Nessuna variabile del package ha il nome di una funzione globale (lo controlla
        ``traduci.py``): le funzioni globali si leggono direttamente.
        """
        self._controlla(nome)
        if nome in GLOBALI_CONTESTO:
            return f"c.{nome}"
        if nome in GLOBALI_JINJA:
            return GLOBALI_JINJA[nome]
        return f"V.get({testo_costante(nome)}, J.MANCANTE)"

    # --- istruzioni ----------------------------------------------------------------------

    def _blocco(self, corpo: list[nodes.Node], ambito: _Ambito, uscita: str) -> None:
        prima = len(self._righe)
        for nodo in corpo:
            self._istruzione(nodo, ambito, uscita)
        if len(self._righe) == prima:
            self._scrivi("pass")

    def _istruzione(self, nodo: nodes.Node, ambito: _Ambito, uscita: str) -> None:
        if isinstance(nodo, nodes.Output):
            parti = []
            for figlio in nodo.nodes:
                if isinstance(figlio, nodes.TemplateData):
                    parti.append(testo_costante(figlio.data))
                else:
                    parti.append(f"J.testo({self.e(figlio, ambito)})")
            if len(parti) == 1:
                self._scrivi(f"{uscita}.append({parti[0]})")
            else:
                self._scrivi(f"{uscita}.extend(({', '.join(parti)}))")
        elif isinstance(nodo, nodes.If):
            self._scrivi(f"if {self.e(nodo.test, ambito)}:")
            self._rientro += 1
            self._blocco(nodo.body, ambito, uscita)
            self._rientro -= 1
            for altro in nodo.elif_:
                self._scrivi(f"elif {self.e(altro.test, ambito)}:")
                self._rientro += 1
                self._blocco(altro.body, ambito, uscita)
                self._rientro -= 1
            if nodo.else_:
                self._scrivi("else:")
                self._rientro += 1
                self._blocco(nodo.else_, ambito, uscita)
                self._rientro -= 1
        elif isinstance(nodo, nodes.Assign):
            valore = self.e(nodo.node, ambito)
            self._assegna(nodo.target, valore, ambito)
        elif isinstance(nodo, nodes.AssignBlock):
            self._assegna_blocco(nodo, ambito)
        elif isinstance(nodo, nodes.For):
            self._ciclo(nodo, ambito, uscita)
        elif isinstance(nodo, nodes.ExprStmt):
            self._scrivi(self.e(nodo.node, ambito))
        elif isinstance(nodo, nodes.Break):
            self._scrivi("break")
        elif isinstance(nodo, nodes.Continue):
            self._scrivi("continue")
        else:
            raise NonTraducibile(type(nodo).__name__)

    def _assegna(self, bersaglio: nodes.Node, valore: str, ambito: _Ambito) -> None:
        if isinstance(bersaglio, nodes.Name):
            self._scrivi(f"{_py(ambito.simboli.ref(bersaglio.name))} = {valore}")
        elif isinstance(bersaglio, nodes.NSRef):
            ns = self._nome(bersaglio.name, ambito)
            self._scrivi(
                f"J.imposta_ns({ns}, {testo_costante(bersaglio.attr)}, {valore})"
            )
        elif isinstance(bersaglio, nodes.Tuple):
            nomi = ", ".join(_py(ambito.simboli.ref(n.name)) for n in bersaglio.items)
            self._scrivi(
                f"{nomi}, = {valore}"
                if len(bersaglio.items) == 1
                else f"{nomi} = {valore}"
            )
        else:
            raise NonTraducibile(f"assegnazione a {type(bersaglio).__name__}")

    def _assegna_blocco(self, nodo: nodes.AssignBlock, ambito: _Ambito) -> None:
        """``{% set x %}...{% endset %}``: il corpo ha il suo ambito (come block_frame)."""
        interno = _Ambito(Symbols(parent=ambito.simboli))
        interno.simboli.analyze_node(nodo)
        self._entra(interno)
        buffer = self._temporaneo("b")
        self._scrivi(f"{buffer} = []")
        self._blocco(nodo.body, interno, buffer)
        valore = f"''.join({buffer})"
        if nodo.filter is not None:
            valore = self._filtri_blocco(nodo.filter, valore, interno)
        self._assegna(nodo.target, valore, ambito)

    def _filtri_blocco(self, nodo: nodes.Filter, valore: str, ambito: _Ambito) -> str:
        """I filtri di ``{% set x | f | g %}``: una catena ``g(f(testo))`` in cui il
        filtro più interno (``node`` vuoto) si applica al testo del blocco."""
        if nodo.node is not None:
            if not isinstance(nodo.node, nodes.Filter):  # pragma: no cover
                raise NonTraducibile(f"filtro del blocco su {type(nodo.node).__name__}")
            valore = self._filtri_blocco(nodo.node, valore, ambito)
        return self._filtro(nodo, valore, ambito)

    def _ciclo(self, nodo: nodes.For, ambito: _Ambito, uscita: str) -> None:
        """``{% for %}`` come CodeGenerator.visit_For (senza ``recursive``)."""
        if nodo.recursive:
            raise NonTraducibile("for recursive")
        interno = _Ambito(Symbols(parent=ambito.simboli), ciclo=True)
        esteso = any(n.name == "loop" for n in nodo.find_all(nodes.Name))
        giro = None
        if esteso:
            giro = interno.simboli.declare_parameter("loop")
        interno.simboli.analyze_node(nodo, for_branch="body")
        iterabile = self.e(nodo.iter, ambito)
        if nodo.test is not None:
            prova = _Ambito(Symbols(parent=ambito.simboli))
            prova.simboli.analyze_node(nodo, for_branch="test")
            bersaglio = self._bersaglio_ciclo(nodo.target, prova)
            iterabile = f"(_x for _x in {iterabile} for {bersaglio} in [_x] if {self.e(nodo.test, prova)})"
        fatto = None
        if nodo.else_:
            fatto = self._temporaneo("vuoto")
            self._scrivi(f"{fatto} = True")
        bersaglio = self._bersaglio_ciclo(nodo.target, interno)
        if esteso:
            self._scrivi(
                f"for {bersaglio}, {_py(giro)} in J.LoopContext({iterabile}, J.Indefinito):"
            )
        else:
            self._scrivi(f"for {bersaglio} in {iterabile}:")
        self._rientro += 1
        self._entra(interno)
        self._blocco(nodo.body, interno, uscita)
        if fatto:
            self._scrivi(f"{fatto} = False")
        self._rientro -= 1
        if nodo.else_:
            altro = _Ambito(Symbols(parent=ambito.simboli))
            altro.simboli.analyze_node(nodo, for_branch="else")
            self._scrivi(f"if {fatto}:")
            self._rientro += 1
            self._entra(altro)
            self._blocco(nodo.else_, altro, uscita)
            self._rientro -= 1

    def _bersaglio_ciclo(self, bersaglio: nodes.Node, ambito: _Ambito) -> str:
        if isinstance(bersaglio, nodes.Name):
            return _py(ambito.simboli.ref(bersaglio.name))
        if isinstance(bersaglio, nodes.Tuple):
            return (
                "("
                + "".join(
                    self._bersaglio_ciclo(n, ambito) + ", " for n in bersaglio.items
                )
                + ")"
            )
        raise NonTraducibile(f"bersaglio del ciclo {type(bersaglio).__name__}")

    # --- espressioni ---------------------------------------------------------------------

    def _nome(self, nome: str, ambito: _Ambito) -> str:
        """Lettura di un nome (come CodeGenerator.visit_Name con ctx load)."""
        ref = ambito.simboli.ref(nome)
        carico = ambito.simboli.find_load(ref)
        if carico is not None and carico[0] == VAR_LOAD_PARAMETER:
            return _py(ref)
        if (
            carico is not None
            and carico[0] == VAR_LOAD_RESOLVE
            and not _salvato(ambito.simboli, nome)
        ):
            # mai assegnato: la variabile del modello o la funzione globale
            if nome in GLOBALI:
                if nome == "states" and TIMER_MOTORE.get():
                    raise NonTraducibile("states come oggetto con i timer del motore")
                return self._risolvi(nome)
            self._controlla(nome)
            return f"V[{testo_costante(nome)}]"
        return f"J.leggi({_py(ref)}, {testo_costante(nome)})"

    def e(self, nodo: nodes.Node, ambito: _Ambito) -> str:
        """Il codice di un'espressione."""
        if isinstance(nodo, nodes.Const):
            return costante(nodo.value)
        if isinstance(nodo, nodes.TemplateData):
            return testo_costante(nodo.data)
        if isinstance(nodo, nodes.Name):
            return self._nome(nodo.name, ambito)
        if isinstance(nodo, nodes.List):
            return "[" + ", ".join(self.e(v, ambito) for v in nodo.items) + "]"
        if isinstance(nodo, nodes.Tuple):
            return "(" + "".join(self.e(v, ambito) + ", " for v in nodo.items) + ")"
        if isinstance(nodo, nodes.Dict):
            return (
                "{"
                + ", ".join(
                    f"{self.e(p.key, ambito)}: {self.e(p.value, ambito)}"
                    for p in nodo.items
                )
                + "}"
            )
        if isinstance(nodo, nodes.Getattr):
            if (entita := _entita_stati(nodo)) is not None and self._globale(
                "states", ambito
            ):
                if TIMER_MOTORE.get() and forse_timer(nodes.Const(entita)):
                    return self._al_timer(f"c.timer.oggetto({testo_costante(entita)})")
                return f"c.oggetto({testo_costante(entita)})"
            if TIMER_MOTORE.get() and self._stati(nodo.node, ambito):
                # states.<dominio>: i timer del motore non sono tra gli stati
                if nodo.attr.lower() == "timer":
                    raise NonTraducibile("states.timer con i timer del motore")
                return f"J.attributo(c.states, {testo_costante(nodo.attr)})"
            return (
                f"J.attributo({self.e(nodo.node, ambito)}, {testo_costante(nodo.attr)})"
            )
        if isinstance(nodo, nodes.Getitem):
            if isinstance(nodo.arg, nodes.Slice):
                return f"J.elemento({self.e(nodo.node, ambito)}, {self._fetta(nodo.arg, ambito)})"
            if TIMER_MOTORE.get() and self._stati(nodo.node, ambito):
                # states[<entity_id>]
                if forse_timer(nodo.arg):
                    return self._al_timer(
                        f"J.elemento(c.timer.stati, {self.e(nodo.arg, ambito)})"
                    )
                return f"J.elemento(c.states, {self.e(nodo.arg, ambito)})"
            return (
                f"J.elemento({self.e(nodo.node, ambito)}, {self.e(nodo.arg, ambito)})"
            )
        if isinstance(nodo, nodes.Call):
            return self._chiamata(nodo, ambito)
        if isinstance(nodo, nodes.Filter):
            return self._filtro(nodo, self.e(nodo.node, ambito), ambito)
        if isinstance(nodo, nodes.Test):
            return self._test(nodo, ambito)
        if isinstance(nodo, nodes.CondExpr):
            altrimenti = (
                self.e(nodo.expr2, ambito)
                if nodo.expr2 is not None
                else "J.indefinito_senza_else()"
            )
            return f"({self.e(nodo.expr1, ambito)} if {self.e(nodo.test, ambito)} else {altrimenti})"
        if isinstance(nodo, nodes.And):
            return f"({self.e(nodo.left, ambito)} and {self.e(nodo.right, ambito)})"
        if isinstance(nodo, nodes.Or):
            return f"({self.e(nodo.left, ambito)} or {self.e(nodo.right, ambito)})"
        if isinstance(nodo, nodes.Not):
            return f"(not {self.e(nodo.node, ambito)})"
        if isinstance(nodo, nodes.Neg):
            return f"(-{self.e(nodo.node, ambito)})"
        if isinstance(nodo, nodes.Pos):
            return f"(+{self.e(nodo.node, ambito)})"
        if type(nodo) in BINARI:
            return f"({self.e(nodo.left, ambito)} {BINARI[type(nodo)]} {self.e(nodo.right, ambito)})"
        if isinstance(nodo, nodes.Concat):
            return "J.concat(" + ", ".join(self.e(v, ambito) for v in nodo.nodes) + ")"
        if isinstance(nodo, nodes.Compare):
            parti = [self.e(nodo.expr, ambito)]
            for operando in nodo.ops:
                parti.append(OPERATORI[operando.op])
                parti.append(self.e(operando.expr, ambito))
            return "(" + " ".join(parti) + ")"
        raise NonTraducibile(type(nodo).__name__)

    def _globale(self, nome: str, ambito: _Ambito) -> bool:
        """Il nome, in questo ambito, è la variabile del modello o la funzione globale
        (mai assegnato nel modello)."""
        ref = ambito.simboli.find_ref(nome)
        carico = ambito.simboli.find_load(ref) if ref else None
        return (
            carico is not None
            and carico[0] == VAR_LOAD_RESOLVE
            and not _salvato(ambito.simboli, nome)
        )

    def _stati(self, nodo: nodes.Node, ambito: _Ambito) -> bool:
        """``nodo`` è la funzione globale ``states``."""
        return (
            isinstance(nodo, nodes.Name)
            and nodo.name == "states"
            and self._globale("states", ambito)
        )

    def _fetta(self, fetta: nodes.Slice, ambito: _Ambito) -> str:
        parti = [
            "None" if parte is None else self.e(parte, ambito)
            for parte in (fetta.start, fetta.stop, fetta.step)
        ]
        return f"slice({', '.join(parti)})"

    def _argomenti(
        self, nodo: nodes.Call | nodes.Filter | nodes.Test, ambito: _Ambito
    ) -> list[str]:
        if nodo.dyn_args is not None or nodo.dyn_kwargs is not None:
            raise NonTraducibile("*args o **kwargs")
        argomenti = [self.e(a, ambito) for a in nodo.args]
        argomenti += [
            f"**{{{testo_costante(k.key)}: {self.e(k.value, ambito)}}}"
            if _PAROLE_NOME.search(k.key)
            else f"{k.key}={self.e(k.value, ambito)}"
            for k in nodo.kwargs
        ]
        return argomenti

    def _chiamata(self, nodo: nodes.Call, ambito: _Ambito) -> str:
        argomenti = self._argomenti(nodo, ambito)
        if (
            isinstance(nodo.node, nodes.Name)
            and nodo.node.name in GLOBALI
            and self._globale(nodo.node.name, ambito)
        ):
            # una funzione globale (sicura per la sandbox): si chiama direttamente
            nome = nodo.node.name
            # expand legge tutti i suoi argomenti, le altre funzioni il primo
            primo = (
                nodes.List(list(nodo.args))
                if nome == "expand"
                else (nodo.args[0] if nodo.args else None)
            )
            if nodo.kwargs and nome == "expand":
                primo = None
            if (
                TIMER_MOTORE.get()
                and nome == "integration_entities"
                and not (
                    nodo.args
                    and isinstance(nodo.args[0], nodes.Const)
                    and isinstance(nodo.args[0].value, str)
                    and nodo.args[0].value != "timer"
                )
            ):
                # i timer del package non sono più entità dell'integrazione timer
                raise NonTraducibile(
                    "integration_entities('timer') con i timer del motore"
                )
            if TIMER_MOTORE.get() and self._lettura_timer(nome, primo, GLOBALI_TIMER):
                return self._al_timer(f"c.timer.{nome}({', '.join(argomenti)})")
            return f"{self._risolvi(nome)}({', '.join(argomenti)})"
        return f"J.chiama({', '.join([self.e(nodo.node, ambito), *argomenti])})"

    def _lettura_timer(
        self, nome: str, primo: nodes.Node | None, instradabili: set[str]
    ) -> bool:
        """Con TIMER_MOTORE: la lettura ``nome`` con primo argomento ``primo`` (None se
        non si conosce) va ai timer del motore? Una lettura che i timer del motore non
        sanno fare, se può riguardare un timer, ferma la traduzione."""
        if nome not in instradabili and nome not in ALTRE_LETTURE:
            return False
        if not forse_timer(primo):
            return False
        if nome in ALTRE_LETTURE:
            raise NonTraducibile(f"{nome} di un timer con i timer del motore")
        return True

    def _filtro(self, nodo: nodes.Filter, valore: str, ambito: _Ambito) -> str:
        argomenti = self._argomenti(nodo, ambito)
        if nodo.name in ("map", "select", "reject", "selectattr", "rejectattr"):
            argomenti = self._nomi_ha(nodo, argomenti, ambito)
        if (
            nodo.name in self.filtri_ha
            and TIMER_MOTORE.get()
            and self._lettura_timer(nodo.name, nodo.node, FILTRI_TIMER)
        ):
            funzione = self._al_timer(f"c.timer.filtro({nodo.name!r})")
        elif nodo.name in self.filtri_ha:
            funzione = f"c.filtro({nodo.name!r})"
        elif hasattr(J, f"f_{nodo.name}"):
            funzione = f"J.f_{nodo.name}"
        else:
            raise NonTraducibile(f"filtro {nodo.name}")
        return f"{funzione}({', '.join([valore, *argomenti])})"

    def _nomi_ha(
        self, nodo: nodes.Filter, argomenti: list[str], ambito: _Ambito
    ) -> list[str]:
        """``map('nome')``, ``select('test')``...: un filtro o test di Home Assistant che
        legge gli stati passa come funzione del contesto."""
        posto = 1 if nodo.name in ("selectattr", "rejectattr") else 0
        if len(nodo.args) > posto and isinstance(nodo.args[posto], nodes.Const):
            nome = nodo.args[posto].value
            # il filtro o il test si applica a ogni elemento (con selectattr e rejectattr a
            # un attributo di ogni elemento)
            elementi = (
                nodo.node
                if posto == 0
                and not forse_timer_tra(nodo.node, lambda n: self._globale(n, ambito))
                else None
            )
            if TIMER_MOTORE.get() and self._lettura_timer(
                nome,
                nodes.Const(None) if elementi is not None else None,
                FILTRI_TIMER if nodo.name == "map" else TEST_TIMER,
            ):
                parola = "filtro" if nodo.name == "map" else "test"
                argomenti[posto] = self._al_timer(f"c.timer.{parola}({nome!r})")
            elif nodo.name == "map" and nome in self.filtri_ha:
                argomenti[posto] = f"c.filtro({nome!r})"
            elif nodo.name != "map" and nome in self.test_ha:
                argomenti[posto] = f"c.test({nome!r})"
        return argomenti

    def _test(self, nodo: nodes.Test, ambito: _Ambito) -> str:
        argomenti = [self.e(nodo.node, ambito), *self._argomenti(nodo, ambito)]
        if (
            nodo.name in self.test_ha
            and TIMER_MOTORE.get()
            and self._lettura_timer(nodo.name, nodo.node, TEST_TIMER)
        ):
            return self._al_timer(
                f"c.timer.test({nodo.name!r})({', '.join(argomenti)})"
            )
        if nodo.name in self.test_ha:
            return f"c.test({nodo.name!r})({', '.join(argomenti)})"
        if hasattr(J, f"t_{nodo.name}"):
            return f"J.t_{nodo.name}({', '.join(argomenti)})"
        return f"J.prova({nodo.name!r}, {', '.join(argomenti)})"


def _salvato(simboli: Symbols, nome: str) -> bool:
    """Il nome è assegnato in questo ambito o in uno esterno."""
    corrente: Symbols | None = simboli
    while corrente is not None:
        if nome in corrente.stores:
            return True
        corrente = corrente.parent
    return False


def _entita_stati(nodo: nodes.Getattr) -> str | None:
    """``states.dominio.oggetto`` con nomi fissi: l'entity_id."""
    interno = nodo.node
    if (
        isinstance(interno, nodes.Getattr)
        and isinstance(interno.node, nodes.Name)
        and interno.node.name == "states"
        and interno.node.ctx == "load"
    ):
        return f"{interno.attr}.{nodo.attr}"
    return None


def _py(ref: str) -> str:
    """Nome Python di una variabile di Jinja (``l_0_x`` -> ``v_x``, ``l_1_x`` -> ``v_x_1``)."""
    _l, livello, nome = ref.split("_", 2)
    return f"v_{nome}" if livello == "0" else f"v_{nome}_{livello}"


def _documento(testo: str) -> str:
    riga = " ".join(testo.split())
    if len(riga) > 90:
        riga = riga[:87] + "..."
    return riga
