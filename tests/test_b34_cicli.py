"""Prove della 9.0.0b34 (cicli di conferma), rilievi della verifica profonda della b33:
- B1-2: i comandi di velocita' del ripristino dopo il Black-Out («Black-Out Off Vel. 0», 9 comandi, e «Black-Out Off
  Free Cool./Heat.», 6 comandi) e della Velocita' 1 del Free con Inquinanti (2 comandi) erano singoli: ora usano il
  ciclo standard (Foglio A23 e A27: «ogni comando viene ripetuto finche' la VMC non lo esegue");
- B3-1: 3 cicli (comando + 4 s) senza la rilettura immediata: ora 1 s + rilettura + 3 s (sempre 4 s in totale);
  anche gli ultimi 2 cicli senza rilettura: fine Inquinanti in Free (4 s -> 1 s + rilettura + 3 s) e fine Umidita'
  in Free (5 s -> 1 s + rilettura + 4 s, come gli altri cicli dell'Umidita');
- B4-3: Inquinanti ON, opzione Iperventilazione: il ciclo delle spie sta prima del ciclo di comando, come nelle 4
  opzioni gemelle.
Nessun tempo cambia: il ciclo standard dura 4 s a giro, l'attesa di 12 s dopo il ripristino resta dov'era."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
COMANDO = re.compile(r"^shell_command\.vmc_master_(velocita_[0-4]|notturna|freecooling|iperventilazione|\{\{.*\}\})$")
ETICHETTA = {
    "velocita_0": "Velocità 0", "velocita_1": "Velocità 1", "velocita_2": "Velocità 2", "velocita_3": "Velocità 3",
    "velocita_4": "Velocità 4", "notturna": "Notturna", "iperventilazione": "Iperventilazione",
    "freecooling": "Free Cooling",
}
MEMORIA = {"vel_prima_del_comando": f"{{{{ states('{LETTURA}') }}}}"}
UNO = {"delay": {"hours": 0, "minutes": 0, "seconds": 1, "milliseconds": 0}}
TRE = {"delay": {"hours": 0, "minutes": 0, "seconds": 3, "milliseconds": 0}}
QUATTRO = {"delay": {"hours": 0, "minutes": 0, "seconds": 4, "milliseconds": 0}}
RILETTURA = {
    "action": "homeassistant.update_entity",
    "target": {"entity_id": "sensor.vmc_master_status_ventola"},
    "alias": "Rilettura immediata della velocità (la velocità non ancora aggiornata non va presa per una scelta "
             "dell'utente)",
}
UTENTE = (f"(vel_prima_del_comando not in ['Non disponibile', 'unknown', 'unavailable', ''] and "
          f"states('{LETTURA}') not in [vel_prima_del_comando, 'Non disponibile', 'unknown', 'unavailable', ''])")
BLACK_OUT = "is_state('binary_sensor.vmc_master_black_out_rilevato', 'on')"


def _fine(etichetta: str) -> str:
    return f"{{{{ states('{LETTURA}') == '{etichetta}' or {UTENTE} or {BLACK_OUT} }}}}"


def _automazione() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _rami(dati: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Rami dei choose di primo livello, per id del trigger (anche gli id in elenco)."""
    out: dict[str, dict[str, Any]] = {}
    for blocco in dati["actions"]:
        for ramo in blocco.get("choose", []):
            ident = ramo["conditions"][0].get("id")
            for nome in ([ident] if isinstance(ident, str) else ident or []):
                out[nome] = ramo
    return out


def _comandi(nodo: Any, dentro: bool = False) -> Iterator[tuple[str, bool]]:
    """Tutti i comandi di velocita' (anche con template) e se stanno dentro un repeat."""
    if isinstance(nodo, dict):
        azione = nodo.get("action")
        if isinstance(azione, str) and COMANDO.match(azione.strip()):
            yield azione, dentro
        for chiave, valore in nodo.items():
            yield from _comandi(valore, dentro or chiave == "repeat")
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _comandi(valore, dentro)


def _coppie(nodo: Any) -> Iterator[tuple[dict[str, Any], dict[str, Any]]]:
    """Ogni passo con un repeat che contiene un comando di velocita', con il passo che lo precede."""
    if isinstance(nodo, list):
        for i, passo in enumerate(nodo):
            if isinstance(passo, dict) and "repeat" in passo and list(_comandi(passo["repeat"]["sequence"])):
                yield (nodo[i - 1] if i else {}), passo
        for valore in nodo:
            yield from _coppie(valore)
    elif isinstance(nodo, dict):
        for valore in nodo.values():
            yield from _coppie(valore)


def _ciclo_standard(precedente: dict[str, Any], passo: dict[str, Any]) -> str:
    """La forma esatta del ciclo standard; restituisce il nome del comando."""
    assert precedente.get("variables") == MEMORIA
    ciclo = passo["repeat"]
    assert set(ciclo) == {"sequence", "until"}
    comando, uno, rilettura, tre = ciclo["sequence"]
    assert set(comando) == {"data", "action"} and comando["data"] == {}
    nome = comando["action"].removeprefix("shell_command.vmc_master_")
    assert (uno, rilettura, tre) == (UNO, RILETTURA, TRE)
    assert ciclo["until"] == [{"condition": "template", "value_template": _fine(ETICHETTA[nome])}]
    return nome


def test_comandi_di_velocita_fuori_ciclo_solo_quelli_voluti() -> None:
    """B1-2: nell'automazione nessun comando di velocita' resta fuori da un ciclo, tranne i 4 della Velocita' 1 nel
    ramo «Spia Velocità 1 CO₂ e/o VOC»: il trigger chiede gia' la lettura «Velocità 1» da 8 s, il comando la
    ribadisce soltanto (con un ciclo uscirebbe al primo giro)."""
    dati = _automazione()
    tutti = list(_comandi(dati["actions"]))
    # b35 (C1-1): +1, Velocita' 0 di fine Fascia ripetuta nel ramo del ritorno della VMC; b36 (C1-5): +1, Velocita' 1
    # dello spegnimento del Calendario con gli Inquinanti ripetuta nel ramo del ritorno della VMC
    assert len(tutti) == 220
    fuori = [azione for azione, dentro in tutti if not dentro]
    assert fuori == ["shell_command.vmc_master_velocita_1"] * 4
    ramo = _rami(dati)["spia_velocita_1_inquinanti_co2_voc"]
    assert [a for a, dentro in _comandi(ramo) if not dentro] == fuori
    (trigger,) = [t for t in dati["triggers"] if t.get("id") == "spia_velocita_1_inquinanti_co2_voc"]
    assert f"and states('{LETTURA}') == 'Velocità 1'\n" in trigger["value_template"]


def test_ripristino_dopo_il_black_out_ogni_comando_nel_ciclo_standard() -> None:
    """B1-2: «Black-Out Off Vel. 0» (8 memorie PdR, Inquinanti -> Velocita' 1 e il caso senza memorie) e «Black-Out
    Off Free Cool./Heat.» (4 casi e i 2 del caso non coperto): ogni comando nel ciclo standard, uguale a quello dei
    rami «Black-Out Off Vel. 1..4, Notturna, Iperventilazione» a parte il comando; l'attesa di 12 s prima di
    spegnere le spie resta."""
    rami = _rami(_automazione())
    alias_modello: set[str] = set()
    for ident in ("Black-Out Off Vel. 1", "Black-Out Off Vel. 2", "Black-Out Off Vel. 3", "Black-Out Off Vel. 4",
                  "Black-Out Off Notturna", "Black-Out Off Iperventilazione"):
        ((precedente, passo),) = list(_coppie(rami[ident]["sequence"]))
        _ciclo_standard(precedente, passo)
        alias_modello.add(passo["alias"])
    (modello_alias,) = alias_modello
    attesi = {
        "Black-Out Off Vel. 0": ["velocita_0", "velocita_1", "velocita_2", "velocita_3", "velocita_4", "notturna",
                                 "freecooling", "iperventilazione", "velocita_1", "velocita_0"],
        "Black-Out Off Free Cool./Heat.": ["freecooling", "freecooling", "freecooling", "velocita_1", "velocita_1",
                                           "freecooling"],
    }
    for ident, nomi in attesi.items():
        ramo = rami[ident]
        assert all(dentro for _, dentro in _comandi(ramo)), ident
        coppie = list(_coppie(ramo["sequence"]))
        assert [_ciclo_standard(p, c) for p, c in coppie] == nomi, ident
        assert all(c["alias"] == modello_alias for _, c in coppie), ident
        attesa = [p for p in ramo["sequence"] if "wait_template" in p]
        assert len(attesa) == 1 and attesa[0]["timeout"] == "00:00:12", ident
        assert attesa[0]["wait_template"] == (
            f"{{{{ states('{LETTURA}') != vel_prima_del_comando or {BLACK_OUT} }}}}"), ident
        # b36 (scelta): il primo passo e' la velocita' scelta dall'utente prima del ripristino (test_b36_scelta)
        assert ramo["sequence"][1]["variables"] == MEMORIA, ident
    # Inquinanti -> Velocita' 1: la memoria della Velocita' 0 si spegne dopo il ciclo, come prima dopo il comando
    scelta = next(p for p in rami["Black-Out Off Vel. 0"]["sequence"] if "choose" in p)
    inquinanti = next(o for o in scelta["choose"] if o["alias"] == "Inquinanti ON, Partenza Vel.0 -> Vel. 1")
    assert [list(p)[0] for p in inquinanti["sequence"]] == ["variables", "alias", "action"]
    assert inquinanti["sequence"][2]["target"]["entity_id"] == ["input_boolean.vmc_master_spia_velocita_0"]


def test_free_con_inquinanti_velocita_1_nel_ciclo_standard() -> None:
    """B1-2: «Spia Velocità Free Heating/Cooling CO₂ e/o VOC»: le 2 Velocita' 1 (Free programmato) hanno lo stesso
    ciclo del Free Cooling del primo caso, a parte il comando."""
    ramo = _rami(_automazione())["spia_velocita_freecooling_inquinanti_co2_voc"]
    assert all(dentro for _, dentro in _comandi(ramo))
    coppie = list(_coppie(ramo["sequence"]))
    assert [_ciclo_standard(p, c) for p, c in coppie] == ["freecooling", "velocita_1", "velocita_1"]
    assert all(set(c) == {"repeat"} for _, c in coppie)


def test_ogni_ciclo_dell_automazione_ha_la_rilettura_immediata() -> None:
    """B3-1: i cicli dei rami 49, 61 e 63 ora hanno 1 s, la rilettura e 3 s; anche fine Inquinanti in Free (1 s +
    rilettura + 3 s, prima 4 s) e fine Umidita' in Free (1 s + rilettura + 4 s, prima 5 s). Nessun ciclo con un
    comando di velocita' resta senza la rilettura immediata e ogni giro dura come prima (4 s, o 5 s nell'Umidita')."""
    dati = _automazione()
    rami = _rami(dati)
    for ident in ("Rip. Free Cool./Heat. No PdR", "TeVsTi Free-Heating -> Imposta Velocità 0",
                  "TeVsTi Free-Cooling -> Imposta Velocità 0"):
        ((precedente, passo),) = list(_coppie(rami[ident]["sequence"]))
        assert precedente.get("variables") == MEMORIA or ident == "Rip. Free Cool./Heat. No PdR", ident
        sequenza = passo["repeat"]["sequence"]
        assert "if" in sequenza[-4], ident
        assert sequenza[-3:] == [UNO, RILETTURA, TRE], ident
        assert all(dentro for _, dentro in _comandi(rami[ident])), ident
    senza = [c for _, c in _coppie(dati["actions"])
             if not any(p.get("action") == "homeassistant.update_entity" for p in c["repeat"]["sequence"])]
    assert senza == []
    finali = [c["repeat"]["sequence"][-3:] for _, c in _coppie(dati["actions"])
              if "else 'Free Cooling')" in c["repeat"]["until"][0]["value_template"]]
    assert finali.count([UNO, RILETTURA, TRE]) == 2  # Rip. Free Cool./Heat. No PdR, fine Inquinanti in Free
    assert finali.count([UNO, RILETTURA, QUATTRO]) == 1  # fine Umidita' in Free
    assert len(finali) == 3


def test_inquinanti_on_iperventilazione_ciclo_delle_spie_prima() -> None:
    """B4-3: nelle 5 opzioni «Caso Velocità 0 con PdR su Velocità X o Spia Inquinanti su Velocità X» (2, 3, 4,
    Notturna, Iperventilazione) l'ordine e' lo stesso: ciclo delle spie, memoria della velocita', ciclo di comando."""
    dati = _automazione()
    opzioni: dict[str, dict[str, Any]] = {}

    def cerca(nodo: Any) -> None:
        if isinstance(nodo, dict):
            alias = " ".join(str(nodo.get("alias", "")).split())
            trovato = re.match(r"Caso Velocità 0 con PdR su Velocità (\w+) o Spia Inquinanti su Velocità \1$", alias)
            if trovato and "conditions" in nodo:
                assert trovato.group(1) not in opzioni
                opzioni[trovato.group(1)] = nodo
            for valore in nodo.values():
                cerca(valore)
        elif isinstance(nodo, list):
            for valore in nodo:
                cerca(valore)

    cerca(dati["actions"])
    assert set(opzioni) == {"1", "2", "3", "4", "Notturna", "Iperventilazione"}
    del opzioni["1"]  # la Velocita' 1 e' un caso a parte: non ha il ciclo delle spie
    for nome, opzione in opzioni.items():
        spie, memoria, comando = opzione["sequence"]
        assert spie["alias"] == "Ripeti FInchè Le Spie rispettano Le Regole", nome
        assert not list(_comandi(spie)), nome
        attesi = "velocita_" + nome if nome.isdigit() else nome.lower()
        assert _ciclo_standard(memoria, comando) == attesi, nome
