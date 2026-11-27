"""«IP già in uso»: i sensori IP delle altre VMC, come ``states.sensor`` nel template."""

from __future__ import annotations

from custom_components.vmc_master.nativa.lettore import Lettore
from custom_components.vmc_master.nativa.modelli import Calcolo
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.util import dt as dt_util

from . import confronto as c

ALTRE = (
    [],
    [("sensor.vmc_sala_ip", "192.168.1.60", {})],
    [("sensor.vmc_sala_ip", " 192.168.1.60 ", {})],
    [("sensor.vmc_sala_ip", "192.168.1.60", {"restored": True})],  # ripristinato: non conta
    [("sensor.vmc_sala2_ip", "192.168.1.60", {})],  # nome con cifre: non è una VMC
    [("sensor.vmc_cucina_ip", "192.168.1.60", {"restored": False})],
    [("sensor.vmc_sala_ip", "192.168.1.61", {}), ("sensor.vmc_cucina_ip", "192.168.1.60", {})],
)


async def test_ip_in_uso_uguale_al_template(hass: HomeAssistant) -> None:
    """Stesso esito del template per ogni combinazione di altre VMC e IP inserito."""
    tpl = Template(c.modelli()[f"sensor.vmc_{c.NOME}_verifica_ip_inserito"]["conf"]["state"], hass)

    def stato(entity_id: str) -> str | None:
        s = hass.states.get(entity_id)
        return None if s is None else s.state

    visti = set()
    for altre in ALTRE:
        for eid in [s.entity_id for s in hass.states.async_all("sensor")]:
            hass.states.async_remove(eid)
        hass.states.async_set(f"sensor.vmc_{c.NOME}_ip", c.IP)
        for eid, valore, attributi in altre:
            hass.states.async_set(eid, valore, attributi)
        for inserito in ("192.168.1.60", "192.168.1.61", c.IP, "", "10.0.0.7"):
            hass.states.async_set(f"input_text.vmc_{c.NOME}_ip_insert", inserito)
            hass.states.async_set(f"input_text.vmc_{c.NOME}_ip_insert_esito", f"ok {inserito}")
            atteso = tpl.async_render(parse_result=False)
            calcolo = Calcolo(lambda k: stato(lettore.entity_id(k)))
            lettore = Lettore(
                c.NOME,
                calcolo.valore,
                stato,
                dt_util.now,
                lambda k, n: None,
                lambda e, n: None,
                ip=c.IP,
                elenca=hass.states.async_all,
            )
            calcolo.lettore = lettore
            assert calcolo.valore("sensor.verifica_ip_inserito") == atteso, (altre, inserito)
            visti.add(atteso)
    assert {"IP già in uso", "IP già impostato", "Nessun IP", "192.168.1.60"} <= visti
