"""Il traduttore con script e comandi dentro il motore (fase 4, parametro ``comandi``).

Senza il parametro il codice generato resta quello di sempre (``test_traduzione.py``).
Con il parametro, rispetto al codice di sempre cambiano solo: i 17 trigger sulle
chiamate dei comandi (segnati per l'aggancio diretto), l'import di ``Comando``, la
funzione ``comandi(c)`` e i 2 modelli degli argomenti dei file .sh.
"""

from __future__ import annotations

import re
from collections import Counter

import pytest
from homeassistant.core import HomeAssistant

from custom_components.vmc_master.nativa.motore.definizioni import (
    COMANDO_IP,
    COMANDO_NESSUNO,
    COMANDO_NOME,
    COMANDO_VMC,
)

from .rinomina import Rinomina
from .traduci import (
    NonTraducibile,
    _comando,
    leggi_comandi,
    leggi_package,
    traduci_configurazione,
    traduzione,
)

AGGANCIO = ", 'enabled': False, 'aggancio_comandi': True"


def test_comandi_del_package() -> None:
    """16 comandi di shell: 13 per la VMC (12 dei tasti e il reset del filtro), il
    cambio del nome, il cambio dell'IP e la pulizia dei file .sh."""
    comandi = leggi_comandi()
    tipi = {nome: _comando(riga) for nome, riga in comandi.items()}
    assert Counter(t for t, _, _ in tipi.values()) == {
        COMANDO_VMC: 13,
        COMANDO_NOME: 1,
        COMANDO_IP: 1,
        COMANDO_NESSUNO: 1,
    }
    assert {n: t for n, (_, t, _) in tipi.items() if t} == {
        "vmc_master_freecooling": "VMWH0000007",
        "vmc_master_notturna": "VMWH0000006",
        "vmc_master_iperventilazione": "VMWH0000005",
        "vmc_master_velocita_4": "VMWH0000004",
        "vmc_master_velocita_3": "VMWH0000003",
        "vmc_master_velocita_2": "VMWH0000002",
        "vmc_master_velocita_1": "VMWH0000001",
        "vmc_master_velocita_0": "VMWH0000000",
        "vmc_master_sensori_on": "VMWH0300000",
        "vmc_master_sensori_off": "VMWH0300002",
        "vmc_master_pannello_led_on": "VMWH0100010",
        "vmc_master_pannello_led_off": "VMWH0100000",
        "vmc_master_reset_filtro": "VMWH0417744",
    }
    assert tipi["vmc_master_aggiorna_indirizzo_ip"][2] == "   {{ ip | default('') }}"
    assert tipi["vmc_master_cambia_nome"][2] == (
        " \"{{ states('input_text.vmc_master_nome_da_inserire') "
        "| replace('\"', '') | replace('\\\\', '') }}\""
    )


def test_comando_sconosciuto() -> None:
    with pytest.raises(NonTraducibile, match="comando di shell sconosciuto"):
        _comando("ls /config")


async def test_package_con_script_interni(hass: HomeAssistant) -> None:
    """Il package tradotto con gli script e i comandi dentro il motore è quello di
    sempre, salvo i 17 trigger segnati, ``Comando`` e ``comandi(c)``."""
    automazioni, script = leggi_package()
    _, _, modelli_oggi, motore_oggi = await traduzione(hass, automazioni, script)
    _, g, modelli, motore = await traduzione(
        hass, automazioni, script, comandi=leggi_comandi()
    )
    assert g.agganci == 17
    assert motore.count(AGGANCIO) == 17
    corpo, separatore, comandi = motore.partition("\n\n\ndef comandi(c):\n")
    assert separatore
    assert (
        corpo.replace(AGGANCIO, "").replace(
            "Automazione, Comando, Script", "Automazione, Script"
        )
        + "\n"
        == motore_oggi + "\n"
    )
    assert len(re.findall(r"Comando\(nome=", comandi)) == 16
    # i 2 modelli degli argomenti dei file .sh vengono dopo quelli di sempre
    assert modelli.startswith(modelli_oggi.removesuffix("\n"))
    assert modelli.count("\ndef m") == modelli_oggi.count("\ndef m") + 2


AUTOMAZIONE = {
    "alias": "Prova",
    "triggers": [{"trigger": "state", "entity_id": "input_boolean.a"}],
    "actions": [],
}


@pytest.mark.parametrize(
    ("azione", "errore"),
    [
        ({"action": "script.altro"}, "script sconosciuto"),
        ({"action": "shell_command.altro"}, "comando sconosciuto"),
        (
            {"action": "script.turn_on", "target": {"entity_id": "script.altro"}},
            "non solo script del package",
        ),
        (
            {"action": "script.turn_on", "data": {"entity_id": "script.s"}},
            "senza entity_id costante",
        ),
        (
            {"action": "script.turn_on", "target": {"entity_id": "{{ 'script.s' }}"}},
            "non solo script del package",
        ),
        (
            {"action": "shell_command.c", "response_variable": "r"},
            "con response_variable",
        ),
    ],
)
async def test_nomi_controllati(hass: HomeAssistant, azione: dict, errore: str) -> None:
    """Con script e comandi dentro il motore un nome costante deve essere del package."""
    automazione = dict(AUTOMAZIONE, actions=[azione])
    script = {"s": {"sequence": []}}
    with pytest.raises(NonTraducibile, match=errore):
        await traduci_configurazione(
            hass,
            [automazione],
            script,
            comandi={"c": "printf 'VMWH0000001\\n' | timeout 5 nc -w 3 1.2.3.4 5001"},
        )


@pytest.mark.parametrize(
    ("trigger", "errore"),
    [
        (
            {"trigger": "event", "event_type": "call_service"},
            "non agganciabile",
        ),
        (
            {
                "trigger": "event",
                "event_type": "call_service",
                "event_data": {"domain": "script", "service": "s"},
            },
            "non agganciabile",
        ),
        (
            {
                "trigger": "event",
                "event_type": "call_service",
                "event_data": {"domain": "shell_command", "service": "altro"},
            },
            "non agganciabile",
        ),
        (
            {
                "trigger": "event",
                "event_type": ["call_service", "prova"],
                "event_data": {"domain": "shell_command", "service": "c"},
            },
            "non agganciabile",
        ),
        (
            {
                "trigger": "event",
                "event_type": "call_service",
                "event_data": {"domain": "shell_command", "service": "c"},
                "context": {"user_id": "x"},
            },
            "non agganciabile",
        ),
        ({"trigger": "event", "event_type": "script_started"}, "script_started"),
    ],
)
async def test_trigger_controllati(
    hass: HomeAssistant, trigger: dict, errore: str
) -> None:
    """Un trigger sulle chiamate che con gli script interni non ci sono più (o che
    l'aggancio diretto non sa agganciare) ferma la traduzione."""
    automazione = dict(AUTOMAZIONE, triggers=[trigger])
    with pytest.raises(NonTraducibile, match=errore):
        await traduci_configurazione(
            hass,
            [automazione],
            {},
            comandi={"c": "printf 'VMWH0000001\\n' | timeout 5 nc -w 3 1.2.3.4 5001"},
        )


async def test_mappa_dei_nomi_senza_script(hass: HomeAssistant) -> None:
    """Gli script e i comandi del motore tengono i nomi di oggi: una mappa dei nomi che
    li cambia non va con loro."""
    mappa = Rinomina({"script.s": "button.s"})
    with pytest.raises(NonTraducibile, match="cambia script o comandi"):
        await traduzione(hass, [], {}, rinomina=mappa, comandi={})
