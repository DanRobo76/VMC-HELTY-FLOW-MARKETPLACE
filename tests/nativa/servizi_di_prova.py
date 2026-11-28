"""I servizi delle scritture del motore registrati in un dominio di prova.

L'integrazione non registra servizi (hassfest vuole services.yaml per ogni servizio
registrato): le prove registrano gli stessi servizi di ``ScritturaComandi`` in un loro
dominio, per confrontarli con quelli degli aiutanti, evento ``call_service`` compreso.
"""

from __future__ import annotations

from functools import partial

from homeassistant.helpers.service import entity_service_call

from custom_components.vmc_master.nativa.comandi import SERVIZI_MOTORE, ScritturaComandi


def registra_servizi(scrittura: ScritturaComandi, dominio: str) -> dict[str, str]:
    """Registra i servizi in ``dominio`` («<dominio>.input_boolean_turn_on»...).

    Restituisce servizio di oggi -> servizio registrato (per la mappa dei nomi).
    """
    nomi: dict[str, str] = {}
    for servizio, (schema, _) in SERVIZI_MOTORE.items():
        nome = servizio.replace(".", "_")
        scrittura.hass.services.async_register(
            dominio,
            nome,
            partial(
                entity_service_call,
                scrittura.hass,
                scrittura._entita(servizio.split(".", 1)[0]),
                scrittura._funzioni[servizio],
            ),
            schema,
        )
        nomi[servizio] = f"{dominio}.{nome}"
    return nomi
