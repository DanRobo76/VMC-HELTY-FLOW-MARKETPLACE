"""Le correzioni chieste dalla revisione del catalogo HACS (hacs/default #15056, 27-11-2026).

Punto 2: il ping della VMC importa ``icmplib`` (nativa/letture.py), che non è un requisito del nucleo
di Home Assistant: va fra i ``requirements`` del manifest, con la stessa versione dell'integrazione
ping di Home Assistant (così non si installa una seconda versione).

Punto 3: la password dell'access point della VMC si scrive nascosta come quella del Wi-Fi di casa
(il modulo lo prova tests/test_integrazione.py, test_server_su_un_altro_wifi).
"""

import json
from pathlib import Path

from homeassistant.components import ping

import custom_components.vmc_master  # noqa: F401  (si prova anche da solo)

CC = Path(__file__).parent.parent / "custom_components" / "vmc_master"


def test_icmplib_fra_i_requisiti_come_nel_ping_di_home_assistant() -> None:
    manifest = json.loads((CC / "manifest.json").read_text(encoding="utf-8"))
    ping_ha = json.loads((Path(ping.__file__).parent / "manifest.json").read_text(encoding="utf-8"))
    icmplib_ha = [r for r in ping_ha["requirements"] if r.startswith("icmplib==")]
    assert icmplib_ha
    assert [r for r in manifest["requirements"] if r.startswith("icmplib")] == icmplib_ha


def test_letture_importa_icmplib() -> None:
    """Se il ping smettesse di usare icmplib, il requisito andrebbe tolto."""
    assert "from icmplib" in (CC / "nativa" / "letture.py").read_text(encoding="utf-8")


# --- Punto 1: il motore è codice dell'integrazione ------------------------------------------------
#
# Niente entità nei domini automation e script, niente classi di altre integrazioni, niente nomi
# privati di Home Assistant (importati o letti sugli oggetti di Home Assistant), niente dati di altre
# integrazioni in hass.data. Il controllo legge il codice (anche quello generato), non i testi.

import ast

# Moduli di altre integrazioni che il motore usava dall'interno
_MODULI_VIETATI = (
    "homeassistant.components.automation",
    "homeassistant.components.script",
    "homeassistant.components.template",
    "homeassistant.components.trace",
    "homeassistant.components.homeassistant.triggers",
)
# Nomi di Home Assistant che servono solo a usare le sue parti interne
_NOMI_VIETATI = {
    "AutomationEntity",
    "ScriptEntity",
    "StateSensorEntity",
    "StateBinarySensorEntity",
    "DATA_SCRIPTS",
    "DATA_NEW_SCRIPT_RUNS_NOT_ALLOWED",
    "DATA_CUSTOMIZE",
    "async_prepare_reload",
    "async_initialize_triggers",
    "async_track_template_result",
    "async_track_template",
    "async_track_same_state",
}
# Attributi privati degli oggetti di Home Assistant (State._cache, StateMachine._states,
# HomeAssistantError._message, Template._renders)
_ATTRIBUTI_PRIVATI = {"_cache", "_states", "_message", "_renders"}


def _alberi() -> list[tuple[Path, ast.AST]]:
    return [
        (file, ast.parse(file.read_text(encoding="utf-8")))
        for file in sorted(CC.rglob("*.py"))
    ]


def test_nessun_nome_privato_di_home_assistant() -> None:
    trovati = []
    for file, albero in _alberi():
        for nodo in ast.walk(albero):
            if isinstance(nodo, ast.ImportFrom) and (nodo.module or "").startswith("homeassistant"):
                trovati += [
                    f"{file.relative_to(CC)}: {nodo.module}.{a.name}"
                    for a in nodo.names
                    if a.name.startswith("_")
                ]
            elif isinstance(nodo, ast.Attribute) and nodo.attr in _ATTRIBUTI_PRIVATI:
                trovati.append(f"{file.relative_to(CC)}:{nodo.lineno}: .{nodo.attr}")
    assert trovati == []


def test_nessuna_parte_interna_di_altre_integrazioni() -> None:
    trovati = []
    for file, albero in _alberi():
        for nodo in ast.walk(albero):
            if isinstance(nodo, ast.ImportFrom) and nodo.level == 0:
                modulo = nodo.module or ""
                nomi = {a.name for a in nodo.names}
                if modulo.startswith(_MODULI_VIETATI) or nomi & _NOMI_VIETATI:
                    trovati.append(f"{file.relative_to(CC)}: from {modulo} import {sorted(nomi)}")
                if modulo == "homeassistant.components":
                    nomi_vietati = {m.rsplit(".", 1)[1] for m in _MODULI_VIETATI}
                    if nomi & nomi_vietati:
                        trovati.append(f"{file.relative_to(CC)}: {sorted(nomi & nomi_vietati)}")
            elif isinstance(nodo, ast.Import):
                trovati += [
                    f"{file.relative_to(CC)}: import {a.name}"
                    for a in nodo.names
                    if a.name.startswith(_MODULI_VIETATI)
                ]
            elif isinstance(nodo, ast.ClassDef):
                basi = {ast.unparse(b).rsplit(".", 1)[-1] for b in nodo.bases}
                if basi & _NOMI_VIETATI:
                    trovati.append(f"{file.relative_to(CC)}: class {nodo.name}{sorted(basi)}")
    assert trovati == []


def _chiave_di_hass_data(nodo: ast.AST) -> ast.AST | None:
    """La chiave di ``hass.data[...]`` o ``hass.data.get/setdefault/pop(...)``, o None."""
    def e_hass_data(n: ast.AST) -> bool:
        return (
            isinstance(n, ast.Attribute)
            and n.attr == "data"
            and ast.unparse(n.value).split(".")[-1] == "hass"
        )

    if isinstance(nodo, ast.Subscript) and e_hass_data(nodo.value):
        return nodo.slice
    if (
        isinstance(nodo, ast.Call)
        and isinstance(nodo.func, ast.Attribute)
        and nodo.func.attr in ("get", "setdefault", "pop")
        and e_hass_data(nodo.func.value)
        and nodo.args
    ):
        return nodo.args[0]
    return None


def test_hass_data_solo_con_le_chiavi_dell_integrazione() -> None:
    """In hass.data l'integrazione usa solo le proprie chiavi (costanti ``HassKey``/``DATI_*``)
    e quella pubblica delle plance (``LOVELACE_DATA``, per registrare la risorsa della scheda)."""
    trovati = []
    for file, albero in _alberi():
        for nodo in ast.walk(albero):
            if (chiave := _chiave_di_hass_data(nodo)) is None:
                continue
            testo = ast.unparse(chiave)
            proprie = isinstance(chiave, ast.Name) and (
                chiave.id == "LOVELACE_DATA"
                or chiave.id.lstrip("_").startswith(("DATI", "BUS", "CAMBI"))
            )
            if not proprie:
                trovati.append(f"{file.relative_to(CC)}:{nodo.lineno}: hass.data[{testo}]")
    assert trovati == []
