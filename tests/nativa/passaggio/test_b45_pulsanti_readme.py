"""b45: la tabella «Pulsante / Cosa fa» dei README fa quello che promette (27-11-2026).

Per ogni riga della tabella, nelle due guide (Marketplace e GitHub) e nelle due lingue:
il pulsante esiste con quel nome nella VMC nativa vera e, premuto con ``button.press``
(come nelle automazioni dell'utente), manda alla VMC il comando giusto. Il comando è lo
stesso del vecchio shell_command con lo stesso nome (protocollo della VMC: 0-4 velocità,
5 Iperventilazione, 6 Notturna, 7 Free Cooling / Free Heating; sensori, LED, filtro).

VMC nativa vera, VMC finta che annota i comandi, ping finto (ON-Line)."""

from __future__ import annotations

import asyncio
import re
from datetime import timedelta
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.vmc_master.nativa.letture import LetturaPing

from ..confronto import RADICE
from .banco import ClientFinto, aggiungi_e_avvia, senza_rete, voce

# pulsante -> comando mandato alla VMC
ATTESI = {
    "button.vmc_master_velocita_0": "VMWH0000000",
    "button.vmc_master_velocita_1": "VMWH0000001",
    "button.vmc_master_velocita_2": "VMWH0000002",
    "button.vmc_master_velocita_3": "VMWH0000003",
    "button.vmc_master_velocita_4": "VMWH0000004",
    "button.vmc_master_notturna": "VMWH0000006",
    "button.vmc_master_iperventilazione": "VMWH0000005",
    "button.vmc_master_freecooling": "VMWH0000007",
    "button.vmc_master_sensori_on": "VMWH0300000",
    "button.vmc_master_sensori_off": "VMWH0300002",
    "button.vmc_master_pannello_led_on": "VMWH0100010",
    "button.vmc_master_pannello_led_off": "VMWH0100000",
    "button.vmc_master_reset_filtro_vmc": "VMWH0417744",
}

# cosa promette la tabella, in italiano e in inglese
PROMESSE = {
    "it": {
        "button.vmc_master_velocita_0": "Ferma la VMC (Velocità 0)",
        "button.vmc_master_velocita_1": "Velocità 1",
        "button.vmc_master_velocita_2": "Velocità 2",
        "button.vmc_master_velocita_3": "Velocità 3",
        "button.vmc_master_velocita_4": "Velocità 4",
        "button.vmc_master_notturna": "Velocità Notturna",
        "button.vmc_master_iperventilazione": "Iperventilazione",
        "button.vmc_master_freecooling": "Free Cooling / Free Heating",
        "button.vmc_master_sensori_on": "Accende i sensori della VMC",
        "button.vmc_master_sensori_off": "Spegne i sensori della VMC",
        "button.vmc_master_pannello_led_on": "Accende i LED del pannello",
        "button.vmc_master_pannello_led_off": "Spegne i LED del pannello",
        "button.vmc_master_reset_filtro_vmc": "Azzera il contatore del filtro",
    },
}

RIGA = re.compile(r"^\| <sub>`(button\.vmc_master_[a-z0-9_]+)`</sub> \| <sub>(.+?)</sub> \|$")


def _tabelle(percorso) -> list[dict[str, str]]:
    """Le tabelle dei pulsanti di un README, nell'ordine (italiano, poi inglese)."""
    tabelle: list[dict[str, str]] = []
    in_tabella = False
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if trovata := RIGA.match(riga):
            if not in_tabella:
                tabelle.append({})
                in_tabella = True
            tabelle[-1][trovata[1]] = trovata[2]
        else:
            in_tabella = False
    return tabelle


@pytest.mark.parametrize("nome", ["README.md", ".github/README.md"])
def test_tabelle_dei_readme(nome: str) -> None:
    """Due tabelle per guida (italiano e inglese), con gli stessi 13 pulsanti nello
    stesso ordine; il testo italiano è quello promesso."""
    italiano, inglese = _tabelle(RADICE / nome)
    assert list(italiano) == list(ATTESI)
    assert list(inglese) == list(ATTESI)
    assert italiano == PROMESSE["it"]


async def _ping_on_line(_self) -> str:
    return "ON-Line"


async def _lascia_girare() -> None:
    """Il ciclo degli eventi gira senza aspettare gli script fermi nelle loro pause (con
    l'orologio fermo async_block_till_done non finirebbe)."""
    for _ in range(200):
        await asyncio.sleep(0)


async def _avanza(hass: HomeAssistant, freezer: FrozenDateTimeFactory, secondi: int) -> None:
    for _ in range(secondi):
        freezer.tick(timedelta(seconds=1))
        async_fire_time_changed(hass)
        await _lascia_girare()


async def test_ogni_pulsante_manda_il_suo_comando(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Ogni pulsante della tabella esiste e, premuto come in un'automazione, manda alla
    VMC il suo comando (e nessun altro)."""
    ClientFinto.istanze.clear()
    with senza_rete(), patch.object(LetturaPing, "_async_update_data", _ping_on_line):
        for componente in ("homeassistant", "persistent_notification"):
            assert await async_setup_component(hass, componente, {})
        una = voce("master")
        await aggiungi_e_avvia(hass, [una])
        (client,) = ClientFinto.istanze
        # oltre i 140 s dell'avvio: le allerte riattivate non mandano più comandi
        await _avanza(hass, freezer, 150)
        for pulsante, comando in ATTESI.items():
            assert hass.states.get(pulsante) is not None, pulsante
            prima = len(client.comandi)
            hass.async_create_task(
                hass.services.async_call(
                    "button", "press", {"entity_id": pulsante}, blocking=True
                )
            )
            # il Reset Filtro è uno script: il comando subito, poi 5 s di conto alla
            # rovescia sotto il pulsante
            await _avanza(hass, freezer, 6)
            assert client.comandi[prima:] == [comando], pulsante
        assert await hass.config_entries.async_unload(una.entry_id)
        await _lascia_girare()
