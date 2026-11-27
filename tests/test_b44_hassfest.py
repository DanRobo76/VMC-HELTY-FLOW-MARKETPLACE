"""Due regole di hassfest controllate anche da pytest (27-11-2026).

Il controllo hassfest della CI era rosso dalla fase 4 e nessuno se n'era accorto (nel repository privato
anche il controllo HACS è sempre rosso, quindi il giro intero risultava comunque fallito):

- ogni integrazione di Home Assistant importata (``homeassistant.components.X``) deve essere fra le
  ``dependencies`` o le ``after_dependencies`` del manifest, oppure fra quelle che hassfest permette
  sempre (piattaforme, ``homeassistant``, ``persistent_notification`` e le integrazioni interne);
- una riparazione che si corregge (``fix_flow``) non può avere anche ``description``: per hassfest
  le due chiavi si escludono.

Le liste sono quelle di hassfest di Home Assistant 2026.11.2 (script/hassfest/dependencies.py e
translations.py): l'unica prova completa resta il controllo hassfest della CI.
"""

import ast
import json
from pathlib import Path

from homeassistant.const import Platform

CC = Path(__file__).parent.parent / "custom_components" / "vmc_master"

# hassfest: CORE_INTEGRATIONS + piattaforme + «Internal integrations» + «Other»
PERMESSE_SEMPRE = {
    "homeassistant",
    "persistent_notification",
    *{piattaforma.value for piattaforma in Platform},
    "alert",
    "automation",
    "conversation",
    "default_config",
    "device_automation",
    "frontend",
    "group",
    "input_boolean",
    "input_button",
    "input_datetime",
    "input_number",
    "input_select",
    "input_text",
    "labs",
    "media_source",
    "onboarding",
    "panel_custom",
    "person",
    "script",
    "shopping_list",
    "sun",
    "system_health",
    "system_log",
    "timer",
    "webhook",
    "websocket_api",
    "zone",
    "mjpeg",
    "stream",
}


def _integrazioni_importate() -> dict[str, set[str]]:
    """Integrazioni importate dal codice, come le legge hassfest: nome -> file che la importano."""
    trovate: dict[str, set[str]] = {}
    for file in sorted(CC.rglob("*.py")):
        for nodo in ast.walk(ast.parse(file.read_text(encoding="utf-8"))):
            if isinstance(nodo, ast.ImportFrom) and nodo.module and nodo.level == 0:
                if nodo.module == "homeassistant.components":
                    nomi = [alias.name for alias in nodo.names]
                elif nodo.module.startswith("homeassistant.components."):
                    nomi = [nodo.module.split(".")[2]]
                else:
                    continue
            elif isinstance(nodo, ast.Import):
                nomi = [
                    alias.name.split(".")[2]
                    for alias in nodo.names
                    if alias.name.startswith("homeassistant.components.")
                ]
            else:
                continue
            for nome in nomi:
                trovate.setdefault(nome, set()).add(str(file.relative_to(CC)))
    return trovate


def test_integrazioni_importate_nel_manifest() -> None:
    """Ogni integrazione importata è dichiarata nel manifest o permessa sempre da hassfest."""
    manifest = json.loads((CC / "manifest.json").read_text(encoding="utf-8"))
    dichiarate = set(manifest.get("dependencies", [])) | set(manifest.get("after_dependencies", []))
    importate = _integrazioni_importate()
    # la lettura trova davvero gli import (le tre del 27-11-2026 comprese)
    assert {"logger", "template", "trace", "sensor"} <= set(importate)
    mancanti = {
        nome: sorted(file)
        for nome, file in importate.items()
        if nome not in PERMESSE_SEMPRE | dichiarate
    }
    assert mancanti == {}


def test_after_dependencies_senza_doppioni() -> None:
    """after_dependencies: solo le tre integrazioni importate, mai ripetute fra le dependencies."""
    manifest = json.loads((CC / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["after_dependencies"] == ["logger", "template", "trace"]
    assert not set(manifest["after_dependencies"]) & set(manifest["dependencies"])
    # hassfest vuole domain e name per primi, poi le chiavi in ordine alfabetico
    chiavi = list(manifest)
    assert chiavi[:2] == ["domain", "name"]
    assert chiavi[2:] == sorted(chiavi[2:])


def test_riparazioni_correggibili_senza_description() -> None:
    """Una riparazione con fix_flow non ha description, in strings.json e in ogni traduzione."""
    file = [CC / "strings.json", *sorted((CC / "translations").glob("*.json"))]
    controllate = 0
    for percorso in file:
        riparazioni = json.loads(percorso.read_text(encoding="utf-8"))["issues"]
        for chiave, riparazione in riparazioni.items():
            if "fix_flow" in riparazione:
                controllate += 1
                assert "description" not in riparazione, (percorso.name, chiave)
    # riavvio_necessario, passaggio_dalla_beta, impostazioni_rinominate in 3 file
    assert controllate == 9
