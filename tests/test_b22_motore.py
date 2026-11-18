"""b22: motore Wi-Fi (motore_installa_vmc.py) e prima_installazione.py.

- B-6: risposta a VMNM? spezzata in più segmenti TCP (VMC finta su 127.0.0.1);
- B-8: restore.json illeggibile messo da parte, causa vera nel log;
- M-3: restore, recover, choose_wifi, run, verify, password_hint, lock di esegui.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
import socket
import threading
import time
from unittest.mock import patch

import pytest

from custom_components.vmc_master import motore_installa_vmc as motore
from custom_components.vmc_master import prima_installazione as pi

Failure = motore.Failure


# ---------------------------------------------------------------- VMC finta TCP
class VmcTcp:
    """VMC finta sulla porta TCP di 127.0.0.1. risponde(richiesta, indice) restituisce i
    pezzi da inviare come (byte, pausa prima del pezzo) e se chiudere poi la connessione."""

    def __init__(self, risponde):
        self.risponde = risponde
        self.richieste: list[bytes] = []
        self._fine = threading.Event()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("127.0.0.1", 0))
        self._server.listen(8)
        self._server.settimeout(0.05)
        self.porta = self._server.getsockname()[1]
        self._thread = threading.Thread(target=self._accetta, daemon=True)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *_args):
        self._fine.set()
        self._thread.join(2)
        self._server.close()

    def _accetta(self):
        while not self._fine.is_set():
            try:
                conn, _ = self._server.accept()
            except (socket.timeout, OSError):
                continue
            threading.Thread(target=self._servi, args=(conn,), daemon=True).start()

    def _servi(self, conn):
        with conn:
            conn.settimeout(1)
            try:
                richiesta = conn.recv(256)
            except OSError:
                return
            indice = len(self.richieste)
            self.richieste.append(richiesta)
            pezzi, chiudi = self.risponde(richiesta, indice)
            try:
                for dati, pausa in pezzi:
                    time.sleep(pausa)
                    conn.sendall(dati)
                if not chiudi:
                    # connessione lasciata aperta: il motore non deve attendere oltre il dovuto
                    self._fine.wait(3)
            except OSError:
                return


def _identifica(pezzi, chiudi=True):
    with VmcTcp(lambda _r, _i: (pezzi, chiudi)) as vmc, patch.object(motore, "PORT", vmc.porta):
        inizio = time.monotonic()
        try:
            return motore.Transport().identify("127.0.0.1"), time.monotonic() - inizio
        except Failure as errore:
            return errore, time.monotonic() - inizio


@pytest.mark.usefixtures("socket_enabled")
def test_nome_in_piu_segmenti() -> None:
    """B-6: la risposta a VMNM? arriva a pezzi distanziati più di 0,12 s: il nome è intero."""
    nome, _ = _identifica([(b"VMNM", 0), (b" Zona Giorno", 0.3)])
    assert nome == "Zona Giorno"
    nome, _ = _identifica([(b"VMNM Pr", 0), (b"ova****", 0.3)], chiudi=False)
    assert nome == "Prova"
    nome, _ = _identifica([(b"VM", 0), (b"NM ", 0.3), (b"Prova", 0.3), (b"\r\n", 0.3)], chiudi=False)
    assert nome == "Prova"
    nome, _ = _identifica([(b"VMNM ", 0), (b"Prova\r\n", 0.5)])
    assert nome == "Prova"


@pytest.mark.usefixtures("socket_enabled")
def test_nome_intero_resta_veloce() -> None:
    """Risposta completa (a capo o asterischi) con la connessione aperta: si attende solo la
    pausa di 0,12 s, come prima. Un dispositivo che non è una VMC si scarta subito."""
    nome, durata = _identifica([(b"VMNM Prova\r\n", 0)], chiudi=False)
    assert nome == "Prova" and durata < 1
    nome, durata = _identifica([(b"VMNM Prova*******", 0)], chiudi=False)
    assert nome == "Prova" and durata < 1
    nome, durata = _identifica([(b"VMNM Prova", 0)])  # chiusura della connessione
    assert nome == "Prova" and durata < 1
    errore, durata = _identifica([(b"HTTP/1.1 400", 0)], chiudi=False)
    assert isinstance(errore, Failure) and errore.code == "invalid_vmc" and durata < 1
    errore, durata = _identifica([(b"VMNM *******\r\n", 0)], chiudi=False)
    assert isinstance(errore, Failure) and errore.code == "invalid_vmc" and durata < 1


@pytest.mark.usefixtures("socket_enabled")
def test_nome_incompleto_entro_il_tempo_massimo() -> None:
    """Una risposta che resta a metà non blocca: dopo il tempo massimo (2 s dall'invio)
    vale quello che è arrivato."""
    nome, durata = _identifica([(b"VMNM Pr", 0)], chiudi=False)
    assert nome == "Pr" and 1.5 < durata < 2.9


def test_risposta_completa() -> None:
    complete = motore.name_answer_complete
    for parziale in (b"", b"V", b"VMNM", b"VMNM ", b"VMNM Pr", b"\x00VMNM Zona "):
        assert not complete(parziale), parziale
    for intera in (b"VMNM Prova\r", b"VMNM Prova\n", b"VMNM Prova\x00", b"VMNM Prova***", b"OK", b"XYZ", b"VMGI 1"):
        assert complete(intera), intera


@pytest.mark.usefixtures("socket_enabled")
def test_elimina_dalla_rete_con_prima_risposta_spezzata(tmp_path: Path) -> None:
    """B-6: «Elimina anche dalla rete» con la prima risposta spezzata e la VMC che resta
    sulla rete di casa: nessuna conferma falsa."""

    def risponde(richiesta, indice):
        if not richiesta.startswith(b"VMNM?"):
            return [], True  # comando Access Point non applicato
        if indice == 0:
            return [(b"VMNM Pr", 0), (b"ova*****", 0.3)], True
        return [(b"VMNM Prova*****", 0)], True

    with VmcTcp(risponde) as vmc, patch.object(motore, "PORT", vmc.porta):
        with pytest.raises(Failure) as errore:
            pi.rimanda_in_access_point(str(tmp_path), "127.0.0.1", attesa=1.0, pausa=0.1)
    assert errore.value.code == "ap_not_applied"
    assert vmc.richieste[1] == motore.access_point_packet()


class TrasportoAp:
    """identify risponde secondo la sequenza (un'eccezione = nessuna risposta), poi ripete l'ultima."""

    def __init__(self, sequenza):
        self.sequenza = list(sequenza)
        self.inviati = []

    def identify(self, ip, interface=""):
        valore = self.sequenza.pop(0) if len(self.sequenza) > 1 else self.sequenza[0]
        if isinstance(valore, Exception):
            raise valore
        return valore

    def send(self, ip, packet, interface=""):
        self.inviati.append(packet)


def test_una_sola_assenza_non_basta(tmp_path: Path) -> None:
    """M15: una sola risposta mancata non vuol dire che la VMC ha lasciato la rete."""
    trasporto = TrasportoAp(["Prova", "Prova", OSError(), "Prova"])
    with patch.object(pi.motore, "Transport", return_value=trasporto), pytest.raises(Failure) as errore:
        pi.rimanda_in_access_point(str(tmp_path), "192.168.1.161", attesa=0.5, pausa=0.02)
    assert errore.value.code == "ap_not_applied"
    trasporto = TrasportoAp(["Prova", OSError(), OSError()])
    with patch.object(pi.motore, "Transport", return_value=trasporto):
        assert pi.rimanda_in_access_point(str(tmp_path), "192.168.1.161", attesa=0.5, pausa=0.02) == "Prova"


# ---------------------------------------------------------------- lock di esegui
def test_una_procedura_alla_volta(tmp_path: Path) -> None:
    """M08: esegui e rimanda_in_access_point con una procedura già in corso -> in_corso."""
    assert pi._BLOCCO.acquire(blocking=False)
    try:
        with pytest.raises(Failure) as errore:
            pi.esegui(str(tmp_path), "recover")
        assert errore.value.code == "in_corso"
        with pytest.raises(Failure) as errore:
            pi.rimanda_in_access_point(str(tmp_path), "192.168.1.161")
        assert errore.value.code == "in_corso"
    finally:
        pi._BLOCCO.release()
    # il blocco si libera anche dopo un errore
    with pytest.raises(Failure):
        pi.esegui(str(tmp_path), "azione_sconosciuta")
    assert pi.esegui(str(tmp_path), "recover")["success"] is True
    assert not pi._BLOCCO.locked()


def test_esegui_insieme_da_due_thread(tmp_path: Path) -> None:
    """Due esegui nello stesso momento: il secondo esce subito con in_corso."""
    entrato, libera = threading.Event(), threading.Event()
    esiti: list = []

    def recover_lento(self):
        entrato.set()
        libera.wait(5)

    with patch.object(motore.Engine, "recover", recover_lento):
        primo = threading.Thread(target=lambda: esiti.append(pi.esegui(str(tmp_path), "recover")))
        primo.start()
        assert entrato.wait(5)
        with pytest.raises(Failure) as errore:
            pi.esegui(str(tmp_path), "recover")
        libera.set()
        primo.join(5)
    assert errore.value.code == "in_corso" and len(esiti) == 1


def test_errore_inatteso_nel_log(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """B-8: un'eccezione inattesa diventa communication_error, ma la causa vera è nel log."""

    def scan_rotto(self):
        raise KeyError("payload")

    with patch.object(motore.Engine, "scan", scan_rotto), caplog.at_level(logging.ERROR):
        with pytest.raises(Failure) as errore:
            pi.esegui(str(tmp_path), "scan")
    assert errore.value.code == "communication_error"
    assert isinstance(errore.value.__cause__, KeyError)
    record = next(r for r in caplog.records if r.name == pi.__name__)
    assert record.exc_info and record.exc_info[0] is KeyError and "scan" in record.getMessage()


# ---------------------------------------------------------------- Supervisor finto
class Orologio:
    def __init__(self):
        self.t = 1000.0

    def now(self):
        return self.t

    def sleep(self, secondi):
        self.t += secondi


class SupervisorFinto:
    """Una scheda Wi-Fi: si collega alla rete VMC con ap_profile e torna com'era col ripristino."""

    def __init__(self, scheda=None, ap_ip="192.168.4.1", torna=True, rifiuta_ripristino=False, ethernet="192.168.1.10/24"):
        self.scheda = scheda or {"interface": "wlan0", "type": "wireless", "enabled": False, "connected": False}
        self.originale = json.loads(json.dumps(self.scheda))
        self.ap_ip, self.torna, self.rifiuta_ripristino = ap_ip, torna, rifiuta_ripristino
        self.ethernet = ethernet
        self.aggiornamenti: list = []

    def info(self):
        interfacce = [self.scheda]
        if self.ethernet:
            interfacce.append({"interface": "end0", "type": "ethernet", "connected": True,
                               "ipv4": {"address": [self.ethernet]}})
        return {"interfaces": interfacce}

    def update(self, interface, payload):
        self.aggiornamenti.append((interface, payload))
        wifi = payload.get("wifi") or {}
        if wifi.get("psk") and wifi.get("ssid", "").startswith("VMC_") and payload["ipv4"].get("route_metric") == 4096:
            self.scheda = {"interface": interface, "type": "wireless", "enabled": True, "connected": True,
                           "wifi": {"ssid": wifi["ssid"]}, "ipv4": {"gateway": self.ap_ip}}
            return {}
        if self.rifiuta_ripristino:
            raise Failure("supervisor_error", "Il Supervisor non ha completato l'operazione di rete.")
        if self.torna:
            self.scheda = json.loads(json.dumps(self.originale))
        return {}

    def accesspoints(self, interface):
        return [{"ssid": "VMC_12345678", "signal": 40, "frequency": 2412},
                {"ssid": "VMC_12345678", "signal": 70, "frequency": 2437},
                {"ssid": "VMC_87654321", "signal": 20, "frequency": 2412},
                {"ssid": "Casa", "signal": 90, "frequency": 5180},
                {"ssid": "", "signal": 99}]


def _engine(tmp_path, supervisor, transport=None, verify_seconds=90):
    orologio = Orologio()
    engine = motore.Engine(tmp_path, supervisor=supervisor, transport=transport,
                           sleep=orologio.sleep, monotonic=orologio.now, verify_seconds=verify_seconds)
    return engine, orologio


SCHEDA_CASA = {"interface": "wlan0", "type": "wireless", "enabled": True, "connected": True,
               "wifi": {"ssid": "Casa", "mode": "infrastructure", "auth": "wpa-psk"},
               "ipv4": {"method": "auto", "address": ["192.168.1.20/24"], "gateway": "192.168.1.1"},
               "ipv6": {"method": "disabled"}}
PAYLOAD_CASA = {"enabled": True, "ipv4": {"method": "auto"}, "ipv6": {"method": "disabled"},
                "wifi": {"ssid": "Casa", "mode": "infrastructure", "auth": "wpa-psk", "psk": "passwordcasa"}}


def _scrivi_ripristino(tmp_path, connected=True):
    motore.atomic_json(tmp_path / "restore.json", {"interface": "wlan0", "payload": PAYLOAD_CASA,
                                                   "connected": connected, "ssid": "Casa"})


# ---------------------------------------------------------------- restore / recover
def test_restore_riuscito(tmp_path: Path) -> None:
    supervisor = SupervisorFinto(scheda={"interface": "wlan0", "type": "wireless", "enabled": True,
                                         "connected": False, "wifi": {"ssid": "VMC_12345678"}})
    supervisor.originale = json.loads(json.dumps(SCHEDA_CASA))
    _scrivi_ripristino(tmp_path)
    engine, orologio = _engine(tmp_path, supervisor)
    engine.restore()
    assert supervisor.aggiornamenti == [("wlan0", PAYLOAD_CASA)]
    assert not (tmp_path / "restore.json").exists()
    assert orologio.t == 1000.0  # già tornato alla rete: nessuna attesa
    assert engine.status.data["stage"] == "Ripristino rete server"
    engine.restore()  # nessun file: non fa nulla
    assert len(supervisor.aggiornamenti) == 1


def test_restore_non_riuscito_con_password(tmp_path: Path) -> None:
    """Il server non torna alla sua rete: restore_failed col suggerimento sulla password,
    restore.json conservato; poi recover riesce."""
    supervisor = SupervisorFinto(scheda={"interface": "wlan0", "type": "wireless", "enabled": True,
                                         "connected": True, "wifi": {"ssid": "VMC_12345678"}}, torna=False)
    _scrivi_ripristino(tmp_path)
    engine, orologio = _engine(tmp_path, supervisor)
    with pytest.raises(Failure) as errore:
        engine.recover()
    assert errore.value.code == "restore_failed"
    assert "La password della rete Casa potrebbe essere sbagliata." in errore.value.message
    assert 1025 <= orologio.t <= 1027  # 25 s di attesa
    assert (tmp_path / "restore.json").exists()
    assert engine.status.data["success"] is False
    supervisor.torna, supervisor.originale = True, json.loads(json.dumps(SCHEDA_CASA))
    engine.recover()
    assert not (tmp_path / "restore.json").exists()
    assert engine.status.data["stage"] == "Rete server ripristinata"
    assert engine.status.data["success"] is True and engine.status.data["progress"] == 100


def test_restore_scheda_non_collegata(tmp_path: Path) -> None:
    """Scheda che prima non era collegata: nessuna attesa della rete."""
    supervisor = SupervisorFinto(torna=False)
    _scrivi_ripristino(tmp_path, connected=False)
    engine, orologio = _engine(tmp_path, supervisor)
    engine.recover()
    assert orologio.t == 1000.0 and not (tmp_path / "restore.json").exists()


@pytest.mark.parametrize("contenuto", [
    '{"interface": "wlan0", "payload": {"enab',   # troncato
    '["wlan0"]',                                  # non un dizionario
    '{"interface": "wlan0"}',                     # senza payload
    '{"interface": "", "payload": {}}',           # senza interfaccia
    '{"interface": "wlan0", "payload": "x"}',     # payload di forma inattesa
    b"\xff\xfe\x00",                              # byte non UTF-8
])
def test_restore_illeggibile(tmp_path: Path, caplog: pytest.LogCaptureFixture, contenuto) -> None:
    """B-8: restore.json illeggibile: messo da parte, causa nel log, la procedura dopo parte."""
    radice = pi.cartella(str(tmp_path))
    radice.mkdir()
    file = radice / "restore.json"
    file.write_bytes(contenuto if isinstance(contenuto, bytes) else contenuto.encode())
    with caplog.at_level(logging.WARNING), pytest.raises(Failure) as errore:
        pi.esegui(str(tmp_path), "recover")
    assert errore.value.code == "restore_failed"
    assert "messo da parte" in errore.value.message
    assert not file.exists() and (radice / "restore.json.illeggibile").exists()
    assert any("restore.json.illeggibile" in r.getMessage() for r in caplog.records if r.name == motore.__name__)
    assert pi.ripristino_in_sospeso(str(tmp_path)) is False
    # secondo tentativo: nessun ripristino in sospeso, la procedura parte
    assert pi.esegui(str(tmp_path), "recover")["success"] is True


def test_restore_illeggibile_prima_del_collegamento(tmp_path: Path) -> None:
    """configure con restore.json illeggibile: il Wi-Fi non viene toccato, al secondo
    tentativo il file non blocca più."""
    radice = pi.cartella(str(tmp_path))
    radice.mkdir()
    (radice / "restore.json").write_text("{")
    supervisor = SupervisorFinto()
    with patch.object(pi.motore, "Supervisor", return_value=supervisor), pytest.raises(Failure) as errore:
        pi.esegui(str(tmp_path), "configure", dict(RICHIESTA))
    assert errore.value.code == "restore_failed" and supervisor.aggiornamenti == []
    assert not (radice / "restore.json").exists()


def test_password_hint() -> None:
    assert motore.password_hint(PAYLOAD_CASA) == " La password della rete Casa potrebbe essere sbagliata."
    assert motore.password_hint({"enabled": True, "wifi": {"ssid": "Casa", "auth": "open"}}) == ""
    assert motore.password_hint({"enabled": False}) == ""
    assert motore.password_hint({"wifi": "Casa"}) == ""
    assert motore.password_hint(None) == ""


def test_choose_wifi() -> None:
    engine = motore.Engine.__new__(motore.Engine)
    with pytest.raises(Failure) as errore:
        engine.choose_wifi({"interfaces": [{"interface": "end0", "type": "ethernet"}]}, "")
    assert errore.value.code == "no_wifi"
    libera = {"interface": "wlan1", "type": "wireless", "enabled": False, "connected": False}
    assert engine.choose_wifi({"interfaces": [SCHEDA_CASA]}, "") is SCHEDA_CASA
    # due schede: si preferisce quella libera, per non togliere il server dalla sua rete
    assert engine.choose_wifi({"interfaces": [SCHEDA_CASA, libera]}, "") is libera
    assert engine.choose_wifi({"interfaces": [SCHEDA_CASA, libera]}, "wlan0") is SCHEDA_CASA
    with pytest.raises(Failure):
        engine.choose_wifi({"interfaces": [SCHEDA_CASA, libera]}, "wlan9")


# ---------------------------------------------------------------- run
RICHIESTA = {"home_ssid": "Casa", "home_password": "passwordcasa", "ap_ssid": "VMC_12345678",
             "ap_password": "12345678", "final_ip": "192.168.1.60"}


class TrasportoRete:
    """VMC che compare sulla rete di casa solo dopo aver ricevuto la rete."""

    def __init__(self, nome="Prova", mac="AA:BB:CC:DD:EE:01", gia_presente=None, invio_rotto=False, compare=True,
                 ip_vmc="192.168.1.60"):
        self.nome, self.mac, self.ip_vmc = nome, mac, ip_vmc
        self.gia_presente, self.invio_rotto, self.compare = gia_presente, invio_rotto, compare
        self.inviati: list = []
        self.identificazioni: list = []

    def identify(self, ip, interface=""):
        self.identificazioni.append((ip, interface))
        if interface == "wlan0" and ip == "192.168.4.1":
            return self.nome
        if self.gia_presente and not self.inviati:
            return self.gia_presente
        if self.inviati and self.compare and ip == self.ip_vmc:
            return self.nome
        raise OSError("nessuna risposta")

    def neighbor_mac(self, ip):
        return self.mac

    def network_info(self, ip):
        return {"ssid": "Casa", "router": "192.168.1.1", "subnet": "255.255.255.0"}

    def send(self, ip, packet, interface=""):
        if self.invio_rotto:
            raise OSError("connessione chiusa")
        self.inviati.append((ip, packet, interface))


def test_run_completo(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    trasporto = TrasportoRete()
    engine, _ = _engine(tmp_path, supervisor, trasporto)
    engine.run(dict(RICHIESTA))
    assert trasporto.inviati == [("192.168.4.1", motore.network_packet("Casa", "passwordcasa"), "wlan0")]
    assert supervisor.aggiornamenti == [
        ("wlan0", motore.ap_profile("VMC_12345678", "12345678")),
        ("wlan0", {"enabled": False}),
    ]
    assert not (tmp_path / "restore.json").exists()
    assert json.loads((tmp_path / "identity.json").read_text()) == {
        "ap_ssid": "VMC_12345678", "ip": "192.168.1.60", "name": "Prova", "mac": "AA:BB:CC:DD:EE:01"}
    dati = engine.status.data
    assert dati["success"] is True and dati["stage"] == "Completato" and dati["network_sent"] is True
    assert dati["vmc_ip"] == "192.168.1.60" and dati["vmc_mac"] == "AA:BB:CC:DD:EE:01"
    assert dati["vmc_network_ssid"] == "Casa" and dati["vmc_router"] == "192.168.1.1"
    assert dati["mac_source"] == "LAN" and "MAC non è rilevabile" not in dati["message"]


def test_run_senza_mac_e_con_ricerca_in_rete(tmp_path: Path) -> None:
    """Senza IP riservato si cerca nella rete del server; senza MAC lo dice il messaggio."""
    supervisor = SupervisorFinto()
    trasporto = TrasportoRete(mac="", ip_vmc="192.168.1.2")
    engine, _ = _engine(tmp_path, supervisor, trasporto)
    with patch.object(engine, "discover", wraps=engine.discover) as ricerca:
        engine.run({**RICHIESTA, "final_ip": "", "lan_cidr": "192.168.1.0/30"})
    assert ricerca.call_args_list[0].args[0] == ["192.168.1.1", "192.168.1.2"]
    assert engine.status.data["success"] is True and engine.status.data["mac_source"] == ""
    assert "MAC non è rilevabile" in engine.status.data["message"]


def test_run_errore_durante_invio_ripristina_il_wifi(tmp_path: Path) -> None:
    """Errore mentre il server è sulla rete VMC: il Wi-Fi torna alla rete di prima."""
    supervisor = SupervisorFinto(scheda=json.loads(json.dumps(SCHEDA_CASA)))
    trasporto = TrasportoRete(invio_rotto=True)
    engine, _ = _engine(tmp_path, supervisor, trasporto)
    with pytest.raises(OSError):
        engine.run(dict(RICHIESTA))
    assert supervisor.scheda["wifi"]["ssid"] == "Casa"
    ripristino = supervisor.aggiornamenti[-1]
    assert ripristino[0] == "wlan0" and ripristino[1]["wifi"]["psk"] == "passwordcasa"  # stessa rete di casa
    assert not (tmp_path / "restore.json").exists()
    assert engine.status.data["network_sent"] is False


def test_run_ripristino_rifiutato(tmp_path: Path) -> None:
    """Il Supervisor rifiuta il ripristino: restore_failed con suggerimento sulla password e
    restore.json conservato per il recupero automatico."""
    supervisor = SupervisorFinto(scheda=json.loads(json.dumps(SCHEDA_CASA)), rifiuta_ripristino=True)
    engine, _ = _engine(tmp_path, supervisor, TrasportoRete())
    with pytest.raises(Failure) as errore:
        engine.run({**RICHIESTA, "home_ssid": "Altra", "restore_password": "passwordserver"})
    assert errore.value.code == "restore_failed"
    assert "La password della rete Casa potrebbe essere sbagliata." in errore.value.message
    salvato = json.loads((tmp_path / "restore.json").read_text())
    assert salvato["interface"] == "wlan0" and salvato["payload"]["wifi"]["psk"] == "passwordserver"


def test_run_serve_la_password_del_server(tmp_path: Path) -> None:
    supervisor = SupervisorFinto(scheda=json.loads(json.dumps(SCHEDA_CASA)))
    engine, _ = _engine(tmp_path, supervisor, TrasportoRete())
    with pytest.raises(Failure) as errore:
        engine.run({**RICHIESTA, "home_ssid": "Altra"})
    assert errore.value.code == "restore_password_required"
    assert supervisor.aggiornamenti == [] and not (tmp_path / "restore.json").exists()


def test_run_rete_vmc_irraggiungibile(tmp_path: Path) -> None:
    supervisor = SupervisorFinto(ap_ip="")
    engine, _ = _engine(tmp_path, supervisor, TrasportoRete())
    with pytest.raises(Failure) as errore:
        engine.run(dict(RICHIESTA))
    assert errore.value.code == "ap_unreachable"
    assert supervisor.aggiornamenti[-1] == ("wlan0", {"enabled": False})
    assert not (tmp_path / "restore.json").exists()


def test_run_stesso_nome_gia_in_rete(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    trasporto = TrasportoRete(gia_presente="Prova")
    engine, _ = _engine(tmp_path, supervisor, trasporto)
    with pytest.raises(Failure) as errore:
        engine.run(dict(RICHIESTA))
    assert errore.value.code == "ambiguous_device" and trasporto.inviati == []
    assert not (tmp_path / "restore.json").exists()


def test_run_vmc_tornata_in_access_point(tmp_path: Path) -> None:
    supervisor = SupervisorFinto()
    engine, orologio = _engine(tmp_path, supervisor, TrasportoRete(compare=False), verify_seconds=9)
    with pytest.raises(Failure) as errore:
        engine.run(dict(RICHIESTA))
    assert errore.value.code == "back_to_access_point" and motore.LED_HINT in errore.value.message
    assert engine.status.data["network_sent"] is True
    supervisor.accesspoints = lambda interface: []
    engine, _ = _engine(tmp_path, supervisor, TrasportoRete(compare=False), verify_seconds=9)
    with pytest.raises(Failure) as errore:
        engine.run(dict(RICHIESTA))
    assert errore.value.code == "verification_timeout"


def test_scan(tmp_path: Path) -> None:
    engine, _ = _engine(tmp_path, SupervisorFinto())
    engine.scan()
    dati = json.loads((tmp_path / "scan.json").read_text())
    assert dati["vmc_networks"] == [{"ssid": "VMC_12345678", "signal": 70, "band": "2,4 GHz"},
                                    {"ssid": "VMC_87654321", "signal": 20, "band": "2,4 GHz"}]
    assert dati["wifi_networks"] == [{"ssid": "Casa", "signal": 90, "band": "5 GHz"}]
    assert engine.status.data["success"] is True and "Trovate 2 reti VMC" in engine.status.data["message"]
    engine, _ = _engine(tmp_path, SupervisorFinto(scheda={"interface": "end0", "type": "ethernet"}))
    with pytest.raises(Failure) as errore:
        engine.scan()
    assert errore.value.code == "no_wifi"


# ---------------------------------------------------------------- verify
class TrasportoVerifica:
    def __init__(self, nome="Prova", mac="AA:BB:CC:DD:EE:01", silenzi=0):
        self.nome, self.mac, self.silenzi = nome, mac, silenzi

    def identify(self, ip, interface=""):
        if self.silenzi:
            self.silenzi -= 1
            raise OSError("nessuna risposta")
        return self.nome

    def neighbor_mac(self, ip):
        return self.mac

    def network_info(self, ip):
        raise OSError("nessuna risposta")


def _identita(tmp_path, **valori):
    dati = {"ap_ssid": "VMC_12345678", "ip": "192.168.1.60", "name": "Prova", "mac": "AA:BB:CC:DD:EE:01"}
    dati.update(valori)
    motore.atomic_json(tmp_path / "identity.json", dati)


def test_verify(tmp_path: Path) -> None:
    _identita(tmp_path)
    engine, orologio = _engine(tmp_path, SupervisorFinto(), TrasportoVerifica(silenzi=2))
    engine.verify({"ip": "192.168.1.70", "ap_ssid": "VMC_12345678"})
    assert orologio.t == 1004.0  # due tentativi senza risposta, 2 s ciascuno
    assert json.loads((tmp_path / "identity.json").read_text())["ip"] == "192.168.1.70"
    dati = engine.status.data
    assert dati["success"] is True and dati["vmc_ip"] == "192.168.1.70" and dati["vmc_mac"] == "AA:BB:CC:DD:EE:01"
    assert dati["vmc_network_ssid"] == ""  # VMSL? senza risposta: dati di rete vuoti


@pytest.mark.parametrize(("trasporto", "codice"), [
    (TrasportoVerifica(mac="AA:BB:CC:DD:EE:02"), "identity_unconfirmed"),
    (TrasportoVerifica(nome="Altra"), "identity_unconfirmed"),
    (TrasportoVerifica(mac=""), "identity_unconfirmed"),
    (TrasportoVerifica(silenzi=1000), "vmc_unreachable"),
])
def test_verify_non_confermata(tmp_path: Path, trasporto, codice) -> None:
    _identita(tmp_path)
    engine, orologio = _engine(tmp_path, SupervisorFinto(), trasporto)
    with pytest.raises(Failure) as errore:
        engine.verify({"ip": "192.168.1.70", "ap_ssid": "VMC_12345678"})
    assert errore.value.code == codice
    assert json.loads((tmp_path / "identity.json").read_text())["ip"] == "192.168.1.60"
    if codice == "vmc_unreachable":
        assert 1030 <= orologio.t <= 1032  # al massimo 30 s


def test_verify_richiesta_non_valida(tmp_path: Path) -> None:
    engine, _ = _engine(tmp_path, SupervisorFinto(), TrasportoVerifica())
    with pytest.raises(Failure) as errore:
        engine.verify({"ip": "192.168.1.70", "ap_ssid": "VMC_12345678"})
    assert errore.value.code == "not_configured"
    _identita(tmp_path, mac="")
    with pytest.raises(Failure) as errore:
        engine.verify({"ip": "192.168.1.70", "ap_ssid": "VMC_12345678"})
    assert errore.value.code == "mac_unavailable"
    with pytest.raises(Failure) as errore:
        engine.verify({"ip": "8.8.8.8", "ap_ssid": "VMC_12345678"})
    assert errore.value.code == "invalid_ip"


def test_run_vmc_muta_o_doppia(tmp_path: Path) -> None:
    """Rete VMC raggiunta ma nessuna risposta sulla 5001; dopo l'invio due VMC con lo stesso nome."""

    class Muta(TrasportoRete):
        def identify(self, ip, interface=""):
            if interface:
                raise OSError("nessuna risposta")
            return super().identify(ip, interface)

    supervisor = SupervisorFinto()
    engine, _ = _engine(tmp_path, supervisor, Muta())
    with pytest.raises(Failure) as errore:
        engine.run(dict(RICHIESTA))
    assert errore.value.code == "vmc_unreachable" and engine.status.data["network_sent"] is False
    assert not (tmp_path / "restore.json").exists()

    class Doppia(TrasportoRete):
        def identify(self, ip, interface=""):
            if self.inviati and not interface:
                return self.nome
            return super().identify(ip, interface)

    engine, _ = _engine(tmp_path, supervisor, Doppia())
    with pytest.raises(Failure) as errore:
        engine.run({**RICHIESTA, "final_ip": "", "lan_cidr": "192.168.1.0/30"})
    assert errore.value.code == "ambiguous_device" and not (tmp_path / "identity.json").exists()
