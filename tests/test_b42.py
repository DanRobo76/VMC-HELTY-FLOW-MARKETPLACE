"""Prove della 9.0.0b42: le finestre della scheda non si riaprono e richiudono più a vicenda senza fine.

Difetto (b41): l'«Automazione VMC Master» è «mode: queued» e per ogni finestra della scheda (input_boolean
vmc_master_opzioni_*, vmc_master_opzione_finestra_*, vmc_master_conferma_pulizia_cronologia) ha un trigger di stato
«... On» (off -> on) e uno «... Off» (on -> off). Il ramo «On» apre la propria finestra e chiude le altre, il ramo «Off»
chiude la propria (e le sue sotto-finestre). Un evento arrivato mentre l'automazione è occupata si esegue più tardi,
quando la finestra può essere già cambiata di nuovo: il ramo «On» vecchio la riapre, il ramo «Off» vecchio la
richiude, ogni cambio accoda un altro evento e il ciclo non finisce più nello stesso istante (CPU al 100 %, memoria di
Home Assistant che cresce). Correzione (b42): ognuno dei 35 rami delle finestre (18 «On» + 17 «Off») si esegue solo se
la finestra è ancora nello stato del suo trigger quando arriva il suo turno (condizione «Finestra ancora aperta/chiusa
al turno di questo evento» nell'opzione del choose). Stessa classe: «VMC Master - Esclusività Finestre Opzioni»
(queued, chiude soltanto) ha la stessa condizione nelle sue 4 opzioni (nella 657227e era una condizione
dell'automazione: Home Assistant la valuta quando il trigger scatta, prima della coda, e al turno di un evento vecchio
non proteggeva). Gemello: i 2 rami «Disattivazione Umidità Limite» (trigger di stato on -> off dell'interruttore
Umidità) si eseguono solo se l'interruttore è ancora spento (sulla b41 un evento vecchio, con l'interruttore già
riacceso, spegneva l'allerta Umidità e mandava la Velocità 0). Corsa (80c9e80): i 3 rami «Off» con più entità
(Monitoraggio, Opzioni, Avvisi) chiudono solo le sotto-finestre, non la propria, già chiusa: con più entità Home
Assistant scrive un giro del ciclo dopo la guardia e richiudeva la finestra riaperta in quel giro.

Prova statica (classe intera, tutto il package come arriva nell'HA dell'utente, vmc_master.yaml e l'automazione senza
le sezioni CLONA e INSTALLA come fa l'installatore, e anche il file completo con le sezioni solo Master):
- ogni trigger di stato su una finestra o su un interruttore di funzione (input_boolean.vmc_master_opzioni_accendi_
  spegni_*), in ogni automazione, ha la guardia valutata al turno dell'evento (condizione di stato nella stessa opzione
  del choose, o la condizione «is_state(trigger.entity_id, trigger.to_state.state)» nell'opzione o tra le azioni prima
  del choose). Una condizione a livello di automazione NON vale come guardia e nessuna automazione la usa: Home
  Assistant la valuta quando il trigger scatta, prima della coda (AutomationEntity.async_trigger), non al turno;
- nessun ramo apre una finestra diversa dalla propria, e la propria solo con la guardia;
- controllo generale: nessun ciclo tra trigger di stato e scritture degli aiutanti in tutto il package (un ramo che
  scrive un'entità su cui scatta un trigger di stato, anche di un'altra automazione), contando come nessun cambio la
  scrittura che porta l'entità nello stato già garantito dalla guardia; restano solo i cicli ammessi, contati;
- il package scritto dall'installatore (genera_file, VMC Master e un'altra VMC) passa la convalida di Home Assistant
  (async_validate_config_item di tutte le automazioni e gli script, modelli degli altri domini compilati), e le righe
  che rimuovi_clona cancella intere sono voci intere (nella b032d06 12 modelli della principale installata erano
  rotti: rimuovi_clona toglieva la riga della finestra Clona, che chiudeva la lista con «])»; corretti nella d254602).

Prova dinamica (Home Assistant vero, orologio controllato): l'Automazione VMC Master vera (il file del package
completo, tutte le 18 finestre con trigger) e «VMC Master - Esclusività Finestre Opzioni» con gli input_boolean veri del
package; i tocchi arrivano a «raffica» (più servizi nello stesso istante, prima che l'automazione elabori il primo
evento, come tocchi veloci sulla scheda), con l'automazione libera e con l'automazione davvero occupata (un'esecuzione
lunga in corso: la rilettura della velocità allo scadere di un'attesa, b38, che aspetta la lettura nuova fino a 2 s).
Ogni raffica deve finire: oltre TETTO_CAMBI cambi di stato delle finestre nello stesso istante la prova spegne subito le
automazioni e fallisce con «ciclo senza fine» (sulla b41 il ciclo non finirebbe e la memoria crescerebbe). Gemello:
interruttore Umidità spento e riacceso, con l'allerta Umidità in corso, mentre l'automazione è occupata. Corsa: ognuna
delle 17 finestre con il ramo «Off», aperta prima, chiusa e riaperta nello stesso istante, resta aperta.

Regola b42 dello stato finale (misurata con Home Assistant 2026.11.2):
- una sola finestra, anche toccata più volte nello stesso istante: vince l'ultimo tocco; ogni evento vecchio trova la
  finestra in un altro stato e non fa niente;
- due finestre che si chiudono a vicenda, aperte nello stesso istante (Avvisi e Telecomando; Opzioni e la sua
  sotto-finestra Audio) con l'automazione occupata: resta aperta la prima elaborata, cioè la prima toccata. Il suo
  evento è il primo della coda e chiude la seconda, già aperta (anche con la variante «vince l'ultimo tocco»: nello
  stesso istante il last_changed della seconda è uguale a quello dell'evento e il confronto è «le»); l'evento di
  apertura della seconda, al suo turno, la trova chiusa e non fa niente. Con l'automazione libera il primo evento parte
  subito: senza la variante la chiusura di più finestre insieme aspetta un giro del ciclo, in cui arrivano anche gli
  altri tocchi, e chiude anche la seconda (resta la prima); con la variante il modello del turn_off è reso prima che
  arrivino gli altri tocchi (resta l'ultima toccata, come con i tocchi lenti);
- di due finestre che si chiudono a vicenda (65 coppie: le 6 finestre principali tra loro, le sotto-finestre di
  Opzioni e dei Sensori, Tempi di Attesa e Timer Lettura Dati VMC dell'Esclusività) alla fine ne resta aperta al
  massimo una, quindi al massimo una finestra principale; una finestra chiusa dal suo ultimo tocco resta chiusa;
  nessuna finestra si apre da sola.
Sulla b41 entrano nel ciclo senza fine gli scenari a, c, d, e con l'automazione libera e a, b, c, d, e con
l'automazione occupata (b con l'automazione libera finisce: l'evento di apertura si esegue subito, a finestra aperta),
e la prima raffica casuale.

Variante «vince l'ultimo tocco» (commit b032d06 e d254602, in attesa della scelta del proprietario; prove nella sola
classe TestVarianteVinceLUltimoTocco): nei 18 rami «On» della principale e nelle 4 opzioni dell'Esclusività il
turn_off chiude solo le finestre accese con last_changed non successivo a quello dell'evento. Con l'automazione occupata
e due finestre toccate in istanti diversi resta aperta l'ultima toccata (Avvisi poi Telecomando: Telecomando; Opzioni
poi Audio: tutte e due); nello stesso istante con l'automazione occupata resta la prima elaborata, come sopra. Se il
proprietario sceglie «resta la prima» si tolgono la classe e i due commit: le altre prove valgono anche senza la
variante (verificate sulla 68e159c con la correzione 80c9e80 dei rami «Off»)."""

from __future__ import annotations

import asyncio
import random
import re
from collections.abc import AsyncIterator, Collection, Iterator, Sequence
from dataclasses import dataclass, field
from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

import probatio
import pytest
from homeassistant.components.automation.config import async_validate_config_item as valida_automazione
from homeassistant.components.script.config import async_validate_config_item as valida_script
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError, TemplateError
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from homeassistant.util import yaml as hay
from pytest_homeassistant_custom_component.common import async_fire_time_changed, async_mock_service

from custom_components.vmc_master import trasforma
from custom_components.vmc_master.installatore import genera_file

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
PRINCIPALE = "Automazione VMC Master"
ESCLUSIVITA = "VMC Master - Esclusività Finestre Opzioni"
INSTALLA_FINESTRE = "VMC Master - Installa VMC Finestre"
# finestre della scheda; gli interruttori di funzione input_boolean.vmc_master_opzioni_accendi_spegni_* non lo sono
FINESTRA = re.compile(r"^input_boolean\.vmc_master_(opzioni_(?!accendi_spegni_)[a-z_]+|opzione_finestra_[a-z_]+"
                      r"|conferma_pulizia_cronologia)$")
IB = "input_boolean.vmc_master_"
FINESTRE_PRINCIPALI = [IB + n for n in ("opzioni_vmc", "opzioni_monitoraggio_sensori", "opzioni_offset_sensori",
                                        "opzioni_avvisi", "opzioni_lettura_sensori", "opzioni_interruttore_calendario")]
# interruttori di funzione con trigger di stato: lo stesso difetto se il ramo si esegue con l'interruttore già cambiato
INTERRUTTORE = re.compile(r"^input_boolean\.vmc_master_opzioni_accendi_spegni_[a-z0-9_]+$")
CLASSI = {"finestre": FINESTRA, "interruttori": INTERRUTTORE}
# guardia generica (l'entità del trigger è ancora nello stato «to» del trigger), nelle due forme usate
GUARDIE_TEMPLATE = {
    "{{ is_state(trigger.entity_id, trigger.to_state.state) }}",
    "{{ trigger.to_state is not none and is_state(trigger.entity_id, trigger.to_state.state) }}",
}


# ------------------------------------------------------------------------------------------------ caricamento
_CACHE: dict[tuple[str, bool], Any] = {}


def _carica(nome: str, installato: bool) -> Any:
    """File del package: installato = come arriva nell'HA dell'utente (senza le sezioni CLONA e INSTALLA, come fa
    l'installatore anche per la VMC Master); altrimenti il file completo, con le sezioni solo Master."""
    if (nome, installato) not in _CACHE:
        testo = (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")
        if installato:
            testo = trasforma.rimuovi_sezioni_solo_master(testo)
        _CACHE[nome, installato] = hay.parse_yaml(testo)
    return _CACHE[nome, installato]


def _automazioni(installato: bool) -> list[dict[str, Any]]:
    """Tutte le automazioni del package: l'Automazione VMC Master e quelle di vmc_master.yaml."""
    return [_carica("vmc_master_automazione.txt", installato), *_carica("vmc_master.yaml", installato)["automation"]]


def _automazione(alias: str, installato: bool = False) -> dict[str, Any]:
    (trovata,) = [a for a in _automazioni(installato) if a["alias"] == alias]
    return trovata


# ------------------------------------------------------------------------------------------------ struttura
def _entita(valore: Any) -> list[str]:
    """Entità di un entity_id (stringa, elenco o modello: in un modello tutte le entità nominate)."""
    if isinstance(valore, list):
        return [e for v in valore for e in _entita(v)]
    if isinstance(valore, str):
        if "{" in valore:
            return re.findall(r"\b[a-z_]+\.vmc_master_[a-z0-9_]+", valore)
        return [v.strip() for v in valore.split(",") if v.strip()]
    return []


def _bersagli(passo: dict[str, Any]) -> list[str]:
    out = _entita(passo.get("entity_id"))
    for chiave in ("target", "data"):
        if isinstance(passo.get(chiave), dict):
            out += _entita(passo[chiave].get("entity_id"))
    return out


def _trigger_di_stato(auto: dict[str, Any]) -> Iterator[tuple[int, dict[str, Any], list[str]]]:
    for i, t in enumerate(auto.get("triggers") or []):
        if t.get("trigger") == "state":
            yield i, t, _entita(t.get("entity_id"))


def _id_trigger(condizioni: Any) -> set[str]:
    """Id dei trigger delle condizioni «trigger», anche dentro «and» e «or»."""
    ids: set[str] = set()
    for c in condizioni if isinstance(condizioni, list) else [condizioni]:
        if isinstance(c, dict) and c.get("condition") == "trigger":
            ids |= {str(i).strip() for i in (c["id"] if isinstance(c["id"], list) else [c["id"]])}
        elif isinstance(c, dict) and c.get("condition") in ("and", "or"):
            ids |= _id_trigger(c.get("conditions"))
    return ids


def _rami(auto: dict[str, Any]) -> Iterator[tuple[set[str] | None, list[Any], Any]]:
    """(id dei trigger, condizioni, sequenza) per ogni opzione dei choose tra le azioni di primo livello; un'automazione
    senza choose è un solo ramo, valido per tutti i trigger (id None)."""
    azioni = auto.get("actions") or []
    scelte = [a for a in azioni if isinstance(a, dict) and "choose" in a]
    if not scelte:
        yield None, [], azioni
        return
    for blocco in scelte:
        for opzione in blocco["choose"]:  # un'opzione senza condizione trigger vale per tutti i trigger
            yield _id_trigger(opzione.get("conditions")) or None, opzione.get("conditions") or [], opzione.get("sequence")
        if "default" in blocco:
            yield None, [], blocco["default"]


def _rami_del_trigger(auto: dict[str, Any], trigger: dict[str, Any]) -> list[tuple[list[Any], Any]]:
    """Rami che il trigger può eseguire (un trigger senza id tutti)."""
    tid = str(trigger.get("id", "")).strip()
    return [(cond, seq) for ids, cond, seq in _rami(auto) if ids is None or not tid or tid in ids]


def _guardia_template(condizione: Any) -> bool:
    return (isinstance(condizione, dict) and condizione.get("condition") == "template"
            and re.sub(r"\s+", " ", str(condizione.get("value_template", ""))).strip() in GUARDIE_TEMPLATE)


def _guardie_di_stato(condizioni: list[Any]) -> set[tuple[str, str]]:
    """(entità, stato) delle condizioni di stato di un'opzione."""
    return {(e, c["state"]) for c in condizioni if isinstance(c, dict) and c.get("condition") == "state"
            and isinstance(c.get("state"), str) for e in _entita(c.get("entity_id"))}


def _guardia_tra_le_azioni(auto: dict[str, Any]) -> bool:
    """La guardia generica come passo «condition» tra le azioni di primo livello, prima del primo choose."""
    for passo in auto.get("actions") or []:
        if isinstance(passo, dict) and "choose" in passo:
            return False
        if _guardia_template(passo):
            return True
    return False


def _guardato(auto: dict[str, Any], trigger: dict[str, Any], finestre: list[str]) -> bool:
    """Ogni ramo del trigger si esegue solo se ognuna delle sue finestre è ancora nello stato del trigger al turno
    dell'evento. Le condizioni dell'automazione («conditions» di primo livello) non contano: sono valutate quando il
    trigger scatta, prima della coda."""
    if _guardia_tra_le_azioni(auto):
        return True
    rami = _rami_del_trigger(auto, trigger)
    verso = trigger.get("to")
    return bool(rami) and all(
        any(_guardia_template(c) for c in cond)
        or (isinstance(verso, str) and all((f, verso) in _guardie_di_stato(cond) for f in finestre))
        for cond, _ in rami)


def _censimento_guardie(installato: bool, classe: re.Pattern[str]) -> dict[str, tuple[int, int, list[str]]]:
    """Per ogni automazione con trigger di stato sulle entità della classe: (numero di trigger, numero di rami che
    possono eseguire, id dei trigger senza guardia)."""
    out: dict[str, tuple[int, int, list[str]]] = {}
    for auto in _automazioni(installato):
        trovati = [(t, [e for e in ent if classe.match(e)]) for _, t, ent in _trigger_di_stato(auto)]
        trovati = [(t, f) for t, f in trovati if f]
        if trovati:
            rami = {id(seq) for t, _ in trovati for _, seq in _rami_del_trigger(auto, t)}
            out[auto["alias"]] = (len(trovati), len(rami), [str(t.get("id")).strip() for t, f in trovati
                                                            if not _guardato(auto, t, f)])
    return out


# (trigger, rami) misurati sulla b42; sulla b41 nessuno era guardato (principale 35/35 finestre, Umidità 1/1)
FISSATI_GUARDIE = {
    "finestre": {
        False: {PRINCIPALE: (35, 35), ESCLUSIVITA: (6, 4), INSTALLA_FINESTRE: (2, 1)},  # file completo
        True: {PRINCIPALE: (33, 33), ESCLUSIVITA: (6, 4)},  # installato: senza i 2 trigger della finestra Clona
    },
    # «Disattivazione Umidità Limite»: l'unico trigger di stato su un interruttore di funzione, 2 rami
    "interruttori": {False: {PRINCIPALE: (1, 2)}, True: {PRINCIPALE: (1, 2)}},
}
GUARDIE_ESCLUSE = {
    INSTALLA_FINESTRE: "sezione INSTALLA, solo Master: rimuovi_sezioni_solo_master la toglie sempre, anche per la VMC "
                       "Master, quindi non arriva mai in Home Assistant; chiude soltanto (nessun ciclo possibile)",
}


@pytest.mark.parametrize("classe", list(CLASSI))
@pytest.mark.parametrize("installato", [True, False], ids=["installato", "file_completo"])
def test_guardia_al_turno_dell_evento(installato: bool, classe: str) -> None:
    """Classe intera: in ogni automazione del package ogni trigger di stato su una finestra della scheda o su un
    interruttore di funzione ha la guardia «ancora nello stato del trigger» valutata al turno dell'evento, in ogni ramo
    che può eseguire. Finestre: principale 35 trigger in 35 rami (18 «On» + 17 «Off»; «Opzioni Sub Conferma Pulizia On»
    non ha «Off»), installata 33 (la finestra Clona è nella sezione CLONA, solo Master); Esclusività 6 trigger nelle 4
    opzioni del choose. Interruttori: «Disattivazione Umidità Limite» nei suoi 2 rami (condizione di stato «off»).
    Trovati, corretti ed esclusi sono contati; esclusi: GUARDIE_ESCLUSE (mai in Home Assistant)."""
    censimento = _censimento_guardie(installato, CLASSI[classe])
    assert {a: (n, r) for a, (n, r, _) in censimento.items()} == FISSATI_GUARDIE[classe][installato]
    senza = {a: ids for a, (_, _, ids) in censimento.items() if ids}
    esclusi = {a for a in GUARDIE_ESCLUSE if a in censimento}
    assert set(senza) == esclusi, senza
    for alias in esclusi:  # le automazioni escluse non hanno nessun trigger guardato
        assert len(senza[alias]) == censimento[alias][0], (alias, senza[alias])


@pytest.mark.parametrize("installato", [True, False], ids=["installato", "file_completo"])
def test_nessuna_guardia_tra_le_condizioni_dell_automazione(installato: bool) -> None:
    """Nessuna automazione usa come condizione di primo livello («conditions» dell'automazione) la guardia sull'entità
    del trigger (modello «is_state(trigger.entity_id, ...)» o condizione di stato su una sua finestra o interruttore):
    Home Assistant la valuterebbe quando il trigger scatta, prima della coda, e al turno di un evento vecchio non
    proteggerebbe (era il caso dell'Esclusività nella 657227e)."""
    trovate: dict[str, list[Any]] = {}
    for auto in _automazioni(installato):
        comandi = {e for _, _, ent in _trigger_di_stato(auto) for e in ent if FINESTRA.match(e) or INTERRUTTORE.match(e)}
        for c in auto.get("conditions") or []:
            testo = re.sub(r"\s+", "", str(c.get("value_template", ""))) if isinstance(c, dict) else ""
            if isinstance(c, dict) and ("is_state(trigger.entity_id" in testo or (
                    c.get("condition") == "state" and comandi & set(_entita(c.get("entity_id"))))):
                trovate.setdefault(auto["alias"], []).append(c.get("alias") or c.get("condition"))
    assert not trovate, trovate


def test_guardie_forma_esatta() -> None:
    """Principale: ogni trigger di finestra ha un solo ramo; la guardia è la seconda condizione, subito dopo la
    condizione trigger, con l'alias «Finestra ancora aperta/chiusa ...» (rami «On»/«Off») o «Riquadro di conferma
    ancora aperto ...» (Conferma Pulizia); 18 rami «On» e 17 «Off». Esclusività: nelle 4 opzioni del choose la seconda
    condizione è il modello «trigger.to_state is not none and is_state(trigger.entity_id, trigger.to_state.state)» e
    l'automazione non ha condizioni di primo livello. Umidità: nei 2 rami «Disattivazione Umidità Limite» la seconda
    condizione è l'interruttore ancora «off»."""
    auto = _automazione(PRINCIPALE)
    versi = {"on": 0, "off": 0}
    for _, t, ent in _trigger_di_stato(auto):
        if not any(FINESTRA.match(e) for e in ent):
            continue
        (finestra,) = ent
        (ramo,) = [cond for cond, _ in _rami_del_trigger(auto, t)]
        assert ramo[0]["condition"] == "trigger", t["id"]
        assert len(ramo) > 1 and ramo[1].get("condition") == "state", f"{t['id']}: manca la guardia"
        guardia = ramo[1]
        assert {k: guardia[k] for k in ("condition", "entity_id", "state")} == {
            "condition": "state", "entity_id": finestra, "state": t["to"]}, t["id"]
        inizio = {"on": "Finestra ancora aperta", "off": "Finestra ancora chiusa"}[t["to"]]
        if finestra == IB + "conferma_pulizia_cronologia":
            inizio = "Riquadro di conferma ancora aperto"
        assert guardia["alias"].startswith(inizio + " al turno di questo evento [b42:"), t["id"]
        versi[t["to"]] += 1
    assert versi == {"on": 18, "off": 17}

    esclusivita = _automazione(ESCLUSIVITA)
    assert "conditions" not in esclusivita and esclusivita["mode"] == "queued"
    (blocco,) = esclusivita["actions"]
    assert len(blocco["choose"]) == 4 and "default" not in blocco
    for opzione in blocco["choose"]:
        prima, guardia = opzione["conditions"][:2]
        assert prima["condition"] == "trigger"
        assert re.sub(r"\s+", " ", guardia["value_template"]).strip() == (
            "{{ trigger.to_state is not none and is_state(trigger.entity_id, trigger.to_state.state) }}")
        assert guardia["alias"].startswith("Finestra (o scheda) ancora nello stato che ha fatto scattare il trigger "
                                           "al turno di questo evento [b42:")

    (trigger_umidita,) = [t for _, t, ent in _trigger_di_stato(auto) if any(INTERRUTTORE.match(e) for e in ent)]
    assert (trigger_umidita["entity_id"], trigger_umidita["from"], trigger_umidita["to"]) == (
        [IB + "opzioni_accendi_spegni_vmc_vs_umidita"], "on", "off")
    rami = [cond for cond, _ in _rami_del_trigger(auto, trigger_umidita)]
    assert len(rami) == 2
    for cond in rami:
        assert {k: cond[1][k] for k in ("condition", "entity_id", "state")} == {
            "condition": "state", "entity_id": IB + "opzioni_accendi_spegni_vmc_vs_umidita", "state": "off"}
        assert cond[1]["alias"].startswith("Interruttore Umidità ancora spento al turno di questo evento [b42:")


# ------------------------------------------------------------------------------------------------ aperture
APERTURE = re.compile(r"^(input_boolean|homeassistant)\.(turn_on|toggle)$")
APERTURE_AMMESSE = {
    ("script.vmc_master_profilo_inizializzazione", IB + "opzioni_offset_sensori"):
        "script avviato dall'utente dalla scheda (Profilo Inizializzazione), nessuna automazione lo chiama: apre il "
        "pannello Opzioni una volta, come un tocco",
}


def _aperture(nodo: Any) -> Iterator[tuple[str, str]]:
    """(servizio, finestra) per ogni passo che può aprire una finestra (turn_on o toggle)."""
    if isinstance(nodo, dict):
        azione = nodo.get("action")
        if isinstance(azione, str) and APERTURE.match(azione.strip()):
            for e in _bersagli(nodo):
                if FINESTRA.match(e):
                    yield azione.strip(), e
        for v in nodo.values():
            yield from _aperture(v)
    elif isinstance(nodo, list):
        for v in nodo:
            yield from _aperture(v)


@pytest.mark.parametrize(("installato", "proprie"), [(True, 16), (False, 17)], ids=["installato", "file_completo"])
def test_nessun_ramo_apre_un_altra_finestra(installato: bool, proprie: int) -> None:
    """Controllo che rende impossibile il ritorno del ciclo: in tutto il package (automazioni e script) una finestra si
    apre (turn_on o toggle) solo nel ramo «On» del suo trigger e con la guardia «finestra ancora aperta» (17 rami «On»
    nel file completo, 16 installato senza Clona; Conferma Pulizia non si riapre), più le aperture dell'utente in
    APERTURE_AMMESSE. Nessun ramo attivato da una finestra apre un'altra finestra; quindi nessuna esecuzione vecchia
    può riaprire una finestra già richiusa."""
    proprie_trovate, altre = 0, {}
    for auto in _automazioni(installato):
        trigger_di_finestra = {str(t.get("id")).strip(): (t, ent) for _, t, ent in _trigger_di_stato(auto)
                               if any(FINESTRA.match(e) for e in ent)}
        nei_rami = 0
        for ids, cond, seq in _rami(auto):
            for azione, finestra in _aperture(seq):
                nei_rami += 1
                mie = [trigger_di_finestra[i] for i in (ids or set()) if i in trigger_di_finestra]
                if (len(mie) == 1 and mie[0][1] == [finestra] and mie[0][0].get("to") == "on"
                        and (finestra, "on") in _guardie_di_stato(cond) and azione == "input_boolean.turn_on"):
                    proprie_trovate += 1
                else:
                    altre[f"automation.{auto.get('id', auto['alias'])}", finestra] = azione
        # nessuna apertura fuori dai rami (passi di primo livello fuori dai choose)
        assert len(list(_aperture(auto.get("actions")))) == nei_rami, auto["alias"]
    for nome, script in (_carica("vmc_master.yaml", installato).get("script") or {}).items():
        for azione, finestra in _aperture(script.get("sequence")):
            altre[f"script.{nome}", finestra] = azione
    assert proprie_trovate == proprie
    assert set(altre) == set(APERTURE_AMMESSE), altre


# ------------------------------------------------------------------------------------------------ cicli
SCRITTURE = {"input_boolean": {"turn_on": "on", "turn_off": "off", "toggle": None},
             "homeassistant": {"turn_on": "on", "turn_off": "off", "toggle": None}}
AIUTANTI = ("input_select", "input_text", "input_number", "input_datetime", "counter", "timer")
CHIAVI_DELLE_CONDIZIONI = {"conditions", "condition", "if", "while", "until", "wait_template", "value_template"}
_ELENCHI = {"Temperatura Esterna": "temp_external_entity", "Temperatura Interna": "temp_internal_entity",
            "Umidità Esterna": "humidity_external_entity", "Umidità Interna": "humidity_internal_entity",
            "CO2 Interna": "co2_internal_entity", "Dispositivo Interna": "notification_device",
            "Media Player Interna": "media_player_entity"}
CICLI_AMMESSI = {
    **{(PRINCIPALE, f"VMC Master Save Selected {n} Entity", f"input_select.vmc_master_selected_{e}"):
       "trigger «cambia stato o qualsiasi attributo» dell'elenco delle entità selezionabili: lo script dell'elenco "
       "riscrive lo stesso input_select (set_options, select_option) con un elenco calcolato dalle entità di Home "
       "Assistant e dal valore memorizzato, non dal trigger: alla seconda scrittura elenco e scelta sono gli stessi, lo "
       "stato non cambia e il trigger non scatta più" for n, e in _ELENCHI.items()},
    ("VMC Master - Aggiorna Aria Scambiata e Gestisci Countdown", "", "input_text.vmc_master_tempo_mancante_reset"):
        "scrive «reset» solo quando la velocità è cambiata e nella stessa esecuzione memorizza la velocità: "
        "l'esecuzione partita dal suo «reset» trova la velocità uguale, non lo riscrive e lo svuota",
}
# misurati sulla b42: (nodi = trigger di stato per entità, archi), file completo e installato; sulla b41 i cicli erano
# 42 nel file completo (i 34 rami delle finestre che scrivono la propria finestra, 17 «On» e 17 «Off», più gli 8
# ammessi) e 40 installato (32 + 8)
FISSATI_GRAFO = {False: (99, 239), True: (79, 203)}


def _effetti(nodo: Any, script: dict[str, Any], visti: set[str], out: list[tuple[str, str | None]]) -> None:
    """(entità, stato nuovo o None se qualsiasi) per ogni scrittura di un aiutante, anche dentro gli script chiamati
    (script.nome o script.turn_on); le condizioni non scrivono."""
    if isinstance(nodo, dict):
        azione = nodo.get("action")
        if isinstance(azione, str) and "." in azione and "{" not in azione:
            dominio, servizio = azione.strip().split(".", 1)
            if servizio in SCRITTURE.get(dominio, {}):
                out += [(e, SCRITTURE[dominio][servizio]) for e in _bersagli(nodo)]
            elif dominio in AIUTANTI:
                out += [(e, None) for e in _bersagli(nodo)]
            elif dominio == "script":
                for s in (_bersagli(nodo) if servizio in ("turn_on", "toggle") else [f"script.{servizio}"]):
                    nome = s.split(".", 1)[1]
                    if nome in script and nome not in visti:
                        visti.add(nome)
                        _effetti(script[nome].get("sequence"), script, visti, out)
        for chiave, v in nodo.items():
            if chiave not in CHIAVI_DELLE_CONDIZIONI:
                _effetti(v, script, visti, out)
    elif isinstance(nodo, list):
        for v in nodo:
            _effetti(v, script, visti, out)


def _scatta(trigger: dict[str, Any], stato: str | None) -> bool:
    if stato is None:
        return True
    verso, non_verso = trigger.get("to"), trigger.get("not_to") or []
    verso = [verso] if isinstance(verso, str) else verso
    non_verso = [non_verso] if isinstance(non_verso, str) else non_verso
    return (verso is None or stato in verso) and stato not in non_verso


def _grafo(installato: bool) -> dict[tuple[str, str, str], set[tuple[str, str, str]]]:
    """Nodi: (automazione, id del trigger, entità) per ogni trigger di stato del package; arco da un nodo a ogni
    trigger di stato (anche di un'altra automazione) su cui può scattare una scrittura dei rami del suo trigger. Una
    scrittura che porta un'entità nello stato già garantito da una condizione di stato dell'opzione non cambia niente
    e non fa arco."""
    script = _carica("vmc_master.yaml", installato).get("script") or {}
    autos = _automazioni(installato)
    nodi = [(a, t, e) for a in autos for _, t, ent in _trigger_di_stato(a) for e in ent]

    def nome(a: dict[str, Any], t: dict[str, Any], e: str) -> tuple[str, str, str]:
        return a["alias"], str(t.get("id", "")).strip(), e

    archi: dict[tuple[str, str, str], set[tuple[str, str, str]]] = {}
    for a, t, e in nodi:
        dest = archi.setdefault(nome(a, t, e), set())
        for cond, seq in _rami_del_trigger(a, t):
            garantiti = _guardie_di_stato(cond)
            scritture: list[tuple[str, str | None]] = []
            _effetti(seq, script, set(), scritture)
            for e2, stato in scritture:
                if stato is not None and (e2, stato) in garantiti:
                    continue
                dest |= {nome(a2, t2, e3) for a2, t2, e3 in nodi if e3 == e2 and _scatta(t2, stato)}
    return archi


def _cicli(archi: dict[Any, set[Any]]) -> list[list[Any]]:
    """Componenti fortemente connesse con un ciclo (Tarjan, senza ricorsione)."""
    indice: dict[Any, int] = {}
    basso: dict[Any, int] = {}
    pila: list[Any] = []
    in_pila: set[Any] = set()
    out: list[list[Any]] = []
    for radice in archi:
        if radice in indice:
            continue
        lavoro = [(radice, iter(sorted(archi[radice])))]
        indice[radice] = basso[radice] = len(indice)
        pila.append(radice)
        in_pila.add(radice)
        while lavoro:
            v, figli = lavoro[-1]
            for w in figli:
                if w not in indice:
                    indice[w] = basso[w] = len(indice)
                    pila.append(w)
                    in_pila.add(w)
                    lavoro.append((w, iter(sorted(archi.get(w, ())))))
                    break
                if w in in_pila:
                    basso[v] = min(basso[v], indice[w])
            else:
                lavoro.pop()
                if lavoro:
                    basso[lavoro[-1][0]] = min(basso[lavoro[-1][0]], basso[v])
                if basso[v] == indice[v]:
                    comp = []
                    while True:
                        w = pila.pop()
                        in_pila.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    if len(comp) > 1 or v in archi.get(v, ()):
                        out.append(sorted(comp))
    return out


@pytest.mark.parametrize("installato", [True, False], ids=["installato", "file_completo"])
def test_nessun_ciclo_tra_trigger_di_stato_e_scritture(installato: bool) -> None:
    """Controllo generale della classe: nel grafo di tutti i trigger di stato del package (tutte le automazioni,
    anche tra un'automazione e l'altra, con gli script chiamati) e delle scritture degli aiutanti dei loro rami non ci
    sono cicli, tranne gli 8 ammessi (CICLI_AMMESSI: scritture che alla seconda volta non cambiano lo stato). Con la
    guardia della b42 il ramo «On» non riapre la propria finestra (è già aperta) e il ramo «Off» non la richiude (è già
    chiusa): restano solo chiusure di altre finestre, che non riattivano nessun ramo «On». Sulla b41 i 34 rami delle
    finestre che scrivono la propria finestra erano cicli. Nodi e archi sono contati (FISSATI_GRAFO): un trigger di
    stato o una scrittura nuova va guardata e il numero aggiornato."""
    archi = _grafo(installato)
    assert (len(archi), sum(len(v) for v in archi.values())) == FISSATI_GRAFO[installato]
    cicli = _cicli(archi)
    assert all(len(c) == 1 for c in cicli), cicli
    assert {nodo for (nodo,) in cicli} == set(CICLI_AMMESSI)


# ------------------------------------------------------------------------------------------------ esclusività
def _chiude(installato: bool = False) -> dict[str, set[str]]:
    """Finestre chiuse da ogni finestra quando si apre (rami dei trigger «to: on» di tutte le automazioni)."""
    chiude: dict[str, set[str]] = {}
    for auto in _automazioni(installato):
        for _, t, ent in _trigger_di_stato(auto):
            if t.get("to") != "on":
                continue
            for cond, seq in _rami_del_trigger(auto, t):
                scritture: list[tuple[str, str | None]] = []
                _effetti(seq, {}, set(), scritture)
                for f in ent:
                    if FINESTRA.match(f):
                        chiude.setdefault(f, set()).update(e for e, s in scritture if s == "off" and e != f)
    return chiude


@lru_cache
def _coppie_esclusive(installato: bool = False) -> frozenset[tuple[str, str]]:
    """Coppie di finestre che si chiudono a vicenda: alla fine al massimo una delle due resta aperta."""
    chiude = _chiude(installato)
    return frozenset((a, b) for a in chiude for b in chiude[a] if a < b and a in chiude.get(b, set()))


def test_finestre_che_si_chiudono_a_vicenda() -> None:
    """Le 6 finestre principali (Telecomando, Sensori, Opzioni, Avvisi, Informazioni, Programmazione Giornaliera) si
    chiudono a vicenda; le coppie esclusive di tutto il package sono 65 (file completo, con Clona): sono la regola
    controllata alla fine di ogni raffica delle prove dinamiche."""
    coppie = _coppie_esclusive()
    for a in FINESTRE_PRINCIPALI:
        for b in FINESTRE_PRINCIPALI:
            assert a == b or (min(a, b), max(a, b)) in coppie, (a, b)
    assert len(coppie) == 65


# ------------------------------------------------------------------------------------------------ convalida
def _modelli(nodo: Any, percorso: str = "") -> Iterator[tuple[str, str]]:
    """(percorso, testo) di ogni stringa con un modello Jinja."""
    if isinstance(nodo, dict):
        for chiave, valore in nodo.items():
            yield from _modelli(valore, f"{percorso}/{chiave}")
    elif isinstance(nodo, list):
        for i, valore in enumerate(nodo):
            yield from _modelli(valore, f"{percorso}[{i}]")
    elif isinstance(nodo, str) and any(segno in nodo for segno in ("{{", "{%", "{#")):
        yield percorso, nodo


# (automazioni, script, modelli degli altri domini) del package scritto dall'installatore; misurati sulla b42
FISSATI_CONVALIDA = (14, 51, 166)


@pytest.mark.parametrize("vmc", ["master", "soggiorno"])
async def test_convalida_di_home_assistant_del_package_installato(hass: HomeAssistant, vmc: str) -> None:
    """Il package come lo scrive l'installatore (installatore.genera_file, per la VMC Master e per un'altra VMC: senza
    le sezioni CLONA e INSTALLA, con nome e IP della VMC): tutte le automazioni (14: le 13 di vmc_<nome>.yaml e
    l'Automazione VMC) e tutti gli script (51) passano la convalida di Home Assistant (la stessa del caricamento:
    async_validate_config_item, con i modelli, i trigger, le condizioni e le azioni) e ogni stringa con un modello
    Jinja degli altri domini (166) compila con l'ambiente dei modelli di Home Assistant. Nella b032d06 rimuovi_clona
    toglieva la riga «'input_boolean.vmc_master_opzione_finestra_clona']) | selectattr(...)» di 12 modelli expand
    della principale e Home Assistant scartava tutta l'Automazione VMC («expected 'all' or 'none' at
    'actions[2].choose[0].sequence[1].target.entity_id'»)."""
    file = genera_file(vmc, "192.168.1.50", "9.0.0b42")
    pacchetto = hay.parse_yaml(file[f"vmc_{vmc}.yaml"])
    automazioni = [*pacchetto["automation"], *hay.parse_yaml(file[f"vmc_{vmc}_automazione.yaml"])["automation"]]
    errori: list[str] = []
    for auto in automazioni:
        try:
            await valida_automazione(hass, auto.get("id", ""), auto)
        except (probatio.Invalid, HomeAssistantError) as err:
            errori.append(f"automazione {auto.get('alias')}: {err}")
    script = pacchetto.get("script") or {}
    for nome, configurazione in script.items():
        try:
            await valida_script(hass, nome, configurazione)
        except (probatio.Invalid, HomeAssistantError) as err:
            errori.append(f"script {nome}: {err}")
    # i modelli di automazioni e script li compila già la convalida; qui quelli degli altri domini
    modelli = list(_modelli({k: v for k, v in pacchetto.items() if k not in ("automation", "script")}))
    for percorso, testo in modelli:
        try:
            Template(testo, hass).ensure_valid()
        except TemplateError as err:
            errori.append(f"modello vmc_{vmc}.yaml{percorso}: {err}")
    assert not errori, "\n".join(errori)
    assert (len(automazioni), len(script), len(modelli)) == FISSATI_CONVALIDA


# righe che rimuovi_clona cancella intere (fuori dalle sezioni CLONA): sicure solo se sono una voce intera
VOCE_YAML = re.compile(r"^ *- [a-z_]+\.vmc_master_[a-z0-9_]+ *(#.*)?$")
VOCE_JINJA = re.compile(r"^ *'[a-z_]+\.vmc_master_[a-z0-9_]+', *$")
ISTRUZIONE_JINJA = re.compile(r"^ *\{%- set [^{}]* -%\} *(\{#- [^{}]* -#\})? *$")  # istruzione completa, sola sulla riga
# (righe con la finestra Clona, righe con altre entità vmc_master_clona_) per file, misurate sulla b42
FISSATI_RIGHE_CLONA = {"vmc_master.yaml": (7, 30), "vmc_master_automazione.txt": (14, 0)}


def test_righe_cancellate_da_rimuovi_clona_sono_voci_intere() -> None:
    """Classe della rottura della b032d06: rimuovi_clona (vmc_script_clona.sh) cancella la riga intera che contiene
    «vmc_master_opzione_finestra_clona» (dopo aver tolto la voce «'...clona', » in mezzo a una riga) o
    «vmc_master_clona_». Fuori dalle sezioni CLONA, nei due file che l'installatore trasforma, ognuna di queste righe
    deve essere una voce intera: per la finestra Clona solo la voce YAML «- input_boolean...» o la voce Jinja
    «'input_boolean...',» (la lista resta valida, Jinja accetta la virgola finale); per le altre entità Clona anche
    un'istruzione «{%- set ... -%}» completa (le righe «RIGA SOLO MASTER»)."""
    trovate: dict[str, tuple[int, int]] = {}
    sbagliate = []
    for nome in FISSATI_RIGHE_CLONA:
        finestra = altre = 0
        in_clona = False
        for numero, riga in enumerate((PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"), 1):
            if in_clona:
                in_clona = trasforma._FINE_CLONA not in riga
                continue
            if trasforma._INIZIO_CLONA in riga:
                in_clona = True
                continue
            corpo = riga.split(" #", 1)[0] if VOCE_YAML.match(riga) else riga
            if "vmc_master_opzione_finestra_clona" in corpo.replace(trasforma._VOCE_FINESTRA_CLONA, ""):
                finestra += 1
                if not (VOCE_YAML.match(riga) or VOCE_JINJA.match(riga)):
                    sbagliate.append(f"{nome}:{numero}: {riga.strip()}")
            elif "vmc_master_clona_" in riga:
                altre += 1
                if not (VOCE_YAML.match(riga) or VOCE_JINJA.match(riga) or ISTRUZIONE_JINJA.match(riga)):
                    sbagliate.append(f"{nome}:{numero}: {riga.strip()}")
        trovate[nome] = (finestra, altre)
    assert not sbagliate, "\n".join(sbagliate)
    assert trovate == FISSATI_RIGHE_CLONA


# ------------------------------------------------------------------------------------------------ banco dinamico
AUTO_PRINCIPALE = "automation.automazione_vmc_master"
SPIA_RITORNO = "input_boolean.vmc_master_spia_calendario_black_out"
TETTO_CAMBI = 100  # cambi di stato delle finestre in una raffica; la b42 ne fa al massimo 11 (raffiche casuali)


class CicloSenzaFine(Exception):
    """Più di TETTO_CAMBI cambi delle finestre nello stesso istante: automazioni spente."""


@dataclass
class Banco:
    """Home Assistant vero con l'Automazione VMC Master e l'Esclusività del package, gli input_boolean veri."""

    hass: HomeAssistant
    freezer: Any
    finestre: list[str] = field(default_factory=list)
    cambi: list[tuple[str, str]] = field(default_factory=list)

    @callback
    def _annota(self, event: Event) -> None:
        if FINESTRA.match(event.data["entity_id"]) and event.data["new_state"] is not None:
            self.cambi.append((event.data["entity_id"].removeprefix(IB), event.data["new_state"].state))

    async def prepara(self) -> None:
        hass = self.hass
        self.freezer.move_to("2026-11-26 10:00:00+01:00")  # lontano dal trigger a orario delle 08:00
        pkg = _carica("vmc_master.yaml", False)
        self.finestre = sorted(f"input_boolean.{k}" for k in pkg["input_boolean"] if FINESTRA.match(f"input_boolean.{k}"))
        assert len(self.finestre) == 21
        assert await async_setup_component(hass, "input_boolean", {"input_boolean": pkg["input_boolean"]})
        assert await async_setup_component(hass, "homeassistant", {})  # homeassistant.update_entity della rilettura
        async_mock_service(hass, "script", "turn_on")  # elenchi delle entità del ramo « Opzioni On»
        # VMC ON-Line con la velocità letta diversa dall'ultima lettura valida: la rilettura della b38 aspetta 2 s
        hass.states.async_set("sensor.vmc_master_status_ip_interfaccia", "ON-Line")
        hass.states.async_set("sensor.vmc_master_status_ventola", "VMGO,00003,00000")
        hass.states.async_set("sensor.vmc_master_status_ventola_memorizzata", "VMGO,00002,00000")
        assert await async_setup_component(hass, "automation", {"automation": [
            _automazione(PRINCIPALE), _automazione(ESCLUSIVITA)]})
        await hass.async_block_till_done()
        hass.bus.async_listen(EVENT_STATE_CHANGED, self._annota)

    async def lavora(self) -> None:
        """Il ciclo di Home Assistant lavora finché ha qualcosa di pronto nell'istante corrente (i timer futuri
        restano fermi); oltre TETTO_CAMBI cambi delle finestre spegne subito le automazioni (le esecuzioni in corso e
        in coda si fermano) e solleva CicloSenzaFine."""
        loop = self.hass.loop
        while True:
            await asyncio.sleep(0)
            if len(self.cambi) > TETTO_CAMBI:
                await self.hass.services.async_call("automation", "turn_off", {"entity_id": "all"}, blocking=True)
                raise CicloSenzaFine
            fine = loop.time() + loop._clock_resolution  # type: ignore[attr-defined]
            if not loop._ready and not any(  # type: ignore[attr-defined]
                    not h.cancelled() and h.when() < fine for h in loop._scheduled):  # type: ignore[attr-defined]
                return

    async def tempo(self, secondi: float) -> None:
        self.freezer.tick(timedelta(seconds=secondi))
        async_fire_time_changed(self.hass)
        await self.lavora()

    def correnti(self) -> int:
        return int(self.hass.states.get(AUTO_PRINCIPALE).attributes.get("current", 0))

    async def occupa(self) -> None:
        """Un'esecuzione lunga vera: Spia Black-Out del Calendario accesa con la VMC ON-Line, dopo 32 s scatta
        «calendario_ritorno_da_black_out» (trigger template con «for»): la rilettura della velocità (b38) aspetta la
        lettura nuova fino a 2 s e l'automazione resta occupata."""
        await self.hass.services.async_call("input_boolean", "turn_on", {"entity_id": SPIA_RITORNO}, blocking=True)
        await self.lavora()
        await self.tempo(32)
        assert self.correnti() == 1

    async def libera(self) -> None:
        """Scadono i 2 s: l'esecuzione lunga finisce (spegne la Spia e si ferma: interruttore del Calendario spento) e
        partono gli eventi in coda."""
        await self.tempo(2)
        assert self.hass.states.get(SPIA_RITORNO).state == "off"

    async def azzera(self) -> None:
        """Automazioni spente (esecuzioni e coda ferme), tutte le finestre chiuse, automazioni riaccese."""
        hass = self.hass
        await hass.services.async_call("automation", "turn_off", {"entity_id": "all"}, blocking=True)
        await hass.services.async_call("input_boolean", "turn_off", {"entity_id": [*self.finestre, SPIA_RITORNO]},
                                       blocking=True)
        await hass.async_block_till_done()
        await hass.services.async_call("automation", "turn_on", {"entity_id": "all"}, blocking=True)
        await hass.async_block_till_done()
        self.cambi.clear()

    async def raffica(self, tocchi: list[tuple[str, str]], occupata: bool = False) -> int:
        """I tocchi della scheda nello stesso istante, senza aspettare l'uno l'altro (come la «raffica» del banco della
        versione nativa); con occupata=True mentre è in corso l'esecuzione lunga. Restituisce le esecuzioni
        dell'Automazione VMC Master in corso o in coda subito dopo i tocchi."""
        if occupata:
            await self.occupa()
        self.cambi.clear()
        compiti = [asyncio.ensure_future(self.hass.services.async_call(
            "input_boolean", f"turn_{verso}", {"entity_id": IB + finestra}, blocking=True))
            for finestra, verso in tocchi]
        await self.lavora()
        in_corso = self.correnti()  # con occupata=True l'esecuzione lunga e gli eventi in coda dietro di lei
        if occupata:
            await self.libera()
        assert all(c.done() for c in compiti)
        assert self.correnti() == 0
        return in_corso

    def aperte(self) -> set[str]:
        return {e.removeprefix(IB) for e in self.finestre if self.hass.states.get(e).state == "on"}


@pytest.fixture
async def banco(hass: HomeAssistant, freezer) -> AsyncIterator[Banco]:
    b = Banco(hass, freezer)
    await b.prepara()
    yield b
    # automazioni spente: nessun timer dei trigger resta dopo la prova
    await hass.services.async_call("automation", "turn_off", {"entity_id": "all"}, blocking=True)
    await hass.async_block_till_done()


def _ciclo(banco: Banco) -> str:
    return (f"CICLO SENZA FINE: più di {TETTO_CAMBI} cambi di stato delle finestre nello stesso istante (automazioni "
            f"spente); primi cambi: {banco.cambi[:8]}")


def _regole(aperte: set[str], prima: Collection[str], tocchi: Sequence[tuple[str, str]]) -> list[str]:
    """Regole b42 dello stato finale che valgono per ogni raffica."""
    errori = []
    principali = sorted(aperte & {f.removeprefix(IB) for f in FINESTRE_PRINCIPALI})
    if len(principali) > 1:
        errori.append(f"più finestre principali aperte: {principali}")
    for a, b in sorted(_coppie_esclusive()):
        if {a.removeprefix(IB), b.removeprefix(IB)} <= aperte:
            errori.append(f"aperte insieme due finestre che si chiudono a vicenda: {a}, {b}")
    ultimo = dict(tocchi)  # l'ultimo tocco di ogni finestra
    if chiuse := sorted(f for f, v in ultimo.items() if v == "off" and f in aperte):
        errori.append(f"aperte nonostante l'ultimo tocco le chiudesse: {chiuse}")
    if da_sole := sorted(aperte - set(prima) - {f for f, v in tocchi if v == "on"}):
        errori.append(f"aperte da sole: {da_sole}")
    if len(ultimo) == 1:
        ((finestra, verso),) = ultimo.items()
        if (finestra in aperte) != (verso == "on"):
            errori.append(f"una sola finestra toccata e l'ultimo tocco non vince: {finestra} {verso}")
    return errori


# ------------------------------------------------------------------------------------------------ scenari
# (nome, finestre aperte prima, tocchi nello stesso istante, finestre aperte alla fine con l'automazione occupata,
# finestre aperte alla fine con l'automazione libera: con «resta la prima» e con la variante «vince l'ultimo tocco»).
# Con l'automazione occupata tutti gli eventi vanno in coda con lo stesso last_changed: resta la prima elaborata con
# tutte e due. Con l'automazione libera il primo evento parte subito: senza la variante la chiusura di più finestre
# insieme aspetta un giro del ciclo e chiude anche quelle toccate nel frattempo (resta la prima); con la variante il
# modello del turn_off è reso prima che arrivino gli altri tocchi, che non sono ancora accesi (resta l'ultima toccata,
# come con i tocchi lenti).
SCENARI = [
    ("a: Avvisi, Audio e Telecomando aperte insieme (banco della versione nativa)", [],
     [("opzioni_avvisi", "on"), ("opzione_finestra_audio", "on"), ("opzioni_vmc", "on")],
     # Avvisi è la prima: chiude Telecomando (la sua lista non contiene Audio, Clona e Conferma Pulizia)
     {"opzioni_avvisi", "opzione_finestra_audio"},
     ({"opzioni_avvisi", "opzione_finestra_audio"}, {"opzioni_vmc"})),  # Telecomando chiude anche Audio
    ("b: una sola finestra aperta e chiusa", [], [("opzioni_avvisi", "on"), ("opzioni_avvisi", "off")],
     set(), (set(), set())),
    ("c: una sola finestra aperta, chiusa e riaperta", [],
     [("opzioni_avvisi", "on"), ("opzioni_avvisi", "off"), ("opzioni_avvisi", "on")],
     {"opzioni_avvisi"}, ({"opzioni_avvisi"}, {"opzioni_avvisi"})),
    ("d: due finestre principali aperte insieme", [], [("opzioni_avvisi", "on"), ("opzioni_vmc", "on")],
     {"opzioni_avvisi"}, ({"opzioni_avvisi"}, {"opzioni_vmc"})),
    ("e: pannello Opzioni e la sua sotto-finestra Audio aperti insieme", [],
     [("opzioni_offset_sensori", "on"), ("opzione_finestra_audio", "on")],
     {"opzioni_offset_sensori"},  # « Opzioni On» chiude tutte le sue sotto-finestre, anche Audio aperta insieme
     ({"opzioni_offset_sensori"}, {"opzioni_offset_sensori", "opzione_finestra_audio"})),
    ("f: una sola finestra aperta prima, poi chiusa e riaperta", ["opzioni_avvisi"],
     [("opzioni_avvisi", "off"), ("opzioni_avvisi", "on")],
     {"opzioni_avvisi"}, ({"opzioni_avvisi"}, {"opzioni_avvisi"})),  # tutte le 17 finestre: test_riaperta_...
]


async def _apri_prima(banco: Banco, prima: Collection[str]) -> None:
    """Finestre aperte un secondo prima della raffica (last_changed più vecchio dei tocchi)."""
    if prima:
        await banco.hass.services.async_call("input_boolean", "turn_on", {"entity_id": [IB + f for f in prima]},
                                             blocking=True)
        await banco.lavora()
        await banco.tempo(1)
        assert banco.aperte() == set(prima)


@pytest.mark.parametrize("occupata", [False, True], ids=["automazione_libera", "automazione_occupata"])
async def test_raffiche_di_tocchi_finiscono_con_la_regola_b42(banco: Banco, occupata: bool) -> None:
    """Scenari a-f, tocchi nello stesso istante. Con l'automazione libera il primo evento parte subito; con
    l'automazione occupata (esecuzione lunga vera in corso) tutti gli eventi dei tocchi vanno in coda e si eseguono dopo,
    quando le finestre sono già cambiate: è il caso del difetto («prima che l'automazione la elabori»). Ogni scenario
    deve finire (niente «ciclo senza fine») con le finestre aperte attese e le regole comuni (_regole); con
    l'automazione libera vale una delle due attese («resta la prima» o la variante «vince l'ultimo tocco», che è fissata
    in TestVarianteVinceLUltimoTocco). Sulla b41 entrano nel ciclo: libera a, c, d, e; occupata a, b, c, d, e (b con
    l'automazione libera finisce anche sulla b41: l'evento di apertura si esegue subito, a finestra aperta). f: la
    finestra riaperta nello stesso istante in cui il ramo «Off» la sta chiudendo resta aperta (vince l'ultimo tocco)."""
    errori = []
    for nome, prima, tocchi, attese_occupata, attese_libera in SCENARI:
        await banco.azzera()
        await _apri_prima(banco, prima)
        try:
            in_corso = await banco.raffica(tocchi, occupata)
        except CicloSenzaFine:
            errori.append(f"{nome}: {_ciclo(banco)}")
            continue
        if occupata:  # l'esecuzione lunga e dietro di lei in coda un evento per ogni tocco
            assert in_corso == 1 + len(tocchi), (nome, in_corso)
        aperte = banco.aperte()
        ammesse = [attese_occupata] if occupata else list(attese_libera)
        if aperte not in ammesse:
            errori.append(f"{nome}: aperte {sorted(aperte)}, attese {' o '.join(str(sorted(a)) for a in ammesse)} "
                          f"(cambi {banco.cambi})")
        errori += [f"{nome}: {e}" for e in _regole(aperte, prima, tocchi)]
    if errori:
        pytest.fail("\n".join(errori))


def _finestre_con_off() -> list[str]:
    """Finestre con un trigger «... Off» (on -> off) nell'Automazione VMC Master (file completo, come nel banco)."""
    return sorted(e.removeprefix(IB) for _, t, ent in _trigger_di_stato(_automazione(PRINCIPALE))
                  if t.get("to") == "off" for e in ent if FINESTRA.match(e))


@pytest.mark.parametrize("occupata", [False, True], ids=["automazione_libera", "automazione_occupata"])
async def test_riaperta_mentre_il_ramo_off_la_chiude(banco: Banco, occupata: bool) -> None:
    """Scenario f per tutte le 17 finestre con il ramo «Off»: la finestra aperta prima (un secondo prima), poi nello
    stesso istante chiusa e riaperta (2 tocchi) e chiusa, riaperta, chiusa e riaperta (4 tocchi): alla fine resta
    aperta (vince l'ultimo tocco) e valgono le regole comuni. Con l'automazione libera l'evento «Off» parte subito e
    passa la guardia; se il suo turn_off ha più entità, Home Assistant le scrive un giro del ciclo dopo (un task per
    entità), quando la riapertura è già arrivata: se tra le entità c'è la finestra stessa la richiude. Sulla 2afccd5
    sbagliano Monitoraggio, Opzioni e Avvisi (6 prove, solo con l'automazione libera); dalla 80c9e80 i loro rami «Off»
    chiudono solo le sotto-finestre. Sulla b41 la prima prova entra nel ciclo senza fine e la prova si ferma lì."""
    finestre = _finestre_con_off()
    assert len(finestre) == 17
    errori = []
    for finestra in finestre:
        for tocchi in ([(finestra, "off"), (finestra, "on")], [(finestra, "off"), (finestra, "on")] * 2):
            nome = f"{finestra}, {len(tocchi)} tocchi"
            await banco.azzera()
            await _apri_prima(banco, [finestra])
            try:
                await banco.raffica(tocchi, occupata)
            except CicloSenzaFine:  # codice senza la guardia (b41): basta il primo, le altre non si provano
                pytest.fail("\n".join([*errori, f"{nome}: {_ciclo(banco)}"]))
            aperte = banco.aperte()
            errori += [f"{nome}: {e} (cambi {banco.cambi})" for e in _regole(aperte, [finestra], tocchi)]
    if errori:
        pytest.fail("\n".join(errori))


# ------------------------------------------------------------------------------------------------ raffiche casuali
SEME = 42
RAFFICHE = 300
OGNI_OCCUPATA = 5  # una raffica ogni 5 arriva con l'automazione occupata
# massimo dei cambi delle finestre in una raffica, misurato con Home Assistant 2026.11.2, uguale con «resta la prima»
# (68e159c con la 80c9e80) e con la variante «vince l'ultimo tocco» (sulla 68e159c senza la 80c9e80 era 10)
MASSIMO_CAMBI = 11
# proprietà della sequenza generata (dipendono solo dal seme): la prova copre i casi del difetto
FISSATI_SEQUENZA = {"tocchi": 1076, "occupate": 60, "stessa_finestra_aperta_e_chiusa": 43,
                    "due_principali_aperte": 39}


def _sequenza() -> list[list[tuple[str, str]]]:
    rng = random.Random(SEME)
    finestre = sorted(k.removeprefix("input_boolean.") for k in _carica("vmc_master.yaml", False)["input_boolean"]
                      if FINESTRA.match(f"input_boolean.{k}"))
    nomi = [f.removeprefix("vmc_master_") for f in finestre]
    return [[(rng.choice(nomi), "on" if rng.random() < 0.6 else "off") for _ in range(rng.randint(1, 6))]
            for _ in range(RAFFICHE)]


def test_sequenza_casuale_copre_i_casi_del_difetto() -> None:
    """La sequenza casuale (seme fisso) contiene raffiche con la stessa finestra aperta e chiusa nello stesso istante e
    con due finestre principali aperte insieme, e una raffica ogni OGNI_OCCUPATA con l'automazione occupata."""
    sequenza = _sequenza()
    principali = {f.removeprefix(IB) for f in FINESTRE_PRINCIPALI}
    conteggi = {
        "tocchi": sum(len(r) for r in sequenza),
        "occupate": sum(1 for k in range(len(sequenza)) if k % OGNI_OCCUPATA == OGNI_OCCUPATA - 1),
        "stessa_finestra_aperta_e_chiusa": sum(1 for r in sequenza if any(
            (f, "on") in r and (f, "off") in r for f, _ in r)),
        "due_principali_aperte": sum(1 for r in sequenza if len({f for f, v in r if v == "on" and f in principali}) > 1),
    }
    assert conteggi == FISSATI_SEQUENZA


async def test_raffiche_casuali_finiscono_con_la_regola_b42(banco: Banco) -> None:
    """(f) RAFFICHE raffiche casuali (seme SEME) da 1 a 6 tocchi su tutte le 21 finestre (aperture 60 %, chiusure 40 %),
    senza azzerare tra una raffica e l'altra; una ogni OGNI_OCCUPATA con l'automazione occupata. Ogni raffica deve
    finire entro TETTO_CAMBI cambi delle finestre e rispettare le regole comuni: al massimo una finestra principale
    aperta, nessuna coppia di finestre che si chiudono a vicenda aperta, una finestra chiusa dal suo ultimo tocco resta
    chiusa, nessuna finestra si apre da sola, una raffica su una sola finestra finisce come l'ultimo tocco."""
    await banco.azzera()
    massimo = 0
    for k, tocchi in enumerate(_sequenza()):
        prima = banco.aperte()
        ciclo = False
        try:
            await banco.raffica(tocchi, occupata=k % OGNI_OCCUPATA == OGNI_OCCUPATA - 1)
        except CicloSenzaFine:
            ciclo = True
        if ciclo:
            pytest.fail(f"raffica {k} {tocchi} (aperte prima {sorted(prima)}): {_ciclo(banco)}")
        massimo = max(massimo, len(banco.cambi))
        if errori := _regole(banco.aperte(), prima, tocchi):
            pytest.fail(f"raffica {k} {tocchi} (aperte prima {sorted(prima)}): {errori}; cambi {banco.cambi}")
    assert massimo == MASSIMO_CAMBI, massimo


# ------------------------------------------------------------------------------------------------ esclusività
# (tocchi nello stesso istante con l'automazione libera, finestre aperte alla fine con la guardia al turno
# dell'evento: con «resta la prima» e con la variante «vince l'ultimo tocco»)
ESCLUSIVITA_SCENARI = {
    "Tempi di Attesa aperta, Audio aperta e chiusa": (
        [("opzione_finestra_tempi_attesa", "on"), ("opzione_finestra_audio", "on"), ("opzione_finestra_audio", "off")],
        ({"opzione_finestra_tempi_attesa"}, set())),
    "Tempi di Attesa e Audio aperte insieme": (
        [("opzione_finestra_tempi_attesa", "on"), ("opzione_finestra_audio", "on")],
        ({"opzione_finestra_tempi_attesa"}, {"opzione_finestra_audio"})),
    "Timer Lettura Dati VMC aperta, Offset aperta e chiusa": (
        [("opzione_finestra_prossime_letture", "on"), ("opzioni_interruttore_offset_sensori", "on"),
         ("opzioni_interruttore_offset_sensori", "off")],
        ({"opzione_finestra_prossime_letture"}, set())),
}


async def test_esclusivita_evento_vecchio(banco: Banco) -> None:
    """«VMC Master - Esclusività Finestre Opzioni» (queued, chiude soltanto), tocchi nello stesso istante: ogni
    scenario finisce con una delle due attese. Con «resta la prima» l'evento vecchio di Audio (o di Offset), già
    richiusa al suo turno, non chiude la finestra Tempi di Attesa (o Timer Lettura Dati VMC) aperta nello stesso
    istante; con la variante resta l'ultima toccata, come con i tocchi lenti. Sulla 657227e (condizione
    dell'automazione, valutata quando il trigger scatta) e sulla b41 (nessuna condizione) Tempi di Attesa e Audio
    aperte insieme si chiudevano tutte e due."""
    errori = []
    for nome, (tocchi, ammesse) in ESCLUSIVITA_SCENARI.items():
        await banco.azzera()
        try:
            await banco.raffica(tocchi)
        except CicloSenzaFine:
            errori.append(f"{nome}: {_ciclo(banco)}")
            continue
        if (aperte := banco.aperte()) not in ammesse:
            errori.append(f"{nome}: aperte {sorted(aperte)}, attese {' o '.join(str(sorted(a)) for a in ammesse)} "
                          f"(cambi {banco.cambi})")
        errori += [f"{nome}: {e}" for e in _regole(aperte, set(), tocchi)]
    if errori:
        pytest.fail("\n".join(errori))


# ------------------------------------------------------------------------------------------------ interruttore Umidità
UMIDITA = IB + "opzioni_accendi_spegni_vmc_vs_umidita"
ALLERTA_UMIDITA = IB + "umidita_verifica_soglia_valore_spia"


async def test_interruttore_umidita_spento_e_riacceso_prima_del_turno(banco: Banco) -> None:
    """Gemello (stessa classe, trigger di stato su un interruttore): allerta Umidità in corso con la VMC ON-Line e
    l'interruttore Umidità acceso; mentre l'automazione è occupata l'utente lo spegne e lo riaccende. Al suo turno
    l'evento «Disattivazione Umidità Limite» (on -> off) trova l'interruttore già riacceso e non fa niente: l'allerta
    resta accesa e nessun comando alla VMC. Sulla b41 l'evento vecchio spegneva l'allerta Umidità e mandava il comando
    Velocità 0 (shell_command.vmc_master_velocita_0) con l'interruttore acceso."""
    hass = banco.hass
    comandi = async_mock_service(hass, "shell_command", "vmc_master_velocita_0")
    await hass.services.async_call("automation", "turn_off", {"entity_id": "all"}, blocking=True)
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": [UMIDITA, ALLERTA_UMIDITA]},
                                   blocking=True)
    await hass.services.async_call("automation", "turn_on", {"entity_id": "all"}, blocking=True)
    await banco.lavora()
    assert banco.correnti() == 0
    await banco.occupa()
    for verso in ("off", "on"):
        await hass.services.async_call("input_boolean", f"turn_{verso}", {"entity_id": UMIDITA}, blocking=True)
        await banco.lavora()
    in_corso = banco.correnti()
    await banco.libera()
    stato = {e.removeprefix(IB): hass.states.get(e).state for e in (UMIDITA, ALLERTA_UMIDITA)}
    assert in_corso == 2  # l'esecuzione lunga e dietro di lei l'evento on -> off (off -> on non ha trigger di stato)
    assert (stato, [c.service for c in comandi]) == (
        {"opzioni_accendi_spegni_vmc_vs_umidita": "on", "umidita_verifica_soglia_valore_spia": "on"}, [])


# ------------------------------------------------------------------------------------------------ variante
class TestVarianteVinceLUltimoTocco:
    """Variante «vince l'ultimo tocco» (commit b032d06 e d254602, da confermare dal proprietario): aprendo una finestra
    si chiudono solo le finestre accese con last_changed non successivo a quello dell'evento (modello expand nel
    turn_off dei 18 rami «On» della principale e delle 4 opzioni dell'Esclusività). Fissa le attese della variante:
    finestre toccate in istanti diversi con l'automazione occupata e raffica con l'automazione libera (seconda attesa di
    SCENARI e ESCLUSIVITA_SCENARI). Sulla 68e159c con la 80c9e80 (senza la variante) falliscono tutte e 4 le prove, le
    altre 23 passano. Se il proprietario sceglie «resta la prima» questa classe si toglie insieme ai due commit."""

    FORMA = re.compile(
        r"^\{\{ expand\(\[ ?((?:'input_boolean\.[a-z0-9_]+', ?)*'input_boolean\.[a-z0-9_]+',?) ?\]\) "
        r"\| selectattr\('state', 'eq', 'on'\) \| selectattr\('last_changed', 'le', trigger\.to_state\.last_changed\) "
        r"\| map\(attribute='entity_id'\) \| list \}\}$")

    @staticmethod
    def _chiusure(nodo: Any) -> Iterator[dict[str, Any]]:
        """Passi input_boolean.turn_off che chiudono finestre (anche annidati)."""
        if isinstance(nodo, dict):
            if str(nodo.get("action", "")).strip() == "input_boolean.turn_off" and any(
                    FINESTRA.match(e) for e in _bersagli(nodo)):
                yield nodo
            for valore in nodo.values():
                yield from TestVarianteVinceLUltimoTocco._chiusure(valore)
        elif isinstance(nodo, list):
            for valore in nodo:
                yield from TestVarianteVinceLUltimoTocco._chiusure(valore)

    @pytest.mark.parametrize("installato", [True, False], ids=["installato", "file_completo"])
    def test_turn_off_solo_delle_finestre_aperte_prima(self, installato: bool) -> None:
        """Ogni turn_off di finestre dei 18 rami «On» della principale e delle 4 opzioni dell'Esclusività ha come
        entity_id il modello «expand([...]) | selectattr('state', 'eq', 'on') | selectattr('last_changed', 'le',
        trigger.to_state.last_changed) | map(attribute='entity_id') | list», con sole finestre e senza la finestra
        del ramo; uno per ramo (22 in tutto). Installato: la riga della Clona tolta lascia la lista valida."""
        trovati = {PRINCIPALE: 0, ESCLUSIVITA: 0}
        for alias in trovati:
            auto = _automazione(alias, installato)
            for _, t, ent in _trigger_di_stato(auto):
                finestre = [e for e in ent if FINESTRA.match(e)]
                if not finestre or (alias == PRINCIPALE and t.get("to") != "on"):
                    continue
                for _, seq in _rami_del_trigger(auto, t):
                    passi = list(self._chiusure(seq))
                    assert len(passi) == 1, (alias, t.get("id"), len(passi))
                    modello = re.sub(r"\s+", " ", str(passi[0]["target"]["entity_id"])).strip()
                    corrisponde = self.FORMA.match(modello)
                    assert corrisponde, (alias, t.get("id"), modello)
                    chiuse = re.findall(r"'([^']+)'", corrisponde.group(1))
                    assert all(FINESTRA.match(e) for e in chiuse) and len(set(chiuse)) == len(chiuse), chiuse
                    if alias == PRINCIPALE:
                        assert finestre[0] not in chiuse, t.get("id")
            # rami distinti: nell'Esclusività più trigger condividono un'opzione
            trovati[alias] = len({id(seq) for _, t, ent in _trigger_di_stato(auto) if any(FINESTRA.match(e) for e in ent)
                                  and (alias != PRINCIPALE or t.get("to") == "on") for _, seq in _rami_del_trigger(auto, t)})
        assert trovati == {PRINCIPALE: 17 if installato else 18, ESCLUSIVITA: 4}

    PASSO = 0.5  # secondi tra un tocco e l'altro, tutti mentre l'esecuzione lunga aspetta (al massimo 2 s)
    # (nome, tocchi uno dopo l'altro con l'automazione occupata, passo in secondi, finestre aperte alla fine)
    SCENARI_DI_FILA = [
        ("Avvisi poi Telecomando", [("opzioni_avvisi", "on"), ("opzioni_vmc", "on")], PASSO, {"opzioni_vmc"}),
        ("Opzioni poi Audio", [("opzioni_offset_sensori", "on"), ("opzione_finestra_audio", "on")], PASSO,
         {"opzioni_offset_sensori", "opzione_finestra_audio"}),
        ("Audio poi Opzioni", [("opzione_finestra_audio", "on"), ("opzioni_offset_sensori", "on")], PASSO,
         {"opzioni_offset_sensori"}),  # « Opzioni On» chiude Audio, aperta prima di lui
        # nello stesso istante i last_changed sono uguali e «le» li include: resta la prima elaborata
        ("Avvisi e Telecomando nello stesso istante", [("opzioni_avvisi", "on"), ("opzioni_vmc", "on")], 0,
         {"opzioni_avvisi"}),
    ]

    async def test_raffica_libera_resta_l_ultima_toccata(self, banco: Banco) -> None:
        """Automazione libera, tocchi nello stesso istante: con la variante resta l'ultima toccata (seconda attesa
        degli scenari a-f e dell'Esclusività), come con i tocchi lenti: il primo evento rende il modello del turn_off
        prima che arrivino gli altri tocchi. Sulla 68e159c resta la prima (prima attesa)."""
        errori = []
        for nome, prima, tocchi, _, (_, attese) in SCENARI:
            await banco.azzera()
            await _apri_prima(banco, prima)
            try:
                await banco.raffica(tocchi)
            except CicloSenzaFine:
                errori.append(f"{nome}: {_ciclo(banco)}")
                continue
            if (aperte := banco.aperte()) != attese:
                errori.append(f"{nome}: aperte {sorted(aperte)}, attese {sorted(attese)} (cambi {banco.cambi})")
        for nome, (tocchi, (_, attese)) in ESCLUSIVITA_SCENARI.items():
            await banco.azzera()
            try:
                await banco.raffica(tocchi)
            except CicloSenzaFine:
                errori.append(f"Esclusività, {nome}: {_ciclo(banco)}")
                continue
            if (aperte := banco.aperte()) != attese:
                errori.append(f"Esclusività, {nome}: aperte {sorted(aperte)}, attese {sorted(attese)}")
        if errori:
            pytest.fail("\n".join(errori))

    async def test_finestre_toccate_di_fila_con_l_automazione_occupata(self, banco: Banco) -> None:
        """Automazione occupata (esecuzione lunga vera), tutte le finestre chiuse, due finestre che si chiudono a vicenda
        toccate una dopo l'altra (PASSO secondi): resta aperta l'ultima toccata, come con l'automazione libera; Opzioni
        poi Audio restano aperte tutte e due (Audio è stata aperta dopo l'evento di Opzioni). Nello stesso istante
        resta la prima elaborata. Sulla 68e159c («resta la prima») restano Avvisi e Opzioni; sulla b41 il ciclo senza
        fine."""
        errori = []
        for nome, tocchi, passo, attese in self.SCENARI_DI_FILA:
            await banco.azzera()
            try:
                await banco.occupa()
                banco.cambi.clear()
                for i, (finestra, verso) in enumerate(tocchi):
                    if i and passo:
                        await banco.tempo(passo)
                    await banco.hass.services.async_call("input_boolean", f"turn_{verso}", {"entity_id": IB + finestra},
                                                         blocking=True)
                await banco.lavora()
                in_corso = banco.correnti()
                await banco.libera()
            except CicloSenzaFine:
                errori.append(f"{nome}: {_ciclo(banco)}")
                continue
            assert in_corso == 1 + len(tocchi), (nome, in_corso)
            assert banco.correnti() == 0, nome
            if (aperte := banco.aperte()) != attese:
                errori.append(f"{nome}: aperte {sorted(aperte)}, attese {sorted(attese)} (cambi {banco.cambi})")
            errori += [f"{nome}: {e}" for e in _regole(aperte, set(), tocchi)]
        if errori:
            pytest.fail("\n".join(errori))
