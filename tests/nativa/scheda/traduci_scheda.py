"""Traduttore della scheda «VMC Master» ai nomi delle entità native (fase 4).

La scheda di oggi è ``package/vmc_master_scheda_manuale_interfaccia.txt``: l'integrazione
la serve a ogni VMC con ``trasforma.per_vmc`` (tolte le sezioni Clona VMC e Installa VMC,
poi nome e IP della VMC). Usa gli aiutanti, i timer, gli script e i comandi di shell del
package; domani quelli che la scheda mostra o comanda sono entità native con lo stesso
oggetto dopo il punto e il dominio nuovo (colonna «Domani» di ``aiutanti_fase1.csv``).

Il traduttore parte dalla scheda della VMC Master senza le due sezioni
(``rimuovi_sezioni_solo_master``) e cambia soltanto:

- ``nome``: ogni entità prende il nome di domani (``input_boolean.vmc_master_x`` ->
  ``switch.vmc_master_x``), ovunque compaia (righe, condizioni, bersagli, modelli);
- ``frammento``: i nomi che i modelli compongono a pezzi
  (``'input_datetime.vmc_master_accensione_' ~ giorno``) cambiano dominio, se tutte le
  entità che cominciano così vanno nello stesso dominio con lo stesso oggetto;
- ``servizio``: ``input_boolean.toggle`` / ``turn_on`` / ``turn_off`` -> ``switch.*``;
  ``script.turn_on`` dello script ``x`` -> ``button.press`` del pulsante ``x``;
- ``comando``: un comando di shell chiamato dalla scheda
  (``shell_command.vmc_master_velocita_1``, senza bersaglio) -> ``button.press`` con
  bersaglio il pulsante dello stesso oggetto;
- ``riga conto alla rovescia``: la riga di un timer (conto alla rovescia «0:04:59» o
  «Inattivo») diventa la riga ``custom:vmc-master-conto-alla-rovescia`` della scheda
  (``frontend/vmc-master-card.js``) sul sensore con l'ora di fine, che disegna la stessa
  riga del timer;
- ``colore riga conto alla rovescia``: la stessa riga ha scritto il colore che la scheda
  entities dà oggi alla riga del timer (``color: state``, o ``none`` se la scheda ha
  ``state_color: false``): il frontend lo passa alle righe senza tipo, non a quelle
  ``custom:``, e senza l'icona del timer attivo non sarebbe più colorata;
- ``condizione timer``: ``state: active`` -> ``state_not: [unknown, unavailable]`` e
  ``state: idle`` -> ``state: unknown`` (il sensore vale l'ora di fine mentre il timer
  interno gira, ``unknown`` quando è fermo, vedi ``CONTO_ALLA_ROVESCIA``);
- ``elenco``: dall'elenco di «Pulisci cronologia» escono le voci che domani non sono
  entità (aiutanti e script interni del motore, automazioni del motore, voci tolte);
- ``riga tolta``: escono le righe di una voce tolta (b46: il campo «Cambia IP VMC», che
  domani non c'è) e le righe ``conditional`` con una condizione su una voce tolta; l'IP si
  cambia dall'ingranaggio della VMC;
- ``chiave tipi``: nel modello che conta le voci dell'elenco per tipo, le chiavi dei
  domini di oggi diventano quelle di domani;
- ``esclusioni``: dal modello di «Pulisci cronologia» esce il ramo per le entità escluse dal
  Recorder (da ``{%- set escluse = ...`` a ``{%- else -%}``, e il suo ``{%- endif -%}``):
  domani nessuna entità è esclusa (un'integrazione del catalogo non può escludere entità dal
  Recorder) e il riquadro mostra sempre il ramo che c'era già per questo caso, con tutte le
  entità e il loro numero vero, qualunque cosa scriva il sensore delle entità escluse;
- ``testo``: i testi che domani non sono più veri (il package e i suoi file, i domini degli
  aiutanti, le automazioni e gli script, le esclusioni dal Recorder, i tempi di attesa
  modificabili) diventano quelli di ``TESTI``, ognuno trovato esattamente le volte previste;
- ``intestazione``: nelle righe di commento prima della scheda il link al repository di
  prima diventa quello nuovo (``COMMENTI``), con la cornice di «#» allineata.

Tutto il resto (gli altri testi, disposizione, stili, gli altri commenti) resta identico,
byte per byte.
Ogni modifica è nella lista ``Traduzione.modifiche``; un nome che il traduttore non sa
tradurre ferma la traduzione (``NonTraducibile``).
"""

from __future__ import annotations

import bisect
import csv
import io
import re
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from custom_components.vmc_master.trasforma import rimuovi_sezioni_solo_master

RADICE = Path(__file__).resolve().parents[3]
QUI = Path(__file__).resolve().parent
SCHEDA = (
    RADICE
    / "custom_components/vmc_master/package/vmc_master_scheda_manuale_interfaccia.txt"
)
USCITA = RADICE / "custom_components/vmc_master/nativa/scheda_nativa.txt"
MODIFICHE = QUI / "modifiche_scheda.csv"
TOTALI = QUI / "modifiche_scheda_totali.txt"
FASE_1 = RADICE / "tests/nativa/motore/aiutanti_fase1.csv"
TRADUZIONE_FASE_1 = QUI / "traduzione_scheda.csv"

# Riga della scheda (frontend/vmc-master-card.js) che disegna il conto alla rovescia di un
# timer interno dal sensore con l'ora di fine.
RIGA_CONTO = "custom:vmc-master-conto-alla-rovescia"
# Stati del sensore con l'ora di fine (convenzione della fase 4): ora di fine (ISO 8601,
# classe timestamp) mentre il timer interno gira, «unknown» quando è fermo; mai
# «unavailable» mentre l'integrazione gira. Le condizioni del timer diventano:
CONTO_ALLA_ROVESCIA = {
    "active": "state_not: [unknown, unavailable]",
    "idle": "state: unknown",
}

SERVIZI = {
    "input_boolean.toggle": "switch.toggle",
    "input_boolean.turn_on": "switch.turn_on",
    "input_boolean.turn_off": "switch.turn_off",
    "script.turn_on": "button.press",
}
COMANDO = "shell_command"
PREMI = "button.press"

# Chiavi del modello «tipi» di «Pulisci cronologia» (dominio di oggi -> dominio di domani).
CHIAVI_TIPI = {
    "input_boolean": "switch",
    "input_datetime": "time",
    "input_number": "number",
    "input_select": "select",
    "input_text": "text",
}
_INIZIO_TIPI = "{%- set tipi = {"
_INIZIO_ELENCO = "{%- set elenco = ["
_FINE_ELENCO = "] -%}"


@dataclass(frozen=True)
class Testo:
    """Un testo della scheda che domani non è più vero: ``prima`` (parole separate da uno
    spazio; nel file ogni spazio può essere anche un a capo con il rientro; un ``\\n`` è la
    fine di un capoverso, cioè nel file una riga vuota) diventa ``dopo``, esattamente
    ``volte`` volte."""

    prima: str
    dopo: str
    volte: int = 1


# I testi da aggiornare (regola del progetto: quando il comportamento cambia, si aggiornano
# tutte le descrizioni). Domani non ci sono il package né i suoi file (vmc_master.yaml, le
# esclusioni dal Recorder, la cartella dei backup), gli aiutanti, le automazioni e gli
# script: c'è l'integrazione, con spie (sensori binari), interruttori e pulsanti.
TESTI = (
    Testo(
        "il package usa la sonda della VMC", "l'integrazione usa la sonda della VMC", 2
    ),
    Testo("'Interruttori (input_boolean)'", "'Interruttori'"),
    Testo("'Orari (input_datetime)'", "'Orari'"),
    Testo("'Valori numerici (input_number)'", "'Valori numerici'"),
    Testo("'Selettori (input_select)'", "'Selettori'"),
    Testo("'Testi (input_text)'", "'Testi'"),
    Testo("Se il Package ti è utile", "Se l'integrazione ti è utile"),
    Testo(
        "/marketplace/repository?owner=DanRobo76&repository=VMC-HELTY-FLOW-MARKETPLACE&",
        "/marketplace/repository?owner=DanRobo76&repository=VMC-HELTY-FLOW-MASTER&",
    ),
    Testo(
        '<a href="https://github.com/DanRobo76/VMC-HELTY-FLOW">GitHub</a>',
        '<a href="https://github.com/DanRobo76/VMC-HELTY-FLOW-MASTER">GitHub</a>',
    ),
    Testo(
        "Sono i dati da cui il Package ricava",
        "Sono i dati da cui l'integrazione ricava",
    ),
    Testo(
        "Gli intervalli sono gli scan_interval del file vmc_master.yaml e non si"
        " modificano dalla scheda.",
        "Gli intervalli sono fissati dall'integrazione e non si modificano dalla scheda.",
    ),
    Testo(
        "si sovrappongono ai comandi dell'automazione VMC Master:",
        "si sovrappongono ai comandi dell'integrazione VMC Master:",
    ),
    Testo(
        "le decisioni restano solo all'automazione,",
        "le decisioni restano solo all'integrazione,",
    ),
    Testo(
        "influenzano il comportamento del Package",
        "influenzano il comportamento dell'integrazione",
        2,
    ),
    Testo("bypassando il presente Package.", "bypassando l'integrazione."),
    Testo(
        "Il Package confronta il Δ solo con il Set",
        "L'integrazione confronta il Δ solo con il Set",
    ),
    Testo("dello script della Fascia", "della procedura della Fascia", 4),
    Testo(
        "Il controllo che il Package esegue", "Il controllo che l'integrazione esegue"
    ),
    Testo(
        "Cancella dal database lo storico (grafici e registro) delle entità del Package;"
        " entità e impostazioni restano invariate. Prima di procedere mostra un riquadro"
        " con il numero e l'elenco delle sole entità registrate nel database e chiede"
        " conferma con «Sì» o «No». Le entità registrate e quelle escluse sono indicate"
        " nell'unico elenco della sezione «recorder» del file vmc_master.yaml (riga"
        " commentata con # = registrata). Il file è scritto dall'integrazione e non va"
        " modificato: se viene modificato a mano, all'avvio di Home Assistant la sua copia"
        " viene salvata nella cartella vmc_master_backup, il file torna quello"
        " dell'integrazione e compare una notifica.",
        "Cancella dal database lo storico (grafici e registro) delle entità della VMC;"
        " entità e impostazioni restano invariate. Prima di procedere mostra un riquadro"
        " con il numero e l'elenco delle entità e chiede conferma con «Sì» o «No».",
    ),
    Testo(
        "<b>Quando i sensori della VMC vengono ricaricati</b>: dopo un aggiornamento"
        " dell'integrazione, 20-60 secondi dopo l'avvio, oppure con Impostazioni →"
        " Strumenti → YAML → Ricarica.",
        "<b>Quando i sensori della VMC vengono ricaricati</b>: dopo un aggiornamento"
        " dell'integrazione oppure con «Ricarica» nel menu dell'integrazione"
        " (Impostazioni → Dispositivi e servizi).",
    ),
    Testo(
        "<strong>Nota Conferma degli Script</strong>",
        "<strong>Nota Conferma dei Pulsanti</strong>",
    ),
    Testo("Ogni script chiede conferma", "Ogni pulsante chiede conferma"),
    Testo(
        "<strong>Nota Countdown degli Script</strong>",
        "<strong>Nota Countdown dei Pulsanti</strong>",
    ),
    Testo(
        "Mentre gira uno script che dura qualche secondo,",
        "Mentre è in corso un'operazione che dura qualche secondo,",
    ),
    Testo(
        "se l'automazione finisce prima gli eventi in coda), Profilo Inizializzazione 10"
        " s, Reset Filtro 5 s. Alla fine dello script la riga scompare. Gli altri script"
        " durano al massimo pochi secondi",
        "se l'integrazione finisce prima gli eventi in coda), Profilo Inizializzazione 10"
        " s, Reset Filtro 5 s. Alla fine dell'operazione la riga scompare. Le altre"
        " operazioni durano al massimo pochi secondi",
    ),
    # b46: il campo «Cambia IP VMC» non c'è più (riga tolta): la sua nota dice solo dove
    # si cambia l'IP
    Testo(
        "<strong>Nota Cambia IP VMC (Riavvio di H.A.)</strong>",
        "<strong>Nota Cambia IP VMC</strong>",
    ),
    Testo(
        "Il campo cambia l'IP con cui Home Assistant comunica con la VMC sulla porta 5001."
        " Sono ammessi quattro numeri da 0 a 255 separati da punti, senza zeri iniziali."
        " Non sono ammessi 0.x.x.x, 127.x.x.x, 169.254.x.x e gli indirizzi da 224.x.x.x"
        " in su. L'IP non deve essere già usato da un'altra VMC. Questo controllo vede"
        " solo le VMC già attive: una VMC appena aggiunta, in attesa del riavvio di Home"
        " Assistant, non viene vista. In quel caso, dopo il riavvio l'integrazione rimette"
        " l'IP di prima e lo segnala. Poi l'integrazione controlla che a quell'IP risponda"
        " la VMC con il suo nome. Se il nome della VMC non è ancora stato letto, basta che"
        " risponda una VMC. Se un controllo non va bene, non cambia nulla e sotto il campo"
        " compare il motivo. Altrimenti l'IP viene aggiornato in tutti i file del Package"
        " e dopo 2 secondi Home Assistant si riavvia. Il riavvio parte anche se"
        " l'Automazione VMC Master sta eseguendo altri eventi. Il campo non chiede"
        " conferma: verificare l'IP prima di scriverlo. Per salvare un IP a cui la VMC non"
        " risponde: Impostazioni → Dispositivi e servizi, nella pagina dell'integrazione,"
        " icona ingranaggio sulla riga della VMC → «Cambia l'IP della VMC».",
        "L'IP della VMC si cambia da *Impostazioni → Dispositivi e servizi → VMC Master →"
        " ⚙️ → Cambia l'IP della VMC*.",
    ),
    Testo(
        "si è appena avviato (per esempio dopo Cambia IP VMC), prima",
        "si è appena avviato, prima",
    ),
    Testo(
        "correttamente alle automazioni e/o comandi.",
        "correttamente alle logiche automatiche e/o ai comandi.",
    ),
    Testo(
        "attende che l'automazione termini l'azione in corso",
        "attende che l'integrazione termini l'azione in corso",
    ),
    Testo(
        "Inizializza tutte le Variabili Booleane su [False]",
        "Inizializza tutte le Spie e tutti gli Interruttori su Off",
        2,
    ),
    # b44: per una VMC nuova il Profilo Inizializzazione parte da solo, una volta
    # (__init__._inizializza_una_volta); il pulsante serve per rifarlo
    Testo(
        "Da impiegare solo la prima volta appena installato il Package.",
        "Parte da solo una volta, 140 s dopo l'aggiunta di una VMC nuova (se la VMC è "
        "spenta, quando si accende); non parte per una VMC riaggiunta o passata dalla "
        "versione Marketplace. Il pulsante serve per rifarlo.",
    ),
    # I 24 Tempi di Attesa domani sono valori interni del motore (nessuna entità: nessuno li
    # può cambiare) e lo script che li ripristina è interno (nessun pulsante): riportarli ai
    # valori originali, nel Profilo Inizializzazione o a ogni avvio, non cambia niente di
    # quello che l'utente vede.
    Testo(
        "Attiva i 6 Profili sopra Esposti, Riporta i Tempi di Attesa ai Valori Originali,",
        "Attiva i 6 Profili sopra Esposti,",
    ),
    # lo script non è nella scheda nativa: la sua nota non serve (prova del proprietario del
    # 27-11-2026); il testo parte dalla fine della nota di prima, che resta con il suo «<br>»
    Testo(
        "(10 s). Non riavvia Home Assistant.\n<br>\n<strong>VMC Master - Ripristina Tempi di"
        " Attesa Originali</strong>\nNon ha un pulsante nella scheda: i Tempi di Attesa sono"
        " fissi e non vanno modificati.\nRiporta i 24 Tempi di Attesa dell'Automazione ai"
        " Valori Originali. È compreso nel Profilo Inizializzazione e parte da solo a ogni"
        " avvio di Home Assistant.",
        "(10 s). Non riavvia Home Assistant.",
    ),
    Testo(
        "<summary><b>16 Booleans ON</b></summary>",
        "<summary><b>16 Spie e Interruttori ON</b></summary>",
    ),
    Testo(
        "le variabili booleane (input_boolean) del Package che in questo momento sono su"
        " ON. Sono le «spie» con cui le automazioni ricordano quale logica sta comandando"
        " la VMC e a quale velocità tornare. Le variabili sono raggruppate per funzione:"
        " un riquadro compare solo se almeno una sua variabile è ON; se nessuna è ON la"
        " voce resta vuota.",
        "le spie e gli interruttori dell'integrazione che in questo momento sono su ON."
        " Con le «spie» l'integrazione ricorda quale logica sta comandando la VMC e a"
        " quale velocità tornare. Spie e interruttori sono raggruppati per funzione: un"
        " riquadro compare solo se almeno uno dei suoi è ON; se nessuno è ON la voce resta"
        " vuota.",
    ),
    Testo(
        "Le spie sono gestite solo dalle automazioni e non vanno modificate a mano.",
        "Le spie sono gestite solo dall'integrazione e non si possono modificare a mano.",
    ),
    Testo(
        "I Secondi indicati sono fissi e non vanno modificati: il Profilo"
        " Inizializzazione li riporta comunque ai valori",
        "I Secondi indicati sono fissi e non si possono modificare.",
    ),
    Testo("originali. Mentre l'automazione", "Mentre l'integrazione"),
    Testo("l'automazione non la distingue", "l'integrazione non la distingue"),
    Testo(
        "(automazione «VMC Master - Ripartenza della VMC»;",
        "(logica «Ripartenza della VMC» dell'integrazione;",
    ),
    Testo(
        "avviso di aggiornamento del Package",
        "avviso di aggiornamento dell'integrazione",
    ),
    Testo("comando dell'automazione", "comando dell'integrazione", 4),
    Testo("Il Package lo ricava dal", "L'integrazione lo ricava dal"),
    Testo(
        "Il Package confronta il Punto di Rugiada Interno",
        "L'integrazione confronta il Punto di Rugiada Interno",
    ),
    Testo(
        "che leggono le spie e le allerte dell'automazione. Servono solo"
        " all'interfaccia: non comandano la VMC e non registrano storico.",
        "che leggono le spie e le allerte dell'integrazione. Servono solo"
        " all'interfaccia: non comandano la VMC.",
    ),
)
# Fra due parole del testo: uno spazio, oppure un a capo con il rientro (mai una riga vuota)
_SPAZIO = r"(?:[ \t]+|[ \t]*\r?\n[ \t]*)"
# Fra due capoversi: un a capo, una riga vuota e un a capo con il rientro
_CAPOVERSO = r"[ \t]*\r?\n[ \t]*\r?\n[ \t]*"


def modello_testo(prima: str) -> re.Pattern[str]:
    """Il testo ``prima`` come espressione regolare: ogni spazio è uno spazio o un a capo,
    ogni ``\\n`` una riga vuota."""
    return re.compile(
        _CAPOVERSO.join(
            _SPAZIO.join(re.escape(p) for p in capoverso.split(" "))
            for capoverso in prima.split("\n")
        )
    )


@dataclass(frozen=True)
class Commento:
    """Un testo dell'intestazione della scheda (le righe di commento «#» prima della scheda)
    che domani non è più vero: ``prima`` diventa ``dopo``, una volta. La riga resta lunga
    uguale (in caratteri): gli spazi prima del «#» che chiude la cornice crescono o calano
    di quanto il testo si accorcia o si allunga."""

    prima: str
    dopo: str


# Il repository dell'integrazione domani si chiama VMC-HELTY-FLOW-MASTER (il proprietario
# rinomina VMC-HELTY-FLOW-MARKETPLACE quando esce la versione nativa)
COMMENTI = (
    Commento(
        "(https://github.com/DanRobo76/VMC-HELTY-FLOW-MARKETPLACE)",
        "(https://github.com/DanRobo76/VMC-HELTY-FLOW-MASTER)",
    ),
)
_CORNICE = re.compile(r"( +)#")

# Il ramo del modello di «Pulisci cronologia» per le entità escluse dal Recorder: le sue
# prime tre righe (intere); poi la riga che lo chiude e quella che chiude il «se».
RAMO_ESCLUSE = (
    (
        "{%- set escluse = state_attr('input_select.vmc_master_entita_escluse_recorder',"
        " 'options') -%}"
    ),
    "{%- set registrate = elenco | reject('in', escluse or []) | list -%}",
    "{%- if escluse is not none -%}",
)
_ALTRIMENTI = "{%- else -%}"
_FINE_SE = "{%- endif -%}"


DOMINI_DI_OGGI = frozenset(
    {
        "automation",
        "binary_sensor",
        "input_boolean",
        "input_datetime",
        "input_number",
        "input_select",
        "input_text",
        "script",
        "sensor",
        COMANDO,
        "timer",
    }
)
# Un nome «dominio.oggetto» (anche solo l'inizio dell'oggetto) dentro un testo.
_NOME = re.compile(r"(?<![A-Za-z0-9_.])([a-z_]+)\.([a-z0-9_]*)")
_VOCE_ELENCO = re.compile(
    r"^(?P<rientro>[ ]*)'(?P<nome>[a-z_]+\.[a-z0-9_]+)'(?P<virgola>,?)$"
)


class NonTraducibile(Exception):
    """Un pezzo della scheda che il traduttore non sa tradurre."""


# ----------------------------------------------------------------------------- mappa
def _leggi_csv(percorso: Path) -> list[dict[str, str]]:
    with percorso.open(encoding="utf-8-sig", newline="") as flusso:
        return list(csv.DictReader(flusso, delimiter=";"))


TOLTA = "tolta"
"""Una voce che domani non c'è più (b46: il campo «Cambia IP VMC» e chi lo serve)."""


def mappa_fase_1() -> dict[str, str | None]:
    """Entità di oggi -> entità di domani (``None``: domani non è un'entità, interna o
    tolta).

    Aiutanti, script e comandi di shell dalla colonna «Domani» di ``aiutanti_fase1.csv``;
    sensori, sensori binari e automazioni dalla tabella di traduzione della scheda della
    fase 1 (``traduzione_scheda.csv``, colonna «Diventa»). Dove ci sono tutte e due devono
    dire la stessa cosa.
    """
    mappa: dict[str, str | None] = {}
    for riga in _leggi_csv(FASE_1):
        domani = riga["Domani"]
        interna = domani.startswith("interna") or domani == TOLTA
        mappa[riga["Entità oggi"]] = None if interna else domani
    for riga in _leggi_csv(TRADUZIONE_FASE_1):
        oggi, diventa = riga["Entità nella scheda oggi"], riga["Diventa"]
        domani = None if "(tolta dalla scheda)" in diventa else diventa
        if oggi in mappa and mappa[oggi] != domani:
            raise NonTraducibile(f"{oggi}: le due tabelle della fase 1 non coincidono")
        mappa[oggi] = domani
    return mappa


def tolte_fase_1() -> frozenset[str]:
    """Le voci di oggi tolte (b46): «tolta» nella colonna «Domani» di ``aiutanti_fase1.csv``
    o nella colonna «Diventa» di ``traduzione_scheda.csv``."""
    tolte = {r["Entità oggi"] for r in _leggi_csv(FASE_1) if r["Domani"] == TOLTA}
    tolte |= {
        r["Entità nella scheda oggi"]
        for r in _leggi_csv(TRADUZIONE_FASE_1)
        if r["Diventa"].startswith(f"{TOLTA} ")
    }
    return frozenset(tolte)


@dataclass
class Mappa:
    """Nomi di oggi -> nomi di domani; ``tolte``: le voci tolte (le loro righe escono)."""

    entita: dict[str, str | None]
    tolte: frozenset[str] = frozenset()

    def frammento(self, nome: str) -> str:
        """Il pezzo di nome ``nome`` (inizio di più entità) con il dominio di domani (le
        voci tolte non contano: domani non ci sono)."""
        _dominio, oggetto = nome.split(".", 1)
        domani = set()
        for vecchia, nuova in self.entita.items():
            if not vecchia.startswith(nome) or vecchia in self.tolte:
                continue
            if nuova is None or nuova.split(".", 1)[1] != vecchia.split(".", 1)[1]:
                raise NonTraducibile(
                    f"{nome!r}: {vecchia} domani non ha lo stesso oggetto"
                )
            domani.add(nuova.split(".", 1)[0])
        if len(domani) != 1:
            raise NonTraducibile(
                f"{nome!r}: inizio di entità di domini {sorted(domani)}"
            )
        return f"{domani.pop()}.{oggetto}"


# ------------------------------------------------------------------------ traduzione
@dataclass(frozen=True)
class Modifica:
    """Una modifica della scheda (riga e colonna nella scheda master, da 1)."""

    riga: int
    colonna: int
    tipo: str
    posto: str
    prima: str
    dopo: str


@dataclass
class Traduzione:
    """La scheda tradotta e l'elenco delle modifiche."""

    testo: str
    modifiche: list[Modifica]

    def totali(self) -> Counter[tuple[str, str]]:
        """Numero di modifiche per tipo e per «cosa» (domini, servizio...)."""
        return Counter((m.tipo, _cosa(m)) for m in self.modifiche)


def _cosa(m: Modifica) -> str:
    if m.tipo in ("nome", "frammento", "elenco"):
        dopo = m.dopo.split(".", 1)[0] if m.dopo else "(tolta)"
        return f"{m.prima.split('.', 1)[0]} -> {dopo} [{m.posto}]"
    if m.tipo in ("servizio", "comando"):
        return (
            f"{m.prima.split('.', 1)[0]} -> {PREMI if m.tipo == 'comando' else m.dopo}"
        )
    if m.tipo == "condizione timer":
        return m.prima
    return m.posto


@dataclass(order=True)
class _Taglio:
    """Un pezzo del testo da sostituire: [inizio, fine) -> nuovo."""

    inizio: int
    fine: int
    nuovo: str = field(compare=False)
    modifiche: list[tuple[int, str, str, str, str]] = field(
        compare=False, default_factory=list
    )


class _Traduttore:
    def __init__(
        self,
        testo: str,
        mappa: Mappa,
        testi: tuple[Testo, ...],
        commenti: tuple[Commento, ...] = (),
    ) -> None:
        self.testo = testo
        self.mappa = mappa
        self.testi = testi
        self.commenti = commenti
        self._modelli = [modello_testo(t.prima) for t in testi]
        # quante volte è stato trovato ogni testo di ``testi``
        self.trovati: Counter[int] = Counter()
        self.a_capo = "\r\n" if "\r\n" in testo else "\n"
        self.tagli: list[_Taglio] = []
        # pezzi di testo coperti da un taglio: lì i nomi li cambia il taglio
        self.coperti: list[tuple[int, int]] = []
        # le voci dell'elenco di «Pulisci cronologia»
        self.elenco = (0, 0)
        # le mappe che contengono il nodo che si sta visitando, dalla radice
        self._antenati: list[yaml.MappingNode] = []
        self._inizi_riga = [0] + [i + 1 for i, c in enumerate(testo) if c == "\n"]

    # -------------------------------------------------------------- aiuti
    def _taglio(self, inizio: int, fine: int, nuovo: str, *modifiche) -> None:
        self.tagli.append(_Taglio(inizio, fine, nuovo, list(modifiche)))
        self.coperti.append((inizio, fine))

    def _coperto(self, inizio: int, fine: int) -> bool:
        return any(a <= inizio and fine <= b for a, b in self.coperti)

    def _riga_colonna(self, indice: int) -> tuple[int, int]:
        riga = bisect.bisect_right(self._inizi_riga, indice)
        return riga, indice - self._inizi_riga[riga - 1] + 1

    def _domani(self, nome: str) -> str | None:
        if nome not in self.mappa.entita:
            raise NonTraducibile(f"{nome}: non è nella mappa della fase 1")
        return self.mappa.entita[nome]

    # -------------------------------------------------------------- visita
    def traduci(self) -> Traduzione:
        radice = yaml.compose(self.testo)
        self._intestazione(radice.start_mark.index)
        self._visita(radice, None, None)
        for i, testo in enumerate(self.testi):
            if self.trovati[i] != testo.volte:
                raise NonTraducibile(
                    f"testo {testo.prima!r}: trovato {self.trovati[i]} volte invece di"
                    f" {testo.volte}"
                )
        self._nomi(radice, None, None)
        return self._applica()

    def _visita(
        self, nodo: yaml.Node, chiave: str | None, padre: yaml.MappingNode | None
    ) -> None:
        """Prima passata: le modifiche di struttura (servizi, timer, elenco, tipi)."""
        if isinstance(nodo, yaml.MappingNode):
            coppie = {
                k.value: (k, v) for k, v in nodo.value if isinstance(k, yaml.ScalarNode)
            }
            self._azione(coppie)
            self._timer(coppie)
            self._antenati.append(nodo)
            for k, v in nodo.value:
                self._visita(
                    v, k.value if isinstance(k, yaml.ScalarNode) else None, nodo
                )
            self._antenati.pop()
        elif isinstance(nodo, yaml.SequenceNode):
            for i, v in enumerate(nodo.value):
                if (tolta := self._riga_tolta(v)) is not None:
                    self._togli_riga(nodo, i, *tolta)
                else:
                    self._visita(v, chiave, padre)
        elif isinstance(nodo, yaml.ScalarNode) and isinstance(nodo.value, str):
            self._testi(nodo, _posto(chiave, padre))
            if _INIZIO_ELENCO in nodo.value:
                self._elenco(nodo)
                self._esclusioni(nodo, _posto(chiave, padre))
            if _INIZIO_TIPI in nodo.value:
                self._tipi(nodo)

    def _riga_tolta(self, nodo: yaml.Node) -> tuple[str, str] | None:
        """(posto, voce tolta) se ``nodo`` è la riga di una voce tolta o una riga
        ``conditional`` con una condizione su una voce tolta."""
        if not isinstance(nodo, yaml.MappingNode):
            return None
        coppie = {k.value: v for k, v in nodo.value if isinstance(k, yaml.ScalarNode)}
        entita = coppie.get("entity")
        if isinstance(entita, yaml.ScalarNode) and entita.value in self.mappa.tolte:
            return "riga", entita.value
        tipo, condizioni = coppie.get("type"), coppie.get("conditions")
        if (
            isinstance(tipo, yaml.ScalarNode)
            and tipo.value == "conditional"
            and isinstance(condizioni, yaml.SequenceNode)
        ):
            for condizione in condizioni.value:
                tolta = self._riga_tolta(condizione)
                if tolta is not None:
                    return "riga condizionale", tolta[1]
        return None

    def _togli_riga(self, elenco: yaml.SequenceNode, i: int, posto: str, voce: str) -> None:
        """Toglie la voce ``i`` di ``elenco``: dall'inizio della sua riga («- ») all'inizio
        della riga della voce che segue (mai l'ultima: niente da indovinare dopo)."""
        nodo = elenco.value[i]
        inizio = self.testo.rfind("\n", 0, nodo.start_mark.index) + 1
        if self.testo[inizio : nodo.start_mark.index].strip() != "-":
            raise NonTraducibile(f"riga {nodo.start_mark.line + 1}: riga tolta non in un elenco")
        if i + 1 == len(elenco.value):
            raise NonTraducibile(f"riga {nodo.start_mark.line + 1}: riga tolta in fondo")
        seguente = elenco.value[i + 1].start_mark.index
        fine = self.testo.rfind("\n", 0, seguente) + 1
        if self.testo[fine:seguente].strip() != "-":
            raise NonTraducibile(f"riga {nodo.start_mark.line + 1}: riga dopo non prevista")
        self._taglio(inizio, fine, "", (inizio, "riga tolta", posto, voce, ""))

    def _azione(self, coppie: dict[str, tuple[yaml.Node, yaml.Node]]) -> None:
        if "perform_action" not in coppie:
            return
        if "service" in coppie:
            raise NonTraducibile("azione con «service» e «perform_action»")
        k, v = coppie["perform_action"]
        servizio = v.value
        dominio = servizio.split(".", 1)[0]
        if dominio not in DOMINI_DI_OGGI:
            return
        inizio, fine = v.start_mark.index, v.end_mark.index
        if self.testo[inizio:fine] != servizio:
            raise NonTraducibile(
                f"riga {v.start_mark.line + 1}: servizio non scritto semplice"
            )
        if servizio in SERVIZI:
            nuovo = SERVIZI[servizio]
            bersagli = self._bersagli(coppie)
            dominio_nuovo = nuovo.split(".", 1)[0]
            if not bersagli or any(
                (self._domani(b) or "").split(".", 1)[0] != dominio_nuovo
                for b in bersagli
            ):
                raise NonTraducibile(
                    f"{servizio}: bersagli {bersagli} non tutti {dominio_nuovo}"
                )
            self._taglio(
                inizio,
                fine,
                nuovo,
                (inizio, "servizio", "perform_action", servizio, nuovo),
            )
            return
        if dominio != COMANDO:
            raise NonTraducibile(f"servizio {servizio} senza traduzione")
        pulsante = self._domani(servizio)
        if pulsante is None or not pulsante.startswith("button."):
            raise NonTraducibile(f"{servizio}: domani non è un pulsante ({pulsante})")
        rientro = " " * k.start_mark.column
        bersaglio = f"target:{self.a_capo}{rientro}  entity_id: {pulsante}"
        modifica = (
            inizio,
            "comando",
            "perform_action",
            servizio,
            f"{PREMI} -> {pulsante}",
        )
        if "target" in coppie:
            kt, vt = coppie["target"]
            if (
                not isinstance(vt, yaml.MappingNode)
                or vt.value
                or kt.start_mark.column != k.start_mark.column
            ):
                raise NonTraducibile(f"{servizio}: bersaglio non vuoto")
            self._taglio(inizio, fine, PREMI, modifica)
            self._taglio(kt.start_mark.index, vt.end_mark.index, bersaglio)
        else:
            self._taglio(
                inizio, fine, f"{PREMI}{self.a_capo}{rientro}{bersaglio}", modifica
            )

    def _bersagli(self, coppie: dict[str, tuple[yaml.Node, yaml.Node]]) -> list[str]:
        bersagli: list[str] = []
        for chiave in ("target", "data"):
            if chiave not in coppie:
                continue
            _k, v = coppie[chiave]
            if not isinstance(v, yaml.MappingNode):
                raise NonTraducibile(f"{chiave} non è una mappa")
            for kk, vv in v.value:
                if kk.value != "entity_id":
                    raise NonTraducibile(f"{chiave}.{kk.value}: dato non previsto")
                valori = vv.value if isinstance(vv, yaml.SequenceNode) else [vv]
                bersagli += [x.value for x in valori]
        return bersagli

    def _timer(self, coppie: dict[str, tuple[yaml.Node, yaml.Node]]) -> None:
        if "entity" not in coppie:
            return
        k, v = coppie["entity"]
        if not (isinstance(v, yaml.ScalarNode) and str(v.value).startswith("timer.")):
            return
        sensore = self._domani(v.value)
        if sensore is None or not sensore.startswith("sensor."):
            raise NonTraducibile(f"{v.value}: domani non è un sensore ({sensore})")
        if "state" in coppie or "state_not" in coppie or "condition" in coppie:
            if (
                set(coppie) != {"condition", "entity", "state"}
                or coppie["condition"][1].value != "state"
            ):
                raise NonTraducibile(
                    f"riga {k.start_mark.line + 1}: condizione del timer non prevista"
                )
            ks, vs = coppie["state"]
            stato = vs.value
            if stato not in CONTO_ALLA_ROVESCIA:
                raise NonTraducibile(
                    f"riga {k.start_mark.line + 1}: stato del timer {stato!r}"
                )
            prima = self.testo[ks.start_mark.index : vs.end_mark.index]
            nuovo = CONTO_ALLA_ROVESCIA[stato]
            self._taglio(
                ks.start_mark.index,
                vs.end_mark.index,
                nuovo,
                (ks.start_mark.index, "condizione timer", "condizione", prima, nuovo),
            )
            return
        if (
            "type" in coppie
            or v.style is not None
            or self.testo[v.start_mark.index : v.end_mark.index] != v.value
        ):
            raise NonTraducibile(
                f"riga {k.start_mark.line + 1}: riga del timer non prevista"
            )
        if "color" in coppie or "state_color" in coppie:
            raise NonTraducibile(
                f"riga {k.start_mark.line + 1}: riga del timer con colore"
            )
        colore = self._colore_della_scheda(k.start_mark.line + 1)
        rientro = " " * k.start_mark.column
        aggiunta = f"{self.a_capo}{rientro}type: {RIGA_CONTO}{self.a_capo}{rientro}color: {colore}"
        # le righe «type:» e «color:» vanno subito dopo «entity:»; il nome lo cambia la
        # seconda passata
        fine = v.end_mark.index
        self.tagli.append(
            _Taglio(
                fine,
                fine,
                aggiunta,
                [
                    (
                        k.start_mark.index,
                        "riga conto alla rovescia",
                        "riga",
                        v.value,
                        sensore,
                    ),
                    (
                        k.start_mark.index,
                        "colore riga conto alla rovescia",
                        "riga",
                        "",
                        f"color: {colore}",
                    ),
                ],
            )
        )

    def _colore_della_scheda(self, riga: int) -> str:
        """Il colore che la scheda entities che contiene la riga dà alle righe senza tipo
        (frontend 20261028: ``{color: "state", ...config}``, ``state_color: false`` diventa
        ``none``). Alle righe con un tipo ``custom:`` il frontend non lo passa: la riga
        tradotta lo deve avere scritto per restare uguale."""
        for antenato in reversed(self._antenati):
            coppie = {
                k.value: v for k, v in antenato.value if isinstance(k, yaml.ScalarNode)
            }
            tipo = coppie.get("type")
            if isinstance(tipo, yaml.ScalarNode) and tipo.value == "entities":
                if "color" in coppie:
                    return coppie["color"].value
                stato = coppie.get("state_color")
                if stato is not None and stato.value.lower() == "false":
                    return "none"
                return "state"
            if "color" in coppie or "state_color" in coppie:
                raise NonTraducibile(
                    f"riga {riga}: colore fra la scheda e la riga del timer"
                )
        raise NonTraducibile(
            f"riga {riga}: riga del timer fuori da una scheda entities"
        )

    def _elenco(self, nodo: yaml.ScalarNode) -> None:
        inizio = self.testo.index(
            _INIZIO_ELENCO, nodo.start_mark.index, nodo.end_mark.index
        )
        fine = self.testo.index(_FINE_ELENCO, inizio, nodo.end_mark.index)
        self.elenco = (inizio, fine)
        righe = self.testo[inizio:fine].split(self.a_capo)[1:-1]
        posizione = (
            inizio
            + len(self.testo[inizio:fine].split(self.a_capo)[0])
            + len(self.a_capo)
        )
        tenute: list[re.Match[str]] = []
        for riga in righe:
            trovata = _VOCE_ELENCO.match(riga)
            if trovata is None:
                raise NonTraducibile(f"voce dell'elenco non prevista: {riga!r}")
            nome = trovata["nome"]
            domani = self._domani(nome)
            lunghezza = len(riga) + len(self.a_capo)
            if domani is None:
                self._taglio(
                    posizione,
                    posizione + lunghezza,
                    "",
                    (posizione, "elenco", "elenco", nome, ""),
                )
            else:
                tenute.append(trovata)
            posizione += lunghezza
        if not tenute or tenute[-1]["virgola"] or righe[-1] != tenute[-1].string:
            raise NonTraducibile("l'ultima voce dell'elenco esce o ha la virgola")

    def _righe(self, inizio: int, fine: int) -> list[tuple[int, str]]:
        """Le righe che cominciano in [inizio, fine): (inizio della riga, riga senza a capo)."""
        primo = bisect.bisect_left(self._inizi_riga, inizio)
        righe = []
        for a in self._inizi_riga[primo:]:
            if a >= fine:
                break
            b = self.testo.find("\n", a)
            righe.append(
                (a, self.testo[a : len(self.testo) if b < 0 else b].rstrip("\r"))
            )
        return righe

    def _esclusioni(self, nodo: yaml.ScalarNode, posto: str) -> None:
        """Dal modello di «Pulisci cronologia» esce il ramo per le entità escluse dal
        Recorder: le righe da ``RAMO_ESCLUSE`` a ``{%- else -%}`` e la riga
        ``{%- endif -%}`` che chiude il modello. Resta il ramo che la scheda mostra quando
        il sensore delle entità escluse non ha l'attributo ``options``: tutte le entità,
        con il loro numero (stesso testo, carattere per carattere, grazie ai ``-`` di
        ``{%-`` e ``-%}``)."""
        righe = self._righe(nodo.start_mark.index, nodo.end_mark.index)
        testi = [r.strip() for _a, r in righe]
        if testi.count(RAMO_ESCLUSE[0]) != 1:
            raise NonTraducibile("ramo delle entità escluse dal Recorder non trovato")
        primo = testi.index(RAMO_ESCLUSE[0])
        if tuple(testi[primo : primo + len(RAMO_ESCLUSE)]) != RAMO_ESCLUSE:
            raise NonTraducibile("ramo delle entità escluse dal Recorder non previsto")
        if testi.count(_ALTRIMENTI) != 1 or testi.count(_FINE_SE) != 1:
            raise NonTraducibile(
                "ramo delle entità escluse: «else» o «endif» non unici"
            )
        altrimenti, fine_se = testi.index(_ALTRIMENTI), testi.index(_FINE_SE)
        if not primo < altrimenti < fine_se:
            raise NonTraducibile("ramo delle entità escluse: righe fuori ordine")
        a_fine_se, riga_fine_se = righe[fine_se]
        fine_testo = a_fine_se + len(riga_fine_se)
        if self.testo[fine_testo : nodo.end_mark.index].strip():
            raise NonTraducibile("ramo delle entità escluse: «endif» non alla fine")
        tolte = righe[primo : altrimenti + 1]
        self._taglio(
            tolte[0][0],
            righe[altrimenti + 1][0],
            "",
            *((a, "esclusioni", posto, r.strip(), "") for a, r in tolte),
        )
        # la riga «{%- endif -%}» con l'a capo che la precede
        self._taglio(
            a_fine_se - len(self.a_capo),
            fine_testo,
            "",
            (a_fine_se, "esclusioni", posto, _FINE_SE, ""),
        )

    def _intestazione(self, fine: int) -> None:
        """I testi di ``commenti`` nelle righe di commento prima della scheda (fino a
        ``fine``): ognuno una volta, su una riga della cornice di «#» che resta lunga
        uguale."""
        for commento in self.commenti:
            posti = [
                m.start()
                for m in re.finditer(re.escape(commento.prima), self.testo[:fine])
            ]
            if len(posti) != 1:
                raise NonTraducibile(
                    f"commento {commento.prima!r}: trovato {len(posti)} volte invece di 1"
                )
            a = posti[0]
            inizio_riga = self.testo.rfind("\n", 0, a) + 1
            riga = self.testo[inizio_riga : self.testo.find("\n", a)].rstrip("\r")
            prima_del_testo = riga[: a - inizio_riga]
            cornice = _CORNICE.fullmatch(riga, a - inizio_riga + len(commento.prima))
            spazi = (
                len(cornice[1]) + len(commento.prima) - len(commento.dopo)
                if cornice
                else 0
            )
            if not prima_del_testo.startswith("#") or spazi < 1:
                raise NonTraducibile(
                    f"commento {commento.prima!r}: non su una riga della cornice"
                )
            self._taglio(
                inizio_riga,
                inizio_riga + len(riga),
                f"{prima_del_testo}{commento.dopo}{' ' * spazi}#",
                (a, "intestazione", "commento", commento.prima, commento.dopo),
            )

    def _tipi(self, nodo: yaml.ScalarNode) -> None:
        inizio = self.testo.index(
            _INIZIO_TIPI, nodo.start_mark.index, nodo.end_mark.index
        )
        fine = self.testo.index("}", inizio + len(_INIZIO_TIPI))
        for oggi, domani in CHIAVI_TIPI.items():
            chiave = f"'{oggi}':"
            if self.testo.count(chiave, inizio, fine) != 1:
                raise NonTraducibile(f"tipi: chiave {chiave} non trovata una volta")
            posto = self.testo.index(chiave, inizio, fine)
            nuovo = f"'{domani}':"
            self._taglio(
                posto,
                posto + len(chiave),
                nuovo,
                (posto, "chiave tipi", "modello tipi", oggi, domani),
            )

    def _testi(self, nodo: yaml.ScalarNode, posto: str) -> None:
        """I testi di ``TESTI`` dentro questo testo della scheda."""
        for i, (testo, modello) in enumerate(
            zip(self.testi, self._modelli, strict=True)
        ):
            for trovato in modello.finditer(
                self.testo, nodo.start_mark.index, nodo.end_mark.index
            ):
                a, b = trovato.span()
                self.trovati[i] += 1
                fine, nuovo = self._testo_nuovo(nodo, a, b, testo.dopo)
                self.tagli.append(
                    _Taglio(
                        a, fine, nuovo, [(a, "testo", posto, testo.prima, testo.dopo)]
                    )
                )

    def _testo_nuovo(
        self, nodo: yaml.ScalarNode, a: int, b: int, dopo: str
    ) -> tuple[int, str]:
        """Dove finisce il pezzo da sostituire (da ``a``) e il testo nuovo come va scritto
        nel file al suo posto.

        Su una riga sola il pezzo è [a, b) e il testo nuovo resta su una riga. Su più righe
        si può solo in un testo ripiegato (``>``) e su righe con il rientro del testo: lì un
        a capo vale uno spazio, così il testo nuovo, con il resto della sua ultima riga, va
        a capo con lo stesso rientro senza superare la riga più lunga di prima (le righe più
        rientrate, invece, tengono i loro a capo)."""
        riga = self._riga_colonna(a)[0]
        if nodo.style == "'" or (nodo.style == '"' and ('"' in dopo or "\\" in dopo)):
            raise NonTraducibile(f"riga {riga}: testo nuovo da scrivere con escape")
        if "\n" not in self.testo[a:b]:
            return b, dopo
        if nodo.style != ">":
            raise NonTraducibile(f"riga {riga}: testo su più righe fuori da un «>»")
        inizio_riga = self.testo.rfind("\n", 0, a) + 1
        fine_riga = self.testo.find("\n", b)
        righe = [r.rstrip("\r") for r in self.testo[inizio_riga:fine_riga].split("\n")]
        # le righe vuote (fra due capoversi) non hanno rientro
        rientri = {len(r) - len(r.lstrip(" ")) for r in righe if r.strip()}
        if rientri != {_rientro_del_blocco(self.testo, nodo)}:
            raise NonTraducibile(f"riga {riga}: testo su righe più rientrate")
        rientro = rientri.pop()
        larghezza = max(len(r) for r in righe)
        # il resto dell'ultima riga va a capo con il testo nuovo, se ha solo spazi singoli
        resto = self.testo[b:fine_riga].rstrip("\r")
        if "  " in resto or "\t" in resto or resto.endswith(" "):
            fine_taglio, resto = b, ""
        else:
            fine_taglio = b + len(resto)
        nuove: list[str] = []
        corrente, lunghezza = "", a - inizio_riga
        for parola in (dopo + resto).split(" "):
            if corrente and lunghezza + 1 + len(parola) > larghezza:
                nuove.append(corrente)
                corrente, lunghezza = parola, rientro + len(parola)
            else:
                lunghezza += len(parola) + (1 if corrente else 0)
                corrente = f"{corrente} {parola}" if corrente else parola
        return fine_taglio, f"{self.a_capo}{' ' * rientro}".join([*nuove, corrente])

    # -------------------------------------------------------------- nomi
    def _nomi(
        self, nodo: yaml.Node, chiave: str | None, padre: yaml.MappingNode | None
    ) -> None:
        """Seconda passata: i nomi dentro ogni testo (chiavi e valori)."""
        if isinstance(nodo, yaml.MappingNode):
            for k, v in nodo.value:
                self._nomi(k, None, nodo)
                self._nomi(v, k.value if isinstance(k, yaml.ScalarNode) else None, nodo)
        elif isinstance(nodo, yaml.SequenceNode):
            for v in nodo.value:
                self._nomi(v, f"{chiave}[]" if chiave else None, padre)
        elif isinstance(nodo, yaml.ScalarNode):
            self._nomi_testo(nodo, _posto(chiave, padre))

    def _nomi_testo(self, nodo: yaml.ScalarNode, posto: str) -> None:
        inizio, fine = nodo.start_mark.index, nodo.end_mark.index
        for trovato in _NOME.finditer(self.testo, inizio, fine):
            nome, dominio = trovato.group(0), trovato.group(1)
            if dominio not in DOMINI_DI_OGGI:
                continue
            a, b = trovato.span()
            if self._coperto(a, b):
                continue
            if nome in SERVIZI or dominio == COMANDO:
                raise NonTraducibile(
                    f"riga {self._riga_colonna(a)[0]}: servizio {nome} fuori da un'azione"
                )
            if nome in self.mappa.entita:
                nuovo = self.mappa.entita[nome]
                if nuovo is None:
                    raise NonTraducibile(
                        f"riga {self._riga_colonna(a)[0]}: {nome} interna fuori dall'elenco"
                    )
                tipo = "nome"
            else:
                nuovo = self.mappa.frammento(nome)
                tipo = "frammento"
            if nuovo != nome:
                dove = "elenco" if self.elenco[0] <= a < self.elenco[1] else posto
                self.tagli.append(_Taglio(a, b, nuovo, [(a, tipo, dove, nome, nuovo)]))

    # -------------------------------------------------------------- uscita
    def _applica(self) -> Traduzione:
        tagli = sorted(self.tagli)
        pezzi: list[str] = []
        modifiche: list[Modifica] = []
        dove = 0
        for taglio in tagli:
            if taglio.inizio < dove:
                raise NonTraducibile(
                    f"tagli sovrapposti a {self._riga_colonna(taglio.inizio)}"
                )
            pezzi.append(self.testo[dove : taglio.inizio])
            pezzi.append(taglio.nuovo)
            dove = taglio.fine
            for indice, tipo, posto, prima, dopo in taglio.modifiche:
                riga, colonna = self._riga_colonna(indice)
                modifiche.append(Modifica(riga, colonna, tipo, posto, prima, dopo))
        pezzi.append(self.testo[dove:])
        modifiche.sort(key=lambda m: (m.riga, m.colonna, m.tipo))
        return Traduzione("".join(pezzi), modifiche)


def _rientro_del_blocco(testo: str, nodo: yaml.ScalarNode) -> int:
    """Il rientro di un testo a blocco (``>`` o ``|``): quello della sua prima riga non
    vuota."""
    for riga in testo[nodo.start_mark.index : nodo.end_mark.index].split("\n")[1:]:
        if riga.strip():
            return len(riga) - len(riga.lstrip(" "))
    raise NonTraducibile(f"riga {nodo.start_mark.line + 1}: testo a blocco vuoto")


def _posto(chiave: str | None, padre: yaml.MappingNode | None) -> str:
    """Dove sta un testo, per contare le modifiche: chiave YAML e, per «entity», se è
    una condizione."""
    if chiave is None:
        return "chiave"
    if chiave == "entity" and padre is not None:
        chiavi = {k.value for k, _v in padre.value if isinstance(k, yaml.ScalarNode)}
        if chiavi & {"state", "state_not", "condition"}:
            return "condizione"
        return "entity"
    if chiave == "content":
        return "modello markdown"
    return chiave


def scheda_master() -> str:
    """La scheda della VMC Master come la serve l'integrazione, prima del nome e dell'IP:
    senza le sezioni Clona VMC e Installa VMC (CRLF come nel file)."""
    with SCHEDA.open(encoding="utf-8", newline="") as flusso:
        return rimuovi_sezioni_solo_master(flusso.read())


def traduci(
    testo: str | None = None,
    mappa: Mappa | None = None,
    testi: tuple[Testo, ...] = TESTI,
    commenti: tuple[Commento, ...] = COMMENTI,
) -> Traduzione:
    """La scheda master tradotta ai nomi delle entità native (con ``testi=()`` senza
    aggiornare i testi, con ``commenti=()`` senza toccare l'intestazione)."""
    return _Traduttore(
        scheda_master() if testo is None else testo,
        mappa or Mappa(mappa_fase_1(), tolte_fase_1()),
        testi,
        commenti,
    ).traduci()


# ---------------------------------------------------------------- file generati
def testo_modifiche(traduzione: Traduzione) -> str:
    """Le modifiche, una per riga (CSV con «;»)."""
    flusso = io.StringIO()
    scrittore = csv.writer(flusso, delimiter=";", lineterminator="\n")
    scrittore.writerow(["riga", "colonna", "tipo", "posto", "prima", "dopo"])
    scrittore.writerows(
        (m.riga, m.colonna, m.tipo, m.posto, m.prima, m.dopo)
        for m in traduzione.modifiche
    )
    return flusso.getvalue()


def testo_totali(traduzione: Traduzione) -> str:
    """I totali delle modifiche per tipo, con il dettaglio."""
    per_tipo = Counter(m.tipo for m in traduzione.modifiche)
    righe = [
        "SCHEDA «VMC MASTER» TRADOTTA AI NOMI DELLE ENTITÀ NATIVE (fase 4) - totali delle modifiche",
        "",
        (
            f"Righe della scheda master: {traduzione_righe(scheda_master())} -> "
            f"{traduzione_righe(traduzione.testo)}"
        ),
        f"Modifiche: {len(traduzione.modifiche)}",
        "",
    ]
    totali = traduzione.totali()
    for tipo, quante in sorted(per_tipo.items(), key=lambda x: (-x[1], x[0])):
        righe.append(f"{quante:6d}  {tipo}")
        dettaglio = sorted(
            ((cosa, n) for (t, cosa), n in totali.items() if t == tipo),
            key=lambda x: (-x[1], x[0]),
        )
        righe += [f"        {n:6d}  {cosa}" for cosa, n in dettaglio]
    return "\n".join(righe) + "\n"


def traduzione_righe(testo: str) -> int:
    """Numero di righe di un testo."""
    return testo.count("\n") + (0 if testo.endswith("\n") else 1)


def file_generati(traduzione: Traduzione) -> Iterator[tuple[Path, str]]:
    """I file scritti dal traduttore: la scheda tradotta, le modifiche e i totali."""
    yield USCITA, traduzione.testo
    yield MODIFICHE, testo_modifiche(traduzione)
    yield TOTALI, testo_totali(traduzione)
