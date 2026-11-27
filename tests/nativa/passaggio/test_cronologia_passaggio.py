"""La cronologia dei sensori continua dopo il passaggio dalla beta: con il registro
(recorder) vero di Home Assistant su un database in un file, comune alle tre istanze
(A la beta, B il primo avvio con la conferma, C la VMC nativa), gli stati dei sensori
nativi si scrivono sotto le stesse righe di ``states_meta`` dei sensori della beta."""

from __future__ import annotations

from pathlib import Path

import pytest
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.db_schema import States, StatesMeta
from homeassistant.components.recorder.util import session_scope
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.components.recorder.common import (
    async_wait_recording_done,
)
from sqlalchemy import func, select

from .banco import (
    aggiungi_e_avvia,
    carica_package,
    conferma_dalla_riparazione,
    entity_id_attesi,
    riavvio,
    scrivi_package_beta,
    senza_rete,
    voce,
)


# Il registro va preparato prima di Home Assistant: qui le due impostazioni comuni dei
# test (conftest.py) chiedono prima il registro.
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(async_test_recorder, enable_custom_integrations):
    """Integrazioni personalizzate abilitate, dopo il registro."""
    yield


@pytest.fixture(autouse=True)
def cartella_config_temporanea(async_test_recorder, hass, tmp_path):
    """Cartella di configurazione temporanea, dopo il registro."""
    hass.config.config_dir = str(tmp_path)
    yield


@pytest.fixture(autouse=True)
def rete_finta():
    with senza_rete():
        yield


async def _righe(hass: HomeAssistant, nome: str) -> dict[str, tuple[int, int]]:
    """entity_id -> (metadata_id, numero di stati) delle righe di states_meta della VMC."""
    await async_wait_recording_done(hass)

    def leggi() -> dict[str, tuple[int, int]]:
        with session_scope(hass=hass, read_only=True) as sessione:
            righe = sessione.execute(
                select(
                    StatesMeta.entity_id,
                    StatesMeta.metadata_id,
                    func.count(States.state_id),
                )
                .outerjoin(States, States.metadata_id == StatesMeta.metadata_id)
                .where(StatesMeta.entity_id.like(f"%.vmc_{nome}_%"))
                .group_by(StatesMeta.metadata_id)
            ).all()
        return {
            entity_id: (metadata_id, stati) for entity_id, metadata_id, stati in righe
        }

    return await get_instance(hass).async_add_executor_job(leggi)


@pytest.mark.parametrize("persistent_database", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_cronologia_dei_sensori_continua(
    async_test_recorder, hass: HomeAssistant, tmp_path: Path
) -> None:
    config_dir = str(tmp_path)
    master = voce("master")
    cartella = scrivi_package_beta(config_dir, "master", master.data["host"])

    async with async_test_recorder(hass):
        await carica_package(hass, [cartella])
        righe_a = await _righe(hass, "master")
        sensori_a = {
            e: r
            for e, r in righe_a.items()
            if e.split(".", 1)[0] in ("sensor", "binary_sensor")
        }
        # i sensori del package con almeno uno stato registrato
        assert len(sensori_a) == 137
        assert all(stati > 0 for _, stati in sensori_a.values())

        async with (
            riavvio(hass, [master], config_dir) as beta,
            async_test_recorder(beta),
        ):
            await carica_package(beta, [cartella])
            await aggiungi_e_avvia(beta, [])
            passo = await conferma_dalla_riparazione(beta)
            assert passo["step_id"] == "confirm"
            righe_b = await _righe(beta, "master")

            async with (
                riavvio(beta, [master], config_dir) as nativa,
                async_test_recorder(nativa),
            ):
                await aggiungi_e_avvia(nativa, [])
                righe_c = await _righe(nativa, "master")

    # stessi metadata_id per i 137 sensori, con stati nuovi scritti dalla VMC nativa; il
    # sensore che verificava l'IP della scheda non c'è più (b46): nessuno stato nuovo
    tolto = "sensor.vmc_master_verifica_ip_inserito"
    assert {e: righe_c[e][0] for e in sensori_a} == {
        e: m for e, (m, _) in sensori_a.items()
    }
    assert all(righe_c[e][1] > righe_b[e][1] for e in sensori_a if e != tolto)
    assert righe_c[tolto][1] == righe_b[tolto][1]
    # nessuna riga nuova «..._2»: le righe nuove sono solo entità native con il loro nome
    nuove = set(righe_c) - set(righe_b)
    assert nuove <= entity_id_attesi("master")
    assert len(nuove) == 367 - 136
