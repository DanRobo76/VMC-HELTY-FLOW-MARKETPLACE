"""Copertura: parti tecniche del motore Wi-Fi e della prima installazione non ancora provate.

Solo test, nessuna modifica al codice. Le logiche di ventilazione non sono toccate.
Le prove usano Supervisor, VMC e file di sistema finti (nessun hardware reale).
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import socket
import threading
from unittest.mock import patch

import pytest

from custom_components.vmc_master import motore_installa_vmc as motore
from custom_components.vmc_master import prima_installazione as pi

from .test_b22_motore import (
    RICHIESTA,
    SCHEDA_CASA,
    SupervisorFinto,
    TrasportoRete,
    TrasportoVerifica,
    VmcTcp,
    _engine,
    _identita,
)

Failure = motore.Failure


def _codice(funzione, *argomenti) -> str:
    with pytest.raises(Failure) as errore:
        funzione(*argomenti)
    return errore.value.code


# ---------------------------------------------------------------- controlli dei dati
@pytest.mark.parametrize("valore", ["", "abc", None, "999.1.1.1", "192.168.1"])
def test_ip_non_valido(valore) -> None:
    assert _codice(motore.private_ip, valore) == "invalid_ip"


def test_ip_non_locale() -> None:
    assert _codice(motore.private_ip, "8.8.8.8") == "invalid_ip"
    assert motore.private_ip("10.0.0.5") == "10.0.0.5"


def test_mac() -> None:
    assert motore.mac("aa-bb-cc-dd-ee-ff") == "AA:BB:CC:DD:EE:FF"
    assert motore.mac("") == ""
    assert _codice(motore.mac, "AA:BB:CC") == "invalid_mac"
    assert _codice(motore.mac, "GG:BB:CC:DD:EE:FF") == "invalid_mac"


def test_password_wifi() -> None:
    assert motore.wifi_password("12345678")
    assert motore.wifi_password("a" * 63)
    assert motore.wifi_password("0123456789abcdef" * 4)  # PSK esadecimale da 64
    assert not motore.wifi_password("1234567")
    assert not motore.wifi_password("g" * 64)
    assert not motore.wifi_password("12345678\x00")


def test_campo_da_32() -> None:
    assert motore.field32("Casa", "c", "Rete") == "Casa" + "*" * 28
    assert _codice(motore.field32, "", "c", "Rete") == "c"
    assert _codice(motore.field32, "x" * 33, "c", "Rete") == "c"
    assert _codice(motore.field32, 123, "c", "Rete") == "c"
    assert _codice(motore.field32, "Città", "c", "Rete") == "unsupported_encoding"
    assert _codice(motore.field32, "Casa*", "c", "Rete") == "ambiguous_padding"


def test_pacchetti() -> None:
    pacchetto = motore.network_packet("Casa", "passwordcasa")
    assert pacchetto.startswith(b"VMSL Casa****") and pacchetto.endswith(motore.SUFFIX_INFRASTRUCTURE.encode())
    assert len(pacchetto) == 5 + 32 + 32 + len(motore.SUFFIX_INFRASTRUCTURE)
    assert motore.access_point_packet().endswith(motore.SUFFIX_ACCESS_POINT.encode())
    assert _codice(motore.network_packet, "Casa", "corta") == "invalid_password"


@pytest.mark.parametrize(("modifica", "codice"), [
    ({"ap_ssid": ""}, "invalid_ap_ssid"),
    ({"ap_ssid": "V" * 33}, "invalid_ap_ssid"),
    ({"ap_password": "123"}, "invalid_ap_password"),
    ({"restore_password": "corta"}, "invalid_restore_password"),
    ({"home_ssid": ""}, "invalid_ssid"),
    ({"final_ip": "8.8.8.8"}, "invalid_ip"),
])
def test_richiesta_non_valida(modifica, codice) -> None:
    assert _codice(motore.normalize_request, {**RICHIESTA, **modifica}) == codice


def test_richiesta_valida() -> None:
    richiesta = motore.normalize_request({**RICHIESTA, "final_ip": " 192.168.1.60 ", "lan_cidr": " 192.168.1.0/24 "})
    assert richiesta["final_ip"] == "192.168.1.60" and richiesta["lan_cidr"] == "192.168.1.0/24"
    assert richiesta["ip_mode"] == "IP riservato sul router"
    assert motore.normalize_request({**RICHIESTA, "final_ip": ""})["ip_mode"] == "DHCP"
    assert _codice(motore.normalize_request, ["non", "un", "dizionario"]) == "invalid_request"


def test_verifica_richiesta_non_dizionario(tmp_path: Path) -> None:
    assert _codice(motore.normalize_verification, "testo", tmp_path) == "invalid_request"


def test_identita_illeggibile(tmp_path: Path) -> None:
    assert motore.read_identity(tmp_path) == {}
    (tmp_path / "identity.json").write_text("{troncato")
    assert motore.read_identity(tmp_path) == {}
    (tmp_path / "identity.json").write_text("[1, 2]")
    assert motore.read_identity(tmp_path) == {}


# ---------------------------------------------------------------- Supervisor (HTTP vero su 127.0.0.1)
class _Gestore(BaseHTTPRequestHandler):
    risposte: dict = {}
    richieste: list = []

    def log_message(self, *_args) -> None:
        pass

    def _rispondi(self) -> None:
        lunghezza = int(self.headers.get("Content-Length") or 0)
        corpo = self.rfile.read(lunghezza) if lunghezza else b""
        type(self).richieste.append((self.command, self.path, self.headers.get("Authorization"), corpo))
        stato, testo = type(self).risposte.get(self.path, (404, b"{}"))
        self.send_response(stato)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(testo)))
        self.end_headers()
        self.wfile.write(testo)

    do_GET = _rispondi
    do_POST = _rispondi


@pytest.fixture
def supervisor_http(socket_enabled):
    _Gestore.risposte, _Gestore.richieste = {}, []
    server = HTTPServer(("127.0.0.1", 0), _Gestore)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}", _Gestore
    server.shutdown()
    server.server_close()


def test_supervisor_senza_token(monkeypatch) -> None:
    monkeypatch.delenv("SUPERVISOR_TOKEN", raising=False)
    monkeypatch.delenv("HASSIO_TOKEN", raising=False)
    assert _codice(motore.Supervisor("http://127.0.0.1:1").info) == "supervisor_unavailable"


def test_supervisor_risposte(supervisor_http) -> None:
    url, gestore = supervisor_http
    ok = json.dumps({"result": "ok", "data": {"interfaces": [{"interface": "wlan0"}]}}).encode()
    gestore.risposte = {
        "/network/info": (200, ok),
        "/network/interface/wlan%2F0/update": (200, b'{"result": "ok"}'),
        "/network/interface/wlan0/accesspoints": (200, b'{"result": "ok", "data": {"accesspoints": [{"ssid": "VMC_1"}]}}'),
    }
    supervisor = motore.Supervisor(url + "/", "segreto")
    assert supervisor.info() == {"interfaces": [{"interface": "wlan0"}]}
    assert supervisor.update("wlan/0", {"enabled": False}) == {}
    assert supervisor.accesspoints("wlan0") == [{"ssid": "VMC_1"}]
    metodo, percorso, autorizzazione, corpo = gestore.richieste[1]
    assert (metodo, percorso, autorizzazione) == ("POST", "/network/interface/wlan%2F0/update", "Bearer segreto")
    assert json.loads(corpo) == {"enabled": False}


def test_supervisor_errori(supervisor_http) -> None:
    url, gestore = supervisor_http
    gestore.risposte = {
        "/network/info": (403, b"{}"),
        "/network/interface/a/accesspoints": (200, b'{"result": "error"}'),
        "/network/interface/b/accesspoints": (200, b"non json"),
        "/network/interface/c/accesspoints": (200, b'{"result": "ok"}'),
    }
    supervisor = motore.Supervisor(url, "segreto")
    assert _codice(supervisor.info) == "supervisor_http"
    assert _codice(supervisor.accesspoints, "a") == "supervisor_error"
    assert _codice(supervisor.accesspoints, "b") == "supervisor_unavailable"
    assert supervisor.accesspoints("c") == []
    assert _codice(motore.Supervisor("http://127.0.0.1:1", "segreto").info) == "supervisor_unavailable"


# ---------------------------------------------------------------- Transport (VMC finta TCP)
def _con_vmc(pezzi, chiudi=True):
    return VmcTcp(lambda _r, _i: (pezzi, chiudi))


@pytest.mark.usefixtures("socket_enabled")
def test_invio_senza_lettura() -> None:
    with _con_vmc([], chiudi=True) as vmc, patch.object(motore, "PORT", vmc.porta):
        motore.Transport().send("127.0.0.1", b"VMSL prova")
    assert vmc.richieste == [b"VMSL prova"]


@pytest.mark.usefixtures("socket_enabled")
def test_nessuna_risposta_entro_il_tempo() -> None:
    with _con_vmc([], chiudi=False) as vmc, patch.object(motore, "PORT", vmc.porta):
        with pytest.raises(socket.timeout):
            motore.Transport().exchange("127.0.0.1", b"VMNM?", timeout=0.3)


@pytest.mark.usefixtures("socket_enabled")
def test_risposta_non_ascii() -> None:
    with _con_vmc([("VMNM Città".encode(), 0)]) as vmc, patch.object(motore, "PORT", vmc.porta):
        assert _codice(motore.Transport().command, "127.0.0.1", "VMNM?") == "invalid_vmc"


@pytest.mark.usefixtures("socket_enabled")
def test_rete_letta_dalla_vmc() -> None:
    risposta = ("VMSL " + "Casa".ljust(32, "*") + "segreta1".ljust(32, "*") + "192.168.001.060" + "05001"
                + "192.168.001.001" + "255.255.255.000" + "10").encode()
    with _con_vmc([(risposta, 0)]) as vmc, patch.object(motore, "PORT", vmc.porta):
        dati = motore.Transport().network_info("127.0.0.1")
    assert dati == {"ssid": "Casa", "router": "192.168.001.001", "subnet": "255.255.255.000"}
    assert "segreta1" not in json.dumps(dati)
    with _con_vmc([(b"VMSL corta", 0)]) as vmc, patch.object(motore, "PORT", vmc.porta):
        assert motore.Transport().network_info("127.0.0.1") == {}


def test_scheda_wifi_non_utilizzabile() -> None:
    """SO_BINDTODEVICE rifiutato (permessi o sistema senza l'opzione): errore chiaro, nessun invio."""

    class Presa:
        def __init__(self, *_args):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def settimeout(self, _secondi):
            pass

        def setsockopt(self, *_args):
            raise PermissionError("operazione non permessa")

        def connect(self, _indirizzo):
            raise AssertionError("non deve collegarsi")

    with patch.object(motore.socket, "socket", Presa):
        assert _codice(motore.Transport().exchange, "192.168.4.1", b"VMNM?", "wlan0") == "wifi_socket"


# ---------------------------------------------------------------- MAC dalla tabella ARP
ROUTE = (
    "Iface\tDestination\tGateway\tFlags\tRefCnt\tUse\tMetric\tMask\tMTU\tWindow\tIRTT\n"
    "wlan0\t00000000\t0101A8C0\t0003\t0\t0\t600\t00000000\t0\t0\t0\n"
    "wlan0\t0001A8C0\t00000000\t0001\t0\t0\t600\t00FFFFFF\t0\t0\t0\n"
    "end0\t0001A8C0\t00000000\t0001\t0\t0\t100\t00FFFFFF\t0\t0\t0\n"
    "corta\t00\n"
    "rotta\tZZZZ\t00000000\t0001\t0\t0\t0\t00FFFFFF\t0\t0\t0\n"
)
ARP = (
    "IP address       HW type     Flags       HW address            Mask     Device\n"
    "192.168.1.60     0x1         0x2         aa:bb:cc:dd:ee:01     *        end0\n"
    "192.168.1.61     0x1         0x0         aa:bb:cc:dd:ee:02     *        end0\n"
    "192.168.1.62     0x1         0x2         00:00:00:00:00:00     *        end0\n"
    "192.168.1.63     0x1         0x2         01:00:5e:00:00:01     *        end0\n"
    "192.168.1.64     0x1         0x2         zz:bb:cc:dd:ee:04     *        end0\n"
    "192.168.1.65     0x1         0x2         aa:bb:cc:dd:ee:05     *        wlan0\n"
    "breve\n"
)


def _file_di_sistema(route=ROUTE, arp=ARP):
    contenuti = {"/proc/net/route": route, "/proc/net/arp": arp}
    originale = Path.read_text

    def leggi(percorso, *args, **kwargs):
        if str(percorso) in contenuti:
            if contenuti[str(percorso)] is None:
                raise OSError("assente")
            return contenuti[str(percorso)]
        return originale(percorso, *args, **kwargs)

    return patch.object(motore.Path, "read_text", leggi)


def test_mac_del_vicino() -> None:
    trasporto = motore.Transport()
    with _file_di_sistema():
        # rete diretta con la metrica più bassa (end0), voce ARP completa
        assert trasporto.neighbor_mac("192.168.1.60") == "AA:BB:CC:DD:EE:01"
        assert trasporto.neighbor_mac("192.168.1.61") == ""  # voce incompleta
        assert trasporto.neighbor_mac("192.168.1.62") == ""  # MAC nullo
        assert trasporto.neighbor_mac("192.168.1.63") == ""  # multicast
        assert trasporto.neighbor_mac("192.168.1.64") == ""  # MAC non valido
        assert trasporto.neighbor_mac("192.168.1.65") == ""  # altra scheda
        assert trasporto.neighbor_mac("10.0.0.5") == ""  # solo attraverso il gateway
    with _file_di_sistema(route=None):
        assert trasporto.neighbor_mac("192.168.1.60") == ""
    with _file_di_sistema(route=ROUTE.splitlines()[0] + "\n"):
        assert trasporto.neighbor_mac("192.168.1.60") == ""
    assert trasporto.neighbor_mac("non-un-ip") == ""


# ---------------------------------------------------------------- reti di ricerca e ripristino
def test_reti_di_ricerca() -> None:
    info = {"interfaces": [
        {"interface": "end0", "connected": True, "ipv4": {"address": ["192.168.1.10/30", "fd00::1/64"]}},
        {"interface": "wlan0", "connected": True, "ipv4": {"ip_address": "203.0.113.5/30"}},
        {"interface": "usb0", "connected": False, "ipv4": {"address": ["10.0.0.2/30"]}},
    ]}
    assert motore.lan_targets(info) == ["192.168.1.9"]  # escluso l'IP del server
    # reti scritte a mano; 10.0.0.2 è del server (anche su una scheda scollegata)
    assert motore.lan_targets(info, "10.0.0.0/30, 192.168.1.8/30") == ["10.0.0.1", "192.168.1.9"]
    assert _codice(motore.lan_targets, info, "non-una-rete") == "invalid_subnet"
    assert _codice(motore.lan_targets, info, "192.168.0.0/23") == "subnet_too_large"
    assert _codice(motore.lan_targets, info, "8.8.8.0/24") == "no_lan"
    assert _codice(motore.lan_targets, {"interfaces": []}) == "no_lan"


def test_profilo_da_ripristinare() -> None:
    assert motore.restore_payload({"enabled": False, "wifi": {"ssid": "Casa"}}) == {"enabled": False}
    statico = {"enabled": True,
               "ipv4": {"method": "static", "ip_address": "192.168.1.20/24", "gateway": "192.168.1.1",
                        "nameservers": None, "ready": True},
               "ipv6": {"method": "auto", "address": ["fd00::2/64"], "gateway": "fd00::1", "addr_gen_mode": "eui64"},
               "wifi": {"ssid": "Aperta", "mode": "infrastructure", "auth": "open", "signal": 50}}
    assert motore.restore_payload(statico) == {
        "enabled": True,
        "ipv4": {"method": "static", "gateway": "192.168.1.1", "address": ["192.168.1.20/24"]},
        "ipv6": {"method": "auto", "addr_gen_mode": "eui64"},
        "wifi": {"ssid": "Aperta", "mode": "infrastructure", "auth": "open"},
    }
    assert motore.restore_payload(SCHEDA_CASA, "segreta123")["wifi"]["psk"] == "segreta123"
    assert _codice(motore.restore_payload, SCHEDA_CASA) == "restore_password_required"
    wep = {"enabled": True, "wifi": {"ssid": "Vecchia", "auth": "wep"}}
    assert _codice(motore.restore_payload, wep) == "unsupported_restore"


def test_password_hint_senza_dati() -> None:
    assert motore.password_hint(None) == ""
    assert motore.password_hint({"wifi": "testo"}) == ""
    assert motore.password_hint({"enabled": False}) == ""


# ---------------------------------------------------------------- Engine
def test_diagnose(tmp_path: Path) -> None:
    engine, _ = _engine(tmp_path, SupervisorFinto())
    engine.diagnose()
    dati = engine.status.data
    assert dati["success"] is True and dati["ethernet_interfaces"] == ["end0"]
    assert dati["wifi_interfaces"] == [{"interface": "wlan0", "enabled": False, "connected": False, "ssid": ""}]
    engine, _ = _engine(tmp_path, SupervisorFinto(scheda={"interface": "end1", "type": "ethernet"}, ethernet=""))
    engine.diagnose()
    assert engine.status.data["success"] is False and engine.status.data["stage"] == "Wi-Fi non disponibile"


def test_restore_illeggibile_non_spostabile(tmp_path: Path, caplog) -> None:
    (tmp_path / "restore.json").write_text("{troncato")
    engine, _ = _engine(tmp_path, SupervisorFinto())
    with patch.object(motore.os, "replace", side_effect=OSError("sola lettura")):
        assert _codice(engine.restore) == "restore_failed"
    assert "non spostato" in caplog.text
    assert (tmp_path / "restore.json").exists()


def test_restore_senza_file_non_fa_nulla(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    engine, _ = _engine(tmp_path, supervisor)
    engine.restore()
    assert supervisor.aggiornamenti == []


def test_rete_vmc_con_ip_indicato(tmp_path: Path) -> None:
    """ap_ip della richiesta sostituisce il gateway letto dal Supervisor."""
    supervisor = SupervisorFinto()
    engine, _ = _engine(tmp_path, supervisor)
    richiesta = {**motore.normalize_request(RICHIESTA), "ap_ip": "192.168.4.2"}
    with engine.ap_session(supervisor.info(), richiesta, "irraggiungibile") as (ip, scheda):
        assert (ip, scheda) == ("192.168.4.2", "wlan0")
    assert not (tmp_path / "restore.json").exists()


def test_rete_vmc_errore_prima_del_collegamento(tmp_path: Path) -> None:
    """Il primo avviso di stato fallisce: nessuna modifica di rete, restore.json tolto."""
    supervisor = SupervisorFinto()
    engine, _ = _engine(tmp_path, supervisor)
    with patch.object(engine.status, "emit", side_effect=OSError("disco pieno")):
        with pytest.raises(OSError):
            with engine.ap_session(supervisor.info(), motore.normalize_request(RICHIESTA), "x"):
                pass
    assert supervisor.aggiornamenti == [] and not (tmp_path / "restore.json").exists()


def test_rete_vmc_ripristino_non_tornato(tmp_path: Path) -> None:
    """Il Wi-Fi del server non torna alla rete di prima entro 25 s: restore_failed con la
    nota sulla password, restore.json conservato."""
    supervisor = SupervisorFinto(scheda=json.loads(json.dumps(SCHEDA_CASA)), torna=False)
    engine, _ = _engine(tmp_path, supervisor, TrasportoRete())
    with pytest.raises(Failure) as errore:
        engine.run({**RICHIESTA, "home_ssid": "Altra", "restore_password": "passwordserver"})
    assert errore.value.code == "restore_failed"
    assert "La password della rete Casa potrebbe essere sbagliata." in errore.value.message
    assert (tmp_path / "restore.json").exists()


def test_rete_vmc_visibile(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    engine, orologio = _engine(tmp_path, supervisor)
    assert engine.ap_visible("VMC_12345678", 30) is True and orologio.t == 1000.0
    assert engine.ap_visible("VMC_00000000", 12) is False and orologio.t == 1015.0
    supervisor.accesspoints = lambda _i: (_ for _ in ()).throw(Failure("scan_failed", "x"))
    assert engine.ap_visible("VMC_12345678", 5) is False
    engine, _ = _engine(tmp_path, SupervisorFinto(scheda={"interface": "end1", "type": "ethernet"}))
    assert engine.ap_visible("VMC_12345678", 5) is None
    supervisor.info = lambda: (_ for _ in ()).throw(Failure("supervisor_unavailable", "x"))
    engine, _ = _engine(tmp_path, supervisor)
    assert engine.ap_visible("VMC_12345678", 5) is None


def test_ricerca_ignora_chi_non_risponde(tmp_path: Path) -> None:
    class Misto:
        def identify(self, ip, interface=""):
            if ip.endswith(".1"):
                raise Failure("invalid_vmc", "non è una VMC")
            if ip.endswith(".2"):
                raise OSError("nessuna risposta")
            return "Altra" if ip.endswith(".3") else "Prova"

        def neighbor_mac(self, ip):
            return "AA:BB:CC:DD:EE:0" + ip[-1]

    engine, _ = _engine(tmp_path, SupervisorFinto(), Misto())
    indirizzi = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]
    assert engine.discover(indirizzi, "", "") == [
        {"ip": "192.168.1.3", "name": "Altra", "mac": "AA:BB:CC:DD:EE:03"},
        {"ip": "192.168.1.4", "name": "Prova", "mac": "AA:BB:CC:DD:EE:04"}]
    assert engine.discover(indirizzi, "Prova", "") == [{"ip": "192.168.1.4", "name": "Prova", "mac": "AA:BB:CC:DD:EE:04"}]
    assert engine.discover(indirizzi, "Prova", "AA:BB:CC:DD:EE:09") == []


def test_scan_casi(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    supervisor.accesspoints = lambda _i: [{"ssid": "VMC_1", "signal": None, "frequency": None},
                                          {"ssid": None, "signal": 80}]
    engine, _ = _engine(tmp_path, supervisor)
    engine.scan()
    assert json.loads((tmp_path / "scan.json").read_text()) == {
        "vmc_networks": [{"ssid": "VMC_1", "signal": 0, "band": ""}], "wifi_networks": []}
    assert "Trovata la rete VMC_1" in engine.status.data["message"]
    supervisor.accesspoints = lambda _i: [{"ssid": "Casa", "signal": 50, "frequency": 2412}]
    engine.scan()
    assert engine.status.data["success"] is False and "Nessuna rete VMC" in engine.status.data["message"]
    supervisor.accesspoints = lambda _i: (_ for _ in ()).throw(Failure("supervisor_error", "x"))
    assert _codice(engine.scan) == "scan_failed"


def test_verifica_aggiorna_solo_l_ip(tmp_path: Path) -> None:
    _identita(tmp_path, extra="resta")
    engine, _ = _engine(tmp_path, SupervisorFinto(), TrasportoVerifica())
    engine.verify({"ip": "192.168.1.70", "ap_ssid": "VMC_12345678"})
    identita = json.loads((tmp_path / "identity.json").read_text())
    assert identita == {"ap_ssid": "VMC_12345678", "ip": "192.168.1.70", "name": "Prova",
                        "mac": "AA:BB:CC:DD:EE:01", "extra": "resta"}


def test_stato_letto_dai_file(tmp_path: Path) -> None:
    assert motore.read_status(tmp_path)["stage"] == "In attesa"
    _identita(tmp_path)
    motore.atomic_json(tmp_path / "scan.json", {"vmc_networks": [{"ssid": "VMC_1"}]})
    (tmp_path / "status.json").write_text("{rotto")
    dati = motore.read_status(tmp_path)
    assert dati["configured_ip"] == "192.168.1.60" and dati["configured_mac"] == "AA:BB:CC:DD:EE:01"
    assert dati["vmc_networks"] == [{"ssid": "VMC_1"}] and dati["wifi_networks"] == []


# ---------------------------------------------------------------- prima_installazione
def test_stato_senza_barra(tmp_path: Path) -> None:
    stato = pi._Stato(tmp_path, None)
    stato.emit("Prova", 40, "messaggio")
    assert json.loads((tmp_path / "status.json").read_text())["progress"] == 40
    barra: list[int] = []
    pi._Stato(tmp_path, barra.append).emit("Prova", None)
    assert barra == [0]


def test_esegui_cerca_la_rete_dal_supervisor(tmp_path: Path) -> None:
    """configure senza lan_cidr: la rete di ricerca arriva dal Supervisor; se il Supervisor
    non risponde decide il motore. Un ripristino in sospeso si fa prima."""
    ricevute: list = []

    class Motore:
        def __init__(self, info):
            self.root = pi.cartella(str(tmp_path))
            self.supervisor = type("S", (), {"info": staticmethod(info)})()
            self.status = type("St", (), {"data": {"stage": "Completato"}})()
            self.ripristini = 0

        def restore(self):
            self.ripristini += 1

        def run(self, dati):
            ricevute.append(dati)

    ampia = {"interfaces": [{"connected": True, "ipv4": {"address": ["192.168.0.20/22"]}}]}
    finto = Motore(lambda: ampia)
    finto.root.mkdir(parents=True)
    (finto.root / "restore.json").write_text("{}")
    with patch.object(pi, "_motore", return_value=finto):
        assert pi.esegui(str(tmp_path), "configure", {"home_ssid": "Casa"}) == {"stage": "Completato"}
    assert finto.ripristini == 1 and ricevute[-1]["lan_cidr"] == "192.168.0.0/24"

    def rotto():
        raise Failure("supervisor_unavailable", "x")

    with patch.object(pi, "_motore", return_value=Motore(rotto)):
        pi.esegui(str(tmp_path), "configure", {})
    assert ricevute[-1] == {}  # nessuna rete: la sceglie il motore
    with patch.object(pi, "_motore", return_value=Motore(rotto)):
        pi.esegui(str(tmp_path), "configure", {"lan_cidr": "10.0.0.0/24"})
    assert ricevute[-1] == {"lan_cidr": "10.0.0.0/24"}
    with patch.object(pi, "_motore", return_value=Motore(rotto)):
        assert _codice(pi.esegui, str(tmp_path), "sconosciuta") == "invalid_action"


def test_stato_e_ultima_vmc(tmp_path: Path) -> None:
    radice = pi.cartella(str(tmp_path))
    assert pi.stato(str(tmp_path))["stage"] == "In attesa"
    assert pi.ultima_vmc(str(tmp_path)) == {} and pi.ripristino_in_sospeso(str(tmp_path)) is False
    _identita(radice)
    (radice / "restore.json").write_text("{}")
    assert pi.ultima_vmc(str(tmp_path))["ip"] == "192.168.1.60"
    assert pi.ripristino_in_sospeso(str(tmp_path)) is True


def test_rete_del_server(tmp_path: Path) -> None:
    def con(info):
        return patch.object(pi.motore, "Supervisor", return_value=type("S", (), {"info": staticmethod(info)})())

    collegato = {"interfaces": [{"type": "ethernet", "connected": True},
                                {"type": "wireless", "connected": False, "wifi": {"ssid": "Spenta"}},
                                {"type": "wireless", "connected": True, "wifi": {"ssid": "Casa"}}]}
    with con(lambda: collegato):
        assert pi.rete_del_server(str(tmp_path)) == "Casa"
    with con(lambda: {"interfaces": [{"type": "wireless", "connected": True}]}):
        assert pi.rete_del_server(str(tmp_path)) == ""
    with con(lambda: {"interfaces": []}):
        assert pi.rete_del_server(str(tmp_path)) == ""

    def rotto():
        raise Failure("supervisor_unavailable", "x")

    with con(rotto):
        assert pi.rete_del_server(str(tmp_path)) == ""


def test_rete_di_ricerca_casi() -> None:
    info = {"interfaces": [
        {"connected": False, "ipv4": {"address": ["10.1.0.2/16"]}},
        {"connected": True, "ipv4": {"address": ["non-un-indirizzo", "fd00::5/64", "203.0.113.9/16"]}},
        {"connected": True, "ipv4": {"address": ["192.168.1.20/24"]}},
    ]}
    assert pi.rete_di_ricerca(info) == ""  # solo /24 o più piccole: cerca il motore
    info["interfaces"].append({"connected": True, "ipv4": {"address": ["172.16.5.9/16", "172.16.5.10/16"]}})
    assert pi.rete_di_ricerca(info) == "192.168.1.0/24,172.16.5.0/24"


def test_rete_da_ripristinare(tmp_path: Path) -> None:
    def con(info):
        return patch.object(pi.motore, "Supervisor", return_value=type("S", (), {"info": staticmethod(info)})())

    with con(lambda: {"interfaces": [SCHEDA_CASA]}):
        assert pi.rete_da_ripristinare(str(tmp_path)) == "Casa"
    with con(lambda: {"interfaces": [{"interface": "wlan1", "type": "wireless", "enabled": False}]}):
        assert pi.rete_da_ripristinare(str(tmp_path)) == ""
    with con(lambda: {"interfaces": []}):
        assert pi.rete_da_ripristinare(str(tmp_path)) == ""


def test_aggiorna_ip(tmp_path: Path) -> None:
    radice = pi.cartella(str(tmp_path))
    pi.aggiorna_ip(str(tmp_path), "192.168.1.60", "192.168.1.70")  # nessuna identità: nulla
    assert not (radice / "identity.json").exists()
    _identita(radice)
    pi.aggiorna_ip(str(tmp_path), "192.168.1.99", "192.168.1.70")  # altra VMC: invariata
    assert pi.ultima_vmc(str(tmp_path))["ip"] == "192.168.1.60"
    pi.aggiorna_ip(str(tmp_path), "192.168.1.60", "192.168.1.70")
    assert pi.ultima_vmc(str(tmp_path))["ip"] == "192.168.1.70"


class _TrasportoAp:
    def __init__(self, nomi, invio=None):
        self.nomi, self.invio, self.inviati = list(nomi), invio, []

    def identify(self, ip, interface=""):
        valore = self.nomi.pop(0) if self.nomi else OSError("assente")
        if isinstance(valore, Exception):
            raise valore
        return valore

    def send(self, ip, packet, interface=""):
        if self.invio:
            raise self.invio
        self.inviati.append(packet)


def _rimanda(tmp_path, trasporto, attesa=10.0):
    with patch.object(pi.motore, "Transport", return_value=trasporto), patch.object(pi.time, "sleep"):
        return pi.rimanda_in_access_point(str(tmp_path), "192.168.1.60", attesa=attesa, pausa=0)


def test_rimanda_in_access_point_errori(tmp_path: Path, caplog) -> None:
    assert _codice(_rimanda, tmp_path, _TrasportoAp([OSError("x")])) == "vmc_unreachable"
    assert _codice(_rimanda, tmp_path, _TrasportoAp(["Prova"], invio=OSError("x"))) == "vmc_unreachable"
    with patch.object(pi.time, "monotonic", side_effect=[0, 0, 5, 11, 11]):
        assert _codice(_rimanda, tmp_path, _TrasportoAp(["Prova", "Prova", "Prova"])) == "ap_not_applied"
    assert _codice(_rimanda, tmp_path, _TrasportoAp(["Prova"], invio=RuntimeError("inatteso"))) == "communication_error"
    assert "interrotto da un errore inatteso" in caplog.text
    assert pi._BLOCCO.acquire(blocking=False)  # il blocco non resta preso
    pi._BLOCCO.release()


def test_rimanda_in_access_point_identita_di_un_altra(tmp_path: Path) -> None:
    """L'identità salvata è di un'altra VMC: resta."""
    radice = pi.cartella(str(tmp_path))
    _identita(radice, ip="192.168.1.99")
    assert _rimanda(tmp_path, _TrasportoAp(["Prova", OSError(), Failure("invalid_vmc", "x")])) == "Prova"
    assert (radice / "identity.json").exists()


def test_esegui_verifica_e_recupero(tmp_path: Path) -> None:
    azioni: list = []

    class Motore:
        status = type("St", (), {"data": {"stage": "Completato"}})()

        def verify(self, dati):
            azioni.append(("verify", dati))

        def recover(self):
            azioni.append(("recover", None))

    with patch.object(pi, "_motore", return_value=Motore()):
        pi.esegui(str(tmp_path), "verify")
        pi.esegui(str(tmp_path), "verify", {"ip": "192.168.1.70"})
        pi.esegui(str(tmp_path), "recover")
    assert azioni == [("verify", {}), ("verify", {"ip": "192.168.1.70"}), ("recover", None)]
