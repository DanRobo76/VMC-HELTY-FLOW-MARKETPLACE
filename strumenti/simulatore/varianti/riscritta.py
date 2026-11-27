"""Variante «riscritta»: riscrive i file del package dal YAML letto (pacchetto.riscrivi) senza togliere niente.

Il differenziale contro «identica» deve dare zero differenze: prova che la riscrittura fatta da
pacchetto.togli (quella che usera' la variante del motore nativo) non cambia il comportamento.
"""
import pacchetto


def prepara_configurazione(cfg_dir: str) -> None:
    pacchetto.riscrivi(cfg_dir)


async def avvia(hass) -> None:
    """Nessun motore da agganciare."""
