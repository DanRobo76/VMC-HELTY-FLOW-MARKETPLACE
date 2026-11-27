"""Impostazioni comuni dei test."""

# Home Assistant 2026.11 va importato prima del plugin dei test: al primo import fa
# di «httpx» un alias di «httpx2» e si ferma se httpx è già stato importato (dal
# plugin, tramite respx). Per questo pytest.ini disattiva il caricamento automatico
# del plugin (-p no:homeassistant) e il plugin viene caricato qui, dopo HA.
import homeassistant  # noqa: F401  # isort:skip
from homeassistant.components import logger as _logger  # isort:skip

# Il plugin 0.13.375 (l'ultimo, per HA 2026.10) importa _clear_logger_overwrites dal
# modulo logger, da dove HA 2026.11 l'ha spostato in logger.helpers.
if not hasattr(_logger, "_clear_logger_overwrites"):
    from homeassistant.components.logger import helpers as _logger_helpers

    _logger._clear_logger_overwrites = _logger_helpers._clear_logger_overwrites

import pytest  # noqa: E402

pytest_plugins = ["pytest_homeassistant_custom_component.plugins"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Abilita le integrazioni personalizzate in tutti i test."""
    yield


@pytest.fixture(autouse=True)
def cartella_config_temporanea(hass, tmp_path):
    """Ogni test scrive packages e backup in una cartella sua."""
    hass.config.config_dir = str(tmp_path)
    yield


@pytest.fixture(autouse=True)
def vmc_nativa_senza_rete(request):
    """Fuori da tests/nativa nessuna prova parla con una VMC: una voce aggiunta avvia la
    VMC nativa con la VMC finta del banco del passaggio (non risponde), il ping fuori
    linea e la versione fissa. Il nome letto dalla VMC resta quello di ogni prova."""
    if "nativa" in request.node.path.parts:
        yield
        return
    from tests.nativa.passaggio.banco import senza_rete

    with senza_rete(anche_il_nome=False):
        yield


@pytest.fixture(autouse=True)
def nessun_apparecchio_agli_ip():
    """Nessuna prova apre la porta 5001 o fa il ping per vedere se a un IP c'è un
    apparecchio che non è una VMC: per tutte a quell'IP non risponde niente. Le prove di
    quel controllo usano la funzione vera (tests/test_b44_apparecchio.py)."""
    from unittest.mock import AsyncMock, patch

    with patch(
        "custom_components.vmc_master.config_flow.async_apparecchio_presente",
        AsyncMock(return_value=False),
    ):
        yield
