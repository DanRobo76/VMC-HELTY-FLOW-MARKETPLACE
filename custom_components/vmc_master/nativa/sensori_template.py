"""I sensori template del package come entità dell'integrazione, con i modelli tradotti.

Oggi i 120 sensori calcolati della VMC sono sensori template senza trigger:
Home Assistant ricalcola ognuno quando cambia un'entità che il suo modello ha letto
l'ultima volta (``async_track_template_result``) e lo scrive subito, durante la consegna
dell'evento che l'ha fatto ricalcolare; un sensore che legge un altro sensore si
ricalcola alla consegna del cambio di quello. Chi segue questi sensori (trigger
``template`` e ``state`` delle automazioni, attese) vede quindi i cambi uno alla volta,
in quest'ordine, con gli stati intermedi.

``StatoVMC`` ricalcola invece tutti i modelli insieme e scrive tutti i cambi in fila: stessi
valori finali, ma un altro ordine e nessuno stato intermedio, e le automazioni possono
scattare in modo diverso (per esempio due trigger dell'Automazione VMC Master al posto di
uno, e un comando in più alla VMC). Per avere gli stessi istanti e lo stesso ordine questi
120 sensori sono entità dell'integrazione che si comportano come le entità template di
Home Assistant (``SensoreModello``, ``BinarioModello``: sensori_modello.py), con la
configurazione del package e i modelli tradotti in Python dal traduttore del motore
(``ModelloHA``, che legge le entità di domani e i valori interni come il motore) al posto
dei Template Jinja: ``motore/generato_fase4/sensori.py``. I modelli si seguono con
``segui`` (la firma di ``async_track_template_result``): di norma
``motore.seguire.traccia_modelli``, che segue anche i valori interni (memoria interna,
timer del motore) letti dai modelli.

Il sensore che legge due timer del motore (Velocità Registrata) li segue come il template
di oggi segue i timer: le letture dei timer del motore si annotano nel ``RenderInfo`` e
``AnnunciDeiTimer`` consegna i cambi dei timer a chi li segue (``CambiInterni``), nel punto
del bus in cui Home Assistant consegnerebbe il loro ``state_changed``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from types import ModuleType
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import (
    CALLBACK_TYPE,
    Event,
    EventOrigin,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.helpers.entity import Entity

from .motore.contesto import Contesto
from .motore.seguire import cambi_interni, traccia_modelli
from .motore.timer import TimerDelMotore, TimerMotore
from .sensori_modello import BinarioModello, Seguire, SensoreModello

_MARCHIO = "vmc_master_annuncio_timer"

SensoriTemplate = tuple[list[SensoreModello], list[BinarioModello]]


def chiave_del_sensore(entity_id: str, nome: str) -> str:
    """La chiave di StatoVMC di un sensore («sensor.vmc_<nome>_x» -> «sensor.x»)."""
    dominio, _, oggetto = entity_id.partition(".")
    return f"{dominio}.{oggetto.removeprefix(f'vmc_{nome}_')}"


def crea_sensori_template(
    hass: HomeAssistant,
    c: Contesto,
    codice: ModuleType,
    ip: str,
    *,
    segui: Seguire = traccia_modelli,
) -> SensoriTemplate:
    """Le entità dei sensori template (sensori, sensori binari) nell'ordine del package,
    dal codice tradotto ``codice`` (``generato_fase4.sensori``) per la VMC di ``c``
    all'indirizzo ``ip`` (il sensore «IP configurato»; oggi l'integrazione lo scrive
    nel package); ``segui`` è come seguono i loro modelli."""
    sensori: list[SensoreModello] = []
    binari: list[BinarioModello] = []
    for entita in in_ordine(hass, c, codice, ip, segui=segui):
        if isinstance(entita, SensoreModello):
            sensori.append(entita)
        else:
            binari.append(entita)
    return sensori, binari


def in_ordine(
    hass: HomeAssistant,
    c: Contesto,
    codice: ModuleType,
    ip: str,
    *,
    segui: Seguire = traccia_modelli,
) -> list[SensoreModello | BinarioModello]:
    """Le entità dei sensori template nell'ordine del package, sensori e sensori binari
    insieme: l'ordine in cui oggi l'integrazione template le aggiunge e in cui, all'avvio,
    ognuna comincia a seguire le entità che legge (chi segue prima un'entità si ricalcola
    prima ai suoi cambi). ``segui`` è come seguono i loro modelli (la firma di
    ``async_track_template_result``)."""
    uscita: list[SensoreModello | BinarioModello] = []
    for dominio, config in codice.sensori(c, ip):
        if dominio == "sensor":
            classe: type[SensoreModello | BinarioModello] = SensoreModello
        elif dominio == "binary_sensor":
            classe = BinarioModello
        else:
            raise ValueError(f"dominio di un sensore template non gestito: {dominio}")
        uscita.append(classe(hass, config, config.get("unique_id"), segui=segui))
    return uscita


def a_gruppi(entita: Sequence[Entity]) -> list[tuple[str, list[Any]]]:
    """Le entità in ordine, a gruppi consecutivi dello stesso dominio («sensor»,
    «binary_sensor»): per aggiungerle a Home Assistant senza cambiare l'ordine."""
    gruppi: list[tuple[str, list[Any]]] = []
    for una in entita:
        dominio = "sensor" if isinstance(una, SensorEntity) else "binary_sensor"
        if not gruppi or gruppi[-1][0] != dominio:
            gruppi.append((dominio, []))
        gruppi[-1][1].append(una)
    return gruppi


class AnnunciDeiTimer:
    """I cambi dei timer del motore a chi li segue come entità.

    Un timer del motore non è nella macchina degli stati: con il package ogni sua
    scrittura era un ``state_changed`` che Home Assistant consegnava a chi segue il timer
    (il sensore template che lo legge, i modelli del motore). Qui ogni scrittura si
    annuncia sul canale del motore (``CambiInterni.manda``: subito, o dopo l'annuncio che
    si sta consegnando); alla consegna il cambio va prima agli ``osservatori`` (per
    esempio la traccia del simulatore) e poi a chi segue il timer (``CambiInterni``).
    Come la memoria interna per i valori interni.
    """

    def __init__(self, hass: HomeAssistant, timer: TimerDelMotore) -> None:
        self.hass = hass
        self._vecchi: dict[str, State | None] = {
            entity_id: t.stato_ha for entity_id, t in timer.timer.items()
        }
        self._osservatori: list[Callable[[Event[Any]], None]] = []
        self._attivo = True
        self._annulla: list[CALLBACK_TYPE] = [timer.ascolta(self._scritto)]

    @callback
    def osserva(self, funzione: Callable[[Event[Any]], None]) -> CALLBACK_TYPE:
        """``funzione(evento state_changed)`` a ogni cambio, prima di chi segue il timer;
        restituisce come smettere."""
        self._osservatori.append(funzione)

        @callback
        def smetti() -> None:
            self._osservatori.remove(funzione)

        return smetti

    @callback
    def ferma(self) -> None:
        self._attivo = False
        for annulla in self._annulla:
            annulla()
        self._annulla.clear()

    @callback
    def _scritto(self, timer: TimerMotore) -> None:
        nuovo = timer.stato_ha
        assert nuovo is not None
        vecchio = self._vecchi.get(timer.entity_id)
        self._vecchi[timer.entity_id] = nuovo
        cambi_interni(self.hass).manda(
            self._consegna,
            {_MARCHIO: (timer.entity_id, vecchio, nuovo)},
            nuovo.context,
        )

    @callback
    def _consegna(self, evento: Event[Any]) -> None:
        if not self._attivo:
            return
        entity_id, vecchio, nuovo = evento.data[_MARCHIO]
        cambio: Event[Any] = Event(
            EVENT_STATE_CHANGED,
            {"entity_id": entity_id, "old_state": vecchio, "new_state": nuovo},
            EventOrigin.local,
            evento.time_fired_timestamp,
            evento.context,
        )
        for funzione in list(self._osservatori):
            funzione(cambio)
        cambi_interni(self.hass).consegna(cambio)
