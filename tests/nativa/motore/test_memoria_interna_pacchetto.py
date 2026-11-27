"""Banco casuale del package intero con la memoria interna (fase 4).

Lo stesso banco di ``test_pacchetto_casuale`` (stessa sequenza casuale, stesso ciclo
degli eventi deterministico, stesse entità di comodo e servizi finti), con una
differenza: da una parte Home Assistant con le integrazioni ``automation`` e ``script`` e
tutti gli aiutanti del package; dall'altra il motore tradotto CON i valori interni
(``traduci(..., interni=INTERNI)``) e la memoria interna al posto dei 67 aiutanti
interni, che non ci sono più nella macchina degli stati.

La scheda non tocca i valori interni (non sono più entità): il generatore li toglie dai
passi della scheda. Si confronta ogni evento osservabile (registro completo, con istanti
e contesti, chiamate ai servizi finti, notifiche, fine delle chiamate del banco, stati
finali), tranne quelli che con la memoria non ci sono più (``banco_memoria``):

- ``state_changed`` dei valori interni: uguali ai cambi della memoria;
- ``call_service`` delle scritture con soli valori interni: uguali alle chiamate alla
  memoria;
- ``state_reported`` dei valori interni: uguali a quelli della memoria (quelli di
  ``homeassistant.update_entity`` li manda il motore, che riscrive i valori interni nel
  loro turno; contati);
- ``homeassistant.update_entity``: senza i valori interni tra le entità (contati).

Anche l'ordine di tutto insieme (``sequenza``) è lo stesso. Lo stato finale dei valori
interni nella memoria è quello degli aiutanti (stato, attributi, last_changed,
last_updated, last_reported).

Le automazioni del motore sono logiche dell'integrazione (``fase3.MotoreFase3``: gli
script restano entità ``script``): i loro stati entrano nel registro nel punto del bus
dei loro state_changed (``fase3.osserva_logiche``), senza ``automation_triggered``, e un
ciclo senza fine ferma la corsa (come in ``test_pacchetto_casuale``).

Con il riavvio la prima parte finisce con la chiusura di Home Assistant
(``hass.async_stop()``, con le esecuzioni in corso) e la seconda riparte da quello che
è stato salvato: con gli aiutanti gli stati salvati da ``restore_state`` alla chiusura,
con la memoria l'archivio della memoria (``MemoriaInterna.async_carica``) e gli stati
delle altre entità. I salvataggi si confrontano (i valori interni salvati dalla memoria
sono quelli che Home Assistant salva per gli aiutanti). Le logiche non hanno stati
salvati (le automazioni di Home Assistant sì, con ``last_triggered``): la seconda parte
di Home Assistant riparte senza gli stati salvati delle automazioni, come le logiche.

    VMC_PASSI_MEMORIA=2000 VMC_SEME_MEMORIA=7 pytest \\
        tests/nativa/motore/test_memoria_interna_pacchetto.py -s
"""

from __future__ import annotations

import asyncio
import difflib
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.components import persistent_notification as pn
from homeassistant.components.homeassistant.services import SCHEMA_UPDATE_ENTITY
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
    EVENT_STATE_REPORTED,
    MATCH_ALL,
)
from homeassistant.core import (
    Context,
    CoreState,
    Event,
    ServiceCall,
    ServiceResponse,
    State,
    SupportsResponse,
    callback,
)
from homeassistant.core_config import _CUSTOMIZE_CONFIG_SCHEMA, DATA_CUSTOMIZE
from homeassistant.helpers import restore_state
from homeassistant.helpers.entity_component import async_update_entity
from homeassistant.helpers.entity_values import EntityValues
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.json import JSONEncoder, json_dumps
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_test_home_assistant

from custom_components.vmc_master.const import NOME_MASTER
from custom_components.vmc_master.nativa.motore import generato
from custom_components.vmc_master.nativa.motore.memoria_interna import (
    CHIAVE_ARCHIVIO,
    INTERNI,
    VERSIONE_ARCHIVIO,
    MemoriaInterna,
    da_stato,
)
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche

from . import test_pacchetto_casuale as casuale
from .banco_memoria import (
    AGGIORNA,
    Smistatore,
    entita_scritte,
    modelli_entita_con_memoria,
    servizi_misti,
)
from .fase3 import MotoreFase3, osserva_logiche, personalizzato
from .test_memoria_interna import IDS
from .test_pacchetto_casuale import (
    AIUTANTI,
    DI_COMODO,
    ESTERNE,
    FINTI,
    LETTORI,
    LETTURE,
    METEO,
    SENSORI,
    STATO,
    VELOCITA,
    CicloInfinito,
    Generatore,
    Normalizzatore,
    Prova,
    Ritmo,
    VmcFinta,
    _avanza,
    _confronta,
    _lavora,
    _package,
)
from .test_semantica import _carica, _gira
from .traduci import (
    GENERATO,
    contenuto,
    leggi_comandi,
    leggi_package,
    traduci,
    traduci_configurazione,
)

VMC_PASSI_MEMORIA = int(os.environ.get("VMC_PASSI_MEMORIA", "300"))
VMC_SEME_MEMORIA = int(os.environ.get("VMC_SEME_MEMORIA", "1"))
CHIAVE = CHIAVE_ARCHIVIO.format(nome=NOME_MASTER)
DOMINI_INTERNI = ("input_boolean", "input_number", "input_text")
# I sensori modello del package che leggono valori interni (domani sensori nativi sullo
# StatoVMC): nel banco li leggono dalla memoria (dalla b46 non il sensore di verifica del
# campo «Cambia IP VMC»: il suo valore di esito non è più un valore interno, è tolto).
SENSORI_CON_INTERNI = [
    "sensor.vmc_master_velocita_registrata",
    "sensor.vmc_master_status_calcolo_aria_scambiata_totale",
    "sensor.vmc_master_tempo_mancante_ricambio",
    "binary_sensor.vmc_master_black_out_rilevato",
]
# Secondi tra la chiusura e la riapertura di Home Assistant nelle prove con riavvio.
PAUSA_RIAVVIO = 30


class GeneratoreSenzaInterni(Generatore):
    """Il generatore del banco casuale senza i valori interni tra quelli che la scheda
    può toccare (gli stati ripristinati all'avvio restano tutti)."""

    def __init__(self, seme: int) -> None:
        super().__init__(seme)
        interni = set(IDS)

        def fuori(dominio: str, nomi: list[str]) -> list[str]:
            return [n for n in nomi if f"{dominio}.{n}" not in interni]

        self.booleani = fuori("input_boolean", self.booleani)
        self.opzioni = fuori("input_boolean", self.opzioni)
        self.numeri = fuori("input_number", self.numeri)
        self.testi = fuori("input_text", self.testi)


# --- il motore tradotto con i valori interni ---------------------------------------------

_TRADOTTO: dict[str, ModuleType] = {}


async def _motore_con_interni() -> ModuleType:
    """Il package tradotto con ``interni=INTERNI`` (una volta per processo, prima delle
    corse: un'altra istanza di Home Assistant di prova, alla fine, rimette il fuso orario
    predefinito).

    I moduli sono quelli di ``generato/`` tranne ``motore.py``, che in più dichiara i
    valori interni: il ``motore.py`` tradotto si carica accanto agli altri moduli di
    ``generato/``."""
    if (modulo := _TRADOTTO.get("motore")) is not None:
        return modulo
    async with async_test_home_assistant() as hass:
        moduli = await traduci(hass, interni=INTERNI)
        await hass.async_stop(force=True)
    diversi = [
        nome
        for nome, testo in moduli.items()
        if contenuto((GENERATO / nome).read_text(encoding="utf-8")) != contenuto(testo)
    ]
    assert diversi == ["motore.py"], diversi
    oggi = (GENERATO / "motore.py").read_text(encoding="utf-8").splitlines()
    righe = moduli["motore.py"].splitlines()
    modifiche = difflib.SequenceMatcher(None, oggi, righe, autojunk=False).get_opcodes()
    aggiunte = [righe[j1:j2] for tag, _, _, j1, j2 in modifiche if tag != "equal"]
    assert all(tag == "insert" for tag, *_ in modifiche if tag != "equal")
    assert aggiunte == [
        [
            "# i valori interni (fase 4): nella memoria interna del motore",
            "INTERNI = (",
            *(f"    {chiave!r}," for chiave in INTERNI),
            ")",
            "",
            "",
        ],
        ["    c.memoria_interna(INTERNI)"],
    ], aggiunte
    _TRADOTTO["motore"] = modulo = _carica("motore_con_interni", moduli["motore.py"])
    return modulo


# --- una corsa ---------------------------------------------------------------------------


def _salvati_da_stati(stati: list[State], adesso: datetime) -> list[dict[str, Any]]:
    """Gli stati come li salva ``restore_state`` (senza dati aggiuntivi)."""
    return [
        {
            "state": json.loads(json.dumps(stato.as_dict(), cls=JSONEncoder)),
            "last_seen": adesso.isoformat(),
        }
        for stato in stati
    ]


def _archivio(valori: dict[str, Any]) -> dict[str, Any]:
    """L'archivio della memoria come lo scrive ``Store``."""
    return {
        "version": VERSIONE_ARCHIVIO,
        "minor_version": 1,
        "key": CHIAVE,
        "data": {"valori": valori},
    }


async def _corsa(
    freezer: FrozenDateTimeFactory,
    prova: Prova,
    *,
    motore: bool,
    archivio: dict[str, Any],
    salvati: list[dict[str, Any]] | None = None,
    riavvio: bool = False,
) -> dict[str, Any]:
    """Una corsa come ``test_pacchetto_casuale._corsa`` (stesso ciclo deterministico),
    con ``_corsa_ciclo`` di qui."""

    async def ciclo(
        freezer: FrozenDateTimeFactory,
        prova: Prova,
        *,
        motore: bool,
        **_altre: Any,
    ) -> dict[str, Any]:
        return await _corsa_ciclo(
            freezer,
            prova,
            motore=motore,
            archivio=archivio,
            salvati=salvati,
            riavvio=riavvio,
        )

    with patch.object(casuale, "_corsa_ciclo", ciclo):
        return await casuale._corsa(freezer, prova, motore=motore)


async def _corsa_ciclo(
    freezer: FrozenDateTimeFactory,
    prova: Prova,
    *,
    motore: bool,
    archivio: dict[str, Any],
    salvati: list[dict[str, Any]] | None,
    riavvio: bool,
) -> dict[str, Any]:
    """``test_pacchetto_casuale._corsa_ciclo`` con la memoria interna nella corsa del
    motore.

    ``salvati``: gli stati salvati alla chiusura precedente (con il riavvio), altrimenti
    quelli di ``prova.ripristino``; con la memoria i valori interni vengono dal suo
    archivio (``archivio``, il ``hass_storage`` della prova). ``riavvio``: la corsa
    finisce chiudendo Home Assistant (senza spegnere prima automazioni e script) e
    restituisce quello che è stato salvato."""
    freezer.move_to(prova.inizio)
    norma = Normalizzatore(prova.inizio)
    pkg = _package()
    vmc = VmcFinta(**vars(prova.vmc))
    ritmo = Ritmo()
    smistatore = Smistatore(IDS, norma, ritmo.conta)
    interni = set(IDS)
    chiamate: list[Any] = []
    notifiche: list[Any] = []
    fine_chiamate: list[Any] = []
    esito: dict[str, Any] = {
        "registro": smistatore.registro,
        "interni": smistatore.interni_cambi,
        "chiamate_interne": smistatore.chiamate_interne,
        "rapporti": smistatore.interni_rapporti,
        "da_aggiornamento": smistatore.rapporti_da_aggiornamento,
        "sequenza": smistatore.sequenza,
        "chiamate": chiamate,
        "notifiche": notifiche,
        "fine_chiamate": fine_chiamate,
    }
    annota_attivo = False
    if salvati is None:
        salvati = _salvati_da_stati(prova.ripristino, prova.inizio)
    memoria: MemoriaInterna | None = None
    m: MotoreFase3 | None = None

    async with async_test_home_assistant(initial_state=CoreState.not_running) as hass:
        hass.import_executor = casuale.EsecutoreSincrono()
        await hass.config.async_set_time_zone(str(casuale.FUSO))
        restore_state.async_get(hass)._async_load_stored_states(
            [v for v in salvati if not motore or v["state"]["entity_id"] not in interni]
        )
        hass.data[DATA_CUSTOMIZE] = EntityValues(
            _CUSTOMIZE_CONFIG_SCHEMA(pkg["homeassistant"])["customize"], {}, {}
        )
        utente = await hass.auth.async_create_user("Utente scheda")

        @callback
        def annota(evento: Event) -> None:
            # automation_triggered: solo con Home Assistant (le logiche non lo hanno)
            if annota_attivo and evento.event_type != "automation_triggered":
                smistatore.evento(evento)

        @callback
        def rapporto(evento: Event) -> None:
            if annota_attivo:
                smistatore.rapporto(evento)

        hass.bus.async_listen(MATCH_ALL, annota)
        smetti = osserva_logiche(hass, annota) if motore else None
        hass.bus.async_listen(
            EVENT_STATE_REPORTED,
            rapporto,
            event_filter=callback(lambda dati: dati["entity_id"] in interni),
        )
        assert await async_setup_component(hass, "homeassistant", {})
        assert await async_setup_component(hass, "persistent_notification", {})
        for dominio in AIUTANTI:
            voci = pkg[dominio]
            if motore and dominio in DOMINI_INTERNI:
                voci = {
                    o: v for o, v in voci.items() if f"{dominio}.{o}" not in interni
                }
            assert await async_setup_component(hass, dominio, {dominio: voci})
        if motore:
            memoria = MemoriaInterna(hass, NOME_MASTER)
            await memoria.async_carica()
            memoria.ascolta_cambi(
                lambda evento: smistatore.cambio(evento) if annota_attivo else None
            )
            memoria.ascolta_chiamate(
                lambda *voce: smistatore.chiamata(*voce) if annota_attivo else None
            )
            servizi_misti(
                hass, memoria, [f"input_boolean.{o}" for o in pkg["input_boolean"]]
            )

        @callback
        def notificato(tipo: Any, voci: dict[str, Any]) -> None:
            notifiche.append(
                (
                    norma(dt_util.utcnow()),
                    str(tipo),
                    norma({k: dict(v) for k, v in voci.items()}),
                )
            )

        pn.async_register_callback(hass, notificato)

        def annota_chiamata(chiamata: ServiceCall) -> None:
            chiamate.append(
                (
                    norma(dt_util.utcnow()),
                    chiamata.domain,
                    chiamata.service,
                    norma(dict(chiamata.data)),
                    norma(chiamata.context),
                )
            )

        def leggi(entita: str) -> None:
            hass.states.async_set(
                entita, vmc.lettura(entita), {"friendly_name": entita}
            )

        async def finto(chiamata: ServiceCall) -> None:
            annota_chiamata(chiamata)

        async def comando(chiamata: ServiceCall) -> None:
            annota_chiamata(chiamata)
            codice = VELOCITA.get(chiamata.service)
            if not vmc.accesa:
                await asyncio.sleep(3)
                return
            await asyncio.sleep(0.05)
            if codice is not None:

                def applica() -> None:
                    if vmc.accesa:
                        vmc.velocita = codice

                hass.loop.call_later(0.5, applica)

        aggiorna_entita = smistatore.segna_aggiornamenti(async_update_entity)

        async def aggiorna_una(entita: str) -> None:
            if entita in DI_COMODO:
                leggi(entita)
            else:
                await aggiorna_entita(hass, entita)

        async def aggiorna(chiamata: ServiceCall) -> None:
            # come il servizio di Home Assistant: ogni entità in un compito suo, creati
            # in fila (asyncio.gather)
            annota_chiamata(chiamata)
            await asyncio.gather(*(aggiorna_una(e) for e in chiamata.data["entity_id"]))

        async def statistiche(chiamata: ServiceCall) -> ServiceResponse:
            annota_chiamata(chiamata)
            return {"statistics": {}}

        for nome in pkg["shell_command"]:
            hass.services.async_register("shell_command", nome, comando)
        for dominio, servizio in FINTI:
            hass.services.async_register(dominio, servizio, finto)
        hass.services.async_register(
            "homeassistant", "update_entity", aggiorna, schema=SCHEMA_UPDATE_ENTITY
        )
        hass.services.async_register(
            "recorder",
            "get_statistics",
            statistiche,
            supports_response=SupportsResponse.ONLY,
        )
        for entita in DI_COMODO:
            leggi(entita)
        for entita, attributi in ESTERNE.items():
            hass.states.async_set(entita, "20", attributi)
        hass.states.async_set(METEO, "sunny", {"temperature": 12.5, "humidity": 60})
        for entita in LETTORI:
            hass.states.async_set(entita, "idle")
        for entita, secondi in LETTURE.items():
            async_track_time_interval(
                hass,
                lambda _istante, entita=entita: leggi(entita),
                timedelta(seconds=secondi),
                cancel_on_shutdown=True,
            )
        assert await async_setup_component(
            hass, "template", {"template": pkg["template"]}
        )
        await hass.async_block_till_done()
        if memoria is not None:
            toccati = modelli_entita_con_memoria(hass, memoria)
            assert toccati == SENSORI_CON_INTERNI
            m = MotoreFase3(hass, memoria=memoria)
            await m.avvia(crea=_TRADOTTO["motore"].crea)
        else:
            assert await async_setup_component(
                hass, "script", {"script": pkg["script"]}
            )
            assert await async_setup_component(
                hass, "automation", {"automation": pkg["automation"]}
            )
        await hass.async_block_till_done()

        # quello che restore_state salva alla chiusura (async_setup_dump, spento nei
        # test); senza l'id del registro delle entità, che nella corsa dopo è un altro
        @callback
        def salva_alla_chiusura(_evento: Event) -> None:
            salvati = []
            for s in restore_state.async_get(hass).async_get_stored_states():
                voce = json.loads(json_dumps(s.as_dict()))
                del voce["entity_registry_id"]
                salvati.append(voce)
            esito["salvati"] = salvati
            esito["salvati_confronto"] = [
                (
                    v["state"]["entity_id"],
                    v["state"]["state"],
                    norma(v["state"]["attributes"]),
                    v["state"]["last_changed"],
                    v["state"]["last_updated"],
                    v["extra_data"],
                    v["last_seen"],
                )
                for v in salvati
            ]

        annota_attivo = True
        compiti: list[asyncio.Future[Any]] = []
        esito["fermate"] = 0
        esito["cicli_infiniti"] = []

        async def _chiama(
            indice: int, dominio: str, servizio: str, dati: Any, con_utente: bool
        ) -> None:
            contesto = Context(user_id=utente.id if con_utente else None)
            try:
                await hass.services.async_call(
                    dominio, servizio, dati, blocking=True, context=contesto
                )
            except BaseException as err:
                fine_chiamate.append(
                    (norma(dt_util.utcnow()), indice, type(err).__name__)
                )
                if isinstance(err, asyncio.CancelledError):
                    raise
                return
            fine_chiamate.append((norma(dt_util.utcnow()), indice))

        async def passo_singolo(indice: int, passo: tuple[Any, ...]) -> None:
            tipo = passo[0]
            if tipo == "attendi":
                esito["fermate"] += await _avanza(hass, freezer, passo[1], ritmo)
                return
            if tipo == "servizio":
                _, dominio, servizio, dati = passo
                try:
                    await hass.services.async_call(
                        dominio,
                        servizio,
                        dati,
                        blocking=True,
                        context=Context(user_id=utente.id),
                    )
                except Exception as err:  # noqa: BLE001
                    smistatore.nota(
                        (norma(dt_util.utcnow()), "errore", indice, repr(err))
                    )
            elif tipo == "chiama":
                _, dominio, servizio, dati, con_utente = passo
                compiti.append(
                    asyncio.ensure_future(
                        _chiama(indice, dominio, servizio, dati, con_utente)
                    )
                )
            elif tipo == "raffica":
                for dominio, servizio, dati in passo[1]:
                    compiti.append(
                        asyncio.ensure_future(
                            _chiama(indice, dominio, servizio, dati, True)
                        )
                    )
            elif tipo == "lettura":
                _, entita, stato, attributi = passo
                hass.states.async_set(entita, stato, attributi)
            elif tipo == "vmc":
                _, campo, valore = passo
                if campo == "leggi":
                    leggi(valore)
                elif campo == "velocita":
                    if vmc.accesa:
                        vmc.velocita = valore
                        leggi(STATO)
                elif campo == "accesa":
                    if valore and not vmc.accesa and vmc.velocita != 0:
                        vmc.velocita = 1
                    vmc.accesa = valore
                else:
                    vmc.disturbo = valore
            elif tipo == "ambiente":
                _, campo, valore, subito = passo
                setattr(vmc, campo, valore)
                if subito:
                    leggi(SENSORI)
            await _lavora(hass, ritmo)

        async def esegui() -> None:
            smistatore.nota(("avvio",))
            avvio = asyncio.ensure_future(hass.async_start())
            while not avvio.done():
                await _avanza(hass, freezer, 100_000, ritmo)
            smistatore.nota(("avviato",))
            hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, salva_alla_chiusura)
            for indice, passo in enumerate(prova.passi):
                await passo_singolo(indice, passo)
            if riavvio:
                # Home Assistant si chiude con le esecuzioni in corso
                smistatore.nota(("chiusura",))
                fermata = asyncio.ensure_future(hass.async_stop())
                while not fermata.done():
                    await _avanza(hass, freezer, 100_000, ritmo)
                smistatore.nota(("chiuso",))
            else:
                esito["fermate"] += await _avanza(hass, freezer, 60_000_000, ritmo)

        try:
            await esegui()
        except CicloInfinito:
            esito["cicli_infiniti"].append(norma(ritmo.istante))
            esito["corsa_interrotta"] = norma(ritmo.istante)
            smistatore.nota((norma(ritmo.istante), "corsa interrotta", ritmo.eventi))
        smistatore.nota(("fine",))
        annota_attivo = False

        def voce(s: State) -> Any:
            return (
                s.entity_id,
                s.state,
                norma(dict(s.attributes)),
                norma(s.last_changed),
                norma(s.last_updated),
            )

        stati = hass.states.async_all()
        logiche = [
            s
            for s in (personalizzato(hass, v) for v in stati_logiche(hass).stati.values())
            if s is not None
        ]
        esito["stati"] = sorted(
            voce(s)[:4] for s in [*stati, *logiche] if s.entity_id not in interni
        )
        finali_interni = (
            [memoria.stato(e) for e in IDS]
            if memoria is not None
            else [hass.states.get(e) for e in IDS]
        )
        if memoria is not None:
            assert not any(s.entity_id in interni for s in stati)
        esito["stati_interni"] = [voce(s) for s in finali_interni if s is not None]
        esito["riportati"] = {
            s.entity_id: norma(s.last_reported) for s in finali_interni if s is not None
        }
        esito["automazioni_script"] = [
            v for v in esito["stati"] if v[0].startswith(("automation.", "script."))
        ]
        esito["notifiche_finali"] = norma(
            {k: dict(v) for k, v in pn._async_get_or_create_notifications(hass).items()}
        )
        esito["vmc"] = dict(vars(vmc))
        esito["update_senza_interni"] = smistatore.update_senza_interni
        if smetti is not None:
            smetti()
        if not riavvio:
            if m is not None:
                await m.ferma()
            else:
                await hass.services.async_call(
                    "automation", "turn_off", {"entity_id": "all"}, blocking=True
                )
            await hass.services.async_call(
                "script", "turn_off", {"entity_id": "all"}, blocking=True
            )
            await hass.services.async_call(
                "timer", "cancel", {"entity_id": "all"}, blocking=True
            )
            await _gira(hass)
            await hass.async_stop(force=True)
        freezer.tick(timedelta(seconds=61))
        await _gira(hass)
        esito["fine"] = dt_util.utcnow()
        for compito in compiti:
            if not compito.done():
                compito.cancel()
        await asyncio.gather(*compiti, return_exceptions=True)
        if memoria is not None:
            memoria.ferma()
    return esito


# --- confronto ---------------------------------------------------------------------------


def _senza_interni_in_chiamate(chiamate: list[Any]) -> tuple[list[Any], int]:
    """Le chiamate ai servizi finti di Home Assistant come le fa il motore con la
    memoria: ``homeassistant.update_entity`` senza i valori interni. Restituisce anche
    quante chiamate cambiano."""
    interni = set(IDS)
    nuove = []
    cambiate = 0
    for voce in chiamate:
        if (voce[1], voce[2]) == AGGIORNA:
            entita = entita_scritte(voce[3].get("entity_id")) or []
            if any(e in interni for e in entita):
                cambiate += 1
                voce = (
                    voce[0],
                    voce[1],
                    voce[2],
                    {**voce[3], "entity_id": [e for e in entita if e not in interni]},
                    voce[4],
                )
        nuove.append(voce)
    return nuove, cambiate


def _confronta_corse(
    atteso: dict[str, Any], ottenuto: dict[str, Any], cosa: str
) -> dict[str, int]:
    """Home Assistant con gli aiutanti e motore con la memoria; restituisce i conteggi
    di quello che con la memoria non c'è più (con ``VMC_DEBUG_MEMORIA=<cartella>`` le
    due sequenze si scrivono in ``ha.txt`` e ``motore.txt``)."""
    chiamate_attese, update_cambiati = _senza_interni_in_chiamate(atteso["chiamate"])
    if cartella := os.environ.get("VMC_DEBUG_MEMORIA"):
        for nome, esito in (("ha", atteso), ("motore", ottenuto)):
            Path(cartella, f"{nome}.txt").write_text(
                "\n".join(repr(v) for v in esito["sequenza"]), encoding="utf-8"
            )
    for voce, a, o in (
        ("chiamate ai servizi finti", chiamate_attese, ottenuto["chiamate"]),
        ("cambi dei valori interni", atteso["interni"], ottenuto["interni"]),
        (
            "chiamate ai valori interni",
            atteso["chiamate_interne"],
            ottenuto["chiamate_interne"],
        ),
        ("state_reported dei valori interni", atteso["rapporti"], ottenuto["rapporti"]),
        (
            "stati di automazioni e script",
            atteso["automazioni_script"],
            ottenuto["automazioni_script"],
        ),
        ("notifiche persistenti", atteso["notifiche"], ottenuto["notifiche"]),
        (
            "fine delle chiamate del banco",
            atteso["fine_chiamate"],
            ottenuto["fine_chiamate"],
        ),
        ("stati finali", atteso["stati"], ottenuto["stati"]),
        (
            "stati finali dei valori interni",
            atteso["stati_interni"],
            ottenuto["stati_interni"],
        ),
        ("registri", atteso["registro"], ottenuto["registro"]),
        ("sequenze", atteso["sequenza"], ottenuto["sequenza"]),
    ):
        if differenza := _confronta(a, o, voce):
            pytest.fail(f"{cosa}: {differenza}")
    # i state_reported di update_entity sui valori interni: con la memoria li manda il
    # motore (non async_update_entity), confrontati con gli altri «rapporti»
    assert not ottenuto["da_aggiornamento"]
    riportati_diversi = sorted(
        e for e, r in atteso["riportati"].items() if ottenuto["riportati"].get(e) != r
    )
    assert not riportati_diversi, riportati_diversi
    assert ottenuto["notifiche_finali"] == atteso["notifiche_finali"]
    assert ottenuto["cicli_infiniti"] == atteso["cicli_infiniti"]
    assert ottenuto.get("corsa_interrotta") == atteso.get("corsa_interrotta")
    assert ottenuto["vmc"] == atteso["vmc"]
    assert ottenuto["fine"] == atteso["fine"]
    return {
        "state_changed dei valori interni": len(atteso["interni"]),
        "call_service con soli valori interni": len(atteso["chiamate_interne"]),
        "state_reported dei valori interni (uguali nella memoria)": len(
            atteso["rapporti"]
        ),
        "state_reported dei valori interni per update_entity (dal motore)": len(
            atteso["da_aggiornamento"]
        ),
        "call_service update_entity con valori interni (tolti)": atteso[
            "update_senza_interni"
        ],
        "chiamate update_entity del banco cambiate": update_cambiati,
        "valori interni con last_reported diverso alla fine": len(riportati_diversi),
        "eventi confrontati": sum(1 for v in atteso["registro"] if len(v) > 2),
    }


def _stampa(
    cosa: str, prova: Prova, conti: dict[str, int], esito: dict[str, Any]
) -> None:
    passi = Counter(p[0] for p in prova.passi)
    print(
        f"\n{cosa}: {len(prova.passi)} passi {dict(passi)}, fermate {esito['fermate']}"
    )
    for chiave, valore in conti.items():
        print(f"  {chiave}: {valore}")


@pytest.mark.parametrize("seme", [VMC_SEME_MEMORIA])
async def test_pacchetto_con_la_memoria(
    seme: int,
    freezer: FrozenDateTimeFactory,
    monkeypatch: pytest.MonkeyPatch,
    hass_storage: dict[str, Any],
) -> None:
    """Stessa sequenza casuale con Home Assistant e gli aiutanti e con il motore e la
    memoria interna: stessi eventi (i cambi e le chiamate dei valori interni uguali a
    quelli della memoria), stessi stati finali."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    await _motore_con_interni()
    prova = GeneratoreSenzaInterni(seme).prova(VMC_PASSI_MEMORIA)
    hass_storage[CHIAVE] = _archivio(
        {
            chiave: da_stato(chiave, s.state)
            for s in prova.ripristino
            for chiave, e in zip(INTERNI, IDS, strict=True)
            if s.entity_id == e
        }
    )
    atteso = await _corsa(freezer, prova, motore=False, archivio=hass_storage)
    ottenuto = await _corsa(freezer, prova, motore=True, archivio=hass_storage)
    conti = _confronta_corse(atteso, ottenuto, f"seme {seme}")
    _stampa(f"seme {seme}", prova, conti, atteso)
    assert conti["state_changed dei valori interni"] > 0


@pytest.mark.parametrize("seme", [VMC_SEME_MEMORIA])
async def test_pacchetto_con_la_memoria_e_riavvio(
    seme: int,
    freezer: FrozenDateTimeFactory,
    monkeypatch: pytest.MonkeyPatch,
    hass_storage: dict[str, Any],
) -> None:
    """Prima parte, chiusura di Home Assistant con le esecuzioni in corso, seconda
    parte da quello che è stato salvato: con gli aiutanti gli stati di restore_state,
    con la memoria il suo archivio. Stessi eventi nelle due parti, stessi salvataggi."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    await _motore_con_interni()
    passi = max(VMC_PASSI_MEMORIA // 2, 1)
    prima = GeneratoreSenzaInterni(seme).prova(passi)
    iniziali = {
        chiave: da_stato(chiave, s.state)
        for s in prima.ripristino
        for chiave, e in zip(INTERNI, IDS, strict=True)
        if s.entity_id == e
    }
    hass_storage[CHIAVE] = _archivio(iniziali)
    atteso_1 = await _corsa(
        freezer, prima, motore=False, archivio=hass_storage, riavvio=True
    )
    hass_storage[CHIAVE] = _archivio(iniziali)
    ottenuto_1 = await _corsa(
        freezer, prima, motore=True, archivio=hass_storage, riavvio=True
    )
    conti_1 = _confronta_corse(atteso_1, ottenuto_1, f"seme {seme}, prima parte")
    _stampa(f"seme {seme}, prima parte", prima, conti_1, atteso_1)

    # i salvataggi alla chiusura: le altre entità come Home Assistant (tranne le
    # automazioni: le logiche non hanno stati salvati), i valori interni nell'archivio
    # della memoria come restore_state salva gli aiutanti
    interni = set(IDS)
    automazioni = [
        v[0] for v in atteso_1["salvati_confronto"] if v[0].startswith("automation.")
    ]
    assert len(automazioni) == 14
    assert [
        v
        for v in atteso_1["salvati_confronto"]
        if v[0] not in interni and v[0] not in automazioni
    ] == ottenuto_1["salvati_confronto"]
    assert not any(
        v[0] in interni or v[0].startswith("automation.")
        for v in ottenuto_1["salvati_confronto"]
    )
    archiviati = hass_storage[CHIAVE]["data"]["valori"]
    per_entita = {v[0]: v[1] for v in atteso_1["salvati_confronto"]}
    assert archiviati == {
        chiave: da_stato(chiave, per_entita[e])
        for chiave, e in zip(INTERNI, IDS, strict=True)
    }
    cambiati = sum(
        1
        for chiave in INTERNI
        if chiave in iniziali and archiviati[chiave] != iniziali[chiave]
    )

    seconda = GeneratoreSenzaInterni(seme + 1).prova(passi)
    seconda.inizio = atteso_1["fine"] + timedelta(seconds=PAUSA_RIAVVIO)
    seconda.vmc = VmcFinta(**atteso_1["vmc"])
    # le automazioni di Home Assistant ripartono senza stato salvato, come le logiche
    atteso_2 = await _corsa(
        freezer,
        seconda,
        motore=False,
        archivio=hass_storage,
        salvati=[
            v
            for v in atteso_1["salvati"]
            if not v["state"]["entity_id"].startswith("automation.")
        ],
    )
    ottenuto_2 = await _corsa(
        freezer,
        seconda,
        motore=True,
        archivio=hass_storage,
        salvati=ottenuto_1["salvati"],
    )
    conti_2 = _confronta_corse(atteso_2, ottenuto_2, f"seme {seme}, seconda parte")
    _stampa(f"seme {seme}, seconda parte", seconda, conti_2, atteso_2)
    print(
        f"  valori salvati alla chiusura: {len(atteso_1['salvati'])} con gli aiutanti, "
        f"{len(ottenuto_1['salvati'])} + {len(archiviati)} nella memoria; valori "
        f"interni diversi da quelli dell'avvio: {cambiati}"
    )
    assert conti_2["eventi confrontati"] > 0


@pytest.mark.parametrize("seme", [VMC_SEME_MEMORIA])
async def test_pacchetto_con_memoria_script_e_timer_del_motore(
    seme: int, freezer: FrozenDateTimeFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Le tre parti della fase 4 insieme: il package tradotto con i valori interni
    (``interni=INTERNI``), con gli script e i comandi dentro il motore
    (``comandi=...``) e con i timer del motore (``timer_motore``), contro Home Assistant
    con tutti i suoi aiutanti, script, shell_command e timer (banco di
    ``test_pacchetto_casuale`` con ``memoria``, ``fedeli`` e ``timer_motore``). Tolti gli
    eventi che non ci sono più, tutto il resto uguale; i cambi e le chiamate dei valori
    interni uguali a quelli della memoria, anche nell'ordine di tutto insieme."""
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )
    nome = f"memoria_script_timer_{seme}"
    async with async_test_home_assistant() as hass:
        automazioni, script = leggi_package()
        testo_modelli, testo_motore = await traduci_configurazione(
            hass,
            automazioni,
            script,
            nome_modelli=f"{nome}_modelli",
            comandi=leggi_comandi(),
            timer_motore=True,
            interni=INTERNI,
        )
        await hass.async_stop(force=True)
    assert "c.memoria_interna(INTERNI)" in testo_motore
    assert "def comandi(c):" in testo_motore
    moduli = [
        f"{generato.__name__}.{nome}_modelli",
        f"{generato.__name__}.{nome}_motore",
    ]
    try:
        _carica(f"{nome}_modelli", testo_modelli)
        codice = _carica(f"{nome}_motore", testo_motore)
        prova = GeneratoreSenzaInterni(seme).prova(VMC_PASSI_MEMORIA)
        opzioni: dict[str, Any] = {
            "timer_motore": True,
            "fedeli": True,
            "memoria": True,
        }
        atteso = await casuale._corsa(freezer, prova, motore=False, **opzioni)
        ottenuto = await casuale._corsa(
            freezer, prova, motore=True, codice=codice, **opzioni
        )
    finally:
        for modulo in moduli:
            sys.modules.pop(modulo, None)
    assert ottenuto["tolti"] == Counter()
    assert not ottenuto["update_senza_interni"]
    assert any(v[0] == "evento" for v in ottenuto["dei_timer"])
    casuale._confronta_corse(atteso, ottenuto, f"seme {seme}, tutto insieme")
    print(
        f"\nseme {seme}, tutto insieme: {len(prova.passi)} passi, "
        f"{sum(1 for v in atteso['registro'] if len(v) > 2)} eventi confrontati, "
        f"{len(atteso['interni'])} cambi e {len(atteso['chiamate_interne'])} chiamate "
        f"dei valori interni, {atteso['update_senza_interni']} update_entity senza "
        f"valori interni, registro dei timer {len(atteso['dei_timer'])} voci, "
        f"tolti {dict(atteso['tolti'])}"
    )
