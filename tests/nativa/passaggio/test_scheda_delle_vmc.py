"""La scheda nativa di ogni VMC, non solo della master (Home Assistant vero, scheda e
JavaScript serviti dall'integrazione).

Per le altre VMC la scheda passa dalla stessa rinomina degli script della beta
(«master» → ‹nome›): devono cambiare solo gli entity_id e i testi. I nomi che non sono
entità (tipi delle schede personalizzate definite dal JavaScript, link, indirizzi)
restano quelli della master."""

from __future__ import annotations

import re

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from custom_components.vmc_master.const import DOMAIN, FILE_SCHEDA_JS, URL_FRONTEND

from .banco import ClientFinto, aggiungi_e_avvia, senza_rete, voce

NOMI = ("master", "nord", "sud")
# indirizzi: link assoluti e attributi href/src (anche relativi) dei testi HTML
RE_INDIRIZZO = re.compile(r"""https?://[^\s"'<>\\]+|(?:href|src)=\\?["'](/[^"'\\]*)""")
RE_TIPO = re.compile(r"\bcustom:([a-z0-9-]+)")
RE_ENTITA = re.compile(r"\b([a-z_]+)\.vmc_([a-z]+)_(\w+)")


@pytest.fixture(autouse=True)
def rete_finta():
    ClientFinto.istanze.clear()
    with senza_rete():
        yield


def _elementi_definiti(js: str) -> set[str]:
    """I tipi che il JavaScript della scheda registra (customElements.define)."""
    costanti = dict(re.findall(r'const (\w+) = "([a-z0-9-]+)";', js))
    definiti = set()
    for argomento in re.findall(r"customElements\.define\(\s*([^,\s]+)", js):
        definiti.add(costanti.get(argomento, argomento.strip("\"'")))
    return definiti


def _indirizzi(testo: str) -> list[str]:
    return sorted(
        relativo or assoluto
        for assoluto, relativo in (
            (m.group(0), m.group(1)) for m in RE_INDIRIZZO.finditer(testo)
        )
    )


async def test_scheda_di_ogni_vmc(hass: HomeAssistant, hass_client) -> None:
    voci = [voce(nome, numero) for numero, nome in enumerate(NOMI)]
    await aggiungi_e_avvia(hass, voci)
    client = await hass_client()
    risposta = await client.get(f"{URL_FRONTEND}/{FILE_SCHEDA_JS}")
    assert risposta.status == 200
    definiti = _elementi_definiti(await risposta.text())
    assert {"vmc-master-card", "vmc-master-conto-alla-rovescia"} <= definiti

    schede: dict[str, str] = {}
    for v in voci:
        risposta = await client.get(f"/api/vmc_master/scheda/{v.entry_id}")
        assert risposta.status == 200
        schede[v.data["nome"]] = await risposta.text()

    registro = er.async_get(hass)
    for nome, testo in schede.items():
        # ogni scheda personalizzata usata dalla scheda esiste nel JavaScript
        tipi = set(RE_TIPO.findall(testo))
        assert tipi, nome
        assert tipi <= definiti, (nome, tipi - definiti)
        # link e indirizzi uguali a quelli della master
        assert _indirizzi(testo) == _indirizzi(schede["master"]), nome
        # gli entity_id sono quelli della master con il nome della VMC
        assert {(d, o) for d, n, o in RE_ENTITA.findall(testo) if n == nome} == {
            (d, o) for d, n, o in RE_ENTITA.findall(schede["master"]) if n == "master"
        }, nome
        assert {n for _d, n, _o in RE_ENTITA.findall(testo)} == {nome}, nome
        # e ogni entità intera della scheda è un'entità della VMC
        voce_vmc = next(v for v in voci if v.data["nome"] == nome)
        entita_vmc = {
            e.entity_id
            for e in er.async_entries_for_config_entry(registro, voce_vmc.entry_id)
        }
        usate = {
            f"{d}.vmc_{nome}_{o}"
            for d, n, o in RE_ENTITA.findall(testo)
            if d in ("sensor", "binary_sensor", "switch", "number", "select", "text")
            and not o.endswith("_")
        }
        assert usate, nome
        assert usate - entita_vmc == set(), nome
    assert len(hass.config_entries.async_entries(DOMAIN)) == 3
