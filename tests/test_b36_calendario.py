"""Prove della 9.0.0b36, fetta CALENDARIO (scelte 3, 4 e 5 del proprietario sull'audit 1:1 della b34).

C1-3: con la Spia Comando non eseguito del Calendario accesa e poi un'allerta Congelamento o Δ Temp., il ritorno della
VMC (trigger «calendario_ritorno_comando») aspetta la fine di Congelamento e Δ Temp.; a fine allerta il blocco
«Calendario in transizione» non fa la ripresa dell'allerta: senza fasce finite o iniziate spegne e riaccende la spia
(nuovo riferimento per il controllo «velocita' cambiata», dopo i comandi dell'allerta) e il ritorno della VMC fa
ripartire la Fascia con la sua velocita' (o ripete la Velocita' 0/1 in sospeso); con una fascia finita o iniziata
durante l'allerta spegne la spia e decide il trigger del giorno.
C1-2: al ritorno della corrente durante una Fascia i 32 s si contano da quando la velocita' torna leggibile (lettura
TCP valida), non dal ping: condizione nel trigger, nella guardia e nelle 2 copie del Countdown; nel riallineamento al
riavvio (trigger di stato) con la velocita' ancora illeggibile si riaccende la Spia Black-Out del Calendario e la Fascia
riparte con il trigger del ritorno.
C1-5: i 2 rami dello spegnimento di «VMC ON/OFF in Funzione del Calendario» durante una Fascia escono come i 14 rami
«Off» (lettura persa per il tempo di rilevazione del Black-Out) con la stessa memoria (Black-Out) e la stessa Spia
Comando non eseguito; il ritorno della VMC ripete la Velocita' 0 anche con l'interruttore del Calendario spento, salvo
velocita' cambiata nel frattempo; con la Spia Inquinanti accesa e la memoria della partenza da Velocita' 0 accesa o
l'interruttore spento ripete la Velocita' 1, dopo aver rimesso le memorie Inquinanti come le lascia lo spegnimento (anche
se intanto gli Inquinanti hanno memorizzato la velocita' letta prima), cosi' a fine Inquinanti la VMC torna a Velocita' 0.
Nessun tempo nuovo.

Le prove dinamiche usano il piccolo esecutore di tests/test_b35_calendario.py (condizioni rese da Home Assistant,
spie scritte negli stati, cicli registrati)."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any

import pytest
from homeassistant.util import dt as dt_util

from tests.test_b35_calendario import (
    ATTESA,
    BO,
    DELTA,
    FASE,
    GELO,
    INTERRUTTORE,
    IP,
    LETTURA,
    LETTURA_INTERFACCIA,
    LETTURA_PERSA,
    MEMORIA,
    PKG,
    SPIA,
    SPIA_BO,
    SPIA_CNE,
    SPIA_V0,
    TCP,
    _automazione,
    _esegui,
    _nuovo_esito,
    _pacchetto,
    _rami,
    _rami_off,
    _render,
    _stato_base,
    _testo,
)

TCP_OK = f"states('{TCP}') not in ['unavailable', 'unknown', '']"
SPIA_CO2 = "input_boolean.vmc_master_spia_co2_o_voc"
PARTENZA = "input_boolean.vmc_master_spia_co2_o_voc_partenza_ritorno_velocita_0"
SPIA_V1 = "input_boolean.vmc_master_spia_velocita_1"
FASCIA_1 = "script.vmc_master_calendario_fascia_1_on"
ALLERTE = {"Congelamento OFF": (GELO, "input_boolean.vmc_master_spia_velocita_2_congelamento"),
           "delta_temp_OFF": (DELTA, "input_boolean.vmc_master_spia_velocita_2_delta_temp_verifica_soglia_valore")}
SPEGNIMENTO = {"Velocità 1": "Calendario Off tra Fascie e Spia Inquinanti ON", "Velocità 0": "Calendario Off tra Fascie"}
V1_CO2 = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc"
V1_PDR = "input_boolean.vmc_master_spia_velocita_1_co2_o_voc_pdr"
V2_CO2 = "input_boolean.vmc_master_spia_velocita_2_co2_o_voc"
MEMORIE_CO2 = [f"input_boolean.vmc_master_spia_velocita_{v}_co2_o_voc"
               for v in ("0", "2", "3", "4", "iperventilazione", "notturna", "freecooling")]
MEMORIA_V1 = MEMORIA.replace("'Velocità 0'", "'Velocità 1'")
SPIA_V1_CNE = SPIA.replace("'Velocità 0'", "'Velocità 1'")


def _trigger(ident: str) -> dict[str, Any]:
    (trigger,) = [t for t in _automazione()["triggers"] if t.get("id") == ident]
    return trigger


def _norm(testo: str) -> str:
    return " ".join(testo.split())


def _copia_guardia(ident: str) -> str:
    testo = _testo("vmc_master_automazione.txt")
    copia = testo[testo.index(f"{{%- elif trigger.id == '{ident}' -%}}\n"):]
    return copia[copia.index("\n") + 1: copia.index("      {%- elif trigger.id == ")]


def _ramo_ritorno() -> dict[str, Any]:
    return _rami(_automazione())["calendario_ritorno_comando"]


def _domenica(hass, freezer, ora: tuple[int, int]) -> float:
    """Domenica 22-11-2026 all'ora data, 1° Fascia 08:00-10:00 e 2° Fascia 18:00-20:00 valide; restituisce l'ora."""
    freezer.move_to(datetime(2026, 11, 22, *ora, tzinfo=dt_util.get_default_time_zone()))
    assert dt_util.now().weekday() == 6
    _stato_base(hass)
    for chiave, valore in (("accensione_domenica", "08:00:00"), ("spegnimento_domenica", "10:00:00"),
                           ("accensione_domenica_2", "18:00:00"), ("spegnimento_domenica_2", "20:00:00")):
        hass.states.async_set(f"input_datetime.vmc_master_{chiave}", valore)
    for sensore in ("accensione", "spegnimento"):
        for fascia in ("", "_2"):
            hass.states.async_set(f"sensor.vmc_master_status_{sensore}_vmc_tramite_calendario{fascia}", "Domenica")
    return time.time()


def _allerta_in_corso(hass, ramo: str, ora: float, spia_cne_fa: float = 120) -> None:
    """Spia Comando non eseguito accesa da spia_cne_fa secondi, poi l'allerta ha portato la VMC a Velocita' 0 (lettura
    cambiata 60 s fa, dopo l'accensione della spia) e ha memorizzato la Velocita' 2 letta all'inizio."""
    spia, memoria = ALLERTE[ramo]
    hass.states.async_set(SPIA_CNE, "on", timestamp=ora - spia_cne_fa)
    hass.states.async_set(spia, "on")
    hass.states.async_set(memoria, "on")
    hass.states.async_set(TCP, "VMGO,00000", timestamp=ora - 60)
    hass.states.async_set(LETTURA, "Velocità 0", timestamp=ora - 60)
    hass.states.async_set(LETTURA_INTERFACCIA, "Velocità 0", timestamp=ora - 60)


def _fine_allerta(hass, ramo: str) -> tuple[bool, dict[str, list[Any]]]:
    """Esegue il ramo di fine allerta come fa l'automazione, fino alla prima condizione o allo stop."""
    esito = _nuovo_esito()
    continua = _esegui(hass, _rami(_automazione())[ramo]["sequence"], {}, esito)
    return continua, esito


# ------------------------------------------------------------------------------------------------ C1-3 (trigger)
@pytest.mark.parametrize(("gelo", "delta", "atteso"), [("off", "off", "True"), ("on", "off", "False"),
                                                         ("off", "on", "False"), ("on", "on", "False")])
async def test_c1_3_il_ritorno_aspetta_la_fine_di_congelamento_e_delta(hass, gelo, delta, atteso) -> None:
    hass.states.async_set(SPIA_CNE, "on")
    hass.states.async_set(TCP, "VMGO,00002")
    hass.states.async_set(FASE, "0.0")
    hass.states.async_set(GELO, gelo)
    hass.states.async_set(DELTA, delta)
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == atteso


def test_c1_3_trigger_e_copia_nella_guardia() -> None:
    trigger = _trigger("calendario_ritorno_comando")
    testo = _norm(trigger["value_template"])
    assert f"and {TCP_OK} and states('{GELO}') == 'off' and states('{DELTA}') == 'off' )" in testo
    assert _norm(_copia_guardia("calendario_ritorno_comando")) == testo
    assert "for" not in trigger  # nessun tempo nuovo


# ------------------------------------------------------------------------------------------------ C1-3 (fine allerta)
def _blocchi() -> list[dict[str, Any]]:
    rami = _rami(_automazione())
    return [rami[ramo]["sequence"][0] for ramo in ALLERTE]


def test_c1_3_struttura_dei_due_blocchi_di_fine_allerta() -> None:
    gelo, delta = _blocchi()
    for blocco, (spia, _) in zip((gelo, delta), ALLERTE.values()):
        assert blocco["alias"].lstrip().startswith("Calendario in transizione")
        spegni, memorie, fermo = blocco["then"]
        assert spegni["action"] == "input_boolean.turn_off" and spegni["target"] == {"entity_id": SPIA_CNE}
        assert memorie["action"] == "input_boolean.turn_off" and spia in memorie["target"]["entity_id"]
        assert fermo == {"stop": "Ripresa lasciata al Calendario"}
        (sospeso,) = blocco["else"]
        assert sospeso["if"] == [{"condition": "state", "entity_id": SPIA_CNE, "state": "on"}]
        spenta, accesa, memorie_bis, fermo_bis = sospeso["then"]
        assert spenta == {"action": "input_boolean.turn_off", "target": {"entity_id": SPIA_CNE}}
        assert accesa == {"action": "input_boolean.turn_on", "target": {"entity_id": SPIA_CNE}}
        assert memorie_bis == memorie  # stesse memorie dell'allerta spente, spia dell'allerta per ultima
        assert fermo_bis == {"stop": "Ripresa lasciata al Calendario (comando del Calendario in sospeso)"}
        assert "delay" not in str(blocco) and "for" not in blocco
    assert gelo["if"] == delta["if"]
    assert _norm(gelo["else"][0]["alias"]) == _norm(delta["else"][0]["alias"])


@pytest.mark.parametrize("ramo", list(ALLERTE))
async def test_c1_3_fine_allerta_con_la_spia_la_fascia_riparte_con_la_sua_velocita(hass, freezer, ramo) -> None:
    """Fascia 1 in corso (spia accesa, dentro l'orario), comando della Fascia non eseguito (porta 5001 muta), poi
    Congelamento/Δ: la VMC e' a Velocita' 0 dell'allerta e la memoria dell'allerta e' la Velocita' 2 di prima della
    Fascia. A fine allerta nessun ripristino della Velocita' 2: la spia si riaccende, il ritorno della VMC scatta e lo
    script della Fascia riparte (il suo controllo «velocita' cambiata» ora passa)."""
    ora = _domenica(hass, freezer, (9, 0))
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_domenica_1", "on")
    _allerta_in_corso(hass, ramo, ora)
    trigger = _trigger("calendario_ritorno_comando")["value_template"]
    assert _render(hass, trigger) == "False"  # durante l'allerta il ritorno aspetta (b35: scattava e consumava la spia)

    freezer.tick(30)
    continua, esito = _fine_allerta(hass, ramo)
    assert not continua and esito["comandi"] == [] and esito["altro"] == []  # nessun ripristino della Velocita' 2
    assert hass.states.get(SPIA_CNE).state == "on"
    assert abs(hass.states.get(SPIA_CNE).last_changed.timestamp() - time.time()) < 1  # nuovo riferimento
    assert all(hass.states.get(e).state == "off" for e in ALLERTE[ramo])
    assert _render(hass, trigger) == "True"

    esito, variabili = _nuovo_esito(), {}
    _esegui(hass, _ramo_ritorno()["sequence"], variabili, esito)
    assert esito["altro"] == [FASCIA_1] and esito["comandi"] == []
    controllo = _pacchetto()["script"]["vmc_master_calendario_fascia_1_on"]["sequence"][4]["value_template"]
    assert _render(hass, controllo, variabili) == "True"  # la Fascia comanda la sua velocita'
    # con il riferimento della b35 (accensione della spia prima dell'allerta) la Fascia non ripartiva
    assert _render(hass, controllo, {"comando_non_eseguito_dalle": ora - 120}) == "False"


@pytest.mark.parametrize(
    ("caso", "stati", "comando"),
    [
        ("Fascia finita, Velocità 0 di fine Fascia in sospeso", {}, "velocita_0"),
        ("Calendario spento durante la Fascia, Velocità 0 in sospeso", {INTERRUTTORE: "off"}, "velocita_0"),
        ("Calendario spento durante la Fascia con Inquinanti, Velocità 1 in sospeso",
         {INTERRUTTORE: "off", SPIA_CO2: "on", PARTENZA: "on"}, "velocita_1"),
    ],
)
async def test_c1_3_fine_allerta_con_la_spia_senza_fascia(hass, freezer, caso, stati, comando) -> None:
    """Comando di fine Fascia o dello spegnimento del Calendario in sospeso, poi Congelamento: a fine allerta nessun
    ripristino della velocita' memorizzata (quella della Fascia, mai cambiata nella lettura) ma la Velocita' 0 (o 1)
    in sospeso."""
    ora = _domenica(hass, freezer, (11, 0))
    for entita, stato in stati.items():
        hass.states.async_set(entita, stato)
    _allerta_in_corso(hass, "Congelamento OFF", ora)
    freezer.tick(30)
    continua, esito = _fine_allerta(hass, "Congelamento OFF")
    assert not continua and esito["comandi"] == [], caso
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == "True", caso
    esito = _nuovo_esito()
    _esegui(hass, _ramo_ritorno()["sequence"], {}, esito)
    assert esito["comandi"] == [comando] and esito["altro"] == [], caso


@pytest.mark.parametrize(("ora", "spia"), [((11, 0), "domenica_1"),  # 1° Fascia finita durante l'allerta
                                           ((0, 10), "sabato_2"),  # fascia di ieri finita prima della mezzanotte
                                           ((9, 0), None)])  # 1° Fascia iniziata durante l'allerta
async def test_c1_3_fine_allerta_con_fascia_finita_o_iniziata_decide_il_giorno(hass, freezer, ora, spia) -> None:
    """Calendario in transizione: la spia si spegne (il comando lo rifa' il trigger del giorno, 3 s dopo) e il
    ritorno della VMC non scatta, cosi' non manda la velocita' della Fascia finita (o la Velocita' 0) prima del
    trigger del giorno."""
    adesso = _domenica(hass, freezer, ora)
    if spia:
        hass.states.async_set(f"input_boolean.vmc_master_spia_calendario_{spia}", "on")
    _allerta_in_corso(hass, "delta_temp_OFF", adesso)
    continua, esito = _fine_allerta(hass, "delta_temp_OFF")
    assert not continua and esito["comandi"] == []
    assert hass.states.get(SPIA_CNE).state == "off"
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == "False"


async def test_c1_3_fine_allerta_senza_spia_e_senza_transizione_ripresa_normale(hass, freezer) -> None:
    _domenica(hass, freezer, (9, 0))
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_domenica_1", "on")
    for ramo in ALLERTE:
        esito = _nuovo_esito()
        assert _esegui(hass, _rami(_automazione())[ramo]["sequence"][:1], {}, esito)  # il blocco non ferma la ripresa
        assert esito["comandi"] == [] and esito["altro"] == []
        assert hass.states.get(SPIA_CNE).state == "off"


# ------------------------------------------------------------------------------------------------ C1-2 (trigger)
@pytest.mark.parametrize(("tcp", "fase", "atteso"),
                         [("VMGO,00002", "0.0", "True"), ("unavailable", "0.0", "False"), ("unknown", "0.0", "False"),
                          ("", "0.0", "False"), ("VMGO,00002", "2.0", "False"), ("VMGO,00002", "4.0", "True")])
async def test_c1_2_il_ritorno_della_corrente_conta_dalla_lettura_valida(hass, tcp, fase, atteso) -> None:
    hass.states.async_set(SPIA_BO, "on")
    hass.states.async_set(IP, "ON-Line")
    hass.states.async_set(TCP, tcp)
    hass.states.async_set(FASE, fase)
    trigger = _trigger("calendario_ritorno_da_black_out")
    assert _render(hass, trigger["value_template"]) == atteso
    assert trigger["for"] == {"seconds": "{{ states('input_number.vmc_master_attesa_blackout_ripristino') | int(32) }}"}


def test_c1_2_copie_nella_guardia_e_nel_countdown() -> None:
    testo = _norm(_trigger("calendario_ritorno_da_black_out")["value_template"])
    assert f"and states('{IP}') == \"ON-Line\" and {TCP_OK} )" in testo
    assert _norm(_copia_guardia("calendario_ritorno_da_black_out")) == testo
    pacchetto = _testo("vmc_master.yaml").replace("\r\n", "\n")
    for verso in ("ON", "OFF"):
        etichetta = f'id: "{verso}|blackout_ripristino|blackout_ripristino|Calendario - VMC di nuovo ON-Line dopo un Black-Out"'
        assert pacchetto.count(etichetta) == 1
        copia = pacchetto[pacchetto.index(etichetta):]
        copia = copia[copia.index("value_template: |-\n") + len("value_template: |-\n"): copia.index("      - trigger:")]
        if verso == "OFF":
            apertura = "{%- set vmc_master_esito -%}"
            copia = copia[copia.index(apertura) + len(apertura): copia.index("{%- endset -%}")]
        assert _norm(copia) == testo, verso


# ------------------------------------------------------------------------------------------------ C1-2 (ramo 97)
def _riallineamento(hass, tcp: str) -> tuple[bool, dict[str, list[Any]]]:
    """Corrente tornata durante il riallineamento al riavvio (fase 2) con la 1° Fascia di lunedi' in corso; la lettura
    memorizzata e' quella di prima del Black-Out."""
    _stato_base(hass)
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_lunedi_1", "on")
    hass.states.async_set(FASE, "2.0")
    hass.states.async_set(TCP, tcp)
    hass.states.async_set(LETTURA_INTERFACCIA, "Velocità 2")
    hass.states.async_set(LETTURA, "Velocità 2")
    esito = _nuovo_esito()
    passi = _rami(_automazione())["calendario_ritorno_da_black_out_riallineamento"]["sequence"]
    return _esegui(hass, passi, {}, esito), esito


async def test_c1_2_riallineamento_con_la_velocita_illeggibile_memorizza_il_black_out(hass) -> None:
    continua, esito = _riallineamento(hass, "unavailable")
    assert not continua and esito["altro"] == [] and esito["comandi"] == []  # b35: script della Fascia gia' qui
    assert hass.states.get(SPIA_BO).state == "on"
    trigger = _trigger("calendario_ritorno_da_black_out")["value_template"]
    assert _render(hass, trigger) == "False"  # fase 2 e lettura assente
    hass.states.async_set(FASE, "4.0")
    assert _render(hass, trigger) == "False"  # lettura ancora assente
    hass.states.async_set(TCP, "VMGO,00001")
    assert _render(hass, trigger) == "True"  # da qui i 32 s del ritorno, poi la Fascia (ramo del ritorno)
    esito = _nuovo_esito()
    _esegui(hass, _rami(_automazione())["calendario_ritorno_da_black_out"]["sequence"], {}, esito)
    assert esito["altro"] == [FASCIA_1] and hass.states.get(SPIA_BO).state == "off"


async def test_c1_2_riallineamento_con_la_velocita_leggibile_come_prima(hass) -> None:
    continua, esito = _riallineamento(hass, "VMGO,00001")
    assert continua and esito["altro"] == [FASCIA_1]
    assert hass.states.get(SPIA_BO).state == "off"


async def test_c1_2_riallineamento_senza_fascia_nessuna_memoria(hass) -> None:
    _stato_base(hass)
    hass.states.async_set(TCP, "unavailable")
    esito = _nuovo_esito()
    _esegui(hass, _rami(_automazione())["calendario_ritorno_da_black_out_riallineamento"]["sequence"], {}, esito)
    assert esito["altro"] == [] and hass.states.get(SPIA_BO).state == "off"


# ------------------------------------------------------------------------------------------------ C1-5 (struttura)
def test_c1_5_rami_dello_spegnimento_come_i_rami_off() -> None:
    dati = _automazione()
    rami = _rami(dati)
    off = _rami_off(dati)["1° Lunedì Off"]["sequence"]
    i = next(k for k, p in enumerate(off) if "repeat" in p)
    for velocita, ident in SPEGNIMENTO.items():
        opzione = rami[ident]["sequence"][0]["choose"][0]
        passi = opzione["sequence"]
        assert SPIA_CNE in passi[0]["target"]["entity_id"]  # il comando dello spegnimento sostituisce quello in sospeso
        k = next(n for n, p in enumerate(passi) if "repeat" in p)
        (fine,) = passi[k]["repeat"]["until"]
        assert fine["alias"] == off[i]["repeat"]["until"][0]["alias"]
        assert fine["value_template"] == off[i]["repeat"]["until"][0]["value_template"].replace(
            "'Velocità 0'", f"'{velocita}'")
        assert fine["value_template"].endswith(f" or {LETTURA_PERSA} }}}}")
        memoria, spia = passi[k + 1:]
        if velocita == "Velocità 0":
            assert [memoria, spia] == [off[i + 2], off[i + 3]]
        else:
            assert memoria["if"] == [{"condition": "template", "value_template": MEMORIA_V1}]
            assert memoria["then"][0]["target"]["entity_id"] == SPIA_V1
            assert memoria["then"][1]["target"]["entity_id"][0] == SPIA_V0
            assert spia["if"] == [{"condition": "template", "value_template": SPIA_V1_CNE}]
            assert spia["then"] == [{"action": "input_boolean.turn_on", "target": {"entity_id": SPIA_CNE}}]
        assert "delay" not in str(passi[k + 1:])


def test_c1_5_ramo_del_ritorno_ripete_la_velocita_1_con_lo_stesso_ciclo() -> None:
    dati = _automazione()
    scelta = _ramo_ritorno()["sequence"][3]["choose"]
    terza, quarta = scelta[2], scelta[3]
    assert [_norm(c["value_template"]) for c in terza["conditions"][:3]] == [
        _norm(c["value_template"]) for c in quarta["conditions"][:3]]
    # Velocita' 1 con la Spia Inquinanti accesa e la memoria della partenza da Velocita' 0 accesa o l'interruttore
    # spento; la terza opzione esclude esattamente lo stesso caso
    caso = (f"states('{SPIA_CO2}') == 'on' and (states('{PARTENZA}') == 'on' or states('{INTERRUTTORE}') == 'off')")
    assert len(terza["conditions"]) == len(quarta["conditions"]) == 4
    assert _norm(terza["conditions"][3]["value_template"]) == f"{{{{ not ({caso}) }}}}"
    assert _norm(quarta["conditions"][3]["value_template"]) == f"{{{{ {caso} }}}}"
    passi_74 = _rami(dati)[SPEGNIMENTO["Velocità 1"]]["sequence"][0]["choose"][0]["sequence"]
    k = next(n for n, p in enumerate(passi_74) if "repeat" in p)
    # prima del ciclo le memorie Inquinanti come le lascia lo spegnimento: memorie di velocita' spente (stesso elenco e
    # stesso ordine dello spegnimento) e stessa accensione di spia, partenza da Velocita' 0 e Velocita' 1 e PdR
    spente, accese = quarta["sequence"][:2]
    assert spente["action"] == "input_boolean.turn_off"
    assert spente["target"]["entity_id"] == [e for e in passi_74[0]["target"]["entity_id"] if e in MEMORIE_CO2]
    assert spente["target"]["entity_id"] == MEMORIE_CO2
    assert passi_74[k - 2]["action"] == "input_boolean.turn_on" and "alias" not in passi_74[k - 2]
    assert {c: v for c, v in accese.items() if c != "alias"} == passi_74[k - 2]
    assert set(accese["target"]["entity_id"]) == {V1_PDR, PARTENZA, SPIA_CO2, V1_CO2}
    assert quarta["sequence"][2:] == passi_74[k - 1:]
    assert "script." not in str(quarta)
    # l'interruttore del Calendario solo nelle opzioni della Fascia
    condizione = _ramo_ritorno()["sequence"][2]["value_template"]
    assert INTERRUTTORE not in condizione
    for opzione in scelta[:2]:
        assert {"condition": "state", "entity_id": INTERRUTTORE, "state": "on"}.items() <= opzione["conditions"][1].items()
    for opzione in scelta[2:]:
        assert INTERRUTTORE not in str(opzione["conditions"][:3])


# ------------------------------------------------------------------------------------------------ C1-5 (dinamica)
def _spegnimento(hass, velocita: str, ip: str) -> dict[str, list[Any]]:
    """L'utente spegne l'interruttore del Calendario durante la 1° Fascia di martedi' (VMC a Velocita' 2) mentre la
    velocita' non si legge da 36 s."""
    _stato_base(hass)
    hass.states.async_set(INTERRUTTORE, "off")
    hass.states.async_set("input_boolean.vmc_master_spia_calendario_martedi_1", "on")
    hass.states.async_set(SPIA_CNE, "on", timestamp=time.time() - 300)  # comando della Fascia in sospeso
    hass.states.async_set(LETTURA, "Velocità 2", timestamp=time.time() - 600)
    if velocita == "Velocità 1":
        hass.states.async_set(SPIA_CO2, "on")
    hass.states.async_set(TCP, "unavailable", timestamp=time.time() - 36)
    hass.states.async_set(IP, ip)
    esito = _nuovo_esito()
    assert _esegui(hass, _rami(_automazione())[SPEGNIMENTO[velocita]]["sequence"], {}, esito)
    assert esito["comandi"] == [velocita.replace("Velocità ", "velocita_")]
    assert esito["uscita"] == [True]  # b35: la ripetizione non finiva (l'automazione in coda restava ferma)
    assert hass.states.get("input_boolean.vmc_master_spia_calendario_martedi_1").state == "off"
    return esito


@pytest.mark.parametrize("velocita", list(SPEGNIMENTO))
async def test_c1_5_spegnimento_con_la_velocita_illeggibile_spia_comando_non_eseguito(hass, velocita) -> None:
    _spegnimento(hass, velocita, "ON-Line")
    spia = hass.states.get(SPIA_CNE)
    assert spia.state == "on" and abs(spia.last_changed.timestamp() - time.time()) < 1  # nuovo riferimento
    assert hass.states.get(SPIA_V0).state == "off" and hass.states.get(SPIA_V1).state == "off"


@pytest.mark.parametrize(("velocita", "memoria"), [("Velocità 0", SPIA_V0), ("Velocità 1", SPIA_V1)])
async def test_c1_5_spegnimento_con_la_vmc_off_line_memoria_del_black_out(hass, velocita, memoria) -> None:
    _spegnimento(hass, velocita, "OFF-Line")
    assert hass.states.get(memoria).state == "on"
    assert hass.states.get(SPIA_CNE).state == "off"


@pytest.mark.parametrize(
    ("velocita", "tcp", "lettura_fa", "comandi"),
    [
        ("Velocità 0", "VMGO,00002", 600, ["velocita_0"]),  # velocita' invariata: si ripete la Velocita' 0
        ("Velocità 1", "VMGO,00002", 600, ["velocita_1"]),  # con gli Inquinanti la Velocita' 1
        ("Velocità 0", "VMGO,00003", 600, []),  # cambiata durante il silenzio (telecomando): resta
        ("Velocità 1", "VMGO,00003", 600, []),
        ("Velocità 1", "VMGO,00002", 10, []),  # cambiata e tornata dopo l'accensione della spia: si rispetta
    ],
)
async def test_c1_5_ritorno_della_vmc_ripete_il_comando_dello_spegnimento(hass, velocita, tcp, lettura_fa,
                                                                          comandi) -> None:
    _spegnimento(hass, velocita, "ON-Line")
    ora = time.time()
    hass.states.async_set(SPIA_CNE, "off", timestamp=ora - 31)  # spia accesa dallo spegnimento 30 s fa
    hass.states.async_set(SPIA_CNE, "on", timestamp=ora - 30)
    hass.states.async_set(LETTURA, "Velocità 1", timestamp=ora - lettura_fa - 1)
    hass.states.async_set(LETTURA, "Velocità 2", timestamp=ora - lettura_fa)
    hass.states.async_set(TCP, tcp)
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == "True"
    esito = _nuovo_esito()

    def vmc_esegue() -> None:
        hass.states.async_set(TCP, f"VMGO,0000{velocita[-1]}")
        hass.states.async_set(LETTURA, velocita)

    _esegui(hass, _ramo_ritorno()["sequence"], {}, esito, al_ciclo=vmc_esegue)
    assert esito["comandi"] == comandi and esito["altro"] == []
    assert esito["uscita"] == [True] * len(comandi)
    assert hass.states.get(SPIA_CNE).state == "off"


def _memoria_velocita_2_inquinanti(hass) -> None:
    """Mentre la velocita' non si legge gli Inquinanti memorizzano la Velocita' 2 letta prima (ramo «Spia Velocita' 2
    CO2 e/o VOC»): memoria Velocita' 2 accesa, memoria della partenza da Velocita' 0 e memorie Velocita' 1 spente."""
    hass.states.async_set(V2_CO2, "on")
    for entita in (PARTENZA, V1_CO2, V1_PDR):
        hass.states.async_set(entita, "off")


def _memorie_dello_spegnimento(hass) -> None:
    assert all(hass.states.get(e) is None or hass.states.get(e).state == "off" for e in MEMORIE_CO2)
    assert all(hass.states.get(e).state == "on" for e in (SPIA_CO2, PARTENZA, V1_CO2, V1_PDR))


@pytest.mark.parametrize("memoria_v2", [False, True])
async def test_c1_5_ritorno_con_gli_inquinanti_rimette_le_memorie_dello_spegnimento(hass, memoria_v2) -> None:
    """Caso del simulatore: 1° Fascia a Velocita' 2, allerta CO2, velocita' illeggibile, Calendario spento; lo
    spegnimento esce con la Spia Comando non eseguito e intanto gli Inquinanti memorizzano la Velocita' 2 letta prima.
    Al ritorno della lettura (VMC ancora a Velocita' 2) si ripete la Velocita' 1 con le memorie Inquinanti dello
    spegnimento: a fine Inquinanti la VMC torna a Velocita' 0 (prima: Velocita' 0 subito, poi di nuovo la Velocita' 1
    degli Inquinanti)."""
    _spegnimento(hass, "Velocità 1", "ON-Line")
    _memorie_dello_spegnimento(hass)
    if memoria_v2:
        _memoria_velocita_2_inquinanti(hass)
    ora = time.time()
    hass.states.async_set(SPIA_CNE, "off", timestamp=ora - 31)  # spia accesa dallo spegnimento 30 s fa
    hass.states.async_set(SPIA_CNE, "on", timestamp=ora - 30)
    hass.states.async_set(TCP, "VMGO,00002")
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == "True"
    esito = _nuovo_esito()

    def vmc_esegue() -> None:
        hass.states.async_set(TCP, "VMGO,00001")
        hass.states.async_set(LETTURA, "Velocità 1")

    _esegui(hass, _ramo_ritorno()["sequence"], {}, esito, al_ciclo=vmc_esegue)
    assert esito["comandi"] == ["velocita_1"] and esito["uscita"] == [True] and esito["altro"] == []
    _memorie_dello_spegnimento(hass)
    assert hass.states.get(SPIA_CNE).state == "off"


@pytest.mark.parametrize(("interruttore", "partenza", "comando"), [
    ("off", "off", "velocita_1"),  # Calendario spento con gli Inquinanti: Velocita' 1 anche senza la memoria
    ("on", "on", "velocita_1"),  # memoria della partenza da Velocita' 0 accesa (come la b36 prima)
    ("on", "off", "velocita_0"),  # Fascia finita con gli Inquinanti: Velocita' 0 (Foglio A25)
])
async def test_c1_5_ritorno_con_gli_inquinanti_quale_velocita(hass, interruttore, partenza, comando) -> None:
    _stato_base(hass)
    hass.states.async_set(INTERRUTTORE, interruttore)
    hass.states.async_set(SPIA_CNE, "on", timestamp=time.time() - 60)
    hass.states.async_set(SPIA_CO2, "on")
    _memoria_velocita_2_inquinanti(hass)
    hass.states.async_set(PARTENZA, partenza)
    hass.states.async_set(TCP, "VMGO,00002", timestamp=time.time() - 600)
    hass.states.async_set(LETTURA, "Velocità 2", timestamp=time.time() - 600)
    esito = _nuovo_esito()
    _esegui(hass, _ramo_ritorno()["sequence"], {}, esito)
    assert esito["comandi"] == [comando]
    assert hass.states.get(V2_CO2).state == ("off" if comando == "velocita_1" else "on")


async def test_c1_5_fine_fascia_con_inquinanti_resta_la_velocita_0(hass) -> None:
    """Dopo la fine della Fascia con gli Inquinanti la memoria della partenza da Velocita' 0 e' spenta: si ripete la
    Velocita' 0 e poi la logica Inquinanti riparte dalla VMC ferma (Foglio A25)."""
    _stato_base(hass)
    hass.states.async_set(SPIA_CNE, "on", timestamp=time.time() - 60)
    hass.states.async_set(SPIA_CO2, "on")
    hass.states.async_set(LETTURA, "Velocità 1", timestamp=time.time() - 600)
    esito = _nuovo_esito()
    _esegui(hass, _ramo_ritorno()["sequence"], {}, esito)
    assert esito["comandi"] == ["velocita_0"]


# ------------------------------------------------------------------------------------------------ regole
def test_nessun_tempo_nuovo_e_file_validi() -> None:
    automazione = _testo("vmc_master_automazione.txt")
    assert "\r" not in automazione
    dati = (PKG / "vmc_master.yaml").read_bytes()
    assert dati.count(b"\r\n") == dati.count(b"\n")
    assert _automazione()["mode"] == "queued"
    for ident in ("calendario_ritorno_comando", "calendario_ritorno_da_black_out"):
        assert _norm(_copia_guardia(ident)) == _norm(_trigger(ident)["value_template"])
    # le attese nuove riusano solo l'helper del tempo di rilevazione del Black-Out (nessun valore nuovo)
    assert ATTESA in LETTURA_PERSA


# ------------------------------------------------------------------------------------------------ con Home Assistant
async def test_rami_cambiati_validi_per_home_assistant(hass) -> None:
    import homeassistant.helpers.config_validation as cv

    for ident in ("calendario_ritorno_comando", "calendario_ritorno_da_black_out_riallineamento", "Congelamento OFF",
                  "delta_temp_OFF", *SPEGNIMENTO.values()):
        cv.SCRIPT_SCHEMA(_rami(_automazione())[ident]["sequence"])


async def test_c1_3_fine_allerta_con_il_motore_di_home_assistant(hass) -> None:
    """Stesso caso eseguito dal motore degli script di Home Assistant (if/else e stop veri): Calendario spento durante
    la Fascia con la Velocita' 0 in sospeso, poi Congelamento; a fine allerta nessun ripristino della Velocita' 2
    memorizzata e il ritorno della VMC ripete la Velocita' 0."""
    from tests.test_b35_allerte import _esegui as _esegui_ha

    _stato_base(hass)
    hass.states.async_set(INTERRUTTORE, "off")
    _allerta_in_corso(hass, "Congelamento OFF", time.time())
    comandi = await _esegui_ha(hass, _rami(_automazione())["Congelamento OFF"]["sequence"], {}, attesa=1.0)
    assert comandi == []
    assert hass.states.get(SPIA_CNE).state == "on"
    assert time.time() - hass.states.get(SPIA_CNE).last_changed.timestamp() < 5
    assert all(hass.states.get(e).state == "off" for e in ALLERTE["Congelamento OFF"])
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == "True"
    comandi = await _esegui_ha(hass, _ramo_ritorno()["sequence"], {}, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_0"]


async def test_c1_5_ritorno_con_gli_inquinanti_con_il_motore_di_home_assistant(hass) -> None:
    """Caso del simulatore eseguito dal motore degli script di Home Assistant: Calendario spento, Inquinanti presenti
    con la Velocita' 2 memorizzata sulla lettura vecchia; il ritorno della VMC rimette le memorie dello spegnimento e
    invia la Velocita' 1."""
    from tests.test_b35_allerte import _esegui as _esegui_ha

    _stato_base(hass)
    hass.states.async_set(INTERRUTTORE, "off")
    hass.states.async_set(SPIA_CO2, "on")
    _memoria_velocita_2_inquinanti(hass)
    hass.states.async_set(SPIA_CNE, "on", timestamp=time.time() - 30)
    hass.states.async_set(TCP, "VMGO,00002", timestamp=time.time() - 600)
    hass.states.async_set(LETTURA, "Velocità 2", timestamp=time.time() - 600)
    assert _render(hass, _trigger("calendario_ritorno_comando")["value_template"]) == "True"
    comandi = await _esegui_ha(hass, _ramo_ritorno()["sequence"], {}, attesa=0.5)
    assert comandi[:1] == ["vmc_master_velocita_1"]
    _memorie_dello_spegnimento(hass)
