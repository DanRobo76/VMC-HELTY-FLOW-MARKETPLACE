"""Il file JavaScript della scheda (Home Assistant vero, plance in modalità storage).

La versione nativa lo serve dalla cartella dell'integrazione (percorso statico), senza
copie in /config. La beta lo copiava in /config/www/vmc_master e la risorsa delle plance
puntava a /local/vmc_master/...: finché la VMC aspetta il passaggio, copia e risorsa
restano come le ha lasciate la beta; con il passaggio confermato la risorsa passa
all'indirizzo dell'integrazione (stessa voce, dall'interfaccia delle risorse di Home
Assistant) e la copia della beta si toglie, come la cartella del package."""

from __future__ import annotations

from pathlib import Path

import pytest
from homeassistant.components.frontend import DATA_EXTRA_MODULE_URL
from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.core import HomeAssistant

from custom_components.vmc_master.const import DOMAIN, FILE_SCHEDA_JS, URL_FRONTEND

from .banco import (
    VERSIONE_BETA,
    aggiungi_e_avvia,
    carica_package,
    conferma_dalla_riparazione,
    file_scritti,
    riavvio,
    scrivi_package_beta,
    senza_rete,
    voce,
)

URL_DELLA_BETA = f"/local/vmc_master/{FILE_SCHEDA_JS}?v={VERSIONE_BETA}"
JS_DELLA_BETA = b"// vmc-master-card.js della beta\n"


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


def _url_nativa(hass: HomeAssistant) -> str:
    versione = hass.data["integrations"][DOMAIN].version
    return f"{URL_FRONTEND}/{FILE_SCHEDA_JS}?v={versione}"


def _risorse(hass: HomeAssistant) -> list[tuple[str, str, str]]:
    return [
        (r["id"], r["type"], r["url"])
        for r in hass.data[LOVELACE_DATA].resources.async_items()
    ]


RISORSE_DELLA_BETA = [
    {"id": "risorsa_della_beta", "type": "module", "url": URL_DELLA_BETA},
    {"id": "risorsa_utente", "type": "module", "url": "/local/mia_scheda.js"},
]


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_dalla_beta_alla_nativa(
    hass: HomeAssistant, hass_storage, hass_client, tmp_path: Path
) -> None:
    config_dir = str(tmp_path)
    www = tmp_path / "www"
    copia = www / "vmc_master" / FILE_SCHEDA_JS
    copia.parent.mkdir(parents=True)
    copia.write_bytes(JS_DELLA_BETA)
    hass_storage["lovelace_resources"] = {
        "version": 1,
        "minor_version": 1,
        "key": "lovelace_resources",
        "data": {"items": RISORSE_DELLA_BETA},
    }
    master = voce("master")
    cartella = scrivi_package_beta(config_dir, "master", master.data["host"])
    prima = file_scritti(www)

    # primo avvio nativo, package della beta ancora caricato: la beta resta com'è
    await carica_package(hass, [cartella])
    await aggiungi_e_avvia(hass, [master])
    await hass.data[LOVELACE_DATA].resources.async_get_info()
    assert file_scritti(www) == prima
    assert copia.read_bytes() == JS_DELLA_BETA
    assert _risorse(hass) == [
        ("risorsa_della_beta", "module", URL_DELLA_BETA),
        ("risorsa_utente", "module", "/local/mia_scheda.js"),
    ]
    # il JavaScript nativo si serve dalla cartella dell'integrazione
    client = await hass_client()
    risposta = await client.get(f"{URL_FRONTEND}/{FILE_SCHEDA_JS}")
    assert risposta.status == 200
    assert "vmc-master-conto-alla-rovescia" in await risposta.text()
    assert _url_nativa(hass) in hass.data[DATA_EXTRA_MODULE_URL].urls

    # passaggio confermato: la stessa risorsa con l'indirizzo dell'integrazione, la
    # copia della beta tolta (con la sua cartella, rimasta vuota)
    await conferma_dalla_riparazione(hass)
    assert _risorse(hass) == [
        ("risorsa_della_beta", "module", _url_nativa(hass)),
        ("risorsa_utente", "module", "/local/mia_scheda.js"),
    ]
    assert file_scritti(www) == {}
    assert not (www / "vmc_master").exists()

    # dopo il riavvio: VMC nativa, la risorsa resta quella, nulla in www
    async with riavvio(hass, [master], config_dir) as nativa:
        await aggiungi_e_avvia(nativa, [])
        await nativa.data[LOVELACE_DATA].resources.async_get_info()
        assert _risorse(nativa) == [
            ("risorsa_della_beta", "module", _url_nativa(nativa)),
            ("risorsa_utente", "module", "/local/mia_scheda.js"),
        ]
        assert file_scritti(www) == {}


async def test_installazione_nuova(hass: HomeAssistant, tmp_path: Path) -> None:
    """Prima VMC senza la beta: la risorsa con l'indirizzo dell'integrazione, nessun file
    in /config/www; con l'ultima VMC eliminata la risorsa si toglie."""
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    await hass.data[LOVELACE_DATA].resources.async_get_info()
    assert [(t, u) for _i, t, u in _risorse(hass)] == [("module", _url_nativa(hass))]
    assert not (tmp_path / "www").exists()
    assert _url_nativa(hass) in hass.data[DATA_EXTRA_MODULE_URL].urls
    assert await hass.config_entries.async_remove(master.entry_id)
    await hass.async_block_till_done()
    assert _risorse(hass) == []
    assert not (tmp_path / "www").exists()
