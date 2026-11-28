"""9.0.0b48: i consigli della revisione del catalogo HACS (hacs/default #15056, approvata).

- Nessuna funzione riservata al nucleo di Home Assistant (``async_fire_internal``) e
  nessuna parte privata della macchina degli stati: la macchina degli stati dei modelli
  del motore dà solo le parti pubbliche.
- La licenza Apache-2.0 accanto al codice ripreso da Home Assistant, e ogni file che ne
  riprende una parte dice dove si trova.
- La configurazione di una VMC nuova avvisa che il Wi-Fi del server passa per circa un
  minuto alla rete della VMC (anche nel README).
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

import custom_components.vmc_master  # noqa: F401  (si prova anche da solo)
from custom_components.vmc_master.nativa.motore.memoria_interna import StatiConMemoria

RADICE = Path(__file__).resolve().parents[1]
CC = RADICE / "custom_components/vmc_master"
LICENZA = CC / "LICENSE-Apache-2.0.txt"
# i file che riprendono parti di Home Assistant 2026.11 (Apache-2.0)
RIPRESI = (
    "nativa/sensori_modello.py",
    "nativa/motore/attivazioni.py",
    "nativa/motore/chiusura.py",
    "nativa/motore/contesto.py",
    "nativa/motore/jinja.py",
    "nativa/motore/logiche.py",
    "nativa/motore/seguire.py",
    "nativa/motore/timer.py",
)


def _alberi() -> list[tuple[Path, ast.AST]]:
    return [
        (file, ast.parse(file.read_text(encoding="utf-8")))
        for file in sorted(CC.rglob("*.py"))
    ]


def test_nessuna_funzione_riservata_al_nucleo() -> None:
    trovati = [
        f"{file.relative_to(CC)}:{nodo.lineno}"
        for file, albero in _alberi()
        for nodo in ast.walk(albero)
        if isinstance(nodo, ast.Attribute) and nodo.attr == "async_fire_internal"
    ]
    assert trovati == []


def test_nessuna_parte_privata_della_macchina_degli_stati() -> None:
    # nessuno la definisce (la leggerebbe il motore dei modelli di Home Assistant)...
    trovati = [
        f"{file.relative_to(CC)}:{nodo.lineno}"
        for file, albero in _alberi()
        for nodo in ast.walk(albero)
        if isinstance(nodo, ast.FunctionDef | ast.AsyncFunctionDef)
        and nodo.name == "_states"
    ]
    assert trovati == []

    # ... e la macchina degli stati dei modelli non dà le parti private di quella vera
    class Vera:
        def __init__(self) -> None:
            self._states = {"sensor.x": object()}
            self.valore = 1

    stati = StatiConMemoria(Vera(), {})
    assert stati.valore == 1
    with pytest.raises(AttributeError):
        _ = stati._states


def test_licenza_apache_accanto_al_codice_ripreso() -> None:
    testo = LICENZA.read_text(encoding="utf-8")
    assert testo.lstrip().startswith("Apache License")
    assert "Version 2.0, January 2004" in testo
    assert "END OF TERMS AND CONDITIONS" in testo
    for nome in RIPRESI:
        sorgente = " ".join((CC / nome).read_text(encoding="utf-8").split())
        assert "Apache-2.0" in sorgente, nome
        assert "LICENSE-Apache-2.0.txt" in sorgente, nome


@pytest.mark.parametrize("percorso", [RADICE / "README.md", RADICE / ".github/README.md"], ids=["radice", "github"])
def test_readme_licenza_apache(percorso: Path) -> None:
    testo = percorso.read_text(encoding="utf-8")
    link = "(https://github.com/DanRobo76/VMC-HELTY-FLOW-MASTER/blob/main/custom_components/vmc_master/LICENSE-Apache-2.0.txt)"
    assert testo.count(f"Alcune parti del motore sono riprese da Home Assistant e restano sotto licenza [Apache-2.0]{link}.") == 1
    assert testo.count(f"Some parts of the engine come from Home Assistant and stay under the [Apache-2.0]{link} licence.") == 1


_AVVISO_IT = (
    "⚠️ Dopo Invia il Wi-Fi del server passa per circa un minuto alla rete della VMC: se"
    " Home Assistant raggiunge la rete di casa solo via Wi-Fi, in quel minuto non è"
    " raggiungibile. Da fuori casa si perde il collegamento finché il server non torna"
    " sulla rete di casa."
)
_AVVISO_EN = (
    "⚠️ After Submit the server's Wi-Fi switches to the unit network for about a minute:"
    " if Home Assistant reaches the home network only through Wi-Fi, it cannot be reached"
    " during that minute. If you are away from home, you lose the connection until the"
    " server is back on the home network."
)


@pytest.mark.parametrize(
    ("file", "avviso"),
    [
        ("strings.json", _AVVISO_EN),
        ("translations/en.json", _AVVISO_EN),
        ("translations/it.json", _AVVISO_IT),
    ],
)
def test_avviso_wifi_nella_configurazione(file: str, avviso: str) -> None:
    passo = json.loads((CC / file).read_text(encoding="utf-8"))["config"]["step"]["rete_vmc"]
    assert passo["description"].count(avviso) == 1


def test_avviso_wifi_nel_readme() -> None:
    testo = (RADICE / ".github/README.md").read_text(encoding="utf-8")
    assert testo.count(
        "**VMC nuova** (senza l'App Air Guard, vedere *Requisiti*):\n\n> ⚠️ Durante il"
        " collegamento il Wi-Fi del server passa per circa un minuto alla rete della VMC: se"
        " Home Assistant raggiunge la rete di casa solo via Wi-Fi, in quel minuto non è"
        " raggiungibile. Da fuori casa si perde il collegamento finché il server non torna"
        " sulla rete di casa.\n\n1. "
    ) == 1
    assert testo.count(
        "**New unit** (without the Air Guard app, see *Requirements*):\n\n> ⚠️ During the"
        " connection the server's Wi-Fi switches to the unit network for about a minute: if"
        " Home Assistant reaches the home network only through Wi-Fi, it cannot be reached"
        " during that minute. If you are away from home, you lose the connection until the"
        " server is back on the home network.\n\n1. "
    ) == 1
