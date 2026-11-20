"""Prove della 9.0.0b32: durante il riavvio di Home Assistant le schede delle allerte di un gruppo non ancora
riattivato dicono «ATTENDERE LA RIATTIVAZIONE DEL N° GRUPPO», come il pannello «Riattivazione delle Allerte»."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
SPIA_INQUINANTI = "input_boolean.vmc_master_spia_co2_o_voc"
G2 = "ATTENDERE LA RIATTIVAZIONE DEL 2° GRUPPO (IN CIMA ALLA SCHEDA).."
G3 = "ATTENDERE LA RIATTIVAZIONE DEL 3° GRUPPO (IN CIMA ALLA SCHEDA).."


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _schede() -> dict[str, str]:
    """Contenuto markdown delle 4 schede delle allerte con azioni sospese dal riallineamento."""
    scheda = hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))
    contenuti = [c["card"].get("content", "") for c in scheda["cards"] if c.get("card", {}).get("type") == "markdown"]
    con_attesa = [c for c in contenuti if "{% set attendere =" in c]
    assert len(con_attesa) == 4
    trova = {
        "inquinanti": "ALLERTA LIVELLO DI CONCENTRAZIONE DI ANIDRIDE CARB",
        "pdr": "ALLERTA SUPERAMENTO DEL LIM. Δ PUNTO DI RUGIADA",
        "free": "RIPRISTINO SULLA VELOCITA' FREE HEATING",
        "umidita": "PREPARAZIONE AL MANTENIMENTO AUTOMATICO DELLA VMC",
    }
    schede = {}
    for chiave, segno in trova.items():
        uniche = [c for c in con_attesa if segno in c]
        assert len(uniche) == 1, chiave
        schede[chiave] = uniche[0]
    assert len({id(c) for c in schede.values()}) == 4
    return schede


def _intestazione(contenuto: str) -> str:
    """Le righe «{% set fase_riavvio / attendere / attendere_avvio %}» in cima alla scheda."""
    fine = contenuto.index("{% set", contenuto.index("{% set attendere =") + 1)
    if "attendere_avvio" in contenuto[:fine + 40]:
        fine = contenuto.index("{% set", contenuto.index("{% set attendere_avvio") + 1)
    return contenuto[:fine]


def test_nessun_attendere_fisso_nelle_quattro_schede() -> None:
    for chiave, contenuto in _schede().items():
        corpo = contenuto[len(_intestazione(contenuto)):]
        assert not re.search(r"ATTENDERE ?\.\.", corpo), chiave
        assert "{{ attendere }}" in corpo, chiave


def test_conteggio_dei_messaggi_con_attesa() -> None:
    """Ogni «ATTENDERE..» della b31 e' diventato la variabile (conteggio esatto per scheda); nella scheda PdR il Msg 1
    «ARRESTO DELLA VMC» ha ora l'attesa come il Msg 2 (A2-7); nella scheda Free i Msg 15 e 15.1 annunciano il ripristino in
    Free come i Msg 11 (A3-5). b33: nella scheda PdR anche il Msg 24 (PdR non calcolabile) annuncia la ripresa (A2-2)."""
    attesi = {"inquinanti": (10, 3), "pdr": (14, 0), "free": (12, 0), "umidita": (5, 0)}
    for chiave, contenuto in _schede().items():
        assert (contenuto.count("{{ attendere }}"), contenuto.count("{{ attendere_avvio }}")) == attesi[chiave], chiave


def test_avvio_inquinanti_solo_nei_tre_messaggi_di_avvio() -> None:
    contenuto = _schede()["inquinanti"]
    righe = [r for r in contenuto.splitlines() if "{{ attendere_avvio }}" in r]
    assert len(righe) == 3
    assert all(r.strip().endswith("INQUINANTI, {{ attendere_avvio }}</strong>") for r in righe)


@pytest.mark.parametrize(
    ("chiave", "fase", "spia", "atteso", "atteso_avvio"),
    [
        # 2° gruppo (Inquinanti): in pausa solo nella fase 1 e 2
        ("inquinanti", "0.0", "off", "ATTENDERE..", "ATTENDERE.."),
        ("inquinanti", "1.0", "off", G2, G2),
        ("inquinanti", "2.0", "off", G2, G2),
        ("inquinanti", "3.0", "off", "ATTENDERE..", "ATTENDERE.."),
        ("inquinanti", "4.0", "off", "ATTENDERE..", "ATTENDERE.."),
        # allerta Inquinanti gia' in corso al riavvio: l'avvio non aspetta il gruppo
        ("inquinanti", "1.0", "on", G2, "ATTENDERE.."),
        # 3° gruppo (Punto di Rugiada, Free Heating/Cooling, Umidità): in pausa nelle fasi 1, 2 e 3
        ("pdr", "0.0", "off", "ATTENDERE..", None),
        ("pdr", "1.0", "off", G3, None),
        ("pdr", "3.0", "off", G3, None),
        ("pdr", "4.0", "off", "ATTENDERE..", None),
        ("free", "2.0", "off", G3, None),
        ("free", "4.0", "off", "ATTENDERE..", None),
        ("umidita", "3.0", "off", G3, None),
        ("umidita", "0.0", "off", "ATTENDERE..", None),
        # fase non ancora disponibile (avvio): nessuna pausa mostrata
        ("umidita", "unknown", "off", "ATTENDERE..", None),
    ],
)
async def test_testo_secondo_la_fase(
    hass: HomeAssistant, chiave: str, fase: str, spia: str, atteso: str, atteso_avvio: str | None
) -> None:
    hass.states.async_set(FASE, fase)
    hass.states.async_set(SPIA_INQUINANTI, spia)
    sorgente = _intestazione(_schede()[chiave]) + "{{ attendere }}|{{ attendere_avvio | default('-') }}"
    reso = Template(sorgente, hass).async_render(parse_result=False).strip()
    testo, avvio = reso.split("|")
    assert testo == atteso
    assert avvio == (atteso_avvio or "-")


def test_gruppi_uguali_a_quelli_dell_automazione() -> None:
    """Le soglie di fase delle schede sono quelle dei trigger dell'automazione (Inquinanti >= 3, gli altri >= 4)."""
    automazione = _testo("vmc_master_automazione.txt")

    def soglia(id_trigger: str) -> int:
        i = automazione.index(f"id: {id_trigger}")
        blocco = automazione[automazione.rindex("value_template", 0, i) : i]
        return int(re.search(r"fase_riallineamento_al_riavvio'\) \| float\(0\) >= (\d)", blocco).group(1))

    assert soglia("inquinanti_co2_voc_on") == soglia("inquinanti_co2_voc_off") == 3
    assert soglia("spia_umidita_on") == soglia("spia_umidita_off") == 4
    assert soglia("PdR Vel. 1-> Imposta Velocità 0") == 4
    assert soglia("'Rip. Free Heating No TeVsTi '") == 4
    # l'avvio degli Inquinanti non aspetta il gruppo se l'allerta era gia' in corso (spia accesa)
    i = automazione.index("id: inquinanti_co2_voc_on")
    blocco = automazione[automazione.rindex("value_template", 0, i) : i]
    assert "float(0) >= 3 or states('input_boolean.vmc_master_spia_co2_o_voc') == 'on'" in blocco


def test_nota_avvio_di_home_assistant() -> None:
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    i = scheda.index("<strong>Nota Avvio di Home Assistant</strong>")
    nota = re.sub(r"\s+", " ", scheda[i : scheda.index("<br>", i)])
    assert "«ATTENDERE LA RIATTIVAZIONE DEL 2° GRUPPO» o «DEL 3° GRUPPO»" in nota
    # solo i messaggi che chiedono di attendere (prova su HA reale: Msg. 3/5 senza riga di attesa)
    assert "Intanto, nei messaggi che chiedono di attendere, le schede delle allerte" in nota


def _commento(entita: str) -> str:
    dominio, oggetto = entita.split(".", 1)
    pacchetto = _testo("vmc_master.yaml")
    sezione = pacchetto.index(f"\n{dominio}:")
    return re.compile(rf"\n  {oggetto}: +# (.+)").search(pacchetto, sezione).group(1)


@pytest.mark.parametrize("entita", [FASE, SPIA_INQUINANTI])
def test_richiami_interfaccia(entita: str) -> None:
    n = len(re.findall(re.escape(entita) + r"(?![A-Za-z0-9_])", _testo("vmc_master_scheda_manuale_interfaccia.txt")))
    assert f"[INTERFACCIA, {n} RICHIAMI]" in _commento(entita)


def test_versioni() -> None:
    assert "RELEASE [VER. 9.0.0b32]" in _testo("vmc_master_scheda_manuale_interfaccia.txt")[:2000]
    manifest = (PKG.parent / "manifest.json").read_text(encoding="utf-8")
    assert '"version": "9.0.0b32"' in manifest
