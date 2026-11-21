"""b25: verifica al riavvio su inizi e azioni delle allerte, copie 1:1, spia Black-Out del Calendario."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
FASE = "states('input_number.vmc_master_fase_riallineamento_al_riavvio') | float(0)"
GUARDIA = re.compile(
    r"\) and \(" + re.escape(FASE) + r" == 0 or " + re.escape(FASE) + r" >= ([234])( or .+)?\) \}\}$"
)
# Allerte gia' prese in carico prima del riavvio: la loro azione riparte subito
PRESE_IN_CARICO = {
    "states('input_boolean.vmc_master_spia_co2_o_voc') == 'on'",
    "states('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0') == 'on'",
}
SPIA_BLACK_OUT = "input_boolean.vmc_master_spia_calendario_black_out"
SPIA_U0 = "input_boolean.vmc_master_spia_umidita_velocita_0"
SPIA_U0_MANTENUTA = "input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0"


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


def _trigger_template() -> list[dict]:
    automazione = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    return [t for t in automazione["triggers"] if t.get("trigger") == "template"]


def _copie_countdown() -> tuple[Counter, Counter]:
    righe = (PKG / "vmc_master.yaml").read_text(encoding="utf-8").split("\n")
    inizio = next(k for k, r in enumerate(righe) if 'id: "vmc_master_countdown_attese_automazione"' in r)
    fine = next(k for k in range(inizio + 1, len(righe)) if righe[k].startswith("  - id:"))
    accese: Counter = Counter()
    spente: Counter = Counter()
    k = inizio
    while k < fine:
        if not righe[k].strip().startswith("value_template: |-"):
            k += 1
            continue
        rientro = len(righe[k]) - len(righe[k].lstrip())
        a = b = k + 1
        while b < fine and (righe[b] == "" or len(righe[b]) - len(righe[b].lstrip()) > rientro):
            b += 1
        corpo = "\n".join(righe[a:b])
        apertura = "{%- set vmc_master_esito -%}"
        if apertura in corpo:
            spente[_norm(corpo[corpo.index(apertura) + len(apertura) : corpo.index("{%- endset -%}")])] += 1
        else:
            accese[_norm(corpo)] += 1
        k = b
    return accese, spente


def test_verifica_al_riavvio_sempre_nella_stessa_forma():
    con_fase = [_norm(str(t["value_template"])) for t in _trigger_template() if "fase_riallineamento" in str(t["value_template"])]
    assert len(con_fase) == 142  # b34: ritorno della VMC dopo un comando della Fascia non eseguito
    soglie: Counter = Counter()
    for testo in con_fase:
        trovata = GUARDIA.search(testo)
        assert trovata, testo[-200:]
        soglie[trovata.group(1)] += 1
        if trovata.group(2):
            altra = trovata.group(2)[4:]
            assert altra in PRESE_IN_CARICO or re.fullmatch(
                r"\(states\('input_boolean\.vmc_master_spia_velocita_[a-z0-9_]+_un_solo_avvio'\) == 'on'( or .+)?\)", altra
            ), altra
    assert soglie == Counter({"4": 91, "2": 40, "3": 11})


def test_copie_in_evento_ancora_valido_identiche():
    righe = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8").split("\n")
    trigger = _trigger_template()
    assert len(trigger) == 168  # b28: avviso «Non Disponibile» del Dispositivo per Invio Notifica; b34: ritorno dopo un comando non eseguito
    for t in trigger:
        tid = str(t["id"])
        intestazione = re.compile(r"\{%-? (el)?if trigger\.id == ['\"]" + re.escape(tid) + r"['\"] -?%\}")
        trovate = [k for k, r in enumerate(righe) if intestazione.fullmatch(r.strip())]
        assert len(trovate) == 1, tid
        rientro = len(righe[trovate[0]]) - len(righe[trovate[0]].lstrip())
        fine = next(
            k
            for k in range(trovate[0] + 1, len(righe))
            if len(righe[k]) - len(righe[k].lstrip()) == rientro and re.match(r"\{%-? (elif|else|endif)\b", righe[k].strip())
        )
        assert _norm("\n".join(righe[trovate[0] + 1 : fine])) == _norm(str(t["value_template"])), tid


def test_copie_nel_countdown_identiche():
    con_attesa = [_norm(str(t["value_template"])) for t in _trigger_template() if "for" in t]
    assert len(con_attesa) == 132
    accese, spente = _copie_countdown()
    for testo in con_attesa:
        assert accese[testo] == 1 and spente[testo] == 1, testo[:120]
    assert sum(accese.values()) == sum(spente.values()) == 132


def test_spia_black_out_del_calendario_azzerata_ed_esclusa():
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    automazione = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    scheda = (PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8")
    definizione = re.search(r"\n  vmc_master_spia_calendario_black_out: +# (.+)\n", pacchetto).group(1)
    richiami = [r for r in pacchetto.split("\n") if SPIA_BLACK_OUT in r and not r.lstrip().startswith("#")]
    assert definizione.startswith(
        f"[CONFIGURAZIONE, {len(richiami)} RICHIAMI] [INTERFACCIA, {scheda.count(SPIA_BLACK_OUT)} RICHIAMI] "
        f"[AUTOMAZIONE, {automazione.count(SPIA_BLACK_OUT)} RICHIAMI]"
    )
    assert scheda.count(SPIA_BLACK_OUT) == 2  # elenco Pulisci cronologia + riga «Black-Out durante la fascia» (b31)
    escluse = pacchetto[pacchetto.index("&vmc_master_entita_escluse_recorder") :]
    assert SPIA_BLACK_OUT in escluse[: escluse.index("\n\n")]
    for script in ("\n  vmc_master_azzera_booleans:", '\n    alias: "VMC Master - Pulisci cronologia Entità"'):
        corpo = pacchetto[pacchetto.index(script) :]
        assert SPIA_BLACK_OUT in corpo[: corpo.index("\n  vmc_master_", 10)], script


def test_pulisci_cronologia_e_scheda_hanno_le_stesse_entita():
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    scheda = (PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8")
    corpo = pacchetto[pacchetto.index('\n    alias: "VMC Master - Pulisci cronologia Entità"') :]
    corpo = corpo[: corpo.index("\n    alias:", 10)]
    dello_script = set(re.findall(r"\n +- ([a-z_]+\.vmc_master_[a-z0-9_]+)", corpo))
    elenco = scheda[scheda.index("{%- set elenco = [") :]
    della_scheda = set(re.findall(r"'([a-z_]+\.vmc_master_[a-z0-9_]+)'", elenco[: elenco.index("] -%}")]))
    assert dello_script and dello_script <= della_scheda


def test_ritorno_da_black_out_durante_il_riallineamento():
    """Corrente tornata nelle fasi 1-3: agisce il trigger di stato, una volta sola (spegne prima la spia)."""
    automazione = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    per_id = {str(t.get("id")): t for t in automazione["triggers"]}
    assert per_id["calendario_ritorno_da_black_out"]["trigger"] == "template"
    nuovo = per_id["calendario_ritorno_da_black_out_riallineamento"]
    assert (nuovo["trigger"], nuovo["entity_id"], nuovo["from"], nuovo["to"]) == (
        "state", "sensor.vmc_master_status_ip_interfaccia", "OFF-Line", "ON-Line"
    )
    assert nuovo["for"] == per_id["calendario_ritorno_da_black_out"]["for"]
    testo = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    ramo = testo[testo.index("            id: calendario_ritorno_da_black_out_riallineamento") :]
    ramo = ramo[: ramo.index("\n      - conditions:")]
    assert "float(0) >= 1" in ramo and "float(0) <= 3" in ramo
    assert "attesa_blackout_rilevazione" in ramo
    assert ramo.index(f"entity_id: {SPIA_BLACK_OUT}\n            action: input_boolean.turn_off") < ramo.index("choose:")
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    for verso in ("ON", "OFF"):
        assert pacchetto.count(
            f'id: "{verso}|blackout_ripristino|blackout_ripristino|Calendario - VMC di nuovo ON-Line durante il riallineamento al riavvio"'
        ) == 1


def _passi(nodo, sequenze: list) -> None:
    """Tutte le liste di passi (sequence, then, else, default) dell'automazione."""
    if isinstance(nodo, dict):
        for chiave, valore in nodo.items():
            if chiave in ("sequence", "then", "else", "default") and isinstance(valore, list):
                sequenze.append(valore)
            _passi(valore, sequenze)
    elif isinstance(nodo, list):
        for valore in nodo:
            _passi(valore, sequenze)


def _entita(passo) -> list:
    if not isinstance(passo, dict):
        return []
    entita = (passo.get("target") or {}).get("entity_id") or passo.get("entity_id") or []
    return [entita] if isinstance(entita, str) else list(entita)


def test_memoria_velocita_0_mantenuta_dell_umidita():
    """Velocità 0 mantenuta dall'Umidità (ramo «else» di umidita_velocita_0): accesa solo li', spenta ovunque cambi la spia Velocità 0."""
    automazione = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    sequenze: list = []
    _passi(automazione["actions"], sequenze)
    accese = spente = 0
    for passi in sequenze:
        for k, passo in enumerate(passi):
            if SPIA_U0 not in _entita(passo):
                continue
            azione = passo["action"]
            if SPIA_U0_MANTENUTA in _entita(passo):
                accese += azione == "input_boolean.turn_on"
                spente += azione == "input_boolean.turn_off"
                continue
            assert azione == "input_boolean.turn_on", passo
            seguente = passi[k + 1]
            assert seguente["action"] == "input_boolean.turn_off" and SPIA_U0_MANTENUTA in _entita(seguente), passo
            spente += 1
    # b33: +4 spente al cambio del mese con l'Umidità in corso (A3-7); b36: +1 interruttore Umidità con la VMC non disponibile (C4-5),
    # +3 Set 0 con la Free sospesa nei 2 rami TeVsTi e nella fine Inquinanti in Free (C4-4)
    assert (accese, spente) == (1, 50)
    testo = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    ramo = testo[testo.index("              - umidita_velocita_0\n") :]
    ramo = ramo[: ramo.index("\n      - conditions:")]
    allora = ramo[ramo.index("            then:\n") : ramo.index("            else:\n")]
    altrimenti = ramo[ramo.index("            else:\n") :]
    assert allora.index(f"entity_id: {SPIA_U0_MANTENUTA}") < allora.index("- variables:")
    assert f"- {SPIA_U0}\n                    - {SPIA_U0_MANTENUTA}" in altrimenti
    # b32: +1 nella condizione di umidita_velocita_0 (A3-3); b33: +4 (A3-7); b36: +1 C4-5, +4 C4-4 (fine Umidità, TeVsTi x2, R8)
    assert testo.count(SPIA_U0_MANTENUTA) == 56


def test_memoria_velocita_0_mantenuta_nel_package_e_nella_scheda():
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    automazione = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    scheda = (PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8")
    definizione = re.search(r"\n  vmc_master_spia_umidita_mantenuta_velocita_0: +# (.+)\n", pacchetto).group(1)
    assert definizione.startswith(
        f"[CONFIGURAZIONE, {pacchetto.count(SPIA_U0_MANTENUTA)} RICHIAMI] [INTERFACCIA, 1 RICHIAMO] "
        f"[AUTOMAZIONE, {automazione.count(SPIA_U0_MANTENUTA)} RICHIAMI]"
    )
    assert scheda.count(SPIA_U0_MANTENUTA) == 1
    escluse = pacchetto[pacchetto.index("&vmc_master_entita_escluse_recorder") :]
    assert SPIA_U0_MANTENUTA in escluse[: escluse.index("\n\n")]
    for script in ("\n  vmc_master_azzera_booleans:", '\n    alias: "VMC Master - Pulisci cronologia Entità"'):
        corpo = pacchetto[pacchetto.index(script) :]
        assert SPIA_U0_MANTENUTA in corpo[: corpo.index("\n  vmc_master_", 10)], script
    # le 2 copie del Countdown (ON/OFF) hanno la stessa verifica al riavvio del trigger
    assert pacchetto.count(f"or states('{SPIA_U0_MANTENUTA}') == 'on') }}}}") == 2
    assert f"or states('{SPIA_U0}') == 'on') }}}}" not in pacchetto + automazione
