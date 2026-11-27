"""Sostituti delle entità native della VMC Master, solo per l'anteprima della scheda.

Le entità native degli altri lavori della fase 4 non ci sono ancora: per ogni aiutante,
script o comando di shell che domani resta visibile c'è qui un'entità con l'entity_id di
domani (colonna «Domani» di ``aiutanti_fase1.csv``), il nome e l'icona di oggi, che segue
lo stato dell'entità di oggi e le gira i comandi:

- switch / binary_sensor <- input_boolean (accendi e spegni -> input_boolean.turn_on/off);
- number <- input_number (min, max, step, mode, unità; imposta -> input_number.set_value);
- select <- input_select (opzioni; scegli -> input_select.select_option);
- text <- input_text (min, max, pattern, mode; imposta -> input_text.set_value);
- time <- input_datetime (imposta -> input_datetime.set_datetime);
- button <- script (premi -> script.turn_on) o comando di shell (premi -> shell_command.*);
- sensor <- timer (classe timestamp: ora di fine mentre il timer gira, altrimenti unknown),
  input_number, input_select, input_text (lo stato).

Le classi sono quelle di Home Assistant (SwitchEntity, NumberEntity...): gli attributi
sono quelli che Home Assistant scrive per quel dominio. Nome e icona sono quelli
dell'entità di oggi. L'elenco («voci») e la tabella oggi -> domani («mappa», per i selettori
che contengono un nome di entità) sono nel file ``sostituti_vmc.json`` della cartella di
configurazione (lo scrive ``banco.py``).
"""

from __future__ import annotations

import json
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType

DOMINIO = "sostituti_vmc"
PIATTAFORME = (
    "binary_sensor",
    "button",
    "number",
    "select",
    "sensor",
    "switch",
    "text",
    "time",
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Legge l'elenco dei sostituti e carica le piattaforme."""
    percorso = Path(hass.config.config_dir) / "sostituti_vmc.json"
    hass.data[DOMINIO] = json.loads(
        await hass.async_add_executor_job(percorso.read_text, "utf-8")
    )
    for piattaforma in PIATTAFORME:
        hass.async_create_task(
            async_load_platform(hass, piattaforma, DOMINIO, {}, config)
        )
    return True
