"""Prove della fase 3: gli script del motore come entità ``script`` di Home Assistant.

Il codice di ``generato/`` (fase 3: senza ``comandi``) chiama gli script del package come
servizi di Home Assistant (``script.turn_on``, ``script.<chiave>``) e i suoi modelli leggono
il loro stato (``script.<chiave>``). Il motore tiene sempre i suoi script al proprio interno
(``interni.ScriptInterni``, nessuna entità); per confrontare il codice di ``generato/`` con
Home Assistant queste prove gli passano ``script_come_entita``: ogni script del package
diventa un'entità ``script`` (la classe ``ScriptEntity`` di Home Assistant con la
``Sequenza`` del motore al posto di ``Script``), come facevano il motore e le sue entità
fino alla 9.0.0b45. Le automazioni restano logiche dell'integrazione.

Le prove possono usare le parti interne di Home Assistant; l'integrazione no.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Mapping
from typing import Any

import probatio
from homeassistant.components.script.config import ScriptConfig
from homeassistant.components.script.const import DOMAIN as DOMINIO_SCRIPT
from homeassistant.components.script.entity import ScriptEntity
from homeassistant.components.trace import TRACE_CONFIG_SCHEMA
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.typing import ConfigType
from homeassistant.setup import async_setup_component

from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.definizioni import Automazione, Script
from custom_components.vmc_master.nativa.motore.esecuzione import ComeScript, Sequenza
from custom_components.vmc_master.nativa.motore.ha import Motore, ScriptComeEntita


def _tracce() -> dict[str, Any]:
    """La configurazione predefinita delle tracce (``trace: {}`` validato)."""
    return probatio.Schema(TRACE_CONFIG_SCHEMA)({})


class ComeScriptEntita(ComeScript):
    """``ComeScript`` con ciò che ``ScriptEntity`` (e la ricerca di Home Assistant) legge
    o scrive di uno ``Script``, oltre a ciò che usa uno script interno."""

    def __init__(self, sequenza: Sequenza) -> None:
        super().__init__(sequenza)
        self.top_level = True
        # usati solo dalla ricerca di Home Assistant (entità citate)
        self.referenced_labels: set[str] = set()
        self.referenced_floors: set[str] = set()
        self.referenced_areas: set[str] = set()
        self.referenced_devices: set[str] = set()
        self.referenced_entities: set[str] = set()

    @property
    def last_triggered(self) -> Any:
        return self.sequenza.ultimo_avvio

    @last_triggered.setter
    def last_triggered(self, valore: Any) -> None:
        """``ScriptEntity.async_added_to_hass``: l'ultimo avvio ripreso dopo un riavvio."""
        self.sequenza.ultimo_avvio = valore

    def update_logger(self, logger: logging.Logger | None = None) -> None:
        """I messaggi del motore hanno il proprio registro."""


class ScriptMotore(ScriptEntity):
    """Uno script del package con il motore tradotto (come ScriptEntity)."""

    def __init__(self, definizione: Script, script: ComeScriptEntita) -> None:  # noqa: PLW0231
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


def _ricarica_come_yaml_invariato(component: EntityComponent[Any]) -> None:
    """script.reload rilegge la configurazione YAML e toglie le entità che non vi trova
    più, ma lascia come sono (esecuzioni in corso comprese) quelle il cui YAML non è
    cambiato. Gli script del motore non sono nel YAML: alla configurazione riletta
    (``async_prepare_reload``) si aggiunge una voce per ogni script del motore, così Home
    Assistant li tratta come YAML invariato. Vale per tutti i motori avviati."""
    if getattr(component, "_ricarica_motore", False):
        return
    originale = component.async_prepare_reload

    async def async_prepare_reload(*, skip_reset: bool = False) -> ConfigType:
        conf = dict(await originale(skip_reset=skip_reset))
        script = dict(conf.get(DOMINIO_SCRIPT) or {})
        for entita in component.entities:
            if isinstance(entita, ScriptMotore):
                script.setdefault(entita.unique_id, ScriptConfig())
        conf[DOMINIO_SCRIPT] = script
        return conf

    component.async_prepare_reload = async_prepare_reload  # type: ignore[method-assign]
    component._ricarica_motore = True  # type: ignore[attr-defined]


def script_come_entita(
    configurazione: Mapping[str, Any] | None = None,
) -> ScriptComeEntita:
    """``Motore.avvia(script_come_entita=...)``: come faceva il motore della fase 3 fino
    alla 9.0.0b45, avvia le integrazioni ``automation`` e ``script`` con la configurazione
    della prova (le altre automazioni e gli altri script dell'utente, se ci sono: come
    prima, agganciano i loro trigger prima delle logiche del motore) e aggiunge a
    ``script`` un'entità per ogni script del package."""

    async def crea(motore: Motore, script: list[tuple[Script, Sequenza]]) -> None:
        hass: HomeAssistant = motore.hass
        for dominio in ("automation", DOMINIO_SCRIPT):
            if not await async_setup_component(hass, dominio, dict(configurazione or {})):
                raise RuntimeError(f"{dominio} non si avvia")
        motore.script = [ScriptMotore(s, ComeScriptEntita(seq)) for s, seq in script]
        componente = hass.data[DOMINIO_SCRIPT]
        await componente.async_add_entities(motore.script)
        _ricarica_come_yaml_invariato(componente)

    return crea


class MotoreFase3(Motore):
    """Il motore con il codice di ``generato/`` (fase 3) e gli script come entità."""

    async def avvia(  # type: ignore[override]
        self,
        crea: Callable[[Contesto], tuple[list[Automazione], list[Script]]]
        | None = None,
        configurazione: Mapping[str, Any] | None = None,
        **argomenti: Any,
    ) -> None:
        """Come ``Motore.avvia``, con le entità degli script (``script_come_entita``)."""
        await super().avvia(
            crea, script_come_entita=script_come_entita(configurazione), **argomenti
        )
