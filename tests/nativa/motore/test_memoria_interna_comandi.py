"""Chiamate con impostazioni native e valori interni insieme (fase 4).

Il package spegne la spia interna (``input_boolean.spia_umidita_mantenuta_velocita_0``)
insieme ad altre spie che domani sono entità native: 51 ``input_boolean.turn_off`` e 1
``input_boolean.turn_on`` con bersagli misti. ``ScritturaComandi`` con la memoria
interna (``memoria=``) le scrive tutte in una volta, come oggi Home Assistant con gli
aiutanti. Home Assistant (gli aiutanti) è l'oracolo: stessi cambi e stessi
``state_reported`` (istante, stato, last_changed, last_reported, contesto), stessi
avvisi; l'ordine fra le entità è quello di un insieme di nomi, che domani sono altri:
si confronta ordinato, come in ``test_comandi_confronto``.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import (
    EVENT_CALL_SERVICE,
    EVENT_STATE_CHANGED,
    EVENT_STATE_REPORTED,
)
from homeassistant.core import Context, Event, callback
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    async_test_home_assistant,
)

from custom_components.vmc_master.nativa.comandi import ScritturaComandi, crea_comandi
from custom_components.vmc_master.nativa.motore.memoria_interna import MemoriaInterna
from custom_components.vmc_master.nativa.stato import StatoVMC
from custom_components.vmc_master.nativa.tabelle import DOMANI, IMPOSTAZIONI

from ..servizi_di_prova import registra_servizi

T0 = datetime(2026, 11, 25, 9, 0, 0, tzinfo=UTC)
INTERNO = "input_boolean.spia_umidita_mantenuta_velocita_0"
# Il bersaglio di uno dei 51 spegnimenti misti del package (9 spie native e la spia
# interna) e quello dell'accensione mista.
SPIE = (
    "input_boolean.umidita_verifica_soglia_valore_spia",
    "input_boolean.spia_umidita_velocita_0",
    INTERNO,
    "input_boolean.spia_umidita_velocita_1",
    "input_boolean.spia_umidita_velocita_2",
    "input_boolean.spia_umidita_velocita_3",
    "input_boolean.spia_umidita_velocita_4",
    "input_boolean.spia_umidita_velocita_notturna",
    "input_boolean.spia_umidita_velocita_iperventilazione",
    "input_boolean.spia_umidita_velocita_freecooling",
)
ACCENSIONE = ("input_boolean.spia_umidita_velocita_0", INTERNO)
DOMINIO_PROVA = "vmc_prova_misti"
MANCA = "non_esiste"


def _oggi(chiave: str) -> str:
    dominio, oggetto = chiave.split(".", 1)
    return f"{dominio}.vmc_master_{oggetto}"


def _domani(chiave: str) -> str:
    """Il nome di domani: quello dell'entità nativa, o di oggi per il valore interno."""
    if DOMANI[chiave] == "interna":
        return _oggi(chiave)
    return f"{DOMANI[chiave]}.vmc_master_{chiave.split('.', 1)[1]}"


# (servizio, chiavi, via): via «motore» = ScritturaComandi.chiama (o l'azione degli
# script di Home Assistant, senza «registrato»), «registrato» = servizio registrato
PASSI: list[tuple[str, tuple[str, ...], str]] = [
    ("input_boolean.turn_on", SPIE, "motore"),
    ("input_boolean.turn_off", SPIE, "motore"),
    ("input_boolean.turn_off", SPIE, "motore"),
    ("input_boolean.turn_on", ACCENSIONE, "motore"),
    ("input_boolean.turn_off", (*SPIE, MANCA), "motore"),
    ("input_boolean.turn_on", SPIE, "registrato"),
    ("input_boolean.turn_off", SPIE, "registrato"),
]


async def _corsa(
    freezer: FrozenDateTimeFactory, *, domani: bool, caplog: pytest.LogCaptureFixture
) -> dict[str, Any]:
    freezer.move_to(T0)
    nomi = _domani if domani else _oggi
    indietro = {nomi(k): k for k in SPIE}
    contesti: dict[str, int] = {}
    eventi: list[tuple[Any, ...]] = []
    chiamate: list[tuple[Any, ...]] = []
    esito: dict[str, Any] = {"eventi": eventi, "chiamate": chiamate, "avvisi": []}
    attivo = False

    def forma(contesto: Context) -> tuple[Any, ...]:
        return (contesti.get(contesto.id, "nuovo"), contesto.parent_id)

    @callback
    def annota(evento: Event) -> None:
        if not attivo:
            return
        nuovo = evento.data["new_state"]
        eventi.append(
            (
                indietro[evento.data["entity_id"]],
                (evento.time_fired - T0).total_seconds(),
                evento.event_type,
                nuovo.state,
                (nuovo.last_changed - T0).total_seconds(),
                (nuovo.last_reported - T0).total_seconds(),
                forma(evento.context),
            )
        )

    @callback
    def nostra(dati: Any) -> bool:
        return dati["entity_id"] in indietro

    async with async_test_home_assistant() as hass:
        await hass.config.async_set_time_zone("Europe/Rome")
        assert await async_setup_component(hass, "homeassistant", {})
        hass.bus.async_listen(EVENT_STATE_CHANGED, annota, nostra)
        hass.bus.async_listen(EVENT_STATE_REPORTED, annota, nostra)
        hass.bus.async_listen(
            EVENT_CALL_SERVICE,
            callback(lambda e: chiamate.append((e.data["domain"], e.data["service"]))),
        )
        scrittura: ScritturaComandi | None = None
        if domani:
            stato = StatoVMC(hass, "master")
            memoria = MemoriaInterna(hass, "master", (INTERNO,), stato=stato)
            memoria.ripristina()
            # i cambi e i rapporti del valore interno non passano dal bus: li annuncia
            # la memoria nel canale del motore
            memoria.ascolta_cambi(annota)
            memoria.ascolta_rapporti(annota)
            gruppi: dict[str, list[Any]] = {}
            for dominio, voci in crea_comandi(stato).items():
                for voce in voci:
                    if voce.chiave in SPIE:
                        gruppi.setdefault(dominio, []).append(voce)
            for dominio, voci in gruppi.items():
                assert await async_setup_component(hass, dominio, {})
                piattaforma = MockEntityPlatform(
                    hass, domain=dominio, platform_name="vmc_master"
                )
                await piattaforma.async_add_entities(voci)
            scrittura = ScritturaComandi(
                hass, [v for g in gruppi.values() for v in g], memoria
            )
            registrati = registra_servizi(scrittura, DOMINIO_PROVA)
            assert hass.states.get(_oggi(INTERNO)) is None
        else:
            assert await async_setup_component(
                hass,
                "input_boolean",
                {
                    "input_boolean": {
                        _oggi(k).split(".", 1)[1]: dict(IMPOSTAZIONI[k]) for k in SPIE
                    }
                },
            )
        await hass.async_block_till_done()
        attivo = True
        for numero, (servizio, chiavi, via) in enumerate(PASSI, 1):
            freezer.move_to(T0 + timedelta(seconds=numero))
            contesto = Context(parent_id="genitore")
            contesti[contesto.id] = numero
            bersagli = [
                f"input_boolean.vmc_master_{k}" if k == MANCA else nomi(k)
                for k in chiavi
            ]
            caplog.clear()
            if scrittura is not None and via == "motore":
                await scrittura.chiama(servizio, {"entity_id": bersagli}, contesto)
            else:
                if scrittura is not None:
                    servizio = registrati[servizio]
                dominio, nome = servizio.split(".")
                await hass.services.async_call(
                    dominio,
                    nome,
                    {"entity_id": bersagli},
                    blocking=True,
                    context=contesto,
                )
            await hass.async_block_till_done()
            esito["avvisi"].append(
                [
                    r.getMessage()
                    for r in caplog.records
                    if r.levelname == "WARNING" and r.name.startswith("homeassistant")
                ]
            )
        if domani:
            esito["memoria"] = memoria.stato(_oggi(INTERNO)).state
            esito["stato_vmc"] = stato.stato(INTERNO)
        await hass.async_stop(force=True)
    return esito


async def test_spie_native_e_spia_interna_insieme(
    freezer: FrozenDateTimeFactory, caplog: pytest.LogCaptureFixture
) -> None:
    """Le chiamate miste del package come con gli aiutanti: ogni spia (nativa o
    interna) cambiata o riportata nello stesso istante, con lo stesso contesto."""
    oggi = await _corsa(freezer, domani=False, caplog=caplog)
    domani = await _corsa(freezer, domani=True, caplog=caplog)
    attesi = sum(len(set(c) - {MANCA}) for _, c, _ in PASSI)
    assert len(oggi["eventi"]) == attesi == 62
    assert sorted(oggi["eventi"]) == sorted(domani["eventi"])
    assert {v[2] for v in oggi["eventi"]} == {EVENT_STATE_CHANGED, EVENT_STATE_REPORTED}
    # l'entità che non c'è: lo stesso avviso (con il nome di domani), le altre scritte
    assert [len(a) for a in oggi["avvisi"]] == [len(a) for a in domani["avvisi"]]
    assert len(oggi["avvisi"][4]) == 1
    assert MANCA in oggi["avvisi"][4][0]
    assert oggi["avvisi"][4] == domani["avvisi"][4]
    # via «registrato» con l'evento call_service, via «motore» senza
    assert oggi["chiamate"] == [("input_boolean", s.split(".")[1]) for s, _, _ in PASSI]
    assert domani["chiamate"] == [
        (DOMINIO_PROVA, s.replace(".", "_")) for s, _, v in PASSI if v == "registrato"
    ]
    assert domani["memoria"] == domani["stato_vmc"] == "off"
