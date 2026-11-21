"""Controllo automatico b36: i testi che la descrizione dell'automazione e la scheda (Informazioni, voce 17 e tabella del
cambio di velocità durante un'allerta) hanno in comune devono restare uguali.

Regola del proprietario (21-11-2026): quando cambia un comportamento si aggiornano tutte le descrizioni, non solo il
Foglio; come per i RICHIAMI, una copia dimenticata deve far fallire una prova invece di arrivare all'utente.
"""

from __future__ import annotations

import html
import re

import pytest

from tests.test_b35_allerte import PKG


def _paragrafi_descrizione() -> list[str]:
    righe = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8").split("\n")
    (inizio,) = [k for k, r in enumerate(righe) if r.startswith("description: >-")]
    fine = inizio + 1
    while fine < len(righe) and (righe[fine].startswith("  ") or righe[fine] == ""):
        fine += 1
    paragrafi: list[str] = []
    corrente: list[str] = []
    for riga in righe[inizio + 1 : fine]:
        if riga.strip():
            corrente.append(riga.strip())
        elif corrente:
            paragrafi.append(" ".join(corrente))
            corrente = []
    if corrente:
        paragrafi.append(" ".join(corrente))
    return paragrafi


def _norma(testo: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", testo))).strip()


def _scheda() -> str:
    return (PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8").replace("\r\n", "\n")


TABELLA = "CAMBIO DI VELOCITÀ DURANTE UN'ALLERTA (comportamento misurato):"
SOLO_DESCRIZIONE = ("I Secondi indicati sono fissi e non vanno modificati",)


def _sezioni() -> tuple[list[str], list[str]]:
    """Paragrafi dalla «PRIORITA' DI ATTIVAZIONE» in poi: quelli copiati alla lettera nella voce 17 e le righe della
    tabella del cambio di velocità durante un'allerta (nella scheda è una tabella HTML)."""
    paragrafi = _paragrafi_descrizione()
    (inizio,) = [k for k, p in enumerate(paragrafi) if p.startswith("PRIORITA' DI ATTIVAZIONE DEGLI ALLARMI")]
    (tabella,) = [k for k, p in enumerate(paragrafi) if p == TABELLA]
    fine_tabella = next(k for k in range(tabella + 1, len(paragrafi)) if not paragrafi[k].startswith("- "))
    alla_lettera = [p for k, p in enumerate(paragrafi[inizio:], inizio)
                    if not (tabella <= k < fine_tabella) and not p.startswith(SOLO_DESCRIZIONE)]
    return alla_lettera, paragrafi[tabella + 1 : fine_tabella]


def test_sezioni_trovate() -> None:
    alla_lettera, righe = _sezioni()
    assert len(alla_lettera) >= 20 and len(righe) >= 7


@pytest.mark.parametrize("indice", range(25))
def test_paragrafo_uguale_nella_scheda(indice: int) -> None:
    alla_lettera, _ = _sezioni()
    if indice >= len(alla_lettera):
        pytest.skip("meno paragrafi")
    paragrafo = _norma(alla_lettera[indice])
    assert paragrafo in _norma(_scheda()), paragrafo[:160]


def _righe_tabella_scheda() -> dict[str, list[str]]:
    righe: dict[str, list[str]] = {}
    for riga in _scheda().split("\n"):
        if "<tr>" in riga and "<td" in riga:
            celle = [_norma(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", riga)]
            if len(celle) >= 3:
                righe[celle[0]] = celle[1:]
    return righe


def _minuscola(testo: str) -> str:
    return testo[:1].lower() + testo[1:]


def test_tabella_del_cambio_di_velocita_uguale() -> None:
    """Ogni riga della descrizione «- Allerta: si sceglie un'altra Velocità → …; si sceglie Velocità 0 → …» ha nella
    scheda la riga con lo stesso nome e le stesse celle (prima lettera maiuscola nella scheda)."""
    _, righe = _sezioni()
    tabella = _righe_tabella_scheda()
    for riga in righe:
        nome, testo = _norma(riga)[2:].split(": ", 1)
        assert nome in tabella, nome
        for cella in tabella[nome]:
            assert _minuscola(cella) in testo, (nome, cella[:120])


def test_righe_del_readme_breve_uguali_nel_readme_completo() -> None:
    """Le righe «- <sub>…» della guida breve (README.md, mostrata dal Marketplace) sono copiate alla lettera nella guida
    completa (.github/README.md, mostrata da GitHub): una riga aggiornata in una sola guida fa fallire la prova."""
    radice = PKG.parent.parent.parent
    breve = [r.strip() for r in (radice / "README.md").read_text(encoding="utf-8").split("\n")
             if r.strip().startswith("- <sub>")]
    completo = (radice / ".github" / "README.md").read_text(encoding="utf-8")
    assert len(breve) >= 40
    mancanti = [r[:120] for r in breve if r not in completo]
    assert mancanti == []
