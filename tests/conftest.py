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
