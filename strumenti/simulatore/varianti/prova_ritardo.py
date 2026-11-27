"""Variante di prova del confronto (non e' un motore): ogni chiamata shell_command.vmc_master_velocita_0
parte 10 ms virtuali dopo. Imita un motore che manda un comando alla VMC con un piccolo ritardo.

Il differenziale contro «identica» deve trovare una differenza in ogni scenario in cui qualcuno
(automazione o tasto della scheda) manda la Velocita' 0, e nessuna negli altri.
"""
import asyncio


def prepara_configurazione(cfg_dir: str) -> None:
    """Nessuna modifica alla configurazione."""


async def avvia(hass) -> None:
    from homeassistant.core import ServiceRegistry
    orig = ServiceRegistry.async_call

    async def async_call(reg, domain, service, *a, **k):
        if domain == 'shell_command' and service == 'vmc_master_velocita_0':
            await asyncio.sleep(0.01)
        return await orig(reg, domain, service, *a, **k)

    ServiceRegistry.async_call = async_call
