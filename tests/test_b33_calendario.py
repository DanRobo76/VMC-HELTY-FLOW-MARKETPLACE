"""Prove della 9.0.0b33: i comandi del Calendario usano lo stesso ciclo di conferma delle altre allerte (rilievi
A1-1 e A4-2 della verifica profonda, Foglio A27: «ogni comando dell'automazione viene ripetuto ogni 4-5 secondi
finche' la VMC non lo esegue»). I 3 punti:
1) entrata nella Fascia: script della 1° e della 2° Fascia (ogni comando di velocita');
2) uscita dalla Fascia: 14 rami «Off» dell'automazione (Velocita' 0);
3) ritorno della corrente dopo un Black-Out in Fascia: i due rami richiamano gli script del punto 1.
Il primo comando parte nello stesso istante di prima (nessun tempo cambia)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
LETTURA = "sensor.vmc_master_status_ventola_lettura_codice_interpretato"
ETICHETTA = {
    "velocita_0": "Velocità 0", "velocita_1": "Velocità 1", "velocita_2": "Velocità 2", "velocita_3": "Velocità 3",
    "velocita_4": "Velocità 4", "notturna": "Notturna", "iperventilazione": "Iperventilazione",
    "freecooling": "Free Cooling",
}
UTENTE = (f"(vel_prima_del_comando not in ['Non disponibile', 'unknown', 'unavailable', ''] and "
          f"states('{LETTURA}') not in [vel_prima_del_comando, 'Non disponibile', 'unknown', 'unavailable', ''])")
BLACK_OUT = "is_state('binary_sensor.vmc_master_black_out_rilevato', 'on')"
OFF_LINE = ("(is_state('sensor.vmc_master_status_ip_interfaccia', 'OFF-Line') and "
            "(now() - states.sensor.vmc_master_status_ip_interfaccia.last_changed).total_seconds() >= "
            "states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32))")
# b34 (B1-1): anche la lettura della velocita' persa (porta 5001 muta con il ping OK) per il tempo di rilevazione del
# Black-Out ferma il ciclo, sia in Fascia sia nei 14 rami «Off»
LETTURA_PERSA = ("(is_state('sensor.vmc_master_status_ventola', 'unavailable') and "
                 "(now() - states.sensor.vmc_master_status_ventola.last_changed).total_seconds() >= "
                 "states('input_number.vmc_master_attesa_blackout_rilevazione') | int(32))")
FASCE = ("vmc_master_calendario_fascia_1_on", "vmc_master_calendario_fascia_2_on")


def _script() -> dict[str, Any]:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))["script"]


def _rami_automazione() -> list[dict[str, Any]]:
    dati = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    return [r for blocco in dati["actions"] if "choose" in blocco for r in blocco["choose"]]


def _passi(nodo: Any, dentro_repeat: bool = False) -> Iterator[tuple[dict[str, Any], bool]]:
    """Tutti i passi (dict con «action») e se stanno dentro un repeat."""
    if isinstance(nodo, dict):
        if "action" in nodo:
            yield nodo, dentro_repeat
        for chiave, valore in nodo.items():
            yield from _passi(valore, dentro_repeat or chiave == "repeat")
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _passi(valore, dentro_repeat)


def _cicli(nodo: Any) -> Iterator[dict[str, Any]]:
    if isinstance(nodo, dict):
        if "repeat" in nodo:
            yield nodo["repeat"]
        for valore in nodo.values():
            yield from _cicli(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _cicli(valore)


def _controlla_ciclo(ciclo: dict[str, Any], fascia: bool) -> str:
    """Il ciclo standard: comando, 1 s, rilettura della velocita', 3 s; until velocita' raggiunta, scelta
    dell'utente o Black-Out rilevato (in Fascia anche VMC OFF-Line per il tempo di rilevazione del Black-Out); b34: in
    Fascia e nei rami «Off» anche lettura della velocita' persa per il tempo di rilevazione del Black-Out."""
    comando, uno, rilettura, tre = ciclo["sequence"]
    assert comando["action"].startswith("shell_command.vmc_master_")
    nome = comando["action"].removeprefix("shell_command.vmc_master_")
    assert uno == {"delay": {"hours": 0, "minutes": 0, "seconds": 1, "milliseconds": 0}}
    assert rilettura["action"] == "homeassistant.update_entity"
    assert rilettura["target"] == {"entity_id": "sensor.vmc_master_status_ventola"}
    assert tre == {"delay": {"hours": 0, "minutes": 0, "seconds": 3, "milliseconds": 0}}
    (fine,) = ciclo["until"]
    attesa = f"{{{{ states('{LETTURA}') == '{ETICHETTA[nome]}' or {UTENTE} or {BLACK_OUT}"
    attesa += f" or {OFF_LINE} or {LETTURA_PERSA} }}}}" if fascia else f" or {LETTURA_PERSA} }}}}"
    assert fine["value_template"] == attesa
    return nome


def test_entrata_in_fascia_ogni_comando_nel_ciclo_di_conferma() -> None:
    """Punto 1 (e 3): negli script della Fascia nessun comando resta singolo; la velocita' prima del comando e'
    memorizzata dopo i 5 s (senza, il ciclo si fermerebbe subito: la scelta dell'utente sarebbe sempre vera)."""
    script = _script()
    totale = 0
    for nome in FASCE:
        sequenza = script[nome]["sequence"]
        assert sequenza[0]["action"] == "input_boolean.turn_off", nome  # spie del Black-Out (A4-1), restano prime
        # b34: subito dopo si spegne la Spia Comando non eseguito, che l'ultimo passo riaccende se serve
        assert sequenza[1]["action"] == "input_boolean.turn_off", nome
        assert sequenza[1]["target"] == {"entity_id": "input_boolean.vmc_master_spia_calendario_comando_non_eseguito"}
        assert sequenza[2] == {"delay": {"hours": 0, "minutes": 0, "seconds": 5, "milliseconds": 0}}, nome
        assert sequenza[3]["variables"] == {"vel_prima_del_comando": f"{{{{ states('{LETTURA}') }}}}"}, nome
        # b34: dopo la velocita' prima del comando, il controllo del ritorno dopo un comando non eseguito
        assert sequenza[4]["condition"] == "template" and "comando_non_eseguito_dalle" in sequenza[4]["value_template"]
        assert "choose" in sequenza[5] and "if" in sequenza[6] and len(sequenza) == 7, nome
        comandi = [(p, dentro) for p, dentro in _passi(sequenza) if p["action"].startswith("shell_command.")]
        assert comandi and all(dentro for _, dentro in comandi), nome
        cicli = list(_cicli(sequenza))
        assert len(cicli) == len(comandi) == 180, nome
        assert {_controlla_ciclo(c, fascia=True) for c in cicli} == set(ETICHETTA), nome
        assert script[nome]["mode"] == "restart", nome
        assert "il comando viene ripetuto (circa ogni 4 s) finché la VMC non lo esegue" in " ".join(
            script[nome]["description"].split()), nome
        totale += len(cicli)
    assert totale == 360


def test_uscita_dalla_fascia_velocita_0_nel_ciclo_di_conferma() -> None:
    """Punto 2: i 14 rami «Off» mandano la Velocita' 0 con il ciclo di conferma; lo script di fine Fascia (che
    azzera le spie) viene dopo, e dopo ancora la memoria del Black-Out arrivato prima della conferma (Priorita' 7)."""
    rami = [r for r in _rami_automazione()
            if isinstance(r["conditions"][0].get("id"), str) and r["conditions"][0]["id"].endswith(" Off")
            and r["conditions"][0]["id"][:2] in ("1°", "2°")]
    assert len(rami) == 14
    for ramo in rami:
        passi = ramo["sequence"]
        assert not [p for p in passi if str(p.get("action", "")).startswith("shell_command.")], ramo["conditions"]
        i = next(k for k, p in enumerate(passi) if "repeat" in p)
        assert passi[i - 1]["variables"] == {"vel_prima_del_comando": f"{{{{ states('{LETTURA}') }}}}"}
        assert _controlla_ciclo(passi[i]["repeat"], fascia=False) == "velocita_0"
        assert passi[i + 1]["action"] == "script.vmc_master_calendario_fascia_1_o_2_off"
        memoria = passi[i + 2]
        assert memoria["alias"].startswith("Black-Out prima della conferma -> memorizza la Velocità 0")
        assert memoria["if"][0]["value_template"] == (
            f"{{{{ {BLACK_OUT} and states('{LETTURA}') != 'Velocità 0' }}}}")
        assert memoria["then"][0]["target"]["entity_id"] == "input_boolean.vmc_master_spia_velocita_0"
        assert memoria["then"][0]["action"] == "input_boolean.turn_on"
        assert len(memoria["then"][1]["target"]["entity_id"]) == 7
        assert memoria["then"][1]["action"] == "input_boolean.turn_off"


def test_ritorno_dal_black_out_in_fascia_usa_lo_script_con_il_ciclo() -> None:
    """Punto 3: i rami del ritorno della corrente in Fascia richiamano lo script della Fascia (che attende la fine
    del ciclo: l'automazione in coda non esegue altri eventi nel frattempo, come negli altri cicli) e non mandano
    comandi singoli."""
    rami = {r["conditions"][0]["id"]: r for r in _rami_automazione() if isinstance(r["conditions"][0].get("id"), str)}
    for id_ in ("calendario_ritorno_da_black_out", "calendario_ritorno_da_black_out_riallineamento"):
        passi = list(_passi(rami[id_]["sequence"]))
        azioni = [p["action"] for p, _ in passi]
        assert not [a for a in azioni if a.startswith("shell_command.")], id_
        assert [a for a in azioni if a.startswith("script.")] == [
            "script.vmc_master_calendario_fascia_1_on", "script.vmc_master_calendario_fascia_2_on"], id_
    # anche l'entrata nella Fascia richiama lo script direttamente (attende la fine), non con script.turn_on
    testo = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    assert testo.count("action: script.vmc_master_calendario_fascia_1_on\n") == 10  # b34: +1 ritorno dopo un comando non eseguito
    assert testo.count("action: script.vmc_master_calendario_fascia_2_on\n") == 10


def test_tutti_i_cicli_dell_automazione_restano_uguali() -> None:
    """Le altre allerte non cambiano: tutti i cicli dell'automazione hanno ancora lo stesso until (velocita' raggiunta,
    scelta dell'utente, Black-Out rilevato); nessuno ha la condizione OFF-Line, che vale solo in Fascia. b34 (B1-1):
    la lettura della velocita' persa c'e' solo nei 14 rami «Off» del Calendario."""
    testo = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    assert OFF_LINE not in testo
    assert testo.count(LETTURA_PERSA) == 14
    assert testo.count(UTENTE) == 176 + 14 + 17  # 176 nella b32, piu' i 14 rami «Off», piu' i 17 cicli della b34 (B1-2)
