"""Valori realistici per i modelli del package (banco di test_modelli_motore.py).

Dal package si leggono:

- le entità definite: le opzioni degli ``input_select``, minimo, massimo e passo degli
  ``input_number``, data e ora degli ``input_datetime``, i timer, i sensori con unità di
  misura (numeri);
- i trigger di ogni automazione (piattaforma, ``id``, entità, ``from``/``to``, eventi) e
  quali modelli stanno in quale automazione o script;
- le assegnazioni delle variabili (``variables``, dati passati agli script) e dei valori
  scritti negli aiutanti (``input_text.set_value``, ``input_select.select_option``,
  ``input_number.set_value``), testi fissi o modelli da rendere;
- da ogni modello, i confronti con valori fissi (``states('x') == 'Free Cooling'``,
  ``trigger.id == '...'``, ``parti[1] != 'free_annullamento'``, ``x | float > 25``,
  ``is_state('x', ['on', 'off'])``, ``{...}[x]``...): il «soggetto» del confronto (uno
  stato, un attributo, una variabile con il suo percorso) e i valori che fanno prendere
  l'uno o l'altro ramo.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

import jinja2
import yaml
from jinja2 import nodes

from custom_components.vmc_master.trasforma import rimuovi_sezioni_solo_master

from .traduci import PACKAGE, _qualsiasi_tag, leggi_package
from .traduci_jinja import GLOBALI

ENTITA = re.compile(
    r"\b(?:input_boolean|input_number|input_select|input_text|input_datetime|sensor|"
    r"binary_sensor|switch|timer|automation|script|media_player|weather|sun|zone|person|"
    r"device_tracker|climate|fan|light|number|select|button|calendar|counter|group|"
    r"update|text|event|shell_command)\.[a-z0-9_]+"
)
_AMBIENTE = jinja2.Environment(extensions=["jinja2.ext.loopcontrols", "jinja2.ext.do"])
# Filtri che non cambiano il soggetto di un confronto (``states('x') | float(0) > 5``).
_PASSANTI = {
    "float",
    "int",
    "string",
    "trim",
    "lower",
    "upper",
    "round",
    "default",
    "abs",
    "bool",
    "replace",
}
_NUMERICI = {"float", "int", "round", "abs"}
Soggetto = tuple[Any, ...]


class _Caricatore(getattr(yaml, "CSafeLoader", yaml.SafeLoader)):  # type: ignore[misc]
    """Come ``traduci._Caricatore`` (i tag di Home Assistant restano il loro valore), con
    libyaml quando c'è: il package si legge in un decimo del tempo."""


_Caricatore.add_multi_constructor("!", _qualsiasi_tag)


def e_modello(testo: Any) -> bool:
    return isinstance(testo, str) and ("{{" in testo or "{%" in testo)


def modelli_in(valore: Any) -> Iterator[str]:
    """I modelli (testo senza spazi ai bordi, come ``Template``) dentro un valore."""
    if e_modello(valore):
        yield valore.strip()
    elif isinstance(valore, dict):
        for chiave, voce in valore.items():
            yield from modelli_in(chiave)
            yield from modelli_in(voce)
    elif isinstance(valore, list):
        for voce in valore:
            yield from modelli_in(voce)


def lista(valore: Any) -> list[Any]:
    if valore is None:
        return []
    return valore if isinstance(valore, list) else [valore]


# --- Analisi di un modello ----------------------------------------------------------------


@dataclass
class Analisi:
    """Le variabili lette da un modello e i valori dei suoi confronti."""

    nomi: set[str] = field(default_factory=set)
    candidati: dict[Soggetto, list[Any]] = field(default_factory=dict)
    numerici: set[Soggetto] = field(default_factory=set)
    # tutti i testi (brevi) e i numeri scritti nel modello
    testi: set[str] = field(default_factory=set)
    numeri: set[Any] = field(default_factory=set)

    def aggiungi(self, soggetto: Soggetto | None, valore: Any) -> None:
        if soggetto is None:
            return
        voci = self.candidati.setdefault(soggetto, [])
        if not any(type(v) is type(valore) and v == valore for v in voci):
            voci.append(valore)

    def aggiungi_numeri(self, soggetto: Soggetto | None, numero: float) -> None:
        if soggetto is None:
            return
        self.numerici.add(soggetto)
        for delta in (-1, 0, 1, 0.5):
            valore = numero + delta
            self.aggiungi(soggetto, valore)
            self.aggiungi(soggetto, str(valore))


def _costante(nodo: nodes.Node) -> tuple[bool, Any]:
    try:
        return True, nodo.as_const()
    except nodes.Impossible:
        return False, None


def _divisione(nodo: nodes.Node, alias: dict[str, Any]) -> tuple[Soggetto, str] | None:
    """``x.split('|')`` (o una variabile del modello assegnata così, anche in un ``... if
    ... else ...``): soggetto e separatore."""
    if isinstance(nodo, nodes.CondExpr):
        return _divisione(nodo.expr1, alias) or (
            _divisione(nodo.expr2, alias) if nodo.expr2 is not None else None
        )
    if isinstance(nodo, nodes.Name) and isinstance(alias.get(nodo.name), tuple):
        voce = alias[nodo.name]
        if voce and voce[0] == "split":
            return voce[1], voce[2]
    if (
        isinstance(nodo, nodes.Call)
        and isinstance(nodo.node, nodes.Getattr)
        and nodo.node.attr == "split"
        and len(nodo.args) == 1
        and isinstance(nodo.args[0], nodes.Const)
        and isinstance(nodo.args[0].value, str)
    ):
        soggetto = soggetto_di(nodo.node.node, alias)
        if soggetto is not None:
            return soggetto, nodo.args[0].value
    return None


def soggetto_di(nodo: nodes.Node, alias: dict[str, Any]) -> Soggetto | None:
    """Il soggetto di un'espressione: ``('stato', entità)``, ``('attributo', entità,
    nome)``, ``('var', nome, *percorso)`` o ``('parte', soggetto, separatore, indice)``."""
    if isinstance(nodo, nodes.Filter) and nodo.name in _PASSANTI and nodo.node:
        return soggetto_di(nodo.node, alias)
    if isinstance(nodo, nodes.Call) and isinstance(nodo.node, nodes.Name):
        argomenti = [_costante(a) for a in nodo.args]
        nome = nodo.node.name
        if nome == "states" and len(argomenti) == 1 and argomenti[0][0]:
            return ("stato", argomenti[0][1])
        if (
            nome == "state_attr"
            and len(argomenti) == 2
            and all(a[0] for a in argomenti)
        ):
            return ("attributo", argomenti[0][1], argomenti[1][1])
        if nome in ("float", "int") and nodo.args:
            return soggetto_di(nodo.args[0], alias)
        return None
    if isinstance(nodo, nodes.Name):
        if nodo.name in alias:
            voce = alias[nodo.name]
            return voce if voce and voce[0] != "split" else None
        if nodo.name in GLOBALI:
            return ("globale", nodo.name)
        return ("var", nodo.name)
    if isinstance(nodo, (nodes.Getattr, nodes.Getitem)):
        if isinstance(nodo, nodes.Getattr):
            chiave: Any = nodo.attr
        else:
            costante, chiave = _costante(nodo.arg)
            if not costante:
                return None
        if (divisione := _divisione(nodo.node, alias)) is not None and isinstance(
            chiave, int
        ):
            return ("parte", divisione[0], divisione[1], chiave)
        base = soggetto_di(nodo.node, alias)
        if base is None:
            return None
        if base[0] == "var":
            return (*base, chiave)
        if base == ("globale", "states"):
            return ("dominio", chiave)
        if base[0] == "dominio" and len(base) == 2:
            return ("entita", f"{base[1]}.{chiave}")
        if base[0] == "entita":
            if chiave == "state":
                return ("stato", base[1])
            if chiave == "attributes":
                return ("attributi", base[1])
            return None
        if base[0] == "attributi":
            return ("attributo", base[1], chiave)
    return None


def analizza(sorgente: str) -> Analisi:
    """Variabili e confronti di un modello."""
    albero = _AMBIENTE.parse(sorgente)
    analisi = Analisi()
    salvati = {
        n.name for n in albero.find_all(nodes.Name) if n.ctx in ("store", "param")
    }
    analisi.nomi = {
        n.name
        for n in albero.find_all(nodes.Name)
        if n.ctx == "load" and n.name not in salvati | GLOBALI | {"loop"}
    }
    for costante in albero.find_all(nodes.Const):
        if isinstance(costante.value, str) and len(costante.value) < 80:
            analisi.testi.add(costante.value)
        elif isinstance(costante.value, (int, float)) and not isinstance(
            costante.value, bool
        ):
            analisi.numeri.add(costante.value)
    alias: dict[str, Any] = {}
    for assegnazione in albero.find_all(nodes.Assign):
        if isinstance(assegnazione.target, nodes.Name):
            nome = assegnazione.target.name
            if (divisione := _divisione(assegnazione.node, alias)) is not None:
                alias[nome] = ("split", *divisione)
            elif (soggetto := soggetto_di(assegnazione.node, alias)) is not None:
                alias[nome] = soggetto
    coppie: list[tuple[Soggetto, Soggetto]] = []
    for nodo in albero.find_all(nodes.Node):
        if isinstance(nodo, nodes.Compare) and len(nodo.ops) == 1:
            # x == y tra due soggetti: dopo, ognuno prende anche i valori dell'altro
            primo = soggetto_di(nodo.expr, alias)
            secondo = soggetto_di(nodo.ops[0].expr, alias)
            if primo and secondo and nodo.ops[0].op in ("eq", "ne"):
                coppie.append((primo, secondo))
        if (
            isinstance(nodo, nodes.Test)
            and nodo.name in ("match", "search")
            and nodo.args
        ):
            # x is match('timer\.vmc_master_lettura_'): un testo che lo soddisfa
            costante, espressione = _costante(nodo.args[0])
            if costante and isinstance(espressione, str):
                testo = re.sub(r"\\(.)", r"\1", espressione.strip("^$"))
                for prova in (testo, f"{testo}ping"):
                    if re.search(espressione, prova):
                        analisi.aggiungi(soggetto_di(nodo.node, alias), prova)
        if isinstance(nodo, nodes.Compare):
            sinistra = nodo.expr
            for operando in nodo.ops:
                _confronto(analisi, sinistra, operando.op, operando.expr, alias)
                sinistra = operando.expr
        elif isinstance(nodo, nodes.Call) and isinstance(nodo.node, nodes.Name):
            _chiamata(analisi, nodo, alias)
        elif isinstance(nodo, nodes.Call) and isinstance(nodo.node, nodes.Getattr):
            # x.startswith('a'), {...}.get(x, ...)
            soggetto = soggetto_di(nodo.node.node, alias)
            if nodo.node.attr in ("startswith", "endswith") and nodo.args:
                costante, valore = _costante(nodo.args[0])
                if costante and isinstance(valore, str):
                    analisi.aggiungi(soggetto, valore)
                    analisi.aggiungi(
                        soggetto,
                        f"{valore}|1"
                        if nodo.node.attr == "startswith"
                        else f"1|{valore}",
                    )
            elif nodo.node.attr == "get" and nodo.args:
                costante, dizionario = _costante(nodo.node.node)
                if costante and isinstance(dizionario, dict):
                    for chiave in dizionario:
                        analisi.aggiungi(soggetto_di(nodo.args[0], alias), chiave)
        elif isinstance(nodo, nodes.Getitem):
            costante, dizionario = _costante(nodo.node)
            if costante and isinstance(dizionario, dict):
                for chiave in dizionario:
                    analisi.aggiungi(soggetto_di(nodo.arg, alias), chiave)
        elif isinstance(nodo, nodes.Filter) and nodo.name == "bool" and nodo.node:
            soggetto = soggetto_di(nodo.node, alias)
            for valore in ("on", "off", True, False):
                analisi.aggiungi(soggetto, valore)
        elif isinstance(nodo, nodes.Filter) and nodo.name in _NUMERICI and nodo.node:
            # ``x | int`` senza predefinito: anche testi che sono numeri
            soggetto = soggetto_di(nodo.node, alias)
            if soggetto is not None:
                analisi.numerici.add(soggetto)
                for valore in ("0", "3", "7.5", 2):
                    analisi.aggiungi(soggetto, valore)
        elif isinstance(nodo, (nodes.If, nodes.CondExpr)) and isinstance(
            nodo.test, (nodes.Name, nodes.Getattr)
        ):
            soggetto = soggetto_di(nodo.test, alias)
            if soggetto is not None and soggetto[0] == "var":
                analisi.aggiungi(soggetto, True)
                analisi.aggiungi(soggetto, False)
    for primo, secondo in coppie:
        for valore in [*analisi.candidati.get(primo, [])]:
            analisi.aggiungi(secondo, valore)
        for valore in [*analisi.candidati.get(secondo, [])]:
            analisi.aggiungi(primo, valore)
    return analisi


def _lunghezza(
    analisi: Analisi, nodo: nodes.Node, op: str, numero: Any, alias: dict
) -> None:
    """``x.split('|') | length == 8``: testi con quel numero di parti (e uno in più)."""
    if not (
        isinstance(nodo, nodes.Filter)
        and nodo.name in ("length", "count")
        and nodo.node is not None
        and isinstance(numero, int)
        and op in ("eq", "ne", "gt", "gteq", "lt", "lteq")
    ):
        return
    if (divisione := _divisione(nodo.node, alias)) is None:
        return
    soggetto, separatore = divisione
    for parti in {max(numero, 0), numero + 1}:
        analisi.aggiungi(soggetto, separatore.join(["0"] * parti))
        analisi.aggiungi(soggetto, separatore.join(str(i * 10) for i in range(parti)))


def _confronto(
    analisi: Analisi, sinistra: nodes.Node, op: str, destra: nodes.Node, alias: dict
) -> None:
    fissa_d, valore_d = _costante(destra)
    fissa_s, valore_s = _costante(sinistra)
    if fissa_d and fissa_s:
        return
    if fissa_d:
        _lunghezza(analisi, sinistra, op, valore_d, alias)
    if op in ("eq", "ne"):
        if fissa_d:
            analisi.aggiungi(soggetto_di(sinistra, alias), valore_d)
        if fissa_s:
            analisi.aggiungi(soggetto_di(destra, alias), valore_s)
    elif op in ("in", "notin"):
        if fissa_d and isinstance(valore_d, (list, tuple)):
            soggetto = soggetto_di(sinistra, alias)
            for voce in valore_d:
                analisi.aggiungi(soggetto, voce)
        if fissa_s:
            soggetto = soggetto_di(destra, alias)
            analisi.aggiungi(soggetto, valore_s)
            analisi.aggiungi(soggetto, [valore_s])
            if isinstance(valore_s, str):
                analisi.aggiungi(soggetto, f"x{valore_s}x")
    elif op in ("gt", "gteq", "lt", "lteq"):
        if fissa_d and isinstance(valore_d, (int, float)):
            analisi.aggiungi_numeri(soggetto_di(sinistra, alias), valore_d)
        if fissa_s and isinstance(valore_s, (int, float)):
            analisi.aggiungi_numeri(soggetto_di(destra, alias), valore_s)


def _chiamata(analisi: Analisi, nodo: nodes.Call, alias: dict) -> None:
    nome = nodo.node.name  # type: ignore[attr-defined]
    argomenti = [_costante(a) for a in nodo.args]
    if nome == "is_state" and len(argomenti) == 2 and argomenti[0][0]:
        soggetto: Soggetto = ("stato", argomenti[0][1])
        if argomenti[1][0]:
            for valore in lista(argomenti[1][1]):
                analisi.aggiungi(soggetto, valore)
    elif nome == "is_state_attr" and len(argomenti) == 3:
        if argomenti[0][0] and argomenti[1][0] and argomenti[2][0]:
            analisi.aggiungi(
                ("attributo", argomenti[0][1], argomenti[1][1]), argomenti[2][1]
            )


# --- Il package -----------------------------------------------------------------------------


@dataclass
class Assegnazione:
    """Un valore assegnato nel package a una variabile o a un aiutante."""

    nome: str
    valore: Any
    automazione: int | None  # indice dell'automazione, None in uno script


@dataclass
class Package:
    """Quello che il banco legge dal package."""

    automazioni: list[dict[str, Any]] = field(default_factory=list)
    script: dict[str, dict[str, Any]] = field(default_factory=dict)
    definizioni: dict[str, dict[str, Any]] = field(default_factory=dict)
    numerici: set[str] = field(default_factory=set)
    trigger: list[list[dict[str, Any]]] = field(default_factory=list)
    automazioni_di: dict[str, set[int]] = field(default_factory=dict)
    negli_script: set[str] = field(default_factory=set)
    variabili: list[Assegnazione] = field(default_factory=list)
    scritture: list[Assegnazione] = field(default_factory=list)
    per_ogni: list[Assegnazione] = field(default_factory=list)


def _cerca(valore: Any, dove: int | None, package: Package) -> None:
    """Assegnazioni di variabili, valori scritti negli aiutanti e ``for_each``."""
    if isinstance(valore, list):
        for voce in valore:
            _cerca(voce, dove, package)
        return
    if not isinstance(valore, dict):
        return
    if isinstance(valore.get("variables"), dict):
        for nome, voce in valore["variables"].items():
            package.variabili.append(Assegnazione(nome, voce, dove))
    azione = valore.get("action")
    dati = valore.get("data")
    if isinstance(azione, str) and isinstance(dati, dict):
        if azione.startswith("script.") and azione != "script.turn_on":
            for nome, voce in dati.items():
                package.variabili.append(Assegnazione(nome, voce, dove))
        chiave = {
            "input_text.set_value": "value",
            "input_select.select_option": "option",
            "input_number.set_value": "value",
        }.get(azione)
        if chiave is not None and chiave in dati:
            bersaglio = valore.get("target") or {}
            entita = lista(
                dati.get("entity_id")
                or (bersaglio.get("entity_id") if isinstance(bersaglio, dict) else None)
                or valore.get("entity_id")
            )
            for voce in entita:
                if isinstance(voce, str) and not e_modello(voce):
                    package.scritture.append(Assegnazione(voce, dati[chiave], dove))
    if isinstance(valore.get("repeat"), dict) and "for_each" in valore["repeat"]:
        package.per_ogni.append(
            Assegnazione("item", valore["repeat"]["for_each"], dove)
        )
    for voce in valore.values():
        _cerca(voce, dove, package)


def _carica(nome: str) -> Any:
    return yaml.load(
        rimuovi_sezioni_solo_master((PACKAGE / nome).read_text("utf-8")),
        Loader=_Caricatore,
    )


def leggi() -> Package:
    """Automazioni e script (da ``traduci.leggi_package``), definizioni, trigger,
    assegnazioni del package (dopo le sezioni «solo master»)."""
    completo = _carica("vmc_master.yaml")
    # automazioni e script dalla stessa lettura del traduttore (stesso ordine e stesso
    # contenuto: i nomi delle funzioni tradotte dipendono dall'ordine)
    automazioni, script = leggi_package()
    package = Package(automazioni=automazioni, script=script)
    for dominio in (
        "input_select",
        "input_number",
        "input_text",
        "input_datetime",
        "input_boolean",
        "timer",
    ):
        for nome, config in (completo.get(dominio) or {}).items():
            package.definizioni[f"{dominio}.{nome}"] = dict(config or {})
    for blocco in completo.get("template") or []:
        for voce in blocco.get("sensor") or []:
            if voce.get("unit_of_measurement") and voce.get("default_entity_id"):
                package.numerici.add(voce["default_entity_id"])
    for indice, automazione in enumerate(package.automazioni):
        package.trigger.append(list(automazione.get("triggers") or []))
        for sorgente in modelli_in(automazione):
            package.automazioni_di.setdefault(sorgente, set()).add(indice)
        _cerca(automazione, indice, package)
    for config in package.script.values():
        package.negli_script.update(modelli_in(config))
        _cerca(config, None, package)
    return package
