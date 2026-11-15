"""Impostazioni comuni dei test."""

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Abilita le integrazioni personalizzate in tutti i test."""
    yield


@pytest.fixture(autouse=True)
def cartella_config_temporanea(hass, tmp_path):
    """Ogni test scrive packages e backup in una cartella sua."""
    hass.config.config_dir = str(tmp_path)
    yield
