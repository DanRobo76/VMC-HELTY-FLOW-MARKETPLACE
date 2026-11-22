"""Prove della b36, fetta «grafici»: sensori «_grafico» della CO₂ «Unavailable» dopo le prove di Black-Out.

Segnalazione: sensor.vmc_master_co2_status_grafico e sensor.vmc_master_co2_status_senza_offset_grafico «Unavailable»
con sensor.vmc_master_co2_status e sensor.vmc_master_co2_status_senza_offset a «-». Causa: la VMC non ha la sonda
CO₂/VOC (campi 4 e 11 della risposta VMGI sempre 00000), quindi i 4 grafici di CO₂ e VOC non sono disponibili apposta.

- Voluto (passa prima e dopo): «-» viene dall'ultima lettura valida dei Sensori Ambientali (VMGI?) con la CO₂ ≤ 0;
  il «_grafico» non e' disponibile quando la sorgente non e' un numero (buco nel grafico e non 0). Durante il Black-Out
  i sensori restano sull'ultima lettura valida (nessun buco); dopo il ritorno della corrente la prima lettura arriva
  con la lettura programmata (scan_interval 1227 s) o con Agg. Sensori e, se la VMC indica la CO₂ a 0, «-» resta fino
  alla lettura successiva. Nessuna entita' «_grafico» e' nascosta dal Package o dall'integrazione.
- Errore corretto (fallisce prima, passa dopo): con un Offset CO₂ o VOC positivo una lettura della VMC ≤ 0 («-» del
  sensore senza Offset, sonda assente) diventava il valore dell'Offset (per esempio 50 ppm), il grafico mostrava una
  linea finta invece del buco e con un Offset oltre le soglie (CO₂ > 800 ppm, VOC > 300 ppb) partiva un'allerta
  Inquinanti finta. Ora resta «-» anche con l'Offset (un Offset negativo dava gia' «-»). Temperature e umidita' non
  hanno lo stesso schema: 0 °C e' un valore vero e l'umidita' della VMC a 0 e' gia' «[Non Calcolabile]».

Rese con il motore di Home Assistant: i blocchi template veri del Package (sensore memorizzato a trigger, sensori CO₂ e
VOC, sensori «_grafico») caricati con l'integrazione template."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.setup import async_setup_component
from homeassistant.util import yaml as hay

RADICE = Path(__file__).resolve().parents[1]
PKG = RADICE / "custom_components" / "vmc_master" / "package"
SENSORI = "sensor.vmc_master_sensori"
MEMORIZZATA = "sensor.vmc_master_sensori_memorizzata"
SCELTA_CO2 = "input_select.vmc_master_selected_co2_internal_entity"
CO2 = "sensor.vmc_master_co2_status"
CO2_SO = "sensor.vmc_master_co2_status_senza_offset"
VOC = "sensor.vmc_master_voc_status"
VOC_SO = "sensor.vmc_master_voc_status_senza_offset"
GRAFICI_INQUINANTI = [f"{e}_grafico" for e in (CO2, CO2_SO, VOC, VOC_SO)]
UMIDITA_SO = "sensor.vmc_master_umidita_interna_status_senza_offset"
ALLERTE = ["sensor.vmc_master_co2_status_verifica_soglia", "sensor.vmc_master_voc_status_verifica_soglia",
           "sensor.vmc_master_alert_monitoraggio_co2", "sensor.vmc_master_alert_monitoraggio_voc"]
ENTITA = ["sensor.vmc_master_co2_interna_selezionata", CO2, CO2_SO, VOC, VOC_SO,
          "sensor.vmc_master_temp_interna_positivo_negativo", "sensor.vmc_master_temp_interna_status_senza_offset",
          UMIDITA_SO, *ALLERTE]


def _testo(nome: str) -> str:
    return (PKG / nome).read_text(encoding="utf-8").replace("\r\n", "\n")


def _piatto(testo: str) -> str:
    return " ".join(testo.split())


def _vmgi(co2: int = 600, voc: int = 50, ti: int = 210, te: int = 100, rh: int = 500) -> str:
    return (f"VMGI,{ti:05d},{te:05d},{rh:05d},{co2:05d},00000,00000,00000,00000,00000,00000,{voc:05d},"
            "00000,00000,00000")


def _blocchi() -> list[dict[str, Any]]:
    """Blocchi template del Package: il sensore memorizzato (trigger), i sensori di ENTITA e tutti i «_grafico»."""
    pacchetto = hay.load_yaml(str(PKG / "vmc_master.yaml"))
    blocchi = []
    for blocco in pacchetto["template"]:
        sensori = blocco.get("sensor", []) or []
        ids = [s.get("default_entity_id") for s in sensori]
        if MEMORIZZATA in ids:
            blocchi.append({"triggers": blocco["triggers"], "sensor": [s for s in sensori
                                                                       if s["default_entity_id"] == MEMORIZZATA]})
        elif any(i in ENTITA or str(i).endswith("_grafico") for i in ids):
            blocchi.append({"sensor": sensori})
    return blocchi


async def _avvia(hass: HomeAssistant, offset_co2: float = 0, offset_voc: float = 0) -> None:
    hass.states.async_set(SCELTA_CO2, CO2_SO)          # CO₂ dalla sonda della VMC (voce del Package)
    for nome, valore in (("co2", offset_co2), ("voc", offset_voc)):
        hass.states.async_set(f"input_number.vmc_master_offset_{nome}", str(valore))
    assert await async_setup_component(hass, "template", {"template": _blocchi()})
    await hass.async_block_till_done()


async def _lettura(hass: HomeAssistant, valore: str) -> None:
    hass.states.async_set(SENSORI, valore)
    await hass.async_block_till_done()


def _stati(hass: HomeAssistant, *entita: str) -> list[str]:
    return [hass.states.get(e).state for e in entita]


# ------------------------------------------------------------------------------------- errore corretto: Offset
async def test_lettura_a_zero_resta_trattino_con_offset_positivo(hass: HomeAssistant) -> None:
    """Offset CO₂ +50 e VOC +20: una lettura della VMC con CO₂ e VOC a 0 mostra «-» (non 50 e 20) e i 4 grafici di
    CO₂ e VOC non sono disponibili (buco, non una linea a 50 o 20). Con una lettura valida l'Offset si somma."""
    await _avvia(hass, offset_co2=50, offset_voc=20)
    await _lettura(hass, _vmgi(co2=600, voc=50))
    assert _stati(hass, CO2, CO2_SO, VOC, VOC_SO) == ["650", "600", "70", "50"]
    assert _stati(hass, *GRAFICI_INQUINANTI) == ["650", "600", "70", "50"]
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, CO2, CO2_SO, VOC, VOC_SO) == ["-", "-", "-", "-"]
    assert _stati(hass, *GRAFICI_INQUINANTI) == ["unavailable"] * 4


async def test_offset_negativo_e_sonda_scelta_non_disponibile(hass: HomeAssistant) -> None:
    """Invariati: un Offset negativo che porta il valore a ≤ 0 da' «-»; con l'entita' scelta non disponibile si usa
    la sonda della VMC senza Offset (CO₂ a 0 -> «-»)."""
    await _avvia(hass, offset_co2=-700, offset_voc=-60)
    await _lettura(hass, _vmgi(co2=600, voc=50))
    assert _stati(hass, CO2, VOC) == ["-", "-"]
    hass.states.async_set("input_number.vmc_master_offset_co2", "-100")
    hass.states.async_set("input_number.vmc_master_offset_voc", "-10")
    await _lettura(hass, _vmgi(co2=601, voc=51))
    assert _stati(hass, CO2, VOC) == ["501", "41"]
    hass.states.async_set(SCELTA_CO2, "sensor.non_esiste")
    await hass.async_block_till_done()
    assert _stati(hass, CO2) == ["601"]
    await _lettura(hass, _vmgi(co2=0, voc=51))
    assert _stati(hass, CO2, f"{CO2}_grafico") == ["-", "unavailable"]


async def test_vmc_senza_sonda_co2_voc(hass: HomeAssistant) -> None:
    """VMC senza sonda CO₂/VOC (campi 4 e 11 sempre 00000), la causa della segnalazione. Offset 0: CO₂ e VOC «-», i 4
    grafici di CO₂ e VOC «unavailable» (voluto), livelli «-» e nessuna allerta. Offset +900 ppm e +400 ppb: prima
    dava 900 e 400, «Moderata Concentrazione» e due allerte Inquinanti finte; ora resta tutto «-» e «Nessuna
    Allerta». Offset negativi: «-» come prima."""
    await _avvia(hass)
    await _lettura(hass, _vmgi(co2=0, voc=0))
    assert _stati(hass, CO2, CO2_SO, VOC, VOC_SO) == ["-", "-", "-", "-"]
    assert _stati(hass, *GRAFICI_INQUINANTI) == ["unavailable"] * 4
    assert _stati(hass, *ALLERTE) == ["-", "-", "Nessuna Allerta", "Nessuna Allerta"]
    for co2, voc in ((50, 20), (900, 400), (-50, -20)):
        hass.states.async_set("input_number.vmc_master_offset_co2", str(co2))
        hass.states.async_set("input_number.vmc_master_offset_voc", str(voc))
        await hass.async_block_till_done()
        assert _stati(hass, CO2, VOC, *GRAFICI_INQUINANTI) == ["-", "-"] + ["unavailable"] * 4, (co2, voc)
        assert _stati(hass, *ALLERTE) == ["-", "-", "Nessuna Allerta", "Nessuna Allerta"], (co2, voc)


# ------------------------------------------------------------------------------- voluto: Black-Out e lettura a 0
async def test_black_out_ultima_lettura_e_co2_a_zero_dopo_il_ritorno(hass: HomeAssistant) -> None:
    """Lo scenario della segnalazione. Prima: valori e grafici numerici. Durante il Black-Out la lettura fallisce
    (sensore TCP «unavailable»): il sensore memorizzato tiene l'ultima lettura valida, CO₂ e grafici restano a 600
    (nessun buco). Dopo il ritorno, una lettura con la CO₂ a 0: CO₂ con e senza Offset «-» e i loro grafici
    «unavailable» (lo screenshot), mentre VOC, temperatura e umidita' della stessa lettura restano numeri. La lettura
    successiva valida riporta tutto."""
    await _avvia(hass)
    await _lettura(hass, _vmgi())
    grafici_co2 = [f"{CO2}_grafico", f"{CO2_SO}_grafico"]
    assert _stati(hass, CO2, CO2_SO, *grafici_co2) == ["600", "600", "600", "600"]
    await _lettura(hass, "unavailable")
    assert hass.states.get(MEMORIZZATA).state == _vmgi()
    assert _stati(hass, CO2, CO2_SO, *grafici_co2) == ["600", "600", "600", "600"]
    await _lettura(hass, _vmgi(co2=0))
    assert _stati(hass, CO2, CO2_SO, *grafici_co2) == ["-", "-", "unavailable", "unavailable"]
    assert _stati(hass, f"{VOC}_grafico", "sensor.vmc_master_temp_interna_status_senza_offset_grafico",
                  f"{UMIDITA_SO}_grafico") == ["50", "21.0", "50.0"]
    await _lettura(hass, _vmgi())
    assert _stati(hass, CO2, CO2_SO, *grafici_co2) == ["600", "600", "600", "600"]


async def test_grafici_non_nascosti(hass: HomeAssistant) -> None:
    """I 16 sensori «_grafico» entrano nel registro senza hidden_by: il Package e l'integrazione non li nascondono
    (nessun hidden / hidden_by nei file del Package e nel codice dell'integrazione)."""
    await _avvia(hass)
    registro = er.async_get(hass)
    grafici = [v for v in registro.entities.values() if v.entity_id.endswith("_grafico")]
    assert len(grafici) == 16
    assert {v.hidden_by for v in grafici} == {None}
    assert {v.disabled_by for v in grafici} == {None}
    for file in [*PKG.glob("vmc_master*"), *(RADICE / "custom_components" / "vmc_master").glob("*.py")]:
        assert not re.search(r"hidden|visible_default", file.read_text(encoding="utf-8")), file.name


def test_nessuna_rilettura_dei_sensori_ambientali_dopo_il_black_out() -> None:
    """sensor.vmc_master_sensori si rilegge solo con lo scan_interval (1227 s) e con Agg. Sensori (lo script
    lanciato anche dal ramo «Pannello Avvisi con Problemi»): l'automazione non lo rilegge al ritorno della corrente."""
    pacchetto = _testo("vmc_master.yaml")
    assert re.search(r"payload: \"VMGI\?\"[^\n]*\n\s+scan_interval:\s*\n\s+seconds: 1227\b", pacchetto)
    assert "sensor.vmc_master_sensori\n" not in _testo("vmc_master_automazione.txt")
    script = hay.load_yaml(str(PKG / "vmc_master.yaml"))["script"]
    con_rilettura = sorted(nome for nome, corpo in script.items() if any(
        passo.get("action") == "homeassistant.update_entity"
        and SENSORI in passo.get("target", {}).get("entity_id", []) for passo in corpo["sequence"]))
    assert con_rilettura == ["vmc_master_upgrade_sensors"]


def test_testi_aggiornati() -> None:
    """Nota Grafici dei Sensori della scheda: VMC senza sonda CO₂/VOC (sensori senza Offset a «-», due grafici vuoti)
    e Black-Out (ultima lettura valida, prima lettura dopo il ritorno entro 1227 s o con Agg. Sensori). Dalla b37
    l'Offset si somma sempre al valore letto: la frase della b36 «resta «-» anche con l'Offset» non c'è più nel
    Package (i testi nuovi delle voci 10 e 11 e della Nota sono in tests/test_b37_testi.py)."""
    scheda = _piatto(_testo("vmc_master_scheda_manuale_interfaccia.txt"))
    assert ("Sulle VMC senza sonda CO₂/VOC la risposta Sensori Ambientali ha la CO₂ e i VOC a 00000. CO₂ e VOC della "
            "scheda «Sensori VMC Interni» (senza Offset) restano sempre «-» e i loro due grafici sono vuoti: in Home "
            "Assistant questi sensori «_grafico» risultano non disponibili. Non è un guasto.") in scheda
    assert ("Durante un Black-Out (VMC OFF-Line) i sensori della VMC e i loro grafici restano sull'ultima lettura "
            "valida, senza buchi.") in scheda
    assert ("la prima lettura dei Sensori Ambientali arriva con la lettura programmata (ogni 1227 secondi, cioè "
            "entro circa 20 minuti) oppure subito con «Agg. Sensori»") in scheda
    for nome in ("vmc_master.yaml", "vmc_master_scheda_manuale_interfaccia.txt", "vmc_master_automazione.txt"):
        testo = _piatto(_testo(nome))
        for vecchia in ("resta «-» anche con l'Offset", "anche con un Offset", "un valore letto ≤ 0"):
            assert vecchia not in testo, (nome, vecchia)
