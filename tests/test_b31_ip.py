"""Prove della 9.0.0b31 sull'IP della VMC.

Campo «Cambia IP VMC (Riavvio di H.A.)» della scheda: gli intervalli non ammessi si
rifiutano prima del riavvio con la stessa regola di ip_valido (sensore di verifica,
automazione e script Cambia IP), prima del riavvio il servizio verifica_ip controlla che
a quell'IP risponda la VMC, sotto il campo compare un avviso anche per l'IP non valido.
Finestre dell'integrazione: il nome si legge sempre con due prove.

Dalla b46 il campo, il servizio vmc_master.verifica_ip e la loro automazione non ci sono
più nella versione nativa (test_b46_ip.py): qui restano le prove del package della beta,
con un servizio finto."""

from __future__ import annotations

import re
import subprocess
from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from homeassistant.util.yaml import parse_yaml
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_fire_time_changed

from custom_components.vmc_master.config_flow import esito_verifica_ip, ip_valido
from custom_components.vmc_master.const import DOMAIN
from custom_components.vmc_master.installatore import genera_file
from custom_components.vmc_master.trasforma import per_vmc, rinomina
from tests.test_b30 import _conta_configurazione

CARTELLA = Path(__file__).parent.parent / "custom_components" / "vmc_master"
PKG = CARTELLA / "package"
NOME_VMC = "custom_components.vmc_master.config_flow.async_nome_vmc"
HASSIO = "custom_components.vmc_master.config_flow.is_hassio"
PI = "custom_components.vmc_master.prima_installazione"
IP = "192.168.1.51"
NUOVO_IP = "192.168.1.77"
ALTRO_IP = "192.168.1.78"
IP_ALTRA_VMC = "192.168.1.90"
CARTELLA_HA = "/config/packages/vmc_helty_flow/prova/"

# Intervalli non ammessi da ip_valido: 0.x.x.x, 127.x.x.x, 169.254.x.x, da 224.0.0.0 in su
NON_AMMESSI = [
    "0.0.0.0",
    "0.1.2.3",
    "127.0.0.1",
    "127.255.255.254",
    "169.254.0.1",
    "169.254.255.255",
    "224.0.0.0",
    "224.0.0.251",
    "239.255.255.255",
    "240.0.0.1",
    "255.255.255.254",
    "255.255.255.255",
]
AMMESSI = [
    "1.0.0.1",
    "8.8.8.8",
    "10.0.0.1",
    "126.255.255.255",
    "128.0.0.1",
    "169.253.255.255",
    "169.255.0.1",
    "172.16.250.9",
    "192.168.1.77",
    "223.255.255.255",
]
FORMATO_NON_VALIDO = [
    "abc",
    "192.168.1",
    "1.2.3.4.5",
    "192.168.1.010",
    "01.2.3.4",
    "192.168.1.256",
    "999.999.999.999",
    "1.2.3.-4",
    "1,2,3,4",
]
# Tutti i primi numeri, con i secondi vicini a 169.254
SPAZZATA = [f"{a}.{b}.1.2" for a in range(256) for b in (0, 253, 254, 255)]

# Stati del sensore di verifica con un avviso sotto il campo (oltre a «IP salvato...»)
AVVISI = {
    "IP già in uso": "IP già usato da un'altra VMC del Package",
    "IP già impostato": "Questo è già l'IP della VMC",
    "IP non Valido": (
        "IP non valido: quattro numeri da 0 a 255 separati da punti, senza zeri iniziali. "
        "Non sono ammessi 0.x.x.x, 127.x.x.x, 169.254.x.x e gli indirizzi da 224.x.x.x in su."
    ),
    "Verifica VMC in corso": "Verifica in corso: controllo che a questo IP risponda la VMC",
    "VMC non risponde": "La VMC non risponde a questo IP: non è stato cambiato nulla.",
    "Non è una VMC": "A questo IP risponde un apparecchio che non è una VMC",
    "Nome VMC diverso": "A questo IP risponde una VMC con un altro nome: non è stato cambiato nulla.",
}
STATI_SENZA_RIAVVIO = [*AVVISI, "Nessun IP", "unknown", "unavailable"]


@pytest.fixture(autouse=True)
def _nessuna_vmc_in_rete():
    """Nessuna VMC vera: i test che leggono il nome lo impostano da se'."""
    with patch(NOME_VMC, AsyncMock(return_value=None)):
        yield


@lru_cache(maxsize=1)
def _file() -> dict[str, str]:
    return genera_file("prova", IP, "9.0.0b31")


@lru_cache(maxsize=1)
def _package() -> dict:
    return parse_yaml(_file()["vmc_prova.yaml"])


def _testo(nome: str) -> str:
    with open(PKG / nome, encoding="utf-8", newline="") as f:
        return f.read()


def _sensore_verifica() -> str:
    return next(
        s["state"]
        for blocco in _package()["template"]
        for s in blocco.get("sensor", [])
        if s.get("unique_id") == "vmc_prova_verifica_ip_inserito"
    )


def _automazione() -> dict:
    return next(a for a in _package()["automation"] if a["id"] == "vmc_prova_cambio_ip_vmc")


# ------------------------------------------------------------------ stessa regola ovunque
def test_regola_di_ip_valido() -> None:
    for ip in NON_AMMESSI + FORMATO_NON_VALIDO + [""]:
        assert not ip_valido(ip), ip
    for ip in AMMESSI:
        assert ip_valido(ip), ip


async def test_variabile_ip_valido_dell_automazione(hass: HomeAssistant) -> None:
    modello = Template(_automazione()["actions"][0]["variables"]["ip_valido"], hass)
    for ip in NON_AMMESSI + AMMESSI + FORMATO_NON_VALIDO + SPAZZATA + [""]:
        assert modello.async_render({"ip": ip}) is ip_valido(ip), ip


async def test_sensore_di_verifica_rifiuta_gli_intervalli(hass: HomeAssistant) -> None:
    modello = Template(_sensore_verifica(), hass)
    hass.states.async_set("sensor.vmc_prova_ip", IP)
    for ip in NON_AMMESSI + AMMESSI + FORMATO_NON_VALIDO + SPAZZATA:
        hass.states.async_set("input_text.vmc_prova_ip_insert", ip)
        hass.states.async_set("input_text.vmc_prova_ip_insert_esito", f"ok {ip}")
        stato = modello.async_render(parse_result=False).strip()
        assert stato == (ip if ip_valido(ip) else "IP non Valido"), ip


@pytest.mark.parametrize(
    ("campo", "esito", "atteso"),
    [
        ("", "", "Nessun IP"),
        ("  ", "", "Nessun IP"),
        ("abc", "", "IP non Valido"),
        ("127.0.0.1", "ok 127.0.0.1", "IP non Valido"),
        (IP, f"ok {IP}", "IP già impostato"),
        (IP_ALTRA_VMC, f"ok {IP_ALTRA_VMC}", "IP già in uso"),
        (NUOVO_IP, "", "Verifica VMC in corso"),
        (NUOVO_IP, f"verifica {NUOVO_IP}", "Verifica VMC in corso"),
        # esito di un altro IP: non vale per questo
        (NUOVO_IP, f"non_risponde {ALTRO_IP}", "Verifica VMC in corso"),
        (NUOVO_IP, f"non_risponde {NUOVO_IP}", "VMC non risponde"),
        (NUOVO_IP, f"altro_dispositivo {NUOVO_IP}", "Non è una VMC"),
        (NUOVO_IP, f"nome_diverso {NUOVO_IP}", "Nome VMC diverso"),
        (f" {NUOVO_IP} ", f"ok {NUOVO_IP}", NUOVO_IP),
    ],
)
async def test_stati_del_sensore_di_verifica(
    hass: HomeAssistant, campo: str, esito: str, atteso: str
) -> None:
    hass.states.async_set("sensor.vmc_prova_ip", IP)
    hass.states.async_set("sensor.vmc_altra_ip", IP_ALTRA_VMC)
    hass.states.async_set("input_text.vmc_prova_ip_insert", campo)
    hass.states.async_set("input_text.vmc_prova_ip_insert_esito", esito)
    assert Template(_sensore_verifica(), hass).async_render(parse_result=False).strip() == atteso


def _sandbox_cambio_ip(tmp_path: Path) -> Path:
    for nome in ("vmc_prova.yaml", "vmc_prova_script_cambio_nome.sh", "vmc_prova_script_cambio_ip.sh"):
        with open(tmp_path / nome, "w", encoding="utf-8", newline="") as f:
            f.write(_file()[nome].replace(CARTELLA_HA, f"{tmp_path}/"))
    return tmp_path


@pytest.mark.parametrize("valore", NON_AMMESSI)
def test_script_cambio_ip_rifiuta_gli_intervalli(tmp_path: Path, valore: str) -> None:
    cartella = _sandbox_cambio_ip(tmp_path)
    prima = {p.name: p.read_bytes() for p in cartella.iterdir()}
    esito = subprocess.run(
        ["bash", str(cartella / "vmc_prova_script_cambio_ip.sh"), valore],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert esito.returncode == 1
    assert esito.stdout == f"Indirizzo IP non valido: '{valore}'\n"
    assert {p.name: p.read_bytes() for p in cartella.iterdir()} == prima


def test_controllo_dello_script_uguale_a_ip_valido() -> None:
    """Le righe di controllo dello script, provate in un solo bash su tutti gli IP."""
    script = _file()["vmc_prova_script_cambio_ip.sh"]
    righe = script.splitlines()
    inizio = next(i for i, r in enumerate(righe) if r.startswith("OTTETTO="))
    fine = next(i for i, r in enumerate(righe) if r.startswith("(( A != 0"))
    controllo = "\n".join(righe[inizio : fine + 1])
    programma = (
        'while IFS= read -r ip; do\n'
        f'  ( set -- "$ip"; IP="$1"\n{controllo}\n  echo "SI $ip" ) >/dev/null && echo "SI $ip" || echo "NO $ip"\n'
        "done\n"
    )
    ips = NON_AMMESSI + AMMESSI + FORMATO_NON_VALIDO + SPAZZATA
    esito = subprocess.run(
        ["bash", "-c", programma], input="\n".join(ips) + "\n", capture_output=True, text=True, timeout=120, check=True
    )
    accettati = {riga[3:] for riga in esito.stdout.splitlines() if riga.startswith("SI ")}
    assert accettati == {ip for ip in ips if ip_valido(ip)}
    assert len(esito.stdout.splitlines()) == len(ips)


def test_versione_dello_script() -> None:
    righe = _testo("vmc_master_script_cambio_ip.sh").split("\n")
    assert "SCRIPT CAMBIO IP VMC HELTY FLOW PLUS RELEASE [VER. 9.0.0b31]" in righe[2]
    assert len(righe[2]) == len(righe[3]) and righe[2].endswith("#")


# ------------------------------------------------------------------ campo e avvisi della scheda
def test_campo_ip_al_massimo_15_caratteri_senza_pattern() -> None:
    campi = _package()["input_text"]
    assert campi["vmc_prova_ip_insert"]["max"] == 15
    assert "pattern" not in campi["vmc_prova_ip_insert"]
    assert campi["vmc_prova_ip_insert_esito"] == {
        "name": "Esito Verifica VMC al Nuovo IP",
        "initial": "",
        "icon": "mdi:ip-network-outline",
    }


def _righe_del_sensore(nodo: object) -> list[dict]:
    """Righe condizionali della scheda che dipendono dal sensore di verifica."""
    righe: list[dict] = []
    if isinstance(nodo, dict):
        condizioni = nodo.get("conditions") if nodo.get("type") == "conditional" else None
        if condizioni and condizioni[0].get("entity") == "sensor.vmc_master_verifica_ip_inserito":
            righe.append(nodo)
        for valore in nodo.values():
            righe += _righe_del_sensore(valore)
    elif isinstance(nodo, list):
        for valore in nodo:
            righe += _righe_del_sensore(valore)
    return righe


def test_avvisi_sotto_il_campo_nelle_tre_copie() -> None:
    scheda = _testo("vmc_master_scheda_manuale_interfaccia.txt")
    righe = _righe_del_sensore(parse_yaml(scheda))
    # tre copie del campo: «IP salvato...» e un avviso per ogni stato senza riavvio
    assert len(righe) == 3 * (1 + len(AVVISI))
    for stato, testo in AVVISI.items():
        etichette = [r["row"]["label"] for r in righe if r["conditions"][0].get("state") == stato]
        assert len(etichette) == 3 and all(e.startswith(testo) for e in etichette), stato
    salvato = [r for r in righe if "state_not" in r["conditions"][0]]
    assert len(salvato) == 3
    for riga in salvato:
        # «IP salvato...» solo con un IP verificato: tutti gli altri stati sono esclusi
        assert sorted(riga["conditions"][0]["state_not"]) == sorted(STATI_SENZA_RIAVVIO)
        assert riga["row"]["label"].startswith("IP salvato. Home Assistant si sta riavviando")
    # nessun IP intero nei testi: per le altre VMC per_vmc sostituisce ogni IP con il loro
    for nome, ip in (("master", IP), ("soggiorno", "192.168.1.161")):
        generata = per_vmc(scheda, nome, ip)
        assert generata.count(AVVISI["IP non Valido"]) == 3
        assert re.sub(r"\s+", " ", generata).count("224.x.x.x in su") == 4  # tre avvisi e la Nota


def test_nota_cambia_ip_vmc() -> None:
    scheda = re.sub(r"\s+", " ", _testo("vmc_master_scheda_manuale_interfaccia.txt"))
    inizio = scheda.index("<strong>Nota Cambia IP VMC (Riavvio di H.A.)</strong>")
    nota = scheda[inizio : scheda.index("<br>", inizio)]
    assert "Non sono ammessi 0.x.x.x, 127.x.x.x, 169.254.x.x e gli indirizzi da 224.x.x.x in su." in nota
    assert "controlla che a quell'IP risponda la VMC con il suo nome" in nota
    assert "Questo controllo vede solo le VMC già attive" in nota
    assert "«Cambia l'IP della VMC»" in nota
    assert "un IP non valido viene cancellato" not in nota
    assert not re.search(r"\b(sala|camera|cucina)\b", nota, re.IGNORECASE)


def test_richiami_del_campo_di_esito() -> None:
    entita = "input_text.vmc_master_ip_insert_esito"
    modello = re.compile(re.escape(entita) + r"(?![A-Za-z0-9_])")
    commento = re.search(r"\n  vmc_master_ip_insert_esito: +# (.+)", _testo("vmc_master.yaml")).group(1)
    assert commento.startswith(
        f"[CONFIGURAZIONE, {_conta_configurazione(entita)} RICHIAMI] "
        f"[INTERFACCIA, {len(modello.findall(_testo('vmc_master_scheda_manuale_interfaccia.txt')))} RICHIAMO] "
        f"[AUTOMAZIONE, {len(modello.findall(_testo('vmc_master_automazione.txt')))} RICHIAMI]"
    )
    pacchetto = _testo("vmc_master.yaml")
    escluse = pacchetto[pacchetto.index("&vmc_master_entita_escluse_recorder") :]
    assert f"- {entita}\r\n" in escluse[: escluse.index("\r\n\r\n")]
    assert f"'{entita}'," in _testo("vmc_master_scheda_manuale_interfaccia.txt")


def test_descrizione_dell_automazione() -> None:
    descrizione = next(
        a for a in parse_yaml(_testo("vmc_master.yaml"))["automation"] if a["id"] == "vmc_master_cambio_ip_vmc"
    )["description"]
    assert "master" not in descrizione and "vmc_master_clona_" not in descrizione
    assert not re.search(r"\b[a-z_]+\.vmc_", descrizione)
    assert not re.search(r"[0-9]+\.[0-9]+", descrizione)
    assert "svuota il campo" not in descrizione


# ------------------------------------------------- servizio verifica_ip nel package della beta
def test_servizio_protetto_da_per_vmc() -> None:
    assert rinomina("action: vmc_master.verifica_ip", "soggiorno") == "action: vmc_master.verifica_ip"
    for nome, ip in (("master", IP), ("soggiorno", "192.168.1.161")):
        pacchetto = genera_file(nome, ip, "9.0.0b31")[f"vmc_{nome}.yaml"]
        assert re.findall(r"action: (vmc_[a-z]+\.verifica_ip)", pacchetto) == ["vmc_master.verifica_ip"]
        assert f"entity_id: input_text.vmc_{nome}_ip_insert_esito" in pacchetto
        assert f"states('sensor.vmc_{nome}_nome_status')" in pacchetto
        # nessun IP intero nel package oltre a quello della VMC (lo script Cambia IP li cambia tutti)
        assert set(re.findall(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", pacchetto)) == {ip}


def test_esito_verifica_ip() -> None:
    assert esito_verifica_ip(None, "Prova") == "non_risponde"
    assert esito_verifica_ip("", "") == "altro_dispositivo"
    assert esito_verifica_ip("VMC Prova", "VMC-prova") == "ok"
    assert esito_verifica_ip("Prova", "VMC Prova") == "ok"
    assert esito_verifica_ip("VMC Altra", "VMC Prova") == "nome_diverso"
    assert esito_verifica_ip("VMC Altra", "  ") == "ok"
    # nome senza parole: titolo_voce usa il nome interno, come l'ingranaggio
    assert esito_verifica_ip("-", "VMC prova", "prova") == "ok"


# ------------------------------------------------------------------ automazione Cambio IP
class _Servizi:
    """Servizi finti dell'automazione: verifica_ip, i due shell_command e il riavvio."""

    def __init__(self, hass: HomeAssistant, esiti: dict[str, str], cambia_campo: str | None = None) -> None:
        self.hass, self.esiti, self.cambia_campo = hass, esiti, cambia_campo
        self.verifiche: list[dict] = []
        self.comandi: list[str] = []
        self.riavvii = 0

    async def verifica_ip(self, chiamata: ServiceCall) -> dict:
        self.verifiche.append(dict(chiamata.data))
        if self.cambia_campo and len(self.verifiche) == 1:
            # l'utente scrive un altro IP mentre la VMC viene verificata
            await self.hass.services.async_call(
                "input_text",
                "set_value",
                {"entity_id": "input_text.vmc_prova_ip_insert", "value": self.cambia_campo},
                blocking=True,
            )
        esito = self.esiti[chiamata.data["ip"]]
        return {"risponde": esito != "non_risponde", "nome": "", "esito": esito}

    async def comando(self, chiamata: ServiceCall) -> None:
        self.comandi.append(chiamata.service)

    async def riavvio(self, _chiamata: ServiceCall) -> None:
        self.riavvii += 1


async def _prepara(hass: HomeAssistant, servizi: _Servizi, nome_vmc: str = "Prova") -> None:
    campi = {nome: _package()["input_text"][nome] for nome in ("vmc_prova_ip_insert", "vmc_prova_ip_insert_esito")}
    assert await async_setup_component(hass, "input_text", {"input_text": campi})
    hass.states.async_set("sensor.vmc_prova_ip", IP)
    hass.states.async_set("sensor.vmc_altra_ip", IP_ALTRA_VMC)
    hass.states.async_set("sensor.vmc_prova_nome_status", nome_vmc)
    hass.services.async_register(DOMAIN, "verifica_ip", servizi.verifica_ip, supports_response=SupportsResponse.ONLY)
    for nome in ("vmc_prova_rimuovi_caratteri_di_ritorno", "vmc_prova_aggiorna_indirizzo_ip"):
        hass.services.async_register("shell_command", nome, servizi.comando)
    hass.services.async_register("homeassistant", "restart", servizi.riavvio)
    assert await async_setup_component(hass, "automation", {"automation": [_automazione()]})
    await hass.async_block_till_done()


async def _scrivi(hass: HomeAssistant, valore: str) -> None:
    await hass.services.async_call(
        "input_text", "set_value", {"entity_id": "input_text.vmc_prova_ip_insert", "value": valore}, blocking=True
    )
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=3))
    await hass.async_block_till_done()


@pytest.mark.parametrize("valore", [*NON_AMMESSI[:4], "224.0.0.1", "abc", "192.168.1.010", IP, IP_ALTRA_VMC])
async def test_automazione_rifiuta_senza_verifica_ne_riavvio(hass: HomeAssistant, valore: str) -> None:
    servizi = _Servizi(hass, {})
    await _prepara(hass, servizi)
    await _scrivi(hass, valore)
    assert servizi.verifiche == [] and servizi.comandi == [] and servizi.riavvii == 0
    # il campo resta com'e': sotto il campo compare l'avviso
    assert hass.states.get("input_text.vmc_prova_ip_insert").state == valore
    assert hass.states.get("input_text.vmc_prova_ip_insert_esito").state == ""


@pytest.mark.parametrize("esito", ["non_risponde", "altro_dispositivo", "nome_diverso"])
async def test_automazione_senza_la_vmc_attesa_non_riavvia(hass: HomeAssistant, esito: str) -> None:
    servizi = _Servizi(hass, {NUOVO_IP: esito})
    await _prepara(hass, servizi)
    await _scrivi(hass, NUOVO_IP)
    assert servizi.verifiche == [{"ip": NUOVO_IP, "nome": "Prova"}]
    assert servizi.comandi == [] and servizi.riavvii == 0
    assert hass.states.get("input_text.vmc_prova_ip_insert_esito").state == f"{esito} {NUOVO_IP}"
    assert hass.states.get("input_text.vmc_prova_ip_insert").state == NUOVO_IP


@pytest.mark.parametrize(("nome_vmc", "nome_passato"), [("Prova", "Prova"), ("Non disponibile", ""), ("unavailable", "")])
async def test_automazione_con_la_vmc_attesa_riavvia(
    hass: HomeAssistant, nome_vmc: str, nome_passato: str
) -> None:
    servizi = _Servizi(hass, {NUOVO_IP: "ok"})
    await _prepara(hass, servizi, nome_vmc)
    await _scrivi(hass, NUOVO_IP)
    assert servizi.verifiche == [{"ip": NUOVO_IP, "nome": nome_passato}]
    assert servizi.comandi == ["vmc_prova_rimuovi_caratteri_di_ritorno", "vmc_prova_aggiorna_indirizzo_ip"]
    assert servizi.riavvii == 1
    assert hass.states.get("input_text.vmc_prova_ip_insert_esito").state == f"ok {NUOVO_IP}"


async def test_automazione_ip_cambiato_durante_la_verifica(hass: HomeAssistant) -> None:
    """Un IP scritto durante la verifica aspetta in coda: il primo non si salva."""
    servizi = _Servizi(hass, {NUOVO_IP: "ok", ALTRO_IP: "non_risponde"}, cambia_campo=ALTRO_IP)
    await _prepara(hass, servizi)
    await _scrivi(hass, NUOVO_IP)
    assert [v["ip"] for v in servizi.verifiche] == [NUOVO_IP, ALTRO_IP]
    assert servizi.comandi == [] and servizi.riavvii == 0
    assert hass.states.get("input_text.vmc_prova_ip_insert_esito").state == f"non_risponde {ALTRO_IP}"


# ------------------------------------------------------------------ finestre: due prove
async def test_in_rete_legge_il_nome_con_una_seconda_prova(hass: HomeAssistant) -> None:
    risultato = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {"next_step_id": "in_rete"})
    with patch(NOME_VMC, AsyncMock(side_effect=[None, "VMC Soggiorno", None])) as lettura:
        risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {"host": NUOVO_IP})
        await hass.async_block_till_done()
    # due letture della finestra (la terza e' il titolo della voce letto dopo l'avvio)
    assert [c.args for c in lettura.await_args_list[:2]] == [(NUOVO_IP,)] * 2
    # prima VMC («master»): con il nome letto alla seconda prova non chiede «non raggiungibile»
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    assert risultato["title"] == "VMC Soggiorno"


async def test_ip_fisso_senza_mac_legge_il_nome_con_una_seconda_prova(hass: HomeAssistant) -> None:
    MockConfigEntry(domain=DOMAIN, unique_id="master", data={"nome": "master", "host": "192.168.1.160"}).add_to_hass(
        hass
    )
    collegata = {"ap_ssid": "VMC_12345678", "ip": "192.168.1.50", "name": "VMC Bagno", "mac": ""}
    motore = MagicMock()
    with (
        patch(HASSIO, return_value=True),
        patch(f"{PI}.esegui", motore),
        patch(f"{PI}.ultima_vmc", return_value=dict(collegata)),
    ):
        risultato = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
        risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {"next_step_id": "riprendi"})
        assert risultato["step_id"] == "ip_fisso"
        with patch(NOME_VMC, AsyncMock(side_effect=[None, "VMC Bagno"])) as lettura:
            risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {"host": "192.168.1.60"})
        assert lettura.await_count == 2
        assert risultato["step_id"] == "nome"
        # nessuna risposta nemmeno alla seconda prova: lo dice la finestra
        risultato = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
        risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {"next_step_id": "riprendi"})
        with patch(NOME_VMC, AsyncMock(side_effect=[None, None])) as lettura:
            risultato = await hass.config_entries.flow.async_configure(risultato["flow_id"], {"host": "192.168.1.60"})
        assert lettura.await_count == 2
        assert risultato["errors"] == {"host": "ip_non_risponde_riavvia"}
    motore.assert_not_called()


async def test_cambia_ip_seconda_prova_e_nome_mai_letto(hass: HomeAssistant) -> None:
    """Ingranaggio: stesse due prove; con il nome della VMC mai letto («VMC ‹nome›») non
    c'e' nulla con cui confrontare e si salva subito."""
    voce = MockConfigEntry(
        domain=DOMAIN, unique_id="zona", title="VMC zona",
        data={"nome": "zona", "host": "192.168.1.161", "titolo": "VMC zona"},
    )
    voce.add_to_hass(hass)
    assert await hass.config_entries.async_setup(voce.entry_id)
    await hass.async_block_till_done()
    risultato = await hass.config_entries.options.async_init(voce.entry_id)
    risultato = await hass.config_entries.options.async_configure(risultato["flow_id"], {"next_step_id": "cambia_ip"})
    with patch(NOME_VMC, AsyncMock(side_effect=[None, "VMC Zona Notte"])) as lettura:
        risultato = await hass.config_entries.options.async_configure(risultato["flow_id"], {"host": "192.168.1.170"})
    # due prove della finestra, poi la VMC riparte con il nuovo IP e rilegge il nome per
    # il titolo (la terza lettura, senza risposta: il titolo resta)
    assert lettura.await_count == 3
    assert risultato["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert voce.data["host"] == "192.168.1.170"
