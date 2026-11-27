"""I sensori con memoria nativi contro i template a trigger di oggi: stessi istanti.

Oggi le tre «ultima lettura valida» e le medie sono blocchi template a trigger. Home
Assistant aggancia i loro trigger all'avvio (EVENT_HOMEASSISTANT_START); il trigger
``homeassistant: start`` scatta quando l'avvio è finito (EVENT_HOMEASSISTANT_STARTED);
a ogni trigger il blocco scrive i suoi sensori, anche senza cambio (``state_reported``);
le medie chiamano prima ``recorder.get_statistics``. Domani sono i sensori con memoria
di VMCNativa (vmc.py, entita.py).

Nello stesso Home Assistant i blocchi di oggi (con entity_id ``sensor.oggi_*``) seguono i
sensori delle letture native, così i due lati vedono le stesse letture: in ogni fase
(setup, avvio, avvio finito, letture, minuto 5) devono scrivere gli stessi sensori, nello
stesso ordine, con gli stessi stati, e chiamare recorder.get_statistics con gli stessi dati
(un servizio finto qui, come quello del simulatore).
"""

from __future__ import annotations

import copy
import re
from datetime import timedelta
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import (
    EVENT_CALL_SERVICE,
    EVENT_HOMEASSISTANT_START,
    EVENT_HOMEASSISTANT_STARTED,
    EVENT_STATE_CHANGED,
    EVENT_STATE_REPORTED,
)
from homeassistant.core import (
    CoreState,
    Event,
    HomeAssistant,
    ServiceCall,
    SupportsResponse,
    callback,
)
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    async_fire_time_changed,
)

from custom_components.vmc_master.nativa.client import ErroreVMC
from custom_components.vmc_master.nativa.entita import crea_entita
from custom_components.vmc_master.nativa.memoria import GIORNI_DATI, MEDIE
from custom_components.vmc_master.nativa.vmc import MEMORIZZATE, VMCNativa

from .confronto import package
from .test_client import VMGH, VMGI

MEMORIA = [*MEMORIZZATE.values(), *(chiave for chiave, _, _ in MEDIE), GIORNI_DATI]
LETTE = re.compile(r"sensor\.vmc_master_(status_ventola|sensori|nome)\b")


class _Client:
    """Il client TCP finto del lato nativo: risponde, o non risponde se spenta."""

    host = "192.168.1.50"

    def __init__(self) -> None:
        self.accesa = True
        self.risposte = {"VMGH?": VMGH, "VMGI?": VMGI, "VMNM?": "VMNM Master"}

    async def interroga(self, richiesta: str) -> str:
        if not self.accesa:
            raise ErroreVMC("VMC finta spenta")
        return self.risposte.get(richiesta, "Rete")

    async def comanda(self, comando: str) -> str:
        return ""


def _blocchi_di_oggi() -> list[dict[str, Any]]:
    """I 4 blocchi a trigger dei sensori con memoria, nell'ordine del package, con i
    sensori ``sensor.oggi_*`` che seguono le letture della VMC nativa."""
    oggetti = {chiave.removeprefix("sensor.") for chiave in MEMORIA}
    blocchi = []
    for blocco in package()["template"]:
        sensori = blocco.get("sensor") or []
        if "triggers" not in blocco or not any(
            conf["default_entity_id"].removeprefix("sensor.vmc_master_") in oggetti
            for conf in sensori
        ):
            continue
        nuovo = copy.deepcopy(blocco)
        nuovo["triggers"] = [
            {
                chiave: (
                    LETTE.sub(r"sensor.vmc_nativa_\1", v)
                    if chiave == "entity_id"
                    else v
                )
                for chiave, v in trigger.items()
            }
            for trigger in nuovo["triggers"]
        ]
        for conf in nuovo["sensor"]:
            oggetto = conf["default_entity_id"].removeprefix("sensor.vmc_master_")
            conf["default_entity_id"] = f"sensor.oggi_{oggetto}"
            conf["unique_id"] = f"oggi_{oggetto}"
            conf["state"] = LETTE.sub(r"sensor.vmc_nativa_\1", conf["state"])
        blocchi.append(nuovo)
    assert len(blocchi) == 4
    return blocchi


async def _statistiche(chiamata: ServiceCall) -> dict[str, Any]:
    """recorder.get_statistics finto: 30 giorni di medie orarie per le statistiche chieste."""
    adesso = dt_util.utcnow().replace(minute=0, second=0, microsecond=0)

    def righe(base: float) -> list[dict[str, Any]]:
        return [
            {
                "start": (adesso - timedelta(hours=i)).isoformat(),
                "end": (adesso - timedelta(hours=i - 1)).isoformat(),
                "mean": base + i % 5,
            }
            for i in range(24 * 30, 0, -1)
        ]

    return {
        "statistics": {
            statistica: righe(21.0 if "temp" in statistica else 55.0)
            for statistica in chiamata.data["statistic_ids"]
        }
    }


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_sensori_con_memoria_agli_istanti_dei_template_a_trigger(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Avvio, avvio finito, letture uguali, interruzione e ritorno, minuto 5: identici."""
    freezer.move_to("2026-11-25 10:04:00+00:00")
    hass.set_state(CoreState.not_running)
    fase = "setup"
    visti: dict[str, list[tuple[Any, ...]]] = {"oggi": [], "domani": []}
    domani = {f"sensor.vmc_nativa_{c.removeprefix('sensor.')}" for c in MEMORIA}

    @callback
    def annota(evento: Event) -> None:
        entity_id = evento.data["entity_id"]
        if entity_id.startswith("sensor.oggi_"):
            lato, oggetto = "oggi", entity_id.removeprefix("sensor.oggi_")
        elif entity_id in domani:
            lato, oggetto = "domani", entity_id.removeprefix("sensor.vmc_nativa_")
        else:
            return
        if evento.event_type == EVENT_STATE_REPORTED:
            visti[lato].append((fase, oggetto, "senza cambio"))
            return
        nuovo = evento.data["new_state"]
        interruzione = nuovo.attributes.get("lettura_prima_dell_interruzione")
        visti[lato].append((fase, oggetto, nuovo.state, interruzione))

    @callback
    def chiamata(evento: Event) -> None:
        if evento.data["domain"] != "recorder":
            return
        dati = dict(evento.data["service_data"])
        lato = "oggi" if "vmc_master_" in str(dati["statistic_ids"]) else "domani"
        dati["statistic_ids"] = [
            s.replace("vmc_master_", "vmc_nativa_") for s in dati["statistic_ids"]
        ]
        visti[lato].append((fase, "recorder.get_statistics", dati))

    @callback
    def filtro(dati: Any) -> bool:
        entity_id = dati["entity_id"]
        return entity_id.startswith("sensor.oggi_") or entity_id in domani

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota, event_filter=filtro)
    hass.bus.async_listen(EVENT_STATE_REPORTED, annota, event_filter=filtro)
    hass.bus.async_listen(EVENT_CALL_SERVICE, chiamata)
    hass.services.async_register(
        "recorder",
        "get_statistics",
        _statistiche,
        supports_response=SupportsResponse.ONLY,
    )
    client = _Client()

    async def ping(host: str) -> bool:
        return client.accesa

    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(
        hass, "template", {"template": _blocchi_di_oggi()}
    )
    nativa = VMCNativa(
        hass,
        None,
        "nativa",
        client.host,
        client=client,
        prova_ping=ping,
        versione=False,
    )
    await nativa.avvia()
    sensori, _ = crea_entita(nativa.stato, nativa.letture_dei_sensori())
    voluti = [*MEMORIZZATE, *MEMORIA]
    await MockEntityPlatform(
        hass, domain="sensor", platform_name="vmc_master"
    ).async_add_entities([s for s in sensori if s.chiave in voluti])
    await hass.async_block_till_done()

    async def leggi(*chiavi: str) -> None:
        for chiave in chiavi:
            await nativa.letture[chiave].async_refresh()
        await hass.async_block_till_done()

    fase = "avvio"
    hass.set_state(CoreState.starting)
    hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
    await hass.async_block_till_done()
    fase = "avvio finito"
    hass.set_state(CoreState.running)
    hass.bus.async_fire(EVENT_HOMEASSISTANT_STARTED)
    await hass.async_block_till_done()
    fase = "letture uguali"
    await leggi("sensor.status_ventola", "sensor.sensori")
    fase = "letture cambiate"
    client.risposte["VMGH?"] = "VMGO,00004" + ",00000" * 13
    await leggi("sensor.status_ventola")
    fase = "interruzione"
    client.accesa = False
    await leggi("sensor.status_ventola", "sensor.sensori", "sensor.nome")
    fase = "ritorno"
    client.accesa = True
    await leggi("sensor.status_ventola", "sensor.sensori", "sensor.nome")
    fase = "minuto 5"
    freezer.move_to("2026-11-25 10:05:00+00:00")
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    nativa.ferma()

    oggi = visti["oggi"]
    # Home Assistant: la regola di avvio quando l'avvio è finito (nessuna scrittura
    # all'avvio); al ritorno della VMC le letture uguali si riscrivono senza cambio;
    # al minuto 5 le medie si riscrivono dopo la lettura delle statistiche
    assert not [voce for voce in oggi if voce[0] == "avvio"]
    assert [voce[1] for voce in oggi if voce[0] == "avvio finito"] == [
        "status_ventola_memorizzata",
        "sensori_memorizzata",
        "nome_memorizzata",
        "recorder.get_statistics",
        "temp_interna_media_4w",
        "hum_interna_media_4w",
        "temp_interna_media_8w",
        "hum_interna_media_8w",
        "temp_interna_media_12w",
        "hum_interna_media_12w",
        "rischio_muffa_giorni_dati",
    ]
    assert ("ritorno", "sensori_memorizzata", "senza cambio") in oggi
    assert ("ritorno", "nome_memorizzata", "senza cambio") in oggi
    assert [voce[1:] for voce in oggi if voce[0] == "minuto 5"][1:] == [
        (oggetto, "senza cambio")
        for oggetto in (
            "temp_interna_media_4w",
            "hum_interna_media_4w",
            "temp_interna_media_8w",
            "hum_interna_media_8w",
            "temp_interna_media_12w",
            "hum_interna_media_12w",
            "rischio_muffa_giorni_dati",
        )
    ]
    # all'aggiunta delle entità l'ordine dipende da come si caricano le piattaforme (oggi
    # il blocco con gli attributi arriva per ultimo): conta che scrivano gli stessi stati
    assert sorted(v for v in visti["domani"] if v[0] == "setup") == sorted(
        v for v in oggi if v[0] == "setup"
    )
    assert [v for v in visti["domani"] if v[0] != "setup"] == [
        v for v in oggi if v[0] != "setup"
    ]
