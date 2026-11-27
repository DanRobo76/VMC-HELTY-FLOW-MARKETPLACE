"""Banco delle prove del passaggio (fase 5): VMC finta, voci di configurazione, package
della beta caricato in Home Assistant e riavvio di Home Assistant.

Il riavvio è quello di Home Assistant: alla chiusura si prendono il registro delle entità
(``EntityRegistry._data_to_save``) e gli stati da ripristinare
(``RestoreStateData.async_get_stored_states``, quello che Home Assistant salva alla
chiusura), passati da JSON come nei loro file; la nuova istanza li carica con le sue
funzioni di caricamento (``EntityRegistry.async_load``,
``RestoreStateData._async_load_stored_states``). Gli archivi (``Store``) passano dal
``hass_storage`` delle prove, comune alle due istanze.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterable
from contextlib import ExitStack, asynccontextmanager
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

from homeassistant import loader
from homeassistant.core import CoreState, HomeAssistant, State
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import restore_state as rs
from homeassistant.helpers.json import json_bytes
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_test_home_assistant,
)

from custom_components.vmc_master.const import CONF_HOST, CONF_NOME, CONF_TITOLO, DOMAIN
from custom_components.vmc_master.nativa.client import ErroreVMC
from custom_components.vmc_master.nativa.letture import LetturaPing, LetturaVersione

IP_BASE = "192.168.1.16"


class ClientFinto:
    """La VMC finta: non risponde alle letture, i comandi si annotano."""

    istanze: list[ClientFinto] = []  # noqa: RUF012

    def __init__(self, host: str, *_args: Any, **_kwargs: Any) -> None:
        self.host = host
        self.comandi: list[str] = []
        ClientFinto.istanze.append(self)

    async def interroga(self, richiesta: str) -> str:
        raise ErroreVMC(f"VMC finta {self.host}: nessuna risposta a {richiesta}")

    async def comanda(self, comando: str) -> str:
        self.comandi.append(comando)
        return ""


def senza_rete(*, anche_il_nome: bool = True) -> ExitStack:
    """Niente rete: VMC finta, ping e versione fissi; con ``anche_il_nome`` il nome della
    VMC non si legge (la finestra «Aggiungi dispositivo» non va in rete)."""
    pila = ExitStack()
    pila.enter_context(
        patch("custom_components.vmc_master.nativa.vmc.ClientVMC", ClientFinto)
    )
    pila.enter_context(
        patch.object(
            LetturaPing, "_async_update_data", AsyncMock(return_value="OFF-Line")
        )
    )
    pila.enter_context(
        patch.object(
            LetturaVersione, "_async_update_data", AsyncMock(return_value="9.0.0b41")
        )
    )
    if anche_il_nome:
        pila.enter_context(
            patch(
                "custom_components.vmc_master.config_flow.async_nome_vmc",
                AsyncMock(return_value=None),
            )
        )
    return pila


def voce(
    nome: str, numero: int = 0, entry_id: str | None = None, **in_piu: Any
) -> MockConfigEntry:
    """La voce di configurazione della VMC ``nome`` (come la crea «Aggiungi
    integrazione»), con i dati ``in_piu`` (es. ``da_inizializzare=True``)."""
    return MockConfigEntry(
        domain=DOMAIN,
        title=f"VMC {nome}",
        unique_id=nome,
        entry_id=entry_id or f"voce_{nome}",
        data={
            CONF_NOME: nome,
            CONF_HOST: f"{IP_BASE}{numero}",
            CONF_TITOLO: f"VMC {nome}",
            **in_piu,
        },
    )


async def aggiungi_e_avvia(
    hass: HomeAssistant, voci: Iterable[MockConfigEntry]
) -> None:
    """Aggiunge le voci e avvia l'integrazione (come all'avvio di Home Assistant)."""
    for una in voci:
        una.add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()


def _da_json(dati: Any) -> Any:
    """Il passaggio da file di Home Assistant: ``json_bytes`` (orjson) e ritorno."""
    return json.loads(json_bytes(dati))


def entity_id_attesi(nome: str) -> set[str]:
    """Gli entity_id delle entità native di una VMC, come devono essere (niente «_2»): i
    136 sensori con l'entity_id di oggi; impostazioni, sensori dei timer e pulsanti con
    l'oggetto di oggi e il dominio di domani."""
    from custom_components.vmc_master.nativa.tabelle import (
        DOMANI,
        SENSORI,
    )

    attesi = {f"{k.split('.', 1)[0]}.vmc_{nome}_{k.split('.', 1)[1]}" for k in SENSORI}
    for chiave, dominio in DOMANI.items():
        if dominio not in ("interna", "tolta"):
            attesi.add(f"{dominio}.vmc_{nome}_{chiave.split('.', 1)[1]}")
    return attesi


# Le 13 automazioni del motore (nel componente automation, con gli entity_id della beta):
# la loro voce del registro è legata alla voce della VMC
AUTOMAZIONI_DEL_MOTORE = (
    "aggiorna_aria_scambiata_e_gestisci_countdown",
    "riepilogo_audio_avvio",
    "audio_allerte_e_stato",
    "riallineamento_allerte_al_riavvio",
    "countdown_attese_automazione",
    "countdown_letture_vmc",
    "registro_comandi_e_scelte",
    "rimando_della_scelta",
    "letture_ravvicinate",
    "ripartenza_della_vmc",
    "esclusivita_finestre_opzioni",
    "inizializza_tempi_di_attesa",
)


def automazioni_attese(nome: str) -> set[str]:
    """Gli entity_id delle 13 automazioni del motore della VMC."""
    return {f"automation.vmc_{nome}_{a}" for a in AUTOMAZIONI_DEL_MOTORE} | {
        f"automation.automazione_vmc_{nome}"
    }


def voci_attese(nome: str) -> set[str]:
    """Le voci del registro legate alla voce della VMC: le 367 entità native e le 13
    automazioni del motore."""
    return entity_id_attesi(nome) | automazioni_attese(nome)


def file_scritti(cartella: Path) -> dict[str, float]:
    """Tutti i file sotto ``cartella`` con l'istante dell'ultima modifica."""
    if not cartella.exists():
        return {}
    return {
        str(p.relative_to(cartella)): p.stat().st_mtime for p in cartella.rglob("*")
    }


@asynccontextmanager
async def istanza_nuova(config_dir: str) -> AsyncIterator[HomeAssistant]:
    """Un'altra istanza di Home Assistant con la stessa cartella di configurazione (e lo
    stesso ``hass_storage``), con le integrazioni personalizzate abilitate."""
    async with async_test_home_assistant(config_dir=config_dir) as nuovo:
        nuovo.data.pop(loader.DATA_CUSTOM_COMPONENTS)  # come enable_custom_integrations
        try:
            yield nuovo
        finally:
            if nuovo.state is not CoreState.not_running:  # non già chiusa da un riavvio
                await nuovo.async_stop(force=True)


@asynccontextmanager
async def riavvio(
    hass: HomeAssistant, voci: Iterable[MockConfigEntry], config_dir: str
) -> AsyncIterator[HomeAssistant]:
    """Chiude ``hass`` come Home Assistant (stati da ripristinare e registro salvati) e
    apre una nuova istanza con gli stessi dati e le stesse voci (non ancora avviate)."""
    stati = _da_json(
        [s.as_dict() for s in rs.async_get(hass).async_get_stored_states()]
    )
    registro = _da_json(er.async_get(hass)._data_to_save())
    dati_voci = [(v.entry_id, v.unique_id, dict(v.data), v.title) for v in voci]
    await hass.async_stop()
    carica_registro = er.async_load

    async def carica_registro_salvato(nuovo: HomeAssistant, **kwargs: Any) -> None:
        # Il file del registro letto dalla nuova istanza, con il caricamento di HA
        with patch.object(
            er.async_get(nuovo)._store, "async_load", AsyncMock(return_value=registro)
        ):
            await carica_registro(nuovo, **kwargs)

    pila = ExitStack()
    pila.enter_context(patch.object(er, "async_load", carica_registro_salvato))
    async with istanza_nuova(config_dir) as nuovo:
        pila.close()
        rs.async_get(nuovo)._async_load_stored_states(stati)
        for entry_id, unique_id, data, titolo in dati_voci:
            MockConfigEntry(
                domain=DOMAIN,
                title=titolo,
                unique_id=unique_id,
                entry_id=entry_id,
                data=data,
            ).add_to_hass(nuovo)
        yield nuovo


# --- il package della beta ---------------------------------------------------------------------

VERSIONE_BETA = "9.0.0b41"
DOMINI_AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_text",
    "input_select",
    "input_datetime",
    "timer",
)


def scrivi_package_beta(config_dir: str, nome: str, ip: str) -> Path:
    """La cartella che la beta scriveva per la VMC (file del package e marcatore): la
    scrive la prova, al posto della beta."""
    from custom_components.vmc_master.installatore import genera_file
    from custom_components.vmc_master.passaggio import FILE_MARCATORE

    cartella = Path(config_dir) / "packages" / "vmc_helty_flow" / nome
    cartella.mkdir(parents=True, exist_ok=True)
    for nome_file, testo in genera_file(nome, ip, VERSIONE_BETA).items():
        (cartella / nome_file).write_text(testo, encoding="utf-8")
    (cartella / FILE_MARCATORE).write_text(
        json.dumps({"versione": VERSIONE_BETA, "nome": nome, "ip": ip}),
        encoding="utf-8",
    )
    return cartella


def configurazione_package(cartelle: Iterable[Path]) -> dict[str, Any]:
    """La configurazione dei package (come Home Assistant unisce i package): aiutanti,
    timer, script, sensori template, automazioni (spente: il motore della beta non gira
    nelle prove) e sensori rest, command_line e tcp."""
    from homeassistant.util.yaml.loader import parse_yaml

    config: dict[str, Any] = {d: {} for d in (*DOMINI_AIUTANTI, "script")}
    config.update(template=[], automation=[], sensor=[], command_line=[])
    for cartella in cartelle:
        for percorso in sorted(cartella.glob("*.yaml")):
            parte = parse_yaml(percorso.read_text(encoding="utf-8"))
            for dominio in (*DOMINI_AIUTANTI, "script"):
                config[dominio].update(parte.get(dominio) or {})
            for dominio in ("template", "sensor", "command_line"):
                config[dominio].extend(parte.get(dominio) or [])
            for automazione in parte.get("automation") or []:
                config["automation"].append({**automazione, "initial_state": False})
    return config


def _senza_ora_delle_medie(blocco: dict[str, Any]) -> dict[str, Any]:
    """Il blocco delle medie (azione ``recorder.get_statistics``) senza il trigger
    ``time_pattern`` del minuto 5: senza recorder nelle prove l'azione non c'è e il blocco,
    al minuto 5 dell'orologio vero, lascia un'eccezione che fa fallire la prova solo se
    gira in quel minuto. Le medie le scrive la prova (``dai_valori_alle_memorie``); gli
    altri blocchi restano come sono."""
    azioni = blocco.get("actions") or blocco.get("action") or []
    if not any(a.get("action") == "recorder.get_statistics" for a in azioni):
        return blocco
    trigger = [
        t
        for t in blocco.get("triggers") or blocco.get("trigger") or []
        if (t.get("trigger") or t.get("platform")) != "time_pattern"
    ]
    chiave = "triggers" if "triggers" in blocco else "trigger"
    return {**blocco, chiave: trigger}


async def carica_package(
    hass: HomeAssistant,
    cartelle: Iterable[Path],
    automazioni_personali: Iterable[dict[str, Any]] = (),
    script_personali: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Carica in Home Assistant le parti del package che hanno entità: aiutanti, timer,
    script, sensori template e automazioni con le integrazioni vere; i sensori rest,
    command_line (voce nel registro) e tcp (senza unique_id) solo come stati, perché
    vanno in rete. ``automazioni_personali`` e ``script_personali``: quelli dell'utente
    (automations.yaml, scripts.yaml)."""
    config = configurazione_package(cartelle)
    if not hass.services.has_service("recorder", "get_statistics"):
        config["template"] = [_senza_ora_delle_medie(b) for b in config["template"]]
    for dominio in DOMINI_AIUTANTI:
        assert await async_setup_component(hass, dominio, {dominio: config[dominio]})
    assert await async_setup_component(
        hass, "script", {"script": {**config["script"], **(script_personali or {})}}
    )
    assert await async_setup_component(
        hass, "template", {"template": config["template"]}
    )
    assert await async_setup_component(
        hass,
        "automation",
        {"automation": [*config["automation"], *automazioni_personali]},
    )
    registro = er.async_get(hass)
    for sensore in config["sensor"]:
        entity_id = f"sensor.{sensore['name']}"
        if sensore.get("unique_id"):
            registro.async_get_or_create(
                "sensor",
                sensore["platform"],
                sensore["unique_id"],
                suggested_object_id=sensore["name"],
            )
        hass.states.async_set(entity_id, "unknown")
    for blocco in config["command_line"]:
        sensore = blocco["sensor"]
        registro.async_get_or_create(
            "sensor",
            "command_line",
            sensore["unique_id"],
            suggested_object_id=sensore["name"],
        )
        hass.states.async_set(f"sensor.{sensore['name']}", "unknown")
    await hass.async_block_till_done()
    return config


async def imposta_valori_diversi(hass: HomeAssistant, nome: str) -> dict[str, str]:
    """Scrive in ogni aiutante del package della VMC un valore diverso da quello con cui
    riparte senza valore (spento, minimo, prima opzione, vuoto, mezzanotte). Restituisce
    chiave -> stato scritto (i 241 aiutanti; i timer no)."""
    from custom_components.vmc_master.nativa.tabelle import DOMANI

    scritti: dict[str, str] = {}
    for chiave in DOMANI:
        dominio, oggetto = chiave.split(".", 1)
        entity_id = f"{dominio}.vmc_{nome}_{oggetto}"
        stato = hass.states.get(entity_id)
        if dominio in ("script", "shell_command", "timer"):
            continue
        assert stato is not None, entity_id
        bersaglio = {"entity_id": entity_id}
        if dominio == "input_boolean":
            await hass.services.async_call(dominio, "turn_on", bersaglio, blocking=True)
        elif dominio == "input_number":
            minimo, massimo = stato.attributes["min"], stato.attributes["max"]
            valore = min(minimo + stato.attributes["step"], massimo)
            await hass.services.async_call(
                dominio, "set_value", {**bersaglio, "value": valore}, blocking=True
            )
        elif dominio == "input_select":
            opzioni = stato.attributes["options"]
            await hass.services.async_call(
                dominio,
                "select_option",
                {**bersaglio, "option": opzioni[-1]},
                blocking=True,
            )
        elif dominio == "input_text":
            await hass.services.async_call(
                dominio, "set_value", {**bersaglio, "value": "x1"}, blocking=True
            )
        elif dominio == "input_datetime":
            await hass.services.async_call(
                dominio,
                "set_datetime",
                {**bersaglio, "time": "01:23:45"},
                blocking=True,
            )
        scritti[chiave] = hass.states.get(entity_id).state
    await hass.async_block_till_done()
    return scritti


async def dai_valori_alle_memorie(hass: HomeAssistant, nome: str) -> None:
    """Dà un valore ai 10 sensori con memoria del package: le 3 «ultime letture valide»
    con letture vere dei sensori tcp (una valida, una fallita, un'altra valida: il sensore
    a trigger scrive anche la lettura di prima dell'interruzione); le 7 medie dalle
    statistiche (senza recorder nelle prove) con uno stato scritto come lo scriverebbe il
    loro modello."""
    for lettura, primo, secondo in (
        ("status_ventola", "VMGO,00001,00000", "VMGO,00003,00000"),
        ("sensori", "VMGI,00215,00550", "VMGI,00221,00560"),
        ("nome", "VMNM,Prova", "VMNM,Prova 2"),
    ):
        for valore in (primo, "unavailable", secondo):
            hass.states.async_set(f"sensor.vmc_{nome}_{lettura}", valore)
            await hass.async_block_till_done()
    for oggetto, valore in (
        ("temp_interna_media_4w", "21.4"),
        ("hum_interna_media_4w", "55.1"),
        ("temp_interna_media_8w", "21.2"),
        ("hum_interna_media_8w", "56.3"),
        ("temp_interna_media_12w", "20.9"),
        ("hum_interna_media_12w", "57.0"),
        ("rischio_muffa_giorni_dati", "41.5"),
    ):
        entity_id = f"sensor.vmc_{nome}_{oggetto}"
        hass.states.async_set(entity_id, valore, hass.states.get(entity_id).attributes)
    await hass.async_block_till_done()


def stati_ripristinati_all_avvio(hass: HomeAssistant) -> None:
    """Quello che Home Assistant fa all'avvio (``_write_unavailable_states`` del registro
    delle entità): uno stato «unavailable» ripristinato per ogni voce del registro senza
    entità caricata."""
    esistenti = set(hass.states.async_entity_ids())
    for voce_registro in er.async_get(hass).entities.values():
        if voce_registro.entity_id not in esistenti and not voce_registro.disabled:
            voce_registro.write_unavailable_state(hass)


def carica_stati_conservati(hass: HomeAssistant, stati: Iterable[State]) -> None:
    """Stati conservati per il ripristino, come se letti dal file di Home Assistant."""
    adesso = dt_util.utcnow()
    rs.async_get(hass)._async_load_stored_states(
        _da_json([rs.StoredState(stato, None, adesso).as_dict() for stato in stati])
    )


async def avvia_timer(hass: HomeAssistant, nome: str, quanti: int) -> list[str]:
    """Fa partire (per un'ora) i primi ``quanti`` timer del package; ne restituisce le chiavi."""
    from custom_components.vmc_master.nativa.tabelle import DOMANI

    chiavi = [chiave for chiave in DOMANI if chiave.startswith("timer.")][:quanti]
    for chiave in chiavi:
        await hass.services.async_call(
            "timer",
            "start",
            {"entity_id": f"timer.vmc_{nome}_{chiave[6:]}", "duration": "01:00:00"},
            blocking=True,
        )
    return chiavi


async def conferma_dalla_riparazione(hass: HomeAssistant) -> dict[str, Any]:
    """Il clic dell'utente: apre la riparazione del passaggio e preme Invia (primo passo).
    Restituisce il passo che segue (il riavvio, oppure la fine)."""
    from homeassistant.components.repairs import repairs_flow_manager

    from custom_components.vmc_master import ISSUE_PASSAGGIO

    assert await async_setup_component(hass, "repairs", {})
    gestore = repairs_flow_manager(hass)
    assert gestore is not None
    passo = await gestore.async_init(DOMAIN, data={"issue_id": ISSUE_PASSAGGIO})
    assert passo["step_id"] == "conferma"
    passo = await gestore.async_configure(passo["flow_id"], {})
    await hass.async_block_till_done()
    return passo
