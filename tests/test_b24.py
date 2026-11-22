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
                j = i + 1
                while righe[j].strip() != "data:":
                    j += 1
                rientro = len(righe[j]) - len(righe[j].lstrip())
                chiavi = []
                for altra in righe[j + 1 :]:
                    if altra.strip() and len(altra) - len(altra.lstrip()) <= rientro:
                        break
                    if len(altra) - len(altra.lstrip()) == rientro + 2:
                        chiavi.append(altra.strip().split(":")[0])
                assert chiavi.count("notification_id") == 1, (nome, i + 1)


def test_id_notifiche_unici():
    ids = []
    for nome in ("vmc_master.yaml", "vmc_master_automazione.txt"):
        # Conta solo gli id delle create: un dismiss riusa apposta lo stesso id
        testo = re.sub(r"- action: persistent_notification\.dismiss\s+data:\s+notification_id: \"?\w+", "", (PKG / nome).read_text(encoding="utf-8"))
        ids += re.findall(r"notification_id: \"?(vmc_master_\w+)", testo)
    # b30: la notifica del Dispositivo di Notifica ha due testi (con e senza cellulari) sullo stesso id
    duplicati = {i for i in ids if ids.count(i) > 1} - {"vmc_master_installa_vmc_esito", "vmc_master_aggiorna_entita_dispositivo_notifica"}
    assert not duplicati


SCRIPT_AGGIORNA_ELENCO = {
    "temperatura_esterna": ("input_select.vmc_master_selected_temp_external_entity", "Aggiorna Elenco Entità Temperatura Esterna", "vmc_master_aggiorna_entita_temperatura_esterna"),
    "temperatura_interna": ("input_select.vmc_master_selected_temp_internal_entity", "Aggiorna Elenco Entità Temperatura Interna", "vmc_master_aggiorna_entita_temperatura_interna"),
    "umidita_esterna": ("input_select.vmc_master_selected_humidity_external_entity", "Aggiorna Elenco Entità Umidità Esterna", "vmc_master_aggiorna_entita_umidita_esterna"),
    "umidita_interna": ("input_select.vmc_master_selected_humidity_internal_entity", "Aggiorna Elenco Entità Umidità Interna", "vmc_master_aggiorna_entita_umidita_interna"),
    "co2_interna": ("input_select.vmc_master_selected_co2_internal_entity", "Aggiorna Elenco Entità CO₂ Interna", "vmc_master_aggiorna_entita_co2_interna"),
    "notifica_dispositivo": ("input_select.vmc_master_selected_notification_device", "Aggiorna Elenco Dispositivi per Invio Notifica", "vmc_master_aggiorna_entita_dispositivo_notifica"),
    "media_player": ("input_select.vmc_master_selected_media_player_entity", "Aggiorna Elenco Media Player", "vmc_master_aggiorna_entita_media_player"),
}


def _trova(passi, azione):
    """Restituisce (passo, antenati) per ogni passo con quell'action, a qualsiasi profondità."""
    trovati = []

    def visita(nodo, antenati):
        if isinstance(nodo, dict):
            if nodo.get("action") == azione:
                trovati.append((nodo, antenati))
            for v in nodo.values():
                visita(v, antenati + [nodo])
        elif isinstance(nodo, list):
            for v in nodo:
                visita(v, antenati)

    visita(passi, [])
    return trovati


def test_notifiche_aggiorna_elenco_condizionate_e_chiuse_da_sole():
    import yaml

    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
    script = yaml.load((PKG / "vmc_master.yaml").read_text(encoding="utf-8"), Loader=Loader)["script"]
    for nome, (select, voce, nid) in SCRIPT_AGGIORNA_ELENCO.items():
        passi = script[f"vmc_master_aggiorna_elenco_entita_{nome}"]["sequence"]
        create = _trova(passi, "persistent_notification.create")
        if nome == "media_player":
            # Nessuna notifica per il Media Player: restano i due dismiss (tolgono quella delle versioni precedenti)
            assert not create, nome
            dismiss = _trova(passi, "persistent_notification.dismiss")
            assert len(dismiss) == 2 and all(d["data"]["notification_id"] == nid for d, _ in dismiss), nome
            continue
        if nome == "notifica_dispositivo":
            # b30: secondo testo (nessun cellulare) nel ramo else, stesso id
            assert len(create) == 2 and create[1][0]["data"]["notification_id"] == nid, nome
            assert create[1][0]["data"]["message"].startswith("Nessun cellulare"), nome
            create = create[:1]
        assert len(create) == 1, nome
        nodo, antenati = create[0]
        assert nodo["data"]["notification_id"] == nid, nome
        # La create sta in un if che controlla le opzioni senza la voce "Aggiorna Elenco"
        se = next(a for a in reversed(antenati) if "if" in a and nodo in a.get("then", []))
        condizione = se["if"][0]["value_template"]
        assert f"state_attr('{select}', 'options')" in condizione, nome
        assert f"reject('equalto', '{voce}')" in condizione and "count > 0" in condizione, nome
        # Dismiss con lo stesso id: dopo il ripristino dell'ultima entità e nel ramo entità valida
        dismiss = _trova(passi, "persistent_notification.dismiss")
        assert len(dismiss) == 2, nome
        assert all(d["data"]["notification_id"] == nid for d, _ in dismiss), nome


def test_inizializzazione_spegne_gli_interruttori_prima_di_tutto():
    corpo = _script_inizializzazione()
    spegni = corpo.index("action: input_boolean.turn_off")
    assert spegni < corpo.index("action: script.vmc_master_azzera_booleans")
    for nome in ("pdr", "umidita", "calendario", "freeheating", "freecooling", "co2_e_voc"):
        voce = f"input_boolean.vmc_master_opzioni_accendi_spegni_vmc_vs_{nome}"
        assert spegni < corpo.index(voce) < corpo.index("action: script.vmc_master_azzera_booleans")


def test_verifica_entita_ripetuta_con_vmc_di_nuovo_on_line():
    """La verifica delle entita' del riavvio si ripete quando la VMC torna ON-Line (anche se al riavvio
    non era ancora in rete) e, se presente, quando si accende Invio Notifica."""
    import yaml

    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
    automazione = yaml.load((PKG / "vmc_master_automazione.txt").read_text(encoding="utf-8"), Loader=Loader)
    per_id = {str(t.get("id")): t for t in automazione["triggers"]}
    on_line = per_id["VMC Master Elenco Entità con VMC di nuovo ON-Line"]
    assert (on_line["trigger"], on_line["entity_id"], on_line["from"], on_line["to"]) == (
        "state", "sensor.vmc_master_status_ip_interfaccia", ["OFF-Line", "unavailable"], "ON-Line"
    )
    assert "for" not in on_line
    ids_aggiuntivi = ["VMC Master Elenco Entità con VMC di nuovo ON-Line"]
    if "VMC Master Elenco Entità con Invio Notifica acceso" in per_id:
        notifica = per_id["VMC Master Elenco Entità con Invio Notifica acceso"]
        assert (notifica["entity_id"], notifica["from"], notifica["to"]) == (
            "input_boolean.vmc_master_notifica_status_vmc", "off", "on"
        )
        ids_aggiuntivi.append("VMC Master Elenco Entità con Invio Notifica acceso")
    ramo = next(
        r for r in next(b for b in automazione["actions"] if "choose" in b)["choose"]
        if any("VMC Master Elenco Entità Temperatura e Umidità installate in H.A." in str(c.get("id")) for c in r["conditions"])
    )
    assert all(i in ramo["conditions"][0]["id"] for i in ids_aggiuntivi)
    assert ramo["sequence"][0]["action"] == "script.turn_on"
    assert len(ramo["sequence"][0]["target"]["entity_id"]) == 7
