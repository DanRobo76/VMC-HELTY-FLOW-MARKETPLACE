"""I testi della riparazione del passaggio (traduzioni caricate da Home Assistant).

Il primo passo («conferma») si mostra sempre, anche quando poi non serve un riavvio
(nessun package caricato, per esempio cartella già tolta: le VMC ripartono subito,
native). Non può quindi dare il riavvio per certo: lo chiede, se serve, il passo
seguente («confirm»)."""

from __future__ import annotations

import re

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.translation import async_get_translations

from custom_components.vmc_master import ISSUE_PASSAGGIO
from custom_components.vmc_master.const import DOMAIN

PASSI = f"component.{DOMAIN}.issues.{ISSUE_PASSAGGIO}.fix_flow.step"


@pytest.mark.parametrize(
    ("lingua", "riavvio", "se_serve"),
    [
        ("it", "riavvi", "se serve un riavvio"),
        ("en", "restart", "if a home assistant restart is needed"),
    ],
)
async def test_conferma_senza_dare_il_riavvio_per_certo(
    hass: HomeAssistant, lingua: str, riavvio: str, se_serve: str
) -> None:
    testi = await async_get_translations(hass, lingua, "issues", [DOMAIN])
    frasi = re.split(r"(?<=[.:!?])\s+", testi[f"{PASSI}.conferma.description"].lower())
    del_riavvio = [f for f in frasi if riavvio in f]
    assert del_riavvio, lingua
    assert all(se_serve in f for f in del_riavvio), del_riavvio
    # il riavvio lo chiede il passo seguente
    assert riavvio in testi[f"{PASSI}.confirm.description"].lower()
