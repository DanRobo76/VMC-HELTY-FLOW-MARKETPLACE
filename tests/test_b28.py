"""Prove della 9.0.0b28: riallineamento ripreso dopo la ricarica delle automazioni,
nessun falso «Non Disponibile» scegliendo «Aggiorna Elenco…», countdown di riattivazione
delle allerte in scheda."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.util import yaml as hay

from custom_components.vmc_master.trasforma import per_vmc

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"
TIMER = "timer.vmc_master_countdown_riattivazione_allerte"
FASE = "input_number.vmc_master_fase_riallineamento_al_riavvio"
SELEZIONE = {
    "temperatura_esterna": "temp_external",
    "temperatura_interna": "temp_internal",
    "umidita_esterna": "humidity_external",
    "umidita_interna": "humidity_internal",
    "co2_interna": "co2_internal",
}


def _norm(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


# ------------------------------------------------ riallineamento dopo automation.reload
def _riallineamento(hass: HomeAssistant, nome: str, fase: str | None, in_corso: int | None) -> str:
    registro = er.async_get(hass)
    voce = registro.async_get_or_create(
        "automation",
        "automation",
        f"vmc_{nome}_riallineamento_allerte_al_riavvio",
        suggested_object_id=f"vmc_{nome}_riallineamento_allerte_al_riavvio",
    )
    if in_corso is not None:
        hass.states.async_set(voce.entity_id, "on", {"current": in_corso})
    if fase is not None:
        hass.states.async_set(f"input_number.vmc_{nome}_fase_riallineamento_al_riavvio", fase)
    return voce.entity_id


async def _attendi(condizione, giri: int = 50) -> None:
    """Lascia lavorare il loop senza aspettare le attese (delay) delle automazioni."""
    for _ in range(giri):
        await asyncio.sleep(0)
        if condizione():
            return
    assert condizione()


# ------------------------------------------------ nessun falso «Non Disponibile»
def test_avviso_non_disponibile_ignora_aggiorna_elenco() -> None:
    """Scegliendo «Aggiorna Elenco…» il sensore selezionato vale -100 per 2 s: gli avvisi
    «Non Disponibile» (scheda e cellulare) partono solo per un'entita' davvero scelta."""
    automazione = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    errori = [
        t
        for t in automazione["triggers"]
        if str(t.get("id", "")).startswith("Entità ") and str(t["id"]).endswith(("Errore [Interfaccia]", "Errore [Mobile]"))
    ]
    assert len(errori) == 10
    for trigger in errori:
        testo = _norm(str(trigger["value_template"]))
        selezioni = re.findall(r"input_select\.vmc_master_selected_([a-z0-9_]+)_entity", testo)
        assert len(selezioni) == 1, trigger["id"]
        assert (
            f"not states('input_select.vmc_master_selected_{selezioni[0]}_entity').startswith('Aggiorna Elenco') and"
            in testo
        ), trigger["id"]
        assert "for" not in trigger
    testo = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    for sensore, selezione in SELEZIONE.items():
        assert testo.count(f"input_select.vmc_master_selected_{selezione}_entity") == 5, sensore


def test_richiami_delle_selezioni_aggiornati() -> None:
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    automazione = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    for selezione in SELEZIONE.values():
        entita = f"input_select.vmc_master_selected_{selezione}_entity"
        riga = re.search(rf"\n  vmc_master_selected_{selezione}_entity: +# (.+)", pacchetto).group(1)
        assert f"[AUTOMAZIONE, {automazione.count(entita)} RICHIAMI]" in riga, selezione


# ------------------------------------------------ countdown di riattivazione delle allerte
def test_timer_di_riattivazione_coerente_con_le_fasi() -> None:
    pacchetto = hay.load_yaml(str(PKG / "vmc_master.yaml"))
    assert pacchetto["timer"]["vmc_master_countdown_riattivazione_allerte"]["duration"] == "00:02:20"
    riallineamento = next(
        a for a in pacchetto["automation"] if a.get("id") == "vmc_master_riallineamento_allerte_al_riavvio"
    )
    azioni = riallineamento["actions"]
    avviati = [a["target"]["entity_id"] for a in azioni if a.get("action") == "timer.start"]
    # b30: piu' il countdown di gruppo da 40 s, avviato prima della fase 2 e prima della fase 3
    gruppo = "timer.vmc_master_countdown_fase_allerte"
    assert avviati == ["timer.vmc_master_countdown_avvio_home_assistant", TIMER, gruppo, gruppo]
    # secondi dall'avvio a cui la fase diventa 2, 3, 4 e 0
    trascorsi, fasi = 0, {}
    for azione in azioni:
        if "delay" in azione:
            trascorsi += azione["delay"]["seconds"]
        elif azione.get("action") == "input_number.set_value":
            fasi[azione["data"]["value"]] = trascorsi
    assert fasi == {1: 0, 2: 60, 3: 100, 4: 140, 0: 200}
    # il countdown finisce quando tutte le allerte sono riattivate (fase 4)
    assert fasi[4] == 140


def test_scheda_con_il_countdown_di_riattivazione() -> None:
    """b30: il pannello resta visibile con il timer da 140 s e la VMC ON-Line; le righe dei
    gruppi sono nei test della b30 (tests/test_b30.py)."""
    scheda = hay.load_yaml(str(PKG / "vmc_master_scheda_manuale_interfaccia.txt"))
    carte = [c for c in scheda["cards"] if TIMER in str(c.get("conditions"))]
    assert len(carte) == 1
    carta = carte[0]
    # dalla b31 il timer e' in un «or» con la fase 3 (riga «0» del 3° gruppo, tests/test_b31_pannello.py)
    oppure = next(c for c in carta["conditions"] if c.get("condition") == "or")
    assert {"condition": "state", "entity": TIMER, "state": "active"} in oppure["conditions"]
    assert {"condition": "state", "entity": "sensor.vmc_master_status_ip_interfaccia", "state": "ON-Line"} in carta["conditions"]
    assert carta["card"]["title"] == "Riattivazione delle Allerte"
    # resta anche per le altre VMC (fuori dalle sezioni solo Master)
    assert TIMER.replace("master", "sala") in per_vmc(
        (PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8"), "sala", "192.168.1.161"
    )


def test_timer_di_riattivazione_escluso_e_ripulito() -> None:
    pacchetto = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    escluse = pacchetto[pacchetto.index("&vmc_master_entita_escluse_recorder") :]
    assert TIMER in escluse[: escluse.index("\n\n")]
    corpo = pacchetto[pacchetto.index('\n    alias: "VMC Master - Pulisci cronologia Entità"') :]
    assert TIMER in corpo[: corpo.index("\n    alias:", 10)]
    definizione = re.search(r"\n  vmc_master_countdown_riattivazione_allerte: +# (.+)", pacchetto).group(1)
    configurazione = [r for r in pacchetto.split("\n") if TIMER in r and not r.lstrip().startswith("#")]
    scheda = (PKG / "vmc_master_scheda_manuale_interfaccia.txt").read_text(encoding="utf-8")
    automazione = (PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8")
    assert definizione.startswith(
        f"[CONFIGURAZIONE, {len(configurazione)} RICHIAMI] [INTERFACCIA, {scheda.count(TIMER)} RICHIAMI] "
        f"[AUTOMAZIONE, {automazione.count(TIMER)} RICHIAMI]"
    )


def test_avviso_non_disponibile_del_dispositivo_per_le_notifiche() -> None:
    """Il sesto campo di Sensori da Selezionare: avviso solo in Home Assistant (al telefono
    tolto non si puo' scrivere) quando il dispositivo scelto non c'e' piu' tra quelli dell'app."""
    automazione = hay.load_yaml(str(PKG / "vmc_master_automazione.txt"))
    trigger = [t for t in automazione["triggers"] if t.get("id") == "Dispositivo Notifica Errore [Interfaccia]"]
    assert len(trigger) == 1 and "for" not in trigger[0]
    testo = _norm(str(trigger[0]["value_template"]))
    assert "not states('input_select.vmc_master_selected_notification_device').startswith('Aggiorna Elenco') and" in testo
    # stesso elenco dello script che aggiorna le opzioni; lo stato letto fa rivalutare il
    # trigger quando il dispositivo viene tolto (un telefono appena collegato resta «unknown»)
    assert (
        "integration_entities('mobile_app') | select('match', 'device_tracker') | reject('is_state', 'unavailable') "
        "| map('device_attr', 'name') | select('string') | map('slugify') | list" in testo
    )
    assert "states('input_boolean.vmc_master_notifica_status_vmc') == 'on'" in testo
    azioni = [
        b
        for passo in automazione["actions"]
        for b in (passo.get("choose") or [])
        if any("Dispositivo Notifica Errore [Interfaccia]" in str(c.get("id")) for c in b.get("conditions", []) if isinstance(c, dict))
    ]
    assert len(azioni) == 1
    creata = azioni[0]["sequence"][0]
    assert creata["action"] == "persistent_notification.create"
    assert creata["data"]["notification_id"] == "vmc_master_entita_non_disponibile_dispositivo_notifica"
    assert "notify." not in str(azioni[0])
