"""Variante di prova del confronto (non e' un motore): ogni chiamata tts.google_translate_say parte 10 ms
virtuali dopo. Imita un motore con un piccolo ritardo negli avvisi audio, che i 17.264 scenari di gen.py
non eseguono mai.

Il differenziale contro «identica» sulla famiglia M deve trovare una differenza esattamente negli scenari
con un avviso audio (una voce C tts.google_translate_say nella traccia di A), e nessuna negli altri.
"""
import asyncio


def prepara_configurazione(cfg_dir: str) -> None:
    """Nessuna modifica alla configurazione."""


async def avvia(hass) -> None:
    from homeassistant.core import ServiceRegistry
    orig = ServiceRegistry.async_call

    async def async_call(reg, domain, service, *a, **k):
        if domain == 'tts' and service == 'google_translate_say':
            await asyncio.sleep(0.01)
        return await orig(reg, domain, service, *a, **k)

    ServiceRegistry.async_call = async_call
