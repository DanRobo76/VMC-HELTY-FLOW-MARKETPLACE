"""Il banco della memoria interna (fase 4): Home Assistant con gli aiutanti, il motore
con la memoria interna.

Le due corse si confrontano evento per evento, tranne quelli che con la memoria non ci
sono più perché i 67 valori non sono entità:

- ``state_changed`` di un valore interno: si confronta con il cambio della memoria
  (``MemoriaInterna.ascolta_cambi``: stesso istante, stessi stati, stesso contesto,
  stesso posto tra gli altri eventi);
- ``call_service`` di un servizio degli aiutanti con soli valori interni come
  bersaglio: si confronta con la chiamata alla memoria
  (``MemoriaInterna.ascolta_chiamate``);
- ``call_service`` di ``homeassistant.update_entity``: i valori interni non sono più
  tra le entità da aggiornare (il motore li toglie, ``contesto._senza_interni``).

Qui ci sono anche le parti del banco che domani saranno dell'integrazione:

- ``servizi_misti``: i servizi di ``input_boolean`` con le entità di Home Assistant e il
  valore interno insieme (il package spegne la spia interna insieme ad altre spie),
  come li registra Home Assistant (``entity_service_call`` su tutte, nell'ordine del
  package);
- ``modelli_entita_con_memoria``: i sensori modello del package che leggono valori
  interni (domani sensori nativi sullo ``StatoVMC``) li leggono dalla memoria.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable, Mapping
from functools import partial
from typing import Any

import jinja2
from homeassistant.const import (
    EVENT_CALL_SERVICE,
    EVENT_STATE_CHANGED,
    EVENT_STATE_REPORTED,
)
from homeassistant.core import Event, HassJobType, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_component import DATA_INSTANCES
from homeassistant.helpers.service import entity_service_call
from homeassistant.helpers.template import TemplateEnvironment
from homeassistant.util import dt as dt_util

from custom_components.vmc_master.nativa.motore.memoria_interna import (
    INTERNI,
    MemoriaInterna,
    da_stato,
)

ALTRI_BERSAGLI = ("device_id", "area_id", "floor_id", "label_id")
AGGIORNA = ("homeassistant", "update_entity")
DOMINI_INTERNI = ("input_boolean", "input_number", "input_text")
# Gli entity_id di oggi dei valori interni della Master (nell'ordine di INTERNI).
IDS_INTERNI = tuple(
    f"{dominio}.vmc_master_{oggetto}"
    for dominio, _, oggetto in (chiave.partition(".") for chiave in INTERNI)
)


def salvati_da_stati(stati: Iterable[Any]) -> dict[str, Any]:
    """I valori interni da salvare (per chiave) dagli stati degli aiutanti di oggi."""
    per_entita = dict(zip(IDS_INTERNI, INTERNI, strict=True))
    return {
        per_entita[s.entity_id]: da_stato(per_entita[s.entity_id], s.state)
        for s in stati
        if s.entity_id in per_entita
    }


def entita_scritte(valore: Any) -> list[str] | None:
    """Gli entity_id di un ``entity_id`` dei dati di un servizio (come
    ``cv.comp_entity_ids``), None se non è un elenco di entità."""
    try:
        elenco = cv.comp_entity_ids(valore)
    except Exception:  # noqa: BLE001 - dati non validi: il servizio li rifiuta
        return None
    return elenco if isinstance(elenco, list) else None


def chiamata_interna(dati: Mapping[str, Any], interni: Iterable[str]) -> bool:
    """Se un ``call_service`` è di un servizio degli aiutanti con soli valori interni
    come bersaglio (domani una chiamata alla memoria interna)."""
    if not MemoriaInterna.gestisce(dati["domain"], dati["service"]):
        return False
    servizio = dati.get("service_data") or {}
    entita = entita_scritte(servizio.get("entity_id"))
    if not entita or any(servizio.get(altro) for altro in ALTRI_BERSAGLI):
        return False
    insieme = set(interni)
    return all(e in insieme for e in entita)


def senza_interni(dati: dict[str, Any], interni: Iterable[str]) -> dict[str, Any]:
    """I dati di un ``call_service`` di ``homeassistant.update_entity`` come li manda il
    motore con la memoria: senza i valori interni tra le entità."""
    if (dati["domain"], dati["service"]) != AGGIORNA:
        return dati
    servizio = dati.get("service_data") or {}
    entita = entita_scritte(servizio.get("entity_id"))
    insieme = set(interni)
    if not entita or not any(e in insieme for e in entita):
        return dati
    return {
        **dati,
        "service_data": {
            **servizio,
            "entity_id": [e for e in entita if e not in insieme],
        },
    }


class Smistatore:
    """Gli eventi di una corsa divisi come si confrontano: ``registro`` (tutti gli
    altri), ``interni_cambi`` (cambi dei valori interni), ``chiamate_interne``,
    ``interni_rapporti`` (``state_reported`` dei valori interni) e ``sequenza`` (tutte
    le voci nell'ordine di arrivo: il posto dei cambi interni tra gli altri eventi).

    Con Home Assistant ``evento`` divide gli eventi degli aiutanti interni, con la
    memoria ``cambio`` e ``chiamata`` annotano gli annunci della memoria nello stesso
    formato; ``rapporto`` riceve i ``state_reported`` dei valori interni (degli
    aiutanti o della memoria, che li manda come Home Assistant); ``nota`` annota una
    voce del banco."""

    def __init__(
        self,
        interni: Iterable[str],
        norma: Callable[[Any], Any],
        conta: Callable[[Any], None] | None = None,
    ) -> None:
        self.interni = set(interni)
        self.norma = norma
        self.conta = conta
        self.registro: list[Any] = []
        self.interni_cambi: list[Any] = []
        self.chiamate_interne: list[Any] = []
        self.interni_rapporti: list[Any] = []
        self.sequenza: list[Any] = []
        # i state_reported degli aiutanti interni per homeassistant.update_entity (anche
        # in ``interni_rapporti``): la memoria li manda uguali, ma non da
        # ``async_update_entity`` (il motore toglie i valori interni dalla chiamata e li
        # riscrive lui)
        self.rapporti_da_aggiornamento: list[Any] = []
        self.aggiornando: set[str] = set()
        # call_service di homeassistant.update_entity con valori interni (tolti)
        self.update_senza_interni = 0

    def _voce(self, istante: Any, tipo: str, dati: Any, contesto: Any) -> Any:
        return (self.norma(istante), tipo, self.norma(dati), self.norma(contesto))

    def _aggiungi(self, elenco: list[Any], voce: Any) -> None:
        elenco.append(voce)
        self.sequenza.append(voce)

    def nota(self, voce: Any) -> None:
        """Una voce del banco (avvio, errore di un passo...)."""
        self._aggiungi(self.registro, voce)

    def ascolta_rapporti(self, hass: HomeAssistant) -> Callable[[], None]:
        """Ascolta i ``state_reported`` dei valori interni."""
        return hass.bus.async_listen(
            EVENT_STATE_REPORTED,
            self.rapporto,
            event_filter=callback(lambda dati: dati["entity_id"] in self.interni),
        )

    @callback
    def rapporto(self, evento: Event) -> None:
        """Un ``state_reported`` di un valore interno."""
        dati = {
            "entity_id": evento.data["entity_id"],
            "last_reported": evento.data["last_reported"],
        }
        if dati["entity_id"] in self.aggiornando:
            self.rapporti_da_aggiornamento.append(
                (self.norma(evento.time_fired), "rapporto", self.norma(dati))
            )
        self._aggiungi(
            self.interni_rapporti,
            self._voce(evento.time_fired, "rapporto", dati, evento.context),
        )

    def segna_aggiornamenti(
        self, aggiorna: Callable[[HomeAssistant, str], Awaitable[None]]
    ) -> Callable[[HomeAssistant, str], Awaitable[None]]:
        """``async_update_entity`` che segna i valori interni mentre si aggiornano: i
        loro ``state_reported`` vanno anche in ``rapporti_da_aggiornamento``."""

        async def segnato(hass: HomeAssistant, entity_id: str) -> None:
            if entity_id not in self.interni:
                await aggiorna(hass, entity_id)
                return
            self.aggiornando.add(entity_id)
            try:
                await aggiorna(hass, entity_id)
            finally:
                self.aggiornando.discard(entity_id)

        return segnato

    def evento(self, evento: Event) -> None:
        """Un evento del bus (ascoltatore di tutti gli eventi)."""
        if self.conta is not None:
            self.conta(evento.time_fired)
        dati = dict(evento.data)
        if evento.event_type == EVENT_STATE_CHANGED:
            dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            if dati["entity_id"] in self.interni:
                self._aggiungi(
                    self.interni_cambi,
                    self._voce(evento.time_fired, "cambio", dati, evento.context),
                )
                return
        elif evento.event_type == EVENT_CALL_SERVICE:
            if chiamata_interna(dati, self.interni):
                self._aggiungi(
                    self.chiamate_interne,
                    self._voce(evento.time_fired, "chiamata", dati, evento.context),
                )
                return
            if (ridotti := senza_interni(dati, self.interni)) is not dati:
                self.update_senza_interni += 1
                dati = ridotti
        self._aggiungi(
            self.registro,
            self._voce(evento.time_fired, evento.event_type, dati, evento.context),
        )

    def cambio(self, evento: Event) -> None:
        """Un cambio della memoria interna."""
        if self.conta is not None:
            self.conta(evento.time_fired)
        dati = {
            "entity_id": evento.data["entity_id"],
            "new_state": evento.data["new_state"],
        }
        self._aggiungi(
            self.interni_cambi,
            self._voce(evento.time_fired, "cambio", dati, evento.context),
        )

    def chiamata(
        self,
        istante: float,
        dominio: str,
        servizio: str,
        dati: Mapping[str, Any],
        contesto: Any,
    ) -> None:
        """Una chiamata alla memoria interna."""
        quando = dt_util.utc_from_timestamp(istante)
        if self.conta is not None:
            self.conta(quando)
        voce = {"domain": dominio, "service": servizio, "service_data": dict(dati)}
        self._aggiungi(
            self.chiamate_interne, self._voce(quando, "chiamata", voce, contesto)
        )


def servizi_misti(
    hass: HomeAssistant, memoria: MemoriaInterna, ordine: Iterable[str]
) -> None:
    """``input_boolean.turn_on``/``turn_off``/``toggle`` come li registra Home
    Assistant (``entity_service_call``), sulle entità di Home Assistant e sul valore
    interno insieme, nell'ordine del package (``ordine``: gli entity_id degli
    ``input_boolean`` del package): stesso evento ``call_service``, stesso ordine dei
    bersagli, un compito per bersaglio."""
    componente = hass.data[DATA_INSTANCES]["input_boolean"]
    ordine = list(ordine)
    interni = memoria.valori_del_dominio("input_boolean")

    def entita() -> dict[str, Any]:
        vere = {e.entity_id: e for e in componente.entities}
        return {
            e: vere[e] if e in vere else interni[e]
            for e in ordine
            if e in vere or e in interni
        }

    for servizio, metodo in (
        ("turn_on", "async_turn_on"),
        ("turn_off", "async_turn_off"),
        ("toggle", "async_toggle"),
    ):
        hass.services.async_register(
            "input_boolean",
            servizio,
            partial(entity_service_call, hass, entita, metodo),
            cv.make_entity_service_schema(None),
            job_type=HassJobType.Coroutinefunction,
        )


def modelli_entita_con_memoria(
    hass: HomeAssistant, memoria: MemoriaInterna
) -> list[str]:
    """I modelli dei sensori ``template`` che citano un valore interno si rendono con
    il motore dei modelli di Home Assistant su ``memoria.hass_modelli`` (da chiamare
    prima dell'avvio, quando i sensori modello non hanno ancora reso nulla).
    Restituisce i sensori toccati."""
    ambiente = TemplateEnvironment(memoria.hass_modelli)
    oggetti = [e.split(".", 1)[1] for e in memoria.entity_ids]
    toccati = []
    for dominio in ("sensor", "binary_sensor"):
        if (componente := hass.data[DATA_INSTANCES].get(dominio)) is None:
            continue
        for entita in componente.entities:
            modelli = getattr(entita, "_template_attrs", None) or {}
            for modello in modelli:
                if not any(o in modello.template for o in oggetti):
                    continue
                assert modello._compiled is None, entita.entity_id
                modello.ensure_valid()
                modello._compiled = jinja2.Template.from_code(
                    ambiente, modello._compiled_code, ambiente.globals, None
                )
                if entita.entity_id not in toccati:
                    toccati.append(entita.entity_id)
    return toccati
