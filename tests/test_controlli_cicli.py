"""Controlli automatici di classe sui cicli di conferma e sui ripristini (21-11-2026, controlli «cicli» d1, d4, d6,
portati dal prototipo test_proposto_cicli.py della verifica statica della b36):
- d1: cicli di conferma che non finiscono (uscite «velocita' voluta», «scelta dell'utente», «Black-Out» e, nel
  Calendario, «VMC non raggiungibile»);
- d4: comandi alla VMC fuori da un ciclo di conferma in tutto il package installato;
- d6: velocita' scelta dall'utente persa durante un'attesa (ripristino che parte dopo il «for» del trigger senza
  guardare la lettura).

Il package installato e' quello che arriva nell'HA dell'utente: per vmc_master.yaml le sezioni CLONA e INSTALLA sono
tolte con trasforma.rimuovi_sezioni_solo_master, come fa l'installatore. I numeri fissati (FISSATI) sono quelli
misurati sul codice: un cambio che li sposta va guardato e il numero aggiornato, come in test_b34_cicli (220 comandi)."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from homeassistant.util import yaml as hay

from custom_components.vmc_master import trasforma

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
COMANDO = re.compile(r"^shell_command\.vmc_master_(velocita_[0-4]|notturna|freecooling|iperventilazione|\{\{.*\}\})$")
ALTRI_5001 = re.compile(r"^shell_command\.vmc_master_(sensori_on|sensori_off|pannello_led_on|pannello_led_off|reset_filtro)$")

# ------------------------------------------------------------------------------------------------ caricamento
_CACHE: dict[str, Any] = {}


def _carica(nome: str) -> Any:
    """File del package come arriva nell'HA dell'utente (vmc_master.yaml senza le sezioni CLONA e INSTALLA)."""
    if nome not in _CACHE:
        testo = (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")
        if nome == "vmc_master.yaml":
            testo = trasforma.rimuovi_sezioni_solo_master(testo)
        _CACHE[nome] = hay.parse_yaml(testo)
    return _CACHE[nome]


def _automazione() -> dict[str, Any]:
    return _carica("vmc_master_automazione.txt")


def _package() -> dict[str, Any]:
    return _carica("vmc_master.yaml")


# ------------------------------------------------------------------------------------------------ visite
def _nodi(nodo: Any) -> Iterator[Any]:
    yield nodo
    if isinstance(nodo, dict):
        for v in nodo.values():
            yield from _nodi(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _nodi(v)


def _testo(nodo: Any) -> str:
    if isinstance(nodo, dict):
        return "\n".join(f"{k}: {_testo(v)}" for k, v in nodo.items())
    if isinstance(nodo, list):
        return "\n".join(_testo(v) for v in nodo)
    return str(nodo)


def _comandi(nodo: Any, dentro: bool = False, altri: bool = False) -> Iterator[tuple[str, bool]]:
    """Comandi alla VMC e se stanno dentro un repeat (come test_b34_cicli._comandi; altri=True anche LED, sensori e
    reset del filtro)."""
    if isinstance(nodo, dict):
        azione = nodo.get("action")
        if isinstance(azione, str) and (COMANDO.match(azione.strip()) or (altri and ALTRI_5001.match(azione.strip()))):
            yield azione.strip(), dentro
        for k, v in nodo.items():
            yield from _comandi(v, dentro or k == "repeat", altri)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _comandi(v, dentro, altri)


def _comandi_diretti(sequenza: Any) -> list[str]:
    """Comandi alla VMC di un ciclo senza scendere nei repeat annidati."""
    out: list[str] = []

    def visita(n: Any) -> None:
        if isinstance(n, dict):
            a = n.get("action")
            if isinstance(a, str) and (COMANDO.match(a.strip()) or ALTRI_5001.match(a.strip())):
                out.append(a.strip())
            for k, v in n.items():
                if k != "repeat":
                    visita(v)
        elif isinstance(n, list):
            for v in n:
                visita(v)
    visita(sequenza)
    return out


def _id_trigger(condizioni: Any) -> list[str]:
    ids: list[str] = []
    for n in _nodi(condizioni):
        if isinstance(n, dict) and n.get("condition") == "trigger" and "id" in n:
            ids.extend(str(i).strip() for i in (n["id"] if isinstance(n["id"], list) else [n["id"]]))
    return list(dict.fromkeys(ids))


def _rami() -> Iterator[tuple[str, dict[str, Any]]]:
    """(id dei trigger separati da virgola, ramo) per ogni ramo di primo livello dell'automazione."""
    for blocco in _automazione()["actions"]:
        for ramo in (blocco.get("choose") or []) if isinstance(blocco, dict) else []:
            yield ",".join(_id_trigger(ramo.get("conditions", []))), ramo


def _cicli_con_comando() -> Iterator[tuple[str, str, dict[str, Any]]]:
    """(file, dove, repeat) per ogni ciclo che manda direttamente un comando alla VMC."""
    for nome, ramo in _rami():
        for n in _nodi(ramo):
            if isinstance(n, dict) and isinstance(n.get("repeat"), dict) and _comandi_diretti(n["repeat"].get("sequence")):
                yield "automazione", nome, n["repeat"]
    for chiave in ("script", "automation"):
        sezione = _package().get(chiave) or {}
        voci = sezione.items() if isinstance(sezione, dict) else enumerate(sezione)
        for nome, voce in voci:
            for n in _nodi(voce):
                if isinstance(n, dict) and isinstance(n.get("repeat"), dict) and _comandi_diretti(n["repeat"].get("sequence")):
                    yield "package", f"{chiave}.{nome}", n["repeat"]


# uscite del ciclo (condizione «until»)
U_C = re.compile(r"states\('" + re.escape(LETTURA) + r"'\)\s*not in \[\s*vel_prima_del_comando")
U_B = re.compile(r"is_state\('binary_sensor\.vmc_master_black_out_rilevato',\s*'on'\)")
U_DT = re.compile(r"is_state\('sensor\.vmc_master_status_ventola',\s*'unavailable'\)\s*and\s*\(now\(\)\s*-\s*"
                  r"states\.sensor\.vmc_master_status_ventola\.last_changed\)")
U_DI = re.compile(r"is_state\('sensor\.vmc_master_status_ip_interfaccia',\s*'OFF-Line'\)\s*and\s*\(now\(\)\s*-\s*"
                  r"states\.sensor\.vmc_master_status_ip_interfaccia\.last_changed\)")
CALENDARIO = re.compile(r"[Cc]alendario|^[12]° \w+ Off$")

# ------------------------------------------------------------------------------------------------ d1
# misurati sulla b36 (b36-pdr2): cicli con un comando nell'automazione e nel package installato, cicli dell'automazione
# senza l'uscita «VMC non raggiungibile»
FISSATI = {"cicli_automazione": 210, "cicli_package": 360, "senza_d_automazione": 192}


def test_d1_ogni_ciclo_di_comando_ha_le_uscite_velocita_scelta_black_out() -> None:
    """d1: ogni ciclo che manda un comando alla VMC (automazione e package installato) ha UNA sola condizione «until»
    con le uscite «velocita' cambiata dall'utente» (vel_prima_del_comando) e «Black-Out rilevato»; i cicli sono contati,
    cosi' un ciclo nuovo va guardato. La «velocita' voluta» puo' mancare solo nella forma «lettura cambiata da
    vel_prima_del_comando» (umidita_velocita_0: partendo da Velocita' 0 qualsiasi cambio chiude il ciclo)."""
    cicli = list(_cicli_con_comando())
    n_auto = sum(1 for f, _, _ in cicli if f == "automazione")
    n_pkg = sum(1 for f, _, _ in cicli if f == "package")
    assert (n_auto, n_pkg) == (FISSATI["cicli_automazione"], FISSATI["cicli_package"]), (n_auto, n_pkg)
    sbagliati = []
    for file, dove, ciclo in cicli:
        fine = ciclo.get("until")
        if not (isinstance(fine, list) and len(fine) == 1):
            sbagliati.append((file, dove, "until non unico"))
            continue
        t = _testo(fine)
        if not (U_B.search(t) and U_C.search(t)):
            sbagliati.append((file, dove, "manca Black-Out o scelta dell'utente"))
    assert sbagliati == [], sbagliati


def test_d1_cicli_del_calendario_escono_con_la_vmc_non_raggiungibile() -> None:
    """d1 (B1-1, C1-5, Foglio A27 N.B. «DURANTE UNA FASCIA LA RIPETIZIONE DEL COMANDO SI FERMA SE LA VMC RESTA
    OFF-LINE O LA SUA VELOCITA' NON SI LEGGE PER 32 SECONDI»): ogni ciclo del Calendario (script di fascia, rami
    «N° Giorno Off», «Calendario Off tra Fascie», calendario_ritorno_comando) ha l'uscita «lettura TCP persa»; gli script
    di fascia anche «IP OFF-Line»."""
    sbagliati = []
    for file, dove, ciclo in _cicli_con_comando():
        t = _testo(ciclo.get("until"))
        if file == "package" and "calendario_fascia" in dove:
            if not (U_DT.search(t) and U_DI.search(t)):
                sbagliati.append(dove)
        elif file == "automazione" and any(CALENDARIO.search(i) for i in dove.split(",")):
            if not U_DT.search(t):
                sbagliati.append(dove)
    assert sbagliati == [], sbagliati  # b35: 2 («Calendario Off tra Fascie» e «... e Spia Inquinanti ON», C1-5)


def test_d1_cicli_senza_uscita_vmc_non_raggiungibile_censiti() -> None:
    """d1 (censimento, non correzione): fuori dal Calendario i cicli hanno solo l'uscita Black-Out (Foglio A27: «OGNI
    COMANDO DELL'AUTOMAZIONE VIENE RIPETUTO ... FINCHE' LA VMC NON LO ESEGUE»; A23 per il ripristino). Il numero e'
    fissato: un ciclo nuovo senza l'uscita «VMC non raggiungibile» va guardato e contato qui. Sono 58 solo fuori Fascia
    (Black-Out 22, Umidita' 36: li ferma il Black-Out) e 134 che possono girare anche in Fascia (PdR, Inquinanti, Free,
    Congelamento, Δ Temp., interruttori), dove il Black-Out rilevato non scatta mai (tutti i suoi 11 casi chiedono le
    spie del Calendario spente): decisione del proprietario aperta (Foglio A27 N.B.)."""
    senza = [(f, d) for f, d, c in _cicli_con_comando() if not (U_DT.search(_testo(c.get("until")))
                                                               or U_DI.search(_testo(c.get("until"))))]
    assert all(f == "automazione" for f, _ in senza), [d for f, d in senza if f != "automazione"]
    assert len(senza) == FISSATI["senza_d_automazione"], len(senza)


# ------------------------------------------------------------------------------------------------ d4
PACKAGE_FUORI_CICLO = {
    # script avviati dall'utente, non comandi dell'automazione (Foglio A27 «OGNI COMANDO DELL'AUTOMAZIONE»)
    ("script.vmc_master_bottone_panico", "shell_command.vmc_master_velocita_0"): 2,  # arresto subito e di nuovo dopo
    # la coda, poi attesa della conferma 10 s e memoria Black-Out Velocita' 0 (descrizione dello script)
    ("script.vmc_master_profilo_inizializzazione", "shell_command.vmc_master_velocita_0"): 1,  # primo avvio, lanciato
    ("script.vmc_master_profilo_inizializzazione", "shell_command.vmc_master_sensori_off"): 1,  # dall'utente
    ("script.vmc_master_profilo_inizializzazione", "shell_command.vmc_master_pannello_led_on"): 1,
    ("script.vmc_master_reset_filtro_vmc", "shell_command.vmc_master_reset_filtro"): 1,  # pulsante dell'utente
}


def test_d4_comandi_alla_vmc_fuori_ciclo_in_tutto_il_package() -> None:
    """d4 (estende test_b34_cicli.test_comandi_di_velocita_fuori_ciclo_solo_quelli_voluti, che legge solo
    l'automazione): in TUTTO il package installato (script e automazioni) ogni comando alla porta 5001 sta in un ciclo,
    tranne quelli degli script avviati dall'utente elencati in PACKAGE_FUORI_CICLO; i comandi di velocita' sono 363."""
    pkg = _package()
    totale, fuori = 0, {}
    for chiave in ("script", "automation"):
        sezione = pkg.get(chiave) or {}
        voci = sezione.items() if isinstance(sezione, dict) else enumerate(sezione)
        for nome, voce in voci:
            for azione, dentro in _comandi(voce, altri=True):
                totale += bool(COMANDO.match(azione))
                if not dentro:
                    k = (f"{chiave}.{nome}", azione)
                    fuori[k] = fuori.get(k, 0) + 1
    assert totale == 363, totale
    assert fuori == PACKAGE_FUORI_CICLO, fuori


def test_d4_ripristino_black_out_ogni_comando_nel_ciclo_tutti_i_rami() -> None:
    """d4: tutti i rami con id «Black-Out ...» che mandano comandi (non solo gli 8 scritti a mano in test_b34_cicli) li
    mandano dentro un ciclo."""
    rami = [(n, r) for n, r in _rami() if "Black-Out" in n and list(_comandi(r))]
    assert len(rami) == 8, [n for n, _ in rami]
    assert all(dentro for _, r in rami for _, dentro in _comandi(r))


# ------------------------------------------------------------------------------------------------ d6
T_LETTURA = re.compile(r"states\('" + re.escape(LETTURA) + r"'\)\s*(==\s*['\"][^'\"]+['\"]|==\s*states\('[^']+'\)|in\s*\[)"
                       r"|is_state\('" + re.escape(LETTURA) + r"',\s*'[^']+'\)")
D6_ECCEZIONI = {
    **{f"{n}° {g} Off": "Foglio A25: all'uscita dalla Fascia la VMC si arresta (TIMING 3 s)"
       for g in ("Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica") for n in (1, 2)},
    "TeVsTi Free-Heating -> Imposta Velocità 0": "inizio della sospensione Free, non una fine (fuori perimetro d6)",
    "TeVsTi Free-Heating e Spia Inquinanti ON": "inizio della sospensione Free, non una fine (fuori perimetro d6)",
    "TeVsTi Free-Cooling -> Imposta Velocità 0": "inizio della sospensione Free, non una fine (fuori perimetro d6)",
    "TeVsTi Free-Cooling e Spia Inquinanti ON": "inizio della sospensione Free, non una fine (fuori perimetro d6)",
}
# Punti trovati senza protezione e non ancora decisi. Quando un punto viene corretto basta togliere la sua voce da questa
# lista; se invece il comportamento e' voluto, la voce passa in D6_ECCEZIONI con il riferimento al Foglio.
# «Rip. Vel. 0 No PdR» e «Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON» sono stati corretti nella b36 (A2-1).
# spia_umidita_off: la correzione e' in un altro ramo di lavoro; all'unione si toglie questa voce.
D6_DA_DECIDERE = {
    "spia_umidita_off": "fine Umidita' (28 s) con memorizzazione della scelta a 4 s: nessun controllo come C3-1/C3-2",
}


def _protezione(passo: dict[str, Any]) -> str | None:
    """Firma di un passo che protegge la scelta dell'utente:
    - «S1»: if ... then stop «scelta dall'utente» (A2-1, C3-1, C3-2, ripristino Black-Out): protegge i passi successivi;
    - «S2i»: if/choose che chiede alla lettura una velocita' (il comando parte solo se la VMC e' ancora li'): protegge
      il ramo che controlla;
    - «S3»: last_changed della lettura (scelta recente, ritorno del Calendario): protegge il ramo che controlla e i
      passi successivi."""
    if "if" in passo and any(isinstance(p, dict) and "scelta dall'utente" in str(p.get("stop", ""))
                             for p in passo.get("then") or []):
        return "S1"
    t = _testo({k: v for k, v in passo.items() if k in ("if", "conditions", "variables")})
    if f"states.{LETTURA}.last_changed" in t or ("vel.last_changed" in t and LETTURA in t):
        return "S3"
    return None


def _condizione_sulla_lettura(condizione: Any) -> bool:
    t = _testo(condizione)
    return bool(T_LETTURA.search(t)) and "black_out_rilevato" not in t


def _comandi_senza_protezione(sequenza: Any, protetto: bool = False) -> list[str]:
    """Comandi di velocita' che, seguendo l'ordine della sequenza (e delle sotto-sequenze di if, choose, repeat), non
    hanno una protezione prima di loro sul loro cammino: ogni caso di un choose deve avere la sua."""
    out: list[str] = []
    passi = sequenza if isinstance(sequenza, list) else [sequenza]
    for passo in passi:
        if not isinstance(passo, dict):
            continue
        firma = _protezione(passo)
        azione = passo.get("action")
        if isinstance(azione, str) and COMANDO.match(azione.strip()) and not protetto:
            out.append(azione.strip())
        if "if" in passo:
            dentro = protetto or firma is not None or _condizione_sulla_lettura(passo["if"])
            out += _comandi_senza_protezione(passo.get("then") or [], dentro)
            out += _comandi_senza_protezione(passo.get("else") or [], protetto or firma == "S3")
        for opzione in passo.get("choose") or []:
            dentro = protetto or _condizione_sulla_lettura(opzione.get("conditions", [])) or (
                _protezione({"conditions": opzione.get("conditions", [])}) is not None)
            out += _comandi_senza_protezione(opzione.get("sequence") or [], dentro)
        if "default" in passo:
            out += _comandi_senza_protezione(passo["default"], protetto)
        if isinstance(passo.get("repeat"), dict):
            out += _comandi_senza_protezione(passo["repeat"].get("sequence") or [], protetto)
        for chiave in ("sequence", "parallel"):
            if isinstance(passo.get(chiave), list):
                out += _comandi_senza_protezione(passo[chiave], protetto)
        if firma is not None:
            protetto = True
    return out


def _segnalati_d6() -> dict[str, int]:
    """Rami che mandano un comando di velocita', i cui trigger hanno tutti un «for» senza chiedere alla lettura una
    velocita' (partono anche se l'utente ha appena scelto un'altra velocita'), con il numero di comandi non protetti."""
    trigger: dict[str, list[dict[str, Any]]] = {}
    for t in _automazione()["triggers"]:
        trigger.setdefault(str(t.get("id")).strip(), []).append(t)
    segnalati: dict[str, int] = {}
    for nome, ramo in _rami():
        if not list(_comandi(ramo)):
            continue
        tr = [t for i in nome.split(",") for t in trigger.get(i, [])]
        if not tr or not all("for" in t for t in tr):
            continue
        if any(T_LETTURA.search(_testo({k: v for k, v in t.items() if k != "alias"})) for t in tr):
            continue
        scoperti = _comandi_senza_protezione(ramo.get("sequence", []))
        if scoperti:
            segnalati[nome] = len(scoperti)
    return segnalati


def test_d6_fine_attesa_protegge_la_scelta_dell_utente() -> None:
    """d6 (A2-1, C3-1, C3-2, ripristino Black-Out b36; Foglio F6, A23, A25, A28, A29): un ramo che manda un comando di
    velocita' e i cui trigger hanno tutti un «for» senza chiedere alla lettura una velocita' parte anche se l'utente ha
    appena scelto un'altra velocita' (scelta non ancora memorizzata): ogni suo comando deve avere la firma della
    protezione prima di se', anche in ogni caso di un choose (S1 stop «scelta dall'utente», S2i comando solo con la
    lettura ancora attesa, S3 last_changed della lettura). Senza «for» non c'e' finestra (Congelamento,
    test_c3_1_congelamento_senza_lo_stesso_buco). Restano solo le eccezioni volute (D6_ECCEZIONI) e i punti ancora da
    decidere (D6_DA_DECIDERE)."""
    segnalati = set(_segnalati_d6())
    attesi = set(D6_ECCEZIONI) | set(D6_DA_DECIDERE)
    assert segnalati == attesi, {"nuovi": sorted(segnalati - attesi), "non piu' segnalati": sorted(attesi - segnalati)}


def test_d6_i_due_rami_pdr_corretti_nella_b36_proteggono_ogni_comando() -> None:
    """d6 (b36, A2-1 completato): «Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON» (3 casi con il comando Free
    Cooling) e «Rip. Vel. 0 No PdR» non hanno comandi senza protezione; prima della correzione erano 3 e 1."""
    rami = dict(_rami())
    for nome in ("Rip. Free Cool./Heat. No PdR se Spia Inquinanti ON", "Rip. Vel. 0 No PdR"):
        assert list(_comandi(rami[nome])), nome
        assert _comandi_senza_protezione(rami[nome]["sequence"]) == [], nome
