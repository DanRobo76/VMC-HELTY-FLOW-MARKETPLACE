"""Genera custom_components/vmc_master/nativa/tabelle.py dal package della b42.

L'integrazione nativa non legge il package: nomi, icone, unità e impostazioni dei sensori
e degli helper di oggi stanno in tabelle Python scritte da questo programma. Il test
test_tabelle.py controlla che il file sia uguale a quello che il programma scrive.

Uso (dalla cartella del repository):
    /home/user/hat/bin/python -m tests.nativa.genera_tabelle
"""

from __future__ import annotations

import csv
import pprint
from pathlib import Path
from typing import Any

from homeassistant.util import slugify
from homeassistant.util.yaml.loader import parse_yaml

from .confronto import IP, RADICE, _installatore

FILE = RADICE / "custom_components" / "vmc_master" / "nativa" / "tabelle.py"
# La colonna «Domani» della fase 1 (decisione approvata: dominio di domani per ogni voce)
FASE_1 = RADICE / "tests" / "nativa" / "motore" / "aiutanti_fase1.csv"
INTERNA = "interna"
TOLTA = "tolta"
VERSIONE = "9.0.0b42"
# Due nomi diversi: le parti che cambiano tra le due VMC sono il nome della VMC.
NOMI = ("master", "zeta")

_DOMINI_HELPER = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
    "timer",
)
# Nomi visibili rimasti dal mondo del package che la versione nativa cambia: solo il nome
# (chiave come in tabelle.py; entity_id e unique_id restano quelli del package, così la
# cronologia continua). Il package non c'è più, quindi niente «Package» nei nomi. Valgono
# per i sensori (SENSORI) e gli aiutanti (IMPOSTAZIONI); per i sensori template li usa
# anche il traduttore della fase 4 (tests/nativa/motore/traduci_fase4.py, che scrive
# motore/generato_fase4/sensori.py, da cui nascono le loro entità).
NOMI_NATIVI = {
    "sensor.versione_corrente": "Versione",
    "input_boolean.popup_versione_corrente_vs_repository": "PopUp Notifica Aggiornamento",
}

# b46 (revisione del catalogo): l'IP della VMC si cambia solo dall'ingranaggio della VMC
# («Cambia l'IP della VMC»). Il campo «Cambia IP VMC» della scheda e ciò che serviva solo a
# lui (il sensore che lo controllava, il valore interno con l'esito della verifica, il
# comando che scriveva l'IP nei file e l'automazione che riavviava Home Assistant) non
# sono nella versione nativa: fuori da SENSORI, IMPOSTAZIONI e ORDINE_AIUTANTI (anche dalle
# opzioni che li elencano), «tolta» in DOMANI (come nella colonna «Domani» della fase 1) e
# in TOLTE con il nome che avevano. Chiavi come in tabelle.py.
TOLTE = (
    "input_text.ip_insert",
    "input_text.ip_insert_esito",
    "shell_command.aggiorna_indirizzo_ip",
    "sensor.verifica_ip_inserito",
    "automation.cambio_ip_vmc_riavvio_di_h_a",
)

_CAMPI_MODELLO = {
    "name": "nome",
    "icon": "icona",
    "unit_of_measurement": "unita",
    "device_class": "classe",
    "state_class": "classe_stato",
}


def _package(nome: str) -> dict[str, Any]:
    return parse_yaml(
        _installatore().genera_file(nome, IP, VERSIONE)[f"vmc_{nome}.yaml"]
    )


def _segnaposto(valore: Any, nome: str) -> Any:
    """Il nome della VMC dentro un testo diventa {nome} / {Nome} / {NOME}.

    Come il clona di oggi (s/master/nome/, s/Master/nome/, s/MASTER/nome/): {Nome} e
    {NOME} valgono «Master» e «MASTER» per la VMC Master e il nome così com'è per le altre.
    """
    if isinstance(valore, str):
        return (
            valore.replace(nome, "{nome}")
            .replace(nome.capitalize(), "{Nome}")
            .replace(nome.upper(), "{NOME}")
        )
    if isinstance(valore, list):
        return [_segnaposto(v, nome) for v in valore]
    if isinstance(valore, dict):
        return {k: _segnaposto(v, nome) for k, v in valore.items()}
    return valore


def _chiave(entity_id: str, nome: str) -> str:
    dominio, oggetto = entity_id.split(".", 1)
    return f"{dominio}.{oggetto.removeprefix(f'vmc_{nome}_')}"


def _sensori(pkg: dict[str, Any], nome: str) -> dict[str, dict[str, Any]]:
    uscita: dict[str, dict[str, Any]] = {}
    for blocco in pkg["template"]:
        for dominio in ("sensor", "binary_sensor"):
            for conf in blocco.get(dominio, []) or []:
                chiave = _chiave(conf["default_entity_id"], nome)
                voce: dict[str, Any] = {
                    "tipo": "memoria" if "triggers" in blocco else "modello"
                }
                for campo, nuovo in _CAMPI_MODELLO.items():
                    if campo in conf:
                        valore = conf[campo]
                        if campo == "icon" and ("{{" in valore or "{%" in valore):
                            valore = None  # icona calcolata dal modello
                        voce[nuovo] = _segnaposto(valore, nome)
                if chiave in NOMI_NATIVI:
                    voce["nome"] = NOMI_NATIVI[chiave]
                uscita[chiave] = voce
    for conf in pkg["sensor"]:
        chiave = _chiave(f"sensor.{conf['name']}", nome)
        tipo = {"tcp": "lettura", "rest": "versione"}[conf["platform"]]
        uscita[chiave] = {"tipo": tipo, "nome": _segnaposto(conf["name"], nome)}
    for voce in pkg["command_line"]:
        conf = voce["sensor"]
        if "ping" in conf["command"]:
            uscita[_chiave(f"sensor.{conf['name']}", nome)] = {
                "tipo": "ping",
                "nome": _segnaposto(conf["name"], nome),
            }
    return uscita


def _impostazioni(pkg: dict[str, Any], nome: str) -> dict[str, dict[str, Any]]:
    uscita: dict[str, dict[str, Any]] = {}
    for dominio in _DOMINI_HELPER:
        for oggetto, conf in (pkg.get(dominio) or {}).items():
            chiave = _chiave(f"{dominio}.{oggetto}", nome)
            uscita[chiave] = _segnaposto(dict(conf or {}), nome)
            if chiave in NOMI_NATIVI:
                uscita[chiave]["name"] = NOMI_NATIVI[chiave]
    return uscita


def _ordine(pacchetti: dict[str, dict[str, Any]]) -> dict[str, tuple[str, ...]]:
    """Per ogni dominio degli aiutanti input_*, le voci (chiavi come IMPOSTAZIONI)
    nell'ordine del package del master: l'ordine in cui oggi Home Assistant aggiunge gli
    aiutanti (nelle altre VMC lo stesso, senza le voci solo del master)."""
    uscita: dict[str, tuple[str, ...]] = {}
    for dominio in _DOMINI_HELPER:
        if dominio == "timer":
            continue
        ordini = {
            nome: [
                chiave
                for o in pkg.get(dominio) or {}
                if (chiave := _chiave(f"{dominio}.{o}", nome)) not in TOLTE
            ]
            for nome, pkg in pacchetti.items()
        }
        master = ordini["master"]
        for nome, ordine in ordini.items():
            if ordine != [k for k in master if k in set(ordine)]:
                raise ValueError(f"{dominio}: ordine diverso nella VMC {nome}")
        uscita[dominio] = tuple(master)
    return uscita


def _domani() -> dict[str, str]:
    """Voce del package (chiave come IMPOSTAZIONI) -> dominio di domani, o «interna».

    Dalla colonna «Domani» della fase 1 (scritta per la VMC master): l'oggetto dopo il
    punto non cambia mai, cambia solo il dominio; «interna» = stato del motore, non entità.
    """
    uscita: dict[str, str] = {}
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        for riga in csv.DictReader(flusso, delimiter=";"):
            chiave = _chiave(riga["Entità oggi"], "master")
            domani = riga["Domani"]
            if domani == TOLTA:
                if chiave not in TOLTE:
                    raise ValueError(f"{riga['Entità oggi']}: «{TOLTA}» ma non in TOLTE")
                uscita[chiave] = TOLTA
                continue
            if "." not in domani:
                uscita[chiave] = INTERNA
                continue
            dominio, oggetto = domani.split(".", 1)
            if oggetto != riga["Entità oggi"].split(".", 1)[1]:
                raise ValueError(
                    f"{riga['Entità oggi']}: domani cambia oggetto ({domani})"
                )
            uscita[chiave] = dominio
    return dict(sorted(uscita.items()))


# Fase 4: i comandi di shell che la scheda chiama diventano pulsanti. Uno shell_command non
# ha nome né icona: il nome è l'etichetta del tasto della scheda (come il sensore
# binary_sensor.vmc_<nome>_tasto_* che la scheda mostra sul tasto), l'icona quella dei
# pulsanti degli script (mdi:cursor-pointer). Scelta provvisoria, da confermare.
_ETICHETTE_COMANDI = {
    "freecooling": "Free Cool./Heat.",
    "iperventilazione": "Iperventilazione",
    "notturna": "Notturna",
    "pannello_led_off": "Led Pannello Off",
    "pannello_led_on": "Led Pannello On",
    "sensori_off": "Sensori Off",
    "sensori_on": "Sensori On",
    **{f"velocita_{n}": f"Velocità {n}" for n in range(5)},
}
_ICONA_COMANDI = "mdi:cursor-pointer"


def _pulsanti(pkg: dict[str, Any], nome: str) -> dict[str, dict[str, Any]]:
    """I pulsanti: gli script e i comandi di shell che nella colonna «Domani» della fase 1
    diventano ``button`` (nella fase 1 i nomi sono quelli della Master)."""
    uscita: dict[str, dict[str, Any]] = {}
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        righe = list(csv.DictReader(flusso, delimiter=";"))
    for riga in righe:
        if not riga["Domani"].startswith("button."):
            continue
        tipo, oggetto_master = riga["Entità oggi"].split(".", 1)
        oggetto = oggetto_master.replace("vmc_master_", f"vmc_{nome}_", 1)
        chiave = _chiave(f"button.{oggetto}", nome)
        if tipo == "script":
            conf = pkg["script"][oggetto]
            voce = {"tipo": "script", "nome": conf["alias"], "icona": conf["icon"]}
        else:
            pkg["shell_command"][oggetto]  # il comando c'è
            etichetta = _ETICHETTE_COMANDI[chiave.split(".", 1)[1]]
            # come gli alias degli script: «Master» nella Master, il nome nelle altre
            nome_vmc = "Master" if nome == "master" else nome
            voce = {
                "tipo": "comando",
                "nome": f"VMC {nome_vmc} - {etichetta}",
                "icona": _ICONA_COMANDI,
            }
        uscita[chiave] = _segnaposto(voce, nome)
    return uscita


def _senza_tolte(voci: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Le voci senza quelle tolte (TOLTE), e senza le voci tolte nelle opzioni che elencano
    entity_id (le entità escluse dal Recorder)."""
    tolte = {f"{c.split('.', 1)[0]}.vmc_{{nome}}_{c.split('.', 1)[1]}" for c in TOLTE}
    uscita = {}
    for chiave, voce in voci.items():
        if chiave in TOLTE:
            continue
        if isinstance(voce.get("options"), list):
            voce = {**voce, "options": [o for o in voce["options"] if o not in tolte]}
        uscita[chiave] = voce
    return uscita


def _nomi_tolte(pkg: dict[str, Any], nome: str) -> dict[str, str]:
    """Il nome che le voci tolte (TOLTE) avevano nel package della VMC ``nome`` (un
    comando di shell non ha nome)."""
    nomi = {k: v["nome"] for k, v in _sensori(pkg, nome).items()}
    nomi |= {k: v.get("name", "") for k, v in _impostazioni(pkg, nome).items()}
    nomi |= {_chiave(f"shell_command.{o}", nome): "" for o in pkg["shell_command"]}
    for automazione in pkg["automation"]:
        alias = automazione["alias"]
        nomi[_chiave(f"automation.{slugify(alias)}", nome)] = _segnaposto(alias, nome)
    return {chiave: nomi[chiave] for chiave in TOLTE}


def _come_altra(valore: Any) -> Any:
    """Una voce del master come apparirebbe in un'altra VMC: {Nome} e {NOME} diventano {nome}."""
    if isinstance(valore, str):
        return valore.replace("{Nome}", "{nome}").replace("{NOME}", "{nome}")
    if isinstance(valore, list):
        return [_come_altra(v) for v in valore]
    if isinstance(valore, dict):
        return {k: _come_altra(v) for k, v in valore.items()}
    return valore


def _unisci(master: dict[str, dict], altra: dict[str, dict]) -> dict[str, dict]:
    """Le voci del master (con le sezioni solo del master); dove esistono anche nell'altra
    VMC devono coincidere, segnaposto compresi."""
    for chiave, voce in altra.items():
        if _come_altra(master.get(chiave)) != voce:
            raise ValueError(
                f"{chiave}: master {master.get(chiave)!r}, altra VMC {voce!r}"
            )
    solo_master = sorted(set(master) - set(altra))
    return {
        k: dict(v, solo_master=True) if k in solo_master else v
        for k, v in sorted(master.items())
    }


def contenuto() -> str:
    """Il testo di tabelle.py."""
    pacchetti = {nome: _package(nome) for nome in NOMI}
    sensori = _senza_tolte(_unisci(*(_sensori(pacchetti[n], n) for n in NOMI)))
    impostazioni = _senza_tolte(
        _unisci(*(_impostazioni(pacchetti[n], n) for n in NOMI))
    )
    pulsanti = _unisci(*(_pulsanti(pacchetti[n], n) for n in NOMI))
    stampa = pprint.PrettyPrinter(width=110, sort_dicts=True).pformat
    righe = [
        f'"""Tabelle dei sensori e delle impostazioni della VMC, dal package della {VERSIONE}.',
        "",
        "FILE GENERATO da tests/nativa/genera_tabelle.py: non modificarlo a mano.",
        "",
        "Chiave = entity_id di oggi senza «vmc_<nome>_». Nei testi {nome} è il nome della VMC;",
        "{Nome}/{NOME} valgono Master/MASTER per la VMC Master e il nome per le altre. SENSORI: tipo (modello, memoria, lettura, ping, versione), nome, icona fissa",
        "(None = calcolata dal modello), unità e classi. IMPOSTAZIONI: gli helper di oggi con la",
        "loro configurazione (nome, icona, iniziale, min/max/step, opzioni, durata...).",
        "solo_master = la voce c'è solo nel master (sezioni Clona VMC e Installa VMC).",
        "DOMANI: per ogni voce del package (helper, script, shell_command) il dominio di domani",
        "(colonna «Domani» della fase 1), o «interna» se diventa stato interno del motore, o",
        "«tolta» se la versione nativa non l'ha più (TOLTE).",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        f"VERSIONE_PACKAGE = {VERSIONE!r}",
        "",
        f"SENSORI: dict[str, dict[str, Any]] = {stampa(sensori)}",
        "",
        f"IMPOSTAZIONI: dict[str, dict[str, Any]] = {stampa(impostazioni)}",
        "",
        f"DOMANI: dict[str, str] = {stampa(_domani())}",
        "",
        "# Fase 4: le voci degli aiutanti input_* nell'ordine del package (in cui oggi Home",
        "# Assistant li aggiunge): l'ordine delle scritture di una chiamata con più entità.",
        f"ORDINE_AIUTANTI: dict[str, tuple[str, ...]] = {stampa(_ordine(pacchetti))}",
        "",
        "# Fase 4: gli script e i comandi di shell che la scheda chiama, come pulsanti (tipo",
        "# script o comando: lo script o lo shell_command di oggi con lo stesso oggetto).",
        f"PULSANTI: dict[str, dict[str, Any]] = {stampa(pulsanti)}",
        "",
        "# b46: le voci del package che la versione nativa non ha più (il campo «Cambia IP VMC»",
        "# della scheda e ciò che serviva solo a lui: l'IP si cambia dall'ingranaggio della",
        "# VMC), con il nome che avevano nel package.",
        f"TOLTE: dict[str, str] = {stampa(_nomi_tolte(pacchetti['master'], 'master'))}",
        "",
    ]
    return "\n".join(righe)


def scrivi() -> Path:
    FILE.write_text(contenuto(), encoding="utf-8")
    return FILE


if __name__ == "__main__":
    print(scrivi())
