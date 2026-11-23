"""Prove della 9.0.0b39: comandi dell'automazione durante una Fascia con la VMC non raggiungibile.

Durante una Fascia il Black-Out rilevato non si accende mai (i suoi 11 casi chiedono le 14 spie del Calendario spente):
un ciclo di conferma di un'allerta (PdR, Inquinanti, Congelamento, Δ Temp., Free, interruttori) con la VMC OFF-Line o con
la porta 5001 muta girava finché la VMC non tornava, con la coda dell'automazione ferma e il comando vecchio mandato al
ritorno. Scelta del proprietario (21-11-2026, Foglio A27 N.B.): l'uscita dei 32 s vale per tutti i cicli che possono
girare in una Fascia. La b39:
- A: aggiunge ai 134 cicli che possono partire anche in Fascia l'uscita «velocità non leggibile da 32 s con una Fascia in
  corso» (fuori Fascia è sempre falsa: i cicli restano quelli della b38). I 58 cicli che girano solo fuori Fascia
  (ripristino dopo il Black-Out, Umidità) non la hanno: tutti i loro trigger chiedono le spie del Calendario spente e le
  spie si accendono solo nei rami della stessa automazione (mode: queued), quindi una Fascia non può iniziare mentre
  girano; i cicli del Calendario hanno già la loro uscita (b34-b36).
- M (porta 5001 muta, VMC che risponde al ping): dopo ognuno dei 134 cicli, se è finito senza velocità raggiunta, senza
  scelta dell'utente e senza Black-Out, il comando si memorizza (Comando non eseguito, «velocità|ora») e si ripete appena
  la velocità torna leggibile con la VMC ON-Line, salvo se nel frattempo la velocità è cambiata o se c'è un Black-Out del
  Calendario; con un comando del Calendario non eseguito prima riparte la Fascia (il trigger aspetta la sua Spia spenta),
  salvo con un'allerta Congelamento o Δ Temp. in corso, che ha la precedenza; un ciclo finito normalmente (velocità
  raggiunta, scelta dell'utente, Black-Out) annulla il Comando non eseguito più vecchio (vale l'ultimo comando).
- P (corrente mancata durante una Fascia): i trigger delle allerte chiedono anche la Spia Black-Out del Calendario spenta,
  gemella delle 8 spie del Black-Out fuori Fascia: al ritorno della corrente prima riparte la Fascia (32 s), poi le allerte
  ripartono dalla sua velocità (prima un'allerta comandava la VMC prima del ritorno della Fascia, il ritorno lo prendeva
  per una scelta dell'utente e a fine allerta la VMC andava alla velocità di riaccensione invece che a quella della Fascia).
  Con un'allerta Congelamento o Δ Temp. in corso al ritorno della corrente la Fascia non può ripartire (Foglio A25: aspetta
  la fine dell'allerta): i due rami del ritorno accendono la Spia Comando non eseguito del Calendario, così a fine allerta
  riparte la Fascia e non la Velocità 1 di riaccensione memorizzata dalla riapplicazione del Congelamento.
La verifica dinamica (HA vero, VMC simulata con corrente, rete o porta 5001 interrotte) è nel simulatore (famiglia OF)."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, result_as_boolean
from homeassistant.util import dt as dt_util
from homeassistant.util import yaml as hay

from custom_components.vmc_master import trasforma

PKG = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master" / "package"
GIORNI = ("lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica")
SPIE_FASCIA = tuple(f"input_boolean.vmc_master_spia_calendario_{g}_{n}" for g in GIORNI for n in (1, 2))
FASCIA = " or ".join(f"is_state('{s}', 'on')" for s in SPIE_FASCIA)
LETTURA_PERSA_IN_FASCIA = (
    "(is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - "
    "states.sensor.vmc_master_status_ventola.last_changed).total_seconds() >= "
    "states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32) and (" + FASCIA + "))")
LETTURA_PERSA = (
    "(is_state('sensor.vmc_master_status_ventola', 'unavailable') and (now() - "
    "states.sensor.vmc_master_status_ventola.last_changed).total_seconds() >= "
    "states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32))")
BLACK_OUT = "is_state('binary_sensor.vmc_master_black_out_rilevato', 'on')"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
NON_ESEGUITO = "input_text.vmc_master_comando_non_eseguito"
CAL_NON_ESEGUITO = "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"
CAL_BLACK_OUT = "input_boolean.vmc_master_spia_calendario_black_out"
GUARDIA = f"states('{CAL_BLACK_OUT}') == 'off'"
SPIE_BLACK_OUT = ("0", "1", "2", "3", "4", "notturna", "freecooling", "iperventilazione")
COMANDO = re.compile(r"^shell_command\.vmc_master_(velocita_[0-4]|notturna|freecooling|iperventilazione|\{\{.*\}\})$")
CALENDARIO = re.compile(r"[Cc]alendario|^[12]° \w+ Off$")
# trigger con il blocco del Black-Out che non comandano la VMC (notifiche, errori delle entità, avvisi, nome, aggiornamenti)
SENZA_GUARDIA = {
    "Cambio Nome VMC", "Spia Avvisi On", "Spia Avvisi Off", "Repository Update ON", "Repository Update OFF",
    "Entità Temperatura Esterna Errore [Interfaccia]", "Entità Temperatura Interna Errore [Interfaccia]",
    "Entità Umidità Esterna Errore [Interfaccia]", "Entità Umidità Interna Errore [Interfaccia]",
    "Entità CO2 Interna Errore [Interfaccia]", "Dispositivo Notifica Errore [Interfaccia]", "VMC Velocità 0 da Notificare",
    "VMC Velocità in Funzione da Notificare", "Entità Temperatura Esterno Errore [Mobile]",
    "Entità Temperatura Interna Errore [Mobile]", "Entità Umidità Esterna Errore [Mobile]",
    "Entità Umidità Interna Errore [Mobile]", "Entità CO2 Interna Errore [Mobile]", "pannello_avvisi_problema",
}


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


_CACHE: dict[str, Any] = {}


def _automazione() -> dict[str, Any]:
    if "a" not in _CACHE:
        _CACHE["a"] = hay.parse_yaml(_testo("vmc_master_automazione.txt"))
    return _CACHE["a"]


def _package() -> dict[str, Any]:
    if "p" not in _CACHE:
        _CACHE["p"] = hay.parse_yaml(trasforma.rimuovi_sezioni_solo_master(_testo("vmc_master.yaml").replace("\r\n", "\n")))
    return _CACHE["p"]


def _nodi(nodo: Any) -> Iterator[Any]:
    yield nodo
    if isinstance(nodo, dict):
        for v in nodo.values():
            yield from _nodi(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _nodi(v)


def _ha_comando(sequenza: Any) -> bool:
    return any(isinstance(n, dict) and isinstance(n.get("action"), str) and COMANDO.match(n["action"].strip())
               for n in _nodi(sequenza))


def _trigger() -> dict[str, dict[str, Any]]:
    return {str(t["id"]): t for t in _automazione()["triggers"] if "id" in t}


def _solo_fuori_fascia(ids: list[str]) -> bool:
    """Tutti i trigger del ramo chiedono le 14 spie del Calendario spente (il ramo non può partire in Fascia)."""
    trigger = _trigger()
    return all(all(re.search(re.escape(f"states('{s}')") + r"\s*==\s*'off'", str(trigger[i].get("value_template", "")))
                   for s in SPIE_FASCIA) for i in ids)


def _cicli() -> Iterator[tuple[list[str], str, list[Any], int]]:
    """(id dei trigger del ramo, testo dell'until, sequenza che contiene il ciclo, posizione del ciclo) per ogni ciclo
    dell'automazione che manda un comando alla VMC."""
    def dentro(nodo: Any, ids: list[str]) -> Iterator[tuple[list[str], str, list[Any], int]]:
        if isinstance(nodo, list):
            for k, passo in enumerate(nodo):
                if isinstance(passo, dict) and isinstance(passo.get("repeat"), dict) and _ha_comando(passo["repeat"]["sequence"]):
                    fine = passo["repeat"]["until"]
                    assert isinstance(fine, list) and len(fine) == 1
                    yield ids, str(fine[0]["value_template"]), nodo, k
                else:
                    yield from dentro(passo, ids)
        elif isinstance(nodo, dict):
            for v in nodo.values():
                yield from dentro(v, ids)

    for blocco in _automazione()["actions"]:
        for ramo in (blocco.get("choose") or []) if isinstance(blocco, dict) else []:
            ids = [str(i) for n in _nodi(ramo.get("conditions", [])) if isinstance(n, dict)
                   and n.get("condition") == "trigger" for i in (n["id"] if isinstance(n["id"], list) else [n["id"]])]
            yield from dentro(ramo.get("sequence", []), ids)


def _classi() -> dict[str, list[tuple[list[str], str, list[Any], int]]]:
    out: dict[str, list[tuple[list[str], str, list[Any], int]]] = {"calendario": [], "fuori": [], "fascia": []}
    for ciclo in _cicli():
        ids = ciclo[0]
        if any(CALENDARIO.search(x) for x in ids):
            out["calendario"].append(ciclo)
        elif _solo_fuori_fascia(ids):
            out["fuori"].append(ciclo)
        else:
            out["fascia"].append(ciclo)
    return out


# ------------------------------------------------------------------ versioni
def test_versioni_b39() -> None:
    """Automazione, scheda (elenco della pulizia della cronologia) e manifest cambiano nella b39 (la VER. di un file cambia
    solo quando cambia il file)."""
    for nome, titolo in (("vmc_master_automazione.txt", "AUTOMAZIONE"),
                         ("vmc_master_scheda_manuale_interfaccia.txt", "SCHEDA MANUALE INTERFACCIA")):
        trovata = re.search(titolo + r" VMC HELTY FLOW PLUS RELEASE \[VER\. 9\.0\.0b(\d+)\]", _testo(nome)[:2000])
        assert trovata and int(trovata.group(1)) >= 39, nome
    manifest = json.loads((PKG.parent / "manifest.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"9\.0\.0b(\d+)", manifest["version"]) and int(manifest["version"].split("b")[1]) >= 39


# ------------------------------------------------------------------ A: uscita in Fascia
def test_cicli_in_fascia_escono_con_la_lettura_persa() -> None:
    """211 cicli di conferma: i 18 del Calendario hanno l'uscita senza condizioni (b34-b36); i 135 che possono girare in
    Fascia (134 delle allerte + la ripetizione del Comando non eseguito) hanno l'uscita «velocità non leggibile da 32 s
    con una Fascia in corso», subito dopo il Black-Out e per ultima; i 58 che girano solo fuori Fascia non la hanno."""
    classi = _classi()
    assert {k: len(v) for k, v in classi.items()} == {"calendario": 18, "fuori": 58, "fascia": 135}
    for ids, testo, _, _ in classi["calendario"]:
        assert LETTURA_PERSA in testo and LETTURA_PERSA_IN_FASCIA not in testo, ids
    for ids, testo, _, _ in classi["fuori"]:
        assert "sensor.vmc_master_status_ventola'" not in testo and BLACK_OUT in testo, ids
        assert any(i.startswith(("Black-Out Off", "spia_umidita_", "umidita_")) for i in ids), ids
    for ids, testo, _, _ in classi["fascia"]:
        assert testo.count(BLACK_OUT + " or " + LETTURA_PERSA_IN_FASCIA) == 1, ids
        assert testo.rstrip().endswith(LETTURA_PERSA_IN_FASCIA + " }}"), ids


def test_le_spie_della_fascia_sono_quelle_che_spengono_il_black_out() -> None:
    """Le 14 spie della condizione sono esattamente quelle che tutti gli 11 casi del Black-Out rilevato chiedono spente:
    con una di loro accesa il Black-Out non si accende e serve l'uscita della b39; con tutte spente la ferma il
    Black-Out e la condizione nuova è falsa (fuori Fascia nulla cambia)."""
    sensori = [s for blocco in _package()["template"] for s in blocco.get("binary_sensor", [])]
    (black_out,) = [s for s in sensori if s.get("unique_id") == "vmc_master_black_out_rilevato"]
    casi = re.split(r"\{%-? set t\d+ = ", str(black_out["state"]))[1:]
    assert len(casi) == 11
    for caso in casi:
        spente = set(re.findall(r"states\('(input_boolean\.vmc_master_spia_calendario_\w+?_[12])'\)\s*==\s*'off'", caso))
        assert spente == set(SPIE_FASCIA)


async def test_uscita_solo_in_fascia_e_dopo_32_secondi(hass: HomeAssistant, freezer) -> None:
    """La condizione nuova (valutata con il motore dei template di Home Assistant su un until vero dell'automazione):
    vera solo con la velocità non leggibile da almeno 32 s E una Fascia in corso; con 31 s, fuori Fascia o con la
    velocità leggibile è falsa e il ciclo continua come nella b38."""
    ids, testo, _, _ = next(c for c in _cicli() if c[0][0].startswith("PdR Vel. 1->"))
    fine = Template(testo, hass)
    hass.states.async_set("input_number.vmc_master_attesa_blackout_rilevazione", "32")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set(LETTURA, "Velocità 1")
    for spia in SPIE_FASCIA:
        hass.states.async_set(spia, "off")

    def esce(vel_prima: str = "Velocità 1") -> bool:
        return result_as_boolean(fine.async_render({"vel_prima_del_comando": vel_prima}))

    hass.states.async_set("sensor.vmc_master_status_ventola", "VMGH,1,0")
    assert esce() is False
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=31))
    assert esce() is False
    freezer.tick(timedelta(seconds=30))  # 61 s senza lettura, ma fuori Fascia: lo ferma solo il Black-Out (b38)
    assert esce() is False
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_mercoledi_2", "on")
    assert esce() is True
    hass.states.async_set("sensor.vmc_master_status_ventola", "VMGH,1,0")  # lettura tornata: il ciclo continua
    assert esce() is False
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=31))
    assert esce() is False
    freezer.tick(timedelta(seconds=1))
    assert esce() is True


@pytest.mark.parametrize("spia", SPIE_FASCIA)
async def test_ogni_spia_della_fascia_apre_l_uscita(hass: HomeAssistant, freezer, spia: str) -> None:
    """Ognuna delle 14 spie da sola basta (l'uscita vale per tutte e due le Fasce di tutti i giorni)."""
    _, testo, _, _ = next(c for c in _cicli() if any("delta" in i.lower() for i in c[0]))
    fine = Template(testo, hass)
    hass.states.async_set("input_number.vmc_master_attesa_blackout_rilevazione", "32")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set(LETTURA, "Non disponibile")
    for s in SPIE_FASCIA:
        hass.states.async_set(s, "on" if s == spia else "off")
    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=32))
    assert result_as_boolean(fine.async_render({"vel_prima_del_comando": "Velocità 2"})) is True


# ------------------------------------------------------------------ M: Comando non eseguito
def _passo_dopo(sequenza: list[Any], k: int) -> dict[str, Any]:
    assert k + 1 < len(sequenza)
    return sequenza[k + 1]


def test_dopo_ogni_ciclo_in_fascia_il_comando_non_eseguito() -> None:
    """Classe intera: dopo ognuno dei 135 cicli in Fascia c'è il passo del Comando non eseguito, con la condizione
    «nessuna delle altre uscite» (velocità raggiunta, scelta dell'utente, Black-Out) presa dal suo until, la velocità da
    raggiungere del ciclo; altrimenti (ciclo finito normalmente) l'annullamento del Comando non eseguito più vecchio. La
    Spia Comando non eseguito del Calendario non si tocca (prima riparte la Fascia). I cicli del Calendario e quelli
    fuori Fascia non hanno il passo."""
    classi = _classi()
    for ids, testo, sequenza, k in classi["fascia"]:
        passo = _passo_dopo(sequenza, k)
        interno = testo.strip()[2:-2].strip().replace(BLACK_OUT + " or " + LETTURA_PERSA_IN_FASCIA, BLACK_OUT)
        assert passo["if"] == [{"condition": "template", "value_template": "{{ not (" + interno + ") }}"}], ids
        (memoria,) = passo["then"]
        (annulla,) = passo["else"]
        assert memoria["action"] == "input_text.set_value" and memoria["target"] == {"entity_id": NON_ESEGUITO}, ids
        velocita, ora = memoria["data"]["value"].split("|{{ as_timestamp", 1)
        assert ora == "(now()) | round(1) }}", ids
        bersaglio = re.search(re.escape(f"states('{LETTURA}')") + r"\s*==\s*(.*?)\s+or\s+\(vel_prima_del_comando not in",
                              interno, re.S).group(1).strip()
        if not velocita.startswith("{{"):
            assert bersaglio.startswith(f"'{velocita}'"), ids  # velocità fissa del ciclo
        else:
            assert velocita == "{{ " + bersaglio + " }}", ids  # velocità calcolata come nell'until
        assert {k: v for k, v in annulla.items() if k != "alias"} == {
            "action": "input_text.set_value", "target": {"entity_id": NON_ESEGUITO}, "data": {"value": ""}}, ids
        assert CAL_NON_ESEGUITO not in str(passo), ids
    for ids, _, sequenza, k in classi["calendario"] + classi["fuori"]:
        if k + 1 < len(sequenza):
            assert NON_ESEGUITO not in str(sequenza[k + 1]), ids
    testo = _testo("vmc_master_automazione.txt")
    assert testo.count(f"entity_id: {NON_ESEGUITO}") == 2 * 135 + 1  # 135 passi (then + else) + l'azzeramento nel ramo


def _ramo_ritorno() -> dict[str, Any]:
    (ramo,) = [r for b in _automazione()["actions"] if isinstance(b, dict) for r in b.get("choose", [])
               if r["conditions"][0].get("id") == "comando_non_eseguito_ritorno"]
    return ramo


async def test_trigger_del_comando_non_eseguito(hass: HomeAssistant) -> None:
    """Il ritorno scatta con un Comando non eseguito memorizzato, la velocità di nuovo leggibile e la VMC ON-Line (non
    durante le fasi 1-3 del riallineamento al riavvio); con la Spia Comando non eseguito del Calendario accesa aspetta la
    Fascia, salvo con un'allerta Congelamento o Δ Temp. in corso (allora la Fascia aspetta la fine dell'allerta e il
    comando dell'allerta va per primo)."""
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == "comando_non_eseguito_ritorno"]
    assert trigger["trigger"] == "template" and "for" not in trigger
    t = Template(trigger["value_template"], hass)

    def stato(comando: str, lettura: str, rete: str, fase: str = "0", cal: str = "off", cong: str = "off",
              delta: str = "off") -> bool:
        hass.states.async_set(CAL_NON_ESEGUITO, cal)
        hass.states.async_set("input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia", cong)
        hass.states.async_set("input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia", delta)
        hass.states.async_set(NON_ESEGUITO, comando)
        hass.states.async_set("sensor.vmc_master_status_ventola", lettura)
        hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", rete)
        hass.states.async_set("input_number.vmc_master_fase_riallineamento_al_riavvio", fase)
        return result_as_boolean(t.async_render())

    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line") is True
    assert stato("", "VMGH,00002,0", "ON-Line") is False
    assert stato("Velocità 0|100.0", "unavailable", "ON-Line") is False
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "OFF-Line") is False
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line", "2") is False
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line", "4") is True
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line", cal="on") is False  # prima riparte la Fascia
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line", cal="on", cong="on") is True
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line", cal="on", delta="on") is True
    assert stato("Velocità 0|100.0", "VMGH,00002,0", "ON-Line", cong="on") is True
    # la copia nella condizione «Evento ancora valido» è uguale al trigger
    testo = _testo("vmc_master_automazione.txt")
    corpo = trigger["value_template"].strip()[3:-3].strip()
    assert re.sub(r"\s+", " ", testo).count(re.sub(r"\s+", " ", corpo)) == 2


async def test_ramo_del_comando_non_eseguito(hass: HomeAssistant, freezer) -> None:
    """Il ramo cancella il Comando non eseguito e lo ripete con il ciclo standard (uscita in Fascia compresa) solo se la
    VMC è ON-Line senza Black-Out del Calendario, la velocità è leggibile, diversa da quella del comando e non è
    cambiata da quando il comando non è stato eseguito (anche per la Fascia ripartita prima: l'ordine lo decide il
    trigger, la Spia Comando non eseguito del Calendario non conta qui)."""
    passi = _ramo_ritorno()["sequence"]
    variabili, azzera, condizione, memoria, ciclo, dopo = passi
    assert azzera["action"] == "input_text.set_value" and azzera["target"] == {"entity_id": NON_ESEGUITO}
    assert azzera["data"] == {"value": ""}
    assert memoria["variables"] == {"vel_prima_del_comando": f"{{{{ states('{LETTURA}') }}}}"}
    sequenza = ciclo["repeat"]["sequence"]
    assert sequenza[0]["action"] == "shell_command.vmc_master_{{ comando_vmc }}"
    assert [list(p)[0] for p in sequenza[1:]] == ["delay", "action", "delay"]
    fine = ciclo["repeat"]["until"][0]["value_template"]
    assert fine.startswith(f"{{{{ states('{LETTURA}') == velocita_del_comando or (vel_prima_del_comando not in")
    assert fine.endswith(BLACK_OUT + " or " + LETTURA_PERSA_IN_FASCIA + " }}")
    assert dopo["then"][0]["target"] == {"entity_id": NON_ESEGUITO}  # se si perde di nuovo la lettura, si rimemorizza

    vars_t = {k: Template(v, hass) for k, v in variabili["variables"].items()}
    cond = Template(condizione["value_template"], hass)
    ora = dt_util.utcnow()

    def valuta(comando: str) -> bool:
        hass.states.async_set(NON_ESEGUITO, comando)
        v: dict[str, Any] = {}
        for nome in ("comando_non_eseguito", "velocita_del_comando", "comando_non_eseguito_dalle", "comando_vmc"):
            v[nome] = vars_t[nome].async_render(v)
        return result_as_boolean(cond.async_render(v))

    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set(CAL_BLACK_OUT, "off")
    hass.states.async_set(CAL_NON_ESEGUITO, "off")
    hass.states.async_set(LETTURA, "Velocità 2")
    hass.states.async_set(LETTURA + "_interfaccia", "Velocità 2")
    freezer.tick(timedelta(seconds=60))
    dalle = f"{dt_util.as_timestamp(dt_util.utcnow()):.1f}"
    assert valuta(f"Velocità 0|{dalle}") is True
    assert valuta(f"Free Cooling|{dalle}") is True
    assert valuta(f"Velocità 2|{dalle}") is False  # la VMC ha già la velocità del comando
    assert valuta(f"Velocità 9|{dalle}") is False  # comando sconosciuto
    assert valuta(f"Velocità 0|{dt_util.as_timestamp(ora) - 10:.1f}") is False  # velocità cambiata dopo il comando
    hass.states.async_set(CAL_BLACK_OUT, "on")
    assert valuta(f"Velocità 0|{dalle}") is False  # Black-Out del Calendario: riparte la Fascia, poi le allerte
    hass.states.async_set(CAL_BLACK_OUT, "off")
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "OFF-Line")
    assert valuta(f"Velocità 0|{dalle}") is False
    hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
    hass.states.async_set(CAL_NON_ESEGUITO, "on")  # con Congelamento o Δ Temp. il trigger scatta anche così
    assert valuta(f"Velocità 0|{dalle}") is True
    freezer.tick(timedelta(seconds=5))
    hass.states.async_set(LETTURA, "Velocità 3")  # la Fascia è ripartita prima: la velocità è cambiata
    assert valuta(f"Velocità 0|{dalle}") is False


async def test_passo_memorizza_solo_con_la_lettura_persa(hass: HomeAssistant, freezer) -> None:
    """Il passo dopo il ciclo memorizza il comando solo se il ciclo è finito per la lettura persa in Fascia: con la
    velocità raggiunta, con una scelta dell'utente o con il Black-Out no; il valore è «velocità|ora»."""
    ids, testo, sequenza, k = next(c for c in _cicli() if c[0][0].startswith("PdR Vel. 2->"))
    passo = _passo_dopo(sequenza, k)
    cond = Template(passo["if"][0]["value_template"], hass)
    valore = Template(passo["then"][0]["data"]["value"], hass)
    for s in SPIE_FASCIA:
        hass.states.async_set(s, "off")
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_giovedi_1", "on")
    hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", "off")
    hass.states.async_set("input_number.vmc_master_attesa_blackout_rilevazione", "32")

    def memorizza(lettura: str, black_out: str = "off") -> bool:
        hass.states.async_set(LETTURA, lettura)
        hass.states.async_set("binary_sensor.vmc_master_black_out_rilevato", black_out)
        return result_as_boolean(cond.async_render({"vel_prima_del_comando": "Velocità 2"}))

    hass.states.async_set("sensor.vmc_master_status_ventola", "unavailable")
    freezer.tick(timedelta(seconds=34))
    assert memorizza("Velocità 2") is True  # lettura persa: velocità vecchia, comando non eseguito
    assert memorizza("Velocità 0") is False  # velocità raggiunta
    assert memorizza("Velocità 3") is False  # scelta dell'utente
    assert memorizza("Velocità 2", "on") is False  # Black-Out
    v, ora = valore.async_render().split("|")
    assert v == "Velocità 0" and abs(float(ora) - dt_util.as_timestamp(dt_util.utcnow())) < 1
    assert passo["else"][0]["data"] == {"value": ""}  # ciclo finito normalmente: il comando più vecchio si annulla


def test_comando_non_eseguito_nelle_copie_gemelle() -> None:
    """Helper nuovo: vuoto all'avvio, escluso dal recorder, nello script e nel pannello «Pulisci cronologia»."""
    pkg = _package()
    helper = pkg["input_text"]["vmc_master_comando_non_eseguito"]
    assert helper["initial"] == "" and helper["max"] == 255
    assert NON_ESEGUITO in pkg["recorder"]["exclude"]["entities"]
    pulizia = next(s for s in pkg["script"].values() if s.get("alias") == "VMC Master - Pulisci cronologia Entità")
    assert NON_ESEGUITO in pulizia["sequence"][0]["data"]["entity_id"]
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    elenco = scheda[scheda.index("{%- set elenco = [") :]
    assert f"'{NON_ESEGUITO}'" in elenco[: elenco.index("] -%}")]


# ------------------------------------------------------------------ P: le allerte aspettano il ritorno della Fascia
def test_trigger_delle_allerte_aspettano_il_ritorno_della_fascia() -> None:
    """Classe intera: 118 trigger chiedono le 8 spie del Black-Out spente; i 99 che comandano la VMC chiedono anche la
    Spia Black-Out del Calendario spenta, in «and» subito dopo il blocco; i 19 che non la comandano (notifiche, errori
    delle entità, avvisi, nome, aggiornamenti) no."""
    con_blocco, con_guardia = [], []
    for t in _automazione()["triggers"]:
        testo = str(t.get("value_template", ""))
        if all(re.search(r"vmc_master_spia_velocita_" + s + r"'\)\s*==\s*'off'", testo) for s in SPIE_BLACK_OUT):
            con_blocco.append(str(t["id"]))
            if GUARDIA in testo:
                con_guardia.append(str(t["id"]))
                assert testo.count(GUARDIA) == 1, t["id"]
                assert re.search(r"vmc_master_spia_velocita_\w+'\)\s*==\s*'off' and " + re.escape(GUARDIA), testo), t["id"]
    assert len(con_blocco) == 118 and len(con_guardia) == 99
    assert set(con_blocco) - set(con_guardia) == SENZA_GUARDIA


async def test_guardia_ferma_il_trigger_durante_il_ritorno_della_fascia(hass: HomeAssistant) -> None:
    """Sul trigger vero «PdR Vel. 1-> Imposta Velocità 0»: con le condizioni dell'allerta vere scatta solo con la Spia
    Black-Out del Calendario spenta."""
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == "PdR Vel. 1-> Imposta Velocità 0"]
    t = Template(trigger["value_template"], hass)
    for nome, valore in (("sensor.vmc_master_punto_di_rugiada_verifica_confronto", "Se ne sconsiglia l'impiego"),
                         ("input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_pdr", "on"), (LETTURA, "Velocità 1"),
                         (LETTURA + "_interfaccia", "Velocità 1"), ("input_boolean.vmc_master_spia_co2_o_voc", "off"),
                         ("input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia", "off"),
                         ("input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia", "off"),
                         ("sensor.vmc_master_status_ip_interfaccia", "ON-Line"),
                         ("input_number.vmc_master_fase_riallineamento_al_riavvio", "0")):
        hass.states.async_set(nome, valore)
    for s in SPIE_BLACK_OUT:
        hass.states.async_set(f"input_boolean.vmc_master_spia_velocita_{s}", "off")
    hass.states.async_set(CAL_BLACK_OUT, "off")
    assert result_as_boolean(t.async_render()) is True
    hass.states.async_set(CAL_BLACK_OUT, "on")
    assert result_as_boolean(t.async_render()) is False


# ------------------------------------------------------------------ ritorno dopo un Black-Out in Fascia con Congelamento/Δ
def _rami_ritorno_black_out() -> dict[str, list[Any]]:
    return {r["conditions"][0]["id"]: r["sequence"] for b in _automazione()["actions"] if isinstance(b, dict)
            for r in b.get("choose", []) if r["conditions"][0].get("id") in
            ("calendario_ritorno_da_black_out", "calendario_ritorno_da_black_out_riallineamento")}


def test_ritorno_dopo_black_out_con_congelamento_aspetta_la_fine_dell_allerta() -> None:
    """Classe intera (i 2 rami che fanno ripartire la Fascia al ritorno della corrente): subito prima della scelta della
    Fascia, con Congelamento o Δ Temp. in corso si accende la Spia Comando non eseguito del Calendario e il ramo si ferma
    (lo script della Fascia la spegnerebbe e non comanderebbe: le sue opzioni chiedono Congelamento e Δ Temp. assenti)."""
    rami = _rami_ritorno_black_out()
    assert len(rami) == 2
    for nome, passi in rami.items():
        k = next(i for i, p in enumerate(passi) if "choose" in p)
        passo = passi[k - 1]
        assert passo["then"] == [{"data": {}, "target": {"entity_id": CAL_NON_ESEGUITO}, "action": "input_boolean.turn_on"},
                                 {"stop": "Fascia rimandata alla fine dell'allerta Congelamento o Δ Temp."}], nome
        assert sum("Fascia rimandata" in str(p) for p in passi) == 1, nome


@pytest.mark.parametrize("ramo", ["calendario_ritorno_da_black_out", "calendario_ritorno_da_black_out_riallineamento"])
async def test_condizione_del_rinvio_della_fascia(hass: HomeAssistant, ramo: str) -> None:
    passi = _rami_ritorno_black_out()[ramo]
    k = next(i for i, p in enumerate(passi) if "choose" in p)
    cond = Template(passi[k - 1]["if"][0]["value_template"], hass)
    CONG = "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia"
    DELTA = "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia"

    def rinvia(cong: str, delta: str, spia: str | None) -> bool:
        hass.states.async_set(CONG, cong)
        hass.states.async_set(DELTA, delta)
        for s in SPIE_FASCIA:
            hass.states.async_set(s, "on" if s == spia else "off")
        return result_as_boolean(cond.async_render())

    assert rinvia("off", "off", SPIE_FASCIA[0]) is False  # nessuna allerta: la Fascia riparte subito
    for spia in SPIE_FASCIA:
        assert rinvia("on", "off", spia) is True
        assert rinvia("off", "on", spia) is True
    assert rinvia("on", "on", None) is False  # nessuna Fascia: niente da rimandare


@pytest.mark.parametrize(("cong", "delta", "fascia_riparte"), [
    ("off", "off", True),  # nessuna allerta: la Fascia riparte subito (come nella b38)
    ("on", "off", False),  # Congelamento in corso: Fascia rimandata alla fine dell'allerta
    ("off", "on", False),  # Δ Temp. in corso: idem
])
async def test_ritorno_della_fascia_con_congelamento_o_delta(hass: HomeAssistant, cong: str, delta: str,
                                                            fascia_riparte: bool) -> None:
    """Il ramo vero eseguito da Home Assistant (stesso banco di prova del ritorno della Fascia della b36): con Congelamento
    o Δ Temp. in corso lo script della Fascia non parte, la Spia Comando non eseguito del Calendario si accende (a fine
    allerta il Congelamento OFF / Δ Temp. OFF fa ripartire la Fascia) e nessun comando va alla VMC."""
    import time

    from tests.test_b35_allerte import IP, LETTURA, _ramo, _spente
    from tests.test_b36_allerte import CALENDARIO, _esegui, _stato
    adesso = time.time()
    chiamati: list[str] = []

    async def _script(call: Any) -> None:
        chiamati.append(call.service)

    hass.services.async_register("script", "vmc_master_calendario_fascia_1_on", _script)
    hass.services.async_register("script", "vmc_master_calendario_fascia_2_on", _script)
    stati = {CAL_BLACK_OUT: "on", "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_calendario": "on",
             LETTURA + "_interfaccia": "Velocità 1", **_spente(CALENDARIO), CAL_NON_ESEGUITO: "off",
             "input_boolean.vmc_master_spia_calendario_sabato_2": "on",
             "input_boolean.vmc_master_congelamento_verifica_soglia_valore_spia": cong,
             "input_boolean.vmc_master_delta_temp_verifica_soglia_valore_spia": delta}
    hass.states.async_set(IP, "ON-Line", timestamp=adesso - 32)
    hass.states.async_set(LETTURA, "Velocità 1", timestamp=adesso - 10)
    comandi = await _esegui(hass, _ramo("calendario_ritorno_da_black_out")["sequence"], stati, attesa=0.5)
    assert comandi == []
    assert chiamati == (["vmc_master_calendario_fascia_2_on"] if fascia_riparte else [])
    assert _stato(hass, CAL_BLACK_OUT) == "off"
    assert _stato(hass, CAL_NON_ESEGUITO) == ("off" if fascia_riparte else "on")


# ------------------------------------------------------------------ fine Δ Temp. con il comando dell'allerta non eseguito
async def test_fine_delta_velocita_vecchia_non_e_una_scelta(hass: HomeAssistant, freezer) -> None:
    """Simulazione OF «DON M E» (porta 5001 muta in Fascia, Δ Temp. finito durante l'interruzione): la Velocità 1 del Δ
    non è arrivata, la velocità letta è ancora quella di prima e a fine Δ la regola D6 la prendeva per una scelta
    dell'utente (nessun ripristino, nessun ciclo): restava il Comando non eseguito della Velocità 1, rimandato al ritorno
    della lettura. Ora con un Comando non eseguito e la velocità non cambiata da allora non è una scelta (ripristino, il
    cui ciclo annulla il comando vecchio); una velocità cambiata dopo resta una scelta."""
    (ramo,) = [r for b in _automazione()["actions"] if isinstance(b, dict) for r in b.get("choose", [])
               if r["conditions"][0].get("id") == ["delta_temp_OFF"]]
    (passo,) = [p for p in ramo["sequence"] if "if" in p and "vel_fine_delta in" in str(p["if"])]
    cond = Template(passo["if"][0]["value_template"], hass)

    def scelta(vel_fine: str) -> bool:
        return result_as_boolean(cond.async_render({"vel_fine_delta": vel_fine}))

    hass.states.async_set(LETTURA, "Velocità 2")
    hass.states.async_set(NON_ESEGUITO, "")
    assert scelta("Velocità 2") is True  # nessun comando in sospeso: D6 come nella b38
    freezer.tick(timedelta(seconds=35))
    hass.states.async_set(NON_ESEGUITO, f"Velocità 1|{dt_util.as_timestamp(dt_util.utcnow()):.1f}")
    assert scelta("Velocità 2") is False  # velocità vecchia: non è una scelta
    freezer.tick(timedelta(seconds=5))
    hass.states.async_set(LETTURA, "Velocità 3")  # scelta dell'utente dopo il comando non eseguito
    assert scelta("Velocità 3") is True
    assert scelta("Velocità 1") is False  # la Velocità 1 non è mai una scelta (D6)


# ------------------------------------------------------------------ fine Fascia durante il Black-Out con Inquinanti in corso
def _rami_fine_fascia() -> dict[str, list[dict[str, Any]]]:
    return {r["conditions"][0]["id"]: r["sequence"] for b in _automazione()["actions"] if isinstance(b, dict)
            for r in b.get("choose", [])
            if isinstance(r.get("conditions"), list) and r["conditions"] and isinstance(r["conditions"][0], dict)
            and re.fullmatch(r"[12]° \w+ Off", str(r["conditions"][0].get("id", "")))}


def test_fine_fascia_con_black_out_un_solo_riavvio_degli_inquinanti() -> None:
    """Famiglie Black-Out C5c (16 sbagliati sulla b39 0cf0dd4, giusti sulla b38): Black-Out in Fascia, la Fascia finisce
    durante il Black-Out, Inquinanti in corso. Al ritorno il ramo di fine Fascia azzera le spie (Spia Black-Out del
    Calendario compresa) e riarma gli Inquinanti (Spia CO₂/VOC ON): partivano insieme «Spia Velocità 0 CO₂/VOC» (V1,
    Velocità Registrata 0) e l'avvio degli Inquinanti, sbloccato dalla Spia Black-Out spenta (classe P), che vedeva V1 e
    cancellava la Velocità Registrata: a fine Inquinanti la VMC restava a V1 invece di tornare a V0. Classe intera (14 rami
    di fine Fascia): la Spia Black-Out si legge all'inizio del ramo e con la Spia accesa il riarmo non si fa (riparte solo
    l'avvio degli Inquinanti, una volta, come nella b38)."""
    rami = _rami_fine_fascia()
    assert len(rami) == 14
    for nome, passi in rami.items():
        k_var = [i for i, p in enumerate(passi) if "black_out_durante_la_fascia" in p.get("variables", {})]
        assert len(k_var) == 1, nome
        assert passi[k_var[0]]["variables"]["black_out_durante_la_fascia"] == (
            "{{ is_state('input_boolean.vmc_master_spia_calendario_black_out', 'on') }}"), nome
        k_riarmo = [i for i, p in enumerate(passi) if "if" in p and "vmc_master_spia_co2_o_voc" in str(p.get("then"))]
        assert len(k_riarmo) == 1, nome
        assert k_var[0] < k_riarmo[0], nome
        assert passi[k_riarmo[0]]["if"][0]["value_template"].rstrip().endswith("and not black_out_durante_la_fascia }}"), nome
        # la Spia si legge prima di ogni comando e prima delle spie azzerate dallo script di fine Fascia
        primi = [i for i, p in enumerate(passi) if "repeat" in p or "fascia_1_o_2_off" in str(p.get("action", ""))]
        assert primi and k_var[0] < min(primi), nome


async def test_condizione_del_riarmo_degli_inquinanti_a_fine_fascia(hass: HomeAssistant) -> None:
    passi = _rami_fine_fascia()["1° Giovedì Off"]
    (riarmo,) = [p for p in passi if "if" in p and "vmc_master_spia_co2_o_voc" in str(p.get("then"))]
    cond = Template(riarmo["if"][0]["value_template"], hass)
    hass.states.async_set("sensor.vmc_master_alert_monitoraggio_co2", "Allerta")
    hass.states.async_set("sensor.vmc_master_alert_monitoraggio_voc", "Nessuna Allerta")
    hass.states.async_set("input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_co2_e_voc", "on")
    assert result_as_boolean(cond.async_render({"black_out_durante_la_fascia": False})) is True   # come nella b38
    assert result_as_boolean(cond.async_render({"black_out_durante_la_fascia": True})) is False   # riparte l'avvio
    hass.states.async_set("sensor.vmc_master_alert_monitoraggio_co2", "Nessuna Allerta")
    assert result_as_boolean(cond.async_render({"black_out_durante_la_fascia": False})) is False
