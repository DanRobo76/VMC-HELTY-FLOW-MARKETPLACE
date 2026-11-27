"""b46: le automazioni del motore non sono più entità (le voci della b45 si tolgono).

Fino alla 9.0.0b45 le 14 automazioni del motore erano entità del componente
``automation``: la loro pagina (Impostazioni → Automazioni e scenari) si apriva in sola
lettura con la configurazione data dal motore (``automation/config``) e la loro voce del
registro era legata alla voce della VMC. Dalla 9.0.0b46 sono logiche dell'integrazione,
senza entità: dopo l'avvio nativo non c'è nessuna entità ``automation`` della VMC (né la
pagina da aprire) e ``_togli_le_automazioni_di_prima`` toglie le voci del registro
rimaste dalla b45 (piattaforma ``automation``, legate alla voce della VMC: anche quella
di «Cambio IP VMC (Riavvio di H.A.)», che dalla 9.0.0b46 non c'è più, 13 automazioni);
le voci delle entità native e le automazioni dell'utente (senza voce di configurazione,
anche con un nome da VMC) restano.

Home Assistant vero, VMC finta (nessuna rete)."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche

from .banco import aggiungi_e_avvia, automazioni_attese, senza_rete, voce, voci_attese


async def test_nessuna_entita_e_voci_della_b45_tolte(hass: HomeAssistant) -> None:
    """Le voci delle 14 automazioni della b45, legate alla voce della VMC, si tolgono
    all'avvio nativo; l'automazione dell'utente resta com'era; nessuna entità
    ``automation`` della VMC, le 13 logiche avviate con gli entity_id di prima."""
    with senza_rete():
        una = voce("master")
        una.add_to_hass(hass)
        registro = er.async_get(hass)
        attese = automazioni_attese("master")
        assert len(attese) == 13
        # come le lasciava la b45 (14 automazioni, con quella del cambio d'IP): unique_id
        # e entity_id delle automazioni del package, voce legata alla voce della VMC
        cambio_ip = "automation.vmc_master_cambio_ip_vmc_riavvio_di_h_a"
        della_b45 = [
            registro.async_get_or_create(
                "automation",
                "automation",
                "vmc_master_cambio_ip_vmc"
                if entity_id == cambio_ip
                else entity_id.split(".", 1)[1],
                suggested_object_id=entity_id.split(".", 1)[1],
                config_entry=una,
            )
            for entity_id in sorted({*attese, cambio_ip})
        ]
        assert sorted(v.entity_id for v in della_b45) == sorted({*attese, cambio_ip})
        # un'automazione dell'utente (automations.yaml) con un nome da VMC
        dell_utente = registro.async_get_or_create(
            "automation",
            "automation",
            "1764200000000",
            suggested_object_id="vmc_master_mia_automazione",
        )

        await aggiungi_e_avvia(hass, [])

        # nessuna entità automation della VMC: le logiche hanno uno stato interno
        assert [
            s.entity_id
            for s in hass.states.async_all("automation")
            if s.entity_id in attese or "vmc_master" in s.entity_id
        ] == []
        assert set(stati_logiche(hass).stati) == attese
        assert sorted(a.entity_id for a in una.runtime_data.vmc.motore.automazioni) == (
            sorted(attese)
        )

        # le voci della b45 tolte, quella dell'utente com'era, le native legate
        assert [v.entity_id for v in della_b45 if registro.async_get(v.entity_id)] == []
        assert registro.async_get(dell_utente.entity_id) == dell_utente
        legate = er.async_entries_for_config_entry(registro, una.entry_id)
        assert {v.entity_id for v in legate} == voci_attese("master")
        assert not [v for v in legate if v.platform == "automation"]

        # la VMC ricaricata: nessuna voce da togliere, le native restano
        assert await hass.config_entries.async_reload(una.entry_id)
        await hass.async_block_till_done()
        legate = er.async_entries_for_config_entry(registro, una.entry_id)
        assert {v.entity_id for v in legate} == voci_attese("master")
        assert registro.async_get(dell_utente.entity_id) == dell_utente
        assert set(stati_logiche(hass).stati) == attese

        assert await hass.config_entries.async_unload(una.entry_id)
        await hass.async_block_till_done()
        assert stati_logiche(hass).stati == {}
