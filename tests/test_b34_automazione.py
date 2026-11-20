"""Prove della b34 (fetta «automazione»): rilievi B3-2, B3-3, B3-4, B3-5, B4-1, B4-2 e B4-4 della verifica profonda
1:1 della b33. Statiche sul testo e sulla struttura YAML; il confronto di versione, il sensore dell'umidità esterna e
la condizione di B4-4 sono resi con l'ambiente Jinja di Home Assistant."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
CONGELAMENTO_O_DELTA = "se Spia Congelamento ON o Spia Delta Temp ON"
DISATTIVAZIONI_FREE = {  # id del trigger -> (gemello con la correzione O2, Free)
    " Disattivazione VMC ON/OFF, in Funzione della Vel. Free Heating precedentemente Armato e Spia Inquinanti ON": (
        "Disattivazione VMC ON/OFF, in Funzione della Vel. Free Heating precedentemente Armato", "freeheating"),
    " Disattivazione VMC ON/OFF, in Funzione della Vel. Free Cooling precedentemente Armato e Spia Inquinanti ON": (
        "Disattivazione VMC ON/OFF, in Funzione della Vel. Free Cooling precedentemente Armato", "freecooling"),
}
VERSIONE_NUOVA = (
    "(((_{x}.split('b'))[0].split('.') | map('int') | list) + [0, 0][(_{x}.split('b'))[0].count('.'):] + "
    "([0, (_{x}.split('b'))[1] | int] if 'b' in _{x} else [1, 0]))"
)
VERSIONE_B33 = (
    "(((_{x}.split('b'))[0].split('.') | map('int') | list) + ([0, (_{x}.split('b'))[1] | int] if 'b' in _{x} else [1, 0]))"
)
# (installata, repository, versione nuova): 5 coppie (*) davano l'esito sbagliato nella b33
COPPIE_VERSIONI = [
    ("9.0.0b33", "9.0.0b34", True), ("9.0.0b34", "9.0.0b33", False),
    ("9.0.0b34", "9.0.0", True), ("9.0.0", "9.0.0b34", False),
    ("9.0.0", "9.0", False),  # (*)
    ("9.0", "9.0.0", False),
    ("9.0.0", "9.0.1", True), ("9.0.1", "9.0.0", False),
    ("9.0.9", "9.1", True), ("9.1", "9.0.9", False),
    ("9.9.9", "10.0.0", True), ("10.0.0", "9.9.9", False),
    ("9.0.0", "9.0.0", False), ("9.0.0b34", "9.0.0b34", False), ("9.0", "9.0", False),
    ("9.0.0b9", "9.0.0b10", True), ("9.0.0b10", "9.0.0b9", False),
    ("9", "9.0.0", False), ("9.0.0", "9", False),  # (*)
    ("9.0b5", "9.0.0b5", False), ("9.0.0b5", "9.0b5", False),  # (*)
    ("9.0b5", "9.0.0", True),  # (*)
    ("9.1.0", "9.1", False),  # (*)
    ("9.1", "9.1.0", False), ("9.1", "9.0.0b34", False), ("9.0.0b34", "9.1", True),
    ("9.0.0", "9.1b1", True), ("9.1b1", "9.0.0", False),
    ("v9.0.0b33", "v9.0.0b34", True), (" 9.0.0 ", "9.0.1", True),
]
VERSIONI_NON_VALIDE = [("9.0.0", "Errore Connessione"), ("unknown", "9.0.0"), ("9.0.0", "unavailable"), ("9.0.0", "")]
STATI_NON_VALIDI = ["Non disponibile", "sconosciuto", "unknown", "unavailable", "", "OFF-Line"]
SCRIPT_DEL_CALENDARIO = {
    "script.vmc_master_calendario_fascia_1_on",
    "script.vmc_master_calendario_fascia_2_on",
    "script.vmc_master_calendario_fascia_1_o_2_off",
}


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8")


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


def _automazione() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))


def _opzioni() -> list[dict]:
    return _automazione()["actions"][1]["choose"]


def _ramo(id_: str) -> dict:
    trovati = [o for o in _opzioni() if any(c.get("condition") == "trigger" and id_ in (
        [c["id"]] if isinstance(c["id"], str) else c["id"]) for c in o["conditions"])]
    assert len(trovati) == 1, id_
    return trovati[0]


def _trigger(id_: str) -> dict:
    trovati = [t for t in _automazione()["triggers"] if t.get("id") == id_]
    assert len(trovati) == 1, id_
    return trovati[0]


def _copia_guardia(id_: str) -> str:
    """La copia nella guardia «Evento ancora valido»: dalle righe dopo «{%- elif trigger.id == '…' -%}» fino al
    successivo elif/else/endif con lo stesso rientro (come in test_b25_package)."""
    righe = _testo("vmc_master_automazione.txt").split("\n")
    testa = "{%- elif trigger.id == '" + id_ + "' -%}"
    trovate = [k for k, r in enumerate(righe) if r.strip() == testa]
    assert len(trovate) == 1, id_
    rientro = len(righe[trovate[0]]) - len(righe[trovate[0]].lstrip())
    fine = next(k for k in range(trovate[0] + 1, len(righe))
                if len(righe[k]) - len(righe[k].lstrip()) == rientro and re.match(r"\{%-? (elif|else|endif)\b", righe[k].strip()))
    return "\n".join(righe[trovate[0] + 1 : fine])


def _passi_congelamento_o_delta(id_: str) -> list[dict]:
    opzioni = [o for o in _ramo(id_)["sequence"][0]["choose"] if o.get("alias") == CONGELAMENTO_O_DELTA]
    assert len(opzioni) == 1, id_
    return opzioni[0]["sequence"]


def _cammina(nodo, visita) -> None:
    if isinstance(nodo, dict):
        visita(nodo)
        for valore in nodo.values():
            _cammina(valore, visita)
    elif isinstance(nodo, list):
        for valore in nodo:
            _cammina(valore, visita)


# ------------------------------------------------------------------------------------------------ B3-2
def test_correzione_o2_anche_nei_rami_con_inquinanti() -> None:
    """B3-2: rami 70 e 72 (Disattivazione Free con Inquinanti), caso Congelamento o Δ: oltre a riaccendere
    l'interruttore spengono l'attesa Free quando il mese non è più programmato, con lo stesso if dei rami 69 e 71."""
    for id_, (gemello, free) in DISATTIVAZIONI_FREE.items():
        passi, passi_gemello = _passi_congelamento_o_delta(id_), _passi_congelamento_o_delta(gemello)
        assert [p["action"] for p in passi[:1]] == ["input_boolean.turn_on"]
        assert passi[0]["target"]["entity_id"] == f"input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_{free}"
        assert len(passi) == len(passi_gemello) == 2
        assert passi[1] == passi_gemello[1], id_
        correzione = passi[1]
        assert "(correzione O2)" in correzione["alias"]
        assert correzione["if"][0]["value_template"] == f"{{{{ states('sensor.vmc_master_status_{free}') != 'OK' }}}}"
        assert correzione["then"][0]["action"] == "input_boolean.turn_off"
        assert correzione["then"][0]["target"]["entity_id"] == (
            f"input_boolean.vmc_master_spia_velocita_freecooling_un_solo_avvio_per_programmazione_{free}"
        )
    assert _testo("vmc_master_automazione.txt").count("(correzione O2)") == 4


# ------------------------------------------------------------------------------------------------ B3-3 / B4-2
def test_nessuna_voce_doppia_nelle_liste_di_entita() -> None:
    """B3-3, B4-2: nessuna lista entity_id dell'automazione contiene due volte la stessa entità."""
    doppie: list = []
    liste = 0

    def visita(nodo: dict) -> None:
        nonlocal liste
        valore = nodo.get("entity_id")
        if isinstance(valore, list):
            liste += 1
            conteggio = Counter(str(v).strip() for v in valore)
            doppie.extend(e for e, n in conteggio.items() if n > 1)

    _cammina(_automazione()["actions"], visita)
    assert liste > 100
    assert doppie == []
    # le 4 liste corrette (rami 14, 156, 158, 160) spengono ancora la finestra Free, una volta sola
    for id_ in ("Opzioni Sub Lim. Δ P. di Rugiada On", "Opzioni Sub Sensori Opzionati On",
                "Opzioni Sub Elementi Chimici On", "Opzioni Sub Elementi Audio On"):
        spente = [p for p in _ramo(id_)["sequence"] if p.get("action") == "input_boolean.turn_off"]
        assert len(spente) == 1, id_
        assert spente[0]["target"]["entity_id"].count("input_boolean.vmc_master_opzioni_free_heating_o_free_cooling") == 1


def test_alias_del_ramo_sub_extra_sensori_off() -> None:
    """B3-3: il ramo «Opzioni Sub Extra Sensori Off» spegne: l'alias dice «Disattivazione», come il suo trigger."""
    ramo = _ramo("Opzioni Sub Extra Sensori Off")
    assert ramo["sequence"][0]["action"] == "input_boolean.turn_off"
    assert ramo["alias"] == "Trigger Disattivazione Sotto Finestra Sensori Extra - Finestra Monitoraggio"
    assert _ramo("Opzioni Sub Extra Sensori On")["alias"].startswith("Trigger Attivazione ")


# ------------------------------------------------------------------------------------------------ B3-4
def test_confronto_di_versione_uguale_in_tutte_le_copie() -> None:
    """B3-4: lo stesso confronto nei trigger ON e OFF, nelle 2 copie della guardia e nelle 2 copie del Countdown."""
    automazione, pacchetto = _testo("vmc_master_automazione.txt"), _testo("vmc_master.yaml")
    for x in ("r", "i"):
        assert automazione.count(VERSIONE_NUOVA.format(x=x)) == 4
        assert pacchetto.count(VERSIONE_NUOVA.format(x=x)) == 2
        assert VERSIONE_B33.format(x=x) not in automazione + pacchetto
    for id_ in ("Repository Update ON", "Repository Update OFF"):
        assert _norm(_copia_guardia(id_)) == _norm(_trigger(id_)["value_template"])


def _modello_versione(id_: str) -> str:
    """Le 4 righe «set» del trigger vero (_i, _r, _nuova, _valida), poi l'esito."""
    righe = _trigger(id_)["value_template"].split("\n")
    assert [r.split("=")[0] for r in righe[:4]] == ["{%- set _i ", "{%- set _r ", "{%- set _nuova ", "{%- set _valida "]
    return "\n".join(righe[:4]) + "{{ _nuova }}|{{ _valida }}"


def _rendi_versione(hass: HomeAssistant, modello: Template, installata: str, repository: str) -> tuple[bool, bool]:
    hass.states.async_set("sensor.vmc_master_versione_corrente", installata)
    hass.states.async_set("sensor.vmc_master_versione_repository", repository)
    nuova, valida = modello.async_render(parse_result=False).strip().split("|")
    return nuova == "True", valida == "True"


async def test_confronto_di_versione_reso_con_home_assistant(hass: HomeAssistant) -> None:
    """B3-4: con un numero diverso di componenti («9.0» contro «9.0.0») due versioni uguali non sono più «nuove»;
    nel formato x.y.z[bN] del progetto l'esito resta quello della b33."""
    for id_ in ("Repository Update ON", "Repository Update OFF"):
        nuovo = Template(_modello_versione(id_), hass)
        vecchio = Template(_modello_versione(id_).replace(VERSIONE_NUOVA.format(x="r"), VERSIONE_B33.format(x="r"))
                           .replace(VERSIONE_NUOVA.format(x="i"), VERSIONE_B33.format(x="i")), hass)
        sbagliate_b33 = 0
        for installata, repository, attesa in COPPIE_VERSIONI:
            assert _rendi_versione(hass, nuovo, installata, repository) == (attesa, True), (installata, repository)
            sbagliate_b33 += _rendi_versione(hass, vecchio, installata, repository)[0] != attesa
        assert sbagliate_b33 == 5
        for installata, repository in VERSIONI_NON_VALIDE:
            assert _rendi_versione(hass, nuovo, installata, repository) == (False, False), (installata, repository)
        # formato del progetto: stesso esito della b33 su tutte le coppie
        versioni = [f"{a}.{b}.{c}{s}" for a in (0, 9, 10) for b in (0, 1) for c in (0, 9) for s in ("", "b1", "b10")]
        for installata in versioni:
            for repository in versioni:
                assert _rendi_versione(hass, nuovo, installata, repository) == _rendi_versione(
                    hass, vecchio, installata, repository), (installata, repository)


async def test_trigger_aggiornamento_resi_interi(hass: HomeAssistant) -> None:
    """B3-4: i trigger interi ON e OFF, resi con le altre condizioni vere, seguono il confronto di versione."""
    for entita, stato in {
        "input_boolean.vmc_master_popup_versione_corrente_vs_repository": "off",
        "sensor.vmc_master_status_ip_interfaccia": "ON-Line",
        "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia": "Velocità 1",
        **{f"input_boolean.vmc_master_spia_velocita_{v}": "off"
           for v in ("0", "1", "2", "3", "4", "notturna", "freecooling", "iperventilazione")},
    }.items():
        hass.states.async_set(entita, stato)
    acceso = Template(_trigger("Repository Update ON")["value_template"], hass)
    spento = Template(_trigger("Repository Update OFF")["value_template"], hass)
    for installata, repository, attesa in (("9.0.0", "9.0", False), ("9.0.0b33", "9.0.0b34", True), ("9.1", "9.0.9", False)):
        hass.states.async_set("sensor.vmc_master_versione_corrente", installata)
        hass.states.async_set("sensor.vmc_master_versione_repository", repository)
        assert acceso.async_render() is attesa, (installata, repository)
        assert spento.async_render() is (not attesa), (installata, repository)


# ------------------------------------------------------------------------------------------------ B3-5
def test_trigger_errore_umidita_esterna_come_gli_altri() -> None:
    """B3-5: tutti i 10 trigger di errore delle entità usano «…_selezionata == '-100'»; copia della guardia uguale."""
    errori = [t for t in _automazione()["triggers"] if re.fullmatch(r"Entità .+ Errore \[(Mobile|Interfaccia)\]", str(t.get("id")))]
    assert len(errori) == 10
    for t in errori:
        prima = _norm(t["value_template"]).removeprefix("{{ ").split(" and ")[0]
        assert re.fullmatch(r"states\('sensor\.vmc_master_[a-z0-9_]+_selezionata'\) == '-100'", prima), t["id"]
        assert "for" not in t
        assert _norm(_copia_guardia(t["id"])) == _norm(t["value_template"]), t["id"]
    automazione = _testo("vmc_master_automazione.txt")
    assert "umidita_esterna_status') in [" not in automazione
    assert automazione.count("states('sensor.vmc_master_umidita_esterna_selezionata') == '-100'") == 4


async def test_umidita_esterna_selezionata_vale_meno_100_se_non_disponibile(hass: HomeAssistant) -> None:
    """B3-5: il sensore «Umidità Ext. Selezionata» vale -100 quando l'entità scelta non dà un valore (l'umidità esterna
    non ha una sonda nella VMC, Foglio A2): è proprio il caso che il trigger deve segnalare."""
    sensori = [s for blocco in hay.load_yaml(str(PKG / "vmc_master.yaml"))["template"] for s in blocco.get("sensor", [])
               if s.get("default_entity_id") == "sensor.vmc_master_umidita_esterna_selezionata"]
    assert len(sensori) == 1
    stato = Template(sensori[0]["state"], hass)
    scelta = "input_select.vmc_master_selected_humidity_external_entity"
    casi = [
        ({scelta: "sensor.prova_umidita", "sensor.prova_umidita": "unavailable"}, "-100"),
        ({scelta: "sensor.prova_umidita", "sensor.prova_umidita": "unknown"}, "-100"),
        ({scelta: "sensor.prova_assente"}, "-100"),
        ({scelta: "weather.prova", "weather.prova": "unavailable"}, "-100"),
        ({scelta: "Aggiorna Elenco Entità"}, "-100"),
        ({scelta: "sensor.prova_umidita", "sensor.prova_umidita": "55.5"}, "55.5"),
    ]
    for stati, atteso in casi:
        for entita, valore in stati.items():
            hass.states.async_set(entita, valore)
        assert stato.async_render(parse_result=False).strip() == atteso, stati


# ------------------------------------------------------------------------------------------------ B4-1
def test_agg_sensori_avviato_senza_bloccare_l_automazione() -> None:
    """B4-1: il ramo pannello_avvisi_problema avvia «Agg. Sensori» con script.turn_on; le sole chiamate dirette
    (bloccanti) rimaste nell'automazione sono quelle agli script del Calendario."""
    passi = _ramo("pannello_avvisi_problema")["sequence"]
    assert len(passi) == 1
    assert passi[0]["action"] == "script.turn_on"
    assert passi[0]["target"]["entity_id"] == "script.vmc_master_upgrade_sensors"
    dirette: Counter = Counter()

    def visita(nodo: dict) -> None:
        azione = nodo.get("action")
        if isinstance(azione, str) and azione.startswith("script.") and azione not in (
                "script.turn_on", "script.turn_off", "script.toggle", "script.reload"):
            dirette[azione] += 1

    _cammina(_automazione()["actions"], visita)
    assert set(dirette) == SCRIPT_DEL_CALENDARIO
    assert sum(dirette.values()) == 32
    assert hay.load_yaml(str(PKG / "vmc_master.yaml"))["script"]["vmc_master_upgrade_sensors"]["mode"] == "restart"


# ------------------------------------------------------------------------------------------------ B4-4
def _passi_umidita_velocita_0() -> list[dict]:
    return _ramo("umidita_velocita_0")["sequence"]


def test_umidita_velocita_0_lettura_appena_tornata_struttura() -> None:
    """B4-4: prima dell'if una condizione ferma il ramo quando lo stato precedente non è valido; l'if e l'altrimenti
    restano come prima (senza la vecchia esclusione nell'if)."""
    assert _trigger("umidita_velocita_0")["trigger"] == "template"
    porta, scelta = _passi_umidita_velocita_0()
    assert porta["condition"] == "template" and "(B4-4)" in porta["alias"]
    assert all(f"'{s}'" in porta["value_template"] for s in STATI_NON_VALIDI)
    condizione = scelta["if"][0]["value_template"]
    assert "from_state" not in condizione
    assert condizione == (
        "{{ is_state('input_boolean.vmc_master_spia_umidita_velocita_0', 'on') and "
        "is_state('input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0', 'off') and "
        "states('input_select.vmc_master_speed_umidita') != 'Velocità 0' }}"
    )
    assert scelta["then"][0]["action"] == "input_boolean.turn_off"
    assert scelta["else"][0]["target"]["entity_id"] == [
        "input_boolean.vmc_master_spia_umidita_velocita_0", "input_boolean.vmc_master_spia_umidita_mantenuta_velocita_0"]


@pytest.mark.parametrize(
    ("precedente", "prosegue"),
    [
        # stato precedente valido: l'utente preme 0, una spia si spegne, la fase del riavvio passa a 4
        ("Velocità 2", True), ("Free Cooling", True), ("on", True), ("Nessuna Allerta", True), ("3.0", True),
        # VMC di nuovo leggibile: nessuna memoria cambiata
        *[(s, False) for s in STATI_NON_VALIDI],
    ],
)
async def test_umidita_velocita_0_lettura_appena_tornata_resa(hass: HomeAssistant, precedente: str, prosegue: bool) -> None:
    porta = Template(_passi_umidita_velocita_0()[0]["value_template"], hass)
    trigger = {"platform": "template", "from_state": State("sensor.prova", precedente),
               "to_state": State("sensor.prova", "Velocità 0")}
    assert porta.async_render({"trigger": trigger}) is prosegue


async def test_umidita_velocita_0_senza_stato_precedente(hass: HomeAssistant) -> None:
    """B4-4: senza stato precedente (aggiornamento a tempo del template) il ramo prosegue come prima."""
    porta = Template(_passi_umidita_velocita_0()[0]["value_template"], hass)
    assert porta.async_render({"trigger": {"platform": "template", "from_state": None, "to_state": None}}) is True
    assert porta.async_render({"trigger": {"platform": "template"}}) is True
