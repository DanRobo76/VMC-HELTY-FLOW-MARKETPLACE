"""Entità native dei sensori: mostrano in Home Assistant i valori di StatoVMC.

Stessi entity_id, unique_id, nomi, icone, unità e classi dei sensori del package (tabelle.py):
così la cronologia dei sensori resta la stessa. I valori li calcola StatoVMC; l'entità
scrive il suo stato quando StatoVMC le dice che la sua chiave è cambiata, con il contesto
della scrittura che l'ha cambiata (come il template di oggi, che prende il contesto
dell'evento che lo fa ricalcolare).

I sensori delle letture (tcp, ping e versione di oggi) sono invece la lettura del loro
coordinatore (``SensoreLetturaVMC``): si scrivono a ogni lettura, anche uguale (come
l'aggiornamento del sensore di oggi, che scrive sempre), e ``homeassistant.update_entity``
rilegge la VMC prima di scrivere; StatoVMC segue il loro stato (vmc.py).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .letture import LetturaPing
from .memoria import IN_ORDINE
from .stato import NON_DISPONIBILE, SCONOSCIUTO, Cambi, StatoVMC
from .tabelle import SENSORI


def nome_visibile(testo: str, nome: str) -> str:
    """Nome con il nome della VMC: {nome} così com'è, {Nome}/{NOME} Master/MASTER per la Master."""
    maiuscolo = "Master" if nome == "master" else nome
    return (
        testo.replace("{Nome}", maiuscolo)
        .replace("{NOME}", maiuscolo.upper() if nome == "master" else nome)
        .replace("{nome}", nome)
    )


class EntitaVMC(Entity):
    """Parte comune: identità dalla tabella, stato e icona da StatoVMC."""

    _attr_should_poll = False

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Entità per la chiave (es. «sensor.co2_status») della VMC di ``stato``."""
        voce = SENSORI[chiave]
        oggetto = chiave.split(".", 1)[1]
        self._stato = stato
        self._chiave = chiave
        self._icona_calcolata = "icona" in voce and voce["icona"] is None
        self.entity_id = stato.entity_id(chiave)
        self._attr_unique_id = f"vmc_{stato.nome}_{oggetto}"
        self._attr_name = nome_visibile(voce["nome"], stato.nome)
        if not self._icona_calcolata:
            self._attr_icon = voce.get("icona")

    @property
    def chiave(self) -> str:
        """Chiave del sensore in StatoVMC."""
        return self._chiave

    async def async_added_to_hass(self) -> None:
        """Segue i cambi della sua chiave."""
        await super().async_added_to_hass()
        self.async_on_remove(self._stato.ascolta(self._cambi))

    @callback
    def _cambi(self, cambi: Cambi) -> None:
        if self._chiave in cambi:
            if (contesto := self._stato.contesto_cambi) is not None:
                self.async_set_context(contesto)
            self.async_write_ha_state()

    def _valore(self) -> str | None:
        valore = self._stato.stato(self._chiave)
        return None if valore in (None, SCONOSCIUTO) else valore

    @property
    def available(self) -> bool:
        """Non disponibile come il sensore di oggi (lettura fallita, template in errore)."""
        return self._stato.stato(self._chiave) != NON_DISPONIBILE

    @property
    def icon(self) -> str | None:
        """Icona fissa, o calcolata dal modello."""
        if self._icona_calcolata:
            return self._stato.icona(self._chiave)
        return self._attr_icon

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Attributi del sensore di oggi (solo l'ultima lettura dello stato ventola ne ha)."""
        voce = self._stato.voce(self._chiave)
        if voce is None or not voce.attributi:
            return None
        return dict(voce.attributi)


class SensoreVMC(EntitaVMC, SensorEntity):
    """Sensore (template, lettura tcp, ping o versione di oggi)."""

    def __init__(self, stato: StatoVMC, chiave: str) -> None:
        """Sensore con unità e classi del package."""
        super().__init__(stato, chiave)
        voce = SENSORI[chiave]
        self._attr_native_unit_of_measurement = voce.get("unita")
        if "classe" in voce:
            self._attr_device_class = SensorDeviceClass(voce["classe"])
        if "classe_stato" in voce:
            self._attr_state_class = SensorStateClass(voce["classe_stato"])

    @property
    def native_value(self) -> str | None:
        """Lo stato come lo mostrava il sensore di oggi (None = unknown)."""
        return self._valore()


class SensoreMemoriaVMC(SensoreVMC, RestoreEntity):
    """Sensore con memoria: Home Assistant ne conserva l'ultimo stato tra un riavvio e l'altro.

    Lo stato conservato lo rilegge StatoVMC all'avvio (come i sensori a trigger di oggi).
    """


class SensoreLetturaVMC(SensoreVMC):
    """Sensore di una lettura (tcp, ping o versione di oggi): il dato del suo coordinatore."""

    def __init__(
        self, stato: StatoVMC, chiave: str, lettura: DataUpdateCoordinator[str]
    ) -> None:
        """Sensore della chiave ``chiave`` con la lettura ``lettura``."""
        super().__init__(stato, chiave)
        self._lettura = lettura
        self._in_aggiornamento = False

    async def async_added_to_hass(self) -> None:
        """Segue la sua lettura (non StatoVMC: è StatoVMC che segue lui)."""
        await Entity.async_added_to_hass(self)
        self.async_on_remove(self._lettura.async_add_listener(self._letta))

    @callback
    def _letta(self) -> None:
        # durante update_entity scrive Home Assistant, una volta, dopo la lettura
        if not self._in_aggiornamento:
            self.async_write_ha_state()

    async def async_update(self) -> None:
        """``homeassistant.update_entity``: come l'aggiornamento del sensore di oggi. Il
        ping (command_line) ha il suo (``LetturaPing.aggiorna_per_entita``: la lettura
        scrive, poi scrive Home Assistant); tcp e rest leggono, poi scrive solo Home
        Assistant, una volta."""
        if isinstance(self._lettura, LetturaPing):
            await self._lettura.aggiorna_per_entita()
            return
        self._in_aggiornamento = True
        try:
            await self._lettura.async_refresh()
        finally:
            self._in_aggiornamento = False

    def _valore(self) -> str | None:
        return self._lettura.data

    @property
    def available(self) -> bool:
        """Non disponibile se la lettura non è riuscita (VMC che non risponde)."""
        return self._lettura.last_update_success


class SensoreBinarioVMC(EntitaVMC, BinarySensorEntity):
    """Sensore binario (template di oggi): on/off dal modello."""

    @property
    def is_on(self) -> bool | None:
        """on/off; None (unknown) per ogni altro valore."""
        valore = self._valore()
        if valore == "on":
            return True
        if valore == "off":
            return False
        return None


def crea_entita(
    stato: StatoVMC, letture: Mapping[str, DataUpdateCoordinator[str]] | None = None
) -> tuple[list[SensoreVMC], list[SensoreBinarioVMC]]:
    """Le 136 entità sensore della VMC: (sensori, sensori binari).

    ``letture`` (chiave -> coordinatore, ``VMCNativa.letture_dei_sensori``): i sensori
    delle letture; senza, anche loro sono viste su StatoVMC.
    """
    letture = letture or {}
    sensori: list[SensoreVMC] = []
    binari: list[SensoreBinarioVMC] = []
    con_memoria: dict[str, SensoreMemoriaVMC] = {}
    for chiave, voce in SENSORI.items():
        if chiave.startswith("binary_sensor."):
            binari.append(SensoreBinarioVMC(stato, chiave))
        elif chiave in letture:
            sensori.append(SensoreLetturaVMC(stato, chiave, letture[chiave]))
        elif voce["tipo"] == "memoria":
            con_memoria[chiave] = SensoreMemoriaVMC(stato, chiave)
        else:
            sensori.append(SensoreVMC(stato, chiave))
    # i sensori con memoria per primi e nell'ordine del Package: quando scrivono insieme
    # (StatoVMC li avvisa nell'ordine in cui si sono aggiunti) scrivono come i sensori a
    # trigger di oggi, prima dei sensori che li leggono
    sensori[:0] = [con_memoria[chiave] for chiave in IN_ORDINE]
    return sensori, binari
