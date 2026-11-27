"""Più VMC nello stesso Home Assistant: il motore come i package clonati.

L'integrazione installa un package per ogni VMC (``installatore.genera_file``): per le
VMC diverse dalla Master è lo stesso package con «master» rinominato
(``trasforma.rinomina``). Il motore tradotto ha invece un solo modulo generato per tutte
le VMC e un ``Contesto`` per ciascuna, che rinomina i testi con ``c.N``.

Qui un solo Home Assistant carica i package di tre VMC, come li scrive l'integrazione: la
Master, una VMC con un nome qualsiasi e una con «master» dentro il nome (il nome più
scomodo che l'integrazione accetta: solo lettere minuscole, ``const.NOME_RE``; una
rinomina fatta due volte qui si vede). In una seconda corsa gli stessi package girano con
un motore per VMC al posto delle automazioni e degli script. Con lo stesso orologio e gli
stessi eventi (alcuni toccano una sola VMC, altri tutte) devono essere identici, nello
stesso ordine e allo stesso istante: servizi chiamati, cambi di stato, automazioni e
script avviati, notifiche; e le entità registrate (entity_id, unique_id...) devono essere
quelle di Home Assistant.

I comandi alla VMC (``shell_command``), le notifiche (``notify``,
``persistent_notification``), il registro (``recorder``), ``homeassistant.update_entity``
e gli altri servizi esterni sono servizi finti che annotano la chiamata; i sensori letti
dalla VMC (tcp, command_line, rest) sono stati scritti dalla prova.

Perché l'ordine si possa confrontare, la prova toglie due fonti di caso che non vengono
né dal package né dal motore (con esse anche due corse di Home Assistant da solo danno
ordini diversi):

- i lavori nei thread (``run_in_executor``) girano subito nel ciclo: con i thread veri le
  piattaforme dei sensori modello si avviano in un ordine che dipende dal tempo vero, e
  con esso l'ordine dei loro stati all'avvio;
- con l'orologio fermo molti timer scadono nello stesso istante e asyncio li esegue in un
  ordine che dipende dalla storia della sua coda (anche dei timer delle corse
  precedenti): qui scade prima quello creato prima, come con un orologio vero.
"""

from __future__ import annotations

import asyncio
import difflib
import itertools
import re
from collections import Counter
from datetime import UTC, datetime, timedelta
from functools import cache
from typing import Any

import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import (
    Context,
    CoreState,
    Event,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    State,
    SupportsResponse,
    callback,
)
from homeassistant.core_config import _CUSTOMIZE_CONFIG_SCHEMA, DATA_CUSTOMIZE
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_values import EntityValues
from homeassistant.helpers.service import SERVICE_DESCRIPTION_CACHE
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from homeassistant.util.yaml.loader import parse_yaml
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_test_home_assistant,
)

from custom_components.vmc_master.const import NOME_MASTER, NOME_RE
from custom_components.vmc_master.installatore import genera_file
from custom_components.vmc_master.nativa.motore.ha import Motore
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.trasforma import rinomina

from .fase3 import MotoreFase3, osserva_logiche, personalizzato
from .test_avvio_motore import _registro_entita
from .test_semantica import PASSO, _gira
from .traduci import _Caricatore, leggi_package

# La Master, un nome qualsiasi e un nome con «master» dentro
NOMI = (NOME_MASTER, "cucina", "masterino")
IP = {
    NOME_MASTER: "192.168.1.50",
    "cucina": "192.168.1.51",
    "masterino": "192.168.1.52",
}
VERSIONE = "9.0.0b42"
FUSO = "Europe/Rome"
# 07:59:00 a Roma: un minuto dopo scattano per tutte le VMC i trigger delle 08:00
INIZIO = datetime(2026, 11, 25, 6, 59, 0, tzinfo=UTC)

AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_text",
    "input_select",
    "input_datetime",
    "timer",
)
# Senza ``automation_triggered``: le automazioni del motore sono logiche dell'integrazione,
# senza l'evento (l'istante in cui partono è nel loro stato: ``last_triggered``, ``current``)
EVENTI = {
    EVENT_STATE_CHANGED,
    EVENT_CALL_SERVICE,
    "script_started",
    "timer.started",
    "timer.finished",
    "timer.cancelled",
    "timer.restarted",
}
# Servizi chiamati dal package che non sono di Home Assistant o che qui non devono agire:
# annotano soltanto la chiamata
FINTI = (
    ("homeassistant", "update_entity"),
    ("homeassistant", "restart"),
    ("persistent_notification", "create"),
    ("persistent_notification", "dismiss"),
    ("recorder", "purge_entities"),
    ("tts", "google_translate_say"),
    ("tts", "clear_cache"),
    ("media_player", "volume_set"),
    ("notify", "mobile_app_telefono"),
)
# I comandi di velocità della VMC (shell_command «printf 'VMWH000000<velocità>\n' | nc...»)
_RE_COMANDO_VELOCITA = re.compile(r"'VMWH000000([0-7])\\n'")
# Un sensore di temperatura esterno, lo stesso per tutte le VMC
ESTERNO = "sensor.esterno_temperatura"


def _vmc(nome: str, testo: str) -> str:
    """Un entity_id o un testo del package per la VMC ``nome`` (come l'integrazione)."""
    return testo if nome == NOME_MASTER else rinomina(testo, nome)


@cache
def _testi(nome: str) -> dict[str, str]:
    """I file del package della VMC come li scrive l'integrazione."""
    return genera_file(nome, IP[nome], VERSIONE)


@cache
def _file(nome: str) -> dict[str, Any]:
    """I due package della VMC (``vmc_<nome>.yaml`` e ``vmc_<nome>_automazione.yaml``)
    letti come li legge Home Assistant."""
    return {
        "package": parse_yaml(_testi(nome)[f"vmc_{nome}.yaml"]),
        "automazione": parse_yaml(_testi(nome)[f"vmc_{nome}_automazione.yaml"]),
    }


def _norma(valore: Any) -> Any:
    """Un valore del registro senza ciò che cambia da una corsa all'altra (gli istanti in
    secondi dall'inizio)."""
    if isinstance(valore, datetime):
        return round((valore - INIZIO).total_seconds(), 3)
    if isinstance(valore, Context):
        return None
    if isinstance(valore, State):
        return (valore.entity_id, valore.state, _norma(dict(valore.attributes)))
    if isinstance(valore, dict):
        return {k: _norma(v) for k, v in sorted(valore.items()) if k != "run_id"}
    if isinstance(valore, (list, tuple)):
        return [_norma(v) for v in valore]
    return valore


def _ventola(velocita: int) -> str:
    """La risposta della VMC a «VMGH?» con la velocità indicata."""
    return f"VMGO,0000{velocita}" + ",00000" * 13


def _sensori(umidita: int = 50, co2: int = 600) -> str:
    """La risposta della VMC a «VMGI?»: 21 °C dentro, 10 °C fuori, umidità e CO₂."""
    return (
        f"VMGI,00210,00100,{umidita * 10:05d},{co2:05d}"
        + ",00000" * 6
        + ",00050,00000,00000,00000"
    )


def _stati_vmc(nome: str, velocita: int) -> dict[str, str]:
    """Gli stati dei sensori letti dalla VMC (tcp, command_line, rest)."""
    return {
        _vmc(nome, "sensor.vmc_master_status_ventola"): _ventola(velocita),
        _vmc(nome, "sensor.vmc_master_sensori"): _sensori(),
        _vmc(nome, "sensor.vmc_master_nome"): f"VMNM {nome.capitalize()}",
        _vmc(nome, "sensor.vmc_master_lan"): f"VMSL,{IP[nome].replace('.', ',')}",
        _vmc(nome, "sensor.vmc_master_status_ip"): "ON-Line",
        _vmc(nome, "sensor.vmc_master_versione_repository"): f"v.{VERSIONE}",
    }


# --- passi della prova ------------------------------------------------------------------


def servizio(
    nome: str, dati: dict[str, Any], *, utente: bool = False
) -> tuple[Any, ...]:
    """Un servizio chiamato (``utente``: da un utente, come un tasto della scheda)."""
    return ("servizio", nome, dati, utente)


def stato(
    entita: str, valore: str, attributi: dict[str, Any] | None = None
) -> tuple[Any, ...]:
    return ("stato", entita, valore, attributi or {})


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


def ventola(nome: str, velocita: int) -> tuple[Any, ...]:
    """La VMC ``nome`` passa da sola alla velocità indicata (telecomando della VMC, App
    Air Guard) e il sensore della ventola la legge."""
    return ("ventola", nome, velocita)


def _scegli(nome: str, selettore: str, opzione: str) -> tuple[Any, ...]:
    return servizio(
        "input_select.select_option",
        {"entity_id": _vmc(nome, selettore), "option": opzione},
    )


PASSI: list[tuple[Any, ...]] = [
    # avvio di Home Assistant (tutte le VMC), poi le 08:00 a Roma (tutte le VMC)
    attendi(70),
    # solo cucina: la VMC passa da sola a Velocità 3 (telecomando della VMC)
    ventola("cucina", 3),
    attendi(20),
    # solo master: comando Velocità 2 dalla scheda (trigger evento call_service con il
    # nome del servizio nei dati)
    servizio("shell_command.vmc_master_velocita_2", {}),
    attendi(12),
    # solo masterino: nuovo IP nel campo Cambia IP (servizio dell'integrazione
    # vmc_master.verifica_ip, che non si rinomina, poi comandi e riavvio)
    servizio(
        "input_text.set_value",
        {"entity_id": "input_text.vmc_masterino_ip_insert", "value": "192.168.1.99"},
    ),
    attendi(5),
    # solo masterino: finestra dei tempi di attesa (esclusività delle finestre)
    servizio(
        "input_boolean.turn_on",
        {"entity_id": "input_boolean.vmc_masterino_opzione_finestra_tempi_attesa"},
    ),
    attendi(3),
    # solo master: elenco dei dispositivi dell'app (il telefono), il telefono per le
    # notifiche, poi la notifica di Velocità 0
    servizio(
        "script.turn_on",
        {"entity_id": "script.vmc_master_aggiorna_elenco_entita_notifica_dispositivo"},
    ),
    attendi(3),
    _scegli(
        NOME_MASTER, "input_select.vmc_master_selected_notification_device", "telefono"
    ),
    attendi(1),
    servizio("script.vmc_master_notifica_velocita_0", {}),
    attendi(3),
    # solo cucina: reset del filtro (5 s con il countdown: il timer che finisce fa
    # scattare il Countdown Letture VMC di tutte le VMC)
    servizio("script.turn_on", {"entity_id": "script.vmc_cucina_reset_filtro_vmc"}),
    attendi(10),
    # tutte: elenco delle entità temperatura esterna (legge anche i sensori delle altre
    # VMC), poi lo stesso sensore esterno per tutte, che cambia
    *(
        servizio(
            "script.turn_on",
            {
                "entity_id": _vmc(
                    nome, "script.vmc_master_aggiorna_elenco_entita_temperatura_esterna"
                )
            },
        )
        for nome in NOMI
    ),
    attendi(8),
    *(
        _scegli(nome, "input_select.vmc_master_selected_temp_external_entity", ESTERNO)
        for nome in NOMI
    ),
    attendi(3),
    stato(
        ESTERNO, "-25.0", {"device_class": "temperature", "unit_of_measurement": "°C"}
    ),
    # solo masterino: mentre il comando di Velocità 0 per il congelamento è in viaggio,
    # un utente preme Velocità 3 nella scheda (Registro Comandi e Scelte, Rimando della
    # Scelta: il servizio si sceglie da una lista di nomi)
    servizio("shell_command.vmc_masterino_velocita_3", {}, utente=True),
    attendi(30),
    # solo masterino: la VMC non risponde più, poi torna
    stato("sensor.vmc_masterino_status_ip", "OFF-Line"),
    attendi(20),
    stato("sensor.vmc_masterino_status_ip", "ON-Line"),
    attendi(20),
    # solo masterino: Profilo Inizializzazione (profili, tempi di attesa, comandi), poi
    # umidità e CO₂ alte
    servizio(
        "script.turn_on", {"entity_id": "script.vmc_masterino_profilo_inizializzazione"}
    ),
    attendi(40),
    stato("sensor.vmc_masterino_sensori", _sensori(umidita=85, co2=1500)),
    attendi(60),
    # solo cucina: Panic Button
    servizio("script.turn_on", {"entity_id": "script.vmc_cucina_bottone_panico"}),
    attendi(30),
    # solo master: aggiornamento di tutti i sensori (79 s)
    servizio("script.turn_on", {"entity_id": "script.vmc_master_upgrade_sensors"}),
    attendi(85),
    # tutte: le tre VMC passano insieme a Velocità 2
    *(ventola(nome, 2) for nome in NOMI),
    attendi(30),
]


_ORDINE_TIMER = itertools.count()


class _TimerInOrdine(asyncio.TimerHandle):
    """Un timer di asyncio che, a pari scadenza, viene dopo quelli creati prima."""

    __slots__ = ("_ordine",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._ordine = next(_ORDINE_TIMER)

    def _chiave(self) -> tuple[float, int]:
        return (self._when, self._ordine)

    @staticmethod
    def _altra(altro: asyncio.TimerHandle) -> tuple[float, int]:
        # i timer creati prima della prova non hanno un numero d'ordine
        return (altro.when(), getattr(altro, "_ordine", -1))

    def __lt__(self, altro: object) -> bool:
        if not isinstance(altro, asyncio.TimerHandle):
            return NotImplemented
        return self._chiave() < self._altra(altro)

    def __le__(self, altro: object) -> bool:
        if not isinstance(altro, asyncio.TimerHandle):
            return NotImplemented
        return self._chiave() <= self._altra(altro)

    def __gt__(self, altro: object) -> bool:
        if not isinstance(altro, asyncio.TimerHandle):
            return NotImplemented
        return self._chiave() > self._altra(altro)

    def __ge__(self, altro: object) -> bool:
        if not isinstance(altro, asyncio.TimerHandle):
            return NotImplemented
        return self._chiave() >= self._altra(altro)


@pytest.fixture
async def deterministico(monkeypatch: pytest.MonkeyPatch) -> None:
    """Lavori dei thread nel ciclo e timer di pari scadenza in ordine di creazione (vedi
    in cima); i trigger time e time_pattern allo stesso microsecondo."""
    ciclo = asyncio.get_running_loop()

    def nel_ciclo(
        _esecutore: Any, funzione: Any, *argomenti: Any
    ) -> asyncio.Future[Any]:
        futuro = ciclo.create_future()
        try:
            futuro.set_result(funzione(*argomenti))
        except BaseException as err:  # noqa: BLE001
            futuro.set_exception(err)
        return futuro

    monkeypatch.setattr(ciclo, "run_in_executor", nel_ciclo)
    monkeypatch.setattr(asyncio.events, "TimerHandle", _TimerInOrdine)
    monkeypatch.setattr(
        "homeassistant.helpers.event.randint", lambda minimo, massimo: minimo
    )


@pytest.fixture
def expected_lingering_timers() -> bool:
    """I sensori modello del package che leggono ``now()`` restano in ascolto del tempo
    anche dopo la chiusura di Home Assistant (che non toglie le entità)."""
    return True


async def _avanza(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, secondi: float
) -> None:
    for _ in range(round(secondi / PASSO)):
        freezer.tick(timedelta(seconds=PASSO))
        await _gira(hass)


def _stati(hass: HomeAssistant, *domini: str) -> list[Any]:
    """Gli stati (di ``domini``, o tutti) con quelli delle logiche del motore."""
    stati = [
        *hass.states.async_all(domini or None),
        *(personalizzato(hass, s) for s in stati_logiche(hass).stati.values()),
    ]
    return sorted((s.entity_id, s.state, _norma(dict(s.attributes))) for s in stati)


async def _corsa(freezer: FrozenDateTimeFactory, *, motore: bool) -> dict[str, Any]:
    freezer.move_to(INIZIO)
    registro: list[Any] = []
    esito: dict[str, Any] = {"registro": registro}
    async with async_test_home_assistant(initial_state=CoreState.not_running) as hass:
        await hass.config.async_set_time_zone(FUSO)
        # le personalizzazioni dei package (icone delle automazioni), come core_config
        esatte: dict[str, Any] = {}
        for nome in NOMI:
            personalizza = _file(nome)["package"]["homeassistant"]
            esatte.update(_CUSTOMIZE_CONFIG_SCHEMA(personalizza)["customize"])
        hass.data[DATA_CUSTOMIZE] = EntityValues(esatte, {}, {})
        assert await async_setup_component(hass, "homeassistant", {})
        for dominio in AIUTANTI:
            voci: dict[str, Any] = {}
            for nome in NOMI:
                voci.update(_file(nome)["package"][dominio])
            assert await async_setup_component(hass, dominio, {dominio: voci})

        # i contesti (id casuali) come numeri d'ordine: si confronta chi ha causato cosa
        contesti: dict[str | None, int | None] = {None: None}

        def contesto(identificativo: str | None) -> int | None:
            return contesti.setdefault(identificativo, len(contesti) - 1)

        def annota_chiamata(chiamata: ServiceCall) -> None:
            registro.append(
                (
                    _norma(dt_util.utcnow()),
                    "finto",
                    f"{chiamata.domain}.{chiamata.service}",
                    _norma(dict(chiamata.data)),
                    contesto(chiamata.context.id),
                )
            )

        # la VMC finta: un comando di velocità cambia la sua velocità, che il sensore
        # della ventola mostra alla lettura seguente (homeassistant.update_entity)
        velocita: dict[str, int] = dict.fromkeys(NOMI, 1)
        comandi: dict[str, tuple[str, int]] = {}
        ventole: dict[str, str] = {}
        for nome in NOMI:
            ventole[_vmc(nome, "sensor.vmc_master_status_ventola")] = nome
            for servizio_vmc, comando in _file(nome)["package"][
                "shell_command"
            ].items():
                if trovato := _RE_COMANDO_VELOCITA.search(comando):
                    comandi[servizio_vmc] = (nome, int(trovato.group(1)))

        async def finto(chiamata: ServiceCall) -> None:
            annota_chiamata(chiamata)
            if chiamata.domain == "shell_command" and chiamata.service in comandi:
                nome, nuova = comandi[chiamata.service]
                velocita[nome] = nuova
            elif (chiamata.domain, chiamata.service) == (
                "homeassistant",
                "update_entity",
            ):
                for entita in chiamata.data["entity_id"]:
                    if (nome := ventole.get(entita)) is not None:
                        hass.states.async_set(entita, _ventola(velocita[nome]))

        async def statistiche(chiamata: ServiceCall) -> ServiceResponse:
            annota_chiamata(chiamata)
            return {}

        async def verifica_ip(chiamata: ServiceCall) -> ServiceResponse:
            annota_chiamata(chiamata)
            return {"nome": chiamata.data["nome"], "esito": "ok"}

        for dominio, nome_servizio in FINTI:
            hass.services.async_register(dominio, nome_servizio, finto)
        hass.services.async_register(
            "recorder",
            "get_statistics",
            statistiche,
            supports_response=SupportsResponse.ONLY,
        )
        hass.services.async_register(
            "vmc_master",
            "verifica_ip",
            verifica_ip,
            supports_response=SupportsResponse.ONLY,
        )
        hass.states.async_set(
            ESTERNO, "5.0", {"device_class": "temperature", "unit_of_measurement": "°C"}
        )
        # un telefono con l'app di Home Assistant (notify.mobile_app_telefono); il titolo
        # della voce è quello che cerca integration_entities('mobile_app')
        app = MockConfigEntry(domain="mobile_app", title="mobile_app")
        app.add_to_hass(hass)
        telefono = dr.async_get(hass).async_get_or_create(
            config_entry_id=app.entry_id,
            identifiers={("mobile_app", "telefono")},
            name="Telefono",
        )
        er.async_get(hass).async_get_or_create(
            "device_tracker",
            "mobile_app",
            "telefono",
            config_entry=app,
            device_id=telefono.id,
            suggested_object_id="telefono",
        )
        hass.states.async_set("device_tracker.telefono", "home")
        for nome in NOMI:
            for nome_servizio in _file(nome)["package"]["shell_command"]:
                hass.services.async_register("shell_command", nome_servizio, finto)
            for entita, valore in _stati_vmc(nome, 1).items():
                hass.states.async_set(entita, valore)
        modelli: list[Any] = []
        for nome in NOMI:
            modelli += _file(nome)["package"]["template"]
        assert await async_setup_component(hass, "template", {"template": modelli})
        motori: list[Motore] = []
        if motore:
            for nome in NOMI:
                motori.append(MotoreFase3(hass, nome))
                await motori[-1].avvia()
        else:
            script: dict[str, Any] = {}
            automazioni: list[Any] = []
            for nome in NOMI:
                script.update(_file(nome)["package"]["script"])
                # come «packages: !include_dir_named»: nella cartella di ogni VMC i file in
                # ordine di nome, prima vmc_<nome>.yaml e poi vmc_<nome>_automazione.yaml
                automazioni += _file(nome)["package"]["automation"]
                automazioni += _file(nome)["automazione"]["automation"]
            assert await async_setup_component(hass, "script", {"script": script})
            assert await async_setup_component(
                hass, "automation", {"automation": automazioni}
            )
        await hass.async_block_till_done()
        esito["entita"] = _registro_entita(hass)
        esito["logiche"] = {a.entity_id for m in motori for a in m.automazioni}
        # le descrizioni dei servizi script.<chiave> (async_set_service_schema degli script)
        esito["descrizioni"] = sorted(
            (servizio, _norma(descrizione))
            for (dominio, servizio), descrizione in hass.data[
                SERVICE_DESCRIPTION_CACHE
            ].items()
            if dominio == "script"
        )
        esito["iniziali"] = _stati(hass, "automation", "script")

        @callback
        def annota(evento: Event) -> None:
            if evento.event_type not in EVENTI:
                return
            dati = evento.data
            if evento.event_type == EVENT_STATE_CHANGED:
                dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            registro.append(
                (
                    _norma(evento.time_fired),
                    evento.event_type,
                    _norma(dict(dati)),
                    contesto(evento.context.id),
                    contesto(evento.context.parent_id),
                )
            )

        togli = hass.bus.async_listen(MATCH_ALL, annota)

        smetti = osserva_logiche(hass, annota)
        avvio = asyncio.ensure_future(hass.async_start())
        for _ in range(100_000):
            await _gira(hass)
            if avvio.done():
                break
            freezer.tick(timedelta(seconds=PASSO))
        registro.append(("avviato",))
        for passo in PASSI:
            if passo[0] == "servizio":
                dominio, nome_servizio = passo[1].split(".")
                await hass.services.async_call(
                    dominio,
                    nome_servizio,
                    passo[2],
                    blocking=True,
                    context=Context(user_id="utente") if passo[3] else None,
                )
                await _gira(hass)
            elif passo[0] == "stato":
                hass.states.async_set(passo[1], passo[2], passo[3])
                await _gira(hass)
            elif passo[0] == "ventola":
                velocita[passo[1]] = passo[2]
                hass.states.async_set(
                    _vmc(passo[1], "sensor.vmc_master_status_ventola"),
                    _ventola(passo[2]),
                )
                await _gira(hass)
            else:
                await _avanza(hass, freezer, passo[1])
        togli()
        smetti()
        esito["finali"] = _stati(hass)
        for m in motori:
            await m.ferma()
        for dominio in ("automation", "script", "timer"):
            await hass.services.async_call(
                dominio,
                "cancel" if dominio == "timer" else "turn_off",
                {"entity_id": "all"},
                blocking=True,
            )
        await _gira(hass)
        await hass.async_stop(force=True)
    return esito


def _rinominato(valore: Any, nome: str) -> Any:
    """Una configurazione letta dal package della Master, per la VMC ``nome``."""
    if isinstance(valore, str):
        return _vmc(nome, valore)
    if isinstance(valore, list):
        return [_rinominato(v, nome) for v in valore]
    if isinstance(valore, dict):
        return {_rinominato(k, nome): _rinominato(v, nome) for k, v in valore.items()}
    return valore


@pytest.mark.parametrize("nome", NOMI)
def test_traduttore_legge_il_package_dell_integrazione(nome: str) -> None:
    """Le automazioni e gli script che legge il traduttore, rinominati per la VMC come fa
    ``c.N``, sono quelli che l'integrazione installa per quella VMC (id dell'automazione
    principale compreso): IP, link e versione che l'integrazione scrive nei file non
    toccano automazioni e script."""
    automazioni, script = leggi_package()
    package = yaml.load(_testi(nome)[f"vmc_{nome}.yaml"], Loader=_Caricatore)
    principale = yaml.load(
        _testi(nome)[f"vmc_{nome}_automazione.yaml"], Loader=_Caricatore
    )
    assert _rinominato(automazioni, nome) == [
        *package["automation"],
        *principale["automation"],
    ]
    assert _rinominato(script, nome) == package["script"]


def _confronta(atteso: list[Any], ottenuto: list[Any], cosa: str) -> None:
    if ottenuto == atteso:
        return
    diff = "\n".join(
        difflib.unified_diff(
            [repr(v) for v in atteso],
            [repr(v) for v in ottenuto],
            "home_assistant",
            "motore",
            lineterm="",
            n=2,
        )
    )
    pytest.fail(f"{cosa} diversi:\n{diff[:20000]}")


@pytest.mark.usefixtures("deterministico")
async def test_tre_vmc_come_home_assistant(freezer: FrozenDateTimeFactory) -> None:
    """Tre VMC nello stesso Home Assistant: stesse entità registrate (e descrizioni dei
    servizi degli script), stesso registro degli eventi (servizi, stati, avvii,
    notifiche, nello stesso ordine) e stessi stati con i package YAML e con tre motori."""
    assert all(NOME_RE.fullmatch(nome) for nome in NOMI)
    atteso = await _corsa(freezer, motore=False)
    ottenuto = await _corsa(freezer, motore=True)
    # i package delle tre VMC: 14 automazioni e 51 script ciascuna, con il nome giusto
    for nome in NOMI:
        mie = [
            voce
            for voce in atteso["iniziali"]
            if f"vmc_{nome}_" in voce[0] or voce[0].endswith(f"_vmc_{nome}")
        ]
        assert len(mie) == 14 + 51, nome
    assert len(atteso["iniziali"]) == 3 * (14 + 51)
    assert len(atteso["descrizioni"]) == 3 * 51
    # i passi arrivano dove devono (con Home Assistant): comandi a tutte le VMC,
    # notifiche, il servizio dell'integrazione e la scelta dell'utente rimandata
    chiamate = Counter(
        voce[2] for voce in atteso["registro"] if len(voce) > 1 and voce[1] == "finto"
    )
    for nome in NOMI:
        assert chiamate[_vmc(nome, "shell_command.vmc_master_velocita_0")], nome
    for servizio_atteso in (
        "notify.mobile_app_telefono",
        "persistent_notification.create",
        "vmc_master.verifica_ip",
        "shell_command.vmc_masterino_aggiorna_indirizzo_ip",
        "homeassistant.restart",
        "shell_command.vmc_cucina_reset_filtro",
    ):
        assert chiamate[servizio_atteso], servizio_atteso
    assert chiamate["shell_command.vmc_masterino_velocita_3"] == 2
    # le automazioni del motore sono logiche, senza voci nel registro delle entità
    automazioni = {voce[0] for voce in atteso["entita"] if voce[0].startswith("automation.")}
    assert len(automazioni) == 3 * 14
    assert ottenuto["logiche"] == automazioni
    _confronta(
        [voce for voce in atteso["entita"] if voce[0] not in automazioni],
        ottenuto["entita"],
        "registri delle entità",
    )
    _confronta(
        atteso["descrizioni"], ottenuto["descrizioni"], "descrizioni dei servizi"
    )
    _confronta(atteso["iniziali"], ottenuto["iniziali"], "stati iniziali")
    _confronta(atteso["registro"], ottenuto["registro"], "registri")
    _confronta(atteso["finali"], ottenuto["finali"], "stati finali")
