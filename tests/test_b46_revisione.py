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
