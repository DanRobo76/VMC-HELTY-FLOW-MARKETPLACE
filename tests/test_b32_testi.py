"""Prove della 9.0.0b32: testi e commenti corretti dalla verifica profonda 1:1 (licenza, nome VMC)."""

from __future__ import annotations

from pathlib import Path

from custom_components.vmc_master import trasforma

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def test_licenza_con_il_nome_dell_integrazione() -> None:
    """La riga della licenza nomina l'integrazione (una sola per tutte le VMC), non la VMC."""
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt", "vmc_master_scheda_manuale_interfaccia.txt",
                 "vmc_master_script_cambio_ip.sh", "vmc_master_script_cambio_nome.sh"):
        riscritto = trasforma.rinomina(_testo(nome), "prova")
        assert riscritto.count("L'INTEGRAZIONE VMC MASTER") == 2, nome
        assert "INTEGRAZIONE VMC PROVA" not in riscritto, nome
        assert ("vmc_prova" in riscritto) == ("vmc_master" in _testo(nome)), nome


def test_script_cambio_nome() -> None:
    script = _testo("vmc_master_script_cambio_nome.sh")
    assert "RELEASE [VER. 9.0.0b32]" in script[:1000]
    assert "NE AMMETTE FINO A 12, LA SCHEDA 10" in script
    assert "pattern: '^[A-Za-z0-9_-]{0,10}$'" in _testo("vmc_master.yaml")


def _scheda() -> str:
    return _testo("vmc_master_scheda_manuale_interfaccia.txt").replace("\r\n", "\n")


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


def test_black_out_velocita_salvata_e_fascia() -> None:
    """A4-4, A4-7: la scheda ridotta e le note dicono anche la velocita' dell'allerta in corso e la fascia finita."""
    scheda = _scheda()
    assert "torna alla velocità salvata (o a quella memorizzata dall'allerta in corso). Non serve fare nulla." in scheda
    assert "riparte con la velocità della fascia (se nel frattempo la fascia è finita, si arresta). Non serve" in scheda
    piatto = _piatto(scheda)
    assert "che la VMC riprende al ritorno della corrente (o la velocità memorizzata dall'allerta in corso)." in piatto
    assert ("compare invece subito la scheda completa, con il countdown «Ripristino dopo Black-Out» (32 secondi): dopo "
            "altri 5 secondi la VMC riparte con la velocità della fascia") in piatto
    assert 'name: "Ripristino dopo Black-Out"' in scheda


def test_calendario_cinque_secondi_all_ingresso() -> None:
    """A4-8, A5-11: la voce 12 (Calendario) dice i 5 secondi dello script della Fascia, come il Foglio."""
    piatto = _piatto(_scheda())
    assert ("L'ingresso e l'uscita dalla Fascia avvengono dopo 3 secondi; all'ingresso il comando alla VMC parte dopo "
            "ulteriori 5 secondi (attesa dello script della Fascia); all'uscita la VMC si arresta.") in piatto
    pacchetto = _testo("vmc_master.yaml")
    assert pacchetto.count("seconds: 5") >= 2


def test_sezione_17_black_out_come_la_descrizione() -> None:
    """A5-9: la voce Black-Out della sezione 17 e' uguale a quella della descrizione dell'automazione."""
    descrizione = _piatto(_testo("vmc_master_automazione.txt").split("\n  - Black-Out: ", 1)[1].split(";\n\n", 1)[0])
    assert "Spia Black-Out del Calendario" in descrizione
    assert "- Black-Out: " + descrizione + ";<br>" in _piatto(_scheda())


def test_scheda_delta_e_congelamento() -> None:
    """A1-8: nessun «NON APPENA:» senza seguito; nella scheda Δ la VMC (a Velocita' 1) «SARÀ» a Velocita' 0."""
    righe = _scheda().split("\n")
    for i, riga in enumerate(righe):
        if "{% if cal_uscita %}AL TERMINE DELL'ALLERTA" in riga:
            con_seguito = "NON APPENA" in righe[i + 1][:60]
            assert ("NON APPENA:{% elif cal_ingresso" in riga) == con_seguito, i + 1
    assert sum("LA VMC SARÀ A <strong>VELOCITÀ 0</strong>" in r for r in righe) == 6
    assert sum("LA VMC RESTERÀ A <strong>VELOCITÀ 0</strong>" in r for r in righe) == 12


def test_grassetti_chiusi_nelle_schede_inquinanti() -> None:
    """A2-7: «[VMC ON/OFF, in Funzione del Lim. Δ P. di Rugiada]» chiude il grassetto nelle 3 schede inquinanti."""
    scheda = _scheda()
    assert "Funzione del Lim. Δ P. di Rugiada]<strong>" not in scheda
    assert scheda.count("Funzione del Lim. Δ P. di Rugiada]</strong>") >= 3


def test_free_tempi_di_ripresa() -> None:
    """A3-12: la voce 14 dice i tempi di ripresa in Free (24 secondi, 20 con Inquinanti)."""
    assert "riparte in Free Cool./Heat. quando la condizione torna favorevole (dopo 24 secondi; 20 con Inquinanti)." in (
        _piatto(_scheda()))
