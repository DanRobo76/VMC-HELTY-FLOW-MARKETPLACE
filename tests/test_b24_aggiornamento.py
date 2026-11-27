"""b24: il filtro che nasconde i timeout del ping della VMC nei primi 2 minuti dopo
l'avvio (la parte dell'aggiornamento con prepara.py non c'e' piu': la VMC nativa non ha
package da riscrivere)."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.vmc_master as integrazione
from custom_components.vmc_master.const import DOMAIN

IP = "192.168.1.160"


async def test_timeout_ping_nascosto_solo_nei_primi_2_minuti(hass: HomeAssistant):
    import logging

    voce = MockConfigEntry(domain=DOMAIN, unique_id="master", data={"nome": "master", "host": IP})
    voce.add_to_hass(hass)
    filtro = integrazione._FiltroPingAvvio(hass)
    adesso = [1000.0]
    filtro._ora = lambda: adesso[0]
    filtro._fine = 1000.0 + integrazione.DURATA_FILTRO_PING

    def record(testo: str) -> logging.LogRecord:
        return logging.LogRecord(
            integrazione.LOGGER_COMMAND_LINE, logging.ERROR, __file__, 1, "Timeout for command: %s", (testo,), None
        )

    ping_vmc = f"ping -c 3 -W 1 -w 4 {IP} 2>/dev/null | grep -q 'bytes from'"
    assert not filtro.filter(record(ping_vmc))
    assert filtro.filter(record("ping -c 3 -W 1 -w 4 192.168.1.99"))  # non e' una VMC
    assert filtro.filter(record(f"curl {IP}"))  # non e' il ping
    adesso[0] = 1000.0 + integrazione.DURATA_FILTRO_PING
    assert filtro.filter(record(ping_vmc))  # dopo 2 minuti gli errori si vedono


async def test_filtro_ping_installato_all_avvio(hass: HomeAssistant):
    import logging

    from homeassistant.setup import async_setup_component

    assert await async_setup_component(hass, DOMAIN, {})
    filtro = hass.data[integrazione.DATI_FILTRO_PING]
    assert filtro in logging.getLogger(integrazione.LOGGER_COMMAND_LINE).filters
    logging.getLogger(integrazione.LOGGER_COMMAND_LINE).removeFilter(filtro)
