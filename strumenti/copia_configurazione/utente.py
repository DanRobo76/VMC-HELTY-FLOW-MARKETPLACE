"""Quello che fa l'utente: le stesse richieste dei pulsanti dell'interfaccia e della scheda.

- aggiungere una VMC (*Impostazioni → Dispositivi e servizi → Aggiungi integrazione /
  Aggiungi dispositivo*): il flusso di configurazione, passo per passo;
- seguire una riparazione (*Impostazioni → Riparazioni*): il flusso di riparazione, con
  «Invia» o la conferma a ogni passo;
- toccare la scheda: i servizi che la scheda chiama (``call_service`` dal websocket, con
  l'utente nel contesto, come il frontend);
- aggiungere la scheda alla plancia (modalità di modifica della plancia: salva la
  configurazione);
- le impostazioni lasciate a valori NON predefiniti, diverse per ogni VMC (così uno
  scambio fra due VMC si vede).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from ha import ClientHA, ErroreHA

DOMINIO = "vmc_master"


@dataclass(frozen=True)
class VMC:
    """Una VMC della casa di prova: nome dell'integrazione, nome della VMC (Air Guard,
    risposta a VMNM?) e indirizzo."""

    nome: str
    nome_vmc: str
    ip: str


CASA: tuple[VMC, ...] = (
    VMC("master", "Master", "192.168.1.160"),
    VMC("nord", "VMC Nord", "192.168.1.161"),
    VMC("sud", "VMC Sud", "192.168.1.162"),
)
"""Le tre VMC: la prima è «master», le altre hanno nomi generici."""


# ------------------------------------------------------------------- flussi
@dataclass
class Passo:
    """Un passo di un flusso come lo vede l'utente."""

    tipo: str
    passo: str | None
    segnaposto: dict[str, Any] = field(default_factory=dict)
    risposta: dict[str, Any] | None = None


async def aggiungi_vmc(client: ClientHA, vmc: VMC) -> list[Passo]:
    """Aggiunge la VMC con il flusso di configurazione (VMC già collegata al Wi-Fi):
    menu → «in_rete» → IP → (nome proposto, accettato) → voce creata."""
    passi: list[Passo] = []
    risultato = await client.richiesta(
        "POST",
        "/api/config/config_entries/flow",
        {"handler": DOMINIO, "show_advanced_options": False},
    )
    risposte = [{"next_step_id": "in_rete"}, {"host": vmc.ip}]
    while True:
        tipo = risultato["type"]
        passo = Passo(
            tipo,
            risultato.get("step_id"),
            risultato.get("description_placeholders") or {},
        )
        passi.append(passo)
        if tipo in ("create_entry", "abort"):
            passo.risposta = {
                k: risultato.get(k) for k in ("title", "reason", "description")
            }
            return passi
        if risposte:
            risposta = risposte.pop(0)
        elif risultato.get("step_id") in ("nome", "nome_manuale"):
            risposta = {"nome": vmc.nome}
        elif tipo == "menu" and risultato.get("step_id") == "non_raggiungibile":
            # VMC che non risponde (spenta): si aggiunge comunque, come l'utente
            risposta = {"next_step_id": "aggiungi_comunque"}
        elif tipo == "form" and not risultato.get("data_schema"):
            risposta = {}
        else:
            raise ErroreHA(f"flusso di {vmc.nome}: passo inatteso {risultato}")
        passo.risposta = risposta
        risultato = await client.richiesta(
            "POST",
            f"/api/config/config_entries/flow/{risultato['flow_id']}",
            risposta,
        )


async def segui_riparazione(
    client: ClientHA, dominio: str, issue_id: str
) -> list[Passo]:
    """Segue una riparazione come l'utente: apre il flusso e conferma ogni passo
    («Invia»; le caselle di conferma spuntate; nei menu la prima voce)."""
    passi: list[Passo] = []
    risultato = await client.richiesta(
        "POST", "/api/repairs/issues/fix", {"handler": dominio, "issue_id": issue_id}
    )
    for _ in range(10):
        tipo = risultato["type"]
        passo = Passo(
            tipo,
            risultato.get("step_id"),
            risultato.get("description_placeholders") or {},
        )
        passi.append(passo)
        if tipo in ("create_entry", "abort"):
            passo.risposta = {k: risultato.get(k) for k in ("reason", "description")}
            return passi
        if tipo == "menu":
            opzioni = risultato.get("menu_options") or []
            opzioni = list(opzioni)
            risposta: dict[str, Any] = {"next_step_id": opzioni[0]}
        else:
            risposta = {}
            for campo in risultato.get("data_schema") or []:
                if campo.get("type") == "boolean" or "boolean" in (
                    campo.get("selector") or {}
                ):
                    risposta[campo["name"]] = True
                elif campo.get("required") and "default" in campo:
                    risposta[campo["name"]] = campo["default"]
        passo.risposta = risposta
        risultato = await client.richiesta(
            "POST", f"/api/repairs/issues/fix/{risultato['flow_id']}", risposta
        )
    raise ErroreHA(f"riparazione {dominio}.{issue_id}: troppi passi")


async def riparazioni(client: ClientHA) -> list[dict[str, Any]]:
    """Le riparazioni in *Impostazioni → Riparazioni* (anche quelle ignorate)."""
    return (await client.ws_comando("repairs/list_issues"))["issues"]


# ------------------------------------------------------------------ servizi
async def tocca(
    client: ClientHA,
    dominio: str,
    servizio: str,
    entity_id: str | list[str] | None = None,
    **dati: Any,
) -> None:
    """Un tocco nella scheda: il servizio chiamato dal frontend (websocket)."""
    comando: dict[str, Any] = {"domain": dominio, "service": servizio}
    if dati:
        comando["service_data"] = dati
    if entity_id is not None:
        comando["target"] = {"entity_id": entity_id}
    await client.ws_comando("call_service", **comando)


# ------------------------------------------------------------------- plancia
def plancia_con_le_schede(voci: dict[str, str]) -> dict[str, Any]:
    """La plancia «Panoramica» dopo aver aggiunto la scheda «VMC Master» una volta per
    VMC (una vista per VMC, come quando ogni VMC ha la sua scheda), più una vista
    «Personale» con una scheda entità scritta dall'utente con alcune entità della VMC
    master (sensori e impostazioni, con i nomi di oggi)."""
    viste = [
        {
            "title": f"VMC {nome}",
            "path": f"vmc-{nome}",
            "cards": [{"type": "custom:vmc-master-card", "vmc": entry_id}],
        }
        for nome, entry_id in voci.items()
    ]
    viste.append(
        {
            "title": "Personale",
            "path": "personale",
            "cards": [
                {
                    "type": "entities",
                    "title": "VMC a colpo d'occhio",
                    "entities": list(ENTITA_PERSONALI),
                }
            ],
        }
    )
    return {"title": "Casa", "views": viste}


ENTITA_PERSONALI: tuple[str, ...] = (
    "sensor.vmc_master_status_ventola_lettura_codice_interpretato_interfaccia",
    "sensor.vmc_master_temp_interna_status_senza_offset",
    "binary_sensor.vmc_master_black_out_rilevato",
    "input_boolean.vmc_master_notifica_status_vmc",
    "input_number.vmc_master_umidita_avvio",
    "input_select.vmc_master_speed_umidita",
    "input_datetime.vmc_master_accensione_lunedi",
    "timer.vmc_master_lettura_ambientali",
)
"""Le entità della scheda personale: tre sensori (restano), quattro impostazioni e un
timer che domani cambiano dominio."""


AUTOMAZIONE_PERSONALE: dict[str, Any] = {
    "id": "vmc_velocita_1_alle_22",
    "alias": "VMC a Velocità 1 alle 22",
    "description": "L'esempio del README della beta.",
    "triggers": [{"trigger": "time", "at": "22:00:00"}],
    "conditions": [],
    "actions": [{"action": "shell_command.vmc_master_velocita_1"}],
    "mode": "single",
}
"""L'automazione d'esempio del README della beta (Comandi della VMC), creata
dall'editor delle automazioni."""


# ------------------------------------------------------------ impostazioni
GIORNI = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]

# Interruttori che restano dopo un riavvio (senza «initial»): quali si invertono, per VMC
INTERRUTTORI_INVERTITI: dict[int, tuple[str, ...]] = {
    0: (
        "notifica_allerta_black_out",
        "notifica_allerta_congelamento",
        "notifica_allerta_inquinanti",
        "notifica_allerta_riepilogo",
        "notifica_audio",
        "opzione_finestra_prossime_letture",
        "opzioni_accendi_spegni_vmc_vs_calendario",
        "opzioni_accendi_spegni_vmc_vs_freecooling",
    ),
    1: (
        "notifica_allerta_differenza_temp_int_est",
        "notifica_allerta_freecooling_heating",
        "notifica_allerta_pdr",
        "notifica_allerta_status_velocita",
        "notifica_status_vmc",
        "opzioni_accendi_spegni_avvisi",
        "opzioni_accendi_spegni_vmc_vs_freeheating",
        "opzioni_accendi_spegni_vmc_vs_umidita",
    ),
    2: (
        "notifica_allerta_umidita",
        "notifica_allerta_black_out",
        "opzione_finestra_audio",
        "opzioni_accendi_spegni_vmc_vs_co2_e_voc",
        "opzioni_accendi_spegni_vmc_vs_pdr",
        "opzioni_accendi_spegni_vmc_vs_calendario",
    ),
}
# Finestre della scheda lasciate aperte (interruttori con «initial: false»), una per VMC
# come nella scheda: due finestre aperte una subito dopo l'altra fanno rincorrere le
# due scelte di «Automazione VMC» (ognuna riaccende la sua e spegne l'altra, in coda)
# senza fine e Home Assistant cresce di memoria finché il kernel lo uccide (b41).
FINESTRE_APERTE: dict[int, tuple[str, ...]] = {
    0: ("opzioni_vmc",),
    1: ("opzioni_avvisi",),
    2: (),
}
# Sensori della casa scelti nella finestra «Sensori Opzionati» (select -> entità)
SENSORI_SCELTI: dict[int, dict[str, str]] = {
    0: {
        "selected_temp_external_entity": "sensor.sonda_temperatura_esterna",
        "selected_humidity_external_entity": "sensor.sonda_umidita_esterna",
    },
    1: {
        "selected_temp_internal_entity": "sensor.sonda_temperatura_interna",
        "selected_co2_internal_entity": "sensor.sonda_co2",
    },
    2: {"selected_humidity_internal_entity": "sensor.sonda_umidita_interna"},
}
# Velocità scelta dal telecomando della scheda dopo il Profilo Inizializzazione
VELOCITA_SCELTA: dict[int, int] = {0: 2, 1: 1, 2: 3}


def numeri(indice: int) -> dict[str, float]:
    """Le soglie e gli offset (input_number visibili), diversi per ogni VMC."""
    return {
        "audio_volume": 0.35 + 0.05 * indice,
        "offset_co2": 25.0 + 5 * indice,
        "offset_temp_esterna": round(0.7 + 0.1 * indice, 1),
        "offset_temp_interna": round(-1.3 - 0.1 * indice, 1),
        "offset_umidita_esterna": round(2.5 + indice, 1),
        "offset_umidita_interna": round(-3.2 + 0.4 * indice, 1),
        "offset_verifica_impiego_vmc": 2.0 + indice,
        "offset_voc": -40.0 + 10 * indice,
        "umidita_avvio": round(72.5 + 1.5 * indice, 1),
        "volume_da_inserire": 180.5 + 10 * indice,
    }


def selezioni(indice: int) -> dict[str, str]:
    """Mesi del Free Heating / Free Cooling e velocità scelte (input_select visibili),
    mai quelli dei profili (PREDEFINITI_DEI_PROFILI)."""
    scelte = {
        "mese_1_fascia_freecooling": ("Maggio", "Giugno", "Agosto"),
        "mese_2_fascia_freecooling": ("Agosto", "Ottobre", "Luglio"),
        "mese_1_fascia_freeheating": ("Novembre", "Settembre", "Dicembre"),
        "mese_2_fascia_freeheating": ("Marzo", "Aprile", "Maggio"),
        "speed_1_fascia_calendario": ("Velocità 3", "Velocità 4", "Notturna"),
        "speed_2_fascia_calendario": (
            "Notturna",
            "Iperventilazione",
            "Free Cool./Heat.",
        ),
        "speed_umidita": ("Velocità 4", "Free Cool./Heat.", "Velocità 2"),
    }
    return {oggetto: valori[indice % 3] for oggetto, valori in scelte.items()}


PREDEFINITI_DEI_PROFILI: dict[str, Any] = {
    "input_select.mese_1_fascia_freecooling": "Luglio",
    "input_select.mese_2_fascia_freecooling": "Settembre",
    "input_select.mese_1_fascia_freeheating": "Ottobre",
    "input_select.mese_2_fascia_freeheating": "Giugno",
    "input_select.speed_1_fascia_calendario": "Velocità 1",
    "input_select.speed_2_fascia_calendario": "Velocità 1",
    "input_select.speed_umidita": "Iperventilazione",
    "input_number.umidita_avvio": 75.0,
    "input_number.audio_volume": 0.3,
    "input_number.offset_verifica_impiego_vmc": 0.0,
    "input_datetime.audio_start_time": "08:00:00",
    "input_datetime.audio_end_time": "21:00:00",
    **{f"input_datetime.accensione_{g}": "00:30:00" for g in GIORNI},
    **{f"input_datetime.spegnimento_{g}": "06:00:00" for g in GIORNI},
    **{f"input_datetime.accensione_{g}_2": "20:00:00" for g in GIORNI},
    **{f"input_datetime.spegnimento_{g}_2": "23:30:00" for g in GIORNI},
}
"""I valori che scrivono i profili del package (Profilo Inizializzazione: Calendario,
Free Heating/Cooling, PdR, Umidità, Audio; gli offset vanno a 0): quelli della scheda
nella costruzione sono tutti diversi."""


def orari(indice: int) -> dict[str, str]:
    """Le fasce del Calendario (due accensioni e due spegnimenti al giorno) e l'orario
    delle notifiche audio, diversi per ogni giorno e per ogni VMC."""
    uscita: dict[str, str] = {}
    for g, giorno in enumerate(GIORNI):
        uscita[f"accensione_{giorno}"] = (
            f"{6 + (g + indice) % 3:02d}:{5 * g + indice:02d}:00"
        )
        uscita[f"spegnimento_{giorno}"] = f"{11 + indice:02d}:{(7 * g) % 60:02d}:00"
        uscita[f"accensione_{giorno}_2"] = f"{17 + g % 2:02d}:{10 + 3 * indice:02d}:00"
        uscita[f"spegnimento_{giorno}_2"] = (
            f"{22 + indice % 2:02d}:{(11 * g) % 60:02d}:00"
        )
    uscita["audio_start_time"] = f"{8 + indice:02d}:30:00"
    uscita["audio_end_time"] = f"{21 - indice:02d}:15:00"
    return uscita


async def imposta_vmc(client: ClientHA, vmc: VMC, indice: int) -> dict[str, Any]:
    """Le impostazioni della VMC come le lascia un utente dalla scheda; restituisce i
    valori scritti (entity_id di oggi -> valore)."""
    n = vmc.nome
    scritti: dict[str, Any] = {}
    for oggetto, valore in numeri(indice).items():
        entita = f"input_number.vmc_{n}_{oggetto}"
        await tocca(client, "input_number", "set_value", entita, value=valore)
        scritti[entita] = valore
    for oggetto, valore in selezioni(indice).items():
        entita = f"input_select.vmc_{n}_{oggetto}"
        await tocca(client, "input_select", "select_option", entita, option=valore)
        scritti[entita] = valore
    for oggetto, valore in orari(indice).items():
        entita = f"input_datetime.vmc_{n}_{oggetto}"
        await tocca(client, "input_datetime", "set_datetime", entita, time=valore)
        scritti[entita] = valore
    for oggetto in INTERRUTTORI_INVERTITI[indice]:
        entita = f"input_boolean.vmc_{n}_{oggetto}"
        await tocca(client, "input_boolean", "toggle", entita)
        scritti[entita] = "toggle"
    for oggetto, sensore in SENSORI_SCELTI[indice].items():
        entita = f"input_select.vmc_{n}_{oggetto}"
        await tocca(client, "input_select", "select_option", entita, option=sensore)
        scritti[entita] = sensore
    for oggetto in FINESTRE_APERTE[indice]:
        entita = f"input_boolean.vmc_{n}_{oggetto}"
        await tocca(client, "input_boolean", "turn_on", entita)
        scritti[entita] = "on"
    return scritti


async def profilo_inizializzazione(client: ClientHA, vmc: VMC) -> None:
    """«Configurazione» del README: Esegui su «VMC ‹nome› - Profilo Inizializzazione»,
    OK e attendere 10 s (lo script finisce dopo 10 s)."""
    await tocca(
        client, "script", "turn_on", f"script.vmc_{vmc.nome}_profilo_inizializzazione"
    )


async def scegli_velocita(client: ClientHA, vmc: VMC, velocita: int) -> None:
    """Un tasto del telecomando della scheda (comando di shell della velocità)."""
    await tocca(client, "shell_command", f"vmc_{vmc.nome}_velocita_{velocita}")


async def avvia_conti_alla_rovescia(
    client: ClientHA, vmc: VMC, indice: int
) -> list[str]:
    """Tasti della scheda che fanno partire un conto alla rovescia (script con timer):
    Agg. Sensori su tutte, Reset Filtro sulla seconda, Panic Button sulla terza."""
    script = ["upgrade_sensors"]
    if indice == 1:
        script.append("reset_filtro_vmc")
    if indice == 2:
        script.append("bottone_panico")
    for nome in script:
        await tocca(client, "script", "turn_on", f"script.vmc_{vmc.nome}_{nome}")
    return script


async def attendi(secondi: float) -> None:
    await asyncio.sleep(secondi)
