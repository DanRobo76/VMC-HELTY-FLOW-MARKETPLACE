"""jinja.py contro il vero motore dei modelli di Home Assistant, su molti valori.

Per ogni costrutto Home Assistant rende (``Template(...).async_render``) un modello come
``{% set r = x | float(d) %}<{{ r }}>{{ r | typeof }}`` per ogni combinazione di valori
(una variabile assente è un indefinito) e lo si confronta con il testo (``jinja.testo``)
e il tipo del risultato della funzione di jinja.py con gli stessi valori. Un errore di
Home Assistant (``TemplateError``) deve essere un'eccezione della funzione, e viceversa;
per gli errori di Jinja (indefinito, sandbox, filtro o test sconosciuto) deve coincidere
anche il messaggio. Si accetta solo il 100 % di accordo.

Con Home Assistant 2026.10 (l'ambiente locale dei test) alcuni casi danno errore dove il
2026.11 (CI e minimo dichiarato in hacs.json) dà il predefinito o un altro risultato:
``OverflowError`` e ``ZeroDivisionError`` in float, int, round, is_number e log, cifre
non ASCII e ``RecursionError`` nell'interpretazione dei risultati. Con il 2026.10 questi
casi si contano a parte e non si confrontano; con il 2026.11 si confrontano tutti.
"""

from __future__ import annotations

import itertools
import logging
import math
import re
from collections import Counter
from collections.abc import Callable, Iterator
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum, IntEnum, StrEnum
from fractions import Fraction
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import jinja2
import pytest
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import TemplateError
from homeassistant.helpers import condition
from homeassistant.helpers.template import ResultWrapper, Template, result_as_boolean
from homeassistant.util.read_only_dict import ReadOnlyDict
from homeassistant.util.yaml.loader import parse_yaml
from jinja2 import nodes

from custom_components.vmc_master import trasforma
from custom_components.vmc_master.nativa import risultato
from custom_components.vmc_master.nativa.motore import jinja

HA_2026_11 = (MAJOR_VERSION, MINOR_VERSION) >= (2026, 11)
PACKAGE = (
    Path(__file__).resolve().parents[3] / "custom_components" / "vmc_master" / "package"
)

# Variabile assente dal modello: in Home Assistant è un indefinito.
INDEFINITO: Any = type("Assente", (), {"__repr__": lambda self: "INDEFINITO"})()

_INDIRIZZO = re.compile(r" at 0x[0-9a-fA-F]+")


# --- Valori -----------------------------------------------------------------------------


class Colore(StrEnum):
    ROSSO = "rosso"


class Livello(IntEnum):
    UNO = 1


class Semplice(Enum):
    A = "a"


ROMA = ZoneInfo("Europe/Rome")

STRINGHE = [
    "21.30",
    "21",
    "0",
    "-3",
    "007",
    "abc",
    "",
    " 5 ",
    "unknown",
    "unavailable",
    "None",
    "True",
    "true",
    "False",
    "on",
    "off",
    "yes",
    "enable",
    "1",
    "1.0",
    "1e3",
    "0x10",
    "nan",
    "inf",
    "-inf",
    "1e400",
    "Velocità 1",
    "città",
    "ÉLAN ß",
    "٣",
    "１２",
    "+5",
    ".5",
    "5.",
    "-0",
    "1_000",
    "1,5",
    "  ",
    "\t7\n",
    "[1, 2]",
    '{"a": 1}',
    "12:30",
    "24:00",
    "2026-11-25 10:30:00",
    "2026-11-25T10:30:00+01:00",
    "2026-11-25",
    "25/11/2026",
    "Free 2",
    "device_tracker.tel",
    "timer.vmc_master_lettura_x",
    "9.0.0b41",
    "192.168.1.50",
    "A",
    "a,b,,c",
    "VMGO,00002\r\n",
    "Aggiorna Elenco Media Player",
]
NUMERI = [
    0,
    1,
    -1,
    2,
    21,
    255,
    -7,
    10**16,
    10**400,
    21.0,
    21.3,
    0.1 + 0.2,
    1e16,
    -0.0,
    0.5,
    1.5,
    2.5,
    -2.5,
    2.675,
    1e-7,
    math.nan,
    math.inf,
    -math.inf,
    True,
    False,
    Decimal("1.5"),
    Fraction(1, 3),
    1j,
]
STATI = [
    {
        "state": "on",
        "mean": 1.5,
        "entity_id": "sensor.vmc_master_ip",
        "start": 5,
        "attributes": {"device_class": "temperature", "restored": True},
    },
    {
        "state": "off",
        "entity_id": "sensor.vmc_sala_ip",
        "start": 1,
        "attributes": {"device_class": "humidity"},
    },
    {"state": "unavailable", "mean": None, "start": 3, "attributes": {}},
    {"state": "On", "mean": 0, "entity_id": "light.x", "start": 2},
]
CONTENITORI = [
    None,
    [],
    [1, 2, 3],
    [3, 1, 2],
    ["a", "B", "a"],
    [" a ", "B ", "21"],
    ["21.5", "x", "3", ""],
    [1, "a"],
    [None, 0, ""],
    [[1], [2]],
    [math.inf, 1],
    [
        "Free 1",
        "device_tracker.a",
        "Aggiorna Elenco Media Player",
        "x_co2_interna_selezionata",
    ],
    (1, 2),
    (),
    {},
    {"a": 1, "b": "x"},
    {"state": "on", "mean": 1.5},
    {1, 2},
    ReadOnlyDict({"a": 1, "b": [Livello.UNO]}),
    STATI,
    [jinja.namespace(state="on")],
    range(3),
    b"abc",
]
DATE = [
    datetime(2026, 11, 25, 10, 30, 15, 123456, tzinfo=ROMA),
    datetime(2026, 11, 25, 10, 30),  # noqa: DTZ001 - data senza fuso voluta
    datetime(2026, 1, 1, tzinfo=UTC),
    date(2026, 11, 25),
    time(10, 30),
    timedelta(hours=1, minutes=30),
    timedelta(days=-1, seconds=5),
    timedelta(0),
]
ENUM = [
    Colore.ROSSO,
    Livello.UNO,
    Semplice.A,
    [Colore.ROSSO, Livello.UNO, Semplice.A],
    {"k": Colore.ROSSO, Livello.UNO: (Colore.ROSSO, [Livello.UNO])},
    [ReadOnlyDict({"x": Colore.ROSSO})],
    {Colore.ROSSO},
    (Semplice.A, Livello.UNO),
]
VALORI = [
    *STRINGHE,
    *NUMERI,
    *CONTENITORI,
    *DATE,
    *ENUM,
    jinja.namespace(a=1),
    INDEFINITO,
]

# Dominio più piccolo per le coppie (operatori): niente interi enormi.
ARITMETICA = [
    0,
    1,
    -3,
    7,
    255,
    2.5,
    -0.0,
    0.1,
    math.nan,
    math.inf,
    True,
    False,
    None,
    "",
    "abc",
    "5",
    "%s",
    [1, 2],
    [],
    (1,),
    {"a": 1},
    DATE[0],
    DATE[1],
    DATE[5],
    date(2026, 1, 1),
    INDEFINITO,
]


# --- Il banco di confronto --------------------------------------------------------------


def _argomenti(variabili: dict[str, Any]) -> dict[str, Any]:
    return {
        n: jinja.indefinito(n) if v is INDEFINITO else v for n, v in variabili.items()
    }


def _tipo(valore: Any) -> str:
    return (
        "Undefined" if isinstance(valore, jinja2.Undefined) else type(valore).__name__
    )


def _breve(valore: Any) -> str:
    testo = repr(valore)
    return testo if len(testo) < 80 else testo[:77] + "..."


class Banco:
    """Rende i modelli con Home Assistant e li confronta con le funzioni di jinja.py."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.modelli: dict[str, Template] = {}
        self.confronti: Counter[str] = Counter()
        self.messaggi = 0
        self.noti_2026_10: Counter[str] = Counter()
        self.differenze: list[str] = []

    def modello(self, sorgente: str) -> Template:
        if (modello := self.modelli.get(sorgente)) is None:
            modello = self.modelli[sorgente] = Template(sorgente, self.hass)
        return modello

    def rendi(
        self, sorgente: str, variabili: dict[str, Any], parse_result: bool = False
    ) -> Any:
        presenti = {n: v for n, v in variabili.items() if v is not INDEFINITO}
        return self.modello(sorgente).async_render(presenti, parse_result=parse_result)

    def _ha(
        self, sorgente: str, variabili: dict[str, Any]
    ) -> tuple[str | None, Exception | None]:
        try:
            return self.rendi(sorgente, variabili), None
        except TemplateError as err:
            return None, err

    def confronta(
        self,
        costrutto: str,
        espressione: str,
        calcolo: Callable[..., Any],
        **variabili: Any,
    ) -> None:
        """``{% set r = espressione %}`` in Home Assistant contro ``calcolo(**variabili)``."""
        sorgente = "{% set r = " + espressione + " %}<{{ r }}>{{ r | typeof }}"
        atteso, errore = self._ha(sorgente, variabili)
        if atteso is not None:
            resa, _, tipo = atteso.rpartition(">")
            atteso = f"{resa}>{'Undefined' if tipo == 'LoggingUndefined' else tipo}"
        try:
            valore = calcolo(**_argomenti(variabili))
            ottenuto, eccezione = f"<{jinja.testo(valore)}>{_tipo(valore)}", None
        except Exception as exc:  # noqa: BLE001
            ottenuto, eccezione = None, exc
        self._registra(
            costrutto, espressione, variabili, atteso, errore, ottenuto, eccezione
        )

    def confronta_resa(
        self,
        costrutto: str,
        sorgente: str,
        calcolo: Callable[..., str],
        **variabili: Any,
    ) -> None:
        """Il testo reso da ``sorgente`` contro il testo di ``calcolo(**variabili)``."""
        atteso, errore = self._ha(sorgente, variabili)
        try:
            ottenuto, eccezione = calcolo(**_argomenti(variabili)), None
        except Exception as exc:  # noqa: BLE001
            ottenuto, eccezione = None, exc
        self._registra(
            costrutto, sorgente, variabili, atteso, errore, ottenuto, eccezione
        )

    def confronta_valori(
        self, costrutto: str, descrizione: str, atteso: Any, ottenuto: Any, uguali: bool
    ) -> None:
        self.confronti[costrutto] += 1
        if not uguali:
            self.differenze.append(
                f"{costrutto}: {descrizione}: HA {_breve(atteso)} / jinja.py {_breve(ottenuto)}"
            )

    def nota_2026_10(self, costrutto: str) -> None:
        self.noti_2026_10[costrutto] += 1

    def _registra(
        self, costrutto, espressione, variabili, atteso, errore, ottenuto, eccezione
    ) -> None:
        if (
            not HA_2026_11
            and errore is not None
            and eccezione is None
            and isinstance(errore.__cause__, (OverflowError, ZeroDivisionError))
        ):
            self.nota_2026_10(costrutto)
            return
        self.confronti[costrutto] += 1
        if atteso is not None:
            atteso = _INDIRIZZO.sub(" at 0x…", atteso)
        if ottenuto is not None:
            ottenuto = _INDIRIZZO.sub(" at 0x…", ottenuto)
        descrizione = f"{espressione} con " + ", ".join(
            f"{n}={_breve(v)}" for n, v in variabili.items()
        )
        if atteso != ottenuto:
            ha = atteso if errore is None else f"errore {errore}"
            mio = (
                ottenuto
                if eccezione is None
                else f"errore {type(eccezione).__name__}: {eccezione}"
            )
            self.differenze.append(
                f"{costrutto}: {descrizione}: HA {ha!r} / jinja.py {mio!r}"
            )
        elif isinstance(eccezione, (jinja2.TemplateError, jinja.ErroreTemplate)):
            # Errori di Jinja: stesso messaggio («UndefinedError: 'x' is undefined»).
            self.messaggi += 1
            # Il nome della classe dell'indefinito è diverso (LoggingUndefined / Indefinito).
            if str(errore).partition(": ")[2].replace(
                "LoggingUndefined", "Indefinito"
            ) != str(eccezione):
                self.differenze.append(
                    f"{costrutto}: {descrizione}: messaggio HA {errore} / jinja.py {eccezione}"
                )

    def verifica(self, minimo: int) -> None:
        totale = sum(self.confronti.values())
        print(
            f"\n{totale} confronti, {self.messaggi} messaggi d'errore uguali; noti 2026.10: {dict(self.noti_2026_10)}"
        )
        for costrutto, numero in sorted(self.confronti.items()):
            print(f"  {costrutto}: {numero}")
        assert not self.differenze, f"{len(self.differenze)} differenze:\n" + "\n".join(
            self.differenze[:60]
        )
        assert totale >= minimo, totale
        if HA_2026_11:
            assert not self.noti_2026_10


@pytest.fixture
def banco(hass: HomeAssistant) -> Iterator[Banco]:
    """Un banco di confronto; gli avvisi dell'indefinito di HA non vanno nel registro."""
    registro = logging.getLogger("homeassistant.helpers.template")
    livello = registro.level
    registro.setLevel(logging.CRITICAL)
    yield Banco(hass)
    registro.setLevel(livello)


# --- Casi ---------------------------------------------------------------------------------


def casi_testo(banco: Banco) -> None:
    for x in VALORI:
        banco.confronta_resa("testo", "<{{ x }}>", lambda x: f"<{jinja.testo(x)}>", x=x)
        banco.confronta("testo", "x", lambda x: x, x=x)
        banco.confronta_resa(
            "testo",
            "<{{ x }}{{ x }}>",
            lambda x: f"<{jinja.testo(x)}{jinja.testo(x)}>",
            x=x,
        )
    for a, b in itertools.product(ARITMETICA + ENUM + [ReadOnlyDict({"a": 1})], VALORI):
        banco.confronta_resa(
            "concat", "<{{ a ~ b }}>", lambda a, b: f"<{jinja.concat(a, b)}>", a=a, b=b
        )
    for a, b in itertools.product(ARITMETICA, repeat=2):
        banco.confronta_resa(
            "concat",
            "<{{ a ~ '-' ~ b ~ 1 }}>",
            lambda a, b: f"<{jinja.concat(a, '-', b, 1)}>",
            a=a,
            b=b,
        )


def casi_numeri(banco: Banco) -> None:
    c = banco.confronta
    for x, d in itertools.product(VALORI, [0, None, -1, "x", 65, 0.5, [], INDEFINITO]):
        c("float", "x | float(d)", lambda x, d: jinja.f_float(x, d), x=x, d=d)
    for x in VALORI:
        c("float", "x | float", lambda x: jinja.f_float(x), x=x)
        c("float", "x | float(default=0)", lambda x: jinja.f_float(x, default=0), x=x)
        c("float", "float(x, 1)", lambda x: jinja.f_float(x, 1), x=x)
    for x, d in itertools.product(VALORI, [0, 32, -1, None, "x", INDEFINITO]):
        c("int", "x | int(d)", lambda x, d: jinja.f_int(x, d), x=x, d=d)
    for x, (d, b) in itertools.product(
        VALORI, [(0, 16), (0, 2), (0, 8), (0, 0), (None, 36), (0, "a"), (0, 1)]
    ):
        c("int", "x | int(d, b)", lambda x, d, b: jinja.f_int(x, d, b), x=x, d=d, b=b)
    for x in VALORI:
        c("int", "x | int", lambda x: jinja.f_int(x), x=x)
        c("int", "x | int(default=5)", lambda x: jinja.f_int(x, default=5), x=x)
        c("int", "x | int(base=16)", lambda x: jinja.f_int(x, base=16), x=x)
        c("int", "int(x, 3)", lambda x: jinja.f_int(x, 3), x=x)
    for x, p in itertools.product(
        VALORI, [0, 1, 2, 3, 6, -1, "a", None, 1.5, INDEFINITO]
    ):
        c("round", "x | round(p)", lambda x, p: jinja.f_round(x, p), x=x, p=p)
    for x, p, m in itertools.product(
        VALORI, [0, 1, 2], ["common", "ceil", "floor", "half", "xyz", INDEFINITO]
    ):
        c(
            "round",
            "x | round(p, m)",
            lambda x, p, m: jinja.f_round(x, p, m),
            x=x,
            p=p,
            m=m,
        )
    for x, d in itertools.product(VALORI, ["def", None, 0]):
        c(
            "round",
            "x | round(1, 'common', d)",
            lambda x, d: jinja.f_round(x, 1, "common", d),
            x=x,
            d=d,
        )
        c(
            "round",
            "x | round(0, 'ceil', d)",
            lambda x, d: jinja.f_round(x, 0, "ceil", d),
            x=x,
            d=d,
        )
    for x in VALORI:
        c("round", "x | round", lambda x: jinja.f_round(x), x=x)
        c("round", "x | round(default=0)", lambda x: jinja.f_round(x, default=0), x=x)
        c(
            "round",
            "x | round(2, default='z')",
            lambda x: jinja.f_round(x, 2, default="z"),
            x=x,
        )
        c(
            "round",
            "x | round(method='floor')",
            lambda x: jinja.f_round(x, method="floor"),
            x=x,
        )
        c("is_number", "x | is_number", lambda x: jinja.f_is_number(x), x=x)
        c("is_number", "is_number(x)", lambda x: jinja.f_is_number(x), x=x)
        c("is_number", "x is is_number", lambda x: jinja.prova("is_number", x), x=x)
        c("abs", "x | abs", lambda x: jinja.f_abs(x), x=x)
        c("bool", "x | bool", lambda x: jinja.f_bool(x), x=x)
        c("log", "log(x)", lambda x: jinja.log(x), x=x)
        c("log", "x | log(10, 0)", lambda x: jinja.log(x, 10, 0), x=x)
    for x, d in itertools.product(VALORI, [False, None, "x", INDEFINITO]):
        c("bool", "x | bool(d)", lambda x, d: jinja.f_bool(x, d), x=x, d=d)
        c("bool", "bool(x, d)", lambda x, d: jinja.f_bool(x, d), x=x, d=d)
    for x, b in itertools.product(
        [1, 100, 2.5, "8", 0, -1, "a", None, INDEFINITO],
        [10, 2, 1, 0, "x", math.e, INDEFINITO],
    ):
        c("log", "log(x, b)", lambda x, b: jinja.log(x, b), x=x, b=b)
        c("log", "log(x, b, -1)", lambda x, b: jinja.log(x, b, -1), x=x, b=b)


def casi_testi(banco: Banco) -> None:
    c = banco.confronta
    for x in VALORI:
        c("trim", "x | trim", lambda x: jinja.f_trim(x), x=x)
        c("lower", "x | lower", lambda x: jinja.f_lower(x), x=x)
        c("capitalize", "x | capitalize", lambda x: jinja.f_capitalize(x), x=x)
        c("string", "x | string", lambda x: jinja.f_string(x), x=x)
        c("length", "x | length", lambda x: jinja.f_length(x), x=x)
        c("count", "x | count", lambda x: jinja.f_count(x), x=x)
        c("list", "x | list", lambda x: jinja.f_list(x), x=x)
        c("from_json", "x | from_json", lambda x: jinja.f_from_json(x), x=x)
        c("from_json", "x | from_json(0)", lambda x: jinja.f_from_json(x, 0), x=x)
        c("default", "x | default", lambda x: jinja.f_default(x), x=x)
        c("join", "x | join", lambda x: jinja.f_join(x), x=x)
        c(
            "join",
            "x | join(',', attribute='state')",
            lambda x: jinja.f_join(x, ",", attribute="state"),
            x=x,
        )
        c("slugify", "x | slugify", lambda x: jinja.f_slugify(x), x=x)
    for x, s in itertools.product(VALORI, ["x", " 5", None, INDEFINITO]):
        c("trim", "x | trim(s)", lambda x, s: jinja.f_trim(x, s), x=x, s=s)
    for x, d in itertools.product(VALORI, ["", 0, [], False, "x", None, INDEFINITO]):
        c("default", "x | default(d)", lambda x, d: jinja.f_default(x, d), x=x, d=d)
        c(
            "default",
            "x | default(d, true)",
            lambda x, d: jinja.f_default(x, d, True),
            x=x,
            d=d,
        )
    for x, s in itertools.product(VALORI, [",", "|", " · ", "", 1, INDEFINITO]):
        c("join", "x | join(s)", lambda x, s: jinja.f_join(x, s), x=x, s=s)
    sostituzioni = [
        ("a", "b"),
        ("Velocità ", ""),
        ("timer.vmc_master_lettura_", ""),
        ("\\", ""),
        ('"', ""),
        ("{}", "X"),
        (" · ", ", "),
        ("", "-"),
        (1, 2),
        ("1", None),
        (INDEFINITO, "x"),
        ("a", INDEFINITO),
    ]
    for x, (a, b) in itertools.product(VALORI, sostituzioni):
        c(
            "replace",
            "x | replace(a, b)",
            lambda x, a, b: jinja.f_replace(x, a, b),
            x=x,
            a=a,
            b=b,
        )
    for x, n in itertools.product(VALORI, [1, 0, -1, None, "a"]):
        c(
            "replace",
            "x | replace('a', 'X', n)",
            lambda x, n: jinja.f_replace(x, "a", "X", n),
            x=x,
            n=n,
        )
    espressioni = ["^[^0-9]*", "^", "a", "[", "\\d+", "", "(\\d)(\\d)", "[aeiou]", 5]
    for x, p, s in itertools.product(
        VALORI, espressioni, ["", "X", "\\2\\1", INDEFINITO]
    ):
        c(
            "regex_replace",
            "x | regex_replace(p, s)",
            lambda x, p, s: jinja.f_regex_replace(x, p, s),
            x=x,
            p=p,
            s=s,
        )
    for x, p in itertools.product(VALORI, ["A", "[A-Z]", "é"]):
        c(
            "regex_replace",
            "x | regex_replace(p, '_', true)",
            lambda x, p: jinja.f_regex_replace(x, p, "_", True),
            x=x,
            p=p,
        )
        c(
            "regex_replace",
            "x | regex_replace(find=p)",
            lambda x, p: jinja.f_regex_replace(x, find=p),
            x=x,
            p=p,
        )


def casi_raccolte(banco: Banco) -> None:
    c = banco.confronta
    for x in VALORI:
        c("unique", "x | unique | list", lambda x: jinja.f_list(jinja.f_unique(x)), x=x)
        c(
            "unique",
            "x | unique(true) | list",
            lambda x: jinja.f_list(jinja.f_unique(x, True)),
            x=x,
        )
        c(
            "unique",
            "x | unique(attribute='state') | list",
            lambda x: jinja.f_list(jinja.f_unique(x, attribute="state")),
            x=x,
        )
        c("max", "x | max", lambda x: jinja.f_max(x), x=x)
        c("max", "x | max(true)", lambda x: jinja.f_max(x, True), x=x)
        c(
            "max",
            "x | max(attribute='start')",
            lambda x: jinja.f_max(x, attribute="start"),
            x=x,
        )
        c("min", "x | min", lambda x: jinja.f_min(x), x=x)
        c(
            "min",
            "x | min(attribute='state')",
            lambda x: jinja.f_min(x, attribute="state"),
            x=x,
        )
        c("sort", "x | sort", lambda x: jinja.f_sort(x), x=x)
        c("sort", "x | sort(true)", lambda x: jinja.f_sort(x, True), x=x)
        c("sort", "x | sort(false, true)", lambda x: jinja.f_sort(x, False, True), x=x)
        c(
            "sort",
            "x | sort(attribute='start')",
            lambda x: jinja.f_sort(x, attribute="start"),
            x=x,
        )
        c("sum", "x | sum", lambda x: jinja.f_sum(x), x=x)
        c(
            "sum",
            "x | sum(attribute='start')",
            lambda x: jinja.f_sum(x, attribute="start"),
            x=x,
        )
        c("sum", "x | sum(start=1.5)", lambda x: jinja.f_sum(x, start=1.5), x=x)
        c("sum", "x | sum(start=[])", lambda x: jinja.f_sum(x, start=[]), x=x)


FILTRI_MAP = [
    "int",
    "float",
    "trim",
    "lower",
    "string",
    "slugify",
    "capitalize",
    "length",
    "abs",
    "is_number",
    "bool",
    "round",
    "list",
    "nonexist",
]
FILTRI_MAP_ARG = [
    ("int", 0),
    ("float", 0),
    ("int", 5),
    ("float", "x"),
    ("regex_replace", "^"),
    ("round", 1),
    ("default", "z"),
    ("replace", "a"),
    ("join", ","),
]
FILTRI_MAP_DUE = [
    ("regex_replace", "^", ""),
    ("replace", "a", "b"),
    ("int", 0, 16),
    ("regex_replace", "^[^0-9]*", ""),
]
TEST_SELECT = [
    "string",
    "number",
    "defined",
    "undefined",
    "none",
    "odd",
    "even",
    "lower",
    "upper",
    "mapping",
    "iterable",
    "sequence",
    "boolean",
    "integer",
    "float",
    "true",
    "false",
    "is_number",
    "list",
    "set",
    "tuple",
    "datetime",
    "string_like",
    "callable",
    "nonexist",
]
TEST_SELECT_ARG = [
    ("match", "Free"),
    ("match", "device_tracker"),
    ("match", "[0-9]"),
    ("search", "_selezionata$"),
    ("search", "a"),
    ("equalto", "a"),
    ("eq", 1),
    ("ne", 1),
    ("in", [1, 2]),
    ("in", "abc"),
    ("gt", 1),
    ("ge", 2),
    ("lt", "b"),
    ("divisibleby", 2),
    ("sameas", None),
    ("==", "B"),
    ("eq", "Aggiorna Elenco Media Player"),
    ("match", "["),
]


def casi_map_select(banco: Banco) -> None:
    c = banco.confronta
    for x, f in itertools.product(VALORI, FILTRI_MAP):
        c(
            "map",
            "x | map(f) | list",
            lambda x, f: jinja.f_list(jinja.f_map(x, f)),
            x=x,
            f=f,
        )
    for x, (f, a) in itertools.product(VALORI, FILTRI_MAP_ARG):
        c(
            "map",
            "x | map(f, a) | list",
            lambda x, f, a: jinja.f_list(jinja.f_map(x, f, a)),
            x=x,
            f=f,
            a=a,
        )
    for x, (f, a, b) in itertools.product(VALORI, FILTRI_MAP_DUE):
        c(
            "map",
            "x | map(f, a, b) | list",
            lambda x, f, a, b: jinja.f_list(jinja.f_map(x, f, a, b)),
            x=x,
            f=f,
            a=a,
            b=b,
        )
    for x, a in itertools.product(
        VALORI,
        [
            "state",
            "a",
            "mean",
            "0",
            "attributes.device_class",
            "real",
            "_x",
            INDEFINITO,
        ],
    ):
        c(
            "map",
            "x | map(attribute=a) | list",
            lambda x, a: jinja.f_list(jinja.f_map(x, attribute=a)),
            x=x,
            a=a,
        )
        c(
            "map",
            "x | map(attribute=a, default=0) | list",
            lambda x, a: jinja.f_list(jinja.f_map(x, attribute=a, default=0)),
            x=x,
            a=a,
        )
    for x in VALORI:
        c("map", "x | map | list", lambda x: jinja.f_list(jinja.f_map(x)), x=x)
        c("select", "x | select | list", lambda x: jinja.f_list(jinja.f_select(x)), x=x)
        c("reject", "x | reject | list", lambda x: jinja.f_list(jinja.f_reject(x)), x=x)
        # Una funzione Python al posto del nome (per i filtri e i test che usano hass).
        c(
            "map (funzione)",
            "x | map('int', 0) | list",
            lambda x: jinja.f_list(jinja.f_map(x, jinja.f_int, 0)),
            x=x,
        )
        c(
            "map (funzione)",
            "x | map('trim') | list",
            lambda x: jinja.f_list(jinja.f_map(x, jinja.f_trim)),
            x=x,
        )
        c(
            "select (funzione)",
            "x | select('match', 'a') | list",
            lambda x: jinja.f_list(jinja.f_select(x, jinja.t_match, "a")),
            x=x,
        )
        c(
            "reject (funzione)",
            "x | reject('none') | list",
            lambda x: jinja.f_list(jinja.f_reject(x, jinja.t_none)),
            x=x,
        )
        c(
            "selectattr (funzione)",
            "x | selectattr('state', 'eq', 'on') | list",
            lambda x: jinja.f_list(
                jinja.f_selectattr(x, "state", lambda v, a: v == a, "on")
            ),
            x=x,
        )
        c(
            "rejectattr (funzione)",
            "x | rejectattr('mean', 'defined') | list",
            lambda x: jinja.f_list(jinja.f_rejectattr(x, "mean", jinja.t_defined)),
            x=x,
        )
    for x, t in itertools.product(VALORI, TEST_SELECT):
        c(
            "select",
            "x | select(t) | list",
            lambda x, t: jinja.f_list(jinja.f_select(x, t)),
            x=x,
            t=t,
        )
        c(
            "reject",
            "x | reject(t) | list",
            lambda x, t: jinja.f_list(jinja.f_reject(x, t)),
            x=x,
            t=t,
        )
    for x, (t, a) in itertools.product(VALORI, TEST_SELECT_ARG):
        c(
            "select",
            "x | select(t, a) | list",
            lambda x, t, a: jinja.f_list(jinja.f_select(x, t, a)),
            x=x,
            t=t,
            a=a,
        )
        c(
            "reject",
            "x | reject(t, a) | list",
            lambda x, t, a: jinja.f_list(jinja.f_reject(x, t, a)),
            x=x,
            t=t,
            a=a,
        )
    attributi = [
        "state",
        "mean",
        "attributes.device_class",
        "attributes.restored",
        "entity_id",
        "start",
        "0",
        INDEFINITO,
    ]
    for x, a in itertools.product(VALORI, attributi):
        c(
            "selectattr",
            "x | selectattr(a) | list",
            lambda x, a: jinja.f_list(jinja.f_selectattr(x, a)),
            x=x,
            a=a,
        )
        c(
            "rejectattr",
            "x | rejectattr(a) | list",
            lambda x, a: jinja.f_list(jinja.f_rejectattr(x, a)),
            x=x,
            a=a,
        )
        for t in ("defined", "undefined", "none", "string", "nonexist"):
            c(
                "selectattr",
                f"x | selectattr(a, '{t}') | list",
                lambda x, a, t=t: jinja.f_list(jinja.f_selectattr(x, a, t)),
                x=x,
                a=a,
            )
            c(
                "rejectattr",
                f"x | rejectattr(a, '{t}') | list",
                lambda x, a, t=t: jinja.f_list(jinja.f_rejectattr(x, a, t)),
                x=x,
                a=a,
            )
    confronti = [
        ("eq", "on"),
        ("ge", 2),
        ("search", "^o"),
        ("match", "o"),
        ("in", ["on", "off"]),
        ("eq", True),
        ("ne", "on"),
        ("search", "^sensor\\.vmc_[a-z]+_ip$"),
        ("eq", "temperature"),
    ]
    for x, a, (t, v) in itertools.product(VALORI, attributi, confronti):
        c(
            "selectattr",
            "x | selectattr(a, t, v) | list",
            lambda x, a, t, v: jinja.f_list(jinja.f_selectattr(x, a, t, v)),
            x=x,
            a=a,
            t=t,
            v=v,
        )
        c(
            "rejectattr",
            "x | rejectattr(a, t, v) | list",
            lambda x, a, t, v: jinja.f_list(jinja.f_rejectattr(x, a, t, v)),
            x=x,
            a=a,
            t=t,
            v=v,
        )


ESPRESSIONI_REGOLARI = [
    "^[0-9]{2}:[0-9]{2}$",
    "^[0-9]+([.][0-9]+)*(b[0-9]+)?$",
    "^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$",
    "^[A-Za-z0-9_-]{1,10}$",
    "timer\\.vmc_master_lettura_",
    "Free",
    "a",
    "",
    "[",
    "^$",
    "\\d",
    "None",
    "T",
]
TEST_NOMI = [
    "defined",
    "undefined",
    "none",
    "string",
    "number",
    "mapping",
    "sequence",
    "iterable",
    "odd",
    "even",
    "boolean",
    "false",
    "true",
    "integer",
    "float",
    "lower",
    "upper",
    "callable",
    "is_number",
    "list",
    "set",
    "tuple",
    "datetime",
    "string_like",
    "escaped",
]
TEST_CON_ARGOMENTO = [
    "eq",
    "ne",
    "lt",
    "le",
    "gt",
    "ge",
    "in",
    "equalto",
    "sameas",
    "divisibleby",
    "match",
    "search",
    "greaterthan",
    "lessthan",
    "==",
    "!=",
    "<",
    ">=",
]


def casi_test(banco: Banco) -> None:
    c = banco.confronta
    for x in VALORI:
        c("defined", "x is defined", lambda x: jinja.t_defined(x), x=x)
        c("defined", "x is not defined", lambda x: not jinja.t_defined(x), x=x)
        c("none", "x is none", lambda x: jinja.t_none(x), x=x)
        c("mapping", "x is mapping", lambda x: jinja.t_mapping(x), x=x)
        c("prova", "x is nonexist", lambda x: jinja.prova("nonexist", x), x=x)
        c(
            "prova (funzione)",
            "x is match('a')",
            lambda x: jinja.prova(jinja.t_match, x, "a"),
            x=x,
        )
        for nome in TEST_NOMI:
            c("prova", f"x is {nome}", lambda x, nome=nome: jinja.prova(nome, x), x=x)
    for x, p in itertools.product(VALORI, ESPRESSIONI_REGOLARI):
        c("match", "x is match(p)", lambda x, p: jinja.t_match(x, p), x=x, p=p)
        c(
            "match",
            "x is match(p, true)",
            lambda x, p: jinja.t_match(x, p, True),
            x=x,
            p=p,
        )
        c(
            "match",
            "x is match(p, ignorecase=true)",
            lambda x, p: jinja.t_match(x, p, ignorecase=True),
            x=x,
            p=p,
        )
        c("prova", "x is search(p)", lambda x, p: jinja.prova("search", x, p), x=x, p=p)
    for x, y, nome in itertools.product(
        VALORI, ARITMETICA[:20] + ["a", "abc", ["a"]], TEST_CON_ARGOMENTO
    ):
        if nome in ("match", "search") and not isinstance(y, str):
            continue
        if nome[0].isalpha():
            c(
                "prova",
                f"x is {nome}(y)",
                lambda x, y, nome=nome: jinja.prova(nome, x, y),
                x=x,
                y=y,
            )
        else:  # «==», «<»...: solo per nome, in select
            c(
                "prova",
                "[x] | select(t, y) | list",
                lambda x, y, t: [x] if jinja.prova(t, x, y) else [],
                x=x,
                y=y,
                t=nome,
            )


def casi_funzioni(banco: Banco) -> None:
    c = banco.confronta
    formati = [
        "%H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
        "",
        5,
        INDEFINITO,
    ]
    for x, f in itertools.product(VALORI, formati):
        c("strptime", "strptime(x, f)", lambda x, f: jinja.strptime(x, f), x=x, f=f)
        c(
            "strptime",
            "strptime(x, f, 0)",
            lambda x, f: jinja.strptime(x, f, 0),
            x=x,
            f=f,
        )
        c(
            "strptime",
            "strptime(x, f, default=None)",
            lambda x, f: jinja.strptime(x, f, default=None),
            x=x,
            f=f,
        )
    for x, d in itertools.product(
        VALORI + ["2026-11-25T10:30:00Z", "2026-11-25 10:30", "2026-02-30 10:00:00"],
        [0, None, INDEFINITO],
    ):
        c(
            "as_timestamp",
            "as_timestamp(x, d)",
            lambda x, d: jinja.as_timestamp(x, d),
            x=x,
            d=d,
        )
        c(
            "as_timestamp",
            "x | as_timestamp(d)",
            lambda x, d: jinja.as_timestamp(x, d),
            x=x,
            d=d,
        )
        c(
            "as_datetime",
            "as_datetime(x, d)",
            lambda x, d: jinja.as_datetime(x, d),
            x=x,
            d=d,
        )
    for x in VALORI:
        c("as_timestamp", "as_timestamp(x)", lambda x: jinja.as_timestamp(x), x=x)
        c("as_datetime", "as_datetime(x)", lambda x: jinja.as_datetime(x), x=x)
        c("as_datetime", "x | as_datetime", lambda x: jinja.as_datetime(x), x=x)
        c(
            "timedelta",
            "timedelta(days=x)",
            lambda x: jinja.chiama(jinja.timedelta, days=x),
            x=x,
        )
        c(
            "timedelta",
            "x - timedelta(hours=1)",
            lambda x: jinja.sottrai(x, jinja.timedelta(hours=1)),
            x=x,
        )
        c("namespace", "namespace(a=x)", lambda x: jinja.namespace(a=x), x=x)
        c(
            "namespace",
            "namespace(a=x).a",
            lambda x: jinja.attributo(jinja.namespace(a=x), "a"),
            x=x,
        )
        c(
            "namespace",
            "namespace(a=x).b",
            lambda x: jinja.attributo(jinja.namespace(a=x), "b"),
            x=x,
        )
        c(
            "namespace",
            "namespace(_a=x)._a",
            lambda x: jinja.attributo(jinja.namespace(_a=x), "_a"),
            x=x,
        )
        c(
            "namespace",
            "namespace(a=x)._a",
            lambda x: jinja.attributo(jinja.namespace(a=x), "_a"),
            x=x,
        )
        c(
            "namespace",
            "namespace(a=x)['a']",
            lambda x: jinja.elemento(jinja.namespace(a=x), "a"),
            x=x,
        )
        c("namespace", "namespace(x)", lambda x: jinja.chiama(jinja.namespace, x), x=x)

    def assegna(x: Any, y: Any) -> Any:
        ns = jinja.namespace(a=x, l=[])
        jinja.imposta_ns(ns, "a", y)
        jinja.imposta_ns(ns, "l", jinja.somma(jinja.attributo(ns, "l"), [x]))
        return [jinja.attributo(ns, "a"), jinja.attributo(ns, "l"), ns]

    def assegna_altro(x: Any) -> Any:
        jinja.imposta_ns(x, "a", 1)
        return jinja.attributo(x, "a")

    for x, y in itertools.product(VALORI, [1, "b", None, INDEFINITO]):
        banco.confronta_resa(
            "namespace (set)",
            "{% set ns = namespace(a=x, l=[]) %}{% set ns.a = y %}{% set ns.l = ns.l + [x] %}"
            "{% set r = [ns.a, ns.l, ns] %}<{{ r }}>",
            lambda x, y: f"<{jinja.testo(assegna(x, y))}>",
            x=x,
            y=y,
        )
    for x in VALORI:
        banco.confronta_resa(
            "namespace (set)",
            "{% set ns = x %}{% set ns.a = 1 %}<{{ ns.a }}>",
            lambda x: f"<{jinja.testo(assegna_altro(x))}>",
            x=x,
        )


NOMI_ATTRIBUTI = [
    "a",
    "b",
    "state",
    "mean",
    "start",
    "split",
    "get",
    "keys",
    "items",
    "values",
    "append",
    "update",
    "pop",
    "clear",
    "add",
    "sort",
    "reverse",
    "insert",
    "remove",
    "copy",
    "setdefault",
    "popitem",
    "discard",
    "strftime",
    "weekday",
    "year",
    "hour",
    "tzinfo",
    "days",
    "seconds",
    "total_seconds",
    "startswith",
    "index",
    "count",
    "isdigit",
    "upper",
    "lower",
    "format",
    "format_map",
    "replace",
    "isoformat",
    "time",
    "real",
    "imag",
    "denominator",
    "mro",
    "x",
    "_x",
    "__class__",
    "__len__",
    "__dict__",
    "entity_id",
    "attributes",
    "last_changed",
    "gi_frame",
    "conjugate",
    "ultimo",
]
CHIAVI = [
    0,
    1,
    -1,
    2,
    10,
    "a",
    "b",
    "state",
    "split",
    "mean",
    "0",
    None,
    True,
    1.5,
    "attributes",
    "_x",
    "__class__",
    "append",
    "keys",
    "x",
    (1, 2),
    INDEFINITO,
]
METODI = [
    ("x.split(',')", lambda x: jinja.chiama(jinja.attributo(x, "split"), ",")),
    ("x.split()", lambda x: jinja.chiama(jinja.attributo(x, "split"))),
    ("x.split(',', 1)", lambda x: jinja.chiama(jinja.attributo(x, "split"), ",", 1)),
    ("x.split(sep='.')", lambda x: jinja.chiama(jinja.attributo(x, "split"), sep=".")),
    ("x.get('a')", lambda x: jinja.chiama(jinja.attributo(x, "get"), "a")),
    (
        "x.get('state', 0)",
        lambda x: jinja.chiama(jinja.attributo(x, "get"), "state", 0),
    ),
    ("x.get(0)", lambda x: jinja.chiama(jinja.attributo(x, "get"), 0)),
    (
        "x.keys() | list",
        lambda x: jinja.f_list(jinja.chiama(jinja.attributo(x, "keys"))),
    ),
    (
        "x.items() | list",
        lambda x: jinja.f_list(jinja.chiama(jinja.attributo(x, "items"))),
    ),
    (
        "x.values() | list",
        lambda x: jinja.f_list(jinja.chiama(jinja.attributo(x, "values"))),
    ),
    (
        "x.strftime('%H:%M')",
        lambda x: jinja.chiama(jinja.attributo(x, "strftime"), "%H:%M"),
    ),
    (
        "x.strftime('%Y-%m-%d %H:%M:%S %Z %z %a %j')",
        lambda x: jinja.chiama(
            jinja.attributo(x, "strftime"), "%Y-%m-%d %H:%M:%S %Z %z %a %j"
        ),
    ),
    ("x.strftime(5)", lambda x: jinja.chiama(jinja.attributo(x, "strftime"), 5)),
    ("x.weekday()", lambda x: jinja.chiama(jinja.attributo(x, "weekday"))),
    ("x.isoformat()", lambda x: jinja.chiama(jinja.attributo(x, "isoformat"))),
    ("x.time()", lambda x: jinja.chiama(jinja.attributo(x, "time"))),
    ("x.date()", lambda x: jinja.chiama(jinja.attributo(x, "date"))),
    (
        "x.replace(microsecond=0)",
        lambda x: jinja.chiama(jinja.attributo(x, "replace"), microsecond=0),
    ),
    (
        "x.replace(microsecond=0).isoformat()",
        lambda x: jinja.chiama(
            jinja.attributo(
                jinja.chiama(jinja.attributo(x, "replace"), microsecond=0), "isoformat"
            )
        ),
    ),
    (
        "x.replace('a', 'b')",
        lambda x: jinja.chiama(jinja.attributo(x, "replace"), "a", "b"),
    ),
    ("x.total_seconds()", lambda x: jinja.chiama(jinja.attributo(x, "total_seconds"))),
    (
        "x.startswith('a')",
        lambda x: jinja.chiama(jinja.attributo(x, "startswith"), "a"),
    ),
    (
        "x.startswith('timer.')",
        lambda x: jinja.chiama(jinja.attributo(x, "startswith"), "timer."),
    ),
    ("x.endswith('1')", lambda x: jinja.chiama(jinja.attributo(x, "endswith"), "1")),
    ("x.index('a')", lambda x: jinja.chiama(jinja.attributo(x, "index"), "a")),
    ("x.index(1)", lambda x: jinja.chiama(jinja.attributo(x, "index"), 1)),
    ("x.count('a')", lambda x: jinja.chiama(jinja.attributo(x, "count"), "a")),
    ("x.count(1)", lambda x: jinja.chiama(jinja.attributo(x, "count"), 1)),
    ("x.isdigit()", lambda x: jinja.chiama(jinja.attributo(x, "isdigit"))),
    ("x.upper()", lambda x: jinja.chiama(jinja.attributo(x, "upper"))),
    ("x.strip()", lambda x: jinja.chiama(jinja.attributo(x, "strip"))),
    ("x.find('a')", lambda x: jinja.chiama(jinja.attributo(x, "find"), "a")),
    (
        "x.join(['a', 'b'])",
        lambda x: jinja.chiama(jinja.attributo(x, "join"), ["a", "b"]),
    ),
    ("x.append(1)", lambda x: jinja.chiama(jinja.attributo(x, "append"), 1)),
    ("x.update({})", lambda x: jinja.chiama(jinja.attributo(x, "update"), {})),
    ("x.pop()", lambda x: jinja.chiama(jinja.attributo(x, "pop"))),
    ("x.clear()", lambda x: jinja.chiama(jinja.attributo(x, "clear"))),
    ("x.sort()", lambda x: jinja.chiama(jinja.attributo(x, "sort"))),
    ("x.add(1)", lambda x: jinja.chiama(jinja.attributo(x, "add"), 1)),
    ("x.copy()", lambda x: jinja.chiama(jinja.attributo(x, "copy"))),
    ("x.format(1)", lambda x: jinja.chiama(jinja.attributo(x, "format"), 1)),
    ("x.format_map({})", lambda x: jinja.chiama(jinja.attributo(x, "format_map"), {})),
    (
        "'{} {}'.format(x, 1)",
        lambda x: jinja.chiama(jinja.attributo("{} {}", "format"), x, 1),
    ),
    (
        "'{0.real}'.format(x)",
        lambda x: jinja.chiama(jinja.attributo("{0.real}", "format"), x),
    ),
    (
        "'{0.__class__}'.format(x)",
        lambda x: jinja.chiama(jinja.attributo("{0.__class__}", "format"), x),
    ),
    (
        "'{0[0]}'.format(x)",
        lambda x: jinja.chiama(jinja.attributo("{0[0]}", "format"), x),
    ),
    (
        "'{0.state}'.format(x)",
        lambda x: jinja.chiama(jinja.attributo("{0.state}", "format"), x),
    ),
    (
        "'{a}'.format_map({'a': x})",
        lambda x: jinja.chiama(jinja.attributo("{a}", "format_map"), {"a": x}),
    ),
    ("'%s'.format(x)", lambda x: jinja.chiama(jinja.attributo("%s", "format"), x)),
    ("x()", lambda x: jinja.chiama(x)),
    ("x.__class__()", lambda x: jinja.chiama(jinja.attributo(x, "__class__"))),
    ("x.mro()", lambda x: jinja.chiama(jinja.attributo(x, "mro"))),
    ("x.conjugate()", lambda x: jinja.chiama(jinja.attributo(x, "conjugate"))),
    (
        "x[0].upper()",
        lambda x: jinja.chiama(jinja.attributo(jinja.elemento(x, 0), "upper")),
    ),
]
ARGOMENTI_METODI = [",", " ", None, 1, "a", INDEFINITO]


def casi_accesso(banco: Banco) -> None:
    c = banco.confronta
    for x, nome in itertools.product(VALORI, NOMI_ATTRIBUTI):
        c("attributo", f"x.{nome}", lambda x, nome=nome: jinja.attributo(x, nome), x=x)
        c(
            "attributo",
            f"x.{nome}.y",
            lambda x, nome=nome: jinja.attributo(jinja.attributo(x, nome), "y"),
            x=x,
        )
    for x, k in itertools.product(VALORI, CHIAVI):
        c("elemento", "x[k]", lambda x, k: jinja.elemento(x, k), x=x, k=k)
    for x, a, b in itertools.product(
        VALORI, [None, 0, 1, -1, 3, "a", INDEFINITO], [None, 2, -1, 10]
    ):
        c(
            "elemento (slice)",
            "x[a:b]",
            lambda x, a, b: jinja.elemento(x, slice(a, b)),
            x=x,
            a=a,
            b=b,
        )
    for x, n in itertools.product(VALORI, [None, 2, -1, 0, "a"]):
        c(
            "elemento (slice)",
            "x[::n]",
            lambda x, n: jinja.elemento(x, slice(None, None, n)),
            x=x,
            n=n,
        )
        c(
            "elemento (slice)",
            "x[:-3]",
            lambda x, n: jinja.elemento(x, slice(None, -3)),
            x=x,
            n=n,
        )
    for x, (espressione, calcolo) in itertools.product(VALORI, METODI):
        c("chiama", espressione, calcolo, x=x)
    for x, y in itertools.product(VALORI, ARGOMENTI_METODI):
        for metodo in (
            "split",
            "get",
            "startswith",
            "index",
            "count",
            "strftime",
            "join",
        ):
            c(
                "chiama",
                f"x.{metodo}(y)",
                lambda x, y, metodo=metodo: jinja.chiama(jinja.attributo(x, metodo), y),
                x=x,
                y=y,
            )


OPERATORI = [
    ("+", jinja.somma),
    ("-", jinja.sottrai),
    ("*", jinja.moltiplica),
    ("/", jinja.dividi),
    ("//", jinja.dividi_intero),
    ("%", jinja.resto),
    ("**", jinja.potenza),
    ("==", lambda a, b: a == b),
    ("!=", lambda a, b: a != b),
    ("<", lambda a, b: a < b),
    ("<=", lambda a, b: a <= b),
    (">", lambda a, b: a > b),
    (">=", lambda a, b: a >= b),
    ("in", lambda a, b: jinja.contiene(b, a)),
    ("not in", lambda a, b: not jinja.contiene(b, a)),
    ("and", lambda a, b: a and b),
    ("or", lambda a, b: a or b),
]


def casi_operatori(banco: Banco) -> None:
    c = banco.confronta
    for (simbolo, funzione), a, b in itertools.product(
        OPERATORI, ARITMETICA, ARITMETICA
    ):
        c(
            f"operatore {simbolo}",
            f"a {simbolo} b",
            lambda a, b, funzione=funzione: funzione(a, b),
            a=a,
            b=b,
        )
    for a in VALORI:
        c("nega", "-a", lambda a: jinja.nega(a), a=a)
        c("positivo", "+a", lambda a: jinja.positivo(a), a=a)
        c("not", "not a", lambda a: not a, a=a)
        c(
            "operatore in",
            "a in 'abc,21.30'",
            lambda a: jinja.contiene("abc,21.30", a),
            a=a,
        )
        c("operatore in", "'a' in a", lambda a: jinja.contiene(a, "a"), a=a)
        c("operatore in", "1 in a", lambda a: jinja.contiene(a, 1), a=a)
        c("if", "1 if a else 2", lambda a: 1 if a else 2, a=a)
        c("operatore ==", "a == a", lambda a: a == a, a=a)  # noqa: PLR0124
        c("operatore -", "a - 1", lambda a: jinja.sottrai(a, 1), a=a)
        c("operatore *", "a * 2", lambda a: jinja.moltiplica(a, 2), a=a)


def _non_ascii(testo: str) -> bool:
    """Cifre decimali non ASCII: dal 2026.11 ``_IS_NUMERIC`` le esclude (``re.ASCII``)."""
    return any(c.isdecimal() and not c.isascii() for c in testo)


RESE = [
    "true",
    "True",
    " TRUE ",
    "tRuE",
    "True\n",
    "truee",
    "false",
    "1",
    "0",
    "2",
    "-1",
    "0.0",
    "1.0",
    "on",
    "ON ",
    "yes",
    "no",
    "enable",
    "disable",
    "off",
    "None",
    "none",
    "null",
    "[1]",
    "[]",
    "{}",
    '{"a": 1}',
    "{'a': [1, {'b': 2}]}",
    "(1)",
    "(True)",
    "b'x'",
    "...",
    "{1, 2}",
    "()",
    "(1,)",
    "1j",
    "1+2j",
    "--1",
    "0007",
    "00.5",
    ".",
    "+",
    "-",
    "",
    "   ",
    "[nan]",
    "-0",
    "-0.0",
    "+0",
    "1e3",
    "1E3",
    "0x10",
    "0o7",
    "0b1",
    "1_000",
    "٣",
    "١٢",
    "٣.٥",
    "１２",
    "²",
    "nan",
    "inf",
    "-inf",
    "1e400",
    "123456789012345678901234567890",
    "1.123456789012345678",
    "'testo'",
    '"testo"',
    "'1'",
    "Velocità 1",
    "[1, 2",
    "{'a': }",
    "set()",
    "frozenset()",
    "True and False",
    "not True",
    "1 if True else 2",
    "x",
    "unknown",
    "unavailable",
    "'a' 'b'",
    "1 2",
    " 5 ",
    " 5",
    "[1, 'a', None, True, 2.5, (1,), {2}]",
    "{1: 'a', 'b': [None]}",
    "-5.",
    "+.5",
    "[" * 300 + "]" * 300,
    "-" * 10000 + "1",
    "1" + "+1" * 100000,
]


def casi_risultati(banco: Banco) -> None:
    testi = [v for v in [*STRINGHE, *RESE] if len(v) < 1000]
    valori = [
        *VALORI,
        *RESE,
        *(f" {v}\n" for v in testi),
        *(v.upper() for v in testi),
        *(v.title() for v in testi),
    ]
    for s in valori:
        descrizione = f"{{{{ s }}}} con s={_breve(s)}"
        # Condizione: testo reso senza interpretarlo.
        atteso = condition.async_template(
            banco.hass, banco.modello("{{ s }}"), {} if s is INDEFINITO else {"s": s}
        )
        resa = jinja.testo(jinja.indefinito("s") if s is INDEFINITO else s)
        banco.confronta_valori(
            "condizione",
            descrizione,
            atteso,
            jinja.condizione(resa),
            atteso is jinja.condizione(resa),
        )
        # Interpretazione del risultato e trigger.
        try:
            interpretato = banco.rendi("{{ s }}", {"s": s}, parse_result=True)
        except RecursionError:
            assert not HA_2026_11
            banco.nota_2026_10("interpreta")
            continue
        if not HA_2026_11 and _non_ascii(resa):
            banco.nota_2026_10("interpreta")
            continue
        mio = jinja.interpreta(resa)
        if isinstance(mio, risultato.Contenitore):
            uguali = (
                isinstance(interpretato, ResultWrapper)
                and isinstance(interpretato, type(mio.valore))
                and interpretato == mio.valore
                and str(interpretato) == mio.testo
            )
        else:
            uguali = (
                not isinstance(interpretato, ResultWrapper)
                and type(interpretato) is type(mio)
                and str(interpretato) == str(mio)
                and (
                    interpretato == mio
                    or (
                        isinstance(mio, float)
                        and math.isnan(mio)
                        and math.isnan(interpretato)
                    )
                )
            )
        banco.confronta_valori("interpreta", descrizione, interpretato, mio, uguali)
        atteso = result_as_boolean(interpretato)
        banco.confronta_valori(
            "trigger_vero",
            descrizione,
            atteso,
            jinja.trigger_vero(mio),
            atteso is jinja.trigger_vero(mio),
        )
        banco.confronta_valori(
            "trigger_vero",
            descrizione,
            atteso,
            jinja.trigger_vero(resa),
            atteso is jinja.trigger_vero(resa),
        )


# --- Test ---------------------------------------------------------------------------------


async def test_testo_e_concat(banco: Banco) -> None:
    casi_testo(banco)
    banco.verifica(5000)


async def test_filtri_numerici(banco: Banco) -> None:
    casi_numeri(banco)
    banco.verifica(10000)


async def test_filtri_dei_testi(banco: Banco) -> None:
    casi_testi(banco)
    banco.verifica(11500)


async def test_filtri_delle_raccolte(banco: Banco) -> None:
    casi_raccolte(banco)
    banco.verifica(2000)


async def test_map_select_reject(banco: Banco) -> None:
    casi_map_select(banco)
    banco.verifica(45000)


async def test_test_di_jinja(banco: Banco) -> None:
    casi_test(banco)
    banco.verifica(55000)


async def test_funzioni(banco: Banco) -> None:
    casi_funzioni(banco)
    banco.verifica(6000)


async def test_attributi_elementi_chiamate(banco: Banco) -> None:
    casi_accesso(banco)
    banco.verifica(33000)


async def test_operatori(banco: Banco) -> None:
    casi_operatori(banco)
    banco.verifica(12500)


async def test_condizioni_trigger_risultati(banco: Banco) -> None:
    casi_risultati(banco)
    banco.verifica(2400)


def test_interpreta_regole_2026_11() -> None:
    """Le regole di ``_parse_result`` del 2026.11 anche con un Home Assistant più vecchio."""
    assert risultato.interpreta("٣") == "٣"  # cifre non ASCII: testo (re.ASCII)
    assert risultato.interpreta("٣.٥") == "٣.٥"
    assert risultato.interpreta("１２") == "１２"
    lungo = (
        "1" + "+1" * 100000
    )  # literal_eval: RecursionError, il risultato resta testo
    assert risultato.interpreta(lungo) == lungo
    assert risultato.interpreta(" 21.30 ") == 21.3


# --- Copertura dei nomi usati dal package -------------------------------------------------

# Funzioni, filtri e test che hanno bisogno di hass: li fa il contesto del motore, non jinja.py.
CON_HASS = {
    "states",
    "is_state",
    "state_attr",
    "now",
    "utcnow",
    "device_name",
    "entity_name",
    "expand",
    "integration_entities",
    "device_attr",
}
FILTRI = {
    "float": jinja.f_float,
    "int": jinja.f_int,
    "round": jinja.f_round,
    "trim": jinja.f_trim,
    "lower": jinja.f_lower,
    "capitalize": jinja.f_capitalize,
    "is_number": jinja.f_is_number,
    "list": jinja.f_list,
    "map": jinja.f_map,
    "reject": jinja.f_reject,
    "select": jinja.f_select,
    "selectattr": jinja.f_selectattr,
    "rejectattr": jinja.f_rejectattr,
    "join": jinja.f_join,
    "length": jinja.f_length,
    "count": jinja.f_count,
    "default": jinja.f_default,
    "unique": jinja.f_unique,
    "max": jinja.f_max,
    "min": jinja.f_min,
    "sort": jinja.f_sort,
    "sum": jinja.f_sum,
    "regex_replace": jinja.f_regex_replace,
    "replace": jinja.f_replace,
    "string": jinja.f_string,
    "abs": jinja.f_abs,
    "bool": jinja.f_bool,
    "from_json": jinja.f_from_json,
}
TEST = {
    "defined": jinja.t_defined,
    "none": jinja.t_none,
    "match": jinja.t_match,
    "mapping": jinja.t_mapping,
}
FUNZIONI = {
    "strptime": jinja.strptime,
    "as_timestamp": jinja.as_timestamp,
    "namespace": jinja.namespace,
    "is_number": jinja.f_is_number,
    "float": jinja.f_float,
    "int": jinja.f_int,
    "log": jinja.log,
    "timedelta": jinja.timedelta,
    "as_datetime": jinja.as_datetime,
}


def _modelli_del_package() -> list[str]:
    modelli: list[str] = []

    def raccogli(valore: Any) -> None:
        if isinstance(valore, str):
            if "{{" in valore or "{%" in valore or "{#" in valore:
                modelli.append(valore)
        elif isinstance(valore, dict):
            for chiave, voce in valore.items():
                raccogli(chiave)
                raccogli(voce)
        elif isinstance(valore, list):
            for voce in valore:
                raccogli(voce)

    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt"):
        raccogli(
            parse_yaml(
                trasforma.rimuovi_sezioni_solo_master(
                    (PACKAGE / nome).read_text(encoding="utf-8")
                )
            )
        )
    return modelli


def test_nomi_del_package_coperti() -> None:
    """Ogni filtro, test, funzione e metodo dei modelli del package ha la sua funzione in
    jinja.py (o è del contesto con hass), e ogni metodo è provato in ``METODI``."""
    ambiente = jinja2.Environment(
        extensions=["jinja2.ext.loopcontrols", "jinja2.ext.do"]
    )
    filtri, test, funzioni, metodi, per_nome = set(), set(), set(), set(), set()
    modelli = _modelli_del_package()
    assert len(modelli) > 3000
    for sorgente in set(modelli):
        for nodo in ambiente.parse(sorgente.strip()).find_all(
            (nodes.Filter, nodes.Test, nodes.Call)
        ):
            if isinstance(nodo, nodes.Filter):
                filtri.add(nodo.name)
            elif isinstance(nodo, nodes.Test):
                test.add(nodo.name)
            elif isinstance(nodo.node, nodes.Name):
                funzioni.add(nodo.node.name)
            elif isinstance(nodo.node, nodes.Getattr):
                metodi.add(nodo.node.attr)
            if isinstance(nodo, nodes.Filter) and nodo.name in (
                "map",
                "select",
                "reject",
                "selectattr",
                "rejectattr",
            ):
                posto = 1 if nodo.name.endswith("attr") else 0
                if len(nodo.args) > posto and isinstance(nodo.args[posto], nodes.Const):
                    per_nome.add(nodo.args[posto].value)
    assert filtri - FILTRI.keys() == set()
    assert test - TEST.keys() == set()
    assert funzioni - FUNZIONI.keys() - CON_HASS == set()
    provati = {
        re.match(r"x\.(\w+)\(", espressione).group(1)
        for espressione, _ in METODI
        if espressione.startswith("x.")
    }
    assert metodi - provati == set()
    # Filtri e test chiamati per nome dentro map/select/reject/selectattr/rejectattr.
    noti = (
        set(FILTRI_MAP)
        | {f for f, *_ in FILTRI_MAP_ARG}
        | {f for f, *_ in FILTRI_MAP_DUE}
    )
    noti |= (
        set(TEST_SELECT)
        | {t for t, _ in TEST_SELECT_ARG}
        | set(TEST_CON_ARGOMENTO)
        | set(TEST_NOMI)
    )
    assert per_nome - noti - CON_HASS == set()
    for nome in per_nome - CON_HASS:
        assert nome in jinja._AMBIENTE.filters or nome in jinja._AMBIENTE.tests, nome


def test_api() -> None:
    """I nomi che usa il traduttore."""
    for nome in (
        "Indefinito",
        "indefinito",
        "ErroreTemplate",
        "testo",
        "concat",
        "attributo",
        "elemento",
        "chiama",
        "somma",
        "sottrai",
        "moltiplica",
        "dividi",
        "dividi_intero",
        "resto",
        "nega",
        "positivo",
        "contiene",
        "f_float",
        "f_int",
        "f_round",
        "f_trim",
        "f_lower",
        "f_capitalize",
        "f_is_number",
        "f_list",
        "f_map",
        "f_reject",
        "f_select",
        "f_selectattr",
        "f_rejectattr",
        "f_join",
        "f_length",
        "f_count",
        "f_default",
        "f_unique",
        "f_max",
        "f_regex_replace",
        "f_replace",
        "f_string",
        "f_abs",
        "f_bool",
        "f_from_json",
        "t_defined",
        "t_match",
        "t_none",
        "prova",
        "strptime",
        "as_timestamp",
        "namespace",
        "imposta_ns",
        "condizione",
        "trigger_vero",
        "interpreta",
    ):
        assert nome in jinja.__all__ and hasattr(jinja, nome), nome
    assert issubclass(jinja.Indefinito, jinja2.Undefined)
    assert jinja.indefinito("x")._undefined_message == "'x' is undefined"
    assert jinja.interpreta is risultato.interpreta
    with pytest.raises(jinja.ErroreTemplate, match="No filter named 'nonexist'"):
        jinja.f_list(jinja.f_map([1], "nonexist"))
    assert (
        jinja.f_list(jinja.f_map([], "nonexist")) == []
    )  # come Jinja: l'errore arriva al primo elemento
