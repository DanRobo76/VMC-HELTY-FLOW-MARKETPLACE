"""Copertura al 100 %: motore Wi-Fi (riga di comando della 8.6.0), installatore e prepara.

Solo test, nessuna modifica al codice dell'integrazione. Le parti del motore provate qui
sono quelle che la Finestra Prima Installazione VMC della release 8.6.0 usa dalla riga di
comando (rinomina, cambio password della rete VMC, Access Point, avvio del worker, stato).
Il motore resta identico alla copia dentro package/vmc_master.yaml. Supervisor, VMC,
socket, segnali e processi sono finti: nessun hardware e nessun processo reale.
"""

from __future__ import annotations

import fcntl
import json
import os
from pathlib import Path
import runpy
import socket
import sys
from types import SimpleNamespace
from unittest.mock import patch
import uuid
import warnings

import pytest

from custom_components.vmc_master import installatore, prepara
from custom_components.vmc_master import motore_installa_vmc as motore

from .test_b22_motore import RICHIESTA, SupervisorFinto, _engine, _identita

Failure = motore.Failure
IP = "192.168.1.160"
VERSIONE = json.loads(
    (Path(installatore.__file__).parent / "manifest.json").read_text(encoding="utf-8")
)["version"]


def _codice(funzione, *argomenti) -> str:
    with pytest.raises(Failure) as errore:
        funzione(*argomenti)
    return errore.value.code


# ---------------------------------------------------------------- socket finto
class PresaFinta:
    """Al posto di socket.socket: invia i pezzi indicati, poi «tempo scaduto»."""

    def __init__(self, pezzi):
        self.pezzi = list(pezzi)
        self.inviati: list[bytes] = []
        self.attese: list[float] = []

    def __call__(self, *_args):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def settimeout(self, secondi):
        self.attese.append(secondi)

    def setsockopt(self, *_args):
        pass

    def connect(self, indirizzo):
        self.indirizzo = indirizzo

    def sendall(self, dati):
        self.inviati.append(dati)

    def recv(self, quanti):
        if not self.pezzi:
            raise socket.timeout("tempo scaduto")
        return self.pezzi.pop(0)[:quanti]


def test_risposta_lunga_si_ferma_a_512_byte() -> None:
    presa = PresaFinta([b"A" * 600])
    with patch.object(motore.socket, "socket", presa):
        assert motore.Transport().exchange("192.168.1.60", b"VMSL?") == b"A" * 512
    assert presa.inviati == [b"VMSL?"] and presa.indirizzo == ("192.168.1.60", motore.PORT)


def test_risposta_incompleta_oltre_il_tempo_massimo() -> None:
    """Pezzo arrivato quando il tempo massimo è già passato: vale quello che c'è."""
    presa = PresaFinta([b"VMNM Pr"])
    orologio = iter([0.0, 5.0])
    with patch.object(motore.socket, "socket", presa), patch.object(
        motore, "time", SimpleNamespace(monotonic=lambda: next(orologio))
    ):
        risposta = motore.Transport().exchange("192.168.1.60", b"VMNM?", complete=lambda _r: False)
    assert risposta == b"VMNM Pr" and presa.attese == [2.0]


def test_rinomina_dalla_vmc() -> None:
    for risposta, accettato in ((b"OK", True), (b"KO", False)):
        presa = PresaFinta([risposta])
        with patch.object(motore.socket, "socket", presa):
            assert motore.Transport().rename("192.168.1.60", "Nuovo") is accettato
        assert presa.inviati == [b"VMNM Nuovo"]


def test_rete_letta_senza_intestazione() -> None:
    """Risposta a VMSL? senza «VMSL » davanti: si legge lo stesso."""
    risposta = ("Casa".ljust(32, "*") + "segreta1".ljust(32, "*") + "192.168.001.060" + "05001"
                + "192.168.001.001" + "255.255.255.000" + "10").encode()
    with patch.object(motore.socket, "socket", PresaFinta([risposta])):
        assert motore.Transport().network_info("192.168.1.60") == {
            "ssid": "Casa", "router": "192.168.001.001", "subnet": "255.255.255.000"}


# ---------------------------------------------------------------- controlli dei dati
RICHIESTA_PASSWORD = {"ap_ssid": "VMC_12345678", "ap_password": "12345678", "new_password": "NuovaPass1"}


def test_pacchetto_cambio_password() -> None:
    assert motore.password_packet("12345678", "NuovaPass1") == (
        b"VMPW 12345678" + b"*" * 24 + b"NuovaPass1" + b"*" * 22)
    assert _codice(motore.password_packet, "corta", "NuovaPass1") == "invalid_ap_password"
    assert _codice(motore.password_packet, "12345678", "corta") == "invalid_new_password"


def test_richiesta_cambio_password() -> None:
    richiesta = motore.normalize_ap_password({**RICHIESTA_PASSWORD, "home_ssid": "Casa"})
    assert richiesta["new_password"] == "NuovaPass1" and richiesta["home_ssid"] == "Casa"
    assert richiesta["home_password"] == "" and richiesta["restore_password"] == ""
    assert _codice(motore.normalize_ap_password, {**RICHIESTA_PASSWORD, "ap_ssid": ""}) == "invalid_ap_ssid"
    assert _codice(motore.normalize_ap_password, {**RICHIESTA_PASSWORD, "new_password": "corta"}) == "invalid_new_password"
    assert _codice(motore.normalize_ap_password, {**RICHIESTA_PASSWORD, "new_password": "Città12345"}) == "invalid_new_password"
    assert _codice(motore.normalize_ap_password, {**RICHIESTA_PASSWORD, "new_password": "12345678"}) == "same_password"
    # password attuale valida per il Wi-Fi ma più lunga dei 32 caratteri del campo Air Guard
    assert _codice(motore.normalize_ap_password, {**RICHIESTA_PASSWORD, "ap_password": "a" * 40}) == "invalid_ap_password"


def test_identita_configurata(tmp_path: Path) -> None:
    assert _codice(motore.configured_identity, ["non", "un", "dizionario"], tmp_path) == "invalid_request"
    assert _codice(motore.configured_identity, {"ap_ssid": "VMC_12345678"}, tmp_path) == "not_configured"
    _identita(tmp_path)
    assert _codice(motore.configured_identity, {"ap_ssid": "VMC_87654321"}, tmp_path) == "not_configured"
    assert motore.configured_identity({"ap_ssid": "VMC_12345678"}, tmp_path) == {
        "ip": "192.168.1.60", "ap_ssid": "VMC_12345678",
        "expected_mac": "AA:BB:CC:DD:EE:01", "expected_name": "Prova"}
    assert motore.normalize_ap_mode({"ap_ssid": "VMC_12345678"}, tmp_path)["ip"] == "192.168.1.60"
    _identita(tmp_path, ip="")
    assert _codice(motore.configured_identity, {"ap_ssid": "VMC_12345678"}, tmp_path) == "not_configured"
    # identità salvata senza MAC e senza nome: niente da confrontare
    motore.atomic_json(tmp_path / "identity.json", {"ap_ssid": "VMC_12345678", "ip": "192.168.1.61"})
    assert motore.configured_identity({"ap_ssid": "VMC_12345678"}, tmp_path) == {
        "ip": "192.168.1.61", "ap_ssid": "VMC_12345678", "expected_mac": "", "expected_name": ""}


def test_richiesta_rinomina(tmp_path: Path) -> None:
    _identita(tmp_path)
    richiesta = motore.normalize_rename({"ap_ssid": "VMC_12345678", "name": " Zona_Giorno "}, tmp_path)
    assert richiesta["new_name"] == "Zona_Giorno" and richiesta["expected_name"] == "Prova"
    for nome in ("", "Nome-troppo-lungo", "Città", "due parole"):
        assert _codice(motore.normalize_rename, {"ap_ssid": "VMC_12345678", "name": nome}, tmp_path) == "invalid_name"


def test_profilo_da_ripristinare_senza_wifi() -> None:
    """Scheda attiva ma senza rete Wi-Fi memorizzata: nessun profilo Wi-Fi da rimettere."""
    assert motore.restore_payload({"enabled": True, "ipv4": {"method": "auto"}, "wifi": {"ssid": ""}}) == {
        "enabled": True, "ipv4": {"method": "auto"}}


# ---------------------------------------------------------------- Engine: parti della 8.6.0
class TrasportoCasa:
    """VMC sulla rete di casa. identify risponde secondo la sequenza (un'eccezione = nessuna
    risposta, l'ultimo valore si ripete); altre: IP -> nome di altre VMC in rete."""

    def __init__(self, nomi, mac="AA:BB:CC:DD:EE:01", rinomina=True, invio=None, altre=None):
        self.nomi, self.mac, self.rinomina, self.invio = list(nomi), mac, rinomina, invio
        self.altre = altre or {}
        self.rinominate: list = []
        self.inviati: list = []
        self.identificazioni: list = []

    def identify(self, ip, interface=""):
        if ip in self.altre:
            return self.altre[ip]
        if ip != "192.168.1.60" and not interface:
            raise OSError("nessuna risposta")
        self.identificazioni.append((ip, interface))
        valore = self.nomi.pop(0) if len(self.nomi) > 1 else self.nomi[0]
        if isinstance(valore, Exception):
            raise valore
        return valore

    def neighbor_mac(self, ip):
        return self.mac

    def rename(self, ip, name):
        if isinstance(self.rinomina, Exception):
            raise self.rinomina
        self.rinominate.append((ip, name))
        return self.rinomina

    def send(self, ip, packet, interface=""):
        if self.invio:
            raise self.invio
        self.inviati.append((ip, packet, interface))


def _richiesta_casa(**valori):
    richiesta = {"ip": "192.168.1.60", "expected_name": "Prova", "expected_mac": "AA:BB:CC:DD:EE:01"}
    richiesta.update(valori)
    return richiesta


def test_conferma_identita(tmp_path: Path) -> None:
    def conferma(trasporto, **valori):
        engine, _ = _engine(tmp_path, SupervisorFinto(), trasporto)
        return engine.confirm_identity(_richiesta_casa(**valori))

    assert conferma(TrasportoCasa(["Prova"])) == "Prova"
    assert conferma(TrasportoCasa(["Prova"], mac="")) == "Prova"  # MAC non leggibile: basta il nome
    assert conferma(TrasportoCasa(["Altra"], mac="AA:BB:CC:DD:EE:09"), expected_name="", expected_mac="") == "Altra"
    with pytest.raises(Failure) as errore:
        conferma(TrasportoCasa([OSError()]))
    assert errore.value.code == "vmc_unreachable" and "192.168.1.60" in errore.value.message
    with pytest.raises(Failure) as errore:
        conferma(TrasportoCasa(["Altra"]))
    assert errore.value.code == "identity_unconfirmed" and "risponde Altra invece di Prova" in errore.value.message
    with pytest.raises(Failure) as errore:
        conferma(TrasportoCasa(["Prova"], mac="AA:BB:CC:DD:EE:09"))
    assert errore.value.code == "identity_unconfirmed" and "MAC" in errore.value.message


def _rinomina(tmp_path, trasporto, nome="Nuovo", supervisor=None):
    engine, orologio = _engine(tmp_path, supervisor or SupervisorFinto(ethernet="192.168.1.10/29"), trasporto)
    engine.rename({"ap_ssid": "VMC_12345678", "name": nome})
    return engine, orologio


def test_rinomina(tmp_path: Path) -> None:
    _identita(tmp_path, extra="resta")
    trasporto = TrasportoCasa(["Prova", "Nuovo"], altre={"192.168.1.9": "Cucina"})
    engine, orologio = _rinomina(tmp_path, trasporto)
    assert trasporto.rinominate == [("192.168.1.60", "Nuovo")] and orologio.t == 1001.0
    assert json.loads((tmp_path / "identity.json").read_text()) == {
        "ap_ssid": "VMC_12345678", "ip": "192.168.1.60", "name": "Nuovo", "mac": "AA:BB:CC:DD:EE:01", "extra": "resta"}
    dati = engine.status.data
    assert dati["success"] is True and dati["stage"] == "Completato" and dati["vmc_name"] == "Nuovo"
    assert "Il nome della rete VMC_12345678 non cambia" in dati["message"]


def test_rinomina_senza_ricerca_e_stesso_nome(tmp_path: Path) -> None:
    """Rete del server non individuata: nessun controllo dei doppioni. Stesso nome: nessun invio."""
    _identita(tmp_path)
    trasporto = TrasportoCasa(["Prova", "Nuovo"])
    _rinomina(tmp_path, trasporto, supervisor=SupervisorFinto(ethernet=""))
    assert trasporto.rinominate == [("192.168.1.60", "Nuovo")]
    trasporto = TrasportoCasa(["Nuovo"])
    engine, _ = _rinomina(tmp_path, trasporto)
    assert trasporto.rinominate == [] and engine.status.data["success"] is True


@pytest.mark.parametrize(("trasporto", "codice", "testo"), [
    (TrasportoCasa(["Prova"], altre={"192.168.1.12": "Nuovo"}), "duplicate_name", "è già usato"),
    (TrasportoCasa(["Prova"], rinomina=OSError("chiusa")), "vmc_unreachable", "nuovo nome"),
    (TrasportoCasa(["Prova"], rinomina=False), "rename_refused", "OK"),
    (TrasportoCasa(["Prova", OSError()]), "rename_unconfirmed", "risponde ancora con nessun nome"),
    (TrasportoCasa(["Prova", "Prova"]), "rename_unconfirmed", "risponde ancora con Prova"),
])
def test_rinomina_non_riuscita(tmp_path: Path, trasporto, codice, testo) -> None:
    _identita(tmp_path)
    with pytest.raises(Failure) as errore:
        _rinomina(tmp_path, trasporto)
    assert errore.value.code == codice and testo in errore.value.message
    assert json.loads((tmp_path / "identity.json").read_text())["name"] == "Prova"


def test_access_point(tmp_path: Path) -> None:
    _identita(tmp_path)
    trasporto = TrasportoCasa(["Prova"])
    engine, orologio = _engine(tmp_path, SupervisorFinto(), trasporto)
    engine.access_point({"ap_ssid": "VMC_12345678"})
    assert trasporto.inviati == [("192.168.1.60", motore.access_point_packet(), "")]
    assert orologio.t == 1010.0 and not (tmp_path / "identity.json").exists()
    dati = engine.status.data
    assert dati["success"] is True and dati["network_sent"] is True and dati["vmc_ip"] == ""
    assert "è di nuovo visibile" in dati["message"]


@pytest.mark.parametrize(("trasporto", "codice"), [
    (TrasportoCasa(["Prova"], invio=OSError("rifiutato")), "vmc_unreachable"),
    (TrasportoCasa(["Prova"]), "ap_not_applied"),
    (TrasportoCasa(["Prova", OSError()]), "ap_unconfirmed"),
    (TrasportoCasa(["Prova", Failure("invalid_vmc", "x")]), "ap_unconfirmed"),
    (TrasportoCasa(["Prova", "Altra"]), "ap_unconfirmed"),
])
def test_access_point_non_riuscito(tmp_path: Path, trasporto, codice) -> None:
    _identita(tmp_path)
    supervisor = SupervisorFinto()
    supervisor.accesspoints = lambda _interfaccia: []
    engine, _ = _engine(tmp_path, supervisor, trasporto)
    with pytest.raises(Failure) as errore:
        engine.access_point({"ap_ssid": "VMC_12345678"})
    assert errore.value.code == codice
    assert (tmp_path / "identity.json").exists()
    assert engine.status.data["network_sent"] is (codice != "vmc_unreachable")


class SupervisorPassword(SupervisorFinto):
    """Dopo il cambio password la rete VMC si raggiunge (o no) con la password nuova."""

    def __init__(self, collega_dopo=True, **valori):
        super().__init__(**valori)
        self.collega_dopo = collega_dopo
        self.collegamenti = 0

    def update(self, interface, payload):
        risultato = super().update(interface, payload)
        if (payload.get("wifi") or {}).get("ssid", "").startswith("VMC_"):
            self.collegamenti += 1
            if self.collegamenti > 1 and not self.collega_dopo:
                self.scheda["connected"] = False
        return risultato


def test_cambia_password(tmp_path: Path) -> None:
    supervisor = SupervisorPassword()
    trasporto = TrasportoCasa(["Prova"])
    engine, orologio = _engine(tmp_path, supervisor, trasporto)
    engine.change_ap_password(dict(RICHIESTA_PASSWORD))
    assert trasporto.inviati == [("192.168.4.1", motore.password_packet("12345678", "NuovaPass1"), "wlan0")]
    assert trasporto.identificazioni == [("192.168.4.1", "wlan0"), ("192.168.4.1", "wlan0")]
    assert supervisor.aggiornamenti == [
        ("wlan0", motore.ap_profile("VMC_12345678", "12345678")),
        ("wlan0", motore.ap_profile("VMC_12345678", "NuovaPass1")),
        ("wlan0", {"enabled": False}),
    ]
    assert orologio.t == 1005.0 and not (tmp_path / "restore.json").exists()
    dati = engine.status.data
    assert dati["success"] is True and dati["stage"] == "Completato" and dati["vmc_name"] == "Prova"


@pytest.mark.parametrize(("supervisor", "trasporto", "codice"), [
    (SupervisorPassword(), TrasportoCasa([OSError()]), "vmc_unreachable"),
    (SupervisorPassword(collega_dopo=False), TrasportoCasa(["Prova"]), "password_unconfirmed"),
    (SupervisorPassword(), TrasportoCasa(["Prova", OSError()]), "password_unconfirmed"),
    (SupervisorPassword(), TrasportoCasa(["Prova", Failure("invalid_vmc", "x")]), "password_unconfirmed"),
    (SupervisorPassword(), TrasportoCasa(["Prova", "Altra"]), "password_unconfirmed"),
])
def test_cambia_password_non_riuscito(tmp_path: Path, supervisor, trasporto, codice) -> None:
    engine, _ = _engine(tmp_path, supervisor, trasporto)
    with pytest.raises(Failure) as errore:
        engine.change_ap_password(dict(RICHIESTA_PASSWORD))
    assert errore.value.code == codice
    # il Wi-Fi del server torna sempre com'era
    assert supervisor.aggiornamenti[-1] == ("wlan0", {"enabled": False})
    assert not (tmp_path / "restore.json").exists()
    assert engine.status.data["network_sent"] is (codice != "vmc_unreachable")


def test_rete_vmc_mai_collegata(tmp_path: Path) -> None:
    """La scheda Wi-Fi non si collega alla rete VMC: dopo l'attesa nessun indirizzo."""
    engine, orologio = _engine(tmp_path, SupervisorFinto())
    assert engine.wait_ap("wlan0", "VMC_12345678", 5) == "" and orologio.t == 1005.0


def test_rete_vmc_errore_con_restore_gia_tolto(tmp_path: Path) -> None:
    """Errore prima del collegamento quando restore.json non c'è più: nulla da togliere."""
    supervisor = SupervisorFinto()
    engine, _ = _engine(tmp_path, supervisor)

    def avviso_rotto(*_args, **_kwargs):
        (tmp_path / "restore.json").unlink()
        raise OSError("disco pieno")

    with patch.object(engine.status, "emit", side_effect=avviso_rotto), pytest.raises(OSError):
        with engine.ap_session(supervisor.info(), motore.normalize_request(RICHIESTA), "x"):
            pass
    assert supervisor.aggiornamenti == [] and not (tmp_path / "restore.json").exists()


def test_scan_tiene_il_segnale_migliore(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    supervisor.accesspoints = lambda _i: [{"ssid": "VMC_1", "signal": 70, "frequency": 2412},
                                          {"ssid": "VMC_1", "signal": 40, "frequency": 5180}]
    engine, _ = _engine(tmp_path, supervisor)
    engine.scan()
    assert json.loads((tmp_path / "scan.json").read_text())["vmc_networks"] == [
        {"ssid": "VMC_1", "signal": 70, "band": "2,4 GHz"}]


# ---------------------------------------------------------------- stato, avvio e worker
def _blocco(radice: Path):
    """Un'altra procedura in corso: tiene il blocco di worker.lock."""
    radice.mkdir(parents=True, exist_ok=True)
    file = open(radice / "worker.lock", "a")
    fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return file


def _libero(radice: Path) -> bool:
    with open(radice / "worker.lock", "a") as file:
        try:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return False
    return True


def _in_corso(radice: Path) -> None:
    motore.Status(radice).emit("Invio rete di casa", 50, "In corso.", job_id="lavoro", action="configure",
                               finished=False)


def test_stato_con_procedura_in_corso(tmp_path: Path) -> None:
    _in_corso(tmp_path)
    blocco = _blocco(tmp_path)
    try:
        dati = motore.read_status(tmp_path)
    finally:
        blocco.close()
    assert dati["finished"] is False and dati["stage"] == "Invio rete di casa"
    assert json.loads((tmp_path / "status.json").read_text())["finished"] is False


def test_stato_con_procedura_interrotta(tmp_path: Path) -> None:
    """Worker terminato in modo anomalo: la scheda non resta bloccata."""
    _identita(tmp_path)
    _in_corso(tmp_path)
    dati = motore.read_status(tmp_path)
    assert dati["finished"] is True and dati["error_code"] == "interrupted" and dati["stage"] == "Errore"
    assert dati["configured_ip"] == "192.168.1.60"
    salvato = json.loads((tmp_path / "status.json").read_text())
    assert salvato["error_code"] == "interrupted" and salvato["success"] is False
    assert not any(k.startswith("configured_") for k in salvato) and "vmc_networks" not in salvato
    _in_corso(tmp_path)
    (tmp_path / "restore.json").write_text("{}")
    assert motore.read_status(tmp_path)["stage"] == "Ripristino necessario"


@pytest.fixture
def processo():
    """Al posto di subprocess.Popen: registra la riga di comando del worker."""
    with patch.object(motore.subprocess, "Popen") as finto:
        yield finto


def test_avvio_del_worker(tmp_path: Path, processo) -> None:
    radice = tmp_path / "motore"
    esito = motore.launch("configure", dict(RICHIESTA), radice)
    assert esito["accepted"] is True and uuid.UUID(esito["job_id"])
    lavoro = json.loads((radice / (esito["job_id"] + ".json")).read_text())
    assert lavoro == {"action": "configure", "payload": RICHIESTA}
    comando = processo.call_args.args[0]
    assert comando[:2] == [sys.executable, str(Path(motore.__file__).resolve())]
    assert comando[2:5] == ["worker", "--job", esito["job_id"]]
    assert processo.call_args.kwargs["start_new_session"] is True
    stato = json.loads((radice / "status.json").read_text())
    assert stato["job_id"] == esito["job_id"] and stato["action"] == "configure" and stato["finished"] is False
    assert _libero(radice)  # il blocco passa al worker: qui si chiude
    # azioni senza dati da controllare
    assert motore.launch("scan", {}, radice)["accepted"] is True


def test_avvio_rifiutato(tmp_path: Path, processo) -> None:
    blocco = _blocco(tmp_path)
    try:
        esito = motore.launch("scan", {}, tmp_path)
    finally:
        blocco.close()
    assert esito == {"accepted": False, "message": "Una procedura è già in corso. Attendere il risultato."}
    assert _codice(motore.launch, "configure", {**RICHIESTA, "home_ssid": ""}, tmp_path) == "invalid_ssid"
    assert _codice(motore.launch, "verify", {"ip": "8.8.8.8"}, tmp_path) == "invalid_ip"
    processo.assert_not_called()
    assert _libero(tmp_path) and list(tmp_path.glob("*-*.json")) == []


def test_avvio_non_riuscito(tmp_path: Path, processo) -> None:
    processo.side_effect = OSError("troppi processi")
    assert _codice(motore.launch, "scan", {}, tmp_path) == "worker_start"
    assert _libero(tmp_path) and list(tmp_path.glob("*-*.json")) == []


class MotoreRegistra:
    def __init__(self, root):
        self.root = Path(root)
        self.chiamate: list = []

    def __getattr__(self, nome):
        return lambda *argomenti: self.chiamate.append((nome, *argomenti))


@pytest.mark.parametrize(("azione", "attese"), [
    ("diagnose", [("diagnose",)]),
    ("recover", [("recover",)]),
    ("verify", [("verify", {"x": 1})]),
    ("scan", [("scan",)]),
    ("rename", [("rename", {"x": 1})]),
    ("ap_mode", [("access_point", {"x": 1})]),
    ("configure", [("run", {"x": 1})]),
    ("ap_password", [("change_ap_password", {"x": 1})]),
])
def test_smistamento(tmp_path: Path, azione, attese) -> None:
    engine = MotoreRegistra(tmp_path)
    motore.dispatch(engine, azione, {"x": 1})
    assert engine.chiamate == attese


def test_smistamento_con_ripristino_in_sospeso(tmp_path: Path) -> None:
    (tmp_path / "restore.json").write_text("{}")
    for azione, metodo in (("configure", "run"), ("ap_password", "change_ap_password")):
        engine = MotoreRegistra(tmp_path)
        motore.dispatch(engine, azione, {})
        assert engine.chiamate == [("restore",), (metodo, {})]
    assert _codice(motore.dispatch, MotoreRegistra(tmp_path), "elimina", {}) == "invalid_action"


@pytest.fixture
def segnali():
    """Al posto del modulo signal: registra gestori e allarmi senza toccare il processo dei test."""
    registro = SimpleNamespace(gestori={}, allarmi=[], SIGTERM=15, SIGALRM=14)
    registro.signal = lambda numero, gestore: registro.gestori.__setitem__(numero, gestore)
    registro.alarm = registro.allarmi.append
    with patch.object(motore, "signal", registro):
        yield registro


def _lavoro(radice: Path, azione: str, dati=None) -> tuple[str, int]:
    lavoro = str(uuid.uuid4())
    motore.atomic_json(radice / (lavoro + ".json"), {"action": azione, "payload": dati or {}})
    return lavoro, os.open(radice / "worker.lock", os.O_CREAT | os.O_RDWR)


def _chiuso(descrittore: int) -> bool:
    try:
        os.fstat(descrittore)
    except OSError:
        return True
    return False


def test_worker(tmp_path: Path, segnali) -> None:
    engine, _ = _engine(tmp_path, SupervisorFinto())
    lavoro, descrittore = _lavoro(tmp_path, "diagnose")
    assert motore.run_worker(lavoro, descrittore, tmp_path, engine) == 0
    stato = json.loads((tmp_path / "status.json").read_text())
    assert stato["finished"] is True and stato["success"] is True and stato["job_id"] == lavoro
    assert stato["action"] == "diagnose" and stato["stage"] == "Server verificato"
    assert not (tmp_path / (lavoro + ".json")).exists() and _chiuso(descrittore)
    assert segnali.allarmi == [420, 0]
    # SIGTERM o il tempo massimo interrompono la procedura con un errore chiaro
    for numero in (segnali.SIGTERM, segnali.SIGALRM):
        with pytest.raises(Failure) as errore:
            segnali.gestori[numero](numero, None)
        assert errore.value.code == "interrupted"


def test_worker_dati_non_validi(tmp_path: Path, segnali) -> None:
    assert motore.run_worker("non-un-lavoro", 3, tmp_path) == 2
    assert motore.run_worker(str(uuid.uuid4()), -1, tmp_path) == 2
    engine, _ = _engine(tmp_path, SupervisorFinto())
    lavoro, descrittore = _lavoro(tmp_path, "verify", {"ip": ""})
    assert motore.run_worker(lavoro, descrittore, tmp_path, engine) == 0
    stato = json.loads((tmp_path / "status.json").read_text())
    assert stato["finished"] is True and stato["success"] is False
    assert stato["error_code"] == "invalid_ip" and stato["stage"] == "Errore"
    assert _chiuso(descrittore) and segnali.allarmi == [420, 0]


@pytest.mark.parametrize(("inviata", "ripristino", "fase"), [
    (True, False, "Verifica non completata"),
    (False, True, "Ripristino necessario"),
    (False, False, "Errore"),
])
def test_worker_errore_inatteso(tmp_path: Path, segnali, inviata, ripristino, fase) -> None:
    engine, _ = _engine(tmp_path, SupervisorFinto())
    engine.status.data["network_sent"] = inviata
    if ripristino:
        (tmp_path / "restore.json").write_text("{}")
    lavoro, descrittore = _lavoro(tmp_path, "scan")
    with patch.object(engine, "scan", side_effect=KeyError("payload")):
        assert motore.run_worker(lavoro, descrittore, tmp_path, engine) == 0
    stato = json.loads((tmp_path / "status.json").read_text())
    assert stato["error_code"] == "communication_error" and stato["stage"] == fase
    assert "Errore di comunicazione" in stato["message"] and stato["finished"] is True
    assert not (tmp_path / (lavoro + ".json")).exists() and _chiuso(descrittore)


def test_errore_dei_dati(tmp_path: Path) -> None:
    radice = tmp_path / "motore"
    motore.report_input_error(Failure("invalid_ssid", "Rete non valida."), radice, "configure")
    stato = json.loads((radice / "status.json").read_text())
    assert stato["error_code"] == "invalid_ssid" and stato["finished"] is True and stato["action"] == "configure"
    # con una procedura in corso lo stato non si sovrascrive
    _in_corso(radice)
    blocco = _blocco(radice)
    try:
        motore.report_input_error(Failure("invalid_name", "Nome non valido."), radice, "rename")
    finally:
        blocco.close()
    assert json.loads((radice / "status.json").read_text())["job_id"] == "lavoro"


# ---------------------------------------------------------------- riga di comando
@pytest.fixture
def riga_di_comando(tmp_path, monkeypatch, processo):
    """La riga di comando lavora nella cartella del test, non accanto al motore."""
    for funzione in (motore.read_status, motore.launch, motore.run_worker, motore.report_input_error):
        monkeypatch.setattr(funzione, "__defaults__", (tmp_path, *funzione.__defaults__[1:]))
    monkeypatch.setattr(motore, "ROOT", tmp_path)

    def esegui(*argomenti):
        monkeypatch.setattr(sys, "argv", ["motore_installa_vmc.py", *argomenti])
        return motore.main()

    return esegui


def _uscita(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def test_riga_di_comando_stato_e_worker(tmp_path: Path, riga_di_comando, capsys) -> None:
    assert riga_di_comando("status") == 0
    assert _uscita(capsys)["stage"] == "In attesa"
    assert riga_di_comando("worker", "--job", "non-un-lavoro", "--lock-fd", "3") == 2
    assert capsys.readouterr().out == ""


def test_riga_di_comando_ripristino(tmp_path: Path, riga_di_comando, processo, capsys) -> None:
    assert riga_di_comando("recover-if-needed") == 0
    assert _uscita(capsys) == {"accepted": False, "message": "Nessun ripristino pendente."}
    processo.assert_not_called()
    (tmp_path / "restore.json").write_text("{}")
    assert riga_di_comando("recover-if-needed") == 0
    assert _uscita(capsys)["accepted"] is True
    assert json.loads((tmp_path / "status.json").read_text())["action"] == "recover"


def test_riga_di_comando_avvio(tmp_path: Path, riga_di_comando, processo, capsys) -> None:
    assert riga_di_comando("start", "--action", "scan") == 0
    assert _uscita(capsys)["accepted"] is True
    assert riga_di_comando("start", "--action", "configure", "--payload", json.dumps(RICHIESTA)) == 0
    esito = _uscita(capsys)
    assert esito["accepted"] is True
    assert json.loads((tmp_path / (esito["job_id"] + ".json")).read_text())["payload"] == RICHIESTA
    assert processo.call_count == 2


@pytest.mark.parametrize(("argomenti", "codice"), [
    (("start", "--payload", "x" * 8193), "invalid_request"),
    (("start", "--action", "rename", "--payload", "{rotto"), "invalid_request"),
    (("start", "--action", "configure", "--payload", json.dumps({**RICHIESTA, "ap_password": "123"})), "invalid_ap_password"),
])
def test_riga_di_comando_dati_non_validi(tmp_path: Path, riga_di_comando, processo, capsys, argomenti, codice) -> None:
    assert riga_di_comando(*argomenti) == 0
    esito = _uscita(capsys)
    assert esito["accepted"] is False and esito["error_code"] == codice
    stato = json.loads((tmp_path / "status.json").read_text())
    assert stato["error_code"] == codice and stato["finished"] is True
    assert stato["action"] == (argomenti[2] if argomenti[1] == "--action" else "diagnose")
    processo.assert_not_called()


def test_motore_avviato_come_programma(monkeypatch) -> None:
    """python3 motore_installa_vmc.py: il codice di uscita è quello di main (2 = lavoro non valido)."""
    monkeypatch.setattr(sys, "argv", ["motore_installa_vmc.py", "worker", "--job", "non-un-lavoro"])
    with pytest.raises(SystemExit) as uscita:
        runpy.run_path(motore.__file__, run_name="__main__")
    assert uscita.value.code == 2


# ---------------------------------------------------------------- installatore e prepara
def test_automazione_gia_con_a_capo_finale() -> None:
    testo = installatore.automazione_come_package("alias: Prova\n", "sala")
    assert testo.endswith("    alias: Prova\n") and not testo.endswith("\n\n")


def test_sensori_di_forma_inattesa() -> None:
    assert installatore._per_piattaforma(None) == {}
    assert installatore._per_piattaforma("testo") is None
    assert installatore._per_piattaforma([{"platform": "rest"}, "testo"]) is None
    assert installatore._ricariche_sensori("testo", []) is None
    assert installatore._ricariche_sensori(None, [{"platform": "rest", "name": "x"}]) == {"rest.reload"}
    assert installatore.ricariche_necessarie("sensor: testo\n", "sensor:\n  - platform: rest\n") is None


def test_ricariche_un_cambio_alla_volta() -> None:
    """Una sola parte cambiata per volta: l'esito di ogni ramo non dipende dall'ordine in cui
    si visitano le chiavi (insiemi, ordine diverso a ogni avvio di Python)."""
    ricariche = installatore.ricariche_necessarie
    sensori = installatore._ricariche_sensori
    # sensori TCP cambiati (IP della VMC): riavvio; gruppo uguale: nulla da ricaricare
    assert sensori([{"platform": "tcp", "host": "a"}], [{"platform": "tcp", "host": "b"}]) is None
    assert sensori([{"platform": "rest", "x": 1}, {"platform": "tcp"}],
                   [{"platform": "rest", "x": 2}, {"platform": "tcp"}]) == {"rest.reload"}
    tcp = "sensor:\n  - platform: tcp\n    host: 192.168.1.160\n"
    assert ricariche(tcp, tcp.replace("160", "170")) is None
    assert ricariche("timer:\n  a: {}\n", "timer:\n  b: {}\n") == {"timer.reload"}
    assert ricariche("shell_command:\n  a: x\n", "shell_command:\n  a: y\n") is None
    recorder = "recorder:\n  exclude:\n    entities:\n      - a.b\n"
    assert ricariche(recorder, recorder + "      - c.d\n") == set()
    assert ricariche(recorder, recorder + "  purge_keep_days: 3\n") is None
    assert ricariche("a: 1\nb: 2\n", "b: 2\na: 1\n") == set()


def test_package_che_non_e_un_dizionario() -> None:
    assert installatore.ricariche_necessarie("- uno\n- due\n", "a: 1\n") is None
    assert installatore.ricariche_necessarie("a: 1\n", "testo semplice\n") is None


def test_marcatore_illeggibile_si_riscrive(tmp_path: Path) -> None:
    config = str(tmp_path)
    installatore.installa(config, "sala", "192.168.1.161", VERSIONE)
    marcatore = installatore.cartella_vmc(config, "sala") / installatore.FILE_MARCATORE
    corretto = marcatore.read_bytes()
    marcatore.write_bytes(b"\xff\xfe non UTF-8")
    esito = installatore.installa(config, "sala", "192.168.1.161", VERSIONE)
    assert esito.file_scritti == [] and esito.backup is None and esito.file_modificati == []
    assert marcatore.read_bytes() == corretto


def test_prepara_con_un_file_mancante(tmp_path: Path) -> None:
    """Uno script tolto dal package non impedisce la preparazione: si riscrive."""
    config = str(tmp_path)
    installatore.installa(config, "master", IP, "9.0.0b1")
    script = installatore.cartella_vmc(config, "master") / "vmc_master_script_cambio_nome.sh"
    script.unlink()
    assert prepara.da_preparare(config, "master", IP, VERSIONE) is True
    assert prepara.prepara(config, [["master", IP]], VERSIONE) == ["master"]
    assert script.is_file()


def test_prepara_dalla_riga_di_comando(tmp_path: Path, capsys) -> None:
    config = str(tmp_path)
    installatore.installa(config, "master", IP, "9.0.0b1")
    assert prepara.main([config, json.dumps([["master", IP], ["sala", "192.168.1.161"]])]) == 0
    assert json.loads(capsys.readouterr().out) == ["master"]
    assert installatore.leggi_marcatore(config, "master")["versione"] == VERSIONE


def test_prepara_avviato_come_modulo(tmp_path: Path, monkeypatch, capsys) -> None:
    """python -m custom_components.vmc_master.prepara: stesso contratto di main."""
    monkeypatch.setattr(sys, "argv", ["prepara", str(tmp_path), "[]"])
    with warnings.catch_warnings():
        # il modulo è già importato dai test: runpy lo segnala, è previsto
        warnings.simplefilter("ignore", RuntimeWarning)
        with pytest.raises(SystemExit) as uscita:
            runpy.run_module("custom_components.vmc_master.prepara", run_name="__main__")
    assert uscita.value.code == 0 and json.loads(capsys.readouterr().out) == []
