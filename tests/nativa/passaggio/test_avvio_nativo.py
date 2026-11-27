"""La VMC nativa dalle voci di configurazione: avvio, scaricamento, ricarica ed
eliminazione, con una VMC e con tre (Home Assistant vero). Nulla si scrive in
/config/packages né in /config/vmc_master_backup."""

from __future__ import annotations

from pathlib import Path

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import EntityStateAttribute
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir

from custom_components.vmc_master import ISSUE_PASSAGGIO, passaggio
from custom_components.vmc_master.const import CONF_HOST, DOMAIN
from custom_components.vmc_master.nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO as CHIAVE_MEMORIA_INTERNA,
)
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.nativa.tabelle import IMPOSTAZIONI

from .banco import (
    ClientFinto,
    aggiungi_e_avvia,
    automazioni_attese,
    file_scritti,
    senza_rete,
    voce,
    voci_attese,
)

ENTITA_PER_VMC = (
    367  # 172 impostazioni + 136 sensori + 34 sensori dei timer + 25 pulsanti
)
AUTOMAZIONI_PER_VMC = 13
# voci del registro legate alla voce della VMC: le entità native (le automazioni del
# motore sono logiche dell'integrazione, senza entità)
VOCI_PER_VMC = ENTITA_PER_VMC


@pytest.fixture(autouse=True)
def rete_finta():
    ClientFinto.istanze.clear()
    with senza_rete():
        yield


def _entita(hass: HomeAssistant, entry_id: str) -> list[er.RegistryEntry]:
    return er.async_entries_for_config_entry(er.async_get(hass), entry_id)


def _della_vmc(entity_id: str, nome: str) -> bool:
    return (
        f"vmc_{nome}_" in entity_id or entity_id == f"automation.automazione_vmc_{nome}"
    )


def _automazioni(hass: HomeAssistant, nome: str) -> list[str]:
    """Le automazioni del motore della VMC avviate: logiche dell'integrazione, con il
    loro stato interno (nessuna entità ``automation`` della VMC, nemmeno ripristinata)."""
    assert [
        s.entity_id
        for s in hass.states.async_all("automation")
        if _della_vmc(s.entity_id, nome)
    ] == []
    return sorted(e for e in stati_logiche(hass).stati if _della_vmc(e, nome))


def _nulla_in_config(config_dir: Path) -> None:
    assert file_scritti(config_dir / "packages") == {}
    assert file_scritti(config_dir / "vmc_master_backup") == {}


async def test_una_vmc_si_avvia_si_ricarica_si_scarica_e_si_elimina(
    hass: HomeAssistant, hass_storage, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    assert master.state is ConfigEntryState.LOADED
    assert master.runtime_data.situazione == passaggio.NATIVA
    voci = _entita(hass, master.entry_id)
    assert len(voci) == VOCI_PER_VMC
    assert all(hass.states.get(v.entity_id) is not None for v in voci)
    assert {v.entity_id for v in voci} == voci_attese("master")  # niente «_2»
    # le automazioni del motore: logiche avviate, senza entità né voci del registro
    assert set(_automazioni(hass, "master")) == automazioni_attese("master")
    assert sorted(a.entity_id for a in master.runtime_data.vmc.motore.automazioni) == (
        sorted(automazioni_attese("master"))
    )
    assert ir.async_get(hass).async_get_issue(DOMAIN, ISSUE_PASSAGGIO) is None
    assert [c.host for c in ClientFinto.istanze] == ["192.168.1.160"]

    # ricarica: stesse entità, una VMC nuova
    vmc_prima = master.runtime_data.vmc
    assert await hass.config_entries.async_reload(master.entry_id)
    await hass.async_block_till_done()
    assert master.state is ConfigEntryState.LOADED
    assert master.runtime_data.vmc is not vmc_prima
    assert {v.entity_id for v in _entita(hass, master.entry_id)} == {
        v.entity_id for v in voci
    }
    # gli stessi oggetti: i 120 sensori template sono ancora i sensori template (non i
    # modelli della fase 2 al loro posto, con i template rifiutati per unique_id doppio)
    assert len(master.runtime_data.vmc.template) == len(vmc_prima.template) == 120
    assert len(master.runtime_data.vmc.sensori) == len(vmc_prima.sensori)
    assert "does not generate unique IDs" not in caplog.text
    assert all(
        not hass.states.get(v.entity_id).attributes.get(EntityStateAttribute.RESTORED)
        for v in voci
    )
    assert len(_automazioni(hass, "master")) == AUTOMAZIONI_PER_VMC

    # scaricata: niente entità vive (il registro resta), logiche del motore fermate
    assert await hass.config_entries.async_unload(master.entry_id)
    await hass.async_block_till_done()
    assert master.state is ConfigEntryState.NOT_LOADED
    assert len(_entita(hass, master.entry_id)) == VOCI_PER_VMC
    assert all(
        hass.states.get(v.entity_id) is None
        or hass.states.get(v.entity_id).state == "unavailable"
        for v in voci
    )
    assert _automazioni(hass, "master") == []

    # eliminata: Home Assistant toglie le sue entità (nessuna voce delle automazioni del
    # motore); la memoria interna resta, con l'istante dell'eliminazione
    # (test_riaggiunta.py)
    assert await hass.config_entries.async_setup(master.entry_id)
    await hass.async_block_till_done()
    assert CHIAVE_MEMORIA_INTERNA.format(nome="master") in hass_storage
    await hass.config_entries.async_remove(master.entry_id)
    await hass.async_block_till_done()
    assert _entita(hass, master.entry_id) == []
    registro = er.async_get(hass)
    assert [e for e in automazioni_attese("master") if registro.async_get(e)] == []
    assert (
        "eliminata"
        in hass_storage[CHIAVE_MEMORIA_INTERNA.format(nome="master")]["data"]
    )
    assert passaggio.CHIAVE_ARCHIVIO.format(nome="master") not in hass_storage
    _nulla_in_config(tmp_path)


async def test_tre_vmc(hass: HomeAssistant, tmp_path: Path) -> None:
    """Tre VMC: ognuna con le sue 367 entità, le sue 13 automazioni e il suo client.
    Nella versione nativa non ci sono parti solo del master (nessuna voce ``solo_master``
    in tabelle.py; le sezioni Clona VMC e Installa VMC non sono nella scheda nativa)."""
    voci = [voce("master", 0), voce("cucina", 1), voce("bagno", 2)]
    await aggiungi_e_avvia(hass, voci)
    assert sorted(c.host for c in ClientFinto.istanze) == [
        "192.168.1.160",
        "192.168.1.161",
        "192.168.1.162",
    ]
    assert not [k for k, v in IMPOSTAZIONI.items() if v.get("solo_master")]
    tutte: set[str] = set()
    for una in voci:
        nome = una.data["nome"]
        assert una.state is ConfigEntryState.LOADED
        entity_ids = {v.entity_id for v in _entita(hass, una.entry_id)}
        assert entity_ids == voci_attese(nome)  # niente «_2»
        assert len(entity_ids) == VOCI_PER_VMC
        assert len(_automazioni(hass, nome)) == AUTOMAZIONI_PER_VMC
        tutte |= entity_ids
    assert len(tutte) == 3 * VOCI_PER_VMC

    # una si ricarica e una si elimina: le altre non si toccano
    vmc_master = voci[0].runtime_data.vmc
    assert await hass.config_entries.async_reload(voci[1].entry_id)
    await hass.config_entries.async_remove(voci[2].entry_id)
    await hass.async_block_till_done()
    assert voci[0].runtime_data.vmc is vmc_master
    assert voci[1].state is ConfigEntryState.LOADED
    assert _entita(hass, voci[2].entry_id) == []
    assert _automazioni(hass, "bagno") == []
    assert len(_automazioni(hass, "master")) == AUTOMAZIONI_PER_VMC
    for una in voci[:2]:
        assert await hass.config_entries.async_unload(una.entry_id)
    await hass.async_block_till_done()
    _nulla_in_config(tmp_path)


async def test_ip_cambiato_dall_ingranaggio_ricarica_la_vmc(
    hass: HomeAssistant,
) -> None:
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    vmc_prima = master.runtime_data.vmc
    hass.config_entries.async_update_entry(
        master, data={**master.data, CONF_HOST: "192.168.1.170"}
    )
    await hass.async_block_till_done()
    assert master.state is ConfigEntryState.LOADED
    assert master.runtime_data.vmc is not vmc_prima
    assert master.runtime_data.ip == "192.168.1.170"
    assert ClientFinto.istanze[-1].host == "192.168.1.170"


async def test_scheda_nativa(hass: HomeAssistant, hass_client) -> None:
    """La scheda della VMC nativa: quella di nativa/scheda_nativa.txt, con i link del
    repository dell'integrazione."""
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    client = await hass_client()
    risposta = await client.get(f"/api/vmc_master/scheda/{master.entry_id}")
    assert risposta.status == 200
    testo = await risposta.text()
    assert "switch.vmc_master_notifica_audio" in testo
    assert "input_boolean.vmc_master_notifica_audio" not in testo
    assert "DanRobo76/VMC-HELTY-FLOW/" not in testo


async def test_codice_tradotto_importato_fuori_dal_ciclo(hass: HomeAssistant) -> None:
    """Il codice tradotto (moduli grandi, secondi di importazione) si importa
    nell'esecutore delle importazioni di Home Assistant: importato nel ciclo degli eventi
    lo bloccherebbe, e Home Assistant lo segnala nel registro («Detected blocking call to
    import_module»), come nella prova del proprietario del 27-11-2026."""
    import importlib
    import sys
    import threading

    from custom_components.vmc_master.nativa import assemblaggio

    moduli = (assemblaggio.CODICE_FASE4, assemblaggio.CODICE_SENSORI)
    # come al primo avvio di Home Assistant: il codice tradotto non è ancora importato
    salvati = {nome: sys.modules.pop(nome) for nome in moduli if nome in sys.modules}
    importa = importlib.import_module
    nel_ciclo: list[str] = []

    def importa_e_annota(nome: str, *args, **kwargs):
        if (
            nome in moduli
            and nome not in sys.modules
            and threading.get_ident() == hass.loop_thread_id
        ):
            nel_ciclo.append(nome)
        return importa(nome, *args, **kwargs)

    try:
        with pytest.MonkeyPatch.context() as patch:
            patch.setattr(importlib, "import_module", importa_e_annota)
            master = voce("master")
            await aggiungi_e_avvia(hass, [master])
        assert master.state is ConfigEntryState.LOADED
        assert all(nome in sys.modules for nome in moduli)
        assert nel_ciclo == []
    finally:
        pacchetto = sys.modules[
            "custom_components.vmc_master.nativa.motore.generato_fase4"
        ]
        for nome, modulo in salvati.items():
            sys.modules[nome] = modulo
            setattr(pacchetto, nome.rsplit(".", 1)[1], modulo)
