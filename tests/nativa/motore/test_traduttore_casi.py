"""Il traduttore dei modelli contro Home Assistant, su costrutti Jinja scelti apposta.

Ogni modello di ``MODELLI`` (costrutti del package o vicini a quelli del package: cicli e
loro ambiti, ``loop.*``, namespace, ``{% set %}`` dentro ``if`` e ``for``, ``set`` a
blocco con filtri, ``break``/``continue``, spazi, ``raw``, filtri e test con le regole di
Home Assistant, confronti tra tipi diversi, divisioni, concatenazioni, fette, attributi ed
elementi di dizionari e stati, indefiniti, ``states.dominio.oggetto``...) si traduce con
``Traduttore`` (come ``traduci.py``) e si rende, con le stesse variabili e gli stessi
stati, da Home Assistant (``Template.async_render``, con ``parse_result`` falso e vero) e
dalla funzione tradotta (``Contesto.testo`` e ``ModelloHA.async_render``): stesso testo,
stesso valore interpretato (stesso tipo), o errore in tutte e due.

I costrutti che il traduttore non conosce (macro, ``call``, ``filter``, ``with``, cicli
ricorsivi, funzioni globali senza traduzione) devono fermare la traduzione
(``NonTraducibile``), mai tradursi in qualcosa d'altro.
"""

from __future__ import annotations

import logging
import math
import re
from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant, State
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.template import (
    RenderInfo,
    ResultWrapper,
    Template,
    TemplateEnvironment,
)

from custom_components.vmc_master.nativa.motore import jinja as J
from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.trasforma import rinomina

from .traduci_jinja import NonTraducibile, Traduttore

_INDIRIZZO = re.compile(r" at 0x[0-9a-fA-F]+")

# --- Modelli ----------------------------------------------------------------------------

MODELLI: dict[str, list[str]] = {
    "cicli": [
        "{% for i in lista %}{{ loop.index0 }}:{{ i }};{% endfor %}",
        (
            "{% for i in lista %}{{ loop.index }}{{ loop.first }}{{ loop.last }}"
            "{{ loop.length }}{{ loop.revindex }}{{ loop.revindex0 }}|{{ loop.previtem }}"
            "|{{ loop.nextitem }}|{{ loop.depth }}{{ loop.depth0 }};{% endfor %}"
        ),
        (
            "{% for i in lista %}{{ loop.cycle('a', 'b') }}{{ loop.changed(i is none) }}"
            "{% endfor %}"
        ),
        (
            "{% for i in lista if i is number %}{{ loop.index0 }}{{ i }}{% else %}vuoto"
            "{% endfor %}"
        ),
        "{% for i in lista if i is not none and loop is undefined %}{{ i }}{% endfor %}",
        "{% for i in [] %}x{% else %}vuoto{{ i }}{{ loop }}{% endfor %}",
        "{% for i in lista %}{% else %}{{ loop.index }}{% endfor %}",
        "{% for i in [1, 2] %}{% continue %}{% else %}E{% endfor %}",
        (
            "{% for i in [1, 2] %}{% if i == 2 %}{% continue %}{% endif %}{{ i }}"
            "{% else %}E{% endfor %}"
        ),
        "{% for i in [] %}{% continue %}{% else %}E{% endfor %}",
        (
            "{% for i in lista %}{% if loop.index0 > 1 %}{% break %}{% endif %}{{ i }}"
            "{% endfor %}"
        ),
        "{% for i in lista %}{% break %}{% else %}E{% endfor %}",
        (
            "{% for a in [1, 2] %}{% for b in [3, 4] %}{{ loop.index0 }}{{ a }}{{ b }},"
            "{% endfor %}{{ loop.index0 }};{% endfor %}"
        ),
        (
            "{% for a in m %}{% for b in a %}{{ b }}{% if loop.last %}|{% endif %}"
            "{% endfor %}{% else %}nessuna{% endfor %}"
        ),
        (
            "{% for a in m %}{% for b in a if b > 1 %}{{ b }}{% else %}-{% endfor %}"
            "{% endfor %}"
        ),
        "{% set i = 'fuori' %}{% for i in [1, 2] %}{{ i }}{% endfor %}{{ i }}",
        "{% for i in [1, 2] %}{{ i }}{% endfor %}{{ i }}",
        (
            "{% set t = 0 %}{% for i in [1, 2] %}{% set t = t + i %}{{ t }}{% endfor %}"
            "{{ t }}"
        ),
        "{% for i in [1, 2] %}{% set y = i %}{% endfor %}{{ y }}",
        "{{ y }}{% for i in lista %}{% set y = i %}{{ y }}{% endfor %}{{ y }}",
        (
            "{{ y }}{% for a in [1] %}{% for b in [2] %}{% set y = b %}{{ y }}{% endfor %}"
            "{% endfor %}{{ y }}"
        ),
        "{% for i in [1, 2] %}{{ y }}{% set y = i %}{{ y }}{% endfor %}",
        "{% for i in [1, 2] %}{{ y }}{% endfor %}{% set y = 2 %}{{ y }}",
        "{% for i in [1, 2] %}{{ x }}{% endfor %}",
        "{% for k, v in d.items() %}{{ k }}={{ v }};{% endfor %}",
        "{% for k, v in d | dictsort %}{{ loop.index }}{{ k }}={{ v }};{% endfor %}",
        "{% for (a, b) in [[1, 2], [3, 4]] %}{{ a + b }}{% endfor %}",
        "{% for a, b in [[1, 2], [3]] %}{{ a }}{% endfor %}",
        "{% for c in s %}{{ c }}.{% endfor %}",
        "{% for c in x %}{{ c }}{% endfor %}",
        "{% for c in indefinita %}{{ c }}{% else %}vuota{% endfor %}",
        "{% for e in entita %}{{ states(e) }}/{{ state_attr(e, 'unit') }};{% endfor %}",
    ],
    "assegnazioni": [
        (
            "{% set ns = namespace(tot=0, voci=[]) %}{% for i in lista %}"
            "{% set ns.tot = ns.tot + (i | float(0)) %}{% set ns.voci = ns.voci + [i] %}"
            "{% endfor %}{{ ns.tot }} {{ ns.voci }}"
        ),
        (
            "{% set ns = namespace(trovato=false) %}{% for i in lista %}{% if i == x %}"
            "{% set ns.trovato = true %}{% endif %}{% endfor %}{{ ns.trovato }}"
        ),
        "{% set ns = namespace(a=1) %}{{ ns.a }}{{ ns['a'] }}{{ ns.b }}|{{ ns }}",
        "{% set ns = 1 %}{% set ns.a = 2 %}{{ ns }}",
        "{% set ns.a = 2 %}{{ ns }}",
        "{% if x %}{% set y = 1 %}{% endif %}{{ y }}",
        "{% if x %}{% set y = 1 %}{% else %}{% set y = 2 %}{% endif %}{{ y }}",
        (
            "{% if x == 5 %}{% set y = 'a' %}{% elif x == '7.5' %}{% set y = 'b' %}"
            "{% endif %}{{ y }}"
        ),
        (
            "{% for i in lista %}{% if i is number %}{% set z = i %}{% endif %}{{ z }}"
            "{% endfor %}{{ z }}"
        ),
        "{% set y = y ~ '!' %}{{ y }}",
        "{% set x = x | float(0) + 1 %}{% for i in [1] %}{{ x }}{% endfor %}{{ x }}",
        "{% set a, b = [1, 2] %}{{ a }}{{ b }}",
        "{% set a, b = lista %}{{ a }}{{ b }}",
        "{% set b %} {{ x }} - {{ y }} {% endset %}[{{ b }}]",
        "{% set b | trim %} {{ x }} {% endset %}[{{ b }}]",
        "{% set b | trim | upper %} ab {{ s }} {% endset %}[{{ b }}]",
        "{% set b | replace('a', 'b') | trim %} aaa {% endset %}[{{ b }}]",
        "{% set b | replace('a', y | string) %}{{ y }} aaa{% endset %}[{{ b }}]",
        "{% set b | float(0) %}{{ x }}{% endset %}{{ b + 1 }}",
        "{% for i in [1, 2] %}{% set b %}<{{ i }}>{% endset %}{{ b }}{% endfor %}{{ b }}",
        "{% set b %}{{ q }}{% endset %}{% set q = 1 %}{{ b }}{{ q }}",
        (
            "{% set b %}{% for i in lista %}{{ i }},{% endfor %}{% endset %}"
            "{{ b.split(',') | count }}"
        ),
        "{% set b %}{% set c = 1 %}{{ c }}{% endset %}{{ b }}{{ c }}",
        "{% do lista.append(1) %}{{ lista }}",
        "{% do d.get('a') %}{{ d }}",
        "{% set states = d %}{{ states.a }}",
        "{% set states = {'sensor': {'t1': 'locale'}} %}{{ states.sensor.t1 }}",
        "{% for states in [d] %}{{ states.b.count }}{% endfor %}",
        "{% set now = 1 %}{{ now }}",
    ],
    "spazi": [
        "  {%- if true -%}  a  {%- endif -%}  ",
        "a\n  {%- if x %}\n  b\n  {% endif -%}\nc",
        "{{- x -}} | {{ y -}}  .  {{- s }}",
        "{% if x %}\n riga\n{% endif %}\nfine\n",
        "{% for i in lista -%}\n  {{ i }}\n{%- endfor %}",
        "{% raw %}{{ x }}{% endraw %} {{ x }}",
        "a{# commento {{ x }} #}b",
        "{#- commento -#} c",
        "{%+ if true %} a{% endif %}",
    ],
    "filtri": [
        "{{ s | float(0) }}|{{ x | float(-1) }}|{{ y | float(default=2) }}",
        "{{ x | float }}",
        "{{ s | int(-1) }}|{{ x | int(0) }}|{{ f | int }}|{{ y | int(base=16, default=0) }}",
        (
            "{{ x | round(1) }}|{{ f | round(0, 'floor') }}|{{ f | round(1, 'ceil') }}"
            "|{{ f | round(2, 'half') }}|{{ f | round }}"
        ),
        "{{ x | round(1, default='n') }}",
        "{{ s | regex_replace('[a-c]+', 'N') }}|{{ s | regex_replace('A', 'z', true) }}",
        "{{ s is match('ab') }}|{{ s is match('AB', true) }}|{{ s is search('def') }}",
        "{{ s | regex_findall('[a-z]') }}|{{ s | regex_match('a') }}",
        "{{ ('{\"a\": [1, 2]}' | from_json).a[1] }}|{{ s | from_json(default='x') }}",
        "{{ s | from_json }}",
        "{{ lista | map('float', 0) | list }}",
        "{{ lista | map('string') | join(',') }}|{{ lista | map('lower') | list }}",
        "{{ lista | select('number') | list }}|{{ lista | reject('none') | list }}",
        "{{ lista | select('is_number') | list }}|{{ lista | reject('string') | list }}",
        "{{ dizionari | selectattr('a', 'eq', 1) | map(attribute='b') | list }}",
        "{{ dizionari | selectattr('a', 'defined') | list | count }}",
        "{{ dizionari | rejectattr('a', 'undefined') | map(attribute='b') | join }}",
        "{{ dizionari | map(attribute='a', default=0) | sum }}",
        "{{ dizionari | map(attribute='a') | list }}",
        "{{ entita | select('is_state', 'on') | list }}",
        "{{ entita | map('states') | list }}|{{ entita | map('state_attr', 'unit') | list }}",
        "{{ entita | select('has_value') | list }}",
        "{{ lista | sort(attribute='x') }}",
        "{{ lista | map('float', 0) | sort | first }}|{{ lista | map('string') | max }}",
        "{{ lista | unique | list }}|{{ lista | count }}|{{ lista | length }}",
        "{{ lista | map('float', 0) | sum }}|{{ lista | map('float', 0) | min }}",
        "{{ s | capitalize }}|{{ s | upper }}|{{ s | lower | trim }}|{{ s | title }}",
        "{{ x | abs }}",
        "{{ x | string }}|{{ x | bool(false) }}|{{ s | bool('n') }}|{{ x | is_number }}",
        "{{ x | bool }}",
        "{{ s | replace('a', 'b') }}|{{ s | replace(',', '') | length }}",
        "{{ indefinita | default('x') }}|{{ n | default('d') }}|{{ n | default('d', true) }}",
        "{{ lista | join(', ') }}|{{ lista | list | first }}|{{ s | list | last }}",
        "{{ x | float(0) | round(2) }}|{{ ((x | float(0)) * 1.1) | round(1) }}",
        "{{ s | slugify }}|{{ s | truncate(5) }}",
        "{{ lista | select('match', 'a') | list }}",
        "{{ lista | map('regex_replace', 'a', 'b') | list }}",
        "{{ lista | map('nessun_filtro') | list }}",
        "{{ lista | select('nessun_test') | list }}",
    ],
    # le funzioni globali che sono anche filtri, come le usano i sensori template del package
    "globali": [
        "{{ float(x) }}",
        "{{ float(s, 0) }}|{{ float(x, -1) }}|{{ float(n, default=2) }}",
        "{{ (float(int(s[1:]) / 10)) if s[1:] | is_number else 'no' }}",
        "{{ int(x) }}|{{ int(f, 0) }}|{{ int(s, default=-1) }}",
        "{{ is_number(x) }}|{{ is_number(s) }}|{{ is_number(n) }}|{{ is_number('inf') }}",
        "{{ log(x) }}|{{ log(f, 10) }}|{{ log(s, default='n') }}|{{ -log(f) }}",
        "{{ log(0) }}",
        "{{ e }}|{{ (e ** (2 * f / (f + 3))) | round(4) }}",
        "{% set e = 3 %}{{ e }}",
    ],
    "test": [
        "{{ x is defined }}|{{ indefinita is defined }}|{{ indefinita is undefined }}",
        "{{ n is none }}|{{ x is none }}|{{ indefinita is none }}|{{ x is not none }}",
        "{{ x is number }}|{{ s is string }}|{{ d is mapping }}|{{ lista is sequence }}",
        "{{ lista is iterable }}|{{ x is integer }}|{{ f is float }}|{{ x is boolean }}",
        "{{ x in lista }}|{{ 'a' not in s }}|{{ 'a' in d }}|{{ x is in(lista) }}",
        "{{ x is eq(5) }}|{{ x is gt(3) }}|{{ s is lower }}|{{ x is odd }}",
        "{{ x is divisibleby(5) }}",
        "{{ x is number and x > 2 }}|{{ x is is_number }}|{{ s is is_number }}",
        "{{ 'sensor.t1' is is_state('21.5') }}|{{ 'sensor.t1' is has_value }}",
        "{{ s is match('a') and s is not search('z') }}",
        "{{ indefinita is mapping }}|{{ d.zz is defined }}|{{ (x if false) is defined }}",
    ],
    "operatori": [
        "{{ x > 3 }}|{{ x == 5 }}|{{ s == 3 }}|{{ x != '5' }}",
        "{{ s < 3 }}",
        "{{ 1 < x < 10 }}|{{ 1 < x > 10 }}|{{ x >= 5 <= 5 }}",
        "{{ 7 / 2 }}|{{ 7 // 2 }}|{{ 7 % 3 }}|{{ -7 // 2 }}|{{ 2 ** 10 }}|{{ -2 ** 2 }}",
        "{{ x / 0 }}",
        "{{ (x | float(0)) / 3 }}|{{ 10 / 4 }}|{{ 0.1 + 0.2 }}|{{ 3 * 1.0 }}",
        "{{ x // 2 }}|{{ x % 2 }}|{{ x ** 2 }}|{{ -x }}|{{ +x }}",
        "{{ x ~ y ~ none ~ true }}|{{ 'a' ~ indefinita ~ 'b' }}|{{ lista ~ d }}",
        "{{ s + 'b' }}|{{ [1] + [2] }}|{{ 'ab' * 2 }}|{{ lista * 2 }}",
        "{{ s + x }}",
        "{{ x + y }}",
        "{{ indefinita + 1 }}",
        "{{ not x }}|{{ not indefinita }}|{{ x and y }}|{{ x or y }}|{{ n or 'v' }}",
        "{{ indefinita or 'v' }}|{{ indefinita and 'v' }}|{{ (indefinita or 0) + 1 }}",
        "{{ 'a' if x else 'b' }}|{{ 'a' if n }}|{{ ('a' if false) ~ 'b' }}",
        "{{ (('a' if false)) == indefinita }}|{{ indefinita == indefinita2 }}",
        "{{ '%s-%d' % ('a', 3) }}|{{ 'x{}y'.format(x) }}|{{ '%05.1f' % f }}",
        "{{ '%02d:%02d' % (x // 60, x % 60) }}",
        "{{ 1e20 }}|{{ 1/3 }}|{{ 10 ** 20 }}|{{ 2.0 }}|{{ -0.0 }}|{{ 1.5e-7 }}",
        "{{ x > n }}",
        "{{ lista < [1] }}",
    ],
    "accesso": [
        "{{ s[1:] }}|{{ s[:-1] }}|{{ lista[::2] }}|{{ s[::-1] }}|{{ lista[1:3] }}",
        "{{ s[x:] }}",
        "{{ indefinita[1:] }}",
        "{{ lista[0] }}|{{ lista[-1] }}|{{ lista[10] }}|{{ s[0] }}",
        "{{ d.a }}|{{ d['a'] }}|{{ d.zz }}|{{ d['zz'] | default('d') }}|{{ d.get('zz', 'no') }}",
        "{{ d.items }}",
        "{{ d['items'] }}|{{ d.keys() | list }}|{{ d.values() | list | count }}",
        "{{ d.zz.yy }}",
        "{{ d.b[1] }}|{{ d['b'][0] }}|{{ d.b.1 }}",
        "{{ (d.zz or 'o') }}|{{ d.zz | default('-') }}",
        "{{ d.__class__ }}",
        "{{ lista.append }}",
        "{{ lista.append(1) }}",
        "{{ s.split(',') }}|{{ s.upper() }}|{{ s.startswith('a') }}|{{ s.replace('a', 'b') }}",
        "{{ s.split(',')[1] | length }}|{{ (s.split(',') | first)[:2] }}",
        "{{ x.real }}",
        "{{ states.sensor.t1.state }}|{{ states.sensor.t1.attributes.unit }}",
        "{{ states.sensor.nessuno.state }}|{{ states.sensor.nessuno }}",
        "{{ states.sensor.t1.name }}|{{ states.sensor.t1.object_id }}|{{ states.sensor.t1.domain }}",
        "{{ states('sensor.t1') }}|{{ states('sensor.nessuno') }}|{{ states.sensor.t1['state'] }}",
        "{{ states['sensor.t1'].state }}|{{ states['sensor.nessuno'] }}",
        "{{ state_attr('sensor.t1', 'unit') }}|{{ state_attr('sensor.t1', 'lista')[1] }}",
        "{{ is_state('sensor.t1', '21.5') }}|{{ is_state('sensor.t2', ['x', 'on']) }}",
        "{{ states.sensor | count }}|{{ states.sensor | map(attribute='entity_id') | list }}",
        "{{ states.sensor.t1.attributes.get('unit') }}|{{ states.sensor.t1.attributes['unit'] }}",
        "{{ states.sensor.t1.last_changed | string | length > 0 }}",
        "{{ states.sensor.t1.attributes.lista | sum }}",
        "{{ states.input_boolean.a.state == 'on' }}|{{ states.binary_sensor.x.state }}",
        "{{ trigger.to_state.state }}|{{ trigger['to_state'].attributes.get('unit') }}",
        "{{ trigger.to_state.attributes.unit }}|{{ trigger.from_state.state }}",
        "{{ trigger.id.split('|')[1] }}|{{ trigger.id.split('|') | length }}",
        "{{ trigger.zz }}|{{ trigger.zz is defined }}",
        "{{ indefinita }}|{{ indefinita | length }}|{{ indefinita | list }}",
        "{{ indefinita.a }}",
        "{{ indefinita['a'] }}",
        "{{ indefinita() }}",
        "{{ n.a }}",
        "{{ {'a': 1, 'b': [1, 2]} }}|{{ (1, 2) }}|{{ (1,) }}|{{ [1, 'a', none, true] }}",
        "{{ {'a': x}['a'] }}|{{ [x, y][1] }}|{{ {'k': lista}.k[0] }}",
        "{{ now().year > 2000 }}|{{ now().tzinfo is not none }}|{{ utcnow().hour }}",
        "{{ as_timestamp('2026-01-01T00:00:00+00:00') }}|{{ as_timestamp(s, 0) }}",
        "{{ strptime('2026-01-01', '%Y-%m-%d').day }}|{{ strptime(s, '%Y', 'no') }}",
        "{{ as_datetime('2026-01-01 10:00:00').hour }}|{{ timedelta(minutes=5).total_seconds() }}",
        "{{ states.sensor.t1.last_changed > now() - timedelta(days=1) }}",
        "{{ (now() - states.sensor.t1.last_changed).total_seconds() | int }}",
        "{{ 'città' | upper }}|{{ 'città' | length }}",
    ],
    "risultati": [
        "{{ lista }}",
        "{{ d }}",
        "{{ [1, 2] }}",
        "{{ {'a': 1} }}",
        "{{ (1, 2) }}",
        "{{ 1.50 }}",
        "007",
        "{{ true }}",
        "none",
        " {{ x }} ",
        "{{ s.split(',') }}",
        "{{ {'x': lista} }}",
        "{{ '{1, 2}' }}",
        "{{ x }}{{ y }}",
        "[{{ x }}, {{ y }}]",
    ],
}

# Modelli con «master» nei testi e nei nomi (variabili, attributi, argomenti per nome):
# per un'altra VMC il modello tradotto deve fare quello che fa Home Assistant con il
# modello rinominato da ``trasforma.rinomina`` (variabili e stati rinominati anche loro).
MODELLI_NOMI = [
    "{{ x_master }}|{{ x_master is defined }}|{{ y_Master | default('d') }}",
    "{% if x %}{% set x_master = 2 %}{% endif %}{{ x_master }}",
    "{{ d.vmc_master_a }}|{{ d['vmc_master_a'] }}|{{ d.get('vmc_master_a') }}",
    "{{ trigger.to_state.attributes.attr_master }}|{{ trigger.to_state.attributes.MASTER }}",
    (
        "{% set ns = namespace(vmc_master=1, b=2) %}{% set ns.vmc_master = ns.vmc_master + 1 %}"
        "{% set ns.c_MASTER = 3 %}{{ ns.vmc_master }}{{ ns.b }}{{ ns.c_MASTER }}{{ ns.c_cucina }}"
    ),
    "{{ states.sensor.vmc_master_t.state }}|{{ states('sensor.vmc_master_t') }}",
    "{{ state_attr('sensor.vmc_master_t', 'attr_master') }}|{{ 'Master MASTER master' }}",
    "{% for vmc_master in [1, 2] %}{{ vmc_master }}{% endfor %}{{ vmc_master }}",
    "{% set vmc_master_esito %}{{ x_master }}{% endset %}{{ vmc_master_esito | trim }}",
]

# Costrutti che il traduttore non conosce: la traduzione si ferma.
NON_TRADUCIBILI = [
    "{% macro m(a) %}{{ a }}{% endmacro %}{{ m(1) }}",
    "{% macro m() %}{{ caller() }}{% endmacro %}{% call m() %}x{% endcall %}",
    "{% filter upper %}a{% endfilter %}",
    "{% with a = 1 %}{{ a }}{% endwith %}",
    "{% for i in m recursive %}{{ loop(i) }}{% endfor %}",
    "{{ range(3) | list }}",
    "{{ max(1, 2) }}",
    "{{ set([1]) }}",
    "{{ x | nessun_filtro }}",
]


def _stato_trigger() -> dict[str, Any]:
    return {
        "platform": "state",
        "id": "ON|famiglia|10|testo",
        "entity_id": "sensor.t1",
        "from_state": State("sensor.t1", "20", {"unit": "°C"}),
        "to_state": State("sensor.t1", "21.5", {"unit": "°C"}),
    }


VARIABILI: list[dict[str, Any]] = [
    {},
    {
        "x": 5,
        "y": "3",
        "s": "abc,def",
        "lista": [3, "a", None, 1.5, True],
        "d": {"a": 1, "b": [1, 2], "items": "campo"},
        "dizionari": [{"a": 1, "b": "u"}, {"a": 2, "b": "d"}, {"b": "n"}],
        "entita": ["sensor.t1", "sensor.t2", "sensor.nessuno"],
        "m": [[1, 2], [3]],
        "n": None,
        "f": 2.55,
        "trigger": _stato_trigger(),
    },
    {
        "x": "7.5",
        "y": 0,
        "s": "",
        "lista": [],
        "d": {},
        "dizionari": [],
        "entita": [],
        "m": [],
        "n": "None",
        "f": -1.25,
        "trigger": {"platform": None},
    },
    {
        "x": None,
        "y": [1, 2],
        "s": "unknown",
        "lista": ["b", "a", "c", "a"],
        "d": {"a": None, "b": "xy"},
        "dizionari": [{"a": 1}, {"a": "1", "b": 2}],
        "entita": ["sensor.t2", "input_boolean.a"],
        "m": [[], [5, 0]],
        "n": 0,
        "f": 0.5,
        "q": "q",
    },
    {
        "x": 125,
        "y": "abc",
        "s": "Aa1 2026",
        "lista": [10, 2.5, -1, "4"],
        "d": {"a": [1], "b": {"c": 1}},
        "dizionari": [{"a": 1, "b": "x"}, {"a": 1, "b": "y"}],
        "entita": ["sensor.t1"],
        "m": [[1], [2, 3, 4]],
        "n": False,
        "f": 1e-7,
    },
]


# --- Banco ------------------------------------------------------------------------------


class Banco:
    """Traduce i modelli e li confronta con Home Assistant."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        ambiente = TemplateEnvironment(hass)
        self.traduttore = Traduttore(
            filtri_ha={n for n in ambiente.filters if not hasattr(J, f"f_{n}")},
            test_ha={n for n in ambiente.tests if not hasattr(J, f"t_{n}")},
            globali_ha=set(ambiente.globals),
        )
        self.c = Contesto(hass)
        self.confronti = 0
        self.errori = 0
        self.differenze: list[str] = []

    def funzione(self, sorgente: str) -> Any:
        """La funzione tradotta di ``sorgente`` (codice generato e compilato)."""
        nome = self.traduttore.funzione(sorgente)
        spazio: dict[str, Any] = {"J": J}
        codice = "\n\n\n".join(self.traduttore.codice)
        exec(compile(codice, "<modelli>", "exec"), spazio)  # noqa: S102
        return spazio[nome]

    def confronta(self, sorgente: str) -> None:
        funzione = self.funzione(sorgente)
        modello_ha = Template(sorgente, self.hass)
        modello_motore = self.c.modello(funzione, sorgente)
        for V in VARIABILI:
            for interpreta in (False, True):
                atteso = _esito(
                    lambda: modello_ha.async_render(V, parse_result=interpreta)  # noqa: B023
                )
                ottenuto = _esito(
                    lambda: modello_motore.async_render(V, parse_result=interpreta)  # noqa: B023
                )
                self.confronti += 1
                self.errori += atteso[0] == "errore"
                if atteso != ottenuto:
                    self.differenze.append(
                        f"{sorgente!r} (parse_result={interpreta}) con "
                        f"{ {k: v for k, v in V.items() if k != 'trigger'} }:\n"
                        f"    HA     {atteso!r}\n    motore {ottenuto!r}"
                    )
            # le letture annotate (entità, domini, tempo): da queste dipendono i trigger
            # «template» (che rendono con parse_result) e le attese; un testo senza Jinja
            # resta un Template di Home Assistant anche nel motore (c.statico)
            if modello_ha.is_static:
                continue
            for interpreta in (False, True):
                atteso = _letture(
                    modello_ha.async_render_to_info(V, parse_result=interpreta)
                )
                ottenuto = _letture(
                    modello_motore.async_render_to_info(V, parse_result=interpreta)
                )
                if atteso != ottenuto:
                    self.differenze.append(
                        f"{sorgente!r} (letture, parse_result={interpreta}) con "
                        f"{ {k: v for k, v in V.items() if k != 'trigger'} }:\n"
                        f"    HA     {atteso!r}\n    motore {ottenuto!r}"
                    )


def _esito(rendi: Any) -> tuple[Any, ...]:
    """Il risultato di una resa in una forma confrontabile: tipo, testo e valore."""
    try:
        valore = rendi()
    except TemplateError:
        return ("errore",)
    testo = _INDIRIZZO.sub(" at 0x…", str(valore))
    if isinstance(valore, ResultWrapper):
        return ("contenitore", type(valore), testo, valore.render_result)
    if isinstance(valore, float) and math.isnan(valore):
        return ("nan",)
    return (type(valore), testo)


def _letture(info: RenderInfo) -> tuple[Any, ...]:
    """Il risultato e quello che la resa ha letto (come lo usano trigger e attese)."""
    return (
        _esito(info.result),
        sorted(info.entities),
        sorted(info.domains),
        sorted(info.domains_lifecycle),
        info.all_states,
        info.all_states_lifecycle,
        info.has_time,
        info.rate_limit,
        info.is_static,
    )


@pytest.fixture
def banco(hass: HomeAssistant, freezer: FrozenDateTimeFactory) -> Iterator[Banco]:
    """Stati fissi e orologio fermo; gli avvisi degli indefiniti non vanno nel registro."""
    freezer.move_to(datetime(2026, 11, 25, 10, 0, tzinfo=UTC))
    hass.states.async_set(
        "sensor.t1", "21.5", {"unit": "°C", "friendly_name": "T1", "lista": [1, 2]}
    )
    hass.states.async_set("sensor.t2", "on", {"unit": None})
    hass.states.async_set("input_boolean.a", "on")
    hass.states.async_set("binary_sensor.x", "off")
    registro = logging.getLogger("homeassistant.helpers.template")
    livello = registro.level
    registro.setLevel(logging.CRITICAL)
    yield Banco(hass)
    registro.setLevel(livello)


@pytest.mark.parametrize("gruppo", sorted(MODELLI))
async def test_modelli_scelti_come_home_assistant(banco: Banco, gruppo: str) -> None:
    """Stesso testo, stesso valore interpretato, o errore in tutte e due."""
    for sorgente in MODELLI[gruppo]:
        banco.confronta(sorgente)
    assert banco.confronti == len(MODELLI[gruppo]) * len(VARIABILI) * 2
    # il banco deve rendere davvero (non solo errori)
    assert banco.errori < banco.confronti / 2
    assert not banco.differenze, f"{len(banco.differenze)} differenze:\n" + "\n".join(
        banco.differenze[:400]
    )


def _rinomina(valore: Any, nome: str) -> Any:
    """Testi, chiavi e stati come li scrive il package per la VMC ``nome`` (la VMC
    «master» usa il package com'è, come ``Contesto.N``)."""
    if isinstance(valore, str):
        return valore if nome == "master" else rinomina(valore, nome)
    if isinstance(valore, dict):
        return {_rinomina(k, nome): _rinomina(v, nome) for k, v in valore.items()}
    if isinstance(valore, list):
        return [_rinomina(v, nome) for v in valore]
    if isinstance(valore, State):
        return State(
            _rinomina(valore.entity_id, nome),
            _rinomina(valore.state, nome),
            _rinomina(dict(valore.attributes), nome),
        )
    return valore


@pytest.mark.parametrize("vmc", ["master", "cucina"])
async def test_nomi_con_master_per_ogni_vmc(banco: Banco, vmc: str) -> None:
    """Per ogni VMC il modello tradotto rende come il modello rinominato in Home
    Assistant, con variabili e stati rinominati."""
    hass = banco.hass
    attributi = {"attr_master": "a", "MASTER": "b"}
    V = {
        "x": 1,
        "x_master": "valore",
        "y_Master": None,
        "d": {"vmc_master_a": 3},
        "trigger": {
            "to_state": State("sensor.vmc_master_t", "7", attributi),
        },
    }
    hass.states.async_set(
        _rinomina("sensor.vmc_master_t", vmc), "7", _rinomina(attributi, vmc)
    )
    c = Contesto(hass, vmc)
    V_vmc = _rinomina(V, vmc)
    for sorgente in MODELLI_NOMI:
        funzione = banco.funzione(sorgente)
        atteso = _esito(
            lambda: Template(_rinomina(sorgente, vmc), hass).async_render(V_vmc)  # noqa: B023
        )
        ottenuto = _esito(lambda: c.modello(funzione, sorgente).async_render(V_vmc))  # noqa: B023
        banco.confronti += 1
        if atteso != ottenuto:
            banco.differenze.append(
                f"{sorgente!r}:\n    HA     {atteso!r}\n    motore {ottenuto!r}"
            )
    assert not banco.differenze, "\n".join(banco.differenze)


@pytest.mark.parametrize("sorgente", NON_TRADUCIBILI)
async def test_costrutti_sconosciuti_fermano_la_traduzione(
    banco: Banco, sorgente: str
) -> None:
    """Un costrutto senza traduzione ferma il traduttore."""
    with pytest.raises(NonTraducibile):
        banco.traduttore.funzione(sorgente)
