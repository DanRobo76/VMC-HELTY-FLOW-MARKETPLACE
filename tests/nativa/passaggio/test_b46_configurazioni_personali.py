"""9.0.0b46: le automazioni e gli script dell'utente che la riparazione dei nomi cambiati
controlla si leggono dalla configurazione YAML di Home Assistant (configuration.yaml con i
file inclusi e i package, quindi anche automations.yaml e scripts.yaml dell'interfaccia),
non più dalle parti interne delle integrazioni automation e script."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

import custom_components.vmc_master  # noqa: F401 - prima delle prove (spazio dei nomi)
from custom_components.vmc_master import passaggio

CONFIGURAZIONE = """
homeassistant:
  packages:
    pacchetto_utente:
      automation:
        id: nel_package_utente
        alias: Nel package
        actions:
          - action: script.vmc_master_profilo_umidita
      script:
        nel_package_script:
          sequence:
            - action: shell_command.vmc_master_velocita_1
    non_un_package: testo
automation:
  - id: con_id
    alias: Con id
    actions:
      - action: input_boolean.turn_on
        target:
          entity_id: input_boolean.vmc_master_notifica_audio
  - alias: Senza id unico
  - alias: Senza id assente
  - triggers: []
  - id: pkg_auto
    alias: Del package
  - non un dizionario
  - {}
  - id: con_progetto
    use_blueprint:
      path: mio/progetto.yaml
      input:
        quale: input_number.vmc_master_umidita_avvio
  - id: progetto_mancante
    use_blueprint:
      path: manca.yaml
  - id: progetto_strano
    use_blueprint: testo
automation altre:
  - alias: Doppia
script:
  mio:
    alias: Mio
    sequence: []
  rinominato:
    sequence: []
  pkg_script:
    sequence: []
  rotto: testo
script vuoto: testo
"""

PROGETTO = """
blueprint:
  name: Progetto
  domain: automation
actions:
  - action: timer.cancel
    target:
      entity_id: timer.vmc_master_progetto
"""


async def test_automazioni_e_script_dalla_configurazione(
    hass: HomeAssistant, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Ogni automazione e script dell'utente con il suo entity_id: dal registro (anche
    rinominato), dallo stato con il suo nome per un'automazione senza id (se è uno solo),
    altrimenti il suo nome; quelli del package e le voci non valide restano fuori; il
    progetto (blueprint) usato fa parte del testo."""
    hass.config.config_dir = str(tmp_path)
    (tmp_path / "configuration.yaml").write_text(CONFIGURAZIONE, encoding="utf-8")
    progetti = tmp_path / "blueprints" / "automation" / "mio"
    progetti.mkdir(parents=True)
    (progetti / "progetto.yaml").write_text(PROGETTO, encoding="utf-8")
    registro = er.async_get(hass)
    registro.async_get_or_create(
        "automation", "automation", "con_id", suggested_object_id="con_id_rinominata"
    )
    registro.async_get_or_create(
        "script", "script", "rinominato", suggested_object_id="altro_nome"
    )
    hass.states.async_set("automation.senza_id_unico", "on", {"friendly_name": "Senza id unico"})
    # con lo stesso nome ma con un id: è un'altra automazione (nel registro)
    hass.states.async_set(
        "automation.finta", "on", {"friendly_name": "Senza id unico", "id": "finta"}
    )
    hass.states.async_set("automation.doppia", "on", {"friendly_name": "Doppia"})
    hass.states.async_set("automation.doppia_2", "on", {"friendly_name": "Doppia"})
    id_package = {
        ("automation", "automation", "pkg_auto"),
        ("script", "script", "pkg_script"),
    }

    with caplog.at_level(logging.DEBUG, logger=passaggio.__name__):
        personali = await passaggio._async_configurazioni_personali(hass, id_package)

    assert [dove for dove, _ in personali] == [
        "automation.con_id_rinominata",
        "automation.senza_id_unico",
        "automation: Senza id assente",
        "automation: -",
        "automation: con_progetto",
        "automation: progetto_mancante",
        "automation: progetto_strano",
        "automation: Doppia",
        "script.mio",
        "script.altro_nome",
        "automation: Nel package",
        "script.nel_package_script",
    ]
    testi = dict(personali)
    assert "input_boolean.vmc_master_notifica_audio" in testi["automation.con_id_rinominata"]
    progetto = testi["automation: con_progetto"]
    assert "input_number.vmc_master_umidita_avvio" in progetto
    assert "timer.vmc_master_progetto" in progetto
    assert "shell_command.vmc_master_velocita_1" in testi["script.nel_package_script"]
    assert "Progetto manca.yaml non letto" in caplog.text


@pytest.mark.parametrize(
    "generale",
    ["", "homeassistant: testo\n", "homeassistant:\n  packages: testo\n"],
    ids=["senza_homeassistant", "homeassistant_non_valido", "packages_non_validi"],
)
async def test_senza_package(hass: HomeAssistant, tmp_path: Path, generale: str) -> None:
    """Senza package (o con valori non validi) si leggono solo le voci principali."""
    hass.config.config_dir = str(tmp_path)
    (tmp_path / "configuration.yaml").write_text(
        generale + "script:\n  solo:\n    sequence: []\n", encoding="utf-8"
    )
    personali = await passaggio._async_configurazioni_personali(hass, set())
    assert [dove for dove, _ in personali] == ["script.solo"]


@pytest.mark.parametrize(
    "testo",
    [None, "automation: !include manca.yaml\n", "- non un dizionario\n"],
    ids=["senza_file", "inclusione_mancante", "non_un_dizionario"],
)
async def test_configurazione_non_letta(
    hass: HomeAssistant,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    testo: str | None,
) -> None:
    """Configurazione che non si legge: nessuna voce, un avviso nel registro (la
    riparazione controlla comunque le plance)."""
    hass.config.config_dir = str(tmp_path)
    if testo is not None:
        (tmp_path / "configuration.yaml").write_text(testo, encoding="utf-8")
    assert await passaggio._async_configurazioni_personali(hass, set()) == []
    assert "Configurazione di Home Assistant non letta" in caplog.text
