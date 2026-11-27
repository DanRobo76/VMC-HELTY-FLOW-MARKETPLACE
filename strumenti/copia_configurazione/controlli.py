"""I controlli del banco: «dopo» contro «prima», con i conteggi esatti.

Ogni controllo è un dizionario ``{"nome", "esito", "conteggi", "dettagli", "spiegazione"}``
con ``esito`` = ``"passato"``, ``"fallito"``, ``"non eseguibile"`` (manca un'istantanea
perché un passo prima non c'è stato: il primo passo mancante lo dice) o
``"informazione"`` (si misura e si racconta, senza un valore atteso deciso).

Le istantanee (istantanea.py) usate dal passo ``passaggio``:

- ``P0_prima``: la beta accesa, con i conti alla rovescia appena avviati dalla scheda;
- ``F0_fermata_controllo`` / ``R_riavvio_di_controllo``: un riavvio della beta senza
  passaggio. Home Assistant è l'oracolo di cosa fa un riavvio: un valore che cambia da
  ``P0`` a ``R`` cambia per Home Assistant stesso (``initial``, automazioni dell'avvio,
  timer senza ``restore``), non per il passaggio;
- ``P_prima_del_passaggio``: la beta di nuovo con i conti alla rovescia, subito prima del
  passaggio; ``FP_fermata_beta``: i file alla fermata della beta, con
  ``core.restore_state`` (gli ultimi valori degli aiutanti: quelli da portare);
- ``M_primo_avvio_nativo`` (+ ``M_file``): il primo avvio con il codice nativo;
- ``FC_fermata_dopo_conferma``, ``A_dopo``, ``FA_fermata_finale``: dopo la conferma
  della riparazione e il riavvio.

I valori da portare sono quelli dell'ultima fermata con il vecchio package caricato
(``ultima_con_il_package``): durante il primo avvio nativo il package gira ancora (le sue
automazioni cambiano dei valori) e la riparazione rilegge i valori alla conferma.
"""

from __future__ import annotations

import importlib.util
import math
import re
from collections import Counter
from collections.abc import Iterable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

import istantanea
import utente

RADICE = Path(__file__).resolve().parents[2]
NOMI = tuple(v.nome for v in utente.CASA)
TOLLERANZA_TIMER = 2.0
"""Secondi: un timer «ripreso» finisce allo stesso istante di prima entro questo scarto
(arrotondamento al secondo dell'avvio dei timer di Home Assistant e del salvataggio)."""

DOMINI_AIUTANTI = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
)
DOMINI_SENSORI = ("sensor", "binary_sensor")
_SUFFISSO = re.compile(r"^(.*)_(\d+)$")


def _tabelle() -> Any:
    """``nativa/tabelle.py`` di questo repository (la colonna «Domani» approvata), letto
    da solo senza importare l'integrazione."""
    percorso = RADICE / "custom_components/vmc_master/nativa/tabelle.py"
    spec = importlib.util.spec_from_file_location("tabelle_copia", percorso)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


TABELLE = _tabelle()
DOMANI: dict[str, str] = TABELLE.DOMANI
IMPOSTAZIONI: dict[str, dict[str, Any]] = TABELLE.IMPOSTAZIONI
SENSORI: dict[str, dict[str, Any]] = TABELLE.SENSORI
INTERNI = tuple(
    k
    for k in IMPOSTAZIONI
    if k.split(".")[0] in DOMINI_AIUTANTI and DOMANI[k] == "interna"
)
VISIBILI = tuple(
    k
    for k in IMPOSTAZIONI
    if k.split(".")[0] in DOMINI_AIUTANTI and DOMANI[k] != "interna"
)
TIMER = tuple(k for k in IMPOSTAZIONI if k.startswith("timer."))


# ------------------------------------------------------------------ aiuti
def vmc_di(entity_id: str) -> str | None:
    """Il nome della VMC a cui appartiene un'entità (``vmc_<nome>_...`` o
    ``automation.automazione_vmc_<nome>``), o None."""
    oggetto = entity_id.split(".", 1)[1]
    for nome in NOMI:
        if oggetto.startswith(f"vmc_{nome}_") or oggetto == f"automazione_vmc_{nome}":
            return nome
    return None


def vecchio_id(chiave: str, nome: str) -> str:
    dominio, oggetto = chiave.split(".", 1)
    return f"{dominio}.vmc_{nome}_{oggetto}"


def nuovo_id(chiave: str, nome: str) -> str:
    return f"{DOMANI[chiave]}.vmc_{nome}_{chiave.split('.', 1)[1]}"


def controllo(
    nome: str,
    esito: str,
    spiegazione: str,
    conteggi: Mapping[str, Any] | None = None,
    dettagli: Iterable[Any] = (),
) -> dict[str, Any]:
    return {
        "nome": nome,
        "esito": esito,
        "spiegazione": spiegazione,
        "conteggi": dict(conteggi or {}),
        "dettagli": list(dettagli)[:400],
    }


def non_eseguibile(nome: str, manca: str) -> dict[str, Any]:
    return controllo(nome, "non eseguibile", f"manca {manca}")


def tutti_passati(controlli: list[dict[str, Any]]) -> bool:
    return all(c["esito"] in ("passato", "informazione") for c in controlli)


def ripristinati(ferma: Mapping[str, Any] | None) -> dict[str, dict[str, Any]]:
    """Gli stati salvati alla fermata (``core.restore_state``) per entity_id."""
    if not ferma:
        return {}
    dati = (ferma.get("storage") or {}).get("core.restore_state") or {}
    return {
        voce["state"]["entity_id"]: voce["state"]
        for voce in dati.get("data") or []
        if isinstance(voce, dict) and "state" in voce
    }


def ultima_con_il_package(
    fc: Mapping[str, Any] | None, fp: Mapping[str, Any] | None
) -> Mapping[str, Any] | None:
    """L'ultima fermata con il vecchio package ancora caricato: quella dopo la conferma
    (il package gira fino a quel riavvio e la riparazione rilegge i valori alla conferma)
    se ha ancora gli aiutanti della beta, altrimenti quella della beta prima del
    passaggio."""
    if fc and any(
        e.split(".")[0] in DOMINI_AIUTANTI and vmc_di(e) for e in ripristinati(fc)
    ):
        return fc
    return fp


def controlla_valori_cambiati(
    fp: Mapping[str, Any] | None, ultima: Mapping[str, Any] | None
) -> dict[str, Any]:
    """Quanti valori della beta cambiano fra la fermata della beta e l'ultima fermata con
    il package caricato (il primo avvio nativo, con il package che gira ancora)."""
    nome = "valori cambiati durante il primo avvio nativo (informazione)"
    if not fp or not ultima or ultima is fp:
        return non_eseguibile(
            nome, "una fermata con il package dopo il primo avvio nativo"
        )
    prima, dopo = ripristinati(fp), ripristinati(ultima)
    cambiati = [
        f"{e}: {prima[e]['state']!r} → {dopo[e]['state']!r}"
        for e in sorted(prima)
        if vmc_di(e)
        and e.split(".")[0] in DOMINI_AIUTANTI
        and e in dopo
        and not uguali(prima[e]["state"], dopo[e]["state"])
    ]
    return controllo(
        nome,
        "informazione",
        "Il vecchio package resta caricato durante il primo avvio nativo e le sue "
        "automazioni continuano: i valori da portare sono quelli dell'ultima fermata con il "
        "package (dopo la conferma), non quelli di prima del passaggio.",
        {"aiutanti cambiati": len(cambiati)},
        cambiati,
    )


def _numero(testo: Any) -> float | None:
    try:
        valore = float(testo)
    except (TypeError, ValueError):
        return None
    return valore if math.isfinite(valore) else None


def uguali(a: Any, b: Any) -> bool:
    """Due valori uguali come valori di Home Assistant (numeri come numeri; acceso /
    spento anche come True / False)."""
    if isinstance(a, bool) or isinstance(b, bool):
        a = {True: "on", False: "off"}.get(a, a) if isinstance(a, bool) else a
        b = {True: "on", False: "off"}.get(b, b) if isinstance(b, bool) else b
    if a == b:
        return True
    na, nb = _numero(a), _numero(b)
    if na is not None and nb is not None:
        return abs(na - nb) < 1e-9
    return str(a) == str(b)


def _stato(istant: Mapping[str, Any] | None, entity_id: str) -> str | None:
    if not istant:
        return None
    voce = istant["stati"].get(entity_id)
    return None if voce is None else voce["state"]


def _iniziale(chiave: str) -> Any:
    """Il valore di ``initial`` dell'aiutante (None se non c'è): dopo un riavvio Home
    Assistant riparte da lì."""
    voce = IMPOSTAZIONI.get(chiave) or {}
    if "initial" not in voce:
        return None
    valore = voce["initial"]
    if chiave.startswith("input_boolean."):
        return "on" if valore else "off"
    return valore


# -------------------------------------------------------------- controlli
def controlla_avvio_beta(p0: Mapping[str, Any] | None) -> dict[str, Any]:
    nome = "beta avviata con le 3 VMC"
    if not p0:
        return non_eseguibile(nome, "l'istantanea P0_prima")
    per_vmc = Counter(vmc_di(e) for e in p0["stati"])
    conteggi = {f"entità {n}": per_vmc.get(n, 0) for n in NOMI}
    ok = all(per_vmc.get(n, 0) > 400 for n in NOMI)
    return controllo(
        nome,
        "passato" if ok else "fallito",
        "Entità di ogni VMC con la beta accesa (package b41).",
        conteggi,
    )


def controlla_primo_avvio(
    esito: Mapping[str, Any], m: Mapping[str, Any] | None
) -> dict[str, Any]:
    nome = "primo avvio con il codice nativo"
    if not m:
        return controllo(
            nome,
            "fallito",
            f"Home Assistant non arriva al primo avvio: {esito.get('errore', '?')}",
        )
    voci = {v["title"]: v["state"] for v in m.get("voci") or []}
    caricate = sum(1 for s in voci.values() if s == "loaded")
    per_dominio = Counter(e.split(".")[0] for e in m["stati"] if vmc_di(e) is not None)
    return controllo(
        nome,
        "passato" if caricate == len(NOMI) else "fallito",
        "Le voci di VMC Master avviate (stato «loaded») al primo avvio nativo, con il "
        "vecchio package ancora in /config/packages.",
        {
            "voci caricate": f"{caricate}/{len(NOMI)}",
            **{f"entità {d}": n for d, n in sorted(per_dominio.items())},
        },
        [f"{t}: {s}" for t, s in voci.items()],
    )


def controlla_riparazione(esito: Mapping[str, Any]) -> dict[str, Any]:
    nome = "riparazione da confermare"
    trovate = esito.get("riparazioni_da_confermare")
    if trovate is None:
        return non_eseguibile(nome, "il primo avvio nativo")
    if not trovate:
        return controllo(
            nome,
            "fallito",
            esito.get("primo_passo_mancante")
            or "Nessuna riparazione di VMC Master da confermare dopo il primo avvio nativo.",
            {"riparazioni": 0},
        )
    seguite = esito.get("riparazioni_seguite") or []
    return controllo(
        nome,
        "passato",
        "Riparazioni di VMC Master da confermare e passi seguiti dall'utente.",
        {
            "riparazioni": len(trovate),
            "riavvio dopo la conferma": esito.get("riavvio_dopo_la_conferma"),
        },
        [
            {
                "issue_id": s["issue_id"],
                "passi": [(p["tipo"], p["passo"], p["segnaposto"]) for p in s["passi"]],
            }
            for s in seguite
        ],
    )


def sensori_della_vmc(istant: Mapping[str, Any]) -> list[str]:
    return sorted(
        e for e in istant["stati"] if e.split(".")[0] in DOMINI_SENSORI and vmc_di(e)
    )


def controlla_sensori(
    p: Mapping[str, Any] | None, a: Mapping[str, Any] | None
) -> dict[str, Any]:
    nome = "sensori con gli stessi entity_id"
    if not p or not a:
        return non_eseguibile(nome, "l'istantanea A_dopo" if p else "l'istantanea P")
    prima = sensori_della_vmc(p)
    mancanti = [e for e in prima if e not in a["stati"]]
    non_disponibili = [
        e for e in prima if e in a["stati"] and a["stati"][e]["state"] == "unavailable"
    ]
    nativi = [
        e for e in mancanti if e.split(".", 1)[1].split("_", 2)[2] in _oggetti_sensori()
    ]
    conteggi = {
        "sensori prima": len(prima),
        "presenti dopo": len(prima) - len(mancanti),
        "mancanti": len(mancanti),
        "mancanti che la nativa dovrebbe avere": len(nativi),
        "presenti ma non disponibili": len(non_disponibili),
    }
    return controllo(
        nome,
        "passato" if not mancanti else "fallito",
        "Ogni sensore e sensore binario delle VMC di prima c'è dopo con lo stesso "
        "entity_id (i sensori binari di oggi; le spie input_boolean → binary_sensor sono "
        "nel controllo delle impostazioni).",
        conteggi,
        [f"mancante: {e}" for e in mancanti]
        + [f"non disponibile: {e}" for e in non_disponibili],
    )


def _oggetti_sensori() -> set[str]:
    return {k.split(".", 1)[1] for k in SENSORI}


def doppioni(stati: Iterable[str]) -> list[str]:
    """Entità delle VMC con «_2», «_3»... alla fine quando la stessa senza c'è o c'era."""
    insieme = set(stati)
    uscita = []
    for e in sorted(insieme):
        trovato = _SUFFISSO.match(e)
        if (
            trovato
            and vmc_di(e)
            and e not in _ID_LEGITTIMI
            and trovato.group(1) in insieme | _ID_ATTESI
        ):
            uscita.append(e)
    return uscita


_ID_ATTESI: set[str] = {nuovo_id(k, n) for k in (*VISIBILI, *TIMER) for n in NOMI} | {
    f"{k.split('.')[0]}.vmc_{n}_{k.split('.', 1)[1]}" for k in SENSORI for n in NOMI
}
_ID_LEGITTIMI: set[str] = (
    _ID_ATTESI
    | {nuovo_id(k, n) for k in DOMANI if DOMANI[k] != "interna" for n in NOMI}
    | {vecchio_id(k, n) for k in DOMANI for n in NOMI}
)
"""Gli entity_id che finiscono con «_2» per nome (la seconda fascia del Calendario:
``accensione_lunedi_2``...): non sono doppioni."""


def controlla_doppioni(
    a: Mapping[str, Any] | None, momento: str = "A_dopo"
) -> dict[str, Any]:
    nome = f"nessun entity_id con «_2» ({momento})"
    if not a:
        return non_eseguibile(nome, f"l'istantanea {momento}")
    negli_stati = doppioni(a["stati"])
    nel_registro = doppioni(v["entity_id"] for v in a["registro"])
    return controllo(
        nome,
        "passato" if not negli_stati and not nel_registro else "fallito",
        "Home Assistant aggiunge «_2» quando un entity_id è ancora occupato da una "
        "voce del registro: i vecchi devono essere liberati prima che nascano i nativi.",
        {"negli stati": len(negli_stati), "nel registro": len(nel_registro)},
        sorted(set(negli_stati) | set(nel_registro)),
    )


def controlla_storico(
    fp: Mapping[str, Any] | None,
    fa: Mapping[str, Any] | None,
    p: Mapping[str, Any] | None,
) -> dict[str, Any]:
    nome = "storico dei sensori continuo (states_meta riusati)"
    if not fp or not fa or not p:
        return non_eseguibile(nome, "le istantanee FP_fermata_beta e FA_fermata_finale")
    prima = fp["registro_storico"].get("states_meta", {})
    dopo = fa["registro_storico"].get("states_meta", {})
    righe_prima = fp["registro_storico"].get("righe", {})
    righe_dopo = fa["registro_storico"].get("righe", {})
    sensori = [e for e in sensori_della_vmc(p) if e in prima]
    riusati, cambiati, senza_righe_nuove = [], [], []
    for e in sensori:
        if dopo.get(e) != prima[e]:
            cambiati.append(f"{e}: {prima[e]} → {dopo.get(e)}")
            continue
        riusati.append(e)
        r0 = (righe_prima.get(str(prima[e])) or {}).get("righe", 0)
        r1 = (righe_dopo.get(str(prima[e])) or {}).get("righe", 0)
        if r1 <= r0:
            senza_righe_nuove.append(f"{e}: {r0} → {r1} righe")
    nuovi_doppioni = doppioni(e for e in dopo if e not in prima)
    totale_righe = sum(
        (righe_prima.get(str(prima[e])) or {}).get("righe", 0) for e in sensori
    )
    return controllo(
        nome,
        "passato" if not cambiati and not nuovi_doppioni else "fallito",
        "Per ogni sensore con storico prima del passaggio, la riga di states_meta "
        "(entity_id → metadata_id) è la stessa dopo e le righe nuove si aggiungono a "
        "quelle di prima.",
        {
            "sensori con storico prima": len(sensori),
            "righe di storico prima (questi sensori)": totale_righe,
            "metadata_id riusati": len(riusati),
            "metadata_id cambiati o persi": len(cambiati),
            "riusati senza righe nuove dopo": len(senza_righe_nuove),
            "nuove righe states_meta con «_2»": len(nuovi_doppioni),
        },
        cambiati + nuovi_doppioni + senza_righe_nuove,
    )


def controlla_statistiche(
    fp: Mapping[str, Any] | None,
    fa: Mapping[str, Any] | None,
    a: Mapping[str, Any] | None,
) -> dict[str, Any]:
    nome = "statistiche a lungo termine continue"
    if not fp or not fa:
        return non_eseguibile(nome, "le istantanee FP_fermata_beta e FA_fermata_finale")
    prima = {
        k: v
        for k, v in fp["registro_storico"].get("statistics_meta", {}).items()
        if vmc_di(k)
    }
    dopo = fa["registro_storico"].get("statistics_meta", {})
    diversi = [
        f"{k}: {v} → {dopo.get(k)}"
        for k, v in prima.items()
        if (dopo.get(k) or {}).get("id") != v["id"]
        or (dopo.get(k) or {}).get("unita") != v["unita"]
    ]
    nuovi = sorted(k for k in dopo if vmc_di(k) and k not in prima)
    problemi_registro = [
        f"{r['domain']}.{r['issue_id']}"
        for r in (a or {}).get("riparazioni") or []
        if r["domain"] in ("sensor", "recorder")
    ]
    return controllo(
        nome,
        "passato" if not diversi and not problemi_registro else "fallito",
        "statistics_meta delle VMC: stesso id e stessa unità; nessuna riparazione del "
        "registro (unità o state_class cambiate).",
        {
            "statistiche prima": len(prima),
            "uguali dopo": len(prima) - len(diversi),
            "diverse o perse": len(diversi),
            "nuove dopo": len(nuovi),
            "riparazioni sensor/recorder": len(problemi_registro),
        },
        diversi + [f"nuova: {k}" for k in nuovi] + problemi_registro,
    )


def controlla_impostazioni(
    p0: Mapping[str, Any] | None,
    r: Mapping[str, Any] | None,
    p: Mapping[str, Any] | None,
    ultima: Mapping[str, Any] | None,
    a: Mapping[str, Any] | None,
    scritte: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Ogni impostazione visibile (173 per VMC) nel suo nuovo dominio con il valore
    dell'ultima fermata con il vecchio package caricato (``ultima_con_il_package``)."""
    nome = "impostazioni visibili portate nel nuovo dominio"
    if not (p0 and r and p and a):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    salvati = ripristinati(ultima)
    esiti: Counter[str] = Counter()
    dettagli = []
    scritte_ok = scritte_tot = 0
    opzioni_diverse = []
    for chiave in VISIBILI:
        for n in NOMI:
            vecchio, nuovo = vecchio_id(chiave, n), nuovo_id(chiave, n)
            valore_p = (salvati.get(vecchio) or {}).get("state", _stato(p, vecchio))
            valore_a = _stato(a, nuovo)
            cambia_col_riavvio = _stato(p0, vecchio) != _stato(r, vecchio)
            iniziale = _iniziale(chiave)
            if valore_a is None:
                classe = "manca"
            elif uguali(valore_p, valore_a):
                classe = "portato"
            elif uguali(valore_a, _stato(r, vecchio)) or (
                cambia_col_riavvio
                and iniziale is not None
                and uguali(valore_a, iniziale)
            ):
                classe = "come dopo un riavvio della beta"
            elif iniziale is not None and uguali(valore_a, iniziale):
                classe = "valore iniziale (initial)"
            else:
                classe = "diverso"
            esiti[classe] += 1
            if classe not in ("portato",):
                dettagli.append(
                    f"{classe}: {vecchio} = {valore_p!r} → {nuovo} = {valore_a!r}"
                )
            if (
                scritte
                and vecchio in scritte
                and scritte[vecchio] != "toggle"
                and iniziale is None
            ):
                scritte_tot += 1
                scritte_ok += classe == "portato"
            if chiave.startswith("input_select.") and valore_a is not None:
                prima_opz = ((salvati.get(vecchio) or {}).get("attributes") or {}).get(
                    "options"
                ) or p["stati"].get(vecchio, {}).get("attributes", {}).get("options")
                dopo_opz = a["stati"][nuovo]["attributes"].get("options")
                if prima_opz != dopo_opz:
                    opzioni_diverse.append(
                        f"opzioni di {nuovo}: {prima_opz} → {dopo_opz}"
                    )
    ok = esiti["manca"] == 0 and esiti["diverso"] == 0 and not opzioni_diverse
    conteggi = {
        "impostazioni (per 3 VMC)": len(VISIBILI) * len(NOMI),
        **{k: v for k, v in sorted(esiti.items())},
        "scritte dall'utente (senza initial) portate": f"{scritte_ok}/{scritte_tot}",
        "select con opzioni diverse": len(opzioni_diverse),
    }
    return controllo(
        nome,
        "passato" if ok else "fallito",
        "Valore di ogni impostazione visibile all'ultima fermata con il vecchio package "
        "caricato (core.restore_state) contro il valore dell'entità nativa dopo il "
        "passaggio. «come dopo un riavvio della beta»: il nativo ha lo stesso valore che "
        "la beta ha allo stesso momento dopo il riavvio di controllo senza passaggio (R, "
        "preso come A a VMC avviate più 15 s: initial, automazioni dell'avvio, fasi del "
        "riallineamento al riavvio).",
        conteggi,
        dettagli + opzioni_diverse,
    )


MEMORIE = tuple(k for k, v in SENSORI.items() if v.get("tipo") == "memoria")
"""I sensori con memoria (template a trigger di oggi: velocità e nome memorizzati,
medie settimanali, giorni di dati del rischio muffa): stesso entity_id dopo, e il valore
deve restare."""


def controlla_memorie(
    p0: Mapping[str, Any] | None,
    r: Mapping[str, Any] | None,
    ultima: Mapping[str, Any] | None,
    a: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """I sensori con memoria: valore all'ultima fermata con il vecchio package
    (core.restore_state) contro lo stato dopo il passaggio."""
    nome = f"{len(MEMORIE)} sensori con memoria con lo stesso valore"
    if not (p0 and r and a):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    salvati = ripristinati(ultima)
    esiti: Counter[str] = Counter()
    dettagli = []
    for n in NOMI:
        for chiave in MEMORIE:
            entita = vecchio_id(chiave, n)
            valore_p = (salvati.get(entita) or {}).get("state", _stato(p0, entita))
            valore_a = _stato(a, entita)
            if valore_a is None:
                classe = "manca"
            elif uguali(valore_p, valore_a):
                classe = "portato"
            elif uguali(valore_a, _stato(r, entita)):
                classe = "come dopo un riavvio della beta"
            else:
                classe = "diverso"
            esiti[classe] += 1
            if classe != "portato":
                dettagli.append(f"{classe}: {entita} = {valore_p!r} → {valore_a!r}")
    return controllo(
        nome,
        "passato" if not esiti["manca"] and not esiti["diverso"] else "fallito",
        "Valore di ogni sensore con memoria all'ultima fermata con il vecchio package "
        "(core.restore_state) contro lo stato dopo il passaggio.",
        {
            f"sensori ({len(MEMORIE)} per 3 VMC)": len(MEMORIE) * len(NOMI),
            **dict(sorted(esiti.items())),
        },
        dettagli,
    )


def memoria_nativa(ferma: Mapping[str, Any] | None, nome: str) -> dict[str, Any] | None:
    """I valori interni salvati dal motore nativo (``vmc_master.memoria_interna.<nome>``)."""
    if not ferma:
        return None
    dati = (ferma.get("storage") or {}).get(f"vmc_master.memoria_interna.{nome}")
    if not dati:
        return None
    return (dati.get("data") or {}).get("valori")


def _testi_delle_attese() -> dict[str, frozenset[str]]:
    """I testi che l'automazione delle attese della beta scrive in
    input_text.countdown_‹attesa› (id dei trigger «ON|‹attesa›|‹attesa›|‹testo›» del
    package). Dopo ogni riavvio li riscrive quando il riallineamento arriva alla fase 2
    (circa 90 s dopo l'avvio, condizione «fase == 0 o >= 2» dei trigger): per esempio
    «Black-Out Velocità 2 terminato, ripristino» con la VMC in linea a velocità 2."""
    testo = (RADICE / "custom_components/vmc_master/package/vmc_master.yaml").read_text(
        encoding="utf-8"
    )
    testi: dict[str, set[str]] = {}
    for attesa, _uguale, scritto in re.findall(
        r'id: "(?:ON|OFF)\|(\w+)\|(\w+)\|([^"]*)"', testo
    ):
        testi.setdefault(attesa, set()).add(scritto)
    return {attesa: frozenset(t) for attesa, t in testi.items()}


TESTI_DELLE_ATTESE = _testi_delle_attese()


def controlla_interni(
    p0: Mapping[str, Any] | None,
    r: Mapping[str, Any] | None,
    ultima: Mapping[str, Any] | None,
    fa: Mapping[str, Any] | None,
    confermata: bool = True,
) -> dict[str, Any]:
    """I 68 valori interni per VMC nella memoria del motore alla fermata finale, contro
    l'ultima fermata con il vecchio package caricato."""
    nome = "68 valori interni nella memoria del motore"
    if not confermata:
        return non_eseguibile(nome, "la conferma della riparazione")
    if not (ultima and fa):
        return non_eseguibile(nome, "l'istantanea FA_fermata_finale")
    salvati = ripristinati(ultima)
    esiti: Counter[str] = Counter()
    dettagli = []
    non_predefiniti = 0
    for n in NOMI:
        memoria = memoria_nativa(fa, n)
        for chiave in INTERNI:
            vecchio = vecchio_id(chiave, n)
            valore_p = (salvati.get(vecchio) or {}).get("state")
            if valore_p is not None and not uguali(valore_p, _predefinito(chiave)):
                non_predefiniti += 1
            if memoria is None or chiave not in memoria:
                classe = "manca"
                valore_a = None
            else:
                valore_a = memoria[chiave]
                cambia_col_riavvio = _stato(p0, vecchio) != _stato(r, vecchio)
                if uguali(valore_p, valore_a):
                    classe = "portato"
                elif chiave.startswith("input_number.aria_scambiata") and (
                    (_numero(valore_a) or 0) >= (_numero(valore_p) or 0)
                ):
                    classe = "contatore cresciuto (la VMC gira)"
                elif cambia_col_riavvio:
                    classe = "cambia anche con un riavvio della beta"
                elif chiave.startswith("input_text.countdown_") and valore_a in (
                    TESTI_DELLE_ATTESE.get(
                        chiave.removeprefix("input_text.countdown_"), ()
                    )
                ):
                    # la beta fa lo stesso dopo un riavvio, ma più tardi dell'istantanea
                    # R (fase 2 del riallineamento): vedere _testi_delle_attese
                    classe = "testo di un'attesa, riscritto dal motore come dalla beta dopo un riavvio"
                else:
                    classe = "diverso"
            esiti[classe] += 1
            if classe != "portato":
                dettagli.append(f"{classe}: {vecchio} = {valore_p!r} → {valore_a!r}")
    ok = esiti["manca"] == 0 and esiti["diverso"] == 0
    return controllo(
        nome,
        "passato" if ok else "fallito",
        "Ultimo valore di ogni aiutante interno all'ultima fermata con il vecchio package "
        "caricato (core.restore_state) contro la memoria del motore salvata alla fermata "
        "finale (.storage/vmc_master.memoria_interna.<nome>). «contatore cresciuto»: i "
        "contatori dell'aria scambiata crescono finché la VMC gira. «testo di un'attesa»: "
        "input_text.countdown_‹attesa› con un testo che l'automazione delle attese scrive "
        "dopo ogni riavvio (fase 2 del riallineamento, dopo l'istantanea R).",
        {
            "valori (68 per 3 VMC)": len(INTERNI) * len(NOMI),
            "diversi dal valore iniziale prima del passaggio": non_predefiniti,
            **dict(sorted(esiti.items())),
        },
        dettagli,
    )


def _predefinito(chiave: str) -> Any:
    voce = IMPOSTAZIONI.get(chiave) or {}
    if "initial" in voce:
        return _iniziale(chiave)
    dominio = chiave.split(".")[0]
    if dominio == "input_number":
        return float(voce.get("min", 0))
    if dominio == "input_boolean":
        return "off"
    return ""


def _fine(valore: Any) -> float | None:
    if not isinstance(valore, str) or valore in ("unknown", "unavailable", ""):
        return None
    try:
        return datetime.fromisoformat(valore).timestamp()
    except ValueError:
        return None


def _fine_timer(
    istant: Mapping[str, Any] | None, entity_id: str
) -> tuple[str, float | None]:
    voce = (istant or {}).get("stati", {}).get(entity_id)
    if voce is None:
        return "assente", None
    if entity_id.startswith("timer."):
        if voce["state"] != "active":
            return voce["state"], None
        return "active", _fine(voce["attributes"].get("finishes_at"))
    fine = _fine(voce["state"])
    return ("active" if fine is not None else voce["state"]), fine


def classe_timer(fine_prima: float | None, stato: str, fine: float | None) -> str:
    if stato == "assente":
        return "assente"
    if fine is None:
        return "fermo"
    if fine_prima is not None and abs(fine - fine_prima) <= TOLLERANZA_TIMER:
        return "ripreso (stessa fine)"
    if fine_prima is not None and fine_prima <= fine:
        return "ripartito (fine più tardi)"
    return "ripartito"


def controlla_timer(
    p0: Mapping[str, Any] | None,
    r: Mapping[str, Any] | None,
    p: Mapping[str, Any] | None,
    a: Mapping[str, Any] | None,
) -> dict[str, Any]:
    nome = "timer: conti alla rovescia dopo il passaggio"
    if not (p0 and r and p and a):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    attivi_p = attivi_p0 = assenti = 0
    dopo_riavvio: Counter[str] = Counter()
    dopo_passaggio: Counter[str] = Counter()
    dettagli = []
    for chiave in TIMER:
        for n in NOMI:
            vecchio = vecchio_id(chiave, n)
            nuovo = nuovo_id(chiave, n)
            _s0, fine_p0 = _fine_timer(p0, vecchio)
            stato_r, fine_r = _fine_timer(r, vecchio)
            _sp, fine_p = _fine_timer(p, vecchio)
            stato_a, fine_a = _fine_timer(a, nuovo)
            if stato_a == "assente":
                assenti += 1
                dettagli.append(f"assente dopo il passaggio: {nuovo}")
            if fine_p0 is not None:
                attivi_p0 += 1
                dopo_riavvio[classe_timer(fine_p0, stato_r, fine_r)] += 1
            if fine_p is not None:
                attivi_p += 1
                classe = classe_timer(fine_p, stato_a, fine_a)
                dopo_passaggio[classe] += 1
                resto_p = fine_p - p["ora"]
                resto_a = (fine_a - a["ora"]) if fine_a is not None else None
                dettagli.append(
                    f"{vecchio}: mancavano {resto_p:.0f} s → {nuovo}: {classe}"
                    + (f", mancano {resto_a:.0f} s" if resto_a is not None else "")
                )
    # Home Assistant è l'oracolo: dopo il passaggio ogni timer attivo finisce come dopo
    # il riavvio di controllo della beta (nessun timer del package ha «restore»: fermo)
    come_un_riavvio = set(dopo_passaggio) <= set(dopo_riavvio)
    ok = assenti == 0 and come_un_riavvio and attivi_p > 0
    return controllo(
        nome,
        "passato" if ok else "fallito",
        "Timer attivi prima del passaggio e cosa ne resta dopo, contro quello che fa un "
        "riavvio della beta (riavvio di controllo). Nel package nessun timer ha «restore: "
        "true»: Home Assistant li riporta tutti fermi a ogni riavvio, e il passaggio non li "
        "porta (passaggio.py). Passato: ogni timer c'è dopo nel nuovo dominio e ogni timer "
        "attivo prima finisce come dopo il riavvio di controllo. Tolleranza «stessa fine»: "
        f"{TOLLERANZA_TIMER:.0f} s.",
        {
            f"timer (34 per {len(NOMI)} VMC)": len(TIMER) * len(NOMI),
            "assenti dopo il passaggio": assenti,
            "attivi prima del riavvio di controllo": attivi_p0,
            **{
                f"dopo un riavvio della beta: {k}": v
                for k, v in sorted(dopo_riavvio.items())
            },
            "attivi prima del passaggio": attivi_p,
            **{f"dopo il passaggio: {k}": v for k, v in sorted(dopo_passaggio.items())},
        },
        dettagli,
    )


def controlla_file(
    fp: Mapping[str, Any] | None,
    m_file: Mapping[str, Any] | None,
    fa: Mapping[str, Any] | None,
    confermata: bool = True,
    f0: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    uscita = []
    nome = "niente più in /config/packages/vmc_helty_flow"
    if not confermata:
        uscita.append(non_eseguibile(nome, "la conferma della riparazione"))
    elif not fa:
        uscita.append(non_eseguibile(nome, "l'istantanea FA_fermata_finale"))
    else:
        rimasti = sorted(
            f for f in fa["file"]["packages"] if f.startswith("vmc_helty_flow/")
        )
        prima = sorted(
            f
            for f in (fp or {}).get("file", {}).get("packages", {})
            if f.startswith("vmc_helty_flow/")
        )
        uscita.append(
            controllo(
                nome,
                "passato" if not rimasti else "fallito",
                "File del vecchio package rimasti dopo la conferma e il riavvio.",
                {"file prima": len(prima), "file dopo": len(rimasti)},
                rimasti,
            )
        )
    nome = "niente scritto in /config/vmc_master_backup"
    if not fa:
        uscita.append(non_eseguibile(nome, "l'istantanea FA_fermata_finale"))
    else:
        scritti = sorted(fa["file"]["vmc_master_backup"])
        uscita.append(
            controllo(
                nome,
                "passato" if not scritti else "fallito",
                "La cartella dei backup della beta non deve comparire.",
                {"file": len(scritti)},
                scritti,
            )
        )
    nome = "fermata della beta per l'aggiornamento senza scritture in packages e www"
    if not (f0 and fp):
        uscita.append(non_eseguibile(nome, "le istantanee F0 e FP"))
    else:
        diversi = file_diversi(f0, fp)
        uscita.append(
            controllo(
                nome,
                "passato" if not diversi else "fallito",
                "Con il codice nativo già al posto della beta (download dal Marketplace), la "
                "beta ancora accesa si ferma per il riavvio: i file di /config/packages e "
                "/config/www restano quelli della fermata di controllo (F0).",
                {
                    "file nuovi, tolti o cambiati": len(diversi),
                    **{
                        f"in /config/{c}": sum(f": {c}/" in d for d in diversi)
                        for c in ("packages", "www")
                    },
                },
                diversi,
            )
        )
    nome = "primo avvio nativo senza scritture in /config/packages e /config/www"
    if not (fp and m_file):
        uscita.append(non_eseguibile(nome, "l'istantanea M_file"))
    else:
        diversi = file_diversi(fp, m_file)
        uscita.append(
            controllo(
                nome,
                "passato" if not diversi else "fallito",
                "Al primo avvio l'integrazione legge le vecchie impostazioni e le salva nei "
                "propri dati, senza scrivere in /config (piano, passo 2).",
                {
                    "file nuovi, tolti o cambiati": len(diversi),
                    **{
                        f"in /config/{c}": sum(f": {c}/" in d for d in diversi)
                        for c in ("packages", "www")
                    },
                },
                diversi,
            )
        )
    return uscita


def file_diversi(prima: Mapping[str, Any], dopo: Mapping[str, Any]) -> list[str]:
    """I file di /config/packages e /config/www nuovi, tolti o cambiati fra due istantanee."""
    diversi = []
    for cartella in ("packages", "www"):
        a, b = prima["file"][cartella], dopo["file"][cartella]
        for f in sorted(set(a) | set(b)):
            if a.get(f) != b.get(f):
                stato = "nuovo" if f not in a else "tolto" if f not in b else "cambiato"
                diversi.append(f"{stato}: {cartella}/{f}")
    return diversi


def controlla_scheda(
    p: Mapping[str, Any] | None,
    a: Mapping[str, Any] | None,
    fotografie: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    uscita = []
    nome = "risorsa della scheda e plancia"
    if not (p and a):
        uscita.append(non_eseguibile(nome, "l'istantanea A_dopo"))
    else:
        nostre = [
            r
            for r in a["risorse"]
            if str(r.get("url", "")).split("?")[0].endswith("vmc-master-card.js")
        ]
        stessa_plancia = a.get("plancia") == p.get("plancia")
        uscita.append(
            controllo(
                nome,
                "passato" if len(nostre) == 1 and stessa_plancia else "fallito",
                "Una sola risorsa «module» della scheda nelle risorse delle plance; la "
                "configurazione della plancia è la stessa di prima (la scheda si aggiorna da sola).",
                {
                    "risorse della scheda prima": sum(
                        1
                        for r in p["risorse"]
                        if "vmc-master-card.js" in str(r.get("url"))
                    ),
                    "risorse della scheda dopo": len(nostre),
                    "plancia uguale": stessa_plancia,
                },
                [f"prima: {r.get('url')}" for r in p["risorse"]]
                + [f"dopo: {r.get('url')}" for r in a["risorse"]],
            )
        )
    uscita.append(
        controlla_fotografie(
            "scheda di ogni VMC senza «Entità non disponibile»", fotografie
        )
    )
    return uscita


ALTEZZA_MINIMA = 500
"""Pixel: sotto, la scheda non si è disegnata (solo l'intestazione o un errore)."""


def controlla_fotografie(
    nome: str, fotografie: list[dict[str, Any]] | None, decide: bool = True
) -> dict[str, Any]:
    """Le viste della plancia fotografate da scatta.js: per ogni vista di una VMC nessun
    avviso della plancia, nessuna scheda in errore, nessun messaggio «non disponibile»,
    una scheda VMC Master disegnata. ``decide`` False: solo un'informazione (la beta
    dopo un riavvio, per confronto)."""
    if not fotografie:
        return non_eseguibile(nome, "le fotografie")
    conteggi: dict[str, Any] = {}
    dettagli = []
    ok = True
    for foto in fotografie:
        if "vista" not in foto:
            ok = False
            dettagli.append(f"errore del browser: {foto.get('errore', '')[:300]}")
            continue
        vista = foto["vista"]
        avvisi = (
            len(foto["avvisi"]) + len(foto["errori"]) + len(foto["messaggi_scheda"])
        )
        if vista.startswith("vmc-"):
            conteggi[f"{vista}: avvisi"] = avvisi
            conteggi[f"{vista}: altezza px"] = foto["altezza"]
            ok = (
                ok
                and avvisi == 0
                and foto["schede_vmc"] == 1
                and foto["altezza"] > ALTEZZA_MINIMA
            )
        else:
            conteggi[f"{vista} (scheda dell'utente, informazione): avvisi"] = avvisi
        dettagli += [
            f"{vista}: {t}"
            for t in foto["avvisi"] + foto["errori"] + foto["messaggi_scheda"]
        ]
        dettagli += [
            f"{vista}: indirizzo esterno bloccato dal banco: {b}"
            for b in foto.get("bloccati") or []
        ]
    return controllo(
        nome,
        ("passato" if ok else "fallito") if decide else "informazione",
        "Ogni vista della plancia aperta in Chromium (Playwright, larghezza 480, "
        "deviceScaleFactor 1): avvisi della plancia (hui-warning, «Entità non "
        "disponibile»), schede in errore (hui-error-card) e messaggio «Scheda VMC Master "
        f"non disponibile»; la scheda VMC Master disegnata (più di {ALTEZZA_MINIMA} px). "
        "La vista «personale» (scheda entità scritta dall'utente con i nomi di oggi) è "
        "solo un'informazione. Il banco non ha rete: gli indirizzi esterni (immagini) "
        "falliscono e sono elencati.",
        conteggi,
        dettagli,
    )


DOMINI_VECCHI = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
    "timer",
    "script",
)


def controlla_vecchie(
    a: Mapping[str, Any] | None, p: Mapping[str, Any] | None
) -> dict[str, Any]:
    nome = "vecchie entità tolte (stati e registro)"
    if not (a and p):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    negli_stati = sorted(
        e for e in a["stati"] if vmc_di(e) and e.split(".")[0] in DOMINI_VECCHI
    )
    vecchie_piattaforme = Counter(
        v["platform"]
        for v in a["registro"]
        if vmc_di(v["entity_id"]) and v["platform"] not in ("vmc_master", "automation")
    )
    prima = Counter(v["platform"] for v in p["registro"] if vmc_di(v["entity_id"]))
    dopo = Counter(v["platform"] for v in a["registro"] if vmc_di(v["entity_id"]))
    restano = sum(vecchie_piattaforme.values())
    return controllo(
        nome,
        "passato" if not negli_stati and not restano else "fallito",
        "Dopo la conferma non restano entità dei domini degli aiutanti, timer e script "
        "delle VMC, né voci del registro delle vecchie piattaforme (template, "
        "command_line, aiutanti, timer, script; le automazioni restano entità "
        "«automation», controllo a parte).",
        {
            "entità vecchie negli stati": len(negli_stati),
            "voci del registro delle vecchie piattaforme": restano,
            **{f"registro prima: {k}": v for k, v in sorted(prima.items())},
            **{f"registro dopo: {k}": v for k, v in sorted(dopo.items())},
        },
        negli_stati[:100]
        + [f"registro: {k} {v}" for k, v in vecchie_piattaforme.items()],
    )


def controlla_automazioni(
    p: Mapping[str, Any] | None, a: Mapping[str, Any] | None
) -> dict[str, Any]:
    nome = "automazioni con gli stessi entity_id"
    if not (a and p):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    prima = sorted(e for e in p["stati"] if e.startswith("automation.") and vmc_di(e))
    mancanti = [e for e in prima if e not in a["stati"]]
    spente = [
        e
        for e in prima
        if e in a["stati"] and a["stati"][e]["state"] != p["stati"][e]["state"]
    ]
    return controllo(
        nome,
        "passato" if not mancanti and not spente else "fallito",
        "Le 14 automazioni di ogni VMC restano entità «automation» con lo stesso "
        "entity_id e lo stesso stato (accesa / spenta).",
        {
            "prima": len(prima),
            "mancanti dopo": len(mancanti),
            "stato diverso": len(spente),
        },
        [f"mancante: {e}" for e in mancanti] + [f"stato diverso: {e}" for e in spente],
    )


AZIONE_PERSONALE = utente.AUTOMAZIONE_PERSONALE["actions"][0]["action"]


def controlla_rinominate(
    a: Mapping[str, Any] | None, p: Mapping[str, Any] | None
) -> dict[str, Any]:
    """La riparazione dei nomi cambiati elenca ogni vecchio nome che l'utente usa ancora:
    gli aiutanti della sua scheda entità (vista «personale») e il comando di shell della
    sua automazione (l'esempio del README della beta)."""
    nome = "riparazione dei nomi cambiati: le cose dell'utente con i vecchi nomi"
    if not (a and p):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    attesi = [
        e for e in utente.ENTITA_PERSONALI if e.split(".")[0] not in DOMINI_SENSORI
    ] + [AZIONE_PERSONALE]
    elenco = " ".join(
        str((r.get("translation_placeholders") or {}).get("elenco", ""))
        for r in a["riparazioni"]
        if r["domain"] == "vmc_master"
    )
    mancanti = [x for x in attesi if f"`{x}`" not in elenco]
    servizio_dopo = AZIONE_PERSONALE.split(".", 1)[1] in (a.get("servizi") or {}).get(
        "shell_command", []
    )
    return controllo(
        nome,
        "passato" if not mancanti else "fallito",
        "Vecchi nomi usati dall'utente (scheda entità della vista «personale» e azione "
        f"«{AZIONE_PERSONALE}» dell'automazione d'esempio del README) contro l'elenco della "
        "riparazione «impostazioni_rinominate» dopo il passaggio.",
        {
            "vecchi nomi usati": len(attesi),
            "elencati": len(attesi) - len(mancanti),
            "mancanti": len(mancanti),
            f"servizio {AZIONE_PERSONALE} dopo": servizio_dopo
            if "servizi" in a
            else "non misurato",
        },
        [f"non elencato: {x}" for x in mancanti],
    )


def controlla_utente(
    a: Mapping[str, Any] | None, p: Mapping[str, Any] | None
) -> dict[str, Any]:
    nome = "cose dell'utente con i nomi di oggi (informazione)"
    if not (a and p):
        return non_eseguibile(nome, "l'istantanea A_dopo")
    automazione = "automation.vmc_a_velocita_1_alle_22"
    riparazioni = [
        f"{r['domain']}.{r['issue_id']} ({r.get('translation_key')}) {r.get('translation_placeholders') or ''}"
        for r in a["riparazioni"]
    ]
    personali = {e: _stato(a, e) for e in utente.ENTITA_PERSONALI}
    return controllo(
        nome,
        "informazione",
        "L'automazione d'esempio del README (shell_command.vmc_master_velocita_1) e la "
        "scheda entità dell'utente: cosa resta e cosa dicono le riparazioni.",
        {
            "automazione personale": _stato(a, automazione),
            "entità della scheda personale presenti": sum(
                v is not None for v in personali.values()
            ),
            "riparazioni dopo": len(a["riparazioni"]),
        },
        [f"{e}: {v}" for e, v in personali.items()] + riparazioni,
    )


def controlla_senza_conferma(
    m: Mapping[str, Any] | None, s: Mapping[str, Any] | None
) -> list[dict[str, Any]]:
    nome = "riavvio senza confermare la riparazione"
    if not (m and s):
        return [non_eseguibile(nome, "l'istantanea S_riavvio_senza_conferma")]
    vecchie_m = sum(
        1 for e in m["stati"] if vmc_di(e) and e.split(".")[0] in DOMINI_AIUTANTI
    )
    vecchie_s = sum(
        1 for e in s["stati"] if vmc_di(e) and e.split(".")[0] in DOMINI_AIUTANTI
    )
    nuove_s = Counter(
        v["entity_id"].split(".")[0]
        for v in s["registro"]
        if vmc_di(v["entity_id"]) and v["platform"] == "vmc_master"
    )
    issue_m = sorted(
        f"{r['domain']}.{r['issue_id']}"
        for r in m["riparazioni"]
        if r["domain"] == "vmc_master"
    )
    issue_s = sorted(
        f"{r['domain']}.{r['issue_id']}"
        for r in s["riparazioni"]
        if r["domain"] == "vmc_master"
    )
    risultati = [
        controllo(
            nome,
            "informazione",
            "Cosa vede l'utente se riavvia senza confermare: il vecchio package resta caricato, "
            "la riparazione resta, nessun entity_id con «_2».",
            {
                "aiutanti vecchi al primo avvio": vecchie_m,
                "aiutanti vecchi dopo il riavvio senza conferma": vecchie_s,
                **{
                    f"voci vmc_master nel registro: {k}": v
                    for k, v in sorted(nuove_s.items())
                },
                "riparazioni VMC Master al primo avvio": len(issue_m),
                "riparazioni VMC Master dopo": len(issue_s),
            },
            [f"primo avvio: {i}" for i in issue_m]
            + [f"senza conferma: {i}" for i in issue_s],
        ),
        controllo(
            "la riparazione resta dopo un riavvio senza conferma",
            "passato" if issue_s and issue_s == issue_m else "fallito",
            "La riparazione del passaggio è ancora lì dopo il riavvio.",
            {"prima": len(issue_m), "dopo": len(issue_s)},
        ),
        controlla_doppioni(s, "S_riavvio_senza_conferma"),
    ]
    return risultati


# ------------------------------------------------------------------- passi
def controlla_passaggio(
    cartella: Path, esito: Mapping[str, Any]
) -> list[dict[str, Any]]:
    leggi = lambda nome: istantanea.leggi(cartella, nome)
    p0, r = leggi("P0_prima"), leggi("R_riavvio_di_controllo")
    p, fp = leggi("P_prima_del_passaggio"), leggi("FP_fermata_beta")
    m, m_file = leggi("M_primo_avvio_nativo"), leggi("M_file")
    a, fa = leggi("A_dopo"), leggi("FA_fermata_finale")
    ultima = ultima_con_il_package(leggi("FC_fermata_dopo_conferma"), fp)
    costruzione = istantanea.leggi(cartella.parent / "costruzione", "esito") or {}
    scritte = costruzione.get("impostazioni_scritte")
    confermata = bool(esito.get("riparazioni_seguite"))
    risultati = [controlla_avvio_beta(p0), controlla_primo_avvio(esito, m)]
    if esito.get("passo") == "senza_conferma":
        risultati += controlla_senza_conferma(m, leggi("S_riavvio_senza_conferma"))
    risultati += [
        controlla_riparazione(esito),
        controlla_sensori(p, a),
        controlla_doppioni(a),
        controlla_storico(fp, fa, p),
        controlla_statistiche(fp, fa, a),
        controlla_impostazioni(p0, r, p, ultima, a, scritte),
        controlla_memorie(p0, r, ultima, a),
        controlla_interni(p0, r, ultima, fa, confermata),
        controlla_valori_cambiati(fp, ultima),
        controlla_timer(p0, r, p, a),
        *controlla_file(fp, m_file, fa, confermata, leggi("F0_fermata_controllo")),
    ]
    if (
        esito.get("passo") != "senza_conferma"
    ):  # lì non si fotografano (sotto i 10 minuti)
        risultati += [
            controlla_fotografie(
                "scheda della beta dopo il riavvio di controllo (informazione)",
                esito.get("fotografie_beta"),
                decide=False,
            ),
            controlla_fotografie(
                "scheda di ogni VMC al primo avvio nativo, prima della conferma",
                esito.get("fotografie_in_attesa"),
            ),
        ]
    risultati += [
        *controlla_scheda(p, a, esito.get("fotografie")),
        controlla_vecchie(a, p),
        controlla_automazioni(p, a),
        controlla_rinominate(a, p),
        controlla_utente(a, p),
    ]
    return risultati


def controlla_riaggiunta(
    cartella: Path, esito: Mapping[str, Any]
) -> list[dict[str, Any]]:
    leggi = lambda nome: istantanea.leggi(cartella, nome)
    a0, e, z = (
        leggi("A0_prima_di_eliminare"),
        leggi("E_eliminata"),
        leggi("Z_riaggiunta"),
    )
    fz = leggi("FZ_fermata_finale")
    fa = istantanea.leggi(cartella.parent / "passaggio", "FA_fermata_finale")
    nome_vmc = utente.CASA[2].nome
    risultati = []
    if not (a0 and e):
        return [non_eseguibile("VMC eliminata", "le istantanee A0 ed E")]
    della = lambda ist: sorted(x for x in ist["stati"] if vmc_di(x) == nome_vmc)
    registro = lambda ist: [
        v for v in ist["registro"] if vmc_di(v["entity_id"]) == nome_vmc
    ]
    rimaste = della(e)
    rimaste_registro = registro(e)
    risultati.append(
        controllo(
            f"VMC {nome_vmc} eliminata: niente resta negli stati e nel registro",
            "passato" if not rimaste and not rimaste_registro else "fallito",
            "Entità e voci del registro della VMC dopo «Elimina» in Dispositivi e servizi "
            "(Home Assistant toglie le voci del registro della voce eliminata; quelle senza "
            "voce di configurazione restano, «unavailable»).",
            {
                "entità prima": len(della(a0)),
                "entità dopo l'eliminazione": len(della(e)),
                "voci del registro prima": len(registro(a0)),
                "voci del registro dopo l'eliminazione": len(registro(e)),
                "riavvio richiesto": (esito.get("eliminazione") or {}).get(
                    "require_restart"
                ),
            },
            [
                f"rimasta: {v['entity_id']} (piattaforma {v['platform']}, voce "
                f"{v.get('config_entry_id')}) = {_stato(e, v['entity_id'])}"
                for v in rimaste_registro
            ],
        )
    )
    if not z:
        risultati.append(
            non_eseguibile(f"VMC {nome_vmc} aggiunta di nuovo", "l'istantanea Z")
        )
        return risultati
    prima = [x for x in della(a0) if x.split(".")[0] in DOMINI_SENSORI]
    mancanti = [x for x in prima if x not in z["stati"]]
    risultati.append(
        controllo(
            f"VMC {nome_vmc} aggiunta di nuovo: stessi entity_id",
            "passato" if not mancanti else "fallito",
            "Sensori della VMC prima dell'eliminazione e dopo averla aggiunta di nuovo.",
            {"sensori prima": len(prima), "mancanti dopo": len(mancanti)},
            mancanti,
        )
    )
    risultati.append(controlla_doppioni(z, "Z_riaggiunta"))
    if fa and fz:
        meta_a = fa["registro_storico"]["states_meta"]
        meta_z = fz["registro_storico"]["states_meta"]
        cambiati = [x for x in prima if x in meta_a and meta_z.get(x) != meta_a[x]]
        risultati.append(
            controllo(
                f"VMC {nome_vmc} aggiunta di nuovo: storico continuo",
                "passato" if not cambiati else "fallito",
                "states_meta dei sensori della VMC riusati dopo l'eliminazione e la nuova aggiunta.",
                {
                    "sensori con storico": sum(1 for x in prima if x in meta_a),
                    "cambiati": len(cambiati),
                },
                cambiati,
            )
        )
    stessi = diversi = 0
    dettagli = []
    for chiave in VISIBILI:
        nuovo = nuovo_id(chiave, nome_vmc)
        v0, v1 = _stato(a0, nuovo), _stato(z, nuovo)
        if uguali(v0, v1):
            stessi += 1
        else:
            diversi += 1
            dettagli.append(f"{nuovo}: {v0!r} → {v1!r}")
    risultati.append(
        controllo(
            f"VMC {nome_vmc} aggiunta di nuovo: impostazioni (informazione)",
            "informazione",
            "Impostazioni della VMC prima dell'eliminazione e dopo la nuova aggiunta "
            "(ripartono dai valori iniziali o restano?).",
            {"uguali": stessi, "diverse": diversi},
            dettagli,
        )
    )
    foto = [
        f for f in esito.get("fotografie") or [] if f.get("vista") == f"vmc-{nome_vmc}"
    ]
    if foto:
        risultati.append(
            controllo(
                f"VMC {nome_vmc} aggiunta di nuovo: scheda nella plancia (informazione)",
                "informazione",
                "La scheda della plancia punta alla voce eliminata (entry_id): cosa mostra.",
                {
                    "avvisi": len(foto[0]["avvisi"]),
                    "messaggi della scheda": len(foto[0]["messaggi_scheda"]),
                },
                foto[0]["messaggi_scheda"] + foto[0]["avvisi"],
            )
        )
    return risultati
