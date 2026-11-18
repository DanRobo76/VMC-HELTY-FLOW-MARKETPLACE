"""Prove della 9.0.0b22 sul package: Cambia IP e Cambia Nome dalla scheda, sensore LAN,
temperatura negativa con un solo carattere, spia dell'audio all'avvio."""

from __future__ import annotations

import os
import shlex
import subprocess
from datetime import timedelta
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.template import Template
from homeassistant.setup import async_setup_component
from homeassistant.util import dt as dt_util
from homeassistant.util.yaml import parse_yaml
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.vmc_master.installatore import genera_file

IP = "192.168.1.51"
NUOVO_IP = "192.168.1.77"
CARTELLA_HA = "/config/packages/vmc_helty_flow/prova/"

# Valori che il controllo dell'automazione rifiuta e che non devono arrivare ai comandi sed.
# Il primo è il caso dell'audit: un IP valido su una riga e comandi sed sulle righe dopo.
IP_RIFIUTATI = [
    "192.168.1.77\n1e touch /tmp/iniettato",
    "1.2.3.4\nfoo",
    "1.2.3.4/;w /tmp/scritto\n1.2.3.4",
    "999.999.999.999",
    "192.168.1.010",
    "192.168.1.256",
    "192.168.1.5 ",
    " 192.168.1.5",
    "192.168.1",
    "",
]
IP_ACCETTATI = ["192.168.1.77", "10.0.0.1", "0.0.0.0", "255.255.255.255", "172.16.250.9"]


def _file_prova() -> dict[str, str]:
    return genera_file("prova", IP, "9.0.0b22")


def _package_prova() -> dict:
    return parse_yaml(_file_prova()["vmc_prova.yaml"])


# ---------------------------------------------------------------- A-1: script Cambia IP


def _sandbox_cambio_ip(tmp_path: Path) -> Path:
    """Script Cambia IP e file della VMC «prova» in una cartella temporanea."""
    file = _file_prova()
    for nome in ("vmc_prova.yaml", "vmc_prova_script_cambio_nome.sh", "vmc_prova_script_cambio_ip.sh"):
        testo = file[nome].replace(CARTELLA_HA, f"{tmp_path}/")
        with open(tmp_path / nome, "w", encoding="utf-8", newline="") as f:
            f.write(testo)
    return tmp_path


def _esegui_cambio_ip(cartella: Path, *argomenti: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(cartella / "vmc_prova_script_cambio_ip.sh"), *argomenti],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def test_vecchio_controllo_riga_per_riga_accettava_piu_righe() -> None:
    """Il controllo della b21 (grep riga per riga) accettava un IP valido seguito da altre righe."""
    vecchio = r"""echo "$1" | grep -Eq '^[0-9]{1,3}(\.[0-9]{1,3}){3}$'"""
    esito = subprocess.run(["bash", "-c", vecchio, "x", IP_RIFIUTATI[0]], check=False)
    assert esito.returncode == 0


@pytest.mark.parametrize("valore", IP_RIFIUTATI)
def test_script_cambio_ip_rifiuta_e_non_tocca_i_file(tmp_path: Path, valore: str) -> None:
    cartella = _sandbox_cambio_ip(tmp_path)
    prima = {p.name: p.read_bytes() for p in cartella.iterdir()}
    # come lo passa lo shell_command dopo il rendering: shlex.split di un valore tra apici
    argomenti = shlex.split(shlex.quote(valore)) if valore else []
    esito = _esegui_cambio_ip(cartella, *argomenti)
    assert esito.returncode == 1
    assert "Indirizzo IP non valido" in esito.stdout
    assert {p.name: p.read_bytes() for p in cartella.iterdir()} == prima


def test_script_cambio_ip_rifiuta_due_argomenti(tmp_path: Path) -> None:
    cartella = _sandbox_cambio_ip(tmp_path)
    prima = (cartella / "vmc_prova.yaml").read_bytes()
    assert _esegui_cambio_ip(cartella, NUOVO_IP, NUOVO_IP).returncode == 1
    assert (cartella / "vmc_prova.yaml").read_bytes() == prima


@pytest.mark.parametrize("valore", IP_ACCETTATI)
def test_script_cambio_ip_accetta_ip_validi(tmp_path: Path, valore: str) -> None:
    """Un IP valido cambia l'IP nel package e dopo «nc -w 3» nello script Cambia Nome."""
    cartella = _sandbox_cambio_ip(tmp_path)
    yaml_prima = (cartella / "vmc_prova.yaml").read_text(encoding="utf-8")
    esito = _esegui_cambio_ip(cartella, valore)
    assert esito.returncode == 0, esito.stdout + esito.stderr
    yaml_dopo = (cartella / "vmc_prova.yaml").read_text(encoding="utf-8")
    assert yaml_dopo == yaml_prima.replace(IP, valore)
    assert yaml_prima.count(IP) > 10
    nome = (cartella / "vmc_prova_script_cambio_nome.sh").read_text(encoding="utf-8")
    assert nome.endswith(f"timeout 5 nc -w 3 {valore} 5001")


def test_shell_command_riceve_l_ip_dall_automazione() -> None:
    """Lo shell_command usa la variabile «ip» passata dall'automazione, non rilegge il campo."""
    package = _package_prova()
    comando = package["shell_command"]["vmc_prova_aggiorna_indirizzo_ip"]
    assert "input_text" not in comando
    assert comando.endswith("vmc_prova_script_cambio_ip.sh   {{ ip | default('') }}")
    automazione = next(a for a in package["automation"] if a["id"] == "vmc_prova_cambio_ip_vmc")
    passi = automazione["actions"][1]["choose"][0]["sequence"]
    chiamata = next(p for p in passi if p.get("action") == "shell_command.vmc_prova_aggiorna_indirizzo_ip")
    assert chiamata["data"] == {"ip": "{{ ip }}"}


async def test_automazione_cambio_ip_passa_l_ip_controllato(hass: HomeAssistant, tmp_path: Path) -> None:
    """Corsa dell'audit resa certa: il campo cambia dopo il controllo e prima dello script.
    Allo script arriva comunque l'IP controllato, come unico argomento."""
    package = _package_prova()
    registro = tmp_path / "argomenti.txt"
    spia = tmp_path / "spia.sh"
    spia.write_text(f'#!/bin/bash\nprintf "%s\\n" "$#" "$@" > {registro}\n', encoding="utf-8")
    spia.chmod(0o755)
    comando = package["shell_command"]["vmc_prova_aggiorna_indirizzo_ip"]
    comando = f"{spia} " + comando.split("   ", 1)[1]

    assert await async_setup_component(
        hass, "input_text", {"input_text": {"vmc_prova_ip_insert": package["input_text"]["vmc_prova_ip_insert"]}}
    )
    assert await async_setup_component(
        hass, "shell_command", {"shell_command": {"vmc_prova_aggiorna_indirizzo_ip": comando}}
    )
    hass.states.async_set("sensor.vmc_prova_ip", IP)
    riavvii: list[ServiceCall] = []

    async def _cambia_il_campo(call: ServiceCall) -> None:
        await hass.services.async_call(
            "input_text",
            "set_value",
            {"entity_id": "input_text.vmc_prova_ip_insert", "value": "1.2.3.4\nfoo"},
            blocking=True,
        )

    async def _riavvio(call: ServiceCall) -> None:
        riavvii.append(call)

    hass.services.async_register("shell_command", "vmc_prova_rimuovi_caratteri_di_ritorno", _cambia_il_campo)
    hass.services.async_register("homeassistant", "restart", _riavvio)
    automazione = next(a for a in package["automation"] if a["id"] == "vmc_prova_cambio_ip_vmc")
    assert await async_setup_component(hass, "automation", {"automation": [automazione]})
    await hass.async_block_till_done()

    await hass.services.async_call(
        "input_text",
        "set_value",
        {"entity_id": "input_text.vmc_prova_ip_insert", "value": NUOVO_IP},
        blocking=True,
    )
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=3))
    await hass.async_block_till_done()

    assert registro.read_text(encoding="utf-8").splitlines() == ["1", NUOVO_IP]
    assert len(riavvii) == 1


# ---------------------------------------------------------------- B-7: Cambia Nome


def _sandbox_cambio_nome(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    """Script Cambia Nome con un «nc» finto che registra argomenti e testo ricevuto."""
    bin_finto = tmp_path / "bin"
    bin_finto.mkdir()
    ricevuto = tmp_path / "ricevuto.txt"
    nc = bin_finto / "nc"
    nc.write_text(f'#!/bin/bash\n{{ echo "$*"; cat; }} > {ricevuto}\n', encoding="utf-8")
    nc.chmod(0o755)
    script = tmp_path / "vmc_prova_script_cambio_nome.sh"
    with open(script, "w", encoding="utf-8", newline="") as f:
        f.write(_file_prova()["vmc_prova_script_cambio_nome.sh"])
    ambiente = dict(os.environ, PATH=f"{bin_finto}:{os.environ['PATH']}")
    return script, ricevuto, ambiente


@pytest.mark.parametrize("nome", ["Prova", "VMC_2", "a-b", "ABCDEFGHIJ", "x"])
def test_script_cambio_nome_invia_i_nomi_validi(tmp_path: Path, nome: str) -> None:
    script, ricevuto, ambiente = _sandbox_cambio_nome(tmp_path)
    esito = subprocess.run(["bash", str(script), nome], env=ambiente, capture_output=True, text=True, check=False)
    assert esito.returncode == 0, esito.stdout + esito.stderr
    assert ricevuto.read_text(encoding="utf-8") == f"-w 3 {IP} 5001\nVMNM {nome}\n"


@pytest.mark.parametrize("nome", ["Cucinà", "a b", "ab\\", "a*b", "ABCDEFGHIJK", "", "a\nb", "a;b"])
def test_script_cambio_nome_rifiuta_i_nomi_non_validi(tmp_path: Path, nome: str) -> None:
    script, ricevuto, ambiente = _sandbox_cambio_nome(tmp_path)
    esito = subprocess.run(["bash", str(script), nome], env=ambiente, capture_output=True, text=True, check=False)
    assert esito.returncode == 1
    assert "Nome non valido" in esito.stdout
    assert not ricevuto.exists()


def test_script_cambio_nome_usa_nc_con_attesa_massima() -> None:
    testo = _file_prova()["vmc_prova_script_cambio_nome.sh"]
    assert testo.splitlines()[-1] == f'echo "VMNM $NOME" | timeout 5 nc -w 3 {IP} 5001'


async def test_shell_command_cambia_nome_toglie_la_barra_rovesciata(hass: HomeAssistant) -> None:
    """Un nome che finisce con «\\» non fa più fallire shlex (No closing quotation)."""
    comando = _package_prova()["shell_command"]["vmc_prova_cambia_nome"]
    argomenti = comando.split(" ", 2)[2]
    for valore, atteso in (("ab\\", "ab"), ('a"b', "ab"), ("Prova", "Prova"), ("L'aria", "L'aria")):
        hass.states.async_set("input_text.vmc_prova_nome_da_inserire", valore)
        reso = Template(argomenti, hass).async_render(parse_result=False)
        assert shlex.split(reso) == [atteso]


def test_campo_e_automazione_accettano_solo_nomi_validi() -> None:
    file = _file_prova()
    campo = parse_yaml(file["vmc_prova.yaml"])["input_text"]["vmc_prova_nome_da_inserire"]
    assert campo["pattern"] == "^[A-Za-z0-9_-]{0,10}$"
    assert campo["max"] == 10
    automazione = file["vmc_prova_automazione.yaml"]
    assert automazione.count(
        "states('input_text.vmc_prova_nome_da_inserire') is match('^[A-Za-z0-9_-]{1,10}$')"
    ) == 2
    assert "states('input_text.vmc_prova_nome_da_inserire') != ''" not in automazione


async def test_condizione_rinomina_con_nomi_validi_e_non_validi(hass: HomeAssistant) -> None:
    condizione = "{{ states('input_text.vmc_prova_nome_da_inserire') is match('^[A-Za-z0-9_-]{1,10}$') }}"
    for valore, atteso in (("Prova", True), ("a-b_9", True), ("", False), ("Cucinà", False), ("a b", False), ("ab\\", False)):
        hass.states.async_set("input_text.vmc_prova_nome_da_inserire", valore)
        assert Template(condizione, hass).async_render() is atteso, valore


# ---------------------------------------------------------------- M-2: sensore LAN

VMSL = (
    "VMSL "
    + "CasaWiFi".ljust(32, "*")
    + "Segreta123".ljust(32, "*")
    + "192.168.200.001"
    + "05001"
    + "192.168.200.254"
    + "255.255.255.000"
    + "10"
)


def _template_lan() -> str:
    sensore = next(s for s in _package_prova()["sensor"] if s.get("name") == "vmc_prova_lan")
    assert sensore["payload"] == "VMSL?"
    assert sensore["scan_interval"] == {"seconds": 57641}
    return sensore["value_template"]


async def test_sensore_lan_nasconde_la_password(hass: HomeAssistant) -> None:
    template = Template(_template_lan(), hass)
    reso = template.async_render({"value": VMSL + "\r\n"}, parse_result=False)
    assert "Segreta123" not in reso
    assert reso == VMSL[:37] + "*" * 32 + VMSL[69:]
    assert len(reso) == len(VMSL)
    # SSID, IP, porta, gateway, maschera e modalità restano
    assert reso.startswith("VMSL CasaWiFi****")
    assert reso.endswith("192.168.200.00105001192.168.200.254255.255.255.00010")


async def test_sensore_lan_risposte_brevi_o_diverse(hass: HomeAssistant) -> None:
    template = Template(_template_lan(), hass)
    # risposta troncata dentro la password: nessun carattere della password resta
    troncata = VMSL[:45]
    assert template.async_render({"value": troncata}, parse_result=False) == VMSL[:37] + "*" * 8
    # risposta che non è VMSL: resta com'è
    assert template.async_render({"value": "ERRORE"}, parse_result=False) == "ERRORE"
    assert template.async_render({"value": "VMSL CasaWiFi"}, parse_result=False) == "VMSL CasaWiFi"


# ---------------------------------------------------------------- B-10: temperatura «1»


@pytest.mark.parametrize(
    ("chiave", "indice"),
    [("temp_esterna", 2), ("temp_interna", 1)],
)
async def test_temperatura_con_un_solo_carattere(hass: HomeAssistant, chiave: str, indice: int) -> None:
    package = _package_prova()
    entita = f"sensor.vmc_prova_{chiave}_status_senza_offset"
    sensore = next(
        s
        for blocco in package["template"]
        for s in blocco.get("sensor", [])
        if s.get("default_entity_id") == entita
    )
    template = Template(sensore["state"], hass)
    casi = [
        ("00215", "positivo", "21.5"),
        ("10215", "negativo", "-21.5"),
        ("00000", "positivo", "0.0"),
        ("10005", "negativo", "-0.5"),
        ("1", "positivo", "0.1"),
        ("1", "negativo", "Non disponibile"),
        ("abc", "positivo", "Non disponibile"),
        ("", "negativo", "Non disponibile"),
    ]
    for grezzo, segno, atteso in casi:
        campi = ["VMGI", "00200", "00100", "500"]
        campi[indice] = grezzo
        hass.states.async_set("sensor.vmc_prova_sensori_memorizzata", ",".join(campi))
        hass.states.async_set(f"sensor.vmc_prova_{chiave}_positivo_negativo", segno)
        assert template.async_render(parse_result=False).strip() == atteso, (grezzo, segno)


# ---------------------------------------------------------------- B-11: spia dell'audio all'avvio

SPIA = "input_boolean.vmc_prova_avvio_home_assistant_in_corso_per_audio"


async def _prepara_riepilogo(hass: HomeAssistant, audio: bool) -> None:
    package = _package_prova()
    booleani = {
        nome: {} for nome in (
            "vmc_prova_avvio_home_assistant_in_corso_per_audio",
            "vmc_prova_notifica_audio",
            "vmc_prova_notifica_allerta_riepilogo",
        )
    }
    assert await async_setup_component(hass, "input_boolean", {"input_boolean": booleani})
    automazione = next(a for a in package["automation"] if a["id"] == "vmc_prova_riepilogo_audio_avvio")
    assert await async_setup_component(hass, "automation", {"automation": [automazione]})
    await hass.async_block_till_done()
    for nome in ("vmc_prova_notifica_audio", "vmc_prova_notifica_allerta_riepilogo"):
        await hass.services.async_call(
            "input_boolean", "turn_on" if audio else "turn_off", {"entity_id": f"input_boolean.{nome}"}, blocking=True
        )


@pytest.mark.parametrize("audio", [True, False])
async def test_spia_avvio_spenta_dopo_10_minuti(hass: HomeAssistant, audio: bool) -> None:
    """Riepilogo interrotto (per esempio senza TTS): la spia non resta accesa."""
    await _prepara_riepilogo(hass, audio)
    await hass.services.async_call("input_boolean", "turn_on", {"entity_id": SPIA}, blocking=True)
    adesso = dt_util.utcnow()
    async_fire_time_changed(hass, adesso + timedelta(minutes=9, seconds=59))
    await hass.async_block_till_done()
    assert hass.states.get(SPIA).state == "on"
    async_fire_time_changed(hass, adesso + timedelta(minutes=10, seconds=1))
    await hass.async_block_till_done()
    assert hass.states.get(SPIA).state == "off"


def test_riepilogo_normale_invariato() -> None:
    """Il riepilogo all'avvio fa gli stessi passi di prima, dopo il ramo della spia."""
    package = _package_prova()
    automazione = next(a for a in package["automation"] if a["id"] == "vmc_prova_riepilogo_audio_avvio")
    assert automazione["mode"] == "queued"
    assert automazione["triggers"][0] == {"trigger": "homeassistant", "event": "start"}
    assert automazione["triggers"][1]["for"] == "00:10:00"
    azioni = automazione["actions"]
    assert azioni[0]["then"][-1] == {"stop": "Spia dell'audio all'avvio spenta"}
    assert azioni[1] == {"action": "input_boolean.turn_on", "target": {"entity_id": SPIA}}
    assert azioni[2] == {"delay": "00:00:10"}
    assert azioni[-1] == {"action": "input_boolean.turn_off", "target": {"entity_id": SPIA}}
