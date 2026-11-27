"""Variante di prova degli scarti dei «time change» (non e' un motore): consuma numeri casuali e crea
ascoltatori di orari che non fanno niente.

Prima dell'avvio di Home Assistant (prima che le automazioni aggancino i trigger) prende qualche numero da
random e registra due ascoltatori di orari (async_track_utc_time_change), uno dei quali annullato subito;
lo stesso ogni 7 s virtuali dopo l'avvio. Non cambia nessuno stato: il differenziale contro «identica» deve
dare zero differenze. Imita un motore che crea gli ascoltatori in un altro ordine o in numero diverso dalle
automazioni YAML. Con gli scarti casuali di Home Assistant (SIM_SCARTI=casuali) gli stessi scarti finivano
ad ascoltatori diversi e trigger e modelli con now() scattavano a frazioni di secondo diverse.
"""
import random


def prepara_configurazione(cfg_dir: str) -> None:
    """Nessuna modifica alla configurazione."""


def _disturba(hass):
    from homeassistant.helpers.event import async_track_utc_time_change

    for _ in range(3):
        random.random()

    def niente(_ora):
        pass

    async_track_utc_time_change(hass, niente, second=30)
    async_track_utc_time_change(hass, niente, second=0)()


async def prima_dell_avvio(hass) -> None:
    _disturba(hass)


async def avvia(hass) -> None:
    def battito():
        _disturba(hass)
        hass.loop.call_later(7, battito)

    hass.loop.call_later(7, battito)
