"""I sensori template nativi contro i sensori template di oggi: stessi cambi, stesso ordine.

Oggi i sensori calcolati della VMC sono sensori template (integrazione ``template``): ognuno
segue le entità che il suo modello ha letto l'ultima volta e si riscrive durante la
consegna dell'evento che lo fa ricalcolare; un sensore che legge un altro sensore si
ricalcola alla consegna del cambio di quello. Le automazioni vedono quindi i cambi uno alla
volta, in quest'ordine e con gli stati intermedi. Nella fase 2 ``StatoVMC`` ricalcolava
tutto insieme e scriveva i cambi in fila (altro ordine, nessuno stato intermedio): nel
simulatore lo scenario «S|CONG|0|F|-» faceva scattare due trigger dell'Automazione VMC
Master al posto di uno, con un comando in più alla VMC (a 14,05 s).

Domani i 121 sensori template sono entità dell'integrazione che si comportano come le
entità template di Home Assistant, con i modelli tradotti (sensori_template.py,
sensori_modello.py). Qui, nello stesso Home Assistant: oggi 120 sensori
template del package con i loro aiutanti (tutti tranne Velocità Registrata, che legge due
timer: qui è uno stato scritto a mano nei due lati); domani le entità di ``crea_sensori_template``
della VMC «nativa», che leggono le entità di domani (con gli stessi stati) e i valori
interni (qui stati con l'entity_id di oggi: un motore senza memoria interna). Le letture e
i sensori con memoria sono stati scritti a mano, uguali nei due lati. A ogni cambio
(letture della VMC, sensori, impostazioni) ogni sensore deve cambiare negli stessi valori,
nello stesso ordine.

L'ordine tra sensori diversi qui non si confronta: in queste prove l'orologio del ciclo è
quello vero e anche i sensori template di oggi, da soli, cambiano a volte ordine da un giro
all'altro (per esempio «Tasto Telecomando Velocità 1» e «3»). Lo confronta il simulatore,
con l'orologio virtuale (strumenti/simulatore, variante nativa4: lo scenario
«S|CONG|0|F|-» è identico al lato A).
"""

from __future__ import annotations

import csv
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    async_fire_time_changed,
)

from custom_components.vmc_master.nativa.motore.contesto import Contesto
from custom_components.vmc_master.nativa.motore.generato_fase4 import (
    sensori as codice_sensori,
)
from custom_components.vmc_master.nativa.motore.timer import TimerDelMotore
from custom_components.vmc_master.nativa.sensori_modello import SensoreModello
from custom_components.vmc_master.nativa.sensori_template import (
    AnnunciDeiTimer,
    chiave_del_sensore,
    crea_sensori_template,
)

from . import confronto as c
from .motore.traduci import RADICE

T0 = datetime(2026, 11, 25, 9, 0, 0, tzinfo=UTC)
NOME = "nativa"
AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
)
FASE_1 = RADICE / "tests/nativa/motore/aiutanti_fase1.csv"

# le letture e i sensori con memoria (oggi tcp, ping e sensori template con trigger): stati
# scritti a mano nei due lati
LETTURE = {
    "sensor.status_ventola": "VMGO,00001,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000",
    "sensor.status_ventola_memorizzata": "VMGO,00001,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000,00000",
    "sensor.sensori": "VMGI,00210,00050,00450,00600,00400,00000,00000,00000,00000,00000,00000,00000,00000,00000",
    "sensor.sensori_memorizzata": "VMGI,00210,00050,00450,00600,00400,00000,00000,00000,00000,00000,00000,00000,00000,00000",
    "sensor.status_ip": "ON-Line",
    "sensor.nome": "VMNM Master",
    "sensor.nome_memorizzata": "VMNM Master",
    "sensor.lan": "VMSL,192,168,1,160",
    # il sensore che legge due timer del motore: qui uno stato scritto a mano (i timer del
    # motore e i loro annunci sono nelle prove del simulatore)
    "sensor.velocita_registrata": "Nessuna",
}


def _per_sensore(voci: list[tuple[str, str]]) -> dict[str, list[str]]:
    """I cambi di ogni sensore, in ordine."""
    uscita: dict[str, list[str]] = {}
    for chiave, stato in voci:
        uscita.setdefault(chiave, []).append(stato)
    return uscita


def _domani() -> dict[str, str]:
    """Colonna «Domani» della fase 1: aiutante di oggi -> entità di domani (o «interna»)."""
    with FASE_1.open(encoding="utf-8-sig", newline="") as f:
        return {r["Entità oggi"]: r["Domani"] for r in csv.DictReader(f, delimiter=";")}


def _di_domani(entity_id: str, domani: dict[str, str]) -> str:
    """L'entity_id che legge il sensore nativo della VMC «nativa» al posto di quello di oggi."""
    nuovo = domani.get(entity_id, entity_id)
    if nuovo.startswith("interna"):
        nuovo = entity_id  # i valori interni tengono l'entity_id di oggi
    return nuovo.replace("vmc_master_", f"vmc_{NOME}_", 1)


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_sensori_template_nello_stesso_ordine_di_oggi(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Letture, sensori e impostazioni che cambiano: stessi cambi, nello stesso ordine."""
    freezer.move_to(T0)
    assert await async_setup_component(hass, "homeassistant", {})
    # il sensore «Versione» tradotto scrive la versione dell'integrazione (manifest.json),
    # come il package che l'integrazione genera
    pacchetto = c.package()
    domani = _domani()
    # oggi: gli aiutanti del package e i sensori template che domani sono nativi
    for dominio in AIUTANTI:
        assert await async_setup_component(
            hass, dominio, {dominio: pacchetto.get(dominio) or {}}
        )
    contesto = Contesto(hass, NOME)
    contesto.timer = TimerDelMotore(contesto, {})
    sensori, binari = crea_sensori_template(hass, contesto, codice_sensori, c.IP)
    chiavi = {chiave_del_sensore(e.entity_id, NOME) for e in (*sensori, *binari)}
    assert len(chiavi) == 121
    chiavi.discard("sensor.velocita_registrata")
    sensori = [e for e in sensori if chiave_del_sensore(e.entity_id, NOME) in chiavi]
    template = [
        {dominio: [s]}
        for b in pacchetto["template"]
        if "triggers" not in b
        for dominio in ("sensor", "binary_sensor")
        for s in b.get(dominio) or []
        if s["default_entity_id"].replace("vmc_master_", "", 1) in chiavi
    ]
    assert len(template) == 120

    async def passo() -> None:
        """Fine di un passo: anche i modelli con un limite di frequenza (che Home Assistant
        rende più tardi, con un timer) si rendono adesso, nei due lati."""
        await hass.async_block_till_done()
        freezer.tick(timedelta(seconds=5))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    def scrivi_letture(valori: dict[str, str]) -> None:
        for chiave, valore in valori.items():
            dominio, oggetto = chiave.split(".", 1)
            for nome in ("master", NOME):
                hass.states.async_set(f"{dominio}.vmc_{nome}_{oggetto}", valore)

    def copia_aiutanti() -> None:
        """Domani gli stessi stati degli aiutanti di oggi, con gli entity_id di domani."""
        for dominio in AIUTANTI:
            for stato in hass.states.async_all(dominio):
                if "vmc_master_" in stato.entity_id:
                    hass.states.async_set(
                        _di_domani(stato.entity_id, domani),
                        stato.state,
                        dict(stato.attributes),
                    )

    scrivi_letture(LETTURE)
    copia_aiutanti()
    await hass.async_block_till_done()
    assert await async_setup_component(hass, "template", {"template": template})
    await hass.async_block_till_done()
    for dominio, entita in (("sensor", sensori), ("binary_sensor", binari)):
        await MockEntityPlatform(
            hass, domain=dominio, platform_name="vmc_master"
        ).async_add_entities(entita)
    await passo()
    # all'avvio i sensori dei due lati hanno gli stessi stati
    for entita in (*sensori, *binari):
        oggi = hass.states.get(entita.entity_id.replace(f"vmc_{NOME}_", "vmc_master_"))
        assert oggi is not None
        assert hass.states.get(entita.entity_id).state == oggi.state, entita.entity_id

    calcolati = {
        f"{k.split('.')[0]}.vmc_{n}_{k.split('.', 1)[1]}"
        for k in chiavi
        for n in ("master", NOME)
    }
    visti: dict[str, list[tuple[str, str]]] = {"master": [], NOME: []}

    @callback
    def annota(evento: Event) -> None:
        entity_id = evento.data["entity_id"]
        if entity_id not in calcolati:
            return
        lato = "master" if "vmc_master_" in entity_id else NOME
        chiave = entity_id.replace(f"vmc_{lato}_", "")
        visti[lato].append((chiave, evento.data["new_state"].state))

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota)

    async def cambia_aiutante(
        dominio: str, servizio: str, dati: dict[str, Any]
    ) -> None:
        await hass.services.async_call(dominio, servizio, dati, blocking=True)
        copia_aiutanti()
        await passo()

    # la VMC passa alla velocità 3, poi alla 0 (lettura e sensore con memoria)
    for codice in ("00003", "00000"):
        valore = LETTURE["sensor.status_ventola"].replace("00001", codice, 1)
        scrivi_letture(
            {
                "sensor.status_ventola": valore,
                "sensor.status_ventola_memorizzata": valore,
            }
        )
        await passo()
    # fuori -20 °C (congelamento), poi di nuovo 5 °C
    for esterna in ("-0200", "00050"):
        valore = LETTURE["sensor.sensori"].replace("00050", esterna, 1)
        scrivi_letture({"sensor.sensori": valore, "sensor.sensori_memorizzata": valore})
        await passo()
    # la VMC non risponde, poi torna
    for ip in ("OFF-Line", "ON-Line"):
        scrivi_letture({"sensor.status_ip": ip})
        await passo()
    # un'impostazione e una spia
    await cambia_aiutante(
        "input_select",
        "select_option",
        {
            "entity_id": "input_select.vmc_master_speed_1_fascia_calendario",
            "option": "Velocità 3",
        },
    )
    await cambia_aiutante(
        "input_boolean",
        "toggle",
        {"entity_id": "input_boolean.vmc_master_spia_velocita_1"},
    )
    assert len(visti["master"]) > 20
    # per ogni sensore gli stessi cambi, nello stesso ordine
    assert _per_sensore(visti[NOME]) == _per_sensore(visti["master"])


async def test_un_timer_del_motore_letto_da_un_sensore_template(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Oggi un sensore template che legge un timer si ricalcola a ogni suo cambio; domani
    il timer è del motore: la lettura si annota nel RenderInfo e AnnunciDeiTimer
    consegna i suoi cambi. Stessi cambi del sensore, negli stessi passi."""
    freezer.move_to(T0)
    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(
        hass, "timer", {"timer": {"vmc_master_prova": {"duration": 10}}}
    )
    sorgente = "{{ states('timer.vmc_master_prova') }}"
    assert await async_setup_component(
        hass,
        "template",
        {
            "template": [
                {
                    "sensor": [
                        {
                            "default_entity_id": "sensor.vmc_master_legge_timer",
                            "name": "Legge timer",
                            "state": sorgente,
                        }
                    ]
                }
            ]
        },
    )
    contesto = Contesto(hass, NOME)
    timer = TimerDelMotore(contesto, {f"vmc_{NOME}_prova": {"duration": 10}})
    contesto.timer = timer
    await timer.prepara()
    annunci = AnnunciDeiTimer(hass, timer)

    def modello(c: Contesto, variabili: Any) -> str:
        return c.timer.states(c.N("timer.vmc_master_prova"))

    nativo = SensoreModello(
        hass,
        {
            "default_entity_id": f"sensor.vmc_{NOME}_legge_timer",
            "name": contesto.statico("Legge timer"),
            "state": contesto.modello(modello, sorgente),
        },
        None,
    )
    await MockEntityPlatform(
        hass, domain="sensor", platform_name="vmc_master"
    ).async_add_entities([nativo])
    await hass.async_block_till_done()
    visti: dict[str, list[tuple[int, str]]] = {"master": [], NOME: []}
    passo = 0

    @callback
    def annota(evento: Event) -> None:
        entity_id = evento.data["entity_id"]
        if entity_id.endswith("_legge_timer"):
            lato = "master" if "vmc_master_" in entity_id else NOME
            visti[lato].append((passo, evento.data["new_state"].state))

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota)
    for passo, (servizio, secondi) in enumerate(
        (("start", 0), (None, 4), ("pause", 0), ("start", 0), (None, 11))
    ):
        if servizio is not None:
            await hass.services.async_call(
                "timer",
                servizio,
                {"entity_id": "timer.vmc_master_prova"},
                blocking=True,
            )
            await timer.servizio(
                servizio, {}, {"entity_id": f"timer.vmc_{NOME}_prova"}, None
            )
        freezer.tick(timedelta(seconds=secondi))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()
    annunci.ferma()
    timer.ferma()
    assert visti["master"] == [
        (0, "active"),
        (2, "paused"),
        (3, "active"),
        (4, "idle"),
    ]
    assert visti[NOME] == visti["master"]
