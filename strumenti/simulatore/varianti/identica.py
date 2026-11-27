"""Variante «identica»: non cambia niente (automazioni e script YAML di oggi).

Serve come lato A del differenziale e, contro se stessa, a provare che il simulatore e' deterministico.
"""


def prepara_configurazione(cfg_dir: str) -> None:
    """Nessuna modifica alla configurazione generata da build_config.py."""


async def avvia(hass) -> None:
    """Nessun motore da agganciare."""
