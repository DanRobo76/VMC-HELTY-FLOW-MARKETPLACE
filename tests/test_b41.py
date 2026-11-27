"""Prove della 9.0.0b41 (risposte del proprietario del 25-11-2026 alle decisioni della b40).

- Decisione 4: con un'allerta Lim. Δ PdR iniziata a Velocità 0, all'arrivo degli Inquinanti la VMC parte a Velocità 1
  dopo 8 secondi, come la regola degli Inquinanti del Foglio Logiche (prima 4 secondi): attesa «Attesa Avvio Allerta
  Inquinanti (con Spia PdR)» = 8 s nel trigger, nello script dei valori originali e nel commento della costante; i 24
  tempi di attesa hanno lo stesso valore originale in tutte le copie (classe intera).
- Il valore originale nuovo vale anche per chi ha già installato l'integrazione: «Inizializza Tempi di Attesa» riporta i
  tempi ai valori originali a ogni avvio di Home Assistant (prima solo al primo avvio).
Le decisioni 2 e 3 (come la b39) e la decisione 1 anche con l'Umidità sono provate in tests/test_b40_free.py."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
ATTESA_PDR0 = "input_number.vmc_master_attesa_inquinanti_avvio_spia_pdr"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _valori_originali() -> dict[str, int]:
    pacchetto = _testo("vmc_master.yaml")
    script = pacchetto[pacchetto.index("  vmc_master_ripristina_tempi_attesa:"):]
    script = script[: script.index("Fine Creazione Script Ripristina Tempi")]
    trovati = re.findall(r"entity_id: (input_number\.vmc_master_attesa_[a-z_]+)\n        data:\n          value: (\d+)", script)
    return {e: int(v) for e, v in trovati}


# ------------------------------------------------------------------------------------------------ decisione 4
def test_inquinanti_con_spia_pdr_velocita_0_dopo_8_secondi() -> None:
    """Trigger «Inquinanti con Spia PdR Velocità 0»: attesa letta dalla costante con 8 come valore di riserva; lo script
    dei valori originali e il commento della costante dicono 8 s (la b40 diceva 4)."""
    automazione, pacchetto = _testo("vmc_master_automazione.txt"), _testo("vmc_master.yaml")
    trigger = automazione[automazione.index("    id: inquinanti_co2_voc_on\n"):]
    trigger = trigger[: trigger.index("    id: Inquinanti con Spia PdR Velocità 0 -> Spia PdR Velocità 0 OFF\n") + 200]
    assert f"seconds: \"{{{{ states('{ATTESA_PDR0}') | int(8) }}}}\"" in trigger
    assert f"states('{ATTESA_PDR0}') | int(4)" not in automazione
    assert _valori_originali()[ATTESA_PDR0] == 8
    (riga,) = [r for r in pacchetto.split("\n") if r.startswith("  vmc_master_attesa_inquinanti_avvio_spia_pdr:")]
    assert "(VALORE ORIGINALE 8 s)" in riga
    # stesso tempo dell'avvio degli Inquinanti (trigger «inquinanti_co2_voc_on», Foglio: TIMING 8 SECONDI)
    assert _valori_originali()["input_number.vmc_master_attesa_inquinanti_avvio"] == 8


def test_tempi_di_attesa_stesso_valore_originale_in_tutte_le_copie() -> None:
    """Classe intera: per ognuno dei 24 tempi di attesa il valore dello script, il «VALORE ORIGINALE» del commento e il
    valore di riserva «int(N)» nell'automazione e nel Countdown sono uguali."""
    valori = _valori_originali()
    assert len(valori) == 24
    pacchetto, automazione = _testo("vmc_master.yaml"), _testo("vmc_master_automazione.txt")
    commenti = {"input_number." + k: int(v)
                for k, v in re.findall(r"^  (vmc_master_attesa_[a-z_]+):.*VALORE ORIGINALE (\d+) s", pacchetto, re.M)}
    assert commenti == valori
    riserve: dict[str, set[int]] = defaultdict(set)
    for testo in (automazione, pacchetto):
        for entita, n in re.findall(r"states\('(input_number\.vmc_master_attesa_[a-z_]+)'\) \| int\((\d+)\)", testo):
            riserve[entita].add(int(n))
    assert len(riserve) == 24
    assert {e: v for e, v in riserve.items() if v != {valori[e]}} == {}


def test_tempi_originali_riportati_a_ogni_avvio() -> None:
    """«Inizializza Tempi di Attesa» chiama lo script dei valori originali a ogni avvio di Home Assistant (così l'attesa
    di 8 s arriva anche a chi aveva già i 4 s), e come prima quando le costanti sono appena create (spia spenta)."""
    pacchetto = _testo("vmc_master.yaml")
    auto = pacchetto[pacchetto.index('  - id: "vmc_master_inizializza_tempi_attesa"'):]
    auto = auto[: auto.index("################### Fine Creazione Automazione Inizializzazione")]
    assert "      - trigger: homeassistant\n        event: start\n" in auto
    assert ("value_template: \"{{ trigger.platform == 'homeassistant' or "
            "is_state('input_boolean.vmc_master_attese_inizializzate', 'off') }}\"") in auto
    assert "condition: state" not in auto
    assert "a ogni avvio di Home Assistant" in auto
    assert "      - action: script.vmc_master_ripristina_tempi_attesa\n" in auto


# ------------------------------------------------------------------------------------------------ testi
FRASI_B41 = [  # frasi della b41: descrizione dell'automazione e voce 17 (riquadro e tabella), una volta ciascuna
    # decisione 1 anche con l'Umidità in corso (Δ Temp., fine Inquinanti, Velocità 0 con gli Inquinanti presenti)
    ("con la Free Cool./Heat. sospesa la ripresa automatica in Free si annulla, come con gli Inquinanti, anche se la "
     "Velocità 0 è scelta negli ultimi Secondi o durante l'attesa della fine, anche con un'allerta Umidità in corso)"),
    ("con la Free Cool./Heat. sospesa la Velocità 0 scelta, durante l'allerta o nell'attesa, annulla la ripresa in Free e "
     "resta, anche con un'allerta Umidità in corso;"),
    ("con la Free Cool./Heat. sospesa la ripresa in Free si annulla, anche se la Velocità 0 è scelta nell'attesa di 8 "
     "Secondi dopo il rientro, anche con un'allerta Umidità in corso)"),
    # Free sospesa (VMC ferma in attesa): Umidità sola = decisione 2, con Δ Temp. o Inquinanti = decisione 1
    ("(con un'allerta Umidità in corso la VMC, a Velocità 1 [Nota 3], si ferma e resta a Velocità 0 fino alla ripresa; "
     "con un'allerta Δ Temp. o Inquinanti in corso, anche insieme all'Umidità, la Velocità 0 scelta resta e annulla la "
     "ripresa)"),
    # decisione 4
    ("se un'allerta Lim. Δ PdR è iniziata con la VMC a Velocità 0, all'arrivo degli Inquinanti la sua memoria di "
     "Velocità 0 si azzera e la VMC parte a Velocità 1 dopo 8 Secondi;"),
]
FRASI_B40_TOLTE = [  # frasi della b40 (decisioni 2-3 e Umidità esclusa dalla decisione 1) che non devono più esserci
    "la ripresa resta in attesa",
    "tornare a Velocità 1 [Nota 3]",
    "torna invece a Velocità 1 [Nota 3]",
    "dopo 4 Secondi torna a Velocità 1 [Nota 3]",
    "la VMC torna a Velocità 1 [Nota 3])",
    "la VMC parte a Velocità 1 dopo 4 Secondi",
    "la Velocità 0 scelta non resta",
]


def test_frasi_b41_nella_descrizione_e_nella_voce_17() -> None:
    from tests.test_b36_testi import _descrizione, _voce_17_come_descrizione
    for testo in (_descrizione(), _voce_17_come_descrizione()):
        for frase in FRASI_B41:
            assert testo.count(frase) == 1, frase[:80]


def test_frasi_b40_delle_decisioni_2_3_tolte() -> None:
    from tests.test_b36_testi import _descrizione, _norm, _scheda
    for testo in (_descrizione(), _norm(_scheda())):
        for frase in FRASI_B40_TOLTE:
            assert frase not in testo, frase


def test_testi_dei_tempi_riportati_a_ogni_avvio() -> None:
    """Descrizione dell'automazione, scheda (Ripristina Tempi di Attesa Originali) e README IT/EN nelle due copie."""
    from tests.test_b36_testi import _descrizione, _norm, _scheda
    assert "che Home Assistant a ogni avvio e il Profilo Inizializzazione riportano ai valori originali." in _descrizione()
    assert "È compreso nel Profilo Inizializzazione e parte da solo a ogni avvio di Home Assistant." in _norm(_scheda())
    radice = PKG.parent.parent.parent
    for readme in (radice / "README.md", radice / ".github" / "README.md"):
        testo = readme.read_text(encoding="utf-8")
        # versione nativa: le attese sono interne e non si possono modificare
        assert "I tempi di attesa sono fissi e non si possono modificare: non compaiono nella scheda.</sub>" in testo
        assert "The wait times are fixed and cannot be changed: they do not appear on the card.</sub>" in testo
        assert "tornano ai valori originali a ogni avvio" not in testo
        assert "il Profilo Inizializzazione li riporta ai valori originali" not in testo
