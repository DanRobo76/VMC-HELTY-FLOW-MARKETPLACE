"""Il motore tradotto su Home Assistant (fase 3): automazioni e script come entità.

Ogni automazione del package diventa un'entità ``automation`` e ogni script un'entità
``script``, con lo stesso entity_id, gli stessi attributi e gli stessi servizi di quelle
che crea Home Assistant dal package: sono le classi di Home Assistant
(``AutomationEntity``, ``ScriptEntity``) con il motore tradotto al posto di ``Script`` e
delle condizioni. Così trigger, ``this``, ``automation.trigger``, ``script.turn_on``,
stato all'avvio e attributi seguono le regole di sempre.

In questa fase il resto del package (aiutanti, sensori template...) resta quello di oggi:
il simulatore confronta il motore tradotto con l'automazione del package.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Mapping
from functools import partial
from typing import Any

import probatio
from homeassistant.components.automation import AutomationEntity
from homeassistant.components.automation.config import AutomationConfig
from homeassistant.components.automation.const import DATA_COMPONENT as AUTOMAZIONI
from homeassistant.components.automation.const import DOMAIN as DOMINIO_AUTOMAZIONI
from homeassistant.components.automation.const import LOGGER as LOGGER_AUTOMAZIONI
from homeassistant.components.script.config import ScriptConfig
from homeassistant.components.script.const import DOMAIN as DOMINIO_SCRIPT
from homeassistant.components.script.entity import ScriptEntity
from homeassistant.components.trace import TRACE_CONFIG_SCHEMA
from homeassistant.const import CONF_ALIAS, CONF_ID, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Context, HomeAssistant
from homeassistant.exceptions import (
    ConditionError,
    ConditionErrorContainer,
    ConditionErrorIndex,
    TemplateError,
)
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.script import (
    DATA_SCRIPTS,
    _async_stop_scripts_at_shutdown,
)
from homeassistant.helpers.script_variables import ScriptVariables
from homeassistant.helpers.typing import ConfigType
from homeassistant.setup import async_setup_component

from .contesto import Contesto
from .definizioni import Automazione, Comando, Script
from .esecuzione import Modello, Sequenza
from .interni import ComandiVMC, Invia, ScriptInterni, ScriptInterno
from .memoria_interna import MemoriaInterna
from .timer import TimerDelMotore, ha_trigger_timer, inizializza_trigger


def _tracce() -> dict[str, Any]:
    """La configurazione predefinita delle tracce (``trace: {}`` validato)."""
    return probatio.Schema(TRACE_CONFIG_SCHEMA)({})


class ComeScript:
    """La parte di ``Script`` che usano AutomationEntity e ScriptEntity, sopra una
    ``Sequenza`` del motore.

    Come ogni ``Script`` di primo livello si iscrive nel registro degli script di Home
    Assistant (``DATA_SCRIPTS``): alla chiusura è Home Assistant stesso
    (``_async_stop_scripts_at_shutdown``) a fermare le esecuzioni in corso e, 60 secondi
    dopo, a vietarne di nuove, con le stesse regole e nello stesso ordine degli script
    YAML.
    """

    def __init__(self, sequenza: Sequenza) -> None:
        self.sequenza = sequenza
        self.name = sequenza.nome
        self.top_level = True
        self._scaricato = False
        # come Script.__init__
        hass = sequenza.hass
        if (tutti := hass.data.get(DATA_SCRIPTS)) is None:
            tutti = hass.data[DATA_SCRIPTS] = {}
            hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_STOP,
                partial(_async_stop_scripts_at_shutdown, hass),
            )
        tutti[id(self)] = {
            "instance": self,  # type: ignore[typeddict-item]
            "started_before_shutdown": not hass.is_stopping,
        }
        # usati solo dalla ricerca di Home Assistant (entità citate)
        self.referenced_labels: set[str] = set()
        self.referenced_floors: set[str] = set()
        self.referenced_areas: set[str] = set()
        self.referenced_devices: set[str] = set()
        self.referenced_entities: set[str] = set()

    def _al_cambio(self, ascoltatore: Callable[[], None]) -> None:
        self.sequenza.al_cambio = ascoltatore

    # AutomationEntity.__init__ e ScriptMotore.__init__ lo scrivono, nessuno lo legge
    change_listener = property(fset=_al_cambio)

    @property
    def is_running(self) -> bool:
        return self.sequenza.in_corso

    @property
    def runs(self) -> int:
        return len(self.sequenza.esecuzioni)

    @property
    def script_mode(self) -> str:
        return self.sequenza.modo

    @property
    def max_runs(self) -> int:
        return self.sequenza.massimo

    @property
    def supports_max(self) -> bool:
        return self.sequenza.con_massimo

    @property
    def last_triggered(self) -> Any:
        return self.sequenza.ultimo_avvio

    @last_triggered.setter
    def last_triggered(self, valore: Any) -> None:
        self.sequenza.ultimo_avvio = valore

    @property
    def last_action(self) -> str | None:
        return self.sequenza.ultima_azione

    def update_logger(self, logger: logging.Logger | None = None) -> None:
        """I messaggi del motore hanno il proprio registro."""

    async def async_run(
        self,
        run_variables: Mapping[str, Any] | None = None,
        context: Context | None = None,
        started_action: Callable[..., Any] | None = None,
    ) -> None:
        """Come Script.async_run (nessuno script del package restituisce dati)."""
        if self._scaricato:
            raise RuntimeError(
                f"Cannot run script '{self.name}' after it has been unloaded"
            )
        await self.sequenza.esegui(run_variables, context, started_action)

    async def async_stop(self, update_state: bool = True, spare: Any = None) -> None:
        await self.sequenza.ferma(aggiorna=update_state)

    async def async_unload(self) -> None:
        """Come Script.async_unload: niente più esecuzioni, si fermano quelle in corso
        e lo script esce dal registro degli script.

        Lo chiama solo ``async_will_remove_from_hass`` dell'entità, una volta: un'entità
        si toglie una volta sola (``Entity.async_remove``) e quelle del motore non si
        riaggiungono (cambiano entity_id sul posto)."""
        self._scaricato = True
        await self.sequenza.ferma()
        del self.sequenza.hass.data[DATA_SCRIPTS][id(self)]


class CondizioniAutomazione:
    """Le condizioni di un'automazione (come ConditionsChecker): tutte vere; un errore
    si registra e vale falso."""

    # usato solo dalla ricerca di Home Assistant (entità citate)
    config: list[Any] = []  # noqa: RUF012

    def __init__(self, c: Contesto, condizioni: tuple[Any, ...], nome: str) -> None:
        self.c = c
        self.condizioni = condizioni
        self.nome = nome

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
            LOGGER_AUTOMAZIONI.warning(
                "Error evaluating condition in '%s':\n%s",
                self.nome,
                ConditionErrorContainer("condition", errors=errori),
            )
            return False
        return True

    def async_unload(self) -> None:
        """Niente da liberare."""


# La pagina di un'automazione (Impostazioni → Automazioni e scenari) chiede la sua
# configurazione a Home Assistant (``automation/config``, cioè ``raw_config``): con None la
# pagina non si apre mai e gira all'infinito. Le automazioni del motore non hanno YAML: la
# pagina mostra il nome e la descrizione, senza attivazioni, condizioni e azioni (sono nel
# codice dell'integrazione), in sola lettura come ogni automazione fuori da automations.yaml;
# con l'id il pulsante «Tracce» della pagina apre l'elenco delle esecuzioni.
NOTA_CONFIGURAZIONE = (
    "Automazione dell'integrazione VMC Master: attivazioni, condizioni e azioni sono nel "
    "codice dell'integrazione, perciò qui risultano vuote e non si modificano (Migra ne "
    "farebbe solo una copia vuota)."
)


def configurazione_mostrata(
    id_: str | None, alias: str, descrizione: str | None
) -> dict[str, Any]:
    """La configurazione che la pagina dell'automazione mostra (``raw_config``)."""
    testo = (
        f"{NOTA_CONFIGURAZIONE}\n\n{descrizione}"
        if descrizione
        else NOTA_CONFIGURAZIONE
    )
    mostrata: dict[str, Any] = {"id": id_} if id_ is not None else {}
    return {
        **mostrata,
        "alias": alias,
        "description": testo,
        "triggers": [],
        "conditions": [],
        "actions": [],
    }


class AutomazioneMotore(AutomationEntity):
    """Un'automazione del package con il motore tradotto."""

    # fase 4: i comandi di shell del motore, che agganciano i trigger delle chiamate dei
    # comandi (``AGGANCIO``); None: tutti i trigger sono di Home Assistant
    comandi: ComandiVMC | None = None

    async def _async_attach_triggers(self) -> Callable[[], None] | None:
        """Come AutomationEntity, più i trigger delle chiamate dei comandi agganciati a
        ``ComandiVMC``: prima degli altri, come Home Assistant aggancia al bus i trigger
        ``event`` prima di aspettare gli altri trigger."""
        if self.comandi is None:
            return await self._aggancia_trigger()
        comandi = self.comandi.aggancia_trigger(
            self._trigger_config, self._async_trigger_if_enabled, str(self.name)
        )
        try:
            altri = await self._aggancia_trigger()
        except BaseException:
            if comandi is not None:
                comandi()
            raise
        if comandi is None or altri is None:
            return comandi or altri

        def stacca() -> None:
            comandi()
            altri()

        return stacca

    async def _aggancia_trigger(self) -> Callable[[], None] | None:
        """Come ``AutomationEntity._async_attach_triggers`` (le stesse righe), con
        ``timer.inizializza_trigger`` al posto di ``async_initialize_triggers`` se
        l'automazione ha trigger dei timer del motore (``timer.TRIGGER``)."""
        if not ha_trigger_timer(self._trigger_config):
            return await super()._async_attach_triggers()
        this = None
        if state := self.hass.states.get(self.entity_id):
            this = state.as_dict()
        variables = {"this": this}
        if self._trigger_variables:
            try:
                variables = self._trigger_variables.async_render(
                    self.hass,
                    variables,
                    limited=True,
                )
            except TemplateError as err:
                self._logger.error("Error rendering trigger variables: %s", err)
                return None

        return await inizializza_trigger(
            self.hass,
            self._trigger_config,
            self._async_trigger_if_enabled,
            DOMINIO_AUTOMAZIONI,
            str(self.name),
            self._log_callback,
            variables=variables,
            did_not_trigger=self._handle_not_triggered,
        )


class ScriptMotore(ScriptEntity):
    """Uno script del package con il motore tradotto (come ScriptEntity)."""

    def __init__(self, definizione: Script, script: ComeScript) -> None:  # noqa: PLW0231
        # come ScriptEntity.__init__, con il motore al posto di Script
        self.icon = definizione.icona
        self.description = definizione.descrizione or ""
        self.fields = dict(definizione.campi)
        self._attr_unique_id = definizione.chiave
        self.entity_id = f"{DOMINIO_SCRIPT}.{definizione.chiave}"
        self.script = script  # type: ignore[assignment]
        script.change_listener = self.async_change_listener
        self._changed = asyncio.Event()
        self.raw_config = None
        self._trace_config = _tracce()
        self._blueprint_inputs = None
        self._attr_name = script.name


def _voce_ricaricata(entita: Any) -> tuple[Any, Any] | None:
    """La voce della configurazione riletta che corrisponde a un'entità del motore
    (None per le altre entità): per un'automazione stesso id e stesso nome, per uno
    script stessa chiave; raw_config quello dell'entità (per un'automazione la
    configurazione mostrata dalla sua pagina, per uno script None)."""
    if isinstance(entita, AutomazioneMotore):
        voce = AutomationConfig({CONF_ALIAS: entita.name})
        voce.raw_config = entita.raw_config
        if entita.unique_id is not None:
            voce[CONF_ID] = entita.unique_id
        return None, voce
    if isinstance(entita, ScriptMotore):
        return entita.unique_id, ScriptConfig()
    return None


def _ricarica_come_yaml_invariato(
    component: EntityComponent[Any], dominio: str
) -> None:
    """automation.reload e script.reload rileggono la configurazione YAML e tolgono le
    entità che non vi trovano più, ma lasciano come sono (esecuzioni in corso comprese)
    quelle il cui YAML non è cambiato. Le automazioni e gli script del motore non sono
    nel YAML: alla configurazione riletta (``async_prepare_reload``, che entrambi i
    servizi chiamano) si aggiunge una voce per ogni entità del motore, così Home
    Assistant le tratta come YAML invariato. Vale per tutti i motori avviati (una VMC
    ciascuno)."""
    if getattr(component, "_ricarica_motore", False):
        return
    originale = component.async_prepare_reload

    async def async_prepare_reload(*, skip_reset: bool = False) -> ConfigType:
        conf = dict(await originale(skip_reset=skip_reset))
        voci = [v for e in component.entities if (v := _voce_ricaricata(e))]
        if dominio == DOMINIO_SCRIPT:
            script = dict(conf.get(dominio) or {})
            for chiave, voce in voci:
                script.setdefault(chiave, voce)
            conf[dominio] = script
        else:
            conf[dominio] = [*(conf.get(dominio) or []), *(v for _, v in voci)]
        return conf

    component.async_prepare_reload = async_prepare_reload  # type: ignore[method-assign]
    component._ricarica_motore = True  # type: ignore[attr-defined]


class Motore:
    """Il motore tradotto di una VMC su Home Assistant."""

    def __init__(
        self,
        hass: HomeAssistant,
        nome: str = "master",
        memoria: MemoriaInterna | None = None,
    ) -> None:
        """Il motore della VMC ``nome``; con ``memoria`` (fase 4) i valori interni sono
        nella memoria interna invece che negli aiutanti di oggi."""
        self.hass = hass
        self.c = Contesto(hass, nome)
        if memoria is not None:
            self.c.usa_memoria(memoria)
        self.sequenze: list[Sequenza] = []
        self.automazioni: list[AutomazioneMotore] = []
        self.script: list[ScriptMotore] = []

    def _come_template(self, valore: Any) -> Any:
        """Le variabili di un'automazione le rende Home Assistant: Template al posto di
        ``Modello``."""
        if isinstance(valore, Modello):
            return self.c.modello(valore.funzione)
        if isinstance(valore, list):
            return [self._come_template(v) for v in valore]
        if isinstance(valore, Mapping):
            return {
                self._come_template(k): self._come_template(v)
                for k, v in valore.items()
            }
        return valore

    def _automazione(self, a: Automazione) -> AutomazioneMotore:
        sequenza = Sequenza(
            self.c,
            a.alias,
            a.corpo,
            a.modo,
            a.massimo,
            avviso_massimo=a.avviso_massimo,
            dominio="automation",
        )
        self.sequenze.append(sequenza)
        condizioni = (
            CondizioniAutomazione(self.c, tuple(a.condizioni), a.alias)
            if a.condizioni is not None
            else None
        )
        variabili = (
            ScriptVariables(self._come_template(dict(a.variabili)))
            if a.variabili
            else None
        )
        return AutomazioneMotore(
            a.id,
            a.alias,
            list(a.trigger),
            condizioni,  # type: ignore[arg-type]
            ComeScript(sequenza),  # type: ignore[arg-type]
            a.stato_iniziale,
            variabili,
            None,
            configurazione_mostrata(a.id, a.alias, a.descrizione),
            None,
            _tracce(),
        )

    def _script(self, s: Script) -> ScriptMotore:
        sequenza = Sequenza(
            self.c,
            s.alias or s.chiave,
            s.corpo,
            s.modo,
            s.massimo,
            avviso_massimo=s.avviso_massimo,
            variabili=s.variabili,
            dominio=DOMINIO_SCRIPT,
        )
        self.sequenze.append(sequenza)
        return ScriptMotore(s, ComeScript(sequenza))

    def _script_interno(self, s: Script) -> ScriptInterno:
        """Fase 4: uno script del package dentro il motore, senza entità."""
        sequenza = Sequenza(
            self.c,
            s.alias or s.chiave,
            s.corpo,
            s.modo,
            s.massimo,
            avviso_massimo=s.avviso_massimo,
            variabili=s.variabili,
            dominio=DOMINIO_SCRIPT,
        )
        self.sequenze.append(sequenza)
        return ScriptInterno(s.chiave, ComeScript(sequenza))

    async def avvia(
        self,
        crea: Callable[[Contesto], tuple[list[Automazione], list[Script]]]
        | None = None,
        configurazione: Mapping[str, Any] | None = None,
        *,
        comandi: Callable[[Contesto], list[Comando]] | None = None,
        invia: Invia | None = None,
        timer: Mapping[str, Mapping[str, Any] | None] | None = None,
    ) -> None:
        """Crea le entità delle automazioni e degli script nei loro domini (``crea``:
        quelle del package, o altre per le prove).

        Con ``comandi`` (fase 4: la funzione ``comandi`` del codice tradotto con gli
        script interni) gli script restano dentro il motore (``ScriptInterni``, nessuna
        entità ``script``) e i comandi di shell sono comandi del motore
        (``ComandiVMC``): vanno alla VMC con ``invia`` (il client TCP).

        ``timer`` (fase 4): la configurazione dei timer del motore (come la chiave
        ``timer:`` del package), per il codice tradotto con ``timer_motore``; senza, il
        motore non ha timer (il codice di ``generato/`` usa i timer di Home Assistant).
        """
        if crea is None:
            from .generato.motore import crea

        hass = self.hass
        if timer is not None:
            self.c.timer = TimerDelMotore(self.c, timer)
            await self.c.timer.prepara()
        automazioni, script = crea(self.c)
        interni = comandi is not None
        # le integrazioni automation e script con la configurazione di Home Assistant (se non
        # sono già avviate): le altre automazioni e gli altri script restano quelli di sempre
        domini = ("automation",) if interni else ("automation", DOMINIO_SCRIPT)
        for dominio in domini:
            if not await async_setup_component(
                hass, dominio, dict(configurazione or {})
            ):
                raise RuntimeError(f"{dominio} non si avvia")
        if comandi is not None:
            self.c.interni = ScriptInterni()
            for s in script:
                self.c.interni.aggiungi(self._script_interno(s))
            self.c.comandi = ComandiVMC(self.c, comandi(self.c), invia=invia)
        else:
            self.script = [self._script(s) for s in script]
        self.automazioni = [self._automazione(a) for a in automazioni]
        for automazione in self.automazioni:
            automazione.comandi = self.c.comandi
        if not interni:
            await hass.data[DOMINIO_SCRIPT].async_add_entities(self.script)
        await hass.data[AUTOMAZIONI].async_add_entities(self.automazioni)
        if not interni:
            _ricarica_come_yaml_invariato(hass.data[DOMINIO_SCRIPT], DOMINIO_SCRIPT)
        _ricarica_come_yaml_invariato(hass.data[AUTOMAZIONI], DOMINIO_AUTOMAZIONI)

    async def scarica_interni(self) -> None:
        """Fase 4: gli script del motore si fermano e non ripartono più (come le entità
        ``script`` tolte). Gli agganci dei comandi li staccano le automazioni quando si
        tolgono, come i loro altri trigger."""
        if self.c.interni is not None:
            await self.c.interni.scarica()
