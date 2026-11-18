"""b24: Profilo Inizializzazione senza riavvio, una sola notifica persistente per problema."""
import re
from pathlib import Path

PKG = Path(__file__).parent.parent / "custom_components" / "vmc_master" / "package"


def _script_inizializzazione() -> str:
    testo = (PKG / "vmc_master.yaml").read_text(encoding="utf-8")
    inizio = testo.index("\n  vmc_master_profilo_inizializzazione:")
    fine = testo.index("\n  vmc_master_", inizio + 10)
    return testo[inizio:fine]


def test_inizializzazione_non_riavvia_home_assistant():
    corpo = _script_inizializzazione()
    assert "action: homeassistant.restart" not in corpo
    assert "input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_umidita" in corpo


def test_ogni_notifica_persistente_del_package_ha_un_id():
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt"):
        righe = (PKG / nome).read_text(encoding="utf-8").splitlines()
        for i, riga in enumerate(righe):
            if riga.strip() == "- action: persistent_notification.create":
                blocco = "\n".join(righe[i : i + 5])
                assert re.search(r"notification_id: \S+", blocco), (nome, i + 1)


def test_id_notifiche_unici():
    ids = []
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt"):
        ids += re.findall(r"notification_id: \"?(vmc_master_\w+)", (PKG / nome).read_text(encoding="utf-8"))
    duplicati = {i for i in ids if ids.count(i) > 1} - {"vmc_master_installa_vmc_esito"}
    assert not duplicati
