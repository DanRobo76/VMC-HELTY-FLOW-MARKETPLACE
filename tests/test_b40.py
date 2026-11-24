"""Prove della 9.0.0b40.

fascia58 (Foglio A25: in Fascia l'Umidità non ha effetto e il Black-Out non si rileva; A23: in Fascia la VMC riparte con
la velocità della Fascia): i 58 cicli di conferma che girano solo fuori Fascia (ripristino dopo il Black-Out 22,
Umidità 36) perdevano il comando con la VMC non raggiungibile; se nel frattempo arrivava l'ora di una Fascia, al ritorno
della VMC il ciclo mandava ancora il comando vecchio (circa 9-10 s alla velocità vecchia) e solo dopo partiva la Fascia
(21 scenari della famiglia OF del simulatore). La Spia della Fascia non può accendersi mentre uno di questi cicli gira
(la accendono solo i 14 rami «N° Giorno On» della stessa automazione, mode: queued), quindi un'uscita sulle 14 spie non
scatterebbe mai: l'uscita usa le stesse condizioni del trigger della Fascia (interruttore del Calendario, giorno e orario
della 1a o 2a Fascia, Congelamento e Δ Temp. non in corso) con la velocità della VMC non leggibile. Nei rami del
Black-Out la memoria del Black-Out resta (la spegne lo script della Fascia quando parte; se la Fascia finisce prima del
ritorno della VMC il ripristino avviene al ritorno)."""

from __future__ import annotations

import re
from datetime import timedelta
from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.util import dt as dt_util

from tests.test_b39 import BLACK_OUT, LETTURA, PKG, SPIE_FASCIA, _automazione, _classi, _nodi, _package

# ------------------------------------------------------------------ fascia58
_G = "['lunedi', 'martedi', 'mercoledi', 'giovedi', 'venerdi', 'sabato', 'domenica'][now().weekday()]"
_ORA = "now().strftime('%H:%M')"


def _fascia(n: int) -> str:
    s = "" if n == 1 else "_2"
    g = _G + (" ~ '_2'" if n == 2 else "")
    return (f"(states('sensor.vmc_master_status_accensione_vmc_tramite_calendario{s}') == ({_G} | capitalize)"
            f" and {_ORA} >= states('input_datetime.vmc_master_accensione_' ~ {g})[0:5]"
            f" and {_ORA} < states('input_datetime.vmc_master_spegnimento_' ~ {g})[0:5])")


FASCIA58 = ("(is_state('sensor.vmc_master_status_ventola', 'unavailable')"
            " and is_state('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario', 'on')"
            " and is_state('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia', 'off')"
            " and is_state('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia', 'off')"
            f" and ({_fascia(1)} or {_fascia(2)}))")
SPIE_VELOCITA = {f"input_boolean.vmc_master_spia_velocita_{v}" for v in
                 ("0", "1", "2", "3", "4", "notturna", "iperventilazione", "freecooling")}
ACCENDE = {"input_boolean.turn_on", "input_boolean.toggle", "homeassistant.turn_on", "homeassistant.toggle"}


def _rami() -> list[tuple[list[str], list[Any]]]:
    out = []
    for blocco in _automazione()["actions"]:
        for ramo in (blocco.get("choose") or []) if isinstance(blocco, dict) else []:
            ids = [str(i) for n in _nodi(ramo.get("conditions", [])) if isinstance(n, dict)
                   and n.get("condition") == "trigger" for i in (n["id"] if isinstance(n["id"], list) else [n["id"]])]
            out.append((ids, ramo.get("sequence", [])))
    return out


def _bersagli(passo: dict[str, Any]) -> set[str]:
    t = passo.get("target") or passo.get("data") or {}
    e = t.get("entity_id", []) if isinstance(t, dict) else []
    return set([e] if isinstance(e, str) else e)


def test_fascia58_i_58_cicli_fuori_fascia_si_fermano_quando_inizia_una_fascia() -> None:
    """Classe intera: i 58 cicli che girano solo fuori Fascia (22 del ripristino dopo il Black-Out, 36 dell'Umidità)
    hanno per ultima, subito dopo il Black-Out, l'uscita «Fascia iniziata con la velocità non leggibile»; nessuno degli
    altri 153 cicli dell'automazione (135 che possono girare in Fascia, 18 del Calendario) la ha."""
    classi = _classi()
    fuori = classi["fuori"]
    assert len(fuori) == 58
    bo = [c for c in fuori if all(i.startswith("Black-Out Off") for i in c[0])]
    umi = [c for c in fuori if all(i.startswith(("spia_umidita_", "umidita_")) for i in c[0])]
    assert (len(bo), len(umi)) == (22, 36)
    for ids, testo, _, _ in fuori:
        assert testo.count(FASCIA58) == 1, ids
        assert testo.rstrip().endswith(BLACK_OUT + " or " + FASCIA58 + " }}"), ids
    for ids, testo, _, _ in classi["fascia"] + classi["calendario"]:
        assert "vmc_master_status_accensione_vmc_tramite_calendario" not in testo, ids


def test_fascia58_rami_del_black_out_attese_e_memoria() -> None:
    """Gli 8 rami «Black-Out Off» (ripristino): le 2 attese di 12 s dopo i cicli (Velocità 0 e Free) non attendono con
    la Fascia iniziata e la velocità non leggibile; prima del passo finale che spegne le 8 spie del Black-Out c'è la
    condizione «non (Fascia iniziata con la velocità non leggibile)»: la memoria del Black-Out resta, così la Fascia
    (che la spegne nel suo script) parte senza il comando vecchio, subito se Home Assistant vede ancora la VMC ON-Line,
    altrimenti al suo ritorno; se la Fascia finisce prima di partire, il ripristino avviene al ritorno della VMC. In tutto il file l'uscita compare 58 + 2 + 8 volte."""
    rami = [(ids, seq) for ids, seq in _rami() if ids and all(i.startswith("Black-Out Off") for i in ids)]
    assert len(rami) == 8
    attese = 0
    for ids, seq in rami:
        ultimo, prima = seq[-1], seq[-2]
        assert ultimo["action"] == "input_boolean.turn_off" and _bersagli(ultimo) == SPIE_VELOCITA, ids
        assert prima["condition"] == "template" and prima["value_template"] == "{{ not " + FASCIA58 + " }}", ids
        for n in _nodi(seq):
            if isinstance(n, dict) and "wait_template" in n:
                attese += 1
                assert n["wait_template"].rstrip().endswith(BLACK_OUT + " or " + FASCIA58 + " }}"), ids
                assert (n["timeout"], n["continue_on_timeout"]) == ("00:00:12", True), ids
    assert attese == 2
    assert (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8").count(FASCIA58) == 58 + 2 + 8 + 9


MEMORIA_BO = "Black-Out prima della conferma"
FINE_UMIDITA = {"spia_umidita_off", "umidita_off_con_inquinanti_partenza_velocita_0"}


def test_fascia58_memoria_del_black_out_dopo_i_9_cicli_di_fine_umidita() -> None:
    """I 9 cicli di FINE Umidità (8 «spia_umidita_off», 1 «umidita_off_con_inquinanti_partenza_velocita_0») spengono le
    spie dell'Umidità prima del comando: se il comando non è confermato, la velocità di fine allerta la ricorda solo il
    passo dopo il ciclo «Black-Out prima della conferma -> memorizza questa velocità» (memoria del Black-Out). Con
    l'uscita per la Fascia (prima della rilevazione del Black-Out) il passo memorizza anche con «Fascia iniziata con la
    velocità non leggibile»: se la Fascia parte la memoria la spegne il suo script, se l'orario finisce prima del ritorno
    della VMC al ritorno si ripristina la velocità di fine Umidità (scenari MF|UOFF|F0|C|P e N del simulatore: senza,
    V2 dell'Umidità invece di V0). Il passo segue il ciclo (dopo la variabile della velocità di fine allerta nella Free);
    gli altri 71 passi con lo stesso nome (cicli che girano anche in Fascia) restano come prima; i 27 cicli di INIZIO
    Umidità non hanno il passo (le spie dell'Umidità restano accese e i rami «umidita_velocita_*» ricomandano la velocità
    al ritorno della VMC)."""
    nuovo = "{{ (" + BLACK_OUT + " or " + FASCIA58 + ") and "
    trovati = altri = senza = 0
    for ids, seq in _rami():
        for lista in (n for n in _nodi(seq) if isinstance(n, list)):
            for i, passo in enumerate(lista):
                if not (isinstance(passo, dict) and str(passo.get("alias", "")).startswith(MEMORIA_BO)):
                    continue
                cond = passo["if"][0]["value_template"]
                if set(ids) & FINE_UMIDITA:
                    assert set(ids) <= FINE_UMIDITA, ids
                    assert cond.startswith(nuovo) and cond.count(FASCIA58) == 1, (ids, passo["alias"])
                    assert "se la Fascia parte la memoria la" in passo["alias"], ids
                    prima = lista[i - 1] if "repeat" in lista[i - 1] else lista[i - 2]
                    assert "variables" in lista[i - 1] or prima is lista[i - 1], ids
                    until = prima["repeat"]["until"][0]["value_template"]
                    assert until.rstrip().endswith(BLACK_OUT + " or " + FASCIA58 + " }}"), ids
                    trovati += 1
                else:
                    assert FASCIA58 not in cond, (ids, passo["alias"])
                    altri += 1
        if ids and all(i.startswith(("spia_umidita_on", "umidita_velocita_")) for i in ids):
            senza += sum(1 for n in _nodi(seq) if isinstance(n, dict) and "repeat" in n
                         and FASCIA58 in str(n["repeat"].get("until")))
            assert not any(isinstance(n, dict) and str(n.get("alias", "")).startswith(MEMORIA_BO) for n in _nodi(seq)), ids
    assert (trovati, altri, senza) == (9, 71, 27)


def test_fascia58_le_spie_della_fascia_le_accendono_solo_i_14_rami_on() -> None:
    """Perché l'uscita non usa le 14 spie: le accendono solo i 14 rami «N° Giorno On» dell'automazione (nessuno script
    né altra automazione del package), che con mode: queued non possono partire mentre un ciclo dell'automazione gira;
    un'uscita «spia della Fascia accesa» nei 58 cicli non scatterebbe mai."""
    trovati: dict[str, set[str]] = {}
    for ids, seq in _rami():
        for n in _nodi(seq):
            if isinstance(n, dict) and isinstance(n.get("action"), str) and n["action"].strip() in ACCENDE:
                for s in _bersagli(n) & set(SPIE_FASCIA):
                    trovati.setdefault(s, set()).update(ids)
    giorni = {"lunedi": "Lunedì", "martedi": "Martedì", "mercoledi": "Mercoledì", "giovedi": "Giovedì",
              "venerdi": "Venerdì", "sabato": "Sabato", "domenica": "Domenica"}
    atteso = {s: {f"{s[-1]}° {giorni[s.split('_')[-2]]} On"} for s in SPIE_FASCIA}
    assert trovati == atteso
    for n in _nodi(_package()):
        if isinstance(n, dict) and isinstance(n.get("action"), str) and n["action"].strip() in ACCENDE:
            assert not (_bersagli(n) & set(SPIE_FASCIA)), n


@pytest.fixture
def stati_fascia(hass: HomeAssistant, freezer):
    """Stati per valutare l'until vero (orologio fermo su un giovedì alle 12:00:00 UTC): VMC non leggibile, Calendario
    acceso, 1a Fascia di oggi in corso (dall'inizio del minuto precedente a 10 minuti dopo), 2a Fascia di oggi più tardi,
    Black-Out non rilevato."""
    freezer.move_to("2026-11-26 12:00:00+00:00")
    def imposta(**cambi: str) -> None:
        for k, v in cambi.items():
            hass.states.async_set(k.replace("__", "."), v)

    def ora(minuti: int) -> str:
        return (dt_util.now() + timedelta(minutes=minuti)).strftime("%H:%M:00")

    g = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")[dt_util.now().weekday()]
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set(LETTURA, "Velocità 0")  # né la velocità del ripristino (2) né quella dell'Umidità (1)
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    hass.states.async_set("input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario", "on")
    hass.states.async_set("input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia", "off")
    hass.states.async_set("input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia", "off")
    for n in ("", "_2"):
        hass.states.async_set(f"sensor.vmc_master_status_accensione_vmc_tramite_calendario{n}", g.capitalize())
    hass.states.async_set(f"input_datetime.vmc_master_accensione_{g}", ora(-1))
    hass.states.async_set(f"input_datetime.vmc_master_spegnimento_{g}", ora(10))
    hass.states.async_set(f"input_datetime.vmc_master_accensione_{g}_2", ora(30))
    hass.states.async_set(f"input_datetime.vmc_master_spegnimento_{g}_2", ora(40))
    for s in SPIE_FASCIA:
        hass.states.async_set(s, "off")
    return g, ora, imposta


async def test_fascia58_uscita_valutata_con_il_motore_di_home_assistant(hass: HomeAssistant, freezer,
                                                                          stati_fascia) -> None:
    """L'until vero di un ciclo del ripristino e di uno dell'Umidità (motore dei template di Home Assistant): esce con la
    velocità non leggibile e l'ora della 1a o della 2a Fascia di oggi arrivata, Calendario acceso, Congelamento e Δ Temp.
    non in corso; non esce con la velocità leggibile (il ciclo continua finché la VMC non esegue), con il Calendario
    spento o la Fascia «Disabilitata», con il Congelamento o il Δ Temp. in corso (la Fascia aspetta la fine
    dell'allerta, A25), prima dell'inizio o dalla fine della Fascia, con la Fascia di un altro giorno."""
    g, ora, imposta = stati_fascia
    fuori = _classi()["fuori"]
    cicli = [next(c for c in fuori if c[0][0] == "Black-Out Off Vel. 2"),
             next(c for c in fuori if c[0][0] == "spia_umidita_on")]
    for ids, testo, _, _ in cicli:
        fine = Template(testo, hass)

        def esce() -> bool:
            return result_as_boolean(fine.async_render({"vel_prima_del_comando": "Velocità 0"}))

        assert esce() is True, ids
        imposta(sensor__vmc_master_status_ventola="VMGH,0,0")
        assert esce() is False, ids
        imposta(sensor__vmc_master_status_ventola="unavailable")
        for entita, valore in (("input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario", "off"),
                               ("input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia", "on"),
                               ("input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia", "on"),
                               ("sensor.vmc_master_status_accensione_vmc_tramite_calendario", "Disabilitata"),
                               ("sensor.vmc_master_status_accensione_vmc_tramite_calendario", "Non disponibile"),
                               (f"input_datetime.vmc_master_accensione_{g}", ora(1)),
                               (f"input_datetime.vmc_master_spegnimento_{g}", ora(0))):
            vecchio = hass.states.get(entita).state
            hass.states.async_set(entita, valore)
            assert esce() is False, (ids, entita, valore)
            hass.states.async_set(entita, vecchio)
        assert esce() is True, ids
        altro = "Lunedi" if g != "lunedi" else "Martedi"
        imposta(sensor__vmc_master_status_accensione_vmc_tramite_calendario=altro)
        assert esce() is False, ids
        # 2a Fascia di oggi in corso (1a fuori dall'orario o di un altro giorno)
        hass.states.async_set(f"input_datetime.vmc_master_accensione_{g}_2", ora(-2))
        hass.states.async_set(f"input_datetime.vmc_master_spegnimento_{g}_2", ora(5))
        assert esce() is True, ids
        imposta(sensor__vmc_master_status_accensione_vmc_tramite_calendario_2=altro)
        assert esce() is False, ids
        imposta(sensor__vmc_master_status_accensione_vmc_tramite_calendario_2=g.capitalize(),
                sensor__vmc_master_status_accensione_vmc_tramite_calendario=g.capitalize())
        hass.states.async_set(f"input_datetime.vmc_master_accensione_{g}_2", ora(30))
        hass.states.async_set(f"input_datetime.vmc_master_spegnimento_{g}_2", ora(40))
        # il Black-Out e la velocità raggiunta fermano il ciclo come prima
        imposta(sensor__vmc_master_status_ventola="VMGH,0,0")
        hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "on")
        assert esce() is True, ids
        hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
        imposta(sensor__vmc_master_status_ventola="unavailable")


async def test_fascia58_l_ora_della_fascia_e_quella_del_trigger(hass: HomeAssistant, freezer, stati_fascia) -> None:
    """Il confronto dell'orario è quello del trigger «N° Giorno On» (ore e minuti, inizio compreso, fine esclusa): la
    Fascia che inizia alle hh:mm apre l'uscita da hh:mm:00 e la chiude a fine Fascia."""
    g, ora, _ = stati_fascia
    fine = Template("{{ " + FASCIA58 + " }}", hass)
    hass.states.async_set(f"input_datetime.vmc_master_accensione_{g}", ora(1))
    hass.states.async_set(f"input_datetime.vmc_master_spegnimento_{g}", ora(3))
    assert result_as_boolean(fine.async_render()) is False
    freezer.tick(timedelta(seconds=59))
    assert result_as_boolean(fine.async_render()) is False
    freezer.tick(timedelta(seconds=1))
    assert result_as_boolean(fine.async_render()) is True
    freezer.tick(timedelta(seconds=119))
    assert result_as_boolean(fine.async_render()) is True
    freezer.tick(timedelta(seconds=1))
    assert result_as_boolean(fine.async_render()) is False


def test_fascia58_il_trigger_della_fascia_chiede_le_stesse_condizioni() -> None:
    """Le condizioni dell'uscita vengono dal trigger della Fascia: i 14 trigger «N° Giorno On» chiedono il sensore
    dell'accensione programmata (1a o 2a) uguale al giorno, l'orario tra accensione e spegnimento della stessa Fascia e
    Congelamento e Δ Temp. non in corso; il sensore vale il giorno solo con l'interruttore del Calendario acceso. Le altre
    condizioni del trigger (VMC ON-Line e velocità leggibile, Spia della Fascia spenta) sono quelle che la VMC non
    raggiungibile e il ciclo in corso impediscono."""
    trigger = {str(t["id"]): str(t.get("value_template", "")) for t in _automazione()["triggers"] if "id" in t}
    giorni = {"Lunedì": "lunedi", "Martedì": "martedi", "Mercoledì": "mercoledi", "Giovedì": "giovedi",
              "Venerdì": "venerdi", "Sabato": "sabato", "Domenica": "domenica"}
    for nome, g in giorni.items():
        for n in (1, 2):
            t = trigger[f"{n}° {nome} On"]
            s = "" if n == 1 else "_2"
            assert f"states('sensor.vmc_master_status_accensione_vmc_tramite_calendario{s}') == \"{g.capitalize()}\"" in t
            assert f"input_datetime.vmc_master_accensione_{g}{s}" in t and f"input_datetime.vmc_master_spegnimento_{g}{s}" in t
            assert "states('input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia')== 'off'" in t
            assert "states('input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia')== 'off'" in t
            assert "states('sensor.vmc_master_status_ip_interfaccia')==\"ON-Line\"" in t
            assert f"states('input_boolean.vmc_master_spia_calendario_{g}_{n}')=='off'" in t
    sensori = [s for b in _package()["template"] for s in b.get("sensor", [])]
    for uid in ("vmc_master_status_accensione_vmc_tramite_calendario",
                "vmc_master_status_accensione_vmc_tramite_calendario_2"):
        (sensore,) = [s for s in sensori if s.get("unique_id") == uid]
        rami = re.findall(r"\{% (?:el)?if weekday == \d(.*?)%\}", str(sensore["state"]))
        assert len(rami) == 7
        assert all("states('input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario') == 'on'" in r for r in rami)
