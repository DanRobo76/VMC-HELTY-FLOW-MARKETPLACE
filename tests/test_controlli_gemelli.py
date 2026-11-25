"""Controlli automatici dei rami «gemelli» (classi d5 e d7/d8), portati dagli script del controllo statico del
21-11-2026 (zone-non-verificate-21-11-2026/controlli/gemelli: comune.py, percorsi.py, gemelli_velocita.py,
gemelli_allerte.py e rapporto.md, con le eccezioni che quel controllo ha già giudicato volute).

Classe d5 - rami gemelli per velocità, giorno, fascia e Free Heating/Cooling: ogni blocco ripetuto (trigger, ramo
d'azione, opzioni gemelle di un choose, script Fascia 1/Fascia 2) viene diviso in pezzi (condizione per condizione,
passo per passo) con il nome proprio sostituito da ⟨V⟩ e quello delle altre copie da ⟨A⟩; i pezzi che non sono
uguali in tutte le copie sono le differenze. Classe A = la differenza sta solo nelle copie «speciali» V0, V1 o Free
(velocità con logica propria nel Foglio); classe B = copie normali o famiglie di 2 (ogni differenza va guardata).

Classe d7/d8 - rami gemelli tra allerte: fine Congelamento contro fine Δ Temp. pezzo per pezzo, protezioni sul cammino
dei comandi alla VMC nei rami di fine allerta e marcatori «(correzione Ox)».

I numeri sono conteggi esatti misurati sul package. Una nuova differenza fa fallire la prova: si corregge oppure si
accetta a mano, con il motivo, aggiornando la tabella (il messaggio dell'errore stampa i conteggi misurati).
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Any

import yaml

from tests.test_b35_allerte import _testo

AUT = "vmc_master_automazione.txt"
YML = "vmc_master.yaml"
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
IGNORA = {"alias", "description", "id", "metadata"}  # testi e identificativi: non cambiano il comportamento


# ------------------------------------------------------------------------------------------------ lettura (comune.py)
class Fonte:
    """Un file del package: righe e albero dei nodi YAML con la loro riga (yaml.compose)."""

    def __init__(self, nome: str) -> None:
        self.nome = nome
        testo = _testo(nome)
        self.righe = testo.split("\n")
        self.radice = yaml.compose(testo, Loader=LOADER)

    def dove(self, riga_: int) -> str:
        return f"{self.nome}:{riga_}"


@lru_cache
def _fonti() -> tuple[Fonte, Fonte]:
    return Fonte(AUT), Fonte(YML)


def mappa(n: Any) -> dict[str, Any]:
    return {k.value: v for k, v in n.value} if isinstance(n, yaml.MappingNode) else {}


def lista(n: Any) -> list[Any]:
    return n.value if isinstance(n, yaml.SequenceNode) else []


def riga(n: Any) -> int:
    return n.start_mark.line + 1


def fine(n: Any) -> int:
    e = n.end_mark
    return e.line if e.column == 0 else e.line + 1


def scalari(n: Any):
    if isinstance(n, yaml.MappingNode):
        for _, v in n.value:
            yield from scalari(v)
    elif isinstance(n, yaml.SequenceNode):
        for x in n.value:
            yield from scalari(x)
    else:
        yield n


_SPAZI_OP = re.compile(r"\s*(==|!=|<=|>=|\(|\)|\[|\]|,|\|)\s*")
_IS_STATE = re.compile(r"is_state\(('[^']*'),('[^']*')\)")
_TAGLIO = re.compile(r"(?=\b(?:and|or)\b)|(?=\{%)|(?<=%\})|(?=\{\{)|(?<=\}\})")
_ENTITA = re.compile(r"[a-z_]+\.vmc_master_[a-z0-9_]+")


def norm_template(s: str) -> str:
    s = re.sub(r"\{#.*?#\}", " ", s, flags=re.S)
    s = s.replace("{%-", "{%").replace("-%}", "%}").replace("{{-", "{{").replace("-}}", "}}")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("\\'", "'")
    s = re.sub(r'"([^"\']*)"', r"'\1'", s)
    s = _SPAZI_OP.sub(r"\1", s)
    s = _IS_STATE.sub(r"states(\1)==\2", s)
    s = re.sub(r"\{\{\s*", "{{", s)
    s = re.sub(r"\s*\}\}", "}}", s)
    s = re.sub(r"\{%\s*", "{%", s)
    return re.sub(r"\s*%\}", "%}", s)


def _pulisci(p: str) -> str:
    m = re.match(r"^(and|or)\b\s*", p)
    op = m.group(1) if m else ""
    corpo = (p[m.end():] if m else p).strip()
    if corpo.startswith("{{"):
        corpo = corpo[2:]
    if corpo.endswith("}}"):
        corpo = corpo[:-2]
    corpo = corpo.lstrip("( ")
    while corpo.endswith(")") and corpo.count(")") > corpo.count("("):
        corpo = corpo[:-1].rstrip()
    while corpo.endswith("("):
        corpo = corpo[:-1].rstrip()
    return (op + " " + corpo).strip()


def pezzi(fonte: Fonte, n: Any) -> list[tuple[str, int]]:
    """Uno scalare diviso in pezzi confrontabili (condizioni separate da and/or e tag Jinja), con la riga di ognuno."""
    s = norm_template(str(n.value))
    parti = [p for p in (_pulisci(p) for p in _TAGLIO.split(s)) if p and p not in ("and", "or", "{{", "}}")]
    a, b = riga(n), max(riga(n), fine(n))
    puntatore, out = a, []
    for p in parti:
        m = _ENTITA.search(p)
        firma = m.group(0) if m else next(iter(re.findall(r"[A-Za-z_]{4,}", p)), None)
        if firma:
            for r in range(puntatore, b + 1):
                if firma in fonte.righe[r - 1]:
                    puntatore = r
                    break
        out.append((p, puntatore))
    return out


def linee(fonte: Fonte, nodo: Any) -> list[tuple[str, str, int]]:
    """Il blocco come elenco di (percorso delle chiavi, pezzo normalizzato, riga)."""
    out: list[tuple[str, str, int]] = []

    def visita(n: Any, percorso: str) -> None:
        if isinstance(n, yaml.MappingNode):
            for k, v in n.value:
                chiave = k.value
                if chiave in IGNORA or (isinstance(v, yaml.MappingNode) and not v.value):
                    continue
                if percorso.endswith("delay") and isinstance(v, yaml.ScalarNode) and v.value in ("0", "00"):
                    continue
                if chiave == "enabled" and isinstance(v, yaml.ScalarNode) and v.value.lower() == "true":
                    continue
                sotto = f"{percorso}/{chiave}" if percorso else chiave
                if isinstance(v, yaml.ScalarNode):
                    out.extend((sotto, p, r) for p, r in pezzi(fonte, v))
                else:
                    visita(v, sotto)
        elif isinstance(n, yaml.SequenceNode):
            for x in n.value:
                visita(x, percorso)
        else:
            out.extend((percorso, p, r) for p, r in pezzi(fonte, n))

    visita(nodo, "")
    return out


class Dimensione:
    """Un asse lungo il quale i blocchi gemelli cambiano (velocità, giorno, fascia, Free Heating/Cooling, allerta)."""

    def __init__(self, nome: str, chiavi: list[str], protezioni: list[tuple[str, str]], regole: list[str],
                 mappa_chiavi: dict[str, str], max_chiavi: int = 2) -> None:
        self.nome, self.chiavi, self.max_chiavi = nome, chiavi, max_chiavi
        self.protezioni = [(re.compile(r), s) for r, s in protezioni]
        self.regole = [re.compile(r, re.I) for r in regole]
        self.mappa = {k.lower(): v for k, v in mappa_chiavi.items()}

    def _protetto(self, t: str) -> tuple[str, dict[str, str]]:
        tenuti: dict[str, str] = {}
        for k, (rx, _) in enumerate(self.protezioni):
            def sost(m: re.Match, k: int = k) -> str:
                chiave = f"\x00{k}.{len(tenuti)}\x00"
                tenuti[chiave] = m.group(0)
                return chiave
            t = rx.sub(sost, t)
        return t, tenuti

    def trova(self, t: str) -> list[tuple[int, int, str]]:
        return self._trova(self._protetto(t)[0])

    def _trova(self, t: str) -> list[tuple[int, int, str]]:
        presi: list[tuple[int, int, str]] = []
        for rx in self.regole:
            for m in rx.finditer(t):
                chiave = self.mappa.get(m.group(1).lower())
                if chiave is None:
                    continue
                a, b = m.span(1)
                if any(not (b <= x or a >= y) for x, y, _ in presi):
                    continue
                presi.append((a, b, chiave))
        return sorted(presi)

    def normalizza(self, t: str, propria: str) -> tuple[str, Counter]:
        t2, tenuti = self._protetto(t)
        trovati = self._trova(t2)
        altre: Counter = Counter()
        if trovati and len({c for _, _, c in trovati}) <= self.max_chiavi:
            parti, ultimo = [], 0
            for a, b, c in trovati:
                parti.append(t2[ultimo:a])
                if c == propria:
                    parti.append("⟨V⟩")
                else:
                    parti.append("⟨A⟩")
                    altre[c] += 1
                ultimo = b
            parti.append(t2[ultimo:])
            t2 = "".join(parti)
        for chiave, originale in tenuti.items():
            t2 = t2.replace(chiave, originale)
        return t2, altre


VELOCITA = Dimensione(
    "velocità", ["0", "1", "2", "3", "4", "N", "I", "F"],
    protezioni=[(r"spia_velocita_1_co2_o_voc_pdr", "V1PDR"),
                (r"spia_velocita_freecooling_un_solo_avvio_per_programmazione_free(?:cooling|heating)", "FREEPROG"),
                (r"spia_co2_o_voc_partenza_ritorno_velocita_0", "PARTENZA0"),
                (r"spia_umidita_mantenuta_velocita_0", "U0MANT"),
                (r"notifica_velocita_(?:0|diversa_da_0)", "NOTIFICA")],
    regole=[r"(?<=shell_command\.vmc_master_)(velocita_[0-4]|notturna|iperventilazione|freecooling)(?![a-z0-9_])",
            # b39: il valore del Comando non eseguito «<velocità>|<istante>» (diviso a «{{», resta «<velocità>|»)
            r"^(Velocità [0-4]|Notturna|Iperventilazione|Free Cooling)(?=\|$)",
            r"(?<=')(Velocità [0-4]|Notturna|Iperventilazione|Free Cooling|Free Cool\./Heat\.)(?=')",
            r"(?<=: )(Velocità [0-4]|Notturna|Iperventilazione|Free Cool\./Heat\.)$",
            r"(?<=velocita_)(0|1|2|3|4|notturna|iperventilazione|freecooling|free_cooling)(?![a-z0-9])",
            r"(?<=Velocità )(0|1|2|3|4|Notturna|Iperventilazione|Free Cool\./Heat\.)(?![0-9])",
            r"(?<=Vel\. )([0-4])(?![0-9])", r"(?<=Vel\.)([0-4])(?![0-9])"],
    mappa_chiavi={"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "notturna": "N", "iperventilazione": "I",
                  "freecooling": "F", "free_cooling": "F", "free cool./heat.": "F", "free cooling": "F",
                  **{f"velocità {k}": k for k in "01234"}, **{f"velocita_{k}": k for k in "01234"}},
    max_chiavi=3,
)
GIORNO = Dimensione(
    "giorno", ["lun", "mar", "mer", "gio", "ven", "sab", "dom"], protezioni=[],
    regole=[r"(lunedi|lunedì|martedi|martedì|mercoledi|mercoledì|giovedi|giovedì|venerdi|venerdì|sabato|domenica)"],
    mappa_chiavi={g: g[:3] for g in ["lunedi", "lunedì", "martedi", "martedì", "mercoledi", "mercoledì", "giovedi",
                                     "giovedì", "venerdi", "venerdì", "sabato", "domenica"]},
    max_chiavi=1,
)
FASCIA = Dimensione(
    "fascia", ["1", "2"], protezioni=[],
    regole=[r"(?<=speed_)(1|2)(?=_fascia)", r"(?<=fascia_)(1|2)(?=_on)", r"(?<=Fascia )(1|2)(?= On)",
            r"(?<=fascia_)(1|2)(?=_o_2)"],
    mappa_chiavi={"1": "1", "2": "2"}, max_chiavi=1,
)
FREE_HC = Dimensione(
    "Free Heating/Cooling", ["H", "C"],
    protezioni=[(r"free_?heating_o_free_?cooling|freeheating_freecooling|free_heating_cooling", "FHOFC"),
                (r"spia_velocita_freecooling_un_solo_avvio_per_programmazione_(?=free)", "PROG"),
                (r"spia_velocita_freecooling(?!_un_solo_avvio_per)", "SVF"),
                (r"codice_interpretato(?:_interfaccia)?'\)(?:==|!=|in\[|not in\[)[^)]*", "VFREE"),
                (r"spia_umidita_velocita_freecooling", "SUVF"),
                (r"shell_command\.vmc_master_freecooling", "SHF"),
                (r"(?<=codice_interpretato'\)==)'Free Cooling'|(?<=codice_interpretato'\)!=)'Free Cooling'", "VFREE"),
                (r"(?<=codice_interpretato_interfaccia'\)==)'Free Cooling'", "VFREE"),
                (r"aria_scambiata_freecooling", "ARIA")],
    # nei messaggi dell'allerta Free il programma Heating va con «Raffrescamento» e Cooling con «Riscaldamento»
    regole=[r"(?:(?<=free)|(?<=free_)|(?<=free )|(?<=free-))(heating|cooling)", r"(Raffrescamento|Riscaldamento)"],
    mappa_chiavi={"heating": "H", "cooling": "C", "raffrescamento": "H", "riscaldamento": "C"}, max_chiavi=1,
)
ALLERTA = Dimensione(
    "allerta", ["C", "D"], protezioni=[],
    regole=[r"(?<=_)(congelamento|delta_temp_verifica_soglia_valore)(?![a-z_])",
            r"(?<=vmc_master_)(congelamento|delta_temp)(?=_verifica_soglia_valore_spia)",
            r"\b(Congelamento|Delta Temp|Δ)"],
    mappa_chiavi={"congelamento": "C", "delta_temp": "D", "delta_temp_verifica_soglia_valore": "D",
                  "Delta Temp": "D", "Δ": "D"},
    max_chiavi=1,
)


class Membro:
    def __init__(self, chiave: str, etichetta: str, fonte: Fonte, nodo: Any) -> None:
        self.chiave, self.etichetta, self.fonte, self.nodo = chiave, etichetta, fonte, nodo
        self.righe = linee(fonte, nodo)
        self.restanti: list[tuple[str, str, int]] = []


def confronta(membri: list[Membro], dim: Dimensione) -> list[dict[str, Any]]:
    """Differenze tra i blocchi gemelli dopo la normalizzazione lungo dim (come comune.confronta)."""
    esatte, dove, altre, altre_dove = {}, {}, {}, {}
    letterali = {m.chiave: Counter((p, t) for p, t, _ in m.righe) for m in membri}
    comuni: Counter = Counter()
    for c in set().union(*letterali.values()):
        comuni[c] = min(letterali[k][c] for k in letterali)
    for m in membri:
        tolti: Counter = Counter()
        m.restanti = []
        for p, t, r in m.righe:
            if tolti[(p, t)] < comuni[(p, t)]:
                tolti[(p, t)] += 1
            else:
                m.restanti.append((p, t, r))
    for m in membri:
        e, d, a, ad = Counter(), defaultdict(list), defaultdict(Counter), defaultdict(list)
        for percorso, t, r in m.restanti:
            t2, oth = dim.normalizza(t, m.chiave)
            if oth:
                a[(percorso, t2)].update(oth)
                ad[(percorso, t2)].append(r)
            else:
                e[(percorso, t2)] += 1
                d[(percorso, t2)].append(r)
        esatte[m.chiave], dove[m.chiave], altre[m.chiave], altre_dove[m.chiave] = e, d, a, ad
    diff: list[dict[str, Any]] = []
    for c in sorted(set().union(*esatte.values())):
        conti = {m.chiave: esatte[m.chiave][c] for m in membri}
        if len(set(conti.values())) > 1:
            diff.append({"tipo": "riga", "percorso": c[0], "testo": c[1], "conti": conti,
                         "righe": {m.chiave: dove[m.chiave].get(c, []) for m in membri}})
    chiavi_membri = {m.chiave for m in membri}
    for c in sorted(set().union(*altre.values())):
        profili = {m.chiave: altre[m.chiave].get(c, Counter()) for m in membri}
        scarti: dict[str, list] = defaultdict(list)
        for s in dim.chiavi:
            if s in chiavi_membri:
                continue
            valori = {k: profili[k][s] for k in chiavi_membri}
            moda = Counter(valori.values()).most_common(1)[0][0]
            for k, v in valori.items():
                if v != moda:
                    scarti[k].append((s, v, moda))
        coppie = {(k, s): profili[k][s] for k in chiavi_membri for s in chiavi_membri if s != k}
        if coppie:
            if len(chiavi_membri) == 2:
                (k1, s1), (k2, s2) = list(coppie)
                if coppie[(k1, s1)] != coppie[(k2, s2)]:
                    scarti[k1].append((s1, coppie[(k1, s1)], coppie[(k2, s2)]))
                    scarti[k2].append((s2, coppie[(k2, s2)], coppie[(k1, s1)]))
            else:
                atteso = {}
                for s in chiavi_membri:
                    valori = Counter(profili[k][s] for k in chiavi_membri if k != s)
                    atteso[s] = max(valori, key=lambda n: (valori[n], n))
                for (k, s), v in coppie.items():
                    if v != atteso[s]:
                        scarti[k].append((s, v, atteso[s]))
                if len(set(atteso.values())) > 1:
                    proprio = (c[0], c[1].replace("⟨A⟩", "⟨V⟩"))
                    for s, n in atteso.items():
                        if n > min(atteso.values()) and esatte[s][proprio] != n:
                            scarti[s].append(("sé", esatte[s][proprio], n))
        if scarti:
            diff.append({"tipo": "altre", "percorso": c[0], "testo": c[1], "scarti": dict(scarti),
                         "righe": {m.chiave: altre_dove[m.chiave].get(c, []) for m in membri}})
    return diff


def raggruppa(diff: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Differenze «riga» con la stessa ripartizione messe insieme; «altre» una per una."""
    gruppi: dict = {}
    out = []
    for d in diff:
        if d["tipo"] == "riga":
            firma = tuple(sorted(d["conti"].items()))
            gruppi.setdefault(firma, {"tipo": "riga", "conti": d["conti"], "voci": []})["voci"].append(d)
        else:
            out.append({"tipo": "altre", "voci": [d]})
    out.extend(gruppi.values())
    return sorted(out, key=lambda g: min((r for v in g["voci"] for rr in v["righe"].values() for r in rr), default=0))


# ------------------------------------------------------------------------------------------------ d5 (gemelli_velocita.py)
VEL_TESTO = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "notturna": "N", "notturno": "N",
             "iperventilazione": "I", "free cool./heat.": "F", "free-cooling": "F", "freecooling": "F",
             "free cooling": "F", "free_cooling": "F"}


def kvel(g: str) -> str:
    g = g.lower()
    m = re.search(r"([0-4])$", g)
    return m.group(1) if m else VEL_TESTO[g]


def khc(g: str) -> str:
    g = g.lower()
    return "H" if g.startswith("on e") or ("heating" in g and not g.startswith("off e")) else "C"


def kgiorno(g: str) -> str:
    return g.lower()[:3]


VX = r"(Vel\. [0-4]|Velocità [0-4]|a Velocità [0-4]|Notturna|Notturno|Iperventilazione|Free Cool\./Heat\.|Free-Cooling)"
SX = r"(0|1|2|3|4|notturna|iperventilazione|freecooling|free_cooling|Free Cooling)"
GIORNI = r"(Lunedì|Martedì|Mercoledì|Giovedì|Venerdì|Sabato|Domenica)"
FAMIGLIE_TRIGGER = [
    ("PdR Vel. X -> Imposta Velocità 0", rf"PdR {VX} ?-> Imposta Velocità 0", kvel, VELOCITA),
    ("PdR Vel. X se Spia Inquinanti ON", rf"PdR {VX} se Spia Inquinanti ON", kvel, VELOCITA),
    ("Rip. Vel. X No PdR", rf"Rip\. {VX} No PdR", kvel, VELOCITA),
    ("Rip. Vel. X No PdR se Spia Inquinanti ON", rf"Rip\. {VX} No PdR +se Spia Inquinanti ON", kvel, VELOCITA),
    ("Black-Out Velocità X [ON]", rf"Black-Out {VX}", kvel, VELOCITA),
    ("Black-Out Velocità X [OFF, Ripristino]", rf"Black-Out Off {VX}", kvel, VELOCITA),
    ("Spia Velocità X CO2/VOC", rf"spia_velocita_{SX}_inquinanti_co2_voc", kvel, VELOCITA),
    ("Spia Velocità X Congelamento", rf"spia_velocita_{SX}_congelamento", kvel, VELOCITA),
    ("Spia Velocità X Δ Temp.", rf"spia_velocita_{SX}_delta_temp", kvel, VELOCITA),
    ("Umidità ON Vel. X", rf"umidita_velocita_{SX}", kvel, VELOCITA),
    ("Calendario 1° <giorno> On", rf"1° {GIORNI} On", kgiorno, GIORNO),
    ("Calendario 1° <giorno> Off", rf"1° {GIORNI} Off", kgiorno, GIORNO),
    ("Calendario 2° <giorno> On", rf"2° {GIORNI} On", kgiorno, GIORNO),
    ("Calendario 2° <giorno> Off", rf"2° {GIORNI} Off", kgiorno, GIORNO),
    ("TeVsTi Free-X -> Imposta Velocità 0", r"TeVsTi Free-(Heating|Cooling) -> Imposta Velocità 0", khc, FREE_HC),
    ("TeVsTi Free-X e Spia Inquinanti ON", r"TeVsTi Free-(Heating|Cooling) e Spia Inquinanti ON", khc, FREE_HC),
    ("Rip. Free X No TeVsTi", r"Rip\. Free (Heating|Cooling) No TeVsTi ?", khc, FREE_HC),
    ("Rip. Free X No TeVsTi e Spia Inquinanti ON", r"Rip\. Free (Heating|Cooling) No TeVsTi e Spia Inquinanti ON", khc,
     FREE_HC),
    ("Disattivazione Vel. Free X",
     r" ?Disattivazione VMC ON/OFF, in Funzione della Vel\. Free (Heating|Cooling) precedentemente Armato", khc, FREE_HC),
    ("Disattivazione Vel. Free X e Spia Inquinanti ON",
     r" ?Disattivazione VMC ON/OFF, in Funzione della Vel\. Free (Heating|Cooling) precedentemente Armato e Spia "
     r"Inquinanti ON", khc, FREE_HC),
    ("PdR Spia Free X ON -> Imposta Velocità 0",
     r"PdR Spia Free Heating (ON e Spia FreeCooling OFF|OFF e Spia FreeCooling ON) -> Imposta Velocità 0", khc, FREE_HC),
    ("PdR Spia Free X ON -> Imposta Velocità 1 se Spia Inquinanti ON",
     r"PdR Spia Free Heating (ON e Spia FreeCooling OFF|OFF e Spia FreeCooling ON) -> Imposta Velocità 1 se Spia "
     r"Inquinanti ON", khc, FREE_HC),
    ("PdR Vel. 0 con Spia FreeX On -> Imposta Velocità 0", r"PdR Vel\. 0 con Spia Free(Heating|Cooling) On -> Imposta "
     r"Velocità 0", khc, FREE_HC),
    ("PdR Vel. 0 con Spia FreeX On e Inquinanti Vel. 1 ON -> Imposta Velocità 1",
     r"PdR Vel\. 0 con Spia Free(Heating|Cooling) On e Inquinanti Vel\. 1 ON  -> Imposta Velocità 1", khc, FREE_HC),
]


def ids_opzione(opz: Any) -> list[str]:
    ids: list[str] = []
    for c in lista(mappa(opz).get("conditions")):
        cm = mappa(c)
        if cm.get("condition") is not None and cm["condition"].value == "trigger":
            n = cm["id"]
            ids += [x.value for x in lista(n)] if lista(n) else [n.value]
    return ids


def _opzioni_principali(aut: Fonte) -> list[Any]:
    return lista(next(mappa(b) for b in lista(mappa(aut.radice)["actions"]) if "choose" in mappa(b))["choose"])


def famiglie_esplicite(aut: Fonte, pkg: Fonte) -> list[tuple[str, list[Membro], Dimensione]]:
    trigger = lista(mappa(aut.radice)["triggers"])
    out = []
    for nome, rx, kf, dim in FAMIGLIE_TRIGGER:
        r = re.compile(rx)
        mt: dict[str, Membro] = {}
        mo: dict[str, Membro] = {}
        for t in trigger:
            tid = mappa(t).get("id")
            if tid is not None and (m := r.fullmatch(tid.value)):
                k = kf(m.group(1))
                assert k not in mt, (nome, tid.value)
                mt[k] = Membro(k, tid.value.strip(), aut, t)
        for o in _opzioni_principali(aut):
            for tid in ids_opzione(o):
                if m := r.fullmatch(tid):
                    k = kf(m.group(1))
                    assert k not in mo, (nome, tid)
                    mo[k] = Membro(k, tid.strip(), aut, o)
        if len(mt) >= 2:
            out.append((f"[trigger] {nome}", list(mt.values()), dim))
        if len(mo) >= 2:
            out.append((f"[ramo d'azione] {nome}", list(mo.values()), dim))
    script = mappa(mappa(pkg.radice)["script"])
    f1, f2 = script.get("vmc_master_calendario_fascia_1_on"), script.get("vmc_master_calendario_fascia_2_on")
    if f1 is not None and f2 is not None:
        out.append(("[script] Calendario Fascia N On",
                    [Membro("1", "fascia_1_on", pkg, f1), Membro("2", "fascia_2_on", pkg, f2)], FASCIA))
    return out


def _choose(nodo: Any, out: list[Any]) -> None:
    if isinstance(nodo, yaml.MappingNode):
        m = mappa(nodo)
        if "choose" in m and lista(m["choose"]):
            out.append(m["choose"])
        for _, v in nodo.value:
            _choose(v, out)
    elif isinstance(nodo, yaml.SequenceNode):
        for x in nodo.value:
            _choose(x, out)


def _ids_profondi(n: Any) -> list[str]:
    """Gli id dei trigger nelle condizioni di un'opzione, anche dentro un «or»."""
    if isinstance(n, yaml.SequenceNode):
        return [i for x in n.value for i in _ids_profondi(x)]
    m = mappa(n)
    if m.get("condition") is not None and m["condition"].value == "trigger":
        return [x.value for x in lista(m["id"])] if lista(m["id"]) else [m["id"].value]
    return _ids_profondi(m["conditions"]) if "conditions" in m else []


def famiglie_annidate(aut: Fonte, pkg: Fonte) -> list[tuple[str, list[Membro], Dimensione]]:
    """Opzioni dello stesso choose con le stesse condizioni a meno della velocità (o di Heating/Cooling). Il nome della
    famiglia non usa le righe (cambiano a ogni modifica): blocco che la contiene (id dei trigger dell'opzione principale,
    script o automazione del package) e alias della prima copia."""
    guardia = next(b for b in lista(mappa(aut.radice)["actions"]) if str(getattr(mappa(b).get("alias"), "value", "")).startswith("Evento ancora valido"))
    fonti: list[tuple[Fonte, Any, str]] = [(aut, guardia, "automazione, guardia")]
    for o in _opzioni_principali(aut):
        ids = [i.strip() for i in _ids_profondi(mappa(o)["conditions"])]
        fonti.append((aut, o, f"automazione «{ids[0]}»" + (f" (+{len(ids) - 1} trigger)" if len(ids) > 1 else "")))
    pr = mappa(pkg.radice)
    fonti += [(pkg, s, f"script {nome}") for nome, s in mappa(pr["script"]).items()]
    for a in lista(pr["automation"]):
        fonti.append((pkg, a, f"automazione del package «{mappa(a)['alias'].value if 'alias' in mappa(a) else '?'}»"))
    out = []
    for fonte, radice, dove in fonti:
        chooses: list[Any] = []
        _choose(radice, chooses)
        for ch in chooses:
            opz = [o for o in lista(ch) if "conditions" in mappa(o)]
            for dim in (VELOCITA, FREE_HC):
                gruppi: dict = defaultdict(list)
                for o in opz:
                    cond = Membro("?", "", fonte, mappa(o)["conditions"]).righe
                    for k in sorted({c for _, t, _ in cond for _, _, c in dim.trova(t)}):
                        firma = tuple(sorted({(p, dim.normalizza(t, k)[0]) for p, t, _ in cond}))
                        if any("⟨V⟩" in t for _, t in firma):
                            gruppi[firma].append((k, o))
                usati: set[int] = set()
                for _, elenco in sorted(gruppi.items(), key=lambda x: -len(x[1])):
                    elenco = [(k, o) for k, o in elenco if id(o) not in usati]
                    volte: dict[int, int] = defaultdict(int)
                    for _, o in elenco:
                        volte[id(o)] += 1
                    per_k: dict[str, Any] = {}
                    for k, o in elenco:
                        if volte[id(o)] == 1 and k not in per_k:
                            per_k[k] = o
                    if len(per_k) < 2:
                        continue
                    usati.update(id(o) for o in per_k.values())
                    membri = []
                    for k, o in per_k.items():
                        et = mappa(o).get("alias")
                        membri.append(Membro(k, ((et.value if et is not None else "") or f"opzione {k}")[:70], fonte, o))
                    out.append((f"[opzioni annidate] {dove}: «{membri[0].etichetta}»", membri, dim))
    return out


SPECIALI = {"0", "1", "F"}  # V0 = VMC ferma, V1 = velocità degli Inquinanti (Foglio E7, NOTA 1), Free = righe 14-19


def devianti(g: dict[str, Any]) -> set[str]:
    if g["tipo"] == "riga":
        conti = g["conti"]
        moda = max(set(conti.values()), key=lambda n: (list(conti.values()).count(n), -n))
        return set(conti) if len(conti) == 2 else {k for k, n in conti.items() if n != moda}
    return set(g["voci"][0]["scarti"])


def classe(dim: Dimensione, g: dict[str, Any]) -> str:
    if dim is not VELOCITA:
        return "B"
    dev = devianti(g)
    return "A" if dev and dev <= SPECIALI else "B"


@lru_cache
def _gemelli_velocita() -> dict[str, tuple[int, int, int, int]]:
    """Per famiglia: (gruppi di classe A, pezzi di classe A, gruppi di classe B, pezzi di classe B)."""
    aut, pkg = _fonti()
    out: dict[str, tuple[int, int, int, int]] = {}
    for nome, membri, dim in famiglie_esplicite(aut, pkg) + famiglie_annidate(aut, pkg):
        assert nome not in out, nome
        conti = Counter()
        for g in raggruppa(confronta(membri, dim)):
            cl = classe(dim, g)
            conti[cl + "g"] += 1
            conti[cl + "p"] += len(g["voci"])
        out[nome] = (conti["Ag"], conti["Ap"], conti["Bg"], conti["Bp"])
    return out


# Gruppi di classe A per famiglia (solo le famiglie con differenze: le altre 42 devono restare identiche). Motivi, dal
# rapporto del controllo statico (differenze volute per le velocità con logica propria nel Foglio):
# - PdR Vel. X: copia Free senza «annulla Ripresa Free», V1 con l'«else» della correzione O3, copia Free che spegne
#   anche la Partenza e le memorie Inquinanti (da decidere, innocuo); se Inquinanti: V1 = Inquinanti già a V1 (E7 NOTA 1,
#   A28), Free = memoria Free e programmazione (righe 14-19, NOTA 2/3);
# - Rip. X No PdR (anche se Inquinanti): ripresa Free e logica V0/V1 (A28);
# - Black-Out [ON]: V1 con i trigger «caso Inquinanti» a parte, V0 che accende la propria spia, copia Free che non spegne
#   spia_velocita_0 (da decidere, nessun effetto: trigger e guardia la chiedono già spenta); Black-Out [OFF]: memoria
#   PdR e Inquinanti partiti da 0 nel V0, scelta Free/Heating nel Free;
# - Spia Vel. X CO2/VOC: A28 (Inquinanti a V0 -> V1 con ritorno a 0, C3-2); Spia Congelamento: il V0 è la velocità del
#   Congelamento; Umidità ON: a V0 l'Umidità non avvia la VMC (F6, A21, b25 ce4d20b);
# - opzioni annidate: Inquinanti ON con memoria PdR (A28); Congelamento ON, passaggio delle memorie V0/V1/Free; fine
#   Congelamento e fine Δ: la regola 03-11-2026 non vale per V0 e a V1 esclude la Velocità 1 avviata dagli Inquinanti
#   partiti da Velocità 0 (A1-2 e il suo gemello nel Congelamento, b36: le due famiglie hanno gli stessi conteggi); Δ ON:
#   il Δ comanda la Velocità 1; fine Umidità (spia_umidita_off); script delle Fasce: Fascia a V0 con Inquinanti -> V1 e
#   ritorno a 0 (A25, A28).
CLASSE_A = {
    # b39: +2/+2/+2/+2/+9 nelle 5 famiglie qui sotto, il passo «Comando non eseguito» dopo i cicli che esistono solo nelle
    # copie speciali (V0/V1/Free): tolti i 135 passi i conteggi tornano quelli della b38 (11, 16, 20, 21, 59), prova
    # rifatta dopo l'«else» che annulla il comando più vecchio (prima il passo di «Rip. Vel. X No PdR se Spia Inquinanti
    # ON» cadeva in un gruppo già contato)
    "[ramo d'azione] PdR Vel. X -> Imposta Velocità 0": 13,
    "[ramo d'azione] PdR Vel. X se Spia Inquinanti ON": 18,
    "[trigger] Rip. Vel. X No PdR": 2,
    "[ramo d'azione] Rip. Vel. X No PdR": 22,
    "[trigger] Rip. Vel. X No PdR se Spia Inquinanti ON": 2,
    # b36 (b36-pdr2): 18 -> 21, la protezione della scelta dell'utente nei 3 casi con comando del ramo Free (dentro il choose)
    "[ramo d'azione] Rip. Vel. X No PdR se Spia Inquinanti ON": 23,
    "[trigger] Black-Out Velocità X [ON]": 1,
    "[ramo d'azione] Black-Out Velocità X [ON]": 2,
    "[ramo d'azione] Black-Out Velocità X [OFF, Ripristino]": 18,
    "[trigger] Spia Velocità X CO2/VOC": 1,
    "[ramo d'azione] Spia Velocità X CO2/VOC": 68,
    "[trigger] Spia Velocità X Congelamento": 1,
    # b40 (free_v0, decisioni 2-3 del 23-11-2026) 2 -> 3 e 22 -> 28; b41 (decisioni 2-3 del proprietario del
    # 25-11-2026: con la Free sospesa la Velocità 0 scelta durante l'Umidità resta, come nella b39) di nuovo 2 e 22
    "[trigger] Umidità ON Vel. X": 2,
    "[ramo d'azione] Umidità ON Vel. X": 22,
    "[opzioni annidate] automazione «inquinanti_co2_voc_on»: «Caso Velocità 0 con PdR su Velocità 1 o Spia Inquinanti "
    "su Velocità 1»": 5,
    "[opzioni annidate] automazione «Congelamento ON» (+8 trigger): «Velocità 0»": 41,
    "[opzioni annidate] automazione «Congelamento OFF»: «Spia Velocità 0 per Congelamento»": 3,
    # b36 (b36-umi): 7 -> 11, protezione della scelta con esclusioni proprie nei casi Velocità 0, 1 e Free Cooling
    "[opzioni annidate] automazione «spia_umidita_off»: «Velocità 0»": 11,
    # b40 (free_v0, decisione 1 del 23-11-2026): 6 -> 8, solo l'opzione Velocità 0 annulla la ripresa Free (le altre
    # velocità scelte la annullano già a fine allerta con il trigger «Cambio Velocità quanto Spia ... - Inquinanti OFF»)
    "[opzioni annidate] automazione «delta_temp_ON» (+8 trigger): «Velocità 0»": 8,
    "[opzioni annidate] automazione «delta_temp_OFF»: «Spia Velocità 0 per Δ Temp. > 23 [°C]»": 3,
    "[opzioni annidate] script vmc_master_calendario_fascia_1_on: «opzione 0»": 7,
    "[opzioni annidate] script vmc_master_calendario_fascia_2_on: «opzione 0»": 7,
}
# Classe B ammessa (famiglia -> (gruppi, pezzi)): la riscrittura compatta B1-3 della b34 di «Allerte Free Cooling ON»
# negli script delle Fasce (B2, equivalenza provata da test_b34_calendario.py, 96 combinazioni) e l'«until» del ramo
# «TeVsTi Free-Cooling e Spia Inquinanti ON» con la spia «per programmazione» Free Cooling in più (B1: la spia viene
# accesa nello stesso giro del ciclo, nessun effetto pratico; da decidere se allineare).
CLASSE_B = {
    # b39: 1 -> 2 pezzi, il passo dopo il ciclo che memorizza il Comando non eseguito ripete l'«until» (con la stessa spia
    # «per programmazione» in più della copia Free Cooling): stessa differenza B1, nessuna nuova
    "[ramo d'azione] TeVsTi Free-X e Spia Inquinanti ON": (1, 2),
    # b36 (b36-umi, Foglio A21): nella protezione della scelta a fine Umidita' ogni velocita' memorizzata (2, 3, 4,
    # Notturna, Iperventilazione) esclude solo se stessa (la Velocita' 1 era gia' in classe A): differenza voluta
    "[opzioni annidate] automazione «spia_umidita_off»: «Velocità 0»": (5, 5),
    "[opzioni annidate] script vmc_master_calendario_fascia_1_on: «Programmato Mese Free Heating»": (7, 61),
    "[opzioni annidate] script vmc_master_calendario_fascia_2_on: «Programmato Mese Free Heating»": (7, 61),
}


def test_rami_gemelli_per_velocita_uguali_a_meno_delle_eccezioni() -> None:
    """d5: 67 famiglie gemelle; nessuna differenza in una copia normale (V2, V3, V4, Notturna, Iperventilazione) né in
    una famiglia di 2 copie, salvo le eccezioni di CLASSE_B; i gruppi di classe A per famiglia sono quelli di CLASSE_A."""
    misurati = _gemelli_velocita()
    assert len(misurati) == 67
    classe_a = {n: c[0] for n, c in misurati.items() if c[0]}
    classe_b = {n: (c[2], c[3]) for n, c in misurati.items() if c[2]}
    assert classe_b == CLASSE_B, f"classe B misurata: {classe_b}"
    assert classe_a == CLASSE_A, f"classe A misurata: {classe_a}"
    # una famiglia puo' stare in tutte e due le classi (b36: «spia_umidita_off»)
    assert sum(1 for c in misurati.values() if any(c)) == len(set(CLASSE_A) | set(CLASSE_B))


def test_fine_congelamento_e_fine_delta_stessi_conteggi_per_velocita() -> None:
    """d5 + d7: le opzioni per velocità di fine Congelamento e di fine Δ Temp. si discostano dalle altre copie negli
    stessi punti (regola 03-11-2026: nessuna a V0, esclusione degli Inquinanti partiti da 0 a V1)."""
    misurati = _gemelli_velocita()
    gelo = misurati["[opzioni annidate] automazione «Congelamento OFF»: «Spia Velocità 0 per Congelamento»"]
    delta = misurati["[opzioni annidate] automazione «delta_temp_OFF»: «Spia Velocità 0 per Δ Temp. > 23 [°C]»"]
    assert gelo == delta == (3, 11, 0, 0)


# ------------------------------------------------------------------------------------------------ d7/d8 (percorsi.py)
TIPI_GARANZIA = {"trigger", "opzione", "se", "condizione", "mentre"}  # condizioni vere quando si arriva al passo
TIPI_ESCLUSIONE = {"esclusa", "se-no"}  # condizioni false quando si arriva al passo


class Guardia:
    __slots__ = ("riga", "testo", "tipo")

    def __init__(self, tipo: str, testo: str, riga_: int) -> None:
        self.tipo, self.testo, self.riga = tipo, testo, riga_


def _testo_condizioni(n: Any) -> str:
    """Tutto il testo di un blocco di condizioni (template normalizzati, condizioni state come «states('x')=='y'»)."""
    parti: list[str] = []

    def visita(c: Any) -> None:
        if isinstance(c, yaml.SequenceNode):
            for x in c.value:
                visita(x)
            return
        if isinstance(c, yaml.ScalarNode):
            parti.append(norm_template(c.value))
            return
        m = mappa(c)
        tipo = m.get("condition")
        if tipo is not None and tipo.value == "state" and "entity_id" in m and "state" in m:
            ent = [x.value for x in lista(m["entity_id"])] or [m["entity_id"].value]
            val = [x.value for x in lista(m["state"])] or [m["state"].value]
            parti.extend(" or ".join(f"states('{e}')=='{v}'" for v in val) for e in ent)
            return
        if tipo is not None and tipo.value in ("and", "or", "not"):
            parti.append(f"{tipo.value}[")
            visita(m.get("conditions"))
            parti.append("]")
            return
        for k, v in c.value:
            if k.value not in ("alias", "id"):
                visita(v)

    if n is not None:
        visita(n)
    return " ".join(parti)


def cammina(seq: Any, guardie: list[Guardia], visita) -> None:
    """Visita ogni passo di una sequenza (anche annidato) con le condizioni del cammino che porta al passo."""
    passi = lista(seq) if isinstance(seq, yaml.SequenceNode) else ([seq] if isinstance(seq, yaml.MappingNode) else [])
    attuali = list(guardie)
    for p in passi:
        m = mappa(p)
        if not m:
            continue
        visita(p, attuali)
        if "condition" in m and "action" not in m and "service" not in m:
            attuali = [*attuali, Guardia("condizione", _testo_condizioni(p), riga(p))]
            continue
        if "wait_template" in m:
            attuali = [*attuali, Guardia("attesa", norm_template(m["wait_template"].value), riga(p))]
        if "choose" in m:
            precedenti: list[Guardia] = []
            for o in lista(m["choose"]):
                om = mappa(o)
                c = _testo_condizioni(om.get("conditions"))
                cammina(om.get("sequence"), [*attuali, *precedenti, Guardia("opzione", c, riga(o))], visita)
                precedenti = [*precedenti, Guardia("esclusa", c, riga(o))]
            if "default" in m:
                cammina(m["default"], attuali + precedenti, visita)
        if "if" in m:
            c = _testo_condizioni(m["if"])
            cammina(m.get("then"), [*attuali, Guardia("se", c, riga(m["if"]))], visita)
            if "else" in m:
                cammina(m["else"], [*attuali, Guardia("se-no", c, riga(m["if"]))], visita)
        if "repeat" in m:
            r = mappa(m["repeat"])
            g = attuali
            if "while" in r:
                g = [*g, Guardia("mentre", _testo_condizioni(r["while"]), riga(r["while"]))]
            cammina(r.get("sequence"), g, visita)
        if "sequence" in m:
            cammina(m["sequence"], attuali, visita)
        if "parallel" in m:
            for x in lista(m["parallel"]) or [m["parallel"]]:
                cammina(x, attuali, visita)


def guardie_trigger(aut: Fonte, opz: Any) -> list[Guardia]:
    """Una guardia «trigger» per ogni trigger dell'opzione (sono in OR: vale solo ciò che hanno tutti)."""
    trigger = {mappa(t)["id"].value: t for t in lista(mappa(aut.radice)["triggers"]) if "id" in mappa(t)}
    out = []
    for i in ids_opzione(opz):
        t = trigger.get(i)
        if t is None:
            continue
        tm = mappa(t)
        testo = (norm_template(tm["value_template"].value) if "value_template" in tm else
                 f"[trigger {tm['trigger'].value if 'trigger' in tm else '?'}] " + " ".join(s.value for s in scalari(t)))
        out.append(Guardia("trigger", testo, riga(t)))
    return out


# ------------------------------------------------------------------------------------------------ d7/d8 (gemelli_allerte.py)
def _spenta(ent: str) -> re.Pattern:
    return re.compile(re.escape(f"states('{ent}')") + r"(?:=='off'|!='on')")


PROTEZIONI = {
    "CONG": _spenta("input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"),
    "DELTA": _spenta("input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia"),
    "PDR": re.compile(r"opzioni_accendi_spegni_vmc_vs_pdr|punto_di_rugiada_verifica_confronto"),
    "V0": _spenta("input_boolean.vmc_master_spia_velocita_0"),
    "FASE": re.compile(r"fase_riallineamento_al_riavvio"),
    "MEMPDR": re.compile(r"spia_velocita_[a-z0-9]+_un_solo_avvio'\)(?!_per)"),
}
COMANDO = re.compile(r"shell_command\.vmc_master_(velocita_[0-4]|notturna|iperventilazione|freecooling|\{\{.*)")
FINE_ALLERTA = [  # (ramo, espressione sugli id dei trigger dell'opzione: l'ultima che combacia vince)
    ("Fine Congelamento", r"Congelamento OFF"),
    ("Fine Δ", r"delta_temp_OFF"),
    ("Fine PdR", r"Rip\. (?:Vel\. )?\S+ No PdR"),
    ("Fine PdR con Inquinanti", r"Rip\. (?:Vel\. )?\S+ No PdR se Spia Inquinanti ON"),
    ("Fine Inquinanti", r"inquinanti_co2_voc_off"),
    ("Fine Umidità", r"spia_umidita_off"),
    ("Fine Umidità con Inquinanti partiti da 0", r"umidita_off_con_inquinanti_partenza_velocita_0"),
    ("Fine Black-Out", r"Black-Out Off .*"),
]


def presenza(guardie: list[Guardia], gt: list[Guardia]) -> dict[str, str]:
    """Per ogni protezione: 'T' nel trigger (tutti i trigger), 'P' nel percorso, 'E' solo in un'esclusione, '-' no."""
    out = {}
    for k, rx in PROTEZIONI.items():
        if gt and all(rx.search(g.testo) for g in gt):
            out[k] = "T"
        elif any(g.tipo in TIPI_GARANZIA and g.tipo != "trigger" and rx.search(g.testo) for g in guardie):
            out[k] = "P"
        elif any(g.tipo in TIPI_ESCLUSIONE and rx.search(g.testo) for g in guardie):
            out[k] = "E"
        else:
            out[k] = "-"
    return out


@lru_cache
def _comandi_fine_allerta() -> tuple[tuple[str, int, str, tuple[tuple[str, str], ...]], ...]:
    """(ramo, riga, comando, protezioni) per ogni comando alla VMC nei rami di fine allerta."""
    aut, _ = _fonti()
    out = []
    for o in _opzioni_principali(aut):
        ids = ids_opzione(o)
        gruppo = None
        for nome, rx in FINE_ALLERTA:
            if ids and all(re.fullmatch(rx, i.strip()) for i in ids):
                gruppo = nome
        if gruppo is None:
            continue
        gt = guardie_trigger(aut, o)
        altre = [c for c in lista(mappa(o)["conditions"])
                 if mappa(c).get("condition") is None or mappa(c)["condition"].value != "trigger"]
        g0 = [Guardia("opzione", " ".join(_testo_condizioni(c) for c in altre), riga(o))] if altre else []

        def visita(nodo: Any, guardie: list[Guardia], gruppo: str = gruppo, gt: list[Guardia] = gt) -> None:
            az = mappa(nodo).get("action") or mappa(nodo).get("service")
            if az is not None and (mc := COMANDO.fullmatch(az.value.strip())):
                out.append((gruppo, riga(nodo), mc.group(1)[:20], tuple(presenza(guardie, gt).items())))

        cammina(mappa(o).get("sequence"), g0, visita)
    return tuple(out)


def test_protezioni_dei_comandi_nei_rami_di_fine_allerta() -> None:
    """d7/d8: ogni comando alla VMC nei rami di fine allerta ha sul cammino la fase del riallineamento al riavvio e la
    spia_velocita_0 spenta (Black-Out non in corso), salvo i rami di fine Black-Out, dove spia_velocita_0 è la memoria
    del Black-Out stesso. Fine Congelamento e fine Δ Temp. hanno lo stesso profilo di protezioni: nessuna delle due legge
    l'altra spia né il PdR, perché i trigger delle altre allerte chiedono Congelamento e Δ spenti (rapporto, parte B)."""
    comandi = _comandi_fine_allerta()
    gruppi = {g for g, *_ in comandi}
    assert gruppi == {nome for nome, _ in FINE_ALLERTA}
    for gruppo, r, comando, prot in comandi:
        p = dict(prot)
        assert p["FASE"] in "TP", (gruppo, r, comando)
        if gruppo != "Fine Black-Out":
            assert p["V0"] in "TP", (gruppo, r, comando)
    profili = {g: sorted((c, prot) for gg, _, c, prot in comandi if gg == g) for g in ("Fine Congelamento", "Fine Δ")}
    assert len(profili["Fine Congelamento"]) == len(profili["Fine Δ"]) == 8
    assert profili["Fine Congelamento"] == profili["Fine Δ"]


def _membri_fine_allerta() -> tuple[Membro, Membro]:
    aut, _ = _fonti()
    (gelo,) = [o for o in _opzioni_principali(aut) if ids_opzione(o) == ["Congelamento OFF"]]
    (delta,) = [o for o in _opzioni_principali(aut) if ids_opzione(o) == ["delta_temp_OFF"]]
    return Membro("C", "Congelamento OFF", aut, gelo), Membro("D", "delta_temp_OFF", aut, delta)


def _righe_del_passo_c3_1(delta: Membro) -> set[int]:
    """Le righe dei due passi che solo il Δ Temp. ha (C3-1 della b35, Foglio D6: velocità scelta negli ultimi secondi)."""
    righe: set[int] = set()
    for p in lista(mappa(delta.nodo)["sequence"]):
        alias = mappa(p).get("alias")
        if alias is not None and (alias.value.startswith("Velocità letta a fine allerta Δ Temp.")
                                  or alias.value.startswith("Velocità cambiata dall'utente negli ultimi Secondi")):
            righe.update(range(riga(p), fine(p) + 1))
    assert righe
    return righe


def test_fine_congelamento_e_fine_delta_gemelli() -> None:
    """d7: fine Congelamento contro fine Δ Temp. pezzo per pezzo (il nome dell'allerta diventa un segnaposto). Restano
    solo le differenze giudicate volute dal controllo statico:
    - A1 (C=1, D=2; 9 pezzi): il Δ spegne le spie delle memorie due volte, il Congelamento una volta;
    - A2 (C=8, D=0 e C=0, D=8; 20 e 10 pezzi): elenchi delle spie spente nei rami per velocità scritti in modo diverso
      (struttura diversa, stesso effetto);
    - A3 (C=0, D=1; 14 pezzi): solo il Δ ha il passo della velocità scelta negli ultimi secondi (C3-1, Foglio D6),
      perché il trigger di fine Δ aspetta 4 s e quello di fine Congelamento no (b39: 14 -> 20 pezzi, la stessa
      condizione esclude la velocità rimasta quella di prima di un comando non eseguito in Fascia; il Congelamento non
      ha il passo e quindi nemmeno l'esclusione).
    A4 (il ramo Velocità 1 di fine Δ esclude la Velocità 1 avviata dagli Inquinanti partiti da Velocità 0, A1-2, e il
    gemello di fine Congelamento no) non c'è più: corretto nella b36.
    b40 (free_v0, decisione 1 del 23-11-2026): nello stesso passo C3-1 del Δ la Velocità 0 scelta con la Free sospesa
    annulla la ripresa Free (A3 20 -> 23 pezzi; A5, C=0, D=2, 2 pezzi: «condition: template» e «input_boolean.turn_off»
    ripetuti dal passo degli Inquinanti); il Congelamento non ha il passo (C6: con la Velocità 0 non cambia nulla)."""
    gelo, delta = _membri_fine_allerta()
    gruppi = raggruppa(confronta([gelo, delta], ALLERTA))
    misurati = {tuple(sorted(g["conti"].items())): len(g["voci"]) for g in gruppi if g["tipo"] == "riga"}
    assert all(g["tipo"] == "riga" for g in gruppi)
    assert misurati == {(("C", 1), ("D", 2)): 9, (("C", 8), ("D", 0)): 20, (("C", 0), ("D", 1)): 23,
                        (("C", 0), ("D", 8)): 10, (("C", 0), ("D", 2)): 2}, misurati
    passo = _righe_del_passo_c3_1(delta)
    (a3,) = [g for g in gruppi if g["conti"] == {"C": 0, "D": 1}]
    (a5,) = [g for g in gruppi if g["conti"] == {"C": 0, "D": 2}]
    fuori = [(v["righe"]["D"], v["testo"]) for v in a3["voci"] + a5["voci"] if not set(v["righe"]["D"]) <= passo]
    assert not fuori, fuori


def test_marcatori_correzione() -> None:
    """d7/d8: i marcatori «(correzione Ox)» negli alias, per controllare che una correzione sia in tutti i rami gemelli
    (per esempio O2 nei 4 rami «Disattivazione Free», 2 × Heating/Cooling)."""
    conti: Counter = Counter()
    for fonte in _fonti():
        for r in fonte.righe:
            conti.update(re.findall(r"\(correzione (O\d+)\)", r))
    assert dict(conti) == {"O2": 4, "O3": 1, "O4": 1, "O5": 2, "O6": 2}
