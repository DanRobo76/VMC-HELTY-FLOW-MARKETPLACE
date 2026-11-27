"""La semantica dei modelli Jinja di Home Assistant, per il codice tradotto dal package.

Il traduttore trasforma ogni modello Jinja del package in un'espressione Python che usa
queste funzioni. Il risultato deve essere identico, byte per byte, a quello del motore
dei modelli di Home Assistant 2026.11 (``homeassistant.helpers.template``):
``TemplateEnvironment`` è un ``ImmutableSandboxedEnvironment`` di Jinja con un valore
indefinito che scrive nel registro (``LoggingUndefined``) e ``finalize=_finalize_output``.

Per non rifare a mano le regole di Jinja, qui c'è un ambiente Jinja vero (``_AMBIENTE``)
costruito come quello di Home Assistant: stesse regole della sandbox per attributi e
chiamate, stessi filtri e test di Jinja, e i filtri e test di Home Assistant che non
hanno bisogno di ``hass`` rifatti con le regole di 2026.11. Così ``x.y``, ``x[k]``,
``x.metodo(...)``, ``map('trim')``, ``select('match', ...)``, ``selectattr(...)`` e gli
altri filtri di Jinja passano esattamente dal codice che usa Home Assistant.

Regole che il traduttore deve conoscere:

- un errore di resa (in Home Assistant ``TemplateError``) qui è un'eccezione qualsiasi:
  il codice tradotto la converte in ``ErroreTemplate``, come Home Assistant fa con
  ``raise TemplateError(err) from err`` per ogni eccezione della resa;
- una variabile che non esiste vale ``indefinito(nome)``;
- ``{{ v }}`` è ``testo(v)``, ``a ~ b`` è ``concat(a, b)``; la resa intera si toglie gli
  spazi ai bordi (``strip``) come in Home Assistant prima di usarla;
- gli operatori aritmetici, i confronti, ``and``, ``or`` e ``not`` di Jinja sono quelli di
  Python (la sandbox non ne intercetta nessuno): le funzioni ``somma``, ``sottrai`` e le
  altre esistono per chiarezza del codice tradotto e fanno l'operazione di Python;
- ``x[a:b]`` in Jinja non passa da ``getitem`` dell'ambiente: ``elemento`` con uno
  ``slice`` fa ``x[a:b]`` di Python;
- i filtri e i test che hanno bisogno di ``hass`` (``device_attr``, ``is_state``...) non
  sono qui: a ``f_map``, ``f_select``, ``f_reject``, ``f_selectattr``, ``f_rejectattr`` e
  ``prova`` si può passare, al posto del nome, la funzione Python che li fa.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Iterator
from datetime import date, datetime, time, timedelta
from enum import ReprEnum
from functools import lru_cache
from numbers import Number
from typing import Any

import jinja2
from homeassistant.helpers.template import template_cv
from homeassistant.util import dt as dt_util
from homeassistant.util import slugify as _slugify
from homeassistant.util.json import JSON_DECODE_EXCEPTIONS, json_loads
from homeassistant.util.read_only_dict import ReadOnlyDict
from jinja2.runtime import AsyncLoopContext, LoopContext
from jinja2.sandbox import ImmutableSandboxedEnvironment
from jinja2.utils import Namespace

from ..risultato import interpreta

__all__ = [
    "ErroreTemplate",
    "Indefinito",
    "as_datetime",
    "as_timestamp",
    "attributo",
    "chiama",
    "concat",
    "condizione",
    "contiene",
    "dividi",
    "dividi_intero",
    "elemento",
    "f_abs",
    "f_bool",
    "f_capitalize",
    "f_count",
    "f_default",
    "f_float",
    "f_from_json",
    "f_int",
    "f_is_number",
    "f_join",
    "f_length",
    "f_list",
    "f_lower",
    "f_map",
    "f_max",
    "f_min",
    "f_regex_replace",
    "f_reject",
    "f_rejectattr",
    "f_replace",
    "f_round",
    "f_select",
    "f_selectattr",
    "f_slugify",
    "f_sort",
    "f_string",
    "f_sum",
    "f_trim",
    "f_unique",
    "imposta_ns",
    "indefinito",
    "interpreta",
    "log",
    "moltiplica",
    "namespace",
    "nega",
    "positivo",
    "potenza",
    "prova",
    "resto",
    "somma",
    "sottrai",
    "strptime",
    "t_defined",
    "t_mapping",
    "t_match",
    "t_none",
    "testo",
    "timedelta",
    "trigger_vero",
]

# Segnaposto per «nessun valore predefinito» (in Home Assistant ``_SENTINEL``).
_MANCANTE: Any = object()


class ErroreTemplate(Exception):
    """Errore di resa di un modello (in Home Assistant ``TemplateError``)."""


class Indefinito(jinja2.Undefined):
    """Il valore indefinito dei modelli di Home Assistant (``LoggingUndefined``).

    Si comporta come ``jinja2.Undefined``: si scrive come testo vuoto, è falso, si
    itera come una sequenza vuota, è uguale a ogni altro indefinito; ogni altra
    operazione (aritmetica, confronto d'ordine, ``float()``, chiamata, attributo,
    elemento) è un errore. Home Assistant in più scrive un avviso nel registro.

    Come ``LoggingUndefined`` non dichiara ``__slots__``: ha ``__dict__`` e ``__weakref__``,
    e ``x.__dict__`` di un indefinito è un indefinito «non sicuro», non un errore.
    """


def indefinito(nome: str) -> Indefinito:
    """Il valore di una variabile ``nome`` che non esiste (come lo crea Jinja)."""
    return Indefinito(name=nome)


# --- Regole di Home Assistant per i filtri senza «hass» (2026.11) ------------------------


def _senza_predefinito(funzione: str, valore: Any) -> Any:
    """Come ``raise_no_default`` di Home Assistant: valore non valido e nessun predefinito.

    Il messaggio dice quale modello si stava rendendo (``template_cv``: durante la resa di
    un modello tradotto lo imposta ``Contesto.testo``, come ``render_with_context``).
    """
    modello, azione = template_cv.get() or ("", "rendering or compiling")
    raise ValueError(
        f"Template error: {funzione} got invalid input '{valore}' when {azione} template"
        f" '{modello}' but no default was specified"
    )


def f_float(value: Any, default: Any = _MANCANTE) -> Any:
    """``value | float(default)`` e ``float(value, default)`` (``forgiving_float``)."""
    try:
        return float(value)
    except (ValueError, TypeError, OverflowError):
        if default is _MANCANTE:
            _senza_predefinito("float", value)
        return default


def f_int(value: Any, default: Any = _MANCANTE, base: int = 10) -> Any:
    """``value | int(default, base)`` e ``int(...)`` (``forgiving_int``).

    Usa ``do_int`` di Jinja come Home Assistant: ``'42.7'`` vale 42, ``'0x1A'`` con base 16
    vale 26. Dal 2026.11 un infinito (``OverflowError``) dà il predefinito.
    """
    try:
        risultato = jinja2.filters.do_int(value, default=default, base=base)
    except OverflowError:
        risultato = default
    if risultato is _MANCANTE:
        _senza_predefinito("int", value)
    return risultato


def f_round(
    value: Any, precision: int = 0, method: str = "common", default: Any = _MANCANTE
) -> Any:
    """``value | round(precision, method, default)`` (``forgiving_round``).

    Metodi ``ceil``, ``floor``, ``half`` (al mezzo più vicino, ignora la precisione);
    ogni altro metodo è l'arrotondamento di Python. Con precisione 0 il risultato è int.
    """
    try:
        moltiplicatore = float(10**precision)
        if method == "ceil":
            value = math.ceil(float(value) * moltiplicatore) / moltiplicatore
        elif method == "floor":
            value = math.floor(float(value) * moltiplicatore) / moltiplicatore
        elif method == "half":
            value = round(float(value) * 2) / 2
        else:
            value = round(float(value), precision)
        return int(value) if precision == 0 else value
    except (ValueError, TypeError, OverflowError):
        if default is _MANCANTE:
            _senza_predefinito("round", value)
        return default


def f_is_number(value: Any) -> bool:
    """``value | is_number``, ``is_number(value)`` e ``value is is_number``."""
    try:
        numero = float(value)
    except (ValueError, TypeError, OverflowError):
        return False
    return math.isfinite(numero)


class _NonBooleano(Exception):
    """Valore che ``cv.boolean`` rifiuta (in Home Assistant ``probatio.Invalid``)."""


def _booleano(valore: Any) -> bool:
    """``homeassistant.helpers.config_validation.boolean``."""
    if isinstance(valore, bool):
        return valore
    if isinstance(valore, str):
        valore = valore.lower().strip()
        if valore in ("1", "true", "yes", "on", "enable"):
            return True
        if valore in ("0", "false", "no", "off", "disable"):
            return False
    elif isinstance(valore, Number):
        return valore != 0
    raise _NonBooleano(f"invalid boolean value {valore}")


def f_bool(value: Any, default: Any = _MANCANTE) -> Any:
    """``value | bool(default)`` e ``bool(value, default)`` (``forgiving_boolean``)."""
    try:
        return _booleano(value)
    except _NonBooleano:
        if default is _MANCANTE:
            _senza_predefinito("bool", value)
        return default


# Stessa cache di Home Assistant per le espressioni regolari.
_regex = lru_cache(maxsize=128)(re.compile)


def t_match(value: Any, find: str = "", ignorecase: bool = False) -> bool:
    """``value is match(find, ignorecase)`` e ``value | regex_match(...)``."""
    if not isinstance(value, str):
        value = str(value)
    return bool(_regex(find, re.IGNORECASE if ignorecase else 0).match(value))


def _cerca(value: Any, find: str = "", ignorecase: bool = False) -> bool:
    """``value is search(find, ignorecase)`` e ``value | regex_search(...)``."""
    if not isinstance(value, str):
        value = str(value)
    return bool(_regex(find, re.IGNORECASE if ignorecase else 0).search(value))


def f_regex_replace(
    value: Any = "", find: str = "", replace: str = "", ignorecase: bool = False
) -> str:
    """``value | regex_replace(find, replace, ignorecase)``."""
    if not isinstance(value, str):
        value = str(value)
    return str(_regex(find, re.IGNORECASE if ignorecase else 0).sub(replace, value))


def _trova_tutti(value: Any, find: str = "", ignorecase: bool = False) -> list[Any]:
    """``value | regex_findall(find, ignorecase)``."""
    if not isinstance(value, str):
        value = str(value)
    return _regex(find, re.IGNORECASE if ignorecase else 0).findall(value)


def _trova_indice(
    value: Any, find: str = "", index: int = 0, ignorecase: bool = False
) -> Any:
    """``value | regex_findall_index(find, index, ignorecase)``."""
    return _trova_tutti(value, find, ignorecase)[index]


def f_slugify(value: Any, separator: str = "_") -> str:
    """``value | slugify(separator)`` e ``slugify(...)``."""
    return _slugify(str(value), separator=separator)


def f_from_json(value: Any, default: Any = _MANCANTE) -> Any:
    """``value | from_json(default)``."""
    try:
        return json_loads(value)
    except JSON_DECODE_EXCEPTIONS:
        if default is _MANCANTE:
            _senza_predefinito("from_json", value)
        return default


def log(value: Any, base: Any = math.e, default: Any = _MANCANTE) -> Any:
    """``log(value, base, default)`` e ``value | log(...)``."""
    try:
        base_numero = float(base)
    except (ValueError, TypeError, OverflowError):
        if default is _MANCANTE:
            _senza_predefinito("log", base)
        return default
    try:
        return math.log(float(value), base_numero)
    except (ValueError, TypeError, OverflowError, ZeroDivisionError):
        if default is _MANCANTE:
            _senza_predefinito("log", value)
        return default


def as_timestamp(value: Any, default: Any = _MANCANTE) -> Any:
    """``as_timestamp(value, default)`` e ``value | as_timestamp(default)``.

    Usa ``dt_util.as_timestamp`` di Home Assistant: un datetime senza fuso orario si
    legge nell'ora locale del sistema (``datetime.timestamp``), un testo si legge con
    ``dt_util.parse_datetime``.
    """
    try:
        return dt_util.as_timestamp(value)
    except (ValueError, TypeError):
        if default is _MANCANTE:
            _senza_predefinito("as_timestamp", value)
        return default


def as_datetime(value: Any, default: Any = _MANCANTE) -> Any:
    """``as_datetime(value, default)`` e ``value | as_datetime(default)``."""
    if type(value) is datetime:
        return value
    if type(value) is date:
        return datetime.combine(value, time(0, 0, 0))
    try:
        return dt_util.utc_from_timestamp(float(value))
    except (ValueError, TypeError):
        try:
            return dt_util.parse_datetime(value, raise_on_error=True)
        except (ValueError, TypeError):
            if default is _MANCANTE:
                # Un testo non valido senza predefinito dà None (compatibilità di HA).
                if isinstance(value, str):
                    return None
                _senza_predefinito("as_datetime", value)
            return default


def strptime(string: Any, fmt: Any, default: Any = _MANCANTE) -> Any:
    """``strptime(string, fmt, default)``: ``datetime.strptime`` con predefinito."""
    try:
        return datetime.strptime(string, fmt)  # noqa: DTZ007 - come Home Assistant
    except (ValueError, AttributeError, TypeError):
        if default is _MANCANTE:
            _senza_predefinito("strptime", string)
        return default


def _is_datetime(value: Any) -> bool:
    """``value is datetime``."""
    return isinstance(value, datetime)


def _is_string_like(value: Any) -> bool:
    """``value is string_like``."""
    return isinstance(value, (str, bytes, bytearray))


def _is_list(value: Any) -> bool:
    """``value is list``."""
    return isinstance(value, list)


def _is_set(value: Any) -> bool:
    """``value is set``."""
    return isinstance(value, set)


def _is_tuple(value: Any) -> bool:
    """``value is tuple``."""
    return isinstance(value, tuple)


# --- Uscita nel testo -------------------------------------------------------------------

_DIZIONARI = (dict, ReadOnlyDict)
_CONTENITORI = (list, set, tuple)


def _finalizza(valore: Any, annidato: bool = False) -> Any:
    """``_finalize_output`` di Home Assistant: i membri ReprEnum dentro liste, insiemi,
    tuple e dizionari (anche ReadOnlyDict) diventano il loro valore, così il testo si
    rilegge con ``literal_eval``; ReadOnlyDict diventa dict. Gli altri tipi restano."""
    if annidato and isinstance(valore, ReprEnum):
        return valore.value
    tipo = type(valore)
    if tipo in _DIZIONARI:
        return {
            _finalizza(chiave, True): _finalizza(voce, True)
            for chiave, voce in valore.items()
        }
    if tipo in _CONTENITORI:
        return tipo(_finalizza(voce, True) for voce in valore)
    return valore


def testo(valore: Any) -> str:
    """Quello che ``{{ valore }}`` scrive: ``str`` del valore dopo ``finalize``.

    Indefinito = ``''``, ``None`` = ``'None'``, ``21.0`` = ``'21.0'``, ``True`` = ``'True'``,
    liste e dizionari come ``str`` di Python.
    """
    if type(valore) is str:
        return valore
    return str(_finalizza(valore))


def concat(*parti: Any) -> str:
    """L'operatore ``~``: ``str`` di ogni parte, senza ``finalize`` (``str_join``)."""
    return "".join(map(str, parti))


# --- L'ambiente Jinja di riferimento ----------------------------------------------------


class _Registro(dict):
    """Filtri o test per nome: un nome che non c'è è un ``ErroreTemplate``.

    Jinja cerca il filtro (o il test) solo quando lo usa, come in ``map('nome')`` sul primo
    elemento: l'errore arriva nello stesso momento in cui arriva in Home Assistant
    (``TemplateRuntimeError: No filter named ...``). Jinja lo cerca con ``get``
    (``Environment._filter_test_common``); con ``[]`` lo cercano solo i modelli compilati,
    e questo ambiente non ne compila.
    """

    def __init__(self, tipo: str, voci: dict[str, Any]) -> None:
        super().__init__(voci)
        self.tipo = tipo

    def get(self, nome: Any, predefinito: Any = None) -> Any:
        if nome in self:
            return self[nome]
        raise ErroreTemplate(f"No {self.tipo} named {nome!r}.")


class _Ambiente(ImmutableSandboxedEnvironment):
    """Come ``TemplateEnvironment`` di Home Assistant, senza le parti che usano ``hass``."""

    def is_safe_attribute(self, obj: Any, attr: str, value: Any) -> bool:
        # Come Home Assistant: gli attributi di loop e namespace sono sempre leggibili
        # (quelli di loop se non iniziano con «_»).
        if isinstance(obj, (LoopContext, AsyncLoopContext)):
            return attr[0] != "_"
        if isinstance(obj, Namespace):
            return True
        return super().is_safe_attribute(obj, attr, value)


_AMBIENTE = _Ambiente(undefined=Indefinito, finalize=_finalizza)
_AMBIENTE.filters.update(
    {
        "float": f_float,
        "int": f_int,
        "round": f_round,
        "bool": f_bool,
        "is_number": f_is_number,
        "regex_match": t_match,
        "regex_search": _cerca,
        "regex_replace": f_regex_replace,
        "regex_findall": _trova_tutti,
        "regex_findall_index": _trova_indice,
        "slugify": f_slugify,
        "from_json": f_from_json,
        "log": log,
        "as_timestamp": as_timestamp,
        "as_datetime": as_datetime,
    }
)
_AMBIENTE.tests.update(
    {
        "match": t_match,
        "search": _cerca,
        "is_number": f_is_number,
        "datetime": _is_datetime,
        "string_like": _is_string_like,
        "list": _is_list,
        "set": _is_set,
        "tuple": _is_tuple,
    }
)
_AMBIENTE.filters = _Registro("filter", _AMBIENTE.filters)
_AMBIENTE.tests = _Registro("test", _AMBIENTE.tests)
# Il contesto passato ai filtri che lo chiedono (map, select...): nessuna variabile.
_CONTESTO = _AMBIENTE.context_class(_AMBIENTE, {}, None, {})


def attributo(obj: Any, nome: str) -> Any:
    """``obj.nome``: prima l'attributo, poi l'elemento, altrimenti indefinito.

    Un attributo non sicuro per la sandbox (che inizia con ``_``, o che modifica una
    lista, un dizionario o un insieme, come ``append`` o ``update``) è un indefinito che
    dà errore appena si usa (``SecurityError``), come in Home Assistant.
    """
    return _AMBIENTE.getattr(obj, nome)


def elemento(obj: Any, chiave: Any) -> Any:
    """``obj[chiave]``: prima l'elemento, poi l'attributo, altrimenti indefinito.

    Con uno ``slice`` (``obj[a:b]``) è l'operazione di Python, come in Jinja.
    """
    if type(chiave) is slice:
        return obj[chiave]
    return _AMBIENTE.getitem(obj, chiave)


def chiama(funzione: Any, *args: Any, **kwargs: Any) -> Any:
    """``funzione(*args, **kwargs)`` dentro la sandbox (per esempio ``x.split(',')``).

    Chiamare un indefinito o una funzione non sicura è un errore; ``str.format`` è
    quello della sandbox (lo restituisce già ``attributo``).
    """
    return _AMBIENTE.call(_CONTESTO, funzione, *args, **kwargs)


# --- Operatori --------------------------------------------------------------------------
# La sandbox di Home Assistant non intercetta nessun operatore: sono quelli di Python,
# con gli errori dell'indefinito (``jinja2.Undefined`` li definisce tutti).


def somma(a: Any, b: Any) -> Any:
    """``a + b``."""
    return a + b


def sottrai(a: Any, b: Any) -> Any:
    """``a - b``."""
    return a - b


def moltiplica(a: Any, b: Any) -> Any:
    """``a * b``."""
    return a * b


def dividi(a: Any, b: Any) -> Any:
    """``a / b``."""
    return a / b


def dividi_intero(a: Any, b: Any) -> Any:
    """``a // b``."""
    return a // b


def resto(a: Any, b: Any) -> Any:
    """``a % b``."""
    return a % b


def potenza(a: Any, b: Any) -> Any:
    """``a ** b``."""
    return a**b


def nega(a: Any) -> Any:
    """``-a``."""
    return -a


def positivo(a: Any) -> Any:
    """``+a``."""
    return +a


def contiene(contenitore: Any, valore: Any) -> bool:
    """``valore in contenitore``."""
    return valore in contenitore


# --- Filtri di Jinja --------------------------------------------------------------------


def _filtro_jinja(nome: str) -> Callable[..., Any]:
    """Il filtro ``nome`` dell'ambiente, chiamato come lo chiama Jinja."""
    funzione = _AMBIENTE.filters[nome]
    if getattr(funzione, "jinja_pass_arg", None) is None:
        return funzione

    def filtro(value: Any, *args: Any, **kwargs: Any) -> Any:
        return _AMBIENTE.call_filter(nome, value, args, kwargs, context=_CONTESTO)

    filtro.__name__ = filtro.__qualname__ = f"f_{nome}"
    filtro.__doc__ = f"``value | {nome}(...)`` (filtro di Jinja)."
    return filtro


f_trim = _filtro_jinja("trim")
f_lower = _filtro_jinja("lower")
f_capitalize = _filtro_jinja("capitalize")
f_list = _filtro_jinja("list")
f_join = _filtro_jinja("join")
f_length = _filtro_jinja("length")
f_count = _filtro_jinja("count")
f_default = _filtro_jinja("default")
f_unique = _filtro_jinja("unique")
f_max = _filtro_jinja("max")
f_min = _filtro_jinja("min")
f_sort = _filtro_jinja("sort")
f_sum = _filtro_jinja("sum")
f_replace = _filtro_jinja("replace")
f_string = _filtro_jinja("string")
f_abs = _filtro_jinja("abs")

_map = _filtro_jinja("map")
_select = _filtro_jinja("select")
_reject = _filtro_jinja("reject")
_selectattr = _filtro_jinja("selectattr")
_rejectattr = _filtro_jinja("rejectattr")


def _funzione(args: tuple[Any, ...], posto: int) -> bool:
    """Vero se al posto del nome del filtro (o del test) c'è una funzione Python."""
    if len(args) <= posto:
        return False
    voce = args[posto]
    return callable(voce) and not isinstance(voce, (str, jinja2.Undefined))


def _mappa_con_funzione(
    value: Any, funzione: Callable[..., Any], args: tuple, kwargs: dict
) -> Iterator[Any]:
    """``map`` con una funzione al posto del nome: come ``do_map`` di Jinja."""
    if value:
        for voce in value:
            yield funzione(voce, *args, **kwargs)


def _scegli_con_funzione(
    value: Any, args: tuple, kwargs: dict, rifiuta: bool, per_attributo: bool
) -> Iterator[Any]:
    """``select``/``reject``/``selectattr``/``rejectattr`` con una funzione al posto del
    nome del test: come ``select_or_reject`` di Jinja."""
    if value:
        if per_attributo:
            leggi = jinja2.filters.make_attrgetter(_AMBIENTE, args[0])
            posto = 1
        else:

            def leggi(voce: Any) -> Any:
                return voce

            posto = 0
        funzione, altri = args[posto], args[posto + 1 :]
        for voce in value:
            esito = funzione(leggi(voce), *altri, **kwargs)
            if (not esito) if rifiuta else esito:
                yield voce


def f_map(value: Any, *args: Any, **kwargs: Any) -> Any:
    """``value | map('filtro', ...)`` o ``value | map(attribute='a', default=...)``.

    Restituisce un generatore come Jinja (gli errori arrivano mentre si legge).
    """
    if _funzione(args, 0):
        return _mappa_con_funzione(value, args[0], args[1:], kwargs)
    return _map(value, *args, **kwargs)


def f_select(value: Any, *args: Any, **kwargs: Any) -> Any:
    """``value | select('test', ...)`` (generatore)."""
    if _funzione(args, 0):
        return _scegli_con_funzione(value, args, kwargs, False, False)
    return _select(value, *args, **kwargs)


def f_reject(value: Any, *args: Any, **kwargs: Any) -> Any:
    """``value | reject('test', ...)`` (generatore)."""
    if _funzione(args, 0):
        return _scegli_con_funzione(value, args, kwargs, True, False)
    return _reject(value, *args, **kwargs)


def f_selectattr(value: Any, *args: Any, **kwargs: Any) -> Any:
    """``value | selectattr('attributo', 'test', ...)`` (generatore)."""
    if _funzione(args, 1):
        return _scegli_con_funzione(value, args, kwargs, False, True)
    return _selectattr(value, *args, **kwargs)


def f_rejectattr(value: Any, *args: Any, **kwargs: Any) -> Any:
    """``value | rejectattr('attributo', 'test', ...)`` (generatore)."""
    if _funzione(args, 1):
        return _scegli_con_funzione(value, args, kwargs, True, True)
    return _rejectattr(value, *args, **kwargs)


# --- Test -------------------------------------------------------------------------------


def t_defined(value: Any) -> bool:
    """``value is defined``."""
    return not isinstance(value, jinja2.Undefined)


def t_none(value: Any) -> bool:
    """``value is none``."""
    return value is None


def t_mapping(value: Any) -> bool:
    """``value is mapping``."""
    return jinja2.tests.test_mapping(value)


def prova(nome: Any, valore: Any, *args: Any, **kwargs: Any) -> bool:
    """``valore is nome(*args)`` per nome (i test di Jinja e quelli di Home Assistant senza
    ``hass``), o con la funzione Python del test al posto del nome."""
    if callable(nome) and not isinstance(nome, (str, jinja2.Undefined)):
        return nome(valore, *args, **kwargs)
    return _AMBIENTE.call_test(nome, valore, args, kwargs, context=_CONTESTO)


# --- Funzioni globali -------------------------------------------------------------------


def namespace(*args: Any, **kwargs: Any) -> Namespace:
    """``namespace(...)`` di Jinja."""
    return Namespace(*args, **kwargs)


def imposta_ns(ns: Any, nome: str, valore: Any) -> None:
    """``{% set ns.nome = valore %}``: solo su un namespace, come Jinja."""
    if not isinstance(ns, Namespace):
        raise jinja2.TemplateRuntimeError(
            "cannot assign attribute on non-namespace object"
        )
    ns[nome] = valore


# --- Interpretazione dei risultati ------------------------------------------------------


def condizione(resa: str) -> bool:
    """Esito di una condizione ``template``: il testo reso (senza spazi ai bordi), in
    minuscolo, è ``true`` (``helpers/condition`` ``async_template``)."""
    return resa.strip().lower() == "true"


def trigger_vero(valore: Any) -> bool:
    """Il risultato di un trigger ``template`` vale vero (``result_as_boolean``).

    ``valore`` è il risultato interpretato (``interpreta``); un testo si interpreta qui
    (``interpreta`` non cambia un testo che ha già interpretato). Veri: ``True``, i numeri
    diversi da 0 e i testi ``1``, ``true``, ``yes``, ``on``, ``enable`` (senza maiuscole e
    spazi ai bordi); tutto il resto è falso.
    """
    if isinstance(valore, str):
        valore = interpreta(valore)
    if valore is None:
        return False
    try:
        return _booleano(valore)
    except _NonBooleano:
        return False


# --- Variabili e cicli nel codice tradotto ----------------------------------------------

# Una variabile di un ambito non ancora assegnata (come ``missing`` del codice di Jinja).
MANCANTE = jinja2.utils.missing


def leggi(valore: Any, nome: str) -> Any:
    """Lettura di una variabile assegnata nel modello: indefinita se non ancora assegnata
    (come ``undefined(name=...) if l_0_x is missing else l_0_x``)."""
    if valore is MANCANTE:
        return indefinito(nome)
    return valore


def indefinito_senza_else() -> jinja2.Undefined:
    """``a if b`` senza ``else`` quando ``b`` è falso (come ``cond_expr_undefined``)."""
    return jinja2.Undefined(
        "the inline if-expression evaluated to false and no else section was defined."
    )


__all__ += ["MANCANTE", "LoopContext", "indefinito_senza_else", "leggi"]
