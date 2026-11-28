"""Script e comandi di shell dentro il motore (fase 4) si comportano come oggi.

Ogni prova fa girare automazioni e script in YAML due volte con lo stesso orologio e gli
stessi passi:

- con Home Assistant: le automazioni e gli script YAML, i 16 shell_command del package
  (le righe di comando vere) e un sottoprocesso finto che fa da VMC (come
  ``strumenti/simulatore/fakevmc.py``: il comando ``VMWH`` arriva alla VMC quando il
  processo parte, ``nc`` dura 0,05 s, 3 s se la VMC non risponde). Il file .sh del
  cambio del nome gira davvero con bash, con un ``nc`` finto che annota quello che
  riceve: è lui a decidere se e cosa arriva alla VMC (dalla b46 il motore non ha il
  cambio dell'IP);
- con il motore: le stesse automazioni e gli stessi script tradotti con gli script e i
  comandi dentro il motore (``traduzione(..., comandi=...)``), i comandi che vanno a una
  VMC finta con gli stessi tempi (``invia``) e i pulsanti per le chiamate della scheda.

Il registro (eventi del bus, comandi arrivati alla VMC, con l'istante e la forma del
contesto) deve essere identico, tolti gli eventi che con gli
script e i comandi dentro il motore non ci sono più (lo stato degli script,
``script_started``, le chiamate ``script.*`` e ``shell_command.*``) e quelli nuovi dei
pulsanti (lo stato dei pulsanti, ``button.press``): li conta ``CONTEGGI``.
"""

from __future__ import annotations

import asyncio
import difflib
import os
import shutil
import subprocess
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import probatio
import pytest
import yaml
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import EVENT_CALL_SERVICE, EVENT_STATE_CHANGED, MATCH_ALL
from homeassistant.core import (
    Context,
    Event,
    HomeAssistant,
    ServiceCall,
    callback,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockEntityPlatform,
    async_test_home_assistant,
)

from custom_components.vmc_master.nativa.client import ErroreVMC
from custom_components.vmc_master.nativa.motore.ha import Motore
from custom_components.vmc_master.nativa.motore.stati_logiche import stati_logiche
from custom_components.vmc_master.nativa.pulsanti import PulsanteVMC
from custom_components.vmc_master.nativa.tabelle import PULSANTI

from . import generato
from .nel_canale import ordine_esterno, stato_di_logica
from .test_semantica import EVENTI, T0, _avanza, _carica, _gira, _norma
from .test_semantica_tempi import ordine_dei_timer  # noqa: F401 (fixture)
from .traduci import PACKAGE, leggi_comandi, traduci_configurazione

AIUTANTI = {
    "input_boolean": {"a": {}, "b": {}, "c": {}},
    "input_number": {"n": {"min": 0, "max": 100, "step": 1}},
    "input_text": {"vmc_master_nome_da_inserire": {"max": 255}},
}
# nc dei comandi: 0,05 s se la VMC risponde, 3 s se non risponde (come fakevmc.py)
DURATA_COMANDO = 0.05
DURATA_SENZA_VMC = 3.0

SCENARI: dict[str, tuple[str, list[tuple[Any, ...]]]] = {}
# eventi tolti e aggiunti, per scenario: {nome: {(lato, tipo): numero}}
CONTEGGI: dict[str, Counter[tuple[str, str]]] = {}


def scenario(nome: str, configurazione: str, *passi: tuple[Any, ...]) -> None:
    SCENARI[nome] = (configurazione, list(passi))


def servizio(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    """Una chiamata senza utente (per esempio dall'esterno)."""
    return ("servizio", nome, dati or {})


def scheda(nome: str, dati: dict[str, Any] | None = None) -> tuple[Any, ...]:
    """Una chiamata della scheda, con l'utente: con il motore è la pressione del
    pulsante."""
    return ("scheda", nome, dati or {})


def attendi(secondi: float) -> tuple[Any, ...]:
    return ("attendi", secondi)


def vmc(risponde: bool) -> tuple[Any, ...]:
    return ("vmc", risponde)


def acceso(entita: str) -> tuple[Any, ...]:
    return servizio("input_boolean.turn_on", {"entity_id": entita})


def spento(entita: str) -> tuple[Any, ...]:
    return servizio("input_boolean.turn_off", {"entity_id": entita})


def nome_scritto(valore: str) -> tuple[Any, ...]:
    return servizio(
        "input_text.set_value",
        {"entity_id": "input_text.vmc_master_nome_da_inserire", "value": valore},
    )


def numero(valore: float) -> tuple[Any, ...]:
    return servizio(
        "input_number.set_value", {"entity_id": "input_number.n", "value": valore}
    )


scenario(
    "modi_e_ordine_di_turn_on",
    """
script:
  prova_single:
    sequence:
      - action: prova.registra
        data: {passo: "single inizio {{ x | default('-') }}"}
      - delay: 2
      - action: prova.registra
        data: {passo: single fine}
  prova_restart:
    mode: restart
    sequence:
      - action: prova.registra
        data: {passo: "restart inizio {{ x | default('-') }}"}
      - delay: 2
      - action: prova.registra
        data: {passo: restart fine}
  prova_coda:
    mode: queued
    max: 2
    sequence:
      - action: prova.registra
        data: {passo: "coda {{ x | default('-') }}"}
      - delay: 1
  prova_parallelo:
    mode: parallel
    max: 2
    sequence:
      - action: prova.registra
        data: {passo: "parallelo {{ x | default('-') }}"}
      - delay: 1
automation:
  - alias: Avvia
    id: avvia
    mode: parallel
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.turn_on
        target:
          entity_id: [script.prova_parallelo, script.prova_coda, script.prova_restart,
                      script.prova_single, script.prova_coda]
        data: {variables: {x: "{{ trigger.to_state.state }}"}}
      - action: prova.registra
        data: {passo: "avviati {{ trigger.to_state.state }}"}
  - alias: Diretta
    id: diretta
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_coda
        data: {x: diretta}
      - action: prova.registra
        data: {passo: dopo diretta}
      - action: script.prova_single
        data: {x: diretta}
      - action: prova.registra
        data: {passo: dopo single}
""",
    numero(1),
    attendi(0.5),
    numero(2),
    attendi(0.3),
    numero(3),
    attendi(0.2),
    acceso("input_boolean.a"),
    attendi(3),
    numero(4),
    attendi(5),
)

scenario(
    "turn_off_e_toggle",
    """
script:
  prova_lungo:
    mode: parallel
    sequence:
      - action: prova.registra
        data: {passo: lungo inizio}
      - delay: 5
      - action: prova.registra
        data: {passo: lungo fine}
  prova_ferma:
    sequence:
      - action: script.turn_off
        target: {entity_id: script.prova_lungo}
      - action: prova.registra
        data: {passo: fermato}
automation:
  - alias: Comanda
    id: comanda
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.a, id: a}
      - {trigger: state, entity_id: input_boolean.b, id: b}
      - {trigger: state, entity_id: input_boolean.c, id: c}
    actions:
      - choose:
          - conditions: [{condition: trigger, id: a}]
            sequence:
              - action: script.turn_on
                target: {entity_id: script.prova_lungo}
          - conditions: [{condition: trigger, id: b}]
            sequence:
              - action: script.prova_ferma
          - conditions: [{condition: trigger, id: c}]
            sequence:
              - action: script.toggle
                target: {entity_id: script.prova_lungo}
      - action: prova.registra
        data: {passo: "fatto {{ trigger.id }}"}
""",
    acceso("input_boolean.a"),
    attendi(1),
    spento("input_boolean.a"),
    attendi(1),
    acceso("input_boolean.b"),
    attendi(1),
    acceso("input_boolean.c"),
    attendi(1),
    spento("input_boolean.c"),
    attendi(1),
    spento("input_boolean.b"),
    attendi(6),
)

scenario(
    "campi_variabili_ed_errori",
    """
script:
  prova_campi:
    fields:
      x: {description: valore}
    variables:
      doppio: "{{ (x | int(0)) * 2 }}"
    sequence:
      - action: prova.registra
        data: {passo: "campi {{ x | default('-') }} {{ doppio }}"}
  prova_errore:
    sequence:
      - action: prova.registra
        data: {passo: prima, errore: true}
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo errore ignorato}
      - action: prova.registra
        data: {passo: errore vero, errore: true}
      - action: prova.registra
        data: {passo: mai}
automation:
  - alias: Campi
    id: campi
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - action: script.prova_campi
        data: {x: "{{ trigger.to_state.state | int }}"}
      - action: script.turn_on
        target: {entity_id: script.prova_campi}
        data: {variables: {x: 7}}
      - action: script.prova_errore
        continue_on_error: true
      - action: prova.registra
        data: {passo: dopo script con errore}
      - action: script.prova_errore
      - action: prova.registra
        data: {passo: mai dopo}
""",
    numero(3),
    attendi(1),
    numero(4),
    attendi(1),
)

scenario(
    "ricorsioni",
    """
script:
  prova_ricorsivo:
    mode: queued
    sequence:
      - action: prova.registra
        data: {passo: "ricorsivo {{ volta | default(0) }}"}
      - if: "{{ (volta | default(0)) | int < 2 }}"
        then:
          - action: script.prova_ricorsivo
            data: {volta: "{{ (volta | default(0)) | int + 1 }}"}
  prova_rilancia:
    mode: parallel
    max: 3
    sequence:
      - action: prova.registra
        data: {passo: "rilancia {{ volta | default(0) }}"}
      - delay: 1
      - if: "{{ (volta | default(0)) | int < 2 }}"
        then:
          - action: script.turn_on
            target: {entity_id: script.prova_rilancia}
            data: {variables: {volta: "{{ (volta | default(0)) | int + 1 }}"}}
automation:
  - alias: Ricorsione
    id: ricorsione
    triggers:
      - {trigger: state, entity_id: input_boolean.a, to: "on"}
    actions:
      - action: script.prova_ricorsivo
      - action: prova.registra
        data: {passo: dopo ricorsivo}
      - action: script.turn_on
        target: {entity_id: script.prova_rilancia}
""",
    acceso("input_boolean.a"),
    attendi(4),
)

_AGGANCIO = """
script:
  vmc_master_reset_filtro_vmc:
    mode: restart
    sequence:
      - action: shell_command.vmc_master_reset_filtro
      - delay: 5
      - action: prova.registra
        data: {passo: reset finito}
  vmc_master_bottone_panico:
    mode: restart
    sequence:
      - action: script.turn_off
        target: {entity_id: script.vmc_master_reset_filtro_vmc}
      - action: shell_command.vmc_master_velocita_0
      - action: prova.registra
        data: {passo: panico}
automation:
  - alias: Registro Comandi
    id: registro_comandi
    mode: queued
    max: 50
    triggers:
      - trigger: event
        event_type: call_service
        event_data: {domain: shell_command, service: vmc_master_velocita_1}
        id: comando
      - trigger: event
        event_type: call_service
        event_data: {domain: shell_command, service: vmc_master_velocita_2}
        id: comando
      - {trigger: state, entity_id: input_boolean.c, id: lettura}
      - trigger: event
        event_type: call_service
        event_data: {domain: shell_command, service: vmc_master_notturna}
      - trigger: event
        event_type: call_service
        event_data: {domain: shell_command, service: vmc_master_velocita_0}
        alias: zero
    actions:
      - action: prova.registra
        data:
          passo: >-
            {{ trigger.id }} {{ trigger.idx }} {{ trigger.alias }} {{ trigger.platform }}
            {{ trigger.description | default('') }}
          servizio: "{{ trigger.event.data.service if trigger.platform == 'event' else '' }}"
          dati: "{{ trigger.event.data.service_data if trigger.platform == 'event' else '' }}"
          utente: >-
            {{ (trigger.event.context.user_id is not none)
               if trigger.platform == 'event' else '' }}
  - alias: Letture
    id: letture
    mode: restart
    triggers:
      - trigger: event
        event_type: call_service
        event_data: {domain: shell_command, service: vmc_master_velocita_1}
      - trigger: event
        event_type: call_service
        event_data: {domain: shell_command, service: vmc_master_velocita_2}
    conditions: "{{ trigger.event.context.user_id is none }}"
    actions:
      - repeat:
          count: 3
          sequence:
            - delay: 1
            - action: prova.registra
              data: {passo: "lettura {{ repeat.index }} {{ trigger.idx }}"}
  - alias: Comanda
    id: comanda
    mode: queued
    triggers:
      - {trigger: state, entity_id: input_boolean.a, id: a}
      - {trigger: state, entity_id: input_boolean.b, id: b}
    actions:
      - if: "{{ trigger.id == 'a' }}"
        then:
          - action: shell_command.vmc_master_velocita_1
        else:
          - action: shell_command.vmc_master_velocita_2
            data: {}
      - action: shell_command.vmc_master_notturna
      - action: prova.registra
        data: {passo: comandi inviati}
"""

scenario(
    "aggancio_dei_comandi",
    _AGGANCIO,
    acceso("input_boolean.a"),
    attendi(0.5),
    scheda("shell_command.vmc_master_velocita_2"),
    attendi(0.5),
    acceso("input_boolean.b"),
    attendi(0.2),
    acceso("input_boolean.c"),
    attendi(0.1),
    scheda("script.turn_on", {"entity_id": "script.vmc_master_reset_filtro_vmc"}),
    attendi(1),
    scheda("script.turn_on", {"entity_id": "script.vmc_master_reset_filtro_vmc"}),
    attendi(2),
    scheda("script.turn_on", {"entity_id": "script.vmc_master_bottone_panico"}),
    scheda("shell_command.vmc_master_notturna"),
    attendi(7),
)

scenario(
    "vmc_che_non_risponde",
    _AGGANCIO,
    vmc(False),
    acceso("input_boolean.a"),
    attendi(1),
    scheda("shell_command.vmc_master_velocita_1"),
    attendi(1),
    vmc(True),
    acceso("input_boolean.b"),
    attendi(8),
)

scenario(
    "nomi_dei_comandi_resi_da_modelli",
    """
automation:
  - alias: Dinamici
    id: dinamici
    mode: queued
    variables:
      servizi: >-
        {{ ['shell_command.vmc_master_velocita_0', 'shell_command.vmc_master_velocita_3',
            'shell_command.vmc_master_freecooling'] }}
    triggers:
      - {trigger: state, entity_id: input_number.n}
    actions:
      - variables:
          indice: "{{ trigger.to_state.state | int % 3 }}"
          comando_vmc: >-
            {{ ['velocita_4', 'iperventilazione', 'sensori_on'][trigger.to_state.state | int % 3] }}
      - action: "{{ servizi[indice] }}"
      - action: "shell_command.vmc_master_{{ comando_vmc }}"
      - action: prova.registra
        data: {passo: "dinamici {{ indice }}"}
      - if: "{{ trigger.to_state.state | int == 5 }}"
        then:
          - action: "shell_command.vmc_master_{{ 'inesistente' }}"
            continue_on_error: true
      - action: prova.registra
        data: {passo: "fine {{ indice }}"}
""",
    numero(1),
    attendi(0.3),
    numero(2),
    numero(3),
    attendi(1),
    numero(5),
    attendi(1),
)

scenario(
    "cambio_del_nome",
    """
automation:
  - alias: Rinomina
    id: rinomina
    mode: queued
    max: 30
    triggers:
      - {trigger: state, entity_id: input_text.vmc_master_nome_da_inserire}
    conditions: "{{ trigger.to_state.state != '' }}"
    actions:
      - action: shell_command.vmc_master_rimuovi_caratteri_di_ritorno
      - alias: Chiama il Servizio per Cambiare nome alla VMC
        action: shell_command.vmc_master_cambia_nome
      - delay: 1
      - action: prova.registra
        data: {passo: "rinominata {{ trigger.to_state.state }}"}
""",
    nome_scritto("Cucina"),
    attendi(1.5),
    *(
        passo
        for nome in (
            "NomeTroppoLungo",
            "1234567890",
            "con spazio",
            'a"b',
            "a\\b",
            "Àrea",
            "x'y",
            "ok_1-2",
            "a$b",
            "-n",
            "a;b",
            "`id`",
            "  bordi  ",
        )
        for passo in (nome_scritto(nome), attendi(1.5))
    ),
    vmc(False),
    nome_scritto("Salotto"),
    attendi(4.5),
)

# --- la VMC finta e i file .sh veri ------------------------------------------------------


class VmcFinta:
    """La VMC dei due lati: annota i comandi ricevuti."""

    def __init__(self, registro: list[Any]) -> None:
        self.registro = registro
        self.risponde = True

    def comando(self, testo: str) -> bool:
        self.registro.append((_norma(dt_util.utcnow()), "vmc", testo))
        return self.risponde


class FileSh:
    """Il file .sh del nome, vero, in una cartella di prova, con un ``nc`` finto (annota
    ciò che riceve)."""

    def __init__(self, cartella: Path) -> None:
        self.cartella = cartella
        nc = cartella / "nc"
        nc.write_text('#!/bin/sh\ncat >> "$NC_USCITA"\n', encoding="utf-8")
        nc.chmod(0o755)
        self.uscita = cartella / "uscita_nc"
        self.nome = cartella / "cambio_nome.sh"
        shutil.copy(PACKAGE / "vmc_master_script_cambio_nome.sh", self.nome)

    def _esegui(self, file: Path, argomenti: list[str]) -> int:
        ambiente = {
            "PATH": f"{self.cartella}:{os.environ['PATH']}",
            "NC_USCITA": str(self.uscita),
        }
        return subprocess.run(
            ["bash", str(file), *argomenti],
            env=ambiente,
            capture_output=True,
            check=False,
            timeout=30,
        ).returncode

    def cambia_nome(self, argomenti: list[str]) -> tuple[int, list[str]]:
        """Il file .sh del nome: codice d'uscita e righe arrivate a nc."""
        self.uscita.write_bytes(b"")
        codice = self._esegui(self.nome, argomenti)
        ricevuto = self.uscita.read_bytes().decode()
        return codice, ricevuto.splitlines()


class ProcessoFinto:
    """Un processo finto: dura ``durata`` (0: finisce senza cedere il ciclo, come un
    comando istantaneo)."""

    def __init__(self, codice: int, durata: float) -> None:
        self.returncode: int | None = None
        self._codice = codice
        self._durata = durata
        self.pid = 1

    async def communicate(self, input: bytes | None = None) -> tuple[bytes, bytes]:
        if self._durata:
            await asyncio.sleep(self._durata)
        self.returncode = self._codice
        return b"", b""

    def kill(self) -> None:
        """Niente da fermare."""


CARTELLA_PACKAGE = "/config/packages/vmc_helty_flow/master/"


def sottoprocessi(
    monkeypatch: pytest.MonkeyPatch, vmc_finta: VmcFinta, file_sh: FileSh
) -> list[str]:
    """Il sottoprocesso finto di Home Assistant (come fakevmc.py, con i file .sh
    veri); restituisce le righe di comando eseguite."""
    eseguiti: list[str] = []

    def processo(argomenti: list[str], riga: str) -> ProcessoFinto:
        eseguiti.append(riga)
        if riga.startswith("printf 'VMWH"):
            codice = riga.split("'")[1].removesuffix("\\n")
            ok = vmc_finta.comando(codice)
            return ProcessoFinto(
                0 if ok else 1, DURATA_COMANDO if ok else DURATA_SENZA_VMC
            )
        if argomenti[:2] == [
            "bash",
            CARTELLA_PACKAGE + "vmc_master_script_cambio_nome.sh",
        ]:
            codice, righe = file_sh.cambia_nome(argomenti[2:])
            if not righe:
                return ProcessoFinto(codice, 0)
            assert len(righe) == 1
            ok = vmc_finta.comando(righe[0])
            return ProcessoFinto(
                0 if ok else 1, DURATA_COMANDO if ok else DURATA_SENZA_VMC
            )
        if riga.startswith("find "):
            return ProcessoFinto(0, 0)
        raise AssertionError(f"comando inatteso: {riga}")

    async def shell(riga: str, *_: Any, **__: Any) -> ProcessoFinto:
        return processo([], riga)

    async def esegui(*argomenti: str, **__: Any) -> ProcessoFinto:
        return processo(list(argomenti), " ".join(argomenti))

    monkeypatch.setattr(asyncio, "create_subprocess_shell", shell)
    monkeypatch.setattr(asyncio, "create_subprocess_exec", esegui)
    return eseguiti


def collegamenti(vmc_finta: VmcFinta) -> dict[str, Any]:
    """``invia`` del motore verso la VMC finta, con i tempi di nc."""

    async def invia(testo: str) -> str:
        if vmc_finta.comando(testo):
            await asyncio.sleep(DURATA_COMANDO)
            return ""
        await asyncio.sleep(DURATA_SENZA_VMC)
        raise ErroreVMC("la VMC non risponde")

    return {"invia": invia}


# --- la corsa ----------------------------------------------------------------------------


def _forma(contesto: Context | None) -> str:
    """La forma del contesto (come il simulatore): u = utente, p = figlio."""
    if contesto is None:
        return ""
    return ("u" if contesto.user_id else "") + ("p" if contesto.parent_id else "")


def _tolto(evento: Event, motore: bool) -> str | None:
    """Il tipo di un evento che c'è solo da un lato (None: si confronta)."""
    tipo, dati = evento.event_type, evento.data
    if tipo == EVENT_STATE_CHANGED:
        dominio = dati["entity_id"].split(".", 1)[0]
        if dominio in ("script", "button"):
            return f"state_changed {dominio}"
    elif tipo == EVENT_CALL_SERVICE and dati["domain"] in (
        "script",
        "shell_command",
        "button",
    ):
        return f"call_service {dati['domain']}"
    elif tipo == "script_started":
        return tipo
    return None


@pytest.fixture
def moduli() -> Iterator[list[str]]:
    nomi: list[str] = []
    yield nomi
    import sys

    for nome in nomi:
        sys.modules.pop(nome, None)


async def _corsa(
    freezer: FrozenDateTimeFactory,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    nome: str,
    configurazione: dict[str, Any],
    passi: list[tuple[Any, ...]],
    *,
    motore: bool,
    moduli: list[str],
) -> tuple[list[Any], Counter[str]]:
    freezer.move_to(T0)
    registro: list[Any] = []
    # quando finiscono le chiamate della scheda: a parte, perché la pressione di un
    # pulsante (servizio di un'entità: il metodo dell'entità gira in un task suo,
    # _handle_single_entity_call) restituisce un giro del ciclo degli eventi dopo la
    # chiamata di oggi, nello stesso istante
    fine: list[Any] = []
    tolti: Counter[str] = Counter()
    vmc_finta = VmcFinta(registro)
    cartella = tmp_path / ("motore" if motore else "home_assistant")
    cartella.mkdir()
    eseguiti = sottoprocessi(monkeypatch, vmc_finta, FileSh(cartella))
    comandi = leggi_comandi()
    async with async_test_home_assistant() as hass:
        assert await async_setup_component(hass, "homeassistant", {})
        for dominio, voci in AIUTANTI.items():
            assert await async_setup_component(hass, dominio, {dominio: voci})

        async def registra(chiamata: ServiceCall) -> None:
            if chiamata.data.get("errore"):
                raise HomeAssistantError("errore voluto")

        hass.services.async_register("prova", "registra", registra)
        # l'utente della scheda (un pulsante, come ogni entità, controlla i permessi)
        utente = await hass.auth.async_create_user("Utente della scheda")
        automazioni = configurazione.get("automation", [])
        script = configurazione.get("script", {})
        m: Motore | None = None
        if motore:
            testo_modelli, testo_motore = await traduci_configurazione(
                hass,
                automazioni,
                script,
                nome_modelli=f"interni_{nome}_modelli",
                comandi=comandi,
            )
            moduli.append(f"{generato.__name__}.interni_{nome}_modelli")
            moduli.append(f"{generato.__name__}.interni_{nome}_motore")
            _carica(f"interni_{nome}_modelli", testo_modelli)
            codice = _carica(f"interni_{nome}_motore", testo_motore)
            m = Motore(hass)
            await m.avvia(
                crea=codice.crea, comandi=codice.comandi, **collegamenti(vmc_finta)
            )
            # i pulsanti di cui la prova ha lo script o il comando
            assert await async_setup_component(hass, "button", {})
            presenti = {f"script.{k}" for k in script} | {
                f"comando.{k}" for k in comandi
            }
            pulsanti = [
                PulsanteVMC(m.c, chiave)
                for chiave, voce in PULSANTI.items()
                if f"{voce['tipo']}.vmc_master_{chiave.split('.', 1)[1]}" in presenti
            ]
            piattaforma = MockEntityPlatform(
                hass, domain="button", platform_name="vmc_master"
            )
            await piattaforma.async_add_entities(pulsanti)
        else:
            assert await async_setup_component(
                hass, "shell_command", {"shell_command": comandi}
            )
            assert await async_setup_component(hass, "script", {"script": script})
            assert await async_setup_component(
                hass, "automation", {"automation": automazioni}
            )
        await _gira(hass)

        @callback
        def annota(evento: Event) -> None:
            if evento.event_type not in EVENTI:
                return
            if (tipo := _tolto(evento, motore)) is not None:
                tolti[tipo] += 1
                return
            dati = evento.data
            if evento.event_type == EVENT_STATE_CHANGED:
                dati = {"entity_id": dati["entity_id"], "new_state": dati["new_state"]}
            registro.append(
                (
                    _norma(evento.time_fired),
                    evento.event_type,
                    _norma(dict(dati)),
                    _forma(evento.context),
                )
            )

        compiti: list[asyncio.Future[None]] = []

        async def chiama(
            indice: int,
            dominio: str,
            nome_servizio: str,
            dati: dict[str, Any],
            contesto: Context | None,
        ) -> None:
            try:
                await hass.services.async_call(
                    dominio, nome_servizio, dati, blocking=True, context=contesto
                )
            except Exception as err:  # noqa: BLE001
                fine.append((_norma(dt_util.utcnow()), indice, type(err).__name__))
                return
            fine.append((_norma(dt_util.utcnow()), indice))

        togli = hass.bus.async_listen(MATCH_ALL, annota)
        if motore:
            # gli stati delle logiche (le automazioni del motore) non sono nella macchina
            # degli stati: entrano nel registro nel punto del bus di state_changed
            smetti = stati_logiche(hass).osserva(
                callback(lambda e: annota(e) if e.event_type == EVENT_STATE_CHANGED else None)
            )
        for indice, passo in enumerate(passi):
            if passo[0] in ("servizio", "scheda"):
                dominio, nome_servizio = passo[1].split(".")
                dati = dict(passo[2])
                contesto = Context(user_id=utente.id) if passo[0] == "scheda" else None
                if motore and passo[0] == "scheda":
                    # con il motore la scheda preme il pulsante dello script o del comando
                    if dominio == "script":
                        oggetto = dati.pop("entity_id").split(".", 1)[1]
                    else:
                        oggetto = nome_servizio
                    assert not dati
                    dominio, nome_servizio = "button", "press"
                    dati = {"entity_id": f"button.{oggetto}"}
                # come la scheda: la chiamata non blocca i passi (un comando dura), si
                # annota quando finisce
                compiti.append(
                    asyncio.ensure_future(
                        chiama(indice, dominio, nome_servizio, dati, contesto)
                    )
                )
                await _gira(hass)
            elif passo[0] == "vmc":
                vmc_finta.risponde = passo[1]
            else:
                await _avanza(hass, freezer, passo[1])
        togli()
        assert all(compito.done() for compito in compiti)
        if m is not None:
            smetti()
            # le logiche si staccano, poi gli script del motore si fermano
            await m.ferma()
        else:
            await hass.services.async_call(
                "automation", "turn_off", {"entity_id": "all"}, blocking=True
            )
            await hass.services.async_call(
                "script", "turn_off", {"entity_id": "all"}, blocking=True
            )
        await _gira(hass)
        await hass.async_stop(force=True)
    if not motore:
        tolti["processi"] = len(eseguiti)
    else:
        assert not eseguiti
    return [*registro, ("fine delle chiamate della scheda", fine)], tolti


def _confronta(atteso: list[Any], ottenuto: list[Any]) -> None:
    if ottenuto == atteso:
        return
    diff = "\n".join(
        difflib.unified_diff(
            [repr(v) for v in atteso],
            [repr(v) for v in ottenuto],
            "home_assistant",
            "motore",
            lineterm="",
            n=3,
        )
    )
    pytest.fail(f"registri diversi:\n{diff}")


@pytest.mark.usefixtures("ordine_dei_timer")
@pytest.mark.parametrize("nome", sorted(SCENARI))
async def test_come_home_assistant(
    nome: str,
    freezer: FrozenDateTimeFactory,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    moduli: list[str],
) -> None:
    """Stesso registro con gli script e i comandi di Home Assistant e con quelli del
    motore (tolti gli eventi che non ci sono più e quelli nuovi dei pulsanti)."""
    testo_conf, passi = SCENARI[nome]
    configurazione = yaml.safe_load(testo_conf)
    atteso, tolti_ha = await _corsa(
        freezer, monkeypatch, tmp_path, nome, configurazione, passi,
        motore=False, moduli=moduli,
    )  # fmt: skip
    ottenuto, tolti_motore = await _corsa(
        freezer, monkeypatch, tmp_path, nome, configurazione, passi,
        motore=True, moduli=moduli,
    )  # fmt: skip
    assert any(v[1] == EVENT_CALL_SERVICE and v[2]["domain"] == "prova" for v in atteso)
    CONTEGGI[nome] = Counter(
        {("home_assistant", k): v for k, v in tolti_ha.items()}
        | {("motore", k): v for k, v in tolti_motore.items()}
    )
    # gli stati delle logiche (le automazioni del motore) non passano dal bus: possono
    # passare prima degli eventi che Home Assistant tiene in coda (nel_canale)
    _confronta(
        ordine_esterno(atteso, stato_di_logica), ordine_esterno(ottenuto, stato_di_logica)
    )


# --- i casi che il package non usa ---------------------------------------------------------

CASI_LIMITE = """
script:
  vmc_master_uno:
    sequence:
      - delay: 10
  vmc_master_due:
    sequence: []
automation:
  - alias: Ascolta
    triggers:
      - trigger: state
        entity_id: input_boolean.a
      - trigger: event
        event_type: call_service
        event_data:
          domain: shell_command
          service: vmc_master_velocita_1
    actions: []
"""


async def test_casi_limite(
    hass: HomeAssistant,
    moduli: list[str],
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Gli script e i comandi del motore nei casi che il package non usa (il traduttore
    li ferma prima): chiamate per altri script, risposte, toggle, ascoltatori che
    sbagliano, aggancio impossibile, scaricamento."""
    configurazione = yaml.safe_load(CASI_LIMITE)
    testo_modelli, testo_motore = await traduci_configurazione(
        hass,
        configurazione["automation"],
        configurazione["script"],
        nome_modelli="interni_casi_limite_modelli",
        comandi=leggi_comandi(),
    )
    moduli.append(f"{generato.__name__}.interni_casi_limite_modelli")
    moduli.append(f"{generato.__name__}.interni_casi_limite_motore")
    _carica("interni_casi_limite_modelli", testo_modelli)
    codice = _carica("interni_casi_limite_motore", testo_motore)
    inviati: list[str] = []

    async def invia(testo: str) -> str:
        inviati.append(testo)
        return ""

    m = Motore(hass)
    await m.avvia(crea=codice.crea, comandi=codice.comandi, invia=invia)
    interni, comandi = m.c.interni, m.c.comandi
    assert interni is not None
    assert comandi is not None
    contesto = Context()

    # quali chiamate script.* sono per il motore
    assert not interni.gestisce("reload", {}, {})
    assert not interni.gestisce("turn_on", {}, {})
    assert not interni.gestisce("turn_on", {}, {"entity_id": "non valido"})
    assert not interni.gestisce("turn_on", {"entity_id": "all"}, {})
    assert not interni.gestisce("turn_on", {}, {"entity_id": ["script.altro"]})
    assert interni.gestisce("turn_off", {"entity_id": "script.vmc_master_uno"}, {})
    with pytest.raises(HomeAssistantError, match="script del motore e altri"):
        interni.gestisce(
            "toggle", {}, {"entity_id": ["script.vmc_master_uno", "script.altro"]}
        )

    # risposta: {} dalla chiamata diretta (fuori da ogni script), errore per turn_on
    assert await interni.chiama("vmc_master_due", {}, {}, contesto, risposta=True) == {}
    with pytest.raises(probatio.Invalid, match="does not support 'response_variable'"):
        await interni.chiama(
            "turn_on",
            {},
            {"entity_id": ["script.vmc_master_due"]},
            contesto,
            risposta=True,
        )

    # turn_off senza script del motore: nulla; toggle: avvia, poi ferma
    assert (
        await interni.chiama("turn_off", {}, {"entity_id": ["script.altro"]}, contesto)
        is None
    )
    uno = interni.script["vmc_master_uno"]
    bersaglio = {"entity_id": ["script.vmc_master_uno"]}
    await interni.chiama("toggle", {}, bersaglio, contesto)
    assert uno.in_corso
    await interni.chiama("toggle", {}, bersaglio, contesto)
    assert not uno.in_corso

    # ascoltatori dei comandi: un filtro o un ascoltatore che sbagliano finiscono nel
    # registro, gli altri sentono il comando (come il bus)
    visti: list[str] = []

    @callback
    def rotto(evento: Event) -> None:
        raise RuntimeError("ascoltatore rotto")

    @callback
    def annota(evento: Event) -> None:
        visti.append(evento.data["service"])

    togli = [
        comandi.ascolta(rotto),
        comandi.ascolta(annota, lambda dati: dati["manca"]),
        comandi.ascolta(annota),
    ]
    await comandi.esegui("vmc_master_velocita_1", {}, {}, contesto)
    await hass.async_block_till_done()
    assert visti == ["vmc_master_velocita_1"]
    assert inviati == ["VMWH0000001"]
    assert "Error in event filter" in caplog.text
    assert "Error running job" in caplog.text
    for funzione in togli:
        funzione()

    # un trigger segnato che non si sa agganciare: errore, e nulla resta agganciato
    ascoltatori = len(comandi._ascoltatori)
    segnato = {
        "aggancio_comandi": True,
        "event_type": ["call_service"],
        "event_data": {"domain": "shell_command", "service": "vmc_master_velocita_2"},
    }
    with pytest.raises(HomeAssistantError, match="non agganciabile"):
        comandi.aggancia_trigger(
            [segnato, {**segnato, "event_type": ["altro"]}], annota, "prova"
        )
    assert len(comandi._ascoltatori) == ascoltatori
    assert comandi.aggancia_trigger([{"trigger": "state"}], annota, "prova") is None

    # se gli altri trigger dell'automazione non si agganciano, si stacca anche il suo
    # aggancio dei comandi
    async def guasto(*argomenti: Any, **chiavi: Any) -> None:
        raise RuntimeError("trigger guasto")

    monkeypatch.setattr(
        "custom_components.vmc_master.nativa.motore.logiche.inizializza_attivazioni",
        guasto,
    )
    with pytest.raises(RuntimeError, match="trigger guasto"):
        await m.automazioni[0]._aggancia()
    assert len(comandi._ascoltatori) == ascoltatori

    # scaricati, gli script si fermano e non ripartono
    await interni.chiama("turn_on", {}, bersaglio, contesto)
    assert uno.in_corso
    await m.scarica_interni()
    assert not uno.in_corso
    with pytest.raises(RuntimeError, match="after it has been unloaded"):
        await interni.chiama("vmc_master_due", {}, {}, contesto)
    await Motore(hass).scarica_interni()
