"""Le condizioni del motore, con le regole di ``homeassistant.helpers.condition``.

Il codice tradotto scrive ogni condizione come una funzione ``k(c, V) -> bool`` che usa
queste: ``modello`` (``condition: template``), ``stato`` (``condition: state``),
``trigger`` (``condition: trigger``), ``e``/``o``/``non`` (``and``/``or``/``not``).

Una condizione che non si può valutare (modello in errore, entità che non esiste) solleva
``ErroreCondizione``; ``e``, ``o``, ``non`` e ``stato`` raccolgono gli errori
(``ConditionError``) come Home Assistant: vanno avanti con le altre condizioni e sollevano
l'errore solo se nessuna ha deciso.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from datetime import timedelta
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.exceptions import ConditionError, TemplateError
from homeassistant.helpers import config_validation as cv
from homeassistant.util import dt as dt_util

from .esecuzione import ErroreCondizione

if TYPE_CHECKING:
    from .contesto import Contesto

Condizione = Callable[["Contesto", Mapping[str, Any]], bool]


def modello(c: Contesto, funzione: Callable[..., str], V: Mapping[str, Any]) -> bool:
    """``condition: template`` (come ``async_template``)."""
    return c.condizione(funzione, V)


def trigger(V: Mapping[str, Any], ids: Iterable[str]) -> bool:
    """``condition: trigger`` (come ``async_trigger_from_config``)."""
    return "trigger" in V and V["trigger"].get("id") in ids


def e(c: Contesto, V: Mapping[str, Any], condizioni: Iterable[Condizione]) -> bool:
    """``condition: and`` (come AndConditionChecker)."""
    errori = []
    for condizione in condizioni:
        try:
            if condizione(c, V) is False:
                return False
        except ConditionError as err:
            errori.append(err)
    if errori:
        raise ErroreCondizione(f"In 'and': {errori}")
    return True


def o(c: Contesto, V: Mapping[str, Any], condizioni: Iterable[Condizione]) -> bool:
    """``condition: or`` (come OrConditionChecker)."""
    errori = []
    for condizione in condizioni:
        try:
            if condizione(c, V) is True:
                return True
        except ConditionError as err:
            errori.append(err)
    if errori:
        raise ErroreCondizione(f"In 'or': {errori}")
    return False


def non(c: Contesto, V: Mapping[str, Any], condizioni: Iterable[Condizione]) -> bool:
    """``condition: not`` (come NotConditionChecker)."""
    errori = []
    for condizione in condizioni:
        try:
            if condizione(c, V) is True:
                return False
        except ConditionError as err:
            errori.append(err)
    if errori:
        raise ErroreCondizione(f"In 'not': {errori}")
    return True


def stato(
    c: Contesto,
    V: Mapping[str, Any],
    entita: Iterable[str],
    stati: list[Any],
    *,
    per: Any = None,
    attributo: str | None = None,
    qualsiasi: bool = False,
) -> bool:
    """``condition: state`` (come ``state_from_config``: tutte le entità, o una con
    ``match: any``)."""
    errori = []
    esito = not qualsiasi
    for entity_id in entita:
        try:
            if _stato(c, V, entity_id, stati, per, attributo):
                esito = True
            elif not qualsiasi:
                return False
        except ConditionError as err:
            errori.append(err)
    if errori:
        raise ErroreCondizione(f"In 'state': {errori}")
    return esito


def _stato(
    c: Contesto,
    V: Mapping[str, Any],
    entity_id: str,
    stati: list[Any],
    per: Any,
    attributo: str | None,
) -> bool:
    """Come ``condition.state`` per un'entità (con la memoria interna, anche per un
    valore interno)."""
    macchina = c.stati
    if (oggetto := macchina.get(entity_id)) is None:
        raise ErroreCondizione(f"In 'state' condition: unknown entity {entity_id}")
    if attributo is not None and attributo not in oggetto.attributes:
        return False
    valore = oggetto.state if attributo is None else oggetto.attributes.get(attributo)
    vero = False
    for voluto in stati:
        atteso = voluto
        if isinstance(voluto, str) and cv.INPUT_ENTITY_ID.match(voluto) is not None:
            if not (altra := macchina.get(voluto)):
                raise ErroreCondizione(
                    f"In 'state' condition: the 'state' entity {voluto} is unavailable"
                )
            atteso = altra.state
        vero = valore == atteso
        if vero:
            break
    if per is None or not vero:
        return vero
    try:
        durata: timedelta = cv.positive_time_period(c.resa_complessa(per, V))
    except TemplateError as err:
        raise ErroreCondizione(f"In 'state' condition: template error: {err}") from err
    except probatio.Invalid as err:
        raise ErroreCondizione(f"In 'state' condition: schema error: {err}") from err
    return dt_util.utcnow() - durata > oggetto.last_changed
