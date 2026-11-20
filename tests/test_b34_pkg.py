"""Prove della 9.0.0b34 (fetta «pkg»): rilievi della verifica profonda b33 B2-1, B2-2, B2-3, B5-1, B5-2, B5-3, B5-4.

Prove statiche sul testo e sulla struttura YAML, rese dei template con il motore di Home Assistant e, per la scheda JS,
la scheda vera caricata in node (saltata se node non c'e')."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path

import pytest
from homeassistant.helpers.template import Template
from homeassistant.util import yaml as hay

RADICE = Path(__file__).resolve().parents[1] / "custom_components" / "vmc_master"
PKG = RADICE / "package"
JS = RADICE / "frontend" / "vmc-master-card.js"
SCRIPT_ELENCO = ("temperatura_esterna", "temperatura_interna", "umidita_esterna", "umidita_interna", "co2_interna",
                 "notifica_dispositivo", "media_player")
STATI_SOSTITUZIONE = "['unknown', 'unavailable', '-100', 'Non disponibile']"


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _pacchetto() -> dict:
    return hay.load_yaml(str(PKG / "vmc_master.yaml"))


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


# ------------------------------------------------------------------------------------------------------------ B2-1
def _rami_aggiorna_elenco(nome: str) -> tuple[list, str]:
    script = _pacchetto()["script"][f"vmc_master_aggiorna_elenco_entita_{nome}"]
    scelte = [passo["choose"] for passo in script["sequence"] if "choose" in passo]
    assert len(scelte) == 1, nome
    non_valida, valida = scelte[0]
    return non_valida["sequence"], valida["conditions"][0]["value_template"]


@pytest.mark.parametrize("nome", SCRIPT_ELENCO)
def test_aggiorna_elenco_non_scrive_la_voce_aggiorna_in_last(nome: str) -> None:
    """B2-1: nel ramo «selezionata non valida» input_text.vmc_master_last_* si scrive solo dentro un if con la stessa
    condizione del ramo «valida» (un'entita' vera): mai «Aggiorna Elenco…»."""
    passi, condizione_valida = _rami_aggiorna_elenco(nome)
    assert not [p for p in passi if p.get("action") == "input_text.set_value"], nome
    se = [p for p in passi if "if" in p and any(t.get("action") == "input_text.set_value" for t in p.get("then", []))]
    assert len(se) == 1, nome
    assert se[0]["if"] == [{"condition": "template", "value_template": condizione_valida}], nome
    assert "Aggiorna Elenco" in condizione_valida and "in valid_options and" in condizione_valida, nome
    scrittura = se[0]["then"]
    assert len(scrittura) == 1 and scrittura[0]["target"]["entity_id"].startswith("input_text.vmc_master_last_"), nome
    # l'ultimo passo del ramo resta la scrittura condizionata (dopo il ripristino e la notifica)
    assert passi[-1] is se[0], nome


async def test_aggiorna_elenco_condizione_della_scrittura(hass) -> None:
    """B2-1: la condizione della scrittura di last_* e' vera solo per un'entita' presente nell'elenco."""
    passi, _ = _rami_aggiorna_elenco("temperatura_esterna")
    condizione = next(p for p in passi if "if" in p and "then" in p and "last_temp" in str(p["then"]))["if"][0]
    selezione = "input_select.vmc_master_selected_temp_external_entity"
    voce = "Aggiorna Elenco Entità Temperatura Esterna"
    opzioni = [voce, "sensor.prova_temperatura", "weather.casa"]
    for stato, atteso in ((voce, False), ("weather.casa", True), ("sensor.prova_temperatura", True), ("unknown", False),
                          ("", False), ("weather.altra", False)):
        hass.states.async_set(selezione, stato, {"options": opzioni})
        assert Template(condizione["value_template"], hass).async_render() is atteso, stato


def test_aggiorna_elenco_notifica_invariata() -> None:
    """B2-1: la notifica «Aggiornare Manualmente…» e il ripristino dell'ultima scelta restano com'erano."""
    testo = _testo("vmc_master.yaml")
    assert testo.count("message: \"Aggiornare Manualmente l'Entità") == 6  # 6 script su 7: il Media Player non notifica
    for nome in SCRIPT_ELENCO:
        passi, _ = _rami_aggiorna_elenco(nome)
        assert len(passi) == 3 and "choose" in passi[0] and "choose" in passi[1], nome
        ripristino = passi[0]["choose"][0]["sequence"][0]
        assert ripristino["action"] == "input_select.select_option", nome
        assert "input_text.vmc_master_last_" in ripristino["data"]["option"], nome


# ------------------------------------------------------------------------------------------------------------ B2-2
def _stato_sensore(entita: str) -> str:
    for blocco in _pacchetto()["template"]:
        for sensore in blocco.get("sensor", []) or []:
            if sensore.get("default_entity_id") == entita:
                return str(sensore["state"])
    raise AssertionError(entita)


def _tempo_atteso(portata: int, volume: float) -> str:
    """Testo visibile della b33 (a capo e spazi ripetuti tolti)."""
    secondi_totali = round((volume / portata) * 3600)
    ore, minuti, secondi = secondi_totali // 3600, (secondi_totali % 3600) // 60, secondi_totali % 60

    def parola(n: int, uno: str, piu: str) -> str:
        return f"{n} {uno if n == 1 else piu}"

    if ore > 0:
        testo = parola(ore, "ora", "ore") + (", " if minuti or secondi else "")
        testo += parola(minuti, "minuto", "minuti") if minuti else ""
        testo += " e " if secondi and minuti else ""
        return testo + (parola(secondi, "secondo", "secondi") if secondi else "")
    if minuti > 0:
        return parola(minuti, "minuto", "minuti") + (" e " + parola(secondi, "secondo", "secondi") if secondi else "")
    return parola(secondi, "secondo", "secondi")


async def test_tempo_ricambio_aria_su_una_riga(hass) -> None:
    """B2-2: su tutte le 10.000 combinazioni (5 portate x volumi da 0,5 a 1000 a passi di 0,5) lo stato e' su una
    riga, senza spazi doppi, con il testo visibile di prima (es. «2 ore, 49 secondi» per 37 m3/h e 74,5 m3)."""
    modello = Template(_stato_sensore("sensor.vmc_master_status_calcolo_portata_ventola"), hass)
    diversi = []
    for portata in (10, 17, 26, 37, 42):
        hass.states.async_set("sensor.vmc_master_status_portata_ventola_lettura_codice_interpretato", str(portata))
        for passo in range(1, 2001):
            volume = passo * 0.5
            hass.states.async_set("input_number.vmc_master_volume_da_inserire", str(volume))
            stato = modello.async_render(parse_result=False)
            if stato != _tempo_atteso(portata, volume) or "\n" in stato or "  " in stato:
                diversi.append((portata, volume, stato))
    assert not diversi, diversi[:5]
    for portata, volume, atteso in (("37", "74.5", "2 ore, 49 secondi"), ("17", "100.0", "5 ore, 52 minuti e 56 secondi"),
                                    ("10", "0.0", "-"), ("Non disponibile", "50.0", "Non disponibile")):
        hass.states.async_set("sensor.vmc_master_status_portata_ventola_lettura_codice_interpretato", portata)
        hass.states.async_set("input_number.vmc_master_volume_da_inserire", volume)
        assert modello.async_render(parse_result=False) == atteso


# ------------------------------------------------------------------------------------------------------------ B2-3
async def test_aria_scambiata_senza_il_confronto_morto(hass) -> None:
    """B2-3: niente confronto con '1 secondi' (il sensore scrive «1 secondo»); resta '0 secondi', comportamento
    invariato: con «1 secondo» il ricambio continua e lo chiude il ramo successivo."""
    testo = _testo("vmc_master.yaml")
    assert "'1 secondi'" not in testo
    condizioni = []

    def cerca(nodo: object) -> Iterator[str]:
        if isinstance(nodo, dict):
            for chiave, valore in nodo.items():
                if chiave == "value_template" and isinstance(valore, str) and "tempo_mancante in" in valore:
                    yield valore
                else:
                    yield from cerca(valore)
        elif isinstance(nodo, list):
            for valore in nodo:
                yield from cerca(valore)

    condizioni = list(cerca(_pacchetto()["automation"]))
    assert len(condizioni) == 1
    assert "tempo_mancante in ['0 secondi'] and" in condizioni[0]
    for tempo, ricomincio, atteso in (("0 secondi", 1.0, True), ("1 secondo", 1.0, False), ("0 secondi", 0.0, False)):
        valore = Template(condizioni[0], hass).async_render({"tempo_mancante": tempo, "ricomincio_val": ricomincio})
        assert valore is atteso, tempo


# ------------------------------------------------------------------------------------------------------------ B5-1
PROVA_NODE = r"""
const classi = {};
globalThis.window = globalThis;
globalThis.HTMLElement = class extends EventTarget {};
globalThis.customElements = { get: (n) => classi[n], define: (n, c) => { classi[n] = c; } };
const [versioneJs, casi] = [process.argv[2], JSON.parse(process.argv[3])];
const url = new URL("./scheda.mjs", import.meta.url);
url.searchParams.set("v", versioneJs);
await import(url.href);
const Scheda = classi["vmc-master-card"];
console.warn = () => {};
const esiti = casi.map((stati) => {
  window.__vmcMasterAvvisoVersione = undefined;
  const scheda = new Scheda();
  const avvisi = [];
  scheda.addEventListener("hass-notification", (evento) => avvisi.push(evento.detail.message));
  scheda._hass = { states: Object.fromEntries(Object.entries(stati).map(([id, stato]) => [id, { state: stato }])) };
  scheda._avvisaVersioneVecchia();
  return avvisi;
});
console.log(JSON.stringify(esiti));
"""


def _avvisi_js(tmp_path: Path, versione_js: str, casi: list[dict[str, str]]) -> list[list[str]]:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node non installato")
    shutil.copyfile(JS, tmp_path / "scheda.mjs")
    (tmp_path / "prova.mjs").write_text(PROVA_NODE, encoding="utf-8")
    uscita = subprocess.run([node, str(tmp_path / "prova.mjs"), versione_js, json.dumps(casi)],
                            capture_output=True, text=True, check=True, timeout=60)
    return json.loads(uscita.stdout)


def test_avviso_versione_testo_del_js() -> None:
    """B5-1: la scheda JS usa la versione piu' alta tra tutti i sensori e avvisa solo se e' piu' nuova."""
    testo = JS.read_text(encoding="utf-8")
    corpo = testo[testo.index("  _avvisaVersioneVecchia() {"):testo.index("  _clicInformazioni(evento) {")]
    assert "const installata = versionePiuAlta(stati);" in corpo
    assert "confrontaVersioni(installata, VERSIONE_JS) <= 0" in corpo
    assert ".find(" not in corpo and "installata === VERSIONE_JS" not in corpo
    assert "ricaricare la pagina" in corpo


COPPIE_VERSIONI = [  # (versione dell'integrazione, versione del JS, l'integrazione e' piu' nuova?)
    ("9.0.0b34", "9.0.0", False), ("9.0.0", "9.0.0b34", True), ("9.0.0b10", "9.0.0b9", True),
    ("9.0.0b9", "9.0.0b10", False), ("9.0.0b33", "9.0.0b33", False), ("9.0", "9.0.0", False), ("9.0.0", "9.0", False),
    ("9.0.1", "9.0.0", True), ("9.0.10", "9.0.9", True), ("10.0.0", "9.9.9", True), ("9.1.0b1", "9.0.9", True),
    ("8.6.0", "9.0.0b1", False), ("9.0.0.1", "9.0.0", True), ("9.0.0b34", "9.0.0b33", True), ("9.0.0b1", "9.0.0b01", False),
]


def test_avviso_versione_confronto(tmp_path: Path) -> None:
    """B5-1: confronto x.y.z[bN] della scheda vera: avviso solo con l'integrazione piu' nuova del JS (15 coppie)."""
    per_js: dict[str, list[tuple[str, bool]]] = {}
    for installata, versione_js, piu_nuova in COPPIE_VERSIONI:
        per_js.setdefault(versione_js, []).append((installata, piu_nuova))
    for versione_js, coppie in per_js.items():
        avvisi = _avvisi_js(tmp_path, versione_js, [{"sensor.vmc_master_versione_corrente": f"v.{v}"} for v, _ in coppie])
        for (installata, piu_nuova), ricevuti in zip(coppie, avvisi, strict=True):
            atteso = [f"VMC Master aggiornata a {installata}: ricaricare la pagina"] if piu_nuova else []
            assert ricevuti == atteso, (installata, versione_js)


def test_avviso_versione_piu_vmc(tmp_path: Path) -> None:
    """B5-1: con piu' VMC conta la versione piu' alta (una VMC disabilitata resta indietro); i valori non validi non
    contano; nessun avviso se l'integrazione e' piu' vecchia della pagina (secondo riavvio richiesto)."""
    casi = [
        {"sensor.vmc_prova_versione_corrente": "v.9.0.0b33", "sensor.vmc_master_versione_corrente": "v.9.0.0b34"},
        {"sensor.vmc_prova_versione_corrente": "v.9.0.0b33", "sensor.vmc_master_versione_corrente": "v.9.0.0b33"},
        {"sensor.vmc_prova_versione_corrente": "unavailable", "sensor.vmc_master_versione_corrente": "v.9.0.0b35"},
        {"sensor.vmc_prova_versione_corrente": "v.9.0.0b36", "sensor.vmc_master_versione_corrente": "v.9.0.0b35"},
        {"sensor.vmc_master_versione_repository": "v.9.9.9", "sensor.vmc_master_versione_corrente": "unknown"},
        {},
    ]
    assert _avvisi_js(tmp_path, "9.0.0b34", casi) == [
        [], [], ["VMC Master aggiornata a 9.0.0b35: ricaricare la pagina"],
        ["VMC Master aggiornata a 9.0.0b36: ricaricare la pagina"], [], []]
    # senza versione nell'indirizzo (?v=) nessun avviso
    assert _avvisi_js(tmp_path, "", casi[2:3]) == [[]]


# ------------------------------------------------------------------------------------------------- B5-2, B5-3, B5-4
def _contenuti(nodo: object) -> Iterator[str]:
    if isinstance(nodo, dict):
        for chiave, valore in nodo.items():
            if chiave == "content" and isinstance(valore, str):
                yield valore
            else:
                yield from _contenuti(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            yield from _contenuti(valore)


def _markdown(segno: str) -> str:
    trovati = [c for c in _contenuti(hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))) if segno in c]
    assert len(trovati) == 1, segno
    return trovati[0]


def _titolo(hass, contenuto: str, stati: dict[str, str]) -> str:
    for entita, stato in stati.items():
        hass.states.async_set(entita, stato)
    resa = _piatto(Template(contenuto, hass).async_render(parse_result=False))
    titoli = re.findall(r"<strong> ([^<]*ALLERTA[^<]*)</strong>", resa)
    assert len(titoli) == 1, resa[:300]
    return titoli[0].strip(), resa


CONGELAMENTO = "ALLERTA PROSSIMA AL CONGELAMENTO NELLA SONDA DELLA VMC{{ e_entita }}"
DELTA = "PRIORITA' ALLERTA CONGELAMENTO {{ dove_congelamento }}"


def test_titoli_testo() -> None:
    """B5-2, B5-3: gli 8 titoli «… E NELL'ENTITÀ SELEZIONATA» usano la stessa variabile, calcolata con la stessa
    prova del package (sonda di riserva quando il sensore «…_selezionata» e' unknown, unavailable, -100 o Non
    disponibile)."""
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    assert "NELLA SONDA DELLA VMC E NELL'ENTITÀ SELEZIONATA" not in scheda
    assert scheda.count("NELLA SONDA DELLA VMC{{ e_entita }}") == 8
    congelamento, delta = _markdown(CONGELAMENTO), _markdown(DELTA)
    assert congelamento.count("{{ e_entita }}") == 4 and delta.count("{{ e_entita }}") == 4
    assert f"states('sensor.vmc_master_temperatura_esterna_selezionata') in {STATI_SOSTITUZIONE}" in congelamento
    for sensore in ("esterna", "interna"):
        assert f"states('sensor.vmc_master_temperatura_{sensore}_selezionata') in {STATI_SOSTITUZIONE}" in delta
    # la stessa prova del package (sensori Temperatura Ext. e Int.)
    pacchetto = _testo("vmc_master.yaml")
    assert pacchetto.count(f"{{% set stati = {STATI_SOSTITUZIONE} %}}\n          {{% set temp_ext = states("
                           "'sensor.vmc_master_temperatura_esterna_selezionata') %}\n          {% if temp_ext in stati %}") == 1
    assert "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C]</strong>" in delta


SONDA_E_ENTITA = "NELLA SONDA DELLA VMC E NELL'ENTITÀ SELEZIONATA"
SOLO_SONDA = "NELLA SONDA DELLA VMC (ENTITÀ SCELTA NON DISPONIBILE)"
CONG = {"sensor.vmc_master_status_ip_interfaccia": "ON-Line",
        "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia": "Velocità 0"}


@pytest.mark.parametrize(("soglia", "velocita", "temperatura", "selezionata", "atteso"), [
    ("Si", "Velocità 0", "-19", "-19", "ALLERTA CONGELAMENTO " + SONDA_E_ENTITA),
    ("Si", "Velocità 0", "-19", "-100", "ALLERTA CONGELAMENTO " + SOLO_SONDA),
    ("Si", "Velocità 2", "-19", "unavailable", "ALLERTA CONGELAMENTO " + SOLO_SONDA),
    ("Si", "Velocità 2", "-19", "-19", "ALLERTA CONGELAMENTO " + SONDA_E_ENTITA),
    ("[No ma Prossimo]", "Velocità 2", "-16", "-100", "ALLERTA PROSSIMA AL CONGELAMENTO " + SOLO_SONDA),
    ("[No ma Prossimo]", "Velocità 2", "-16", "-16", "ALLERTA PROSSIMA AL CONGELAMENTO " + SONDA_E_ENTITA),
    ("No", "Velocità 2", "5", "unknown", "NESSUNA ALLERTA CONGELAMENTO " + SOLO_SONDA),
    ("No", "Velocità 2", "5", "5", "NESSUNA ALLERTA CONGELAMENTO " + SONDA_E_ENTITA),
])
async def test_titoli_congelamento(hass, soglia, velocita, temperatura, selezionata, atteso) -> None:
    """B5-3: con l'entita' scelta non disponibile (stesso valore della sonda) il titolo nomina solo la sonda."""
    titolo, _ = _titolo(hass, _markdown(CONGELAMENTO), CONG | {
        "sensor.vmc_master_congelamento_verifica_soglia": soglia,
        "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia": velocita,
        "sensor.vmc_master_temp_esterna_status": temperatura,
        "sensor.vmc_master_temp_esterna_status_senza_offset": temperatura,
        "sensor.vmc_master_temperatura_esterna_selezionata": selezionata,
    })
    assert titolo == atteso


@pytest.mark.parametrize(("entita", "sonda", "selezionata", "dove"), [
    ("-19", "-12", "-19", "NELL'ENTITÀ SELEZIONATA"),
    ("-12", "-19", "-12", "NELLA SONDA DELLA VMC"),
    ("-19", "-19", "-19", SONDA_E_ENTITA),
    ("-19", "-19", "-100", SOLO_SONDA),
])
async def test_delta_priorita_congelamento(hass, entita, sonda, selezionata, dove) -> None:
    """B5-2: Δ Temp. con priorita' Congelamento: dove e' stata raggiunta la soglia, come nella scheda Congelamento."""
    titolo, resa = _titolo(hass, _markdown(DELTA), {
        "sensor.vmc_master_temp_esterna_status": entita,
        "sensor.vmc_master_temp_esterna_status_senza_offset": sonda,
        "sensor.vmc_master_temp_interna_status": "20",
        "sensor.vmc_master_temp_interna_status_senza_offset": "20",
        "sensor.vmc_master_temperatura_esterna_selezionata": selezionata,
        "sensor.vmc_master_temperatura_interna_selezionata": "20",
    })
    assert titolo == "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C]"
    assert re.search(r"PRIORITA' ALLERTA CONGELAMENTO (.*?) Impostazione di Default", resa).group(1) == dove


@pytest.mark.parametrize(("soglia", "velocita", "esterna", "sel_est", "sel_int", "atteso"), [
    ("Si", "Velocità 0", "-5", "-5", "20", "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C] " + SONDA_E_ENTITA),
    ("Si", "Velocità 0", "-5", "-100", "-100", "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C] NELLA SONDA DELLA VMC (ENTITÀ "
     "SCELTE NON DISPONIBILI)"),
    ("Si", "Velocità 2", "-5", "-100", "20", "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C] " + SONDA_E_ENTITA
     + " (ENTITÀ ESTERNA NON DISPONIBILE)"),
    ("Si", "Velocità 2", "-5", "-5", "unavailable", "ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C] " + SONDA_E_ENTITA
     + " (ENTITÀ INTERNA NON DISPONIBILE)"),
    ("[No ma Prossimo]", "Velocità 2", "-1", "-100", "-100", "ALLERTA 20 °C ≤ DIFF. TEMP. (INT-EST) ≤ 23 °C PROSSIMA "
     "NELLA SONDA DELLA VMC (ENTITÀ SCELTE NON DISPONIBILI)"),
    ("No", "Velocità 2", "10", "10", "20", "NESSUNA ALLERTA DIFF. TEMP. (INT-EST) > 23 [°C] " + SONDA_E_ENTITA),
])
async def test_titoli_delta(hass, soglia, velocita, esterna, sel_est, sel_int, atteso) -> None:
    """B5-3: Δ Temp., titoli «… E NELL'ENTITÀ SELEZIONATA» con le entita' scelte non disponibili."""
    titolo, _ = _titolo(hass, _markdown(DELTA), CONG | {
        "sensor.vmc_master_delta_temp_verifica_soglia": soglia,
        "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia": velocita,
        "sensor.vmc_master_temp_esterna_status": esterna,
        "sensor.vmc_master_temp_esterna_status_senza_offset": esterna,
        "sensor.vmc_master_temp_interna_status": "20",
        "sensor.vmc_master_temp_interna_status_senza_offset": "20",
        "sensor.vmc_master_temperatura_esterna_selezionata": sel_est,
        "sensor.vmc_master_temperatura_interna_selezionata": sel_int,
    })
    assert titolo == atteso


def test_commenti_nota_entita_scelte() -> None:
    """B5-4: i commenti del package citano la nota con il nome della scheda."""
    pacchetto, scheda = _testo("vmc_master.yaml"), _testo("vmc_master_scheda_manuale_interfaccia.txt")
    assert "Sensori Scelti" not in pacchetto
    assert pacchetto.count("(vedere Pannello Informazioni, Nota Entità Scelte non Disponibili) -#}") == 4
    assert "<strong>Nota Entità Scelte non Disponibili</strong>" in scheda
