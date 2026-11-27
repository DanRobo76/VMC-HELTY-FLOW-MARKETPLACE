"""I nomi visibili delle entità native (Home Assistant vero): il package non c'è più,
quindi nessun nome parla del package (genera_tabelle.NOMI_NATIVI). Cambia solo il nome:
entity_id e unique_id restano quelli della beta."""

from __future__ import annotations

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .banco import aggiungi_e_avvia, entity_id_attesi, senza_rete, voce


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_nomi_senza_package(hass: HomeAssistant) -> None:
    voci = [voce("master"), voce("nord", 1)]
    await aggiungi_e_avvia(hass, voci)
    registro = er.async_get(hass)
    for una in voci:
        nome = una.data["nome"]
        versione = f"sensor.vmc_{nome}_versione_corrente"
        avviso = f"binary_sensor.vmc_{nome}_popup_versione_corrente_vs_repository"
        assert hass.states.get(versione).attributes["friendly_name"] == "Versione"
        assert hass.states.get(avviso).attributes["friendly_name"] == (
            "PopUp Notifica Aggiornamento"
        )
        assert registro.async_get(versione).unique_id == f"vmc_{nome}_versione_corrente"
        assert registro.async_get(avviso).unique_id == (
            f"vmc_{nome}_popup_versione_corrente_vs_repository"
        )
        nomi = {
            e: hass.states.get(e).attributes.get("friendly_name", "")
            for e in entity_id_attesi(nome)
        }
        assert {e: n for e, n in nomi.items() if "package" in n.lower()} == {}
