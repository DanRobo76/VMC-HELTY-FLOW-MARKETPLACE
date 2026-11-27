"""Le entità native mostrano in Home Assistant gli stessi sensori dei template di oggi.

Come il banco dei modelli, ma attraverso tutto il percorso nativo: gli stessi ingressi vanno
ai template del package (entity_id di oggi) e a StatoVMC, che aggiorna le entità native
(registrate qui come «<dominio>.nativa_<oggetto>» per stare accanto a quelle di oggi). A ogni
giro si confrontano stato, icona, nome, unità e classi visti in Home Assistant.
"""

from __future__ import annotations

from datetime import timedelta
import os
import random

import pytest

from custom_components.vmc_master.nativa.entita import crea_entita, nome_visibile
from custom_components.vmc_master.nativa.modelli import MODELLI
from custom_components.vmc_master.nativa.stato import StatoVMC
from custom_components.vmc_master.nativa.tabelle import SENSORI
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.setup import async_setup_component

from pytest_homeassistant_custom_component.common import MockEntityPlatform

from . import confronto as c
from .genera_tabelle import NOMI_NATIVI
from .test_modelli_confronto import _ora

GIRI = int(os.environ.get("VMC_GIRI", "400")) // 4
SEME = int(os.environ.get("VMC_SEME", "20261125"))
# il ritardo del Black-Out (delay_on) ha il suo test: qui si confronta solo la sua icona
CON_RITARDO = {k for k, m in MODELLI.items() if m.ritardo_on is not None}
ATTRIBUTI = ("friendly_name", "icon", "unit_of_measurement", "device_class", "state_class")


def _nativa(chiave: str) -> str:
    dominio, oggetto = chiave.split(".", 1)
    return f"{dominio}.nativa_{oggetto}"


def test_nome_visibile() -> None:
    """{Nome}: Master per la Master, il nome così com'è per le altre VMC (come il clona)."""
    assert nome_visibile("VMC {Nome} Temp. Ext. Selezionata", "master") == "VMC Master Temp. Ext. Selezionata"
    assert nome_visibile("VMC {Nome} Temp. Ext. Selezionata", "sala") == "VMC sala Temp. Ext. Selezionata"
    assert nome_visibile("vmc_{nome}_lan {NOME}", "master") == "vmc_master_lan MASTER"
    assert nome_visibile("vmc_{nome}_lan {NOME}", "sala") == "vmc_sala_lan sala"


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_entita_uguali_ai_template(hass: HomeAssistant, freezer) -> None:
    """Stessi stati e attributi dei template del package, giro dopo giro."""
    await hass.config.async_set_time_zone("Europe/Rome")
    assert await async_setup_component(hass, "homeassistant", {})
    rng = random.Random(f"{SEME}-entita")
    stati = c.base_iniziale(rng)
    freezer.move_to(_ora(rng, stati))
    esterni_attr = {eid: c.attributi_esterni(rng, eid) for eid in c.ESTERNI}

    def attributi(eid: str) -> dict:
        return c.attributi_fissi(eid) or esterni_attr.get(eid, {})

    for eid, valore in stati.items():
        hass.states.async_set(eid, valore, attributi(eid))
    assert await async_setup_component(
        hass, "template", {"template": [b for b in c.package()["template"] if "triggers" not in b]}
    )
    await hass.async_block_till_done()

    stato = StatoVMC(hass, c.NOME, c.IP)
    sensori, binari = crea_entita(stato)
    modelli = [e for e in [*sensori, *binari] if e.chiave in MODELLI]
    for entita in modelli:
        entita.entity_id = _nativa(entita.chiave)
    for dominio, gruppo in (("sensor", sensori), ("binary_sensor", binari)):
        piattaforma = MockEntityPlatform(hass, domain=dominio, platform_name="vmc_master")
        await piattaforma.async_add_entities([e for e in gruppo if e.chiave in MODELLI])

    def propri() -> dict[str, tuple[str, dict]]:
        """Ingressi di proprietà della VMC (entity_id di oggi -> chiave) per StatoVMC."""
        uscita = {}
        for eid, valore in stati.items():
            if eid in c.ESTERNI:
                continue
            dominio, oggetto = eid.split(".", 1)
            uscita[f"{dominio}.{oggetto.removeprefix(f'vmc_{c.NOME}_')}"] = (valore, attributi(eid))
        return uscita

    stato.imposta(propri())
    stato.avvia()
    await hass.async_block_till_done()
    scritture: dict[str, int] = {}

    @callback
    def _conta(evento: Event) -> None:
        eid = evento.data["entity_id"]
        scritture[eid] = scritture.get(eid, 0) + 1

    hass.bus.async_listen(EVENT_STATE_CHANGED, _conta)
    tutti = [eid for eid, d in c.modelli().items() if "triggers" not in d["blocco"]]
    differenze: list[str] = []
    for giro in range(GIRI):
        if giro:
            stati = c.campione(rng, stati, rng.randint(1, 10))
            if c.extra.SCENARI and rng.random() < 0.2:
                stati.update(c.extra.SCENARI[sorted(c.extra.SCENARI)[giro % len(c.extra.SCENARI)]])
            freezer.move_to(_ora(rng, stati))
            # il tempo passa da solo, prima degli ingressi (come lo scatto di ogni minuto)
            await hass.services.async_call(
                "homeassistant", "update_entity", {"entity_id": tutti}, blocking=True
            )
            stato.ricalcola()
            if rng.random() < 0.2:
                eid = rng.choice(c.ESTERNI)
                esterni_attr[eid] = c.attributi_esterni(rng, eid)
                hass.states.async_set(eid, stati[eid], attributi(eid))
        # Gli ingressi cambiano uno alla volta, nello stesso ordine per i template e per
        # StatoVMC: così si confrontano anche le scritture nel registro.
        for eid, valore in stati.items():
            attuale = hass.states.get(eid)
            if attuale is None or attuale.state != valore:
                hass.states.async_set(eid, valore, attributi(eid))
                if eid not in c.ESTERNI:
                    dominio, oggetto = eid.split(".", 1)
                    chiave = f"{dominio}.{oggetto.removeprefix(f'vmc_{c.NOME}_')}"
                    stato.imposta({chiave: (valore, attributi(eid))})
        await hass.async_block_till_done()
        await hass.services.async_call("homeassistant", "update_entity", {"entity_id": tutti}, blocking=True)
        stato.ricalcola()
        await hass.async_block_till_done()
        for entita in modelli:
            eid_oggi = f"{entita.chiave.split('.')[0]}.vmc_{c.NOME}_{entita.chiave.split('.', 1)[1]}"
            oggi = hass.states.get(eid_oggi)
            nativa = hass.states.get(entita.entity_id)
            if entita.chiave not in CON_RITARDO and oggi.state != nativa.state:
                differenze.append(f"giro {giro} {entita.chiave}: oggi {oggi.state!r}, nativa {nativa.state!r}")
            for nome in ATTRIBUTI:
                if nome == "icon" and entita.chiave in CON_RITARDO:
                    continue  # l'icona segue lo stato ritardato
                atteso = oggi.attributes.get(nome)
                if nome == "friendly_name" and entita.chiave in NOMI_NATIVI:
                    atteso = NOMI_NATIVI[entita.chiave]  # nome nativo voluto
                if atteso != nativa.attributes.get(nome):
                    differenze.append(
                        f"giro {giro} {entita.chiave} {nome}: oggi {oggi.attributes.get(nome)!r}, "
                        f"nativa {nativa.attributes.get(nome)!r}"
                    )
        assert not differenze, "\n".join(differenze[:30])
    stato.ferma()
    # Scritture nel registro: le entità native non cambiano più spesso dei template di oggi
    # (i template possono passare per stati intermedi a ogni ingresso; le native no).
    oggi_tot = nativa_tot = 0
    di_piu = []
    for entita in modelli:
        if entita.chiave in CON_RITARDO:
            continue
        eid_oggi = f"{entita.chiave.split('.')[0]}.vmc_{c.NOME}_{entita.chiave.split('.', 1)[1]}"
        n_oggi, n_nativa = scritture.get(eid_oggi, 0), scritture.get(entita.entity_id, 0)
        oggi_tot += n_oggi
        nativa_tot += n_nativa
        if n_nativa > n_oggi:
            di_piu.append(f"{entita.chiave}: oggi {n_oggi}, nativa {n_nativa}")
    print(f"scritture: oggi {oggi_tot}, native {nativa_tot}")
    assert not di_piu, "\n".join(di_piu[:30])


async def test_ritardo_black_out(hass: HomeAssistant, freezer) -> None:
    """delay_on: acceso solo se la condizione resta vera per tutto il ritardo; spento subito."""
    chiave = "binary_sensor.black_out_rilevato"
    if chiave not in MODELLI:
        pytest.skip("modello non ancora portato")
    scenario = c.extra.SCENARI["t5"]
    stato = StatoVMC(hass, c.NOME)
    base = {
        f"{eid.split('.')[0]}.{eid.split('.', 1)[1].removeprefix('vmc_master_')}": v
        for eid, v in scenario.items()
    }
    base["input_number.attesa_blackout_rilevazione"] = "32.0"
    stato.imposta({"sensor.status_ip": "ON-Line"})
    assert stato.stato(chiave) == "off"
    stato.imposta(base)  # condizione vera: parte il ritardo di 32 s
    assert stato.stato(chiave) == "off"
    freezer.tick(timedelta(seconds=20))
    from pytest_homeassistant_custom_component.common import async_fire_time_changed  # noqa: PLC0415

    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    assert stato.stato(chiave) == "off"
    stato.imposta({"sensor.status_ip": "ON-Line"})  # condizione falsa prima dei 32 s
    stato.imposta({"sensor.status_ip": "OFF-Line"})  # di nuovo vera: il ritardo riparte
    freezer.tick(timedelta(seconds=20))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    assert stato.stato(chiave) == "off"
    freezer.tick(timedelta(seconds=13))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    assert stato.stato(chiave) == "on"
    assert stato.icona(chiave) is not None
    stato.imposta({"sensor.status_ip": "ON-Line"})  # spento subito
    assert stato.stato(chiave) == "off"
    stato.ferma()


def test_tutte_le_chiavi_hanno_entita() -> None:
    """crea_entita fa un'entità per ognuna delle 136 voci, nel dominio giusto."""
    stato = StatoVMC.__new__(StatoVMC)
    stato.nome = "master"
    sensori, binari = crea_entita(stato)
    assert len(sensori) + len(binari) == len(SENSORI) == 136
    assert {e.chiave for e in binari} == {k for k in SENSORI if k.startswith("binary_sensor.")}
    assert all(e.entity_id == f"{e.chiave.split('.')[0]}.vmc_master_{e.chiave.split('.', 1)[1]}" for e in sensori)
