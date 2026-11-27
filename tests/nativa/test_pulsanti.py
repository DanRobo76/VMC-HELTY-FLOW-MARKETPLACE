"""I 25 pulsanti della VMC (fase 4): identità dalla tabella, pressione verso il motore.

Che la pressione faccia esattamente quello che fa oggi la chiamata della scheda lo
controlla tests/nativa/motore/test_script_interni.py (scenari «aggancio_dei_comandi» e
«vmc_che_non_risponde»); qui i nomi, gli entity_id e i casi senza motore.
"""

from __future__ import annotations

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockEntityPlatform

from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.pulsanti import crea_pulsanti
from custom_components.vmc_master.nativa.tabelle import PULSANTI


@pytest.mark.parametrize("nome", ["master", "zeta"])
def test_identita(hass: HomeAssistant, nome: str) -> None:
    """Oggetto dello script o del comando di oggi, unique_id vmc_<nome>_<oggetto>,
    nome dello script di oggi (VMC Master - ... / VMC zeta - ...)."""
    pulsanti = crea_pulsanti(Contesto(hass, nome))
    assert len(pulsanti) == 25
    per_id = {p.entity_id: p for p in pulsanti}
    profilo = per_id[f"button.vmc_{nome}_audio_profilo"]
    assert profilo.unique_id == f"vmc_{nome}_audio_profilo"
    atteso = "Master" if nome == "master" else nome
    assert profilo.name == f"VMC {atteso} - Profilo Audio"
    assert profilo.icon == "mdi:cursor-pointer"
    assert per_id[f"button.vmc_{nome}_velocita_1"].name == f"VMC {atteso} - Velocità 1"
    assert sorted(p.entity_id.split(".", 1)[1] for p in pulsanti) == sorted(
        f"vmc_{nome}_{chiave.split('.', 1)[1]}" for chiave in PULSANTI
    )


async def test_senza_motore(hass: HomeAssistant) -> None:
    """Un pulsante premuto prima che script e comandi del motore ci siano è un errore
    (nessuna pressione persa in silenzio)."""
    assert await async_setup_component(hass, "button", {})
    c = Contesto(hass)
    pulsanti = [
        p
        for p in crea_pulsanti(c)
        if p.entity_id
        in ("button.vmc_master_audio_profilo", "button.vmc_master_notturna")
    ]
    await MockEntityPlatform(
        hass, domain="button", platform_name="vmc_master"
    ).async_add_entities(pulsanti)
    for entita, messaggio in (
        ("button.vmc_master_audio_profilo", "script del motore"),
        ("button.vmc_master_notturna", "comandi del motore"),
    ):
        with pytest.raises(RuntimeError, match=messaggio):
            await hass.services.async_call(
                "button", "press", {"entity_id": entita}, blocking=True
            )
