"""9.0.0b46: l'IP della VMC si cambia solo dall'ingranaggio della VMC.

Nella versione nativa non ci sono più il campo «Cambia IP VMC» della scheda, il sensore che
lo verificava, il suo valore di esito, il comando che scriveva l'IP, l'automazione «Cambio
IP VMC (Riavvio di H.A.)» (riavviava Home Assistant) e il servizio vmc_master.verifica_ip.
Le loro voci rimaste nel registro da una versione di prima si tolgono all'avvio della VMC.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.vmc_master as integrazione
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.nativa import tabelle
from custom_components.vmc_master.nativa.motore.memoria_interna import INTERNI
from custom_components.vmc_master.trasforma import per_vmc, rinomina

INTEGRAZIONE = Path(integrazione.__file__).parent
GENERATO = INTEGRAZIONE / "nativa" / "motore" / "generato_fase4"
SCHEDA = INTEGRAZIONE / "nativa" / "scheda_nativa.txt"
# il campo, il suo esito, il comando, il sensore e l'automazione (oggetti degli entity_id)
TOLTI = (
    "ip_insert",
    "ip_insert_esito",
    "aggiorna_indirizzo_ip",
    "verifica_ip_inserito",
    "cambio_ip_vmc",
)
ENTITA = (
    "text.vmc_master_ip_insert",
    "sensor.vmc_master_verifica_ip_inserito",
    "automation.vmc_master_cambio_ip_vmc_riavvio_di_h_a",
)
NOTA = (
    "L'IP della VMC si cambia da *Impostazioni → Dispositivi e servizi → VMC Master → ⚙️ → "
    "Cambia l'IP della VMC*."
)


def _voce() -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}
    )


async def test_nessuna_entita_ne_servizio(hass: HomeAssistant) -> None:
    """La VMC nativa avviata: nessuna entità del campo, nessuna automazione che riavvia
    Home Assistant, nessun servizio dell'integrazione; l'ingranaggio cambia ancora l'IP."""
    voce = _voce()
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    vmc = voce.runtime_data.vmc
    assert vmc is not None
    for entity_id in ENTITA:
        assert hass.states.get(entity_id) is None, entity_id
    registrate = {
        e.entity_id
        for e in er.async_entries_for_config_entry(er.async_get(hass), voce.entry_id)
    }
    assert not [e for e in registrate if any(o in e for o in TOLTI)]
    assert len(vmc.motore.automazioni) == 13
    assert not [a for a in vmc.motore.automazioni if "cambio_ip" in a.unique_id]
    assert "vmc_master_aggiorna_indirizzo_ip" not in vmc.c.comandi.comandi
    assert not hass.services.has_service(DOMAIN, "verifica_ip")
    assert hass.services.async_services_for_domain(DOMAIN) == {}
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    assert "cambia_ip" in risultato["menu_options"]


async def test_voci_rimaste_nel_registro(hass: HomeAssistant) -> None:
    """Le voci del campo, del sensore e dell'automazione rimaste nel registro (b44, b45) e
    legate alla voce della VMC si tolgono all'avvio; una non legata alla voce resta."""
    voce = _voce()
    voce.add_to_hass(hass)
    registro = er.async_get(hass)
    campo = registro.async_get_or_create(
        "text", DOMAIN, "vmc_master_ip_insert", config_entry=voce
    )
    automazione = registro.async_get_or_create(
        "automation",
        "automation",
        "vmc_master_cambio_ip_vmc",
        suggested_object_id="vmc_master_cambio_ip_vmc_riavvio_di_h_a",
        config_entry=voce,
    )
    # stesso unique_id, ma non della VMC (nessuna voce): resta
    estraneo = registro.async_get_or_create(
        "sensor", DOMAIN, "vmc_master_verifica_ip_inserito"
    )
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    assert registro.async_get(campo.entity_id) is None
    assert registro.async_get(automazione.entity_id) is None
    assert registro.async_get(estraneo.entity_id) is not None
    assert hass.states.get(campo.entity_id) is None


def test_nessuna_voce_nelle_tabelle() -> None:
    """Le tabelle native non hanno le voci tolte: le elencano in ``TOLTE``."""
    assert set(tabelle.TOLTE) == {
        "input_text.ip_insert",
        "input_text.ip_insert_esito",
        "shell_command.aggiorna_indirizzo_ip",
        "sensor.verifica_ip_inserito",
        "automation.cambio_ip_vmc_riavvio_di_h_a",
    }
    for chiave in tabelle.TOLTE:
        assert chiave not in tabelle.IMPOSTAZIONI and chiave not in tabelle.SENSORI
        assert tabelle.DOMANI.get(chiave, "tolta") == "tolta"
        assert chiave not in INTERNI
    escluse = tabelle.IMPOSTAZIONI["input_select.entita_escluse_recorder"]["options"]
    assert not [o for o in escluse if any(f"_{t}" in o for t in TOLTI)]


def test_nessun_codice_del_motore() -> None:
    """Il codice tradotto della fase 4: nessuna automazione del campo, nessun riavvio di
    Home Assistant, nessun servizio verifica_ip, nessun comando che scrive l'IP."""
    testo = "\n".join(p.read_text(encoding="utf-8") for p in sorted(GENERATO.glob("*.py")))
    for parola in (
        "homeassistant.restart",
        "verifica_ip",
        "ip_insert",
        "cambio_ip",
        "aggiorna_indirizzo_ip",
        "Cambio IP VMC",
    ):
        assert parola not in testo, parola
    assert len(re.findall(r"^\s+Automazione\(", testo, re.MULTILINE)) == 13
    # la descrizione dell'Automazione VMC Master dice dove si cambia l'IP, uguale per ogni VMC
    frase = (
        "- Il Cambio dell'IP non è in questa automazione: si fa da Impostazioni → "
        "Dispositivi e servizi → VMC Master → ⚙️ → Cambia l'IP della VMC."
    )
    assert testo.count(frase) == 1
    assert rinomina(frase, "sala") == frase


def test_nessun_elemento_della_scheda() -> None:
    """La scheda nativa: niente campo né avvisi sotto il campo; la nota dice dove si
    cambia l'IP."""
    testo = SCHEDA.read_text(encoding="utf-8")
    for parola in ("ip_insert", "verifica_ip", "Cambia IP VMC (Riavvio", "IP salvato."):
        assert parola not in testo, parola
    assert testo.count("<strong>Nota Cambia IP VMC</strong>") == 1
    assert NOTA in " ".join(testo.split())
    # per un'altra VMC il nome dell'integrazione nel percorso resta «VMC Master»
    assert NOTA in " ".join(per_vmc(testo, "sala", "192.168.1.161").split())


def test_nessun_servizio_nei_file() -> None:
    """Nessun services.yaml e nessun testo di servizi nelle traduzioni."""
    assert not (INTEGRAZIONE / "services.yaml").exists()
    for file in (
        INTEGRAZIONE / "strings.json",
        *sorted((INTEGRAZIONE / "translations").glob("*.json")),
    ):
        assert "services" not in json.loads(file.read_text(encoding="utf-8")), file
