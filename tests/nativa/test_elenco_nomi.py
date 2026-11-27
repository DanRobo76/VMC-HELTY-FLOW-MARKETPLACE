"""L'elenco dei nomi cambiati (NOMI_NATIVI.md) è quello generato; i README non hanno più il riepilogo."""

from __future__ import annotations

from collections import Counter

import pytest

from .genera_elenco_nomi import (
    INTERNA,
    PAGINA,
    README,
    SEGNAPOSTO,
    gruppi,
    pagina,
    riepiloghi_nel_testo,
    voci,
)

RIGENERA = (
    "rigenerare con: /home/user/hat/bin/python -m tests.nativa.genera_elenco_nomi"
)


def test_pagina_aggiornata() -> None:
    """NOMI_NATIVI.md è esattamente quello che scrive il generatore."""
    assert PAGINA.read_text(encoding="utf-8") == pagina(), RIGENERA


@pytest.mark.parametrize("percorso", README, ids=("README.md", ".github/README.md"))
def test_readme_senza_passaggio_dalla_beta(percorso) -> None:
    """9.0.0b45: le guide non hanno più la sezione «Passaggio dalla beta» né il riepilogo
    dei nomi (l'elenco resta in NOMI_NATIVI.md, aperto dalla riparazione)."""
    testo = percorso.read_text(encoding="utf-8")
    assert riepiloghi_nel_testo(testo) == []
    assert "Passaggio dalla beta" not in testo
    assert "Switching from the beta" not in testo
    assert "NOMI_NATIVI" not in testo


def test_conteggi() -> None:
    """342 voci: 173 impostazioni che cambiano dominio, 34 timer che diventano sensori,
    25 pulsanti (13 script e 12 comandi), 110 interne (68 valori e 38 script, cioè le 106
    del solo elenco «Pulisci cronologia», più 4 comandi di shell)."""
    tutte = voci()
    assert len(tutte) == 342
    impostazioni, timer, pulsanti, interne = (g.voci for g in gruppi(tutte))
    assert Counter((v.dominio, v.domani) for v in impostazioni) == {
        ("input_boolean", "switch"): 37,
        ("input_boolean", "binary_sensor"): 77,
        ("input_number", "number"): 10,
        ("input_number", "sensor"): 1,
        ("input_select", "select"): 14,
        ("input_select", "sensor"): 1,
        ("input_text", "text"): 2,
        ("input_text", "sensor"): 1,
        ("input_datetime", "time"): 30,
    }
    assert len(impostazioni) == 173
    assert Counter((v.dominio, v.domani) for v in timer) == {("timer", "sensor"): 34}
    assert Counter(v.dominio for v in pulsanti) == {"script": 13, "shell_command": 12}
    assert Counter(v.dominio for v in interne) == {
        "input_number": 32,
        "input_text": 35,
        "input_boolean": 1,
        "script": 38,
        "shell_command": 4,
    }
    valori = [v for v in interne if v.dominio not in ("script", "shell_command")]
    script = [v for v in interne if v.dominio == "script"]
    assert (len(valori), len(script), len(valori) + len(script), len(interne)) == (
        68,
        38,
        106,
        110,
    )


def test_ogni_voce_in_un_solo_gruppo() -> None:
    """I gruppi coprono tutte le voci, ognuna una volta sola."""
    chiavi = [v.chiave for g in gruppi() for v in g.voci]
    assert sorted(chiavi) == sorted(v.chiave for v in voci())


def test_stesso_oggetto_dopo_il_punto() -> None:
    """Domani cambia solo il dominio: l'oggetto dopo il punto resta (decisione approvata)."""
    for voce in voci():
        oggi, domani = voce.per_vmc("zeta")
        assert oggi == f"{voce.dominio}.vmc_zeta_{voce.oggetto}"
        if voce.domani == INTERNA:
            assert domani is None
        else:
            assert domani == f"{voce.domani}.vmc_zeta_{voce.oggetto}"


def test_nessun_nome_di_vmc_nella_pagina() -> None:
    """Nella pagina il nome della VMC è sempre ‹nome› (mai «master» dentro un entity_id o un
    nome), salvo la frase che spiega che la prima VMC si chiama `master`."""
    righe = pagina().split("\n")
    with_master = [r for r in righe if "master" in r.lower() and "VMC Master" not in r]
    assert all("`master`" in r for r in with_master), with_master
    assert sum(SEGNAPOSTO in r for r in righe) >= 342
