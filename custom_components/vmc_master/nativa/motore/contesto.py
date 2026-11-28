"""Il contesto del motore su Home Assistant, con le entità di oggi (fase 3).

Il codice tradotto non legge mai Home Assistant da solo: passa da qui. In questa fase il
motore lavora sugli aiutanti e sui sensori del package, così si confronta con
l'automazione di oggi nel simulatore; le funzioni dei modelli che leggono gli stati
(``states``, ``is_state``, ``state_attr``, ``now``...) sono quelle stesse del motore dei
modelli di Home Assistant, che annotano le entità lette (``RenderInfo``) per i trigger e
le attese. Nella fase 4 un altro contesto, con la stessa interfaccia, legge le entità
native.

Un modello tradotto è una funzione ``f(c, V) -> str``: ``c`` è questo contesto, ``V`` le
variabili viste dal modello (una variabile che non c'è vale indefinito). ``ModelloHA`` lo
rende un ``Template`` di Home Assistant, così trigger, attese e condizioni lo usano con le
regole di sempre (``async_render_to_info``, ``TrackTemplateResultInfo``...).
"""

from __future__ import annotations

import re
from ast import literal_eval
from collections.abc import Callable, Iterable, Mapping
from functools import lru_cache, partial
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    HomeAssistant,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.template import (
    MAX_TEMPLATE_OUTPUT,
    RESULT_WRAPPERS,
    Template,
    TemplateEnvironment,
    template_cv,
)
from homeassistant.util import dt as dt_util
from jinja2.runtime import new_context
from jinja2.utils import _PassArg

from ...trasforma import rinomina
from . import jinja as J
from .esecuzione import ErroreCondizione, Modello
from .memoria_interna import HassConMemoria, MemoriaInterna, StatiConMemoria
from .seguire import segui_modello
from .stati_logiche import stati_logiche
from .timer import DOMINIO_SERVIZI, DOMINIO_TIMER

if TYPE_CHECKING:
    from ..comandi import ScritturaComandi
    from .esecuzione import Esecuzione
    from .interni import ComandiVMC, ScriptInterni
    from .timer import TimerDelMotore

Funzione = Callable[["Contesto", Mapping[str, Any]], str]


# I bersagli di un servizio oltre a ``entity_id``.
_ALTRI_BERSAGLI = ("device_id", "area_id", "floor_id", "label_id")
# Aggiorna le entità: i valori interni non sono entità, si tolgono dai bersagli e li
# riscrive il motore (``Contesto._aggiorna_con_interni``).
AGGIORNA_ENTITA = "homeassistant.update_entity"


def _solo_interni(memoria: MemoriaInterna, validati: Mapping[str, Any]) -> bool:
    """Se una chiamata validata ha come bersaglio solo valori interni (almeno uno)."""
    entita = validati.get(ATTR_ENTITY_ID)
    if not isinstance(entita, list) or not entita:
        return False
    if any(validati.get(altro) for altro in _ALTRI_BERSAGLI):
        return False
    return all(entity_id in memoria for entity_id in entita)


def _entita_aggiornate(
    dati: dict[str, Any] | None, bersaglio: dict[str, Any] | None
) -> list[str]:
    """Le entità di ``homeassistant.update_entity`` in ordine (il bersaglio vale sui
    dati, come in ``ServiceRegistry.async_call``)."""
    for valori in (bersaglio, dati):
        if valori and (entita := valori.get(ATTR_ENTITY_ID)) is not None:
            try:
                elenco = cv.comp_entity_ids(entita)
            except probatio.Invalid:
                return []
            return elenco if isinstance(elenco, list) else []
    return []


def _senza_interni(
    memoria: MemoriaInterna, valori: dict[str, Any] | None
) -> dict[str, Any] | None:
    """I dati (o il bersaglio) senza i valori interni tra le entità, scritti come
    sono se non ce ne sono."""
    if not valori or (entita := valori.get(ATTR_ENTITY_ID)) is None:
        return valori
    try:
        elenco = cv.comp_entity_ids(entita)
    except probatio.Invalid:
        return valori
    if not isinstance(elenco, list) or not any(e in memoria for e in elenco):
        return valori
    return {**valori, ATTR_ENTITY_ID: [e for e in elenco if e not in memoria]}


class _Sorgente:
    """Il testo di un modello tradotto (``funzione.sorgente``) con il nome della VMC.

    Va in ``template_cv`` al posto del testo: si calcola solo se un messaggio d'errore lo
    scrive (``str``).
    """

    __slots__ = ("_c", "_funzione")

    def __init__(self, c: Contesto, funzione: Funzione) -> None:
        self._c = c
        self._funzione = funzione

    def __str__(self) -> str:
        return self._c.N(getattr(self._funzione, "sorgente", ""))


class VistaModello:
    """Le variabili come le vede un modello: una variabile che non c'è vale indefinito.

    È una vista sulle variabili, non una copia: la resa è sincrona e un modello non cambia
    le variabili che riceve (``{% set %}`` resta nel modello), quindi legge gli stessi
    valori che Home Assistant copia all'inizio della resa (``kwargs.update(variables)``),
    senza copiarle a ogni resa. Il codice tradotto la legge solo con ``V[nome]`` e
    ``V.get(nome, predefinito)``.
    """

    __slots__ = ("_variabili",)

    def __init__(self, variabili: Mapping[str, Any]) -> None:
        self._variabili = variabili

    def __getitem__(self, nome: str) -> Any:
        try:
            return self._variabili[nome]
        except KeyError:
            return J.indefinito(nome)

    def get(self, nome: str, predefinito: Any = None) -> Any:
        try:
            return self._variabili[nome]
        except KeyError:
            return predefinito


# --- come Home Assistant interpreta un modello reso ------------------------------------------
#
# Da homeassistant/helpers/template/__init__.py di Home Assistant 2026.11.2 (Apache-2.0,
# licenza nel file LICENSE-Apache-2.0.txt dell'integrazione): ``_parse_result``,
# ``_copy_literal`` e ``_cached_parse_result``, le stesse righe.

_IS_NUMERIC = re.compile(r"^[+-]?(?!0\d)\d*(?:\.\d*)?$", re.ASCII)
_EVAL_CACHE_SIZE = 512


def interpreta_resa(render_result: str) -> Any:
    """Il risultato di un modello reso, interpretato come ``Template.async_render``."""
    if _IS_NUMERIC.match(render_result):
        if "." in render_result:
            try:
                return float(render_result)
            except ValueError:
                pass
        else:
            try:
                return int(render_result)
            except ValueError:
                pass
    result = _interpretato(render_result)
    # The cached result is shared, so hand out containers the caller can mutate
    if (wrapper := RESULT_WRAPPERS.get(type(result))) is not None:
        return wrapper(_copia_letterale(result), render_result=render_result)
    return result


def _copia_letterale(value: Any) -> Any:
    """Copy the containers of a literal_eval result, sharing immutable leaves."""
    value_type = type(value)
    if value_type is list:
        return [_copia_letterale(item) for item in value]
    if value_type is dict:
        return {key: _copia_letterale(item) for key, item in value.items()}
    if value_type is tuple:
        return tuple([_copia_letterale(item) for item in value])
    if value_type is set:
        return value.copy()
    return value


@lru_cache(maxsize=_EVAL_CACHE_SIZE)
def _interpretato(render_result: str) -> Any:
    """Parse a result and cache the result (containers unwrapped)."""
    try:
        result = literal_eval(render_result)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return render_result
    if not isinstance(result, (str, complex)) and (
        not isinstance(result, (int, float))
        or isinstance(result, bool)
        or _IS_NUMERIC.match(render_result) is not None
    ):
        return result
    return render_result


class ModelloHA(Template):
    """Un modello tradotto con l'interfaccia di ``Template`` (come lo usa Home Assistant).

    ``sorgente`` è il testo Jinja del package: serve solo per i messaggi nel registro e
    come chiave (due modelli con lo stesso testo sono lo stesso modello).
    """

    __slots__ = ("_c", "_funzione")

    def __init__(self, c: Contesto, funzione: Funzione, sorgente: str) -> None:
        super().__init__(sorgente, c.hass)
        self.is_static = False
        self._c = c
        self._funzione = funzione

    def ensure_valid(self) -> None:
        """Il codice tradotto è già valido."""

    def async_render(  # type: ignore[override]
        self,
        variables: Mapping[str, Any] | None = None,
        parse_result: bool = True,
        limited: bool = False,
        strict: bool = False,
        log_fn: Callable[[int, str], None] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Come ``Template.async_render``: testo senza spazi ai bordi, poi interpretato."""
        # come ``kwargs.update(variables)``, senza copiare le variabili quando non ci sono
        # altri argomenti per nome (sempre, dal motore e da Home Assistant)
        if kwargs:
            if variables is not None:
                kwargs.update(variables)
            variables = kwargs
        elif variables is None:
            variables = kwargs
        resa = self._c.testo(self._funzione, variables)
        if not parse_result:
            return resa
        return interpreta_resa(resa)


class Contesto:
    """Il motore di una VMC su Home Assistant, con le entità di oggi."""

    def __init__(self, hass: HomeAssistant, nome: str = "master") -> None:
        self.hass = hass
        self.nome = nome
        # come l'automazione: un errore si registra e l'esecuzione finisce (nei test si
        # può chiedere di rilanciarlo)
        self.rilancia_errori = False
        self._nomi: dict[str, str] = {}
        self._modelli: dict[int, ModelloHA] = {}
        self._statici: dict[str, Template] = {}
        # la memoria interna (fase 4): senza, i valori interni sono gli aiutanti di oggi
        self.memoria: MemoriaInterna | None = None
        # senza memoria interna i modelli vedono gli stati di Home Assistant e quelli
        # delle logiche (le automazioni del package, che non sono entità)
        self._funzioni_dei_modelli(
            HassConMemoria(hass, StatiConMemoria(hass.states, stati_logiche(hass).stati))
        )
        # script del motore per nome di servizio (script.<nome>), li registra ha.py
        self.script: dict[str, Any] = {}
        # fase 4: gli script e i comandi di shell del package dentro il motore (li mette
        # ha.py); None: sono quelli di Home Assistant (script e shell_command)
        self.interni: ScriptInterni | None = None
        self.comandi: ComandiVMC | None = None
        # i timer del motore (timer.TimerDelMotore), se il motore li ha: servizi
        # ``motore_timer.*`` e letture ``c.timer.*`` del codice tradotto con timer_motore
        self.timer: TimerDelMotore | None = None
        # fase 4: le scritture sulle impostazioni native (comandi.ScritturaComandi, la
        # mette assemblaggio.py): i servizi degli aiutanti di oggi (input_boolean.turn_on...)
        # vanno alle entità native; None: sono quelli degli aiutanti di Home Assistant
        self.scrittura: ScritturaComandi | None = None

    def _funzioni_dei_modelli(self, hass: Any) -> None:
        """Le funzioni dei modelli che leggono Home Assistant: quelle del motore dei
        modelli di Home Assistant, con le stesse letture annotate per trigger e attese.
        ``hass`` è ``HassConMemoria``: lo stesso Home Assistant con una macchina degli
        stati che vede anche i valori interni (gli stati delle logiche e, con la memoria
        interna, i suoi valori)."""
        # la macchina degli stati che leggono le condizioni «state»
        self.stati = hass.states
        ambiente = self._ambiente = TemplateEnvironment(hass)
        self._contesto_jinja = new_context(ambiente, None, {})
        globali = ambiente.globals
        self.states = self._diretta(globali["states"])
        self.is_state = self._diretta(globali["is_state"])
        self.state_attr = self._diretta(globali["state_attr"])
        self.now = self._diretta(globali["now"])
        self.utcnow = self._diretta(globali["utcnow"])
        self.integration_entities = self._diretta(globali["integration_entities"])
        self.expand = self._diretta(globali["expand"])
        self.device_name = self._diretta(globali["device_name"])
        self.entity_name = self._diretta(globali["entity_name"])
        self._filtri = {n: self._diretta(f) for n, f in ambiente.filters.items()}
        self._test = {n: self._diretta(f) for n, f in ambiente.tests.items()}

    # --- memoria interna (fase 4) ---------------------------------------------------------

    def usa_memoria(self, memoria: MemoriaInterna) -> None:
        """Da qui i valori interni sono nella memoria: i modelli e le condizioni li
        leggono da lì, i servizi degli aiutanti che li hanno tutti come bersaglio li
        scrivono lì (``chiama_servizio``)."""
        self.memoria = memoria
        self._funzioni_dei_modelli(memoria.hass_modelli)

    def memoria_interna(self, chiavi: Iterable[str]) -> None:
        """Il codice generato con i valori interni dichiara le loro chiavi: con una
        memoria data al motore (``Motore(..., memoria=...)``) la usa, altrimenti ne crea
        una con i valori iniziali degli aiutanti (senza archivio)."""
        chiavi = tuple(chiavi)
        if (memoria := self.memoria) is None:
            memoria = MemoriaInterna(self.hass, self.nome, chiavi)
            memoria.ripristina()
            self.usa_memoria(memoria)
        elif mancanti := set(chiavi) - set(memoria.chiavi()):
            raise ValueError(f"valori interni senza memoria: {sorted(mancanti)}")

    def _diretta(self, funzione: Any) -> Any:
        """Una funzione del motore dei modelli chiamabile dal codice tradotto: come la
        chiama Jinja, con il contesto, il contesto di valutazione o l'ambiente davanti se
        li chiede (``pass_context``...)."""
        tipo = _PassArg.from_obj(funzione)
        if tipo is _PassArg.context:
            return partial(funzione, self._contesto_jinja)
        if tipo is _PassArg.eval_context:
            return partial(funzione, self._contesto_jinja.eval_ctx)
        if tipo is _PassArg.environment:
            return partial(funzione, self._ambiente)
        return funzione

    # --- nomi ----------------------------------------------------------------------------

    def N(self, testo: str) -> str:
        """Un testo del package con il nome di questa VMC (come ``trasforma.rinomina``)."""
        if self.nome == "master":
            return testo
        if (fatto := self._nomi.get(testo)) is None:
            fatto = self._nomi[testo] = rinomina(testo, self.nome)
        return fatto

    def oggetto(self, entity_id: str) -> Any:
        """``states.<dominio>.<oggetto>`` di un modello (lo stato, o indefinito)."""
        dominio, _, nome = entity_id.partition(".")
        return getattr(getattr(self.states, dominio), nome)

    # --- servizi -------------------------------------------------------------------------

    async def chiama_servizio(
        self,
        r: Esecuzione,
        dominio_servizio: str,
        dati: dict[str, Any],
        bersaglio: dict[str, Any],
        *,
        risposta: bool = False,
    ) -> ServiceResponse:
        """Chiamata di un servizio dal motore (come _async_step_call_service).

        Un servizio che non esiste solleva ServiceNotFound dalla chiamata stessa. Con gli
        script e i comandi dentro il motore, ``script.*`` e ``shell_command.*`` del
        package vanno a loro, con lo stesso nome (anche reso da un modello). Con le
        impostazioni native (fase 4, ``scrittura``) i servizi degli aiutanti di oggi
        vanno a ``ScritturaComandi``.
        """
        dominio, _, servizio = dominio_servizio.partition(".")
        if self.timer is not None and dominio.lower() in (
            DOMINIO_SERVIZI,
            DOMINIO_TIMER,
        ):
            # i servizi dei timer del motore: ``motore_timer.<servizio>`` del codice
            # tradotto con timer_motore, o ``timer.<servizio>`` reso da un modello (i
            # timer del package sono quelli del motore). Come i servizi dei timer di Home
            # Assistant: non restituiscono dati; il nome anche in maiuscolo.
            servizio = servizio.lower()
            if risposta:
                raise probatio.Invalid(
                    "Script does not support 'response_variable' for service "
                    f"'{DOMINIO_TIMER}.{servizio}' which does not support response data."
                )
            await self.timer.servizio(servizio, dati, bersaglio, r.contesto)
            return None
        if (memoria := self.memoria) is not None:
            if memoria.gestisce(dominio, servizio):
                unione = dict(dati or {})
                if bersaglio:
                    unione.update(bersaglio)
                validati = memoria.valida(dominio, servizio, unione)
                if _solo_interni(memoria, validati):
                    if risposta:
                        raise probatio.Invalid(
                            "Script does not support 'response_variable' for service "
                            f"'{dominio}.{servizio}' which does not support response "
                            "data."
                        )
                    await memoria.async_chiama(
                        dominio, servizio, unione, r.contesto, validati
                    )
                    return None
            elif dominio_servizio == AGGIORNA_ENTITA:
                entita = _entita_aggiornate(dati, bersaglio)
                dati, bersaglio = (
                    _senza_interni(memoria, dati),
                    _senza_interni(memoria, bersaglio),
                )
                if any(entity_id in memoria for entity_id in entita):
                    await self._aggiorna_con_interni(
                        memoria, entita, dati, bersaglio, r.contesto
                    )
                    return None
        if dominio == "script" and self.interni is not None:
            if self.interni.gestisce(servizio, dati, bersaglio):
                return await self.interni.chiama(
                    servizio, dati, bersaglio, r.contesto, risposta=risposta
                )
        elif (
            dominio == "shell_command"
            and self.comandi is not None
            and servizio in self.comandi
        ):
            return await self.comandi.esegui(
                servizio, dati, bersaglio, r.contesto, risposta=risposta
            )
        if self.scrittura is not None and self.scrittura.gestisce(dominio.lower()):
            # i servizi degli aiutanti di oggi sulle impostazioni native (il nome anche in
            # maiuscolo, come in Home Assistant): come i servizi degli aiutanti, nessuno
            # restituisce dati
            if risposta:
                raise probatio.Invalid(
                    "Script does not support 'response_variable' for service "
                    f"'{dominio}.{servizio}' which does not support response data."
                )
            await self.scrittura.chiama(
                f"{dominio.lower()}.{servizio.lower()}", dati, r.contesto, bersaglio
            )
            return None
        servizi = self.hass.services
        if servizi.has_service(dominio, servizio):
            supporto = servizi.supports_response(dominio, servizio)
            if supporto == SupportsResponse.ONLY and not risposta:
                raise probatio.Invalid(
                    "Script requires 'response_variable' for response data "
                    f"for service call {dominio}.{servizio}"
                )
            if supporto == SupportsResponse.NONE and risposta:
                raise probatio.Invalid(
                    "Script does not support 'response_variable' for service "
                    f"'{dominio}.{servizio}' which does not support response data."
                )
        return await servizi.async_call(
            dominio,
            servizio,
            dati,
            blocking=True,
            context=r.contesto,
            target=bersaglio,
            return_response=risposta,
        )

    async def _aggiorna_con_interni(
        self,
        memoria: MemoriaInterna,
        entita: list[str],
        dati: dict[str, Any] | None,
        bersaglio: dict[str, Any] | None,
        contesto: Context | None,
    ) -> None:
        """``homeassistant.update_entity`` con dei valori interni tra le ``entita``.

        Oggi il servizio aggiorna ogni entità in un compito suo, creati in fila
        (``asyncio.gather``): un aiutante si riscrive (``state_reported``) nel suo turno,
        subito dopo l'entità che lo precede nell'elenco. Qui il servizio (senza i valori
        interni: ``dati`` e ``bersaglio``) parte in un compito che va avanti subito, fino
        all'attesa dei compiti delle sue entità, e ogni valore interno si riscrive in un
        passo messo in fila dopo di loro; quelli prima della prima entità si mettono in
        fila prima della chiamata. Un valore interno tra due entità si riscriverebbe dopo
        tutte e due: nel package i valori interni sono sempre dopo le entità.
        """
        primi = 0
        while primi < len(entita) and entita[primi] in memoria:
            primi += 1
        in_fila = self.hass.loop.call_soon
        for entity_id in entita[:primi]:
            in_fila(memoria.riscrivi, entity_id)
        chiamata = self.hass.async_create_task(
            self.hass.services.async_call(
                "homeassistant",
                "update_entity",
                dati,
                blocking=True,
                context=contesto,
                target=bersaglio,
            ),
            eager_start=True,
        )
        for entity_id in entita[primi:]:
            if entity_id in memoria:
                in_fila(memoria.riscrivi, entity_id)
        await chiamata

    # --- tempo ---------------------------------------------------------------------------

    def adesso_utc(self) -> Any:
        return dt_util.utcnow()

    # --- filtri e test che leggono Home Assistant -----------------------------------------

    def filtro(self, nome: str) -> Callable[..., Any]:
        """Un filtro di Home Assistant che ha bisogno di ``hass`` (per esempio ``state_attr``)."""
        return self._filtri[nome]

    def test(self, nome: str) -> Callable[..., Any]:
        """Un test di Home Assistant che ha bisogno di ``hass`` (per esempio ``is_state``)."""
        return self._test[nome]

    # --- modelli -------------------------------------------------------------------------

    def testo(self, funzione: Funzione, variabili: Mapping[str, Any]) -> str:
        """La resa di un modello come ``Template.async_render(parse_result=False)``.

        Ogni errore della resa diventa ``TemplateError``, come in Home Assistant. Durante
        la resa ``template_cv`` dice quale modello si rende (come ``render_with_context``):
        lo leggono i messaggi d'errore «senza predefinito» (anche dei filtri di Home
        Assistant), con il testo del modello per questa VMC.
        """
        template_cv.set((_Sorgente(self, funzione), "rendering"))  # type: ignore[arg-type]
        try:
            resa = funzione(self, VistaModello(variabili))
        except Exception as err:
            raise TemplateError(err) from err
        finally:
            template_cv.set(None)
        if len(resa) > MAX_TEMPLATE_OUTPUT:
            raise TemplateError(
                f"Template output exceeded maximum size of {MAX_TEMPLATE_OUTPUT} characters"
            )
        return resa.strip()

    def resa_complessa(self, valore: Any, variabili: Mapping[str, Any]) -> Any:
        """Come ``template.render_complex``: liste, dizionari e modelli (interpretati).

        Un modello si interpreta come ``Template.async_render`` (``interpreta_resa``): una
        lista, un dizionario, un insieme o una tupla resi sono quelli di Home Assistant
        (sottoclassi che si scrivono come sono stati resi), così un modello successivo li
        indicizza, li scorre e li scrive allo stesso modo."""
        if isinstance(valore, list):
            return [self.resa_complessa(v, variabili) for v in valore]
        if isinstance(valore, Mapping):
            return {
                self.resa_complessa(k, variabili): self.resa_complessa(v, variabili)
                for k, v in valore.items()
            }
        if isinstance(valore, Modello):
            return interpreta_resa(self.testo(valore.funzione, variabili))
        return valore

    def modello(self, funzione: Funzione, sorgente: str = "") -> ModelloHA:
        """Il ``Template`` di un modello tradotto (uno per funzione)."""
        chiave = id(funzione)
        if (modello := self._modelli.get(chiave)) is None:
            modello = self._modelli[chiave] = ModelloHA(
                self,
                funzione,
                sorgente or getattr(funzione, "sorgente", "") or funzione.__name__,
            )
        return modello

    def statico(self, testo: str) -> Template:
        """Un ``Template`` senza Jinja di un trigger (per esempio ``event_type``)."""
        if (modello := self._statici.get(testo)) is None:
            modello = self._statici[testo] = Template(testo, self.hass)
        return modello

    def condizione(self, funzione: Funzione, variabili: Mapping[str, Any]) -> bool:
        """Condizione ``template`` (come ``condition.async_template``).

        Home Assistant la rende con ``async_render_to_info``: le letture si annotano, ma
        l'esito dipende solo dal testo.
        """
        modello = self.modello(funzione)
        try:
            info = modello.async_render_to_info(variabili, parse_result=False)
            valore = info.result()
        except TemplateError as err:
            raise ErroreCondizione(f"In 'template' condition: {err}") from err
        return valore.lower() == "true"

    def segui_attesa(
        self, funzione: Funzione, variabili: Mapping[str, Any], vero: Callable[[], None]
    ) -> CALLBACK_TYPE:
        """Attesa di un ``wait_template``: ``vero`` quando il modello passa a vero
        (come ``async_track_template`` usato da ``_async_step_wait_template``: con
        ``seguire.segui_modello``, che segue anche i valori interni)."""

        @callback
        def _cambiato(*_: Any) -> None:
            vero()

        return segui_modello(self.hass, self.modello(funzione), _cambiato, variabili)
