"""L'aggiornamento dalla beta: quando Home Assistant si ferma con la versione nativa già
su disco, la beta (b24-b41) cerca ``prepara.py`` nella versione nuova per riscrivere i
package prima del riavvio (``_versione_su_disco``: «se non c'è prepara.py, niente»).
La versione nativa non ce l'ha: al primo avvio nativo il package della beta è quello
che la beta ha lasciato, caricato com'era, e i valori si leggono da lì."""

from __future__ import annotations

from pathlib import Path

import custom_components.vmc_master as integrazione

CARTELLA = Path(integrazione.__file__).parent


def test_nessun_prepara_per_la_beta() -> None:
    assert not (CARTELLA / "prepara.py").exists()


def test_nessun_codice_che_scrive_il_package() -> None:
    """Nessun modulo dell'integrazione scrive, sposta o copia file del package: restano
    solo la lettura (passaggio.py) e la rimozione confermata dall'utente."""
    sospetti = []
    for modulo in CARTELLA.rglob("*.py"):
        if "generato" in modulo.parts:
            continue
        testo = modulo.read_text(encoding="utf-8")
        for parola in (
            "vmc_master_backup",
            "sposta_in_backup",
            "def installa(",
            "def _scrivi(percorso",
        ):
            if parola in testo:
                sospetti.append(f"{modulo.relative_to(CARTELLA)}: {parola}")
    assert sospetti == ["trasforma.py: vmc_master_backup"]  # solo il testo della beta
