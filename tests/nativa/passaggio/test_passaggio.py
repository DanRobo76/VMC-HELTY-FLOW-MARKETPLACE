"""Passaggio dalla beta con Home Assistant vero: package della beta caricato al primo
avvio nativo, riparazione confermata, riavvio, entità native con gli stessi entity_id e
con i valori della beta.

Le istanze di Home Assistant della prova:

- A, la beta: il package caricato; ogni aiutante prende un valore diverso da quello con
  cui riparte senza valore;
- B, il primo avvio dopo l'aggiornamento: il package è ancora caricato (le sue entità
  hanno ripreso i valori di A con le regole degli aiutanti) e l'integrazione aspetta la
  conferma; gli stati di B sono l'oracolo; qui si conferma dalla riparazione;
- C, il riavvio dopo la conferma: niente package, la VMC nativa;
- D (controllo): una VMC nativa nuova, senza passato, per vedere che ogni valore portato
  cambia davvero qualcosa.

Conto delle 342 voci del package (``DOMANI``), esatto:

- 213 portate: 150 impostazioni visibili e 63 valori interni (stato di B = stato di C);
  206 sono diverse da D; le altre 7 sono gli elenchi di scelta delle entità, che dopo
  ogni riavvio tornano alla loro unica opzione configurata;
- 28 ripartono dal loro ``initial`` (23 visibili, 5 interne), in B come in C;
- 34 timer: fermi dopo il riavvio, in C come dopo ogni riavvio della beta (nessuno ha
  ``restore``), anche quelli attivi in B;
- 67 senza stato: 51 script (13 pulsanti, 38 interni al motore) e 16 comandi di shell
  (12 pulsanti, 4 interni).

Più i 10 sensori con memoria (stato e lettura di prima dell'interruzione portati), le 14
automazioni (logiche del motore con gli entity_id della beta e lo stesso stato, senza
voce del registro) e i 137 sensori con lo stesso entity_id.

Le automazioni del package della beta della prova sono spente (``initial_state: false``,
``banco.configurazione_package``) e fino alla 9.0.0b45 il motore le riprendeva spente;
dalla 9.0.0b46 le logiche girano sempre: nella VMC nativa dopo il passaggio la prova le
avvia senza trigger (``banco.logiche_spente``), così i valori portati restano come sono.
"""

from __future__ import annotations

import shutil
from collections import Counter
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.http import KEY_HASS
from homeassistant.setup import async_setup_component

from custom_components.vmc_master import (
    ISSUE_MANUALE,
    ISSUE_PASSAGGIO,
    ISSUE_RIAVVIO,
    ISSUE_RINOMINATE,
    VmcSchedaView,
    passaggio,
)
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.nativa.comandi import chiavi_comandi
from custom_components.vmc_master.nativa.memoria import IN_ORDINE as SENSORI_CON_MEMORIA
from custom_components.vmc_master.nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO as CHIAVE_MEMORIA_INTERNA,
)
from custom_components.vmc_master.nativa.motore.memoria_interna import INTERNI
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.nativa.tabelle import DOMANI

from .banco import (
    aggiungi_e_avvia,
    automazioni_attese,
    avvia_timer,
    carica_package,
    carica_stati_conservati,
    conferma_dalla_riparazione,
    configurazione_package,
    dai_valori_alle_memorie,
    file_scritti,
    imposta_valori_diversi,
    istanza_nuova,
    logiche_spente,
    riavvio,
    scrivi_package_beta,
    senza_rete,
    stati_ripristinati_all_avvio,
    voce,
    voci_attese,
)

DOMINI_SENSORI = ("sensor", "binary_sensor")
SENZA_STATO = ("script", "shell_command")


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


def _con_initial(config: dict[str, Any], chiave: str, nome: str) -> bool:
    dominio, oggetto = chiave.split(".", 1)
    return (config[dominio].get(f"vmc_{nome}_{oggetto}") or {}).get(
        "initial"
    ) is not None


def _initial_come_stato(config: dict[str, Any], chiave: str, nome: str) -> str:
    dominio, oggetto = chiave.split(".", 1)
    initial = config[dominio][f"vmc_{nome}_{oggetto}"]["initial"]
    if dominio == "input_boolean":
        return "on" if initial else "off"
    if dominio == "input_number":
        return str(float(initial))
    return str(initial)


def _stati_della_vmc(
    hass: HomeAssistant, nome: str, domini: tuple[str, ...]
) -> dict[str, str]:
    return {
        s.entity_id: s.state
        for s in hass.states.async_all(domini)
        if s.entity_id.split(".", 1)[1].startswith(f"vmc_{nome}_")
    }


def _valori_nativi(
    hass: HomeAssistant, vmc: Any, nome: str, chiavi: list[str]
) -> dict[str, str]:
    """Il valore nativo di ogni aiutante: lo stato dell'entità, o del valore interno."""
    valori = {}
    for chiave in chiavi:
        if chiave in INTERNI:
            valori[chiave] = vmc.memoria.stato(vmc.memoria.entity_id(chiave)).state
        else:
            valori[chiave] = hass.states.get(
                passaggio.entity_id_di_domani(chiave, nome)
            ).state
    return valori


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_passaggio_di_una_vmc(
    hass: HomeAssistant, hass_storage, tmp_path: Path
) -> None:
    config_dir = str(tmp_path)
    master = voce("master")
    cartella = scrivi_package_beta(config_dir, "master", master.data["host"])
    aiutanti = [k for k in DOMANI if k.split(".", 1)[0] not in (*SENZA_STATO, "timer")]
    timer = [k for k in DOMANI if k.startswith("timer.")]
    senza_stato = [k for k in DOMANI if k.split(".", 1)[0] in SENZA_STATO]
    assert (len(aiutanti), len(timer), len(senza_stato)) == (241, 34, 67)

    # A: la beta
    config = await carica_package(hass, [cartella])
    scritti = await imposta_valori_diversi(hass, "master")
    assert len(scritti) == 241

    # B: primo avvio dopo l'aggiornamento, package ancora caricato
    async with riavvio(hass, [master], config_dir) as beta:
        await carica_package(beta, [cartella])
        await dai_valori_alle_memorie(beta, "master")
        timer_attivi = await avvia_timer(beta, "master", 4)
        await aggiungi_e_avvia(beta, [])
        voce_b = beta.config_entries.async_get_entry(master.entry_id)
        assert voce_b.state is ConfigEntryState.LOADED
        assert voce_b.runtime_data.situazione == passaggio.IN_ATTESA
        assert voce_b.runtime_data.vmc is None
        registro_b = er.async_get(beta)
        assert er.async_entries_for_config_entry(registro_b, master.entry_id) == []
        problema = ir.async_get(beta).async_get_issue(DOMAIN, ISSUE_PASSAGGIO)
        assert problema is not None and problema.is_fixable
        assert problema.translation_placeholders["elenco"] == (
            "- `/config/packages/vmc_helty_flow/master`"
        )
        chiave_archivio = passaggio.CHIAVE_ARCHIVIO.format(nome="master")
        assert hass_storage[chiave_archivio]["data"]["stato"] == passaggio.LETTO

        oracolo = {
            k: beta.states.get(passaggio.entity_id_di_oggi(k, "master")).state
            for k in aiutanti
        }
        memorie_b = {
            k: beta.states.get(passaggio.entity_id_di_oggi(k, "master"))
            for k in SENSORI_CON_MEMORIA
        }
        sensori_b = _stati_della_vmc(beta, "master", DOMINI_SENSORI)
        assert len(sensori_b) == 137
        id_package = passaggio.id_del_package(config_dir, "master")
        voci_b = {
            e: registro_b.async_get(e).id
            for e in passaggio.voci_del_package(beta, id_package)
        }
        assert (
            Counter(e.split(".", 1)[0] for e in voci_b)
            == {
                "sensor": 118,  # 116 template, rest, command_line (i 4 tcp non hanno unique_id)
                "binary_sensor": 15,
                "input_boolean": 115,
                "input_number": 43,
                "input_text": 38,
                "input_datetime": 30,
                "input_select": 15,
                "timer": 34,
                "script": 51,
                "automation": 14,
            }
        )
        assert len(voci_b) == 473
        automazioni_b = {
            e: (i, beta.states.get(e).state)
            for e, i in voci_b.items()
            if e.startswith("automation.")
        }

        passo = await conferma_dalla_riparazione(beta)

        assert passo["step_id"] == "confirm"  # il riavvio
        assert ir.async_get(beta).async_get_issue(DOMAIN, ISSUE_RIAVVIO) is not None
        assert not cartella.exists()
        assert not cartella.parent.exists()  # vmc_helty_flow, rimasta vuota
        assert passaggio.voci_del_package(beta, id_package) == []
        assert ir.async_get(beta).async_get_issue(DOMAIN, ISSUE_PASSAGGIO) is None
        confermato = hass_storage[chiave_archivio]["data"]
        assert confermato["stato"] == passaggio.CONFERMATO
        assert sorted(confermato["timer_attivi"]) == sorted(timer_attivi)
        assert (len(confermato["impostazioni"]), len(confermato["interni"])) == (
            173,
            68,
        )
        assert (len(confermato["memorie"]), confermato["non_letti"]) == (10, [])

        # C: dopo il riavvio (le logiche senza trigger, come le automazioni della beta)
        async with riavvio(beta, [master], config_dir) as nativa:
            with logiche_spente():
                await aggiungi_e_avvia(nativa, [])
            voce_c = nativa.config_entries.async_get_entry(master.entry_id)
            assert voce_c.state is ConfigEntryState.LOADED
            assert voce_c.runtime_data.situazione == passaggio.NATIVA
            vmc = voce_c.runtime_data.vmc
            registro_c = er.async_get(nativa)

            # stessi entity_id: niente «_2»
            native = {
                e.entity_id
                for e in er.async_entries_for_config_entry(registro_c, master.entry_id)
            }
            attese = (
                {
                    passaggio.entity_id_di_domani(k, "master")
                    for k in DOMANI
                    if DOMANI[k] != "interna"
                }
                | set(sensori_b)
            )
            assert native == attese
            assert len(native) == 369
            assert {e for e in sensori_b if e in native} == set(sensori_b)

            # i 241 aiutanti: stesso valore di B
            valori_c = _valori_nativi(nativa, vmc, "master", aiutanti)
            assert valori_c == oracolo

            # i 10 sensori con memoria
            for chiave, stato_b in memorie_b.items():
                stato_c = nativa.states.get(stato_b.entity_id)
                assert (
                    stato_c.state,
                    stato_c.attributes.get("lettura_prima_dell_interruzione"),
                ) == (
                    stato_b.state,
                    stato_b.attributes.get("lettura_prima_dell_interruzione"),
                ), chiave
            assert (
                sum(
                    s.state not in ("unknown", "unavailable")
                    for s in memorie_b.values()
                )
                == 10
            )

            # le 14 automazioni: logiche con gli entity_id della beta e lo stesso stato,
            # senza voce del registro (quelle della beta tolte con la conferma) e senza
            # entità
            automazioni_c = {
                e: s.state for e, s in stati_logiche(nativa).stati.items()
            }
            assert automazioni_c == {e: s for e, (_, s) in automazioni_b.items()}
            assert len(automazioni_c) == 14
            assert set(automazioni_c) == automazioni_attese("master")
            assert [e for e in automazioni_c if registro_c.async_get(e)] == []
            assert nativa.states.async_entity_ids("automation") == []

            # i 34 timer: tutti fermi, anche i 4 attivi in B
            assert {
                k: vmc.c.timer.timer[vmc.stato.entity_id(k)].state for k in timer
            } == dict.fromkeys(timer, "idle")

            # i 67 senza stato: 25 pulsanti, 42 interni al motore
            pulsanti = [k for k in senza_stato if DOMANI[k] == "button"]
            assert len(pulsanti) == 25
            assert all(
                nativa.states.get(passaggio.entity_id_di_domani(k, "master"))
                for k in pulsanti
            )

            assert (
                hass_storage[CHIAVE_MEMORIA_INTERNA.format(nome="master")]["data"][
                    "valori"
                ]
                == confermato["interni"]
            )
            await nativa.async_block_till_done()
            applicato = hass_storage[chiave_archivio]["data"]
            assert applicato["stato"] == passaggio.APPLICATO
            assert applicato["conteggi"] == {
                "impostazioni": 173,
                "interni": 68,
                "memorie": 10,
                "non_letti": 0,
            }
            assert ir.async_get(nativa).async_get_issue(DOMAIN, ISSUE_RIAVVIO) is None
            assert ir.async_get(nativa).async_get_issue(DOMAIN, ISSUE_PASSAGGIO) is None

    # D: controllo, una VMC nativa nuova (niente registro, niente stati, niente archivi)
    hass_storage.pop(CHIAVE_MEMORIA_INTERNA.format(nome="master"))
    hass_storage.pop(chiave_archivio)
    async with istanza_nuova(config_dir) as nuova:
        await aggiungi_e_avvia(nuova, [voce("master")])
        vmc_d = nuova.config_entries.async_entries(DOMAIN)[0].runtime_data.vmc
        valori_d = _valori_nativi(nuova, vmc_d, "master", aiutanti)

    visibili = set(chiavi_comandi())
    con_initial = {k for k in aiutanti if _con_initial(config, k, "master")}
    portate = [k for k in aiutanti if k not in con_initial]
    conto = Counter(
        (
            "visibile" if k in visibili else "interna",
            "initial" if k in con_initial else "portata",
        )
        for k in aiutanti
    )
    assert conto == {
        ("visibile", "portata"): 150,
        ("interna", "portata"): 63,
        ("visibile", "initial"): 23,
        ("interna", "initial"): 5,
    }
    # ogni valore portato è quello scritto in A ed è diverso da quello di una VMC nuova
    assert {k: oracolo[k] for k in portate} == {k: scritti[k] for k in portate}
    # ... tranne i 7 elenchi di scelta delle entità (input_select con la sola opzione
    # «Aggiorna Elenco ...»: le altre le mette set_options mentre gira, e dopo ogni
    # riavvio Home Assistant torna all'unica opzione configurata, in B come in D)
    uguali_a_una_nuova = [k for k in portate if valori_d[k] == oracolo[k]]
    assert len(uguali_a_una_nuova) == 7
    for chiave in uguali_a_una_nuova:
        dominio, oggetto = chiave.split(".", 1)
        assert dominio == "input_select" and oggetto.startswith("selected_")
        assert config[dominio][f"vmc_master_{oggetto}"]["options"] == [oracolo[chiave]]
    # con initial: in B era già tornato al suo initial (e in C è lo stesso)
    assert {k: oracolo[k] for k in con_initial} == {
        k: _initial_come_stato(config, k, "master") for k in con_initial
    }
    assert [k for k in con_initial if scritti[k] == oracolo[k]] == []
    assert (
        len(portate) + len(con_initial) + len(timer) + len(senza_stato)
        == len(DOMANI)
        == 342
    )


INTERNO_NUMERO = next(k for k in INTERNI if k.startswith("input_number."))
AUTOMAZIONE_PERSONALE = {
    "id": "mia_vmc",
    "alias": "Mia VMC",
    "triggers": [
        {"trigger": "state", "entity_id": "input_boolean.vmc_master_notifica_audio"}
    ],
    "actions": [
        {
            "action": "input_number.set_value",
            "target": {
                "entity_id": passaggio.entity_id_di_oggi(INTERNO_NUMERO, "master")
            },
            "data": {"value": 1},
        }
    ],
}


async def _scheda(hass: HomeAssistant, entry_id: str) -> str:
    """La configurazione della scheda che l'integrazione serve per una voce."""
    richiesta = MagicMock()
    richiesta.app = {KEY_HASS: hass}
    risposta = await VmcSchedaView().get(richiesta, entry_id)
    assert risposta.status == 200
    return risposta.text


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_passaggio_di_tre_vmc(
    hass: HomeAssistant, hass_storage, tmp_path: Path
) -> None:
    """Tre VMC, una riparazione sola; un riavvio senza confermare non cambia nulla; la
    conferma toglie le tre cartelle e segnala le automazioni dell'utente con i vecchi nomi;
    dopo il riavvio tre VMC native con gli stessi entity_id e i valori della beta; una VMC
    aggiunta dopo il passaggio parte subito nativa."""
    config_dir = str(tmp_path)
    voci = [voce("master", 0), voce("cucina", 1), voce("bagno", 2)]
    nomi = [v.data["nome"] for v in voci]
    cartelle = [
        scrivi_package_beta(config_dir, v.data["nome"], v.data["host"]) for v in voci
    ]
    aiutanti = [k for k in DOMANI if k.split(".", 1)[0] not in (*SENZA_STATO, "timer")]

    await carica_package(hass, cartelle)
    for nome in nomi:
        await imposta_valori_diversi(hass, nome)

    async with riavvio(hass, voci, config_dir) as beta:
        await carica_package(beta, cartelle, [AUTOMAZIONE_PERSONALE])
        await aggiungi_e_avvia(beta, [])
        problemi = ir.async_get(beta)
        assert problemi.async_get_issue(
            DOMAIN, ISSUE_PASSAGGIO
        ).translation_placeholders == {
            "elenco": "- `/config/packages/vmc_helty_flow/bagno`\n"
            "- `/config/packages/vmc_helty_flow/cucina`\n"
            "- `/config/packages/vmc_helty_flow/master`"
        }
        # finché aspetta, la scheda è quella della beta (le entità sono del package)
        assert "input_boolean.vmc_master_notifica_audio" in await _scheda(
            beta, voci[0].entry_id
        )
        letto_b = {
            n: hass_storage[passaggio.CHIAVE_ARCHIVIO.format(nome=n)]["data"]
            for n in nomi
        }
        assert {d["stato"] for d in letto_b.values()} == {passaggio.LETTO}

        # riavvio senza conferma: tutto come prima, i valori si rileggono
        async with riavvio(beta, voci, config_dir) as beta2:
            await carica_package(beta2, cartelle, [AUTOMAZIONE_PERSONALE])
            await aggiungi_e_avvia(beta2, [])
            for una in voci:
                voce_b2 = beta2.config_entries.async_get_entry(una.entry_id)
                assert voce_b2.runtime_data.situazione == passaggio.IN_ATTESA
            assert (
                ir.async_get(beta2).async_get_issue(DOMAIN, ISSUE_PASSAGGIO) is not None
            )
            for nome, cartella in zip(nomi, cartelle, strict=True):
                assert cartella.exists()
                letto = hass_storage[passaggio.CHIAVE_ARCHIVIO.format(nome=nome)][
                    "data"
                ]
                assert letto["stato"] == passaggio.LETTO
                assert letto["letto"] > letto_b[nome]["letto"]
            oracoli = {
                n: {
                    k: beta2.states.get(passaggio.entity_id_di_oggi(k, n)).state
                    for k in aiutanti
                }
                for n in nomi
            }
            sensori = {n: _stati_della_vmc(beta2, n, DOMINI_SENSORI) for n in nomi}

            passo = await conferma_dalla_riparazione(beta2)

            assert passo["step_id"] == "confirm"
            assert not cartelle[0].parent.exists()
            rinominate = ir.async_get(beta2).async_get_issue(DOMAIN, ISSUE_RINOMINATE)
            assert rinominate is not None and rinominate.is_persistent
            assert rinominate.learn_more_url == (
                "https://github.com/DanRobo76/VMC-HELTY-FLOW-MASTER/blob/main/NOMI_NATIVI.md"
            )
            assert rinominate.translation_placeholders["elenco"] == (
                "- automation.mia_vmc: `input_boolean.vmc_master_notifica_audio`"
                " → `switch.vmc_master_notifica_audio`\n"
                f"- automation.mia_vmc: `{passaggio.entity_id_di_oggi(INTERNO_NUMERO, 'master')}`"
                " → `-`"
            )

            async with riavvio(beta2, voci, config_dir) as nativa:
                assert await async_setup_component(
                    nativa, "automation", {"automation": [AUTOMAZIONE_PERSONALE]}
                )
                # le logiche senza trigger, come le automazioni della beta
                with logiche_spente():
                    await aggiungi_e_avvia(nativa, [])
                registro = er.async_get(nativa)
                for una, nome in zip(voci, nomi, strict=True):
                    voce_c = nativa.config_entries.async_get_entry(una.entry_id)
                    assert voce_c.runtime_data.situazione == passaggio.NATIVA
                    native = {
                        e.entity_id
                        for e in er.async_entries_for_config_entry(
                            registro, una.entry_id
                        )
                    }
                    assert native == voci_attese(nome)  # niente «_2»
                    assert set(sensori[nome]) <= native
                    valori = _valori_nativi(
                        nativa, voce_c.runtime_data.vmc, nome, aiutanti
                    )
                    assert valori == oracoli[nome]
                assert "switch.vmc_master_notifica_audio" in await _scheda(
                    nativa, voci[0].entry_id
                )

                # una VMC aggiunta dopo il passaggio: subito nativa, nessuna riparazione
                nuova = voce("studio", 3)
                nuova.add_to_hass(nativa)
                assert await nativa.config_entries.async_setup(nuova.entry_id)
                await nativa.async_block_till_done()
                assert nuova.runtime_data.situazione == passaggio.NATIVA
                assert (
                    len(er.async_entries_for_config_entry(registro, nuova.entry_id))
                    == 369
                )
                assert (
                    ir.async_get(nativa).async_get_issue(DOMAIN, ISSUE_PASSAGGIO)
                    is None
                )
                assert (
                    passaggio.CHIAVE_ARCHIVIO.format(nome="studio") not in hass_storage
                )
                assert file_scritti(tmp_path / "packages") == {}
                assert file_scritti(tmp_path / "vmc_master_backup") == {}


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_cartella_gia_tolta_con_voci_rimaste(
    hass: HomeAssistant, hass_storage, tmp_path: Path
) -> None:
    """La cartella della beta tolta a mano, ma le voci del package ancora nel registro:
    la VMC aspetta la conferma (gli entity_id non sono liberi); i valori vengono dagli
    stati che Home Assistant ha conservato; con la conferma la VMC parte subito nativa,
    senza riavvio."""
    config_dir = str(tmp_path)
    master = voce("master")
    cartella = scrivi_package_beta(config_dir, "master", master.data["host"])
    config = await carica_package(hass, [cartella])
    scritti = await imposta_valori_diversi(hass, "master")
    await dai_valori_alle_memorie(hass, "master")
    memorie_a = {
        k: hass.states.get(passaggio.entity_id_di_oggi(k, "master"))
        for k in SENSORI_CON_MEMORIA
    }
    shutil.rmtree(cartella.parent)

    async with riavvio(hass, [master], config_dir) as beta:
        stati_ripristinati_all_avvio(beta)
        await aggiungi_e_avvia(beta, [])
        assert master.entry_id in [
            v.entry_id for v in beta.config_entries.async_entries(DOMAIN)
        ]
        voce_b = beta.config_entries.async_get_entry(master.entry_id)
        assert voce_b.runtime_data.situazione == passaggio.IN_ATTESA
        letto = hass_storage[passaggio.CHIAVE_ARCHIVIO.format(nome="master")]["data"]
        assert (
            len(letto["impostazioni"]),
            len(letto["interni"]),
            len(letto["memorie"]),
        ) == (
            173,
            68,
            10,
        )

        # la VMC nativa parte con la conferma: le logiche senza trigger, come le
        # automazioni della beta
        with logiche_spente():
            passo = await conferma_dalla_riparazione(beta)
            await beta.async_block_till_done()

        assert passo["type"] == "create_entry"  # niente riavvio
        assert ir.async_get(beta).async_get_issue(DOMAIN, ISSUE_RIAVVIO) is None
        await beta.async_block_till_done()
        assert voce_b.state is ConfigEntryState.LOADED
        voce_b = beta.config_entries.async_get_entry(master.entry_id)
        assert voce_b.runtime_data.situazione == passaggio.NATIVA
        native = {
            e.entity_id
            for e in er.async_entries_for_config_entry(
                er.async_get(beta), master.entry_id
            )
        }
        assert native == voci_attese("master")  # niente «_2»
        aiutanti = list(letto["impostazioni"]) + list(letto["interni"])
        valori = _valori_nativi(beta, voce_b.runtime_data.vmc, "master", aiutanti)
        attesi = {
            k: _initial_come_stato(config, k, "master")
            if _con_initial(config, k, "master")
            else scritti[k]
            for k in aiutanti
        }
        assert valori == attesi
        for chiave, stato_a in memorie_a.items():
            stato = beta.states.get(stato_a.entity_id)
            assert stato.state == stato_a.state, chiave


async def test_installazione_a_mano_non_si_tocca(
    hass: HomeAssistant, tmp_path: Path
) -> None:
    """Una cartella del package senza il marcatore della beta (installata a mano): non si
    tocca, la VMC nativa non parte e una riparazione (non correggibile) lo dice."""
    cartella = scrivi_package_beta(str(tmp_path), "master", "192.168.1.160")
    (cartella / passaggio.FILE_MARCATORE).unlink()
    prima = file_scritti(cartella)
    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    assert master.state is ConfigEntryState.LOADED
    assert master.runtime_data.situazione == passaggio.MANUALE
    assert master.runtime_data.vmc is None
    assert er.async_entries_for_config_entry(er.async_get(hass), master.entry_id) == []
    problema = ir.async_get(hass).async_get_issue(DOMAIN, f"{ISSUE_MANUALE}_master")
    assert problema is not None and not problema.is_fixable
    assert ir.async_get(hass).async_get_issue(DOMAIN, ISSUE_PASSAGGIO) is None
    assert file_scritti(cartella) == prima


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_valori_sconosciuti_come_dopo_un_riavvio_della_beta(
    hass: HomeAssistant, hass_storage, tmp_path: Path
) -> None:
    """Valori «unknown» e «unavailable» conservati da Home Assistant passano così come
    sono e l'entità nativa li tratta come l'aiutante della beta al riavvio (oracolo: gli
    aiutanti veri con gli stessi stati conservati). Le voci senza valore partono come in
    una VMC nuova."""
    altrove = scrivi_package_beta(str(tmp_path / "altrove"), "master", "192.168.1.160")
    config = configurazione_package([altrove])
    scelte: list[str] = []
    for dominio in (
        "input_boolean",
        "input_number",
        "input_select",
        "input_text",
        "input_datetime",
    ):
        scelte += [
            k
            for k in DOMANI
            if k.startswith(f"{dominio}.")
            and k not in INTERNI
            and DOMANI[k] != "sensor"
            and not _con_initial(config, k, "master")
        ][:2]
    scelte += [
        next(
            k
            for k in INTERNI
            if k.startswith(d) and not _con_initial(config, k, "master")
        )
        for d in ("input_number.", "input_text.")
    ]
    grezzi = {k: ("unknown", "unavailable")[i % 2] for i, k in enumerate(scelte)}
    carica_stati_conservati(
        hass,
        [State(passaggio.entity_id_di_oggi(k, "master"), v) for k, v in grezzi.items()],
    )
    letti = passaggio.leggi_valori(hass, "master")
    assert {**letti.impostazioni, **{k: grezzi[k] for k in letti.interni}} == grezzi
    assert len(letti.non_letti) == 241 - len(scelte) + 10
    await passaggio.async_salva_letti(hass, "master", letti, passaggio.CONFERMATO)

    master = voce("master")
    await aggiungi_e_avvia(hass, [master])
    assert master.runtime_data.situazione == passaggio.NATIVA
    # l'oracolo: gli aiutanti della beta con gli stessi stati conservati
    for dominio in {k.split(".", 1)[0] for k in scelte}:
        aiutanti = {
            f"vmc_master_{k.split('.', 1)[1]}": config[dominio][
                f"vmc_master_{k.split('.', 1)[1]}"
            ]
            for k in scelte
            if k.startswith(f"{dominio}.")
        }
        assert await async_setup_component(hass, dominio, {dominio: aiutanti})
    await hass.async_block_till_done()
    oracolo = {
        k: hass.states.get(passaggio.entity_id_di_oggi(k, "master")).state
        for k in scelte
    }
    assert _valori_nativi(hass, master.runtime_data.vmc, "master", scelte) == oracolo
