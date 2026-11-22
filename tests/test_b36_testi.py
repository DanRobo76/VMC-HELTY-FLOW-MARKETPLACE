"""Prove della b36, fetta «testi»: i testi per l'utente delle scelte del proprietario sull'audit della b34.

- C5-4 (scelta 9): le 8 frasi del Foglio che mancavano (Set Umidità a Velocità 0, Umidità + Inquinanti in 28 s, Free
  sospesa senza cambio, Velocità 1 durante il Δ, 8 s di memorizzazione degli Inquinanti, A29, PdR non calcolabile, N.B.
  del Calendario) sono nella descrizione dell'automazione, nella voce 17 e, dove servono, nelle voci 7/8/10/12/14.
- C3-2, C4-4, C1-3, C1-2, C1-5, C4-3, C4-5 (scelte 1-7): il comportamento nuovo è scritto in tutti i posti (descrizione,
  voce 17, voci delle Informazioni, Riquadro Avvisi, scheda Umidità, script delle Fasce, Countdown).
- Regola permanente: anche le correzioni della b35 (C1-1, C3-1, C3-3, C4-1, C4-2) sono scritte in tutti i posti, README
  compresi.
- La descrizione dell'automazione e la voce 17 restano la stessa cosa (stesso testo, tabella compresa).
"""

from __future__ import annotations

import html
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

RADICE = Path(__file__).parent.parent
PKG = RADICE / "custom_components" / "vmc_master" / "package"
SET_UMIDITA = "input_select.vmc_master_speed_umidita"
FREE_C = "input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_freecooling"
FREE_ECC = ("salvo la sospensione Free Cool./Heat.: l'Umidità parte comunque a Velocità 1 [Nota 3] e il suo "
            "interruttore non si spegne fino alla ripresa o all'annullamento della Free")
SET0 = "con la [Set Velocità Umidità di Avvio] su Velocità 0 la VMC resta ferma"
VIETATE = ("vmc_master", "master", "input_", "sensor.", "999.999", "clona")


@lru_cache
def _testo(nome: str) -> str:
    return (PKG / nome).read_bytes().decode("utf-8")


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


@lru_cache
def _pacchetto() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


@lru_cache
def _descrizione() -> str:
    return _norm(hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))["description"])


def _scheda() -> str:
    return _testo("vmc_master_scheda_manuale_interfaccia.txt")


def _voce(numero: int) -> str:
    """Una voce del pannello Informazioni della scheda, da «<summary><b>N » alla voce successiva."""
    scheda = _scheda()
    inizio = scheda.index(f"<summary><b>{numero} ")
    return _norm(scheda[inizio: scheda.index("<summary><b>", inizio + 1)])


def _voce_17() -> str:
    """La parte della voce 17 che ripete la descrizione (HTML della scheda)."""
    voce = _scheda()
    voce = voce[voce.index("<summary><b>17 Logiche di Funzionamento</b></summary>"):]
    return _norm(voce[voce.index("- Congelamento ≤ -18"): voce.index("18_priorita_allarmi.png")])


def _voce_17_come_descrizione() -> str:
    """La voce 17 riscritta come la descrizione: tabella in righe «- X: si sceglie un'altra Velocità → …», niente HTML."""
    voce = _scheda().replace("\r\n", "\n")
    voce = voce[voce.index("<summary><b>17 Logiche di Funzionamento</b></summary>"):]
    voce = voce[voce.index("- Congelamento ≤ -18"): voce.index('<a href="https://raw.githubusercontent.com/DanRobo76/'
                                                              "VMC-HELTY-FLOW/main/immagini/Informazioni/"
                                                              "18_priorita_allarmi.png")]

    def riga(trovata: re.Match[str]) -> str:
        celle = re.findall(r"<td[^>]*>(.*?)</td>", trovata.group(0))
        assert len(celle) == 3, trovata.group(0)
        nome, altra, zero = celle
        return (f" - {nome}: si sceglie un'altra Velocità → {altra[0].lower() + altra[1:]}; si sceglie Velocità 0 → "
                f"{zero[0].lower() + zero[1:]}; ")

    voce = re.sub(r"<tr><td.*?</tr>", riga, voce)
    ultima = voce.rindex("; ", 0, voce.index("</table>", voce.index("CAMBIO DI VELOCIT")))
    voce = voce[:ultima] + ". " + voce[ultima + 2:]
    voce = re.sub(r'<tr><th colspan="3"[^>]*>(.*?)</th></tr>', lambda m: " " + m.group(1) + ": ", voce)
    voce = re.sub(r"<tr><th.*?</tr>", " ", voce)
    voce = re.sub(r"<[^>]+>", " ", voce)
    return _norm(html.unescape(voce))


def _render(hass, modello: str, variabili: dict[str, Any] | None = None) -> str:
    return Template(modello, hass).async_render(variabili or {}, parse_result=False)


# ------------------------------------------------------------------------------------------- allineamento
def test_descrizione_e_voce_17_allineate() -> None:
    descrizione = _descrizione()
    descrizione = descrizione[descrizione.index("- Congelamento ≤ -18"):]
    assert _voce_17_come_descrizione() == descrizione


def test_fini_riga_e_yaml() -> None:
    for nome in ("vmc_master.yaml", "vmc_master_scheda_manuale_interfaccia.txt"):
        grezzo = (PKG / nome).read_bytes()
        assert grezzo.count(b"\r\n") == grezzo.count(b"\n"), nome
    assert b"\r" not in (PKG / "vmc_master_automazione.txt").read_bytes()
    for nome in ("README.md", ".github/README.md"):
        assert b"\r" not in (RADICE / nome).read_bytes(), nome
    assert _pacchetto()["script"]
    assert _descrizione()


# ------------------------------------------------------------------- frasi nella descrizione e nella voce 17
# (frase, quante volte nella descrizione e nella voce 17): le frasi delle righe della tabella sono scelte senza la
# prima lettera della cella, che nella descrizione è minuscola
FRASI_17 = [
    # C5-4 n. 1 (A21) e C4-4: Set Umidità a Velocità 0, anche con la Free sospesa (avvio, rami TeVsTi e fine
    # Inquinanti, dove con un'altra Velocità di avvio la Free sospesa dà la Velocità 1)
    ("Umidità: 28 Secondi (la logica Umidità memorizza subito la Velocità in uso); con la [Set Velocità Umidità di "
     "Avvio] su Velocità 0 l'allerta Umidità si accende ma la VMC resta ferma, anche con la Free Cool./Heat. sospesa "
     "(all'avvio dell'Umidità, all'arresto per condizioni sfavorevoli e a fine Inquinanti, dove con un'altra Velocità di "
     "avvio la VMC va a Velocità 1 [Nota 3]); se durante l'allerta si cambia Velocità", 1),
    (f"finché quell'allerta non è finita ({FREE_ECC}; {SET0}). Esempio:", 1),
    (f"l'allerta Umidità non scatta e l'interruttore si spegne normalmente ({FREE_ECC}; {SET0});", 1),
    # C5-4 n. 2 (A21): Umidità avviata da 0 e Inquinanti a fine Umidità, 28 s, la velocità scelta resta
    ("se l'Umidità ha avviato la VMC da Velocità 0, la VMC è ancora alla [Set Velocità Umidità di Avvio] e a fine "
     "Umidità sono ancora presenti gli Inquinanti, la VMC scende a Velocità 1 dopo 28 Secondi e torna a Velocità 0 al "
     "rientro degli Inquinanti (se l'utente ha scelto un'altra Velocità, quella resta);", 1),
    # C5-4 n. 3 (G7): con la Free sospesa nessun cambio
    ("(per fermarla si spegne l'interruttore dell'Umidità; con la Free Cool./Heat. sospesa nessun cambio: la VMC resta "
     "a Velocità 0);", 1),
    ("Con la Free Cool./Heat. sospesa nessun cambio: la VMC resta a Velocità 0", 1),
    # C5-4 n. 4 (D6): Velocità 1 durante il Δ (voce e tabella)
    ("(se l'allerta finisce prima che sia memorizzata, la Velocità scelta resta); scegliere Velocità 1 non cambia la "
     "memoria;", 1),
    ("(se l'allerta finisce prima che sia memorizzata, resta la Velocità scelta); scegliere Velocità 1 non cambia la "
     "memoria;", 1),
    # C5-4 n. 5 (E6): 8 s di memorizzazione degli Inquinanti (voce e tabella)
    ("(anche durante il Congelamento o il Δ Temp.) questa viene memorizzata dopo 8 Secondi e mantenuta, anche dopo il "
     "rientro;", 1),
    ("iene memorizzata dopo 8 Secondi e mantenuta, anche dopo il rientro degli Inquinanti (anche la Velocità 1 scelta "
     "con la VMC in Free Cool./Heat. e PdR superato);", 1),
    # C5-4 n. 6 (A29): Inquinanti durante l'avviso Free e Free scelta con le condizioni sfavorevoli (voce e tabella)
    ("anche se le condizioni sono già tornate favorevoli (con Inquinanti la Velocità scelta viene memorizzata "
     "dall'allerta Inquinanti dopo 8 Secondi); scegliendo Free Cool./Heat. con le condizioni ancora sfavorevoli la VMC "
     "torna a Velocità 0 dopo 24 Secondi;", 1),
    ("(ripresa in attesa); con Inquinanti la Velocità scelta viene memorizzata dall'allerta Inquinanti dopo 8 Secondi; "
     "scegliendo Free Cool./Heat. con le condizioni ancora sfavorevoli la VMC torna a Velocità 0 dopo 24 Secondi;", 1),
    # C5-4 n. 7 (F6): PdR non calcolabile
    ("se il Punto di Rugiada non è calcolabile (per esempio con l'Umidità Esterna non disponibile) l'allerta non parte "
     "e, se è in corso, termina: la VMC riprende la Velocità memorizzata dopo 16 Secondi (12 con Inquinanti);", 1),
    # C5-4 n. 8 (A25 N.B.): attese, uscita con Inquinanti, 2° Fascia in corso, giorno non valido
    ("(attesa dello script della Fascia). L'Ingresso e l'Uscita aspettano la fine di un'allerta Congelamento o Δ Temp. "
     "e il ritorno ON-Line della VMC; dopo un riavvio di Home Assistant aspettano il 3° gruppo del riallineamento (140 "
     "Secondi dall'avvio).", 1),
    ("All'uscita dalla Fascia la VMC si arresta: con Inquinanti presenti la logica Inquinanti riparte dalla VMC ferma "
     "(Velocità 1 fino al rientro, poi Velocità 0); se la 2° Fascia dello stesso giorno è già in corso, la fine della "
     "1° Fascia non ferma la VMC (la comanda la 2° Fascia). Le Fasce non possono attraversare la mezzanotte (lo "
     "Spegnimento deve seguire l'Accensione nello stesso giorno); la 1° Fascia deve precedere la 2° (almeno 1 minuto "
     "tra il 1° Spegnimento e la 2° Accensione) e tutti gli orari devono essere diversi: se una regola non è "
     "rispettata il giorno risulta «Disabilitata» e nessuna delle due Fasce parte.", 1),
    # C3-2: velocità scelta durante gli 8 s di attesa della fine degli Inquinanti (voce e tabella)
    ("anche se prima dell'allerta era a un'altra Velocità; una Velocità scelta durante gli 8 Secondi di attesa dopo il "
     "rientro degli Inquinanti resta e la Velocità memorizzata non viene ripristinata (salvo se la Free Cool./Heat. è "
     "sospesa da un'allerta, che ha la sua ripresa, o con un'allerta Congelamento o Δ Temp. in corso);", 1),
    ("e PdR superato); anche una Velocità scelta durante gli 8 Secondi di attesa dopo il rientro resta (salvo se la "
     "Free Cool./Heat. è sospesa da un'allerta o con un'allerta Congelamento o Δ Temp. in corso)", 1),
    # C1-2: i 32 s si contano da quando la VMC è ON-Line con la velocità di nuovo leggibile (Black-Out e Calendario);
    # durante il riallineamento al riavvio dal ritorno ON-Line, o dalla lettura valida se la velocità non si legge
    ("la VMC riparte con la Velocità della Fascia in corso 32 Secondi dopo che è di nuovo ON-Line con la velocità "
     "leggibile (+5 Secondi dello script della Fascia)", 2),
    ("dopo almeno 32 Secondi OFF-Line, la VMC riparte 32 Secondi dopo il ritorno ON-Line anche se il Black-Out non è "
     "stato ancora memorizzato (se in quel momento la sua velocità non si legge ancora, riparte 32 Secondi dopo che "
     "torna leggibile, non prima dell'ultima fase del riallineamento);", 1),
    # C1-3 e C1-5: attesa della fine di Congelamento/Δ e comando dello spegnimento del Calendario
    ("la Fascia riparte, salvo se nel frattempo la Velocità è cambiata (per esempio con il Telecomando); lo stesso vale "
     "per la Velocità 0 di fine Fascia e per il comando dato spegnendo l'interruttore del Calendario durante una Fascia "
     "(Velocità 0, o Velocità 1 con Inquinanti): appena la velocità torna leggibile il comando viene ripetuto, anche "
     "con l'interruttore del Calendario spento, salvo se nel frattempo la Velocità è cambiata; con un'allerta "
     "Congelamento o Δ Temp. in corso il comando del Calendario aspetta la fine dell'allerta: a fine allerta, appena la "
     "velocità è leggibile, la Fascia riparte con la sua Velocità (o si ripete la Velocità 0, o 1, in sospeso) al posto "
     "della Velocità memorizzata dall'allerta, salvo se si sceglie un'altra Velocità dopo la fine dell'allerta; se "
     "invece la corrente manca proprio mentre la Fascia finisce o mentre si spegne l'interruttore del Calendario, al "
     "ritorno della corrente la VMC si arresta dopo 32 Secondi (o va a Velocità 1, se l'interruttore è stato spento "
     "con Inquinanti presenti);", 1),
    ("si ferma: passa a Velocità 1 e si ferma quando gli Inquinanti rientrano; il comando dato spegnendo "
     "l'interruttore del Calendario viene ripetuto finché la VMC non lo esegue, anche se nel frattempo la sua velocità "
     "non si legge o la VMC va OFF-Line (vedere Black-Out);", 1),
    # C4-3: velocità scelta poco prima del PdR con la ripresa Free in attesa
    ("anche al posto della ripresa in Free Cool./Heat. (lo stesso vale per una Velocità scelta poco prima "
     "dell'allerta, con la ripresa in attesa);", 1),
    # C4-5 (e ramo del PdR con la VMC non disponibile): anche durante il ripristino dopo un Black-Out; l'interruttore
    # dell'Umidita' si riaccende nei casi in cui non si puo' spegnere (altre allerte, Free in attesa, Calendario)
    ("- se la VMC è OFF-Line, la sua velocità non è disponibile o è in corso il ripristino dopo un Black-Out, "
     "l'interruttore del Punto di Rugiada o dell'Umidità spento durante l'allerta resta spento (salvo, per l'Umidità, i "
     "casi qui sopra in cui il suo interruttore non si può spegnere) e si azzerano solo le memorie della sua allerta, "
     "senza comandi alla VMC: al ritorno la VMC resta alla velocità letta (o a quella ripristinata dopo il "
     "Black-Out);", 1),
    # b35 C4-2: Umidità partita da 0 e finita durante il PdR
    ("se l'Umidità aveva avviato la VMC da Velocità 0 ed è finita durante l'allerta, al termine dell'allerta la VMC "
     "resta a Velocità 0;", 1),
    # b35 C3-3: interruttore spento nei primi secondi dell'allerta
    ("- se in quel momento la sua funzione sta comandando la VMC (allerta in corso, anche appena iniziata, o Velocità "
     "impostata da quell'allerta), la VMC si ferma subito (Velocità 0, in 0 Secondi)", 1),
]


@pytest.mark.parametrize(("frase", "volte"), FRASI_17, ids=[f"{n:02d}" for n in range(len(FRASI_17))])
def test_frasi_nuove_nella_descrizione_e_nella_voce_17(frase: str, volte: int) -> None:
    assert _descrizione().count(frase) == volte
    assert _voce_17_come_descrizione().count(frase) == volte


def test_vecchie_frasi_sostituite() -> None:
    """Le frasi della b35 che dicevano i 32 s dal ping, la Free sospesa senza il Set a Velocità 0 e i comandi del
    Calendario non ripetuti con Congelamento o Δ Temp. in corso."""
    for testo in (_descrizione(), _voce_17()):
        assert "la VMC riparte con la Velocità della Fascia in corso dopo 32 Secondi" not in testo
        assert "la VMC riparte 32 Secondi dopo il ritorno anche se" not in testo
        assert "32 Secondi dopo che la sua velocità torna leggibile" not in testo
        assert f"({FREE_ECC})" not in testo
        assert "salvo se nel frattempo la Velocità è cambiata o è in corso un'allerta Congelamento o Δ Temp." not in testo
    assert "la Velocità della Fascia in corso (se nel frattempo la Fascia è finita, si arresta);" in _descrizione()


# ------------------------------------------------------------------------------------- voci delle Informazioni
def test_voce_7_umidita() -> None:
    voce = _voce(7)
    assert f"su ON e senza altre allerte in corso ({FREE_ECC}; {SET0}), comandano l'avvio" in voce
    assert f"l'interruttore si spegne normalmente ({FREE_ECC}; {SET0})." in voce
    assert ("L'avvio e l'arresto avvengono dopo 28 secondi. Con la [Set Velocità Umidità di Avvio] su Velocità 0 "
            "l'allerta Umidità si accende ma la VMC resta ferma, anche con la Free Cool./Heat. sospesa (all'avvio "
            "dell'Umidità, all'arresto per condizioni sfavorevoli e a fine Inquinanti, dove con un'altra velocità di "
            "avvio la VMC va a Velocità 1 [Nota 3]).") in voce
    assert ("Con la Free Cool./Heat. sospesa (Umidità partita a Velocità 1 [Nota 3]) nessun cambio: la VMC resta a "
            "Velocità 0.") in voce
    assert ("• Se l'Umidità ha avviato la VMC da Velocità 0, la VMC è ancora alla [Set Velocità Umidità di Avvio] e a "
            "fine Umidità sono ancora presenti gli Inquinanti, la VMC scende a Velocità 1 dopo 28 secondi e torna a "
            "Velocità 0 al rientro degli Inquinanti (se si è scelta un'altra velocità, quella resta).") in voce
    assert ("• Se l'interruttore viene spento durante un'allerta Umidità, la VMC si arresta; con la VMC OFF-Line, con "
            "la sua velocità non disponibile o durante il ripristino dopo un Black-Out l'interruttore resta spento e si "
            "azzerano solo l'allerta e le memorie "
            "dell'Umidità, senza comandi alla VMC: al ritorno la VMC resta alla velocità letta (o a quella ripristinata "
            "dopo il Black-Out).") in voce


def test_voce_8_pdr_non_calcolabile() -> None:
    assert ("Se il Punto di Rugiada non è calcolabile (per esempio con l'Umidità Esterna non disponibile) l'allerta non "
            "parte e, se è in corso, termina: la VMC riprende la velocità memorizzata dopo 16 secondi (12 con "
            "Inquinanti).") in _voce(8)


def test_voce_10_inquinanti() -> None:
    assert ("Una velocità scelta durante l'allerta viene memorizzata dopo 8 secondi e mantenuta anche a fine allerta "
            "(con la Velocità 0 la VMC riparte invece a Velocità 1 dopo circa 8 secondi). A fine allerta (CO₂ e VOC "
            "entrambi rientrati) la VMC torna dopo 8 secondi alla velocità precedente, Velocità 0 se era ferma; una "
            "velocità scelta durante questi 8 secondi resta (salvo se la velocità da ripristinare è Free Cool./Heat. o "
            "è in corso un'allerta Congelamento o Δ Temp.). Spegnendo l'interruttore durante l'allerta, anche nei "
            "primi 8 secondi, la VMC si arresta subito.") in _voce(10)


def test_voce_12_calendario() -> None:
    voce = _voce(12)
    assert ("all'uscita la VMC si arresta. L'ingresso e l'uscita aspettano la fine di un'allerta Congelamento o Δ "
            "Temp. e il ritorno ON-Line della VMC; dopo un riavvio di Home Assistant aspettano il 3° gruppo (140 "
            "secondi dall'avvio, voce 15, Nota Avvio di Home Assistant). All'uscita, con Inquinanti presenti, la "
            "logica Inquinanti riparte dalla VMC ferma (Velocità 1 fino al rientro, poi Velocità 0); se la 2° Fascia "
            "dello stesso giorno è già in corso, la fine della 1° non ferma la VMC (la comanda la 2° Fascia).") in voce
    assert ("<b>Giorno non valido.</b> Le Fasce non possono attraversare la mezzanotte e devono rispettare le regole "
            "qui sotto: se una regola non è rispettata il giorno risulta «Disabilitata» e nessuna delle due Fasce "
            "parte.") in voce


def test_voce_14_free() -> None:
    voce = _voce(14)
    assert ("Con un'allerta Lim. Δ PdR in corso la ripresa attende il termine dell'allerta. Se però all'inizio "
            "dell'allerta Lim. Δ PdR la VMC è a una velocità scelta dall'utente, a fine allerta torna quella velocità, "
            "al posto della ripresa.") in voce
    assert ("la velocità scelta ha la precedenza. Con Inquinanti la velocità scelta viene memorizzata dall'allerta "
            "Inquinanti dopo 8 secondi. Se si sceglie Velocità 0 non cambia nulla (la VMC è già ferma) e quando la "
            "condizione torna favorevole la VMC riprende in Free Cool./Heat.; scegliendo Free Cool./Heat. con la "
            "condizione ancora sfavorevole la VMC torna a Velocità 0 dopo 24 secondi.") in voce
    # C4-4 esteso ai rami TeVsTi: con il Set a Velocita' 0 l'Umidita' non porta la VMC a Velocita' 1
    assert ("Anche con un'allerta Umidità in corso la VMC, invece di arrestarsi, passa a Velocità 1 (dopo 24 secondi), "
            "salvo con la [Set Velocità Umidità di Avvio] su Velocità 0: in questo caso si arresta.") in voce


def test_voce_15_ripristino_dopo_black_out() -> None:
    assert ("con il countdown «Ripristino dopo Black-Out» (32 secondi, contati da quando la VMC è di nuovo ON-Line con "
            "la velocità leggibile): dopo altri 5 secondi la VMC riparte con la velocità della fascia") in _voce(15)


# ------------------------------------------------------------------------------- Riquadro Avvisi e scheda Umidità
def test_riquadro_avvisi_comando_non_eseguito() -> None:
    riga = ('label: "La VMC risponde in rete ma la sua velocità non si legge: il comando del Calendario (velocità della '
            "fascia, Velocità 0 di fine fascia o comando dato spegnendo l'interruttore del Calendario durante la fascia) "
            "non è confermato. Appena la velocità torna leggibile il comando riparte, salvo se nel frattempo la velocità "
            "è cambiata; con un'allerta Congelamento o Δ Temp. in corso il comando riparte alla fine dell'allerta, al "
            "posto della velocità memorizzata dall'allerta. Non serve fare nulla.\"")
    assert _scheda().count(riga) == 1


def _msg_2_umidita() -> str:
    scheda = _scheda()
    centro = scheda.index("{% set velocita_1_per_free")
    stato = "{{states('sensor.vmc_master_umidita_interna_status_verifica_soglia_valore')}}"
    return scheda[scheda.rindex(stato, 0, centro) + len(stato): scheda.index("Msg. 2", centro)]


@pytest.mark.parametrize(
    ("set_umidita", "spia_free", "atteso", "nota"),
    [
        # C4-4: Set a Velocità 0 e Free sospesa -> la VMC resta ferma (non piu' «Velocita' 1 per Free»)
        ("Velocità 0", "on", "AVVIO AUTOMATICO DELLA VMC SU <strong>Velocità 0</strong> IMPOSTATA", True),
        ("Velocità 0", "off", "AVVIO AUTOMATICO DELLA VMC SU <strong>Velocità 0</strong> IMPOSTATA", True),
        ("Velocità 2", "on", "AVVIO AUTOMATICO DELLA VMC SU <strong>Velocità 1</strong> IMPOSTATA PER ALLERTA FREE", False),
        ("Velocità 2", "off", "AVVIO AUTOMATICO DELLA VMC SU <strong>Velocità 2</strong> IMPOSTATA", True),
    ],
)
async def test_scheda_umidita_msg_2_set_velocita_0(hass, set_umidita: str, spia_free: str, atteso: str,
                                                   nota: bool) -> None:
    hass.states.async_set(SET_UMIDITA, set_umidita)
    hass.states.async_set(FREE_C, spia_free)
    testo = _norm(_render(hass, _msg_2_umidita(), {"attendere": "ATTENDERE"}))
    assert atteso in testo
    assert ("PER ALLERTA FREE" in testo) is (not nota)
    assert ("<strong>NOTA</strong>" in testo) is nota


# ------------------------------------------------- schede Congelamento e Δ Temp.: comando del Calendario in sospeso
CNE = "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"
ANNUNCIO = ("AL TERMINE DELL'ALLERTA RIPARTIRÀ IL COMANDO DEL CALENDARIO IN SOSPESO, NON LA VELOCITÀ MEMORIZZATA "
            "DALL'ALLERTA: LA VMC ANDRÀ ALLA <strong>{{ cal_cne_vel }}</strong>")


def _schede_gelo_delta() -> list[tuple[str, list[str]]]:
    """Per le schede Congelamento e Δ Temp.: le righe «{% set cal_… %}» in cima e gli annunci della ripresa."""
    scheda = _scheda().replace("\r\n", "\n")
    schede = []
    inizio = 0
    while (inizio := scheda.find("{% set cal_g = ", inizio + 1)) != -1:
        testa = scheda[inizio: scheda.index("{% set ti_vmc_ripresa", inizio)]
        fine = scheda.find("{% set cal_g = ", inizio + 1)
        corpo = scheda[inizio: fine if fine != -1 else len(scheda)]
        annunci = [corpo[i: corpo.index("endif %}", i) + len("endif %}")]
                   for i in [m.start() for m in re.finditer(r"\{% if cal_uscita %\}", corpo)]]
        schede.append((testa, annunci))
    return schede


def test_schede_gelo_delta_annuncio_del_comando_in_sospeso() -> None:
    schede = _schede_gelo_delta()
    assert len(schede) == 2
    assert sum(len(annunci) for _, annunci in schede) == 18
    for testa, annunci in schede:
        assert f"{{% set cal_cne = is_state('{CNE}', 'on') %}}" in testa
        for annuncio in annunci:
            # dopo la fascia finita o iniziata durante l'allerta (decide il Calendario), prima della velocita' memorizzata
            assert annuncio.index("{% elif cal_ingresso %}") < annuncio.index("{% elif cal_cne %}" + ANNUNCIO) < \
                annuncio.index('{% elif spia_velocita_0=="on"')
    # le due schede intere restano Jinja valido
    import jinja2

    contenuti: list[str] = []

    def cerca(nodo: Any) -> None:
        if isinstance(nodo, dict):
            for chiave, valore in nodo.items():
                if chiave == "content" and isinstance(valore, str) and "{% set cal_cne =" in valore:
                    contenuti.append(valore)
                cerca(valore)
        elif isinstance(nodo, list):
            for valore in nodo:
                cerca(valore)

    cerca(hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt")))
    assert len(contenuti) == 2
    for contenuto in contenuti:
        jinja2.Environment(extensions=["jinja2.ext.loopcontrols"]).parse(contenuto)


@pytest.mark.parametrize(
    ("cne", "fascia", "inquinanti", "atteso"),
    [
        ("on", False, False, "LA VMC ANDRÀ ALLA <strong>VELOCITÀ 0</strong>"),
        ("on", False, True, "LA VMC ANDRÀ ALLA <strong>VELOCITÀ 1 (INQUINANTI PRESENTI)</strong>"),
        ("on", True, False, "LA VMC ANDRÀ ALLA <strong>VELOCITÀ DELLA FASCIA DEL CALENDARIO</strong>"),
        ("off", False, False, "RIPRESA AUTOMATICA DELLA VMC SULLA <strong>VELOCITA' 2</strong>"),
        ("off", True, False, "RIPRESA AUTOMATICA DELLA VMC SULLA <strong>VELOCITA' 2</strong>"),
    ],
)
async def test_schede_gelo_delta_annuncio_mostrato(hass, cne: str, fascia: bool, inquinanti: bool,
                                                   atteso: str) -> None:
    from homeassistant.util import dt as dt_util

    giorno = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"][dt_util.now().weekday()]
    hass.states.async_set(CNE, cne)
    hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{giorno}_1", "on" if fascia else "off")
    hass.states.async_set(f"input_datetime.vmc_master_accensione_{giorno}", "00:00:00")
    hass.states.async_set(f"input_datetime.vmc_master_spegnimento_{giorno}", "23:59:59")
    hass.states.async_set("input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario", "on")
    for entita in ("input_boolean.vmc_master_spia_co2_o_voc",
                   "input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0"):
        hass.states.async_set(entita, "on" if inquinanti else "off")
    for testa, annunci in _schede_gelo_delta():
        for annuncio in annunci:
            testo = _norm(_render(hass, testa + annuncio, {"spia_velocita_2": "on"}))
            assert atteso in testo, testo
            assert ("IL COMANDO DEL CALENDARIO IN SOSPESO" in testo) is (cne == "on")


# ---------------------------------------------------------------------------- script delle Fasce e Countdown
def test_descrizioni_degli_script_di_fascia() -> None:
    script = _pacchetto()["script"]
    uno, due = (_norm(script[f"vmc_master_calendario_fascia_{n}_on"]["description"]) for n in (1, 2))
    assert uno.replace("1° Fascia", "2° Fascia") == due
    # C1-2 e C1-3
    assert ("al ritorno della corrente dopo un Black-Out (VMC OFF-Line almeno 32 s; lo script parte 32 s dopo che la "
            "VMC è di nuovo ON-Line con la velocità leggibile) e quando la VMC torna a rispondere dopo un comando non "
            "eseguito (con un'allerta Congelamento o Δ Temp. in corso, alla fine dell'allerta, al posto della velocità "
            "memorizzata dall'allerta).") in uno
    assert ("la Velocità 0 viene ripetuta, salvo se nel frattempo la velocità è cambiata (con un'allerta Congelamento o "
            "Δ Temp. in corso, alla fine dell'allerta); se invece la VMC va OFF-Line prima di confermarla") in uno
    # C1-5
    assert ("rimandata al ritorno della corrente. Lo stesso vale per il comando che l'Automazione manda quando si spegne "
            "l'interruttore del Calendario durante la Fascia (Velocità 0, o Velocità 1 con gli Inquinanti), che viene "
            "ripetuto anche con l'interruttore spento.") in uno
    assert "o è in corso un'allerta Congelamento o Δ Temp." not in uno
    for vietata in VIETATE:
        assert vietata not in uno


def test_descrizione_del_countdown_attese() -> None:
    (countdown,) = (a for a in _pacchetto()["automation"] if a["id"] == "vmc_master_countdown_attese_automazione")
    testo = _norm(countdown["description"])
    assert ("per il ritorno della corrente durante una Fascia del Calendario il timer parte quando la VMC è di nuovo "
            "ON-Line con la velocità leggibile e solo se valgono anche le condizioni del ramo dell'automazione") in testo
    assert "vmc_master" not in testo and " master" not in testo


# ------------------------------------------------------------------------------------------------- README
@pytest.mark.parametrize("nome", ["README.md", ".github/README.md"])
def test_readme_black_out_a_fine_fascia(nome: str) -> None:
    """b35 C1-1: se la corrente torna a Fascia finita la VMC si arresta (IT ed EN); b36: una velocità scelta prima del
    ritorno della Fascia resta."""
    testo = (RADICE / nome).read_text(encoding="utf-8")
    assert testo.count("la VMC riparte con la velocità della fascia in corso (se nel frattempo la fascia è finita, si "
                       "arresta; una velocità scelta prima resta).</sub>") == 1
    assert testo.count("the unit restarts at the speed of the current slot (if the slot has ended in the meantime, it "
                       "stops; a speed picked before is kept).</sub>") == 1
