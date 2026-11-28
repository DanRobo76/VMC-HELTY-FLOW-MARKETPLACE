"""Le automazioni del package dentro l'integrazione: le logiche del motore.

Fino alla 9.0.0b45 ogni automazione del package era un'entità del componente
``automation`` di Home Assistant (``AutomationEntity`` con il motore tradotto al posto di
``Script``). Ora è una ``Logica``: codice dell'integrazione, senza entità, con le stesse
regole di ``AutomationEntity`` di Home Assistant 2026.11.2
(``components/automation/entity.py``) per tutto ciò che il package usa:

- sempre attiva (nessuna automazione del package ha ``initial_state`` e nessuno la spegne):
  i trigger si agganciano subito se Home Assistant è avviato, altrimenti in un lavoro di
  avvio (``async_add_startup_job``), come ``_async_enable``;
- i trigger con ``attivazioni.inizializza_attivazioni`` (il codice dell'integrazione al
  posto di ``helpers.trigger``), più quelli delle chiamate dei comandi agganciati a
  ``ComandiVMC`` (prima degli altri) e quelli dei timer del motore;
- a ogni trigger: variabili, condizioni, contesto nuovo figlio di quello del trigger e la
  ``Sequenza`` con la sua modalità (``async_trigger``), con gli stessi messaggi nel
  registro (con il registro dell'integrazione: ``custom_components.vmc_master...``);
- lo stato che l'entità scriveva (``on``, ``id``, ``last_triggered``, ``mode``,
  ``current``, ``max``, ``friendly_name``) è uno stato interno (``StatiLogiche``): non è
  nella macchina degli stati, ma i modelli del motore lo leggono come prima (un modello
  aspetta che l'Automazione VMC Master non abbia esecuzioni in corso, ``current``) e lo
  seguono (``seguire.CambiInterni``), con gli stessi istanti e lo stesso contesto.

Non ci sono più: la traccia, l'evento ``automation_triggered``, le riparazioni di
``automation`` (servizio mancante), ``automation.reload``/``turn_off``/``trigger`` e lo
stato ripreso dopo un riavvio (``last_triggered``: nessuno lo legge).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.const import (
    ATTR_FRIENDLY_NAME,
    ATTR_ID,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    CoreState,
    HassJob,
    HomeAssistant,
    callback,
)
from homeassistant.exceptions import (
    ConditionError,
    ConditionErrorContainer,
    ConditionErrorIndex,
    HomeAssistantError,
    ServiceNotFound,
    TemplateError,
)
from homeassistant.helpers.entity import CONTEXT_RECENT_TIME_SECONDS
from homeassistant.helpers.script import script_stack_cv
from homeassistant.helpers.script_variables import ScriptVariables
from homeassistant.util import slugify

from .attivazioni import inizializza_attivazioni
from .chiusura import registro_sequenze
from .stati_logiche import StatiLogiche

if TYPE_CHECKING:
    from .contesto import Contesto
    from .definizioni import Automazione
    from .esecuzione import Sequenza
    from .interni import ComandiVMC

_LOGGER = logging.getLogger(__name__)

DOMINIO = "automation"
"""Il dominio degli entity_id degli stati interni delle logiche (``automation.<alias>``,
come le entità di prima: i modelli del package li leggono con questo nome)."""

ATTR_LAST_TRIGGERED = "last_triggered"
ATTR_MODE = "mode"
ATTR_CUR = "current"
ATTR_MAX = "max"

Attacca = Callable[..., Any]


class CondizioniAutomazione:
    """Le condizioni di un'automazione (come ``ConditionsChecker``): tutte vere; un
    errore si registra e vale falso."""

    def __init__(
        self, c: Contesto, condizioni: tuple[Any, ...], nome: str, logger: logging.Logger
    ) -> None:
        self.c = c
        self.condizioni = condizioni
        self.nome = nome
        self.logger = logger

    def async_check(self, *, variables: Mapping[str, Any] | None = None) -> bool:
        V = variables if variables is not None else {}
        errori: list[ConditionErrorIndex] = []
        for indice, condizione in enumerate(self.condizioni):
            try:
                if condizione(self.c, V) is False:
                    return False
            except ConditionError as err:
                errori.append(
                    ConditionErrorIndex(
                        "condition", index=indice, total=len(self.condizioni), error=err
                    )
                )
        if errori:
            self.logger.warning(
                "Error evaluating condition in '%s':\n%s",
                self.nome,
                ConditionErrorContainer("condition", errors=errori),
            )
            return False
        return True


class Logica:
    """Un'automazione del package con il motore tradotto, dentro l'integrazione."""

    def __init__(
        self,
        c: Contesto,
        definizione: Automazione,
        sequenza: Sequenza,
        stati: StatiLogiche,
        *,
        comandi: ComandiVMC | None = None,
        altre_piattaforme: Mapping[str, Attacca] | None = None,
        variabili: ScriptVariables | None = None,
    ) -> None:
        self.c = c
        self.hass: HomeAssistant = c.hass
        self.id = definizione.id
        self.nome = definizione.alias
        self.entity_id = f"{DOMINIO}.{slugify(definizione.alias)}"
        self.trigger = list(definizione.trigger)
        self.sequenza = sequenza
        self.stati = stati
        self.comandi = comandi
        self.altre_piattaforme = dict(altre_piattaforme or {})
        self.logger = logging.getLogger(
            f"{_LOGGER.name}.{self.entity_id.partition('.')[2]}"
        )
        self._condizioni = (
            CondizioniAutomazione(c, tuple(definizione.condizioni), self.nome, self.logger)
            if definizione.condizioni is not None
            else None
        )
        self._variabili = variabili
        self._attiva = False
        self._stacca: CALLBACK_TYPE | None = None
        self._togli_lavoro: CALLBACK_TYPE | None = None
        self._contesto: Context | None = None
        self._contesto_quando: float | None = None
        self._scaricata = False
        stati.aggiungi(self.entity_id)
        self._togli_registro = registro_sequenze(self.hass).iscrivi(sequenza)
        sequenza.al_cambio = self.scrivi_stato

    # --- stato ---------------------------------------------------------------------------

    @property
    def accesa(self) -> bool:
        """Come ``AutomationEntity.is_on``."""
        return self._stacca is not None or self._attiva

    def attributi(self) -> dict[str, Any]:
        """Gli attributi che scriveva l'entità, nello stesso ordine (``id``, poi
        ``extra_state_attributes``, poi il nome)."""
        attributi: dict[str, Any] = {}
        if self.id:
            attributi[ATTR_ID] = self.id
        attributi[ATTR_LAST_TRIGGERED] = self.sequenza.ultimo_avvio
        attributi[ATTR_MODE] = self.sequenza.modo
        attributi[ATTR_CUR] = len(self.sequenza.esecuzioni)
        if self.sequenza.con_massimo:
            attributi[ATTR_MAX] = self.sequenza.massimo
        attributi[ATTR_FRIENDLY_NAME] = self.nome
        return attributi

    @callback
    def scrivi_stato(self) -> None:
        """Come ``Entity.async_write_ha_state`` (anche ``change_listener``)."""
        if self._scaricata:
            return
        adesso = time.time()
        if (
            self._contesto_quando is not None
            and adesso - self._contesto_quando > CONTEXT_RECENT_TIME_SECONDS
        ):
            self._contesto = None
            self._contesto_quando = None
        self.stati.scrivi(
            self.entity_id,
            STATE_ON if self.accesa else STATE_OFF,
            self.attributi(),
            self._contesto,
            adesso,
        )

    def _this(self) -> dict[str, Any] | None:
        if (stato := self.stati.stato(self.entity_id)) is None:
            return None
        return stato.as_dict()  # type: ignore[return-value]

    # --- avvio e fermata -----------------------------------------------------------------

    async def avvia(self) -> None:
        """Come l'aggiunta dell'entità: ``async_added_to_hass`` (attiva) e la prima
        scrittura dello stato."""
        await self._attiva_logica()
        self.scrivi_stato()

    async def _attiva_logica(self) -> None:
        """Come ``AutomationEntity._async_enable``."""
        if self._attiva:
            return
        self._attiva = True
        if self.hass.state is not CoreState.not_running:
            await self._aggancia_se_serve()
            return
        # come Home Assistant: i trigger si agganciano dopo gli ascoltatori di
        # EVENT_HOMEASSISTANT_START e prima di EVENT_HOMEASSISTANT_STARTED
        self._togli_lavoro = self.hass.async_add_startup_job(
            HassJob(self._attiva_all_avvio)
        )

    async def _attiva_all_avvio(self) -> None:
        """Come ``_async_enable_automation``."""
        self._togli_lavoro = None
        if not self._attiva or self._stacca is not None:
            return
        await self._aggancia_se_serve()
        self.scrivi_stato()

    async def _aggancia_se_serve(self) -> None:
        """Come ``_async_attach_triggers_for_entity_id`` (l'entity_id non cambia)."""
        stacca = await self._aggancia()
        if not self._attiva or self._stacca is not None:
            if stacca is not None:
                stacca()
            return
        self._stacca = stacca or _niente

    async def ferma(self) -> None:
        """Come ``async_will_remove_from_hass``: niente più trigger, le esecuzioni in
        corso continuano fino alla fine della sequenza (``async_unload`` la ferma), lo
        stato interno si toglie."""
        if self._togli_lavoro is not None:
            self._togli_lavoro()
            self._togli_lavoro = None
        self._attiva = False
        if self._stacca is not None:
            self._stacca()
            self._stacca = None
        self._scaricata = True
        await self.sequenza.ferma()
        self._togli_registro()
        self.stati.togli(self.entity_id)

    # --- trigger -------------------------------------------------------------------------

    def _log(self, livello: int, messaggio: str, **kwargs: Any) -> None:
        """Come ``AutomationEntity._log_callback``."""
        self.logger.log(livello, "%s %s", messaggio, self.nome, **kwargs)

    async def _aggancia(self) -> CALLBACK_TYPE | None:
        """Come ``AutomationEntity._async_attach_triggers``, più i trigger delle chiamate
        dei comandi agganciati a ``ComandiVMC``: prima degli altri, come Home Assistant
        aggancia al bus i trigger ``event`` prima di aspettare gli altri trigger."""
        variabili = {"this": self._this()}
        comandi = (
            self.comandi.aggancia_trigger(
                self.trigger, self._scatta_se_attiva, str(self.nome)
            )
            if self.comandi is not None
            else None
        )
        try:
            altri = await inizializza_attivazioni(
                self.hass,
                self.trigger,
                self._scatta_se_attiva,
                DOMINIO,
                str(self.nome),
                self._log,
                variables=variabili,
                altri=self.altre_piattaforme,
            )
        except BaseException:
            if comandi is not None:
                comandi()
            raise
        if comandi is None or altri is None:
            return comandi or altri

        @callback
        def stacca() -> None:
            comandi()
            altri()

        return stacca

    async def _scatta_se_attiva(
        self,
        run_variables: dict[str, Any],
        context: Context | None = None,
        skip_condition: bool = False,
    ) -> None:
        """Come ``AutomationEntity._async_trigger_if_enabled``."""
        if not self._attiva:
            return
        await self.scatta(run_variables, context, skip_condition)

    async def scatta(
        self,
        run_variables: dict[str, Any],
        context: Context | None = None,
        skip_condition: bool = False,
    ) -> None:
        """Come ``AutomationEntity.async_trigger`` (senza traccia e senza l'evento
        ``automation_triggered``)."""
        motivo = ""
        alias = ""
        if "trigger" in run_variables:
            if "description" in run_variables["trigger"]:
                motivo = f" by {run_variables['trigger']['description']}"
            if "alias" in run_variables["trigger"]:
                alias = f" trigger '{run_variables['trigger']['alias']}'"
        self.logger.debug("Automation%s triggered%s", alias, motivo)

        # un contesto nuovo, figlio di quello del trigger
        genitore = None if context is None else context.id
        contesto = Context(parent_id=genitore)

        variabili: dict[str, Any] = {"this": self._this(), **(run_variables or {})}
        if self._variabili:
            try:
                variabili = self._variabili.async_render(self.hass, variabili)
            except TemplateError as err:
                self.logger.error("Error rendering variables: %s", err)
                return

        if not skip_condition and self._condizioni is not None:
            try:
                passano = self._condizioni.async_check(variables=variabili)
            except (probatio.Invalid, HomeAssistantError) as err:
                self.logger.error(
                    "Error while checking conditions of automation %s: %s",
                    self.entity_id,
                    err,
                )
                return
            except Exception:
                self.logger.exception(
                    "Unexpected error while checking conditions of automation %s",
                    self.entity_id,
                )
                return
            if not passano:
                self.logger.debug("Conditions not met, aborting automation")
                return

        # come Entity.async_set_context
        self._contesto = contesto
        self._contesto_quando = time.time()

        # una pila nuova: un'automazione può far ripartire sé stessa
        script_stack_cv.set([])
        try:
            if self._scaricata:
                raise RuntimeError(
                    f"Cannot run script '{self.nome}' after it has been unloaded"
                )
            await self.sequenza.esegui(variabili, contesto)
        except ServiceNotFound as err:
            self.logger.error(
                "Error while executing automation %s: %s", self.entity_id, err
            )
        except (probatio.Invalid, HomeAssistantError) as err:
            self.logger.error(
                "Error while executing automation %s: %s", self.entity_id, err
            )
        except Exception:
            self.logger.exception(
                "Unexpected error while executing automation %s", self.entity_id
            )


@callback
def _niente() -> None:
    """Nessun trigger da staccare."""
