"""Prove della 9.0.0b37, testi: l'Offset CO₂/VOC si somma sempre al valore letto, anche con la sonda della VMC assente.

Regola del proprietario (22-11-2026): la sonda della VMC senza Offset si usa solo quando va in down un'entità scelta
diversa dalla VMC; altrimenti l'Offset si somma sempre al valore letto (VMC senza sonda CO₂/VOC, sonda della VMC scelta
come entità CO₂ e Offset +900 → CO₂ 900 ppm e allerta Inquinanti). La b36 (commit 0a6b741) aveva scritto il contrario
(«un valore letto ≤ 0 resta «-» anche con l'Offset»): voci 10 e 11 e Nota Grafici dei Sensori della scheda. Qui si
controlla che i testi nuovi ci siano, che la frase vecchia non sia rimasta in nessun file e che i testi sulla sonda
della VMC senza Offset parlino solo dell'entità scelta non disponibile."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

RADICE = Path(__file__).resolve().parents[1]
INTEGRAZIONE = RADICE / "custom_components" / "vmc_master"
PKG = INTEGRAZIONE / "package"


def _testo(percorso: Path) -> str:
    return percorso.read_text(encoding="utf-8").replace("\r\n", "\n")


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


def _scheda() -> str:
    return _piatto(_testo(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))


def _voce(numero: int) -> str:
    scheda = _scheda()
    inizio = scheda.index(f"<summary><b>{numero} ")
    return scheda[inizio: scheda.index("<summary><b>", inizio + 1)]


def _nota_grafici() -> str:
    scheda = _scheda()
    inizio = scheda.index("<strong>Nota Grafici dei Sensori</strong>")
    return scheda[inizio: scheda.index("<strong>Nota Conferma degli Script</strong>", inizio)]


def test_voce_10_offset_co2() -> None:
    assert ("<b>Valori impostabili.</b> [Offset CO₂ Int.] da −1500 a +1500 ppm (passo 1 ppm), si somma sempre al "
            "valore letto dall'entità scelta, anche quando è la sonda della VMC: con la sonda assente («-») e un "
            "Offset positivo si vede il valore dell'Offset. Le fasce di concentrazione sono fisse.") in _voce(10)


def test_voce_11_offset_voc() -> None:
    assert ("<b>Valori impostabili.</b> [Offset VOC Int.] da −1000 a +1000 ppb (passo 1 ppb), si somma sempre al "
            "valore letto dalla sonda della VMC: con la sonda assente («-») e un Offset positivo si vede il valore "
            "dell'Offset. Le fasce di concentrazione sono fisse.") in _voce(11)


def test_tabelle_co2_voc_sul_valore_con_offset() -> None:
    """Le tabelle delle fasce parlano del valore mostrato (dopo l'Offset): ≤ 0 → «-», come nel Package."""
    for numero, sonda in ((10, "CO₂"), (11, "VOC")):
        voce = _voce(numero)
        assert (f'<td style="padding: 4px 8px; border: 1px solid #c3c2b7;">{sonda} ≤ 0</td><td style="padding: 4px '
                '8px; border: 1px solid #c3c2b7;">Assente «-»</td>') in voce, sonda


def test_nota_grafici_vmc_senza_sonda() -> None:
    assert ("Sulle VMC senza sonda CO₂/VOC la risposta Sensori Ambientali ha la CO₂ e i VOC a 00000. CO₂ e VOC della "
            "scheda «Sensori VMC Interni» (senza Offset) restano sempre «-» e i loro due grafici sono vuoti: in Home "
            "Assistant questi sensori «_grafico» risultano non disponibili. Non è un guasto. L'Offset si somma sempre "
            "(voci 10 e 11): con un Offset positivo CO₂ Int. (se l'entità scelta è la sonda della VMC) e VOC Int. "
            "della scheda «Sensori - Selezionati» mostrano il valore dell'Offset e i loro grafici lo disegnano; con "
            "l'Offset a 0 o negativo restano «-».") in _nota_grafici()


def test_nota_grafici_black_out() -> None:
    assert ("Se in quella lettura la VMC indica un valore ≤ 0 (per esempio la CO₂), il sensore senza Offset mostra «-» "
            "e il suo grafico resta vuoto fino alla lettura successiva: in quel tempo il suo sensore «_grafico» "
            "risulta non disponibile. Con un Offset positivo il sensore con Offset che legge la sonda della VMC mostra "
            "invece il valore dell'Offset. Il valore letto si vede nella voce 1 (Info Lettura Dati nella VMC, Sensori "
            "Ambientali: dopo VMGI la CO₂ è il quarto numero, i VOC l'undicesimo).") in _nota_grafici()


def _file_di_testo() -> list[Path]:
    return [*sorted(PKG.iterdir()), INTEGRAZIONE / "strings.json", *sorted((INTEGRAZIONE / "translations").iterdir()),
            INTEGRAZIONE / "frontend" / "vmc-master-card.js",
            RADICE / "README.md", RADICE / ".github" / "README.md"]


VECCHIE = re.compile(
    r"anche con l'Offset|anche con un Offset|resta «-» anche|restano sempre «-», anche|un valore letto ≤ 0"
    r"|even with (?:the|an) offset|stays? «-» even|remains? «-» even|quattro grafici",
    re.IGNORECASE,
)


@pytest.mark.parametrize("percorso", _file_di_testo(), ids=lambda p: str(p.relative_to(RADICE)))
def test_frase_della_b36_non_rimasta(percorso: Path) -> None:
    """Nessun testo (IT o EN, commenti compresi) dice più che una lettura ≤ 0 resta «-» anche con l'Offset."""
    assert not VECCHIE.findall(_piatto(_testo(percorso))), percorso.name


def test_sonda_della_vmc_senza_offset_solo_con_entita_non_disponibile() -> None:
    """I testi sulla sonda della VMC senza Offset restano legati all'entità scelta non disponibile (già giusti)."""
    scheda = _scheda()
    assert ("Se un'entità scelta in Opzioni non è disponibile, al suo posto si usa la sonda della VMC, senza Offset "
            "(l'Offset è tarato sull'entità scelta)") in scheda
    assert "ENTITÀ SCELTA NON DISPONIBILE: IN USO LA SONDA DELLA VMC (SENZA OFFSET)" in scheda
    assert "Al ripristino dell'entità scelta si torna automaticamente al suo valore (con Offset)." in scheda
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt"):
        assert _testo(PKG / nome).count("In sostituzione si usa la sonda della VMC, senza Offset: ") == 4, nome
    assert ("Se un'entità scelta (Temperatura Esterna, Temperatura Interna, Umidità Interna o CO₂ Interna) non è "
            "disponibile, usa al suo posto la sonda della VMC senza Offset") in _piatto(
                _testo(PKG / "vmc_master_automazione.txt"))
