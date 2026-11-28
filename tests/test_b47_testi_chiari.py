"""9.0.0b47: testi più chiari (il comportamento non cambia).

- Ogni richiamo alla Nota 3 dello schema «Logiche di Funzionamento» nella scheda nativa
  dice dove è spiegata: nella voce 7 la spiega la prima delle sue Note, fuori dalla voce 7
  il richiamo indica la voce 7.
- Ogni richiamo a una Nota del Pannello Informazioni (es. «Nota Avvio di Home Assistant»)
  porta a una Nota che esiste e, fuori dalla voce 15 che le contiene, dice la voce.
- I tempi delle letture e del Ping nel README (italiano e inglese, guida del Marketplace e
  guida completa) e nella scheda sono quelli del codice.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import custom_components.vmc_master  # noqa: F401  (si prova anche da solo)

RADICE = Path(__file__).resolve().parents[1]
SCHEDA = RADICE / "custom_components/vmc_master/nativa/scheda_nativa.txt"
LETTURE = RADICE / "custom_components/vmc_master/nativa/letture.py"
README = (RADICE / "README.md", RADICE / ".github/README.md")

# le voci del Pannello Informazioni: «<summary><b>7 Umidità ...»
_VOCE = re.compile(r"<summary><(?:b|strong)>(\d+) ")
_NOTA_3 = re.compile(r"\[(?:Nota|NOTA) 3([^\]]*)\]")
_NOTA_DEFINITA = re.compile(r"<strong>(Nota [^<]+)</strong>")
_NOTA_RICHIAMATA = re.compile(r"(?<!<strong>)\bNota (?=[A-ZÀ-Ý])")


def _testo(percorso: Path) -> str:
    return percorso.read_text(encoding="utf-8")


def _voci(testo: str) -> dict[int, tuple[int, int]]:
    """Inizio e fine di ogni voce numerata del Pannello Informazioni."""
    inizi = [(int(m.group(1)), m.start()) for m in _VOCE.finditer(testo)]
    return {
        numero: (inizio, inizi[i + 1][1] if i + 1 < len(inizi) else len(testo))
        for i, (numero, inizio) in enumerate(inizi)
    }


@pytest.fixture(scope="module")
def scheda() -> str:
    return _testo(SCHEDA)


def test_voci_del_pannello(scheda: str) -> None:
    voci = _voci(scheda)
    assert sorted(voci) == list(range(1, 23))
    assert "7 Umidità Interna" in scheda[slice(*voci[7])]
    assert "17 Logiche di Funzionamento" in scheda[slice(*voci[17])]
    assert "Logiche%20di%20Funzionamento.png" in scheda[slice(*voci[17])]


def test_nota_3_spiegata_nella_voce_7(scheda: str) -> None:
    inizio, fine = _voci(scheda)[7]
    voce_7 = " ".join(scheda[inizio:fine].split())
    spiegazione = re.search(r"• <b>\[Nota 3\] (.+?)<br><br>", voce_7)
    assert spiegazione, "la voce 7 non spiega la [Nota 3]"
    testo = spiegazione.group(1)
    for parte in (
        "Velocità 1 dell'Umidità con la Free Cool./Heat. sospesa</b>",
        "Nota 3 dello schema «Logiche di Funzionamento» in fondo alla voce 17",
        "la VMC va a Velocità 1, qualunque sia la [Set Velocità Umidità di Avvio]",
        "(con Velocità 0 resta ferma)",
        "a fine Umidità torna a Velocità 0",
        "con gli Inquinanti va a Velocità 1 fino al loro rientro",
        "dopo 24 secondi (20 secondi con gli Inquinanti)",
    ):
        assert parte in testo, parte
    # è la prima delle Note della voce 7
    assert voce_7.index("<b>Note.</b> <br><br> • <b>[Nota 3]") > 0


def test_ogni_richiamo_alla_nota_3_dice_dove_leggerla(scheda: str) -> None:
    inizio, fine = _voci(scheda)[7]
    dentro, fuori = [], []
    for trovato in _NOTA_3.finditer(scheda):
        (dentro if inizio <= trovato.start() < fine else fuori).append(trovato)
    # voce 7: la spiegazione e 4 richiami, che la trovano nella stessa voce
    assert [m.group(1) for m in dentro] == [""] * 5
    # fuori: 4 richiami nella voce 17 e 2 nelle scritte delle allerte Free
    assert [m.group(1) for m in fuori] == [
        ", PANNELLO INFORMAZIONI, VOCE 7",
        ", PANNELLO INFORMAZIONI, VOCE 7",
        ", voce 7",
        ", voce 7",
        ", voce 7",
        ", voce 7",
    ]
    inizio_17, fine_17 = _voci(scheda)[17]
    assert all(inizio_17 <= m.start() < fine_17 for m in fuori[2:])


def test_ogni_nota_richiamata_esiste(scheda: str) -> None:
    testo = " ".join(scheda.split())
    definite = set(_NOTA_DEFINITA.findall(testo))
    assert len(definite) == 12
    inizio_15, fine_15 = _voci(testo)[15]
    assert all(
        inizio_15 <= m.start() < fine_15 for m in _NOTA_DEFINITA.finditer(testo)
    )
    richiami = 0
    for trovato in _NOTA_RICHIAMATA.finditer(testo):
        a = trovato.start()
        if testo[a - len("<strong>") : a] == "<strong>":
            continue
        nome = next((n for n in definite if testo.startswith(n, a)), None)
        assert nome, f"richiamo a una Nota che non c'è: {testo[a : a + 60]!r}"
        richiami += 1
        if not inizio_15 <= a < fine_15:
            assert "voce 15, " in testo[a - 40 : a], testo[a - 80 : a + 40]
    assert richiami == 5


@pytest.mark.parametrize("percorso", README, ids=lambda p: p.parent.name or "radice")
def test_readme_richiami_alle_note(percorso: Path) -> None:
    testo = _testo(percorso)
    assert "[Nota" not in testo and "[NOTA" not in testo
    assert testo.count("[Pannello Informazioni → voce 15, Nota Entità Scelte non Disponibili]") == 1
    assert testo.count("[Pannello Informazioni → item 15, Nota Entità Scelte non Disponibili]") == 1


def _intervalli() -> dict[str, int]:
    codice = _testo(LETTURE)
    tcp = dict(re.findall(r'Lettura\("sensor\.(\w+)", "VM\w+\?", (\d+)', codice))
    ping = re.search(r'f"VMC ping \{host\}", (\d+)\)', codice)
    assert ping
    return {
        "Ping": int(ping.group(1)),
        "Sensori Ventilazione": int(tcp["status_ventola"]),
        "Sensori Ambientali": int(tcp["sensori"]),
        "Sensori Lan": int(tcp["lan"]),
        "Sensore Nome": int(tcp["nome"]),
    }


def _ping() -> tuple[int, int]:
    codice = _testo(LETTURE)
    tentativi = re.search(r"^PING_TENTATIVI = (\d+)", codice, re.MULTILINE)
    durata = re.search(r"^PING_DURATA = (\d+)", codice, re.MULTILINE)
    assert tentativi and durata
    return int(tentativi.group(1)), int(durata.group(1))


def test_intervalli_del_codice() -> None:
    assert _intervalli() == {
        "Ping": 10,
        "Sensori Ventilazione": 5,
        "Sensori Ambientali": 1227,
        "Sensori Lan": 57641,
        "Sensore Nome": 43227,
    }
    assert _ping() == (3, 4)


@pytest.mark.parametrize("percorso", README, ids=lambda p: p.parent.name or "radice")
def test_readme_tempi_delle_letture(percorso: Path) -> None:
    testo = _testo(percorso)
    intervalli = _intervalli()
    tentativi, durata = _ping()
    it = ", ".join(f"{n} (ogni {s} s)" for n, s in list(intervalli.items())[:-1])
    it += f" e Sensore Nome (ogni {intervalli['Sensore Nome']} s)"
    en = ", ".join(f"{n} (every {s} s)" for n, s in list(intervalli.items())[:-1])
    en += f" and Sensore Nome (every {intervalli['Sensore Nome']} s)"
    assert testo.count(f"l'ultima lettura: {it} [Sensori - Selezionati → Timer Lettura Dati VMC].") == 1
    assert testo.count(f"the last read happened: {en} [Sensori - Selezionati → Timer Lettura Dati VMC].") == 1
    assert testo.count(
        f"Ogni controllo Ping invia {tentativi} ping, uno al secondo, e dura al massimo"
        f" {durata} secondi: basta una risposta perché la VMC risulti ON-Line."
    ) == 1
    assert testo.count(
        f"Each Ping check sends {tentativi} pings, one per second, and lasts at most"
        f" {durata} seconds: one reply is enough for the unit to be ON-Line."
    ) == 1


def test_scheda_tempi_delle_letture(scheda: str) -> None:
    testo = " ".join(scheda.split())
    intervalli = _intervalli()
    tentativi, durata = _ping()
    elenco = ", ".join(f"{n} (ogni {s} s)" for n, s in list(intervalli.items())[:-1])
    elenco += f" e Sensore Nome (ogni {intervalli['Sensore Nome']} s)"
    assert testo.count(f"«Timer Lettura Dati VMC»: per {elenco} mostra il tempo") == 1
    assert testo.count(
        f"Home Assistant la controlla ogni {intervalli['Ping']} secondi: ogni controllo invia"
        f" {tentativi} ping, uno al secondo, e dura al massimo {durata} secondi; basta una"
        " risposta perché la VMC risulti ON-Line."
    ) == 1
