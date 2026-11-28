"""Installa_vmc 0.4.0: procedura del manuale Helty (App Air Guard) per Home Assistant OS.

Usa solo la libreria standard di Python. Non importa e non modifica le altre parti del Package.
Nell'integrazione nativa il motore si usa da prima_installazione.py: la riga di comando e
il worker separato del package (8.6.0) non ci sono.

Comandi Air Guard (porta TCP 5001), gli stessi usati dall'app ufficiale:
  VMNM?            nome della VMC
  VMNM <nome>      rinomina (massimo 12 caratteri)
  VMSL?            rete memorizzata nella VMC
  VMSL <dati>      modalità Infrastruttura (rete di casa) o Access Point
  VMPW <dati>      cambio password della rete VMC (solo in Access Point)
"""
from __future__ import annotations

import concurrent.futures
import contextlib
import copy
import fcntl
import ipaddress
import json
import logging
import os
from pathlib import Path
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

VERSION = "0.4.0"
PORT = 5001
ROOT = Path(__file__).resolve().parents[2] / ".storage" / "vmc_master_installa_vmc"
# Reti private 10/8, 172.16/12 e 192.168/16 scritte come numeri: lo script Cambia IP sostituisce ogni indirizzo scritto con i punti.
PRIVATE = tuple(ipaddress.ip_network(n) for n in ((0x0A000000, 8), (0xAC100000, 12), (0xC0A80000, 16)))
# Coda del pacchetto VMSL: IP 15 cifre, porta 05001, gateway 15, maschera 15, modalità.
SUFFIX_INFRASTRUCTURE = "0" * 15 + "05001" + "0" * 30 + "10"
SUFFIX_ACCESS_POINT = "0" * 15 + "05001" + "0" * 30 + "01"
NAME_PATTERN = r"[A-Za-z0-9_-]{1,12}"
AP_PASSWORD_PATTERN = r"[A-Za-z0-9$@!%?&]{8,32}"


LOGGER = logging.getLogger(__name__)


class Failure(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def private_ip(value):
    try:
        ip = ipaddress.IPv4Address(value)
    except (ValueError, TypeError):
        raise Failure("invalid_ip", "Inserire un indirizzo IPv4 valido.") from None
    if not any(ip in network for network in PRIVATE):
        raise Failure("invalid_ip", "Usare l'indirizzo locale della VMC, ad esempio 192.168.1.x (x da 1 a 254).")
    return str(ip)


def mac(value):
    compact = re.sub(r"[:-]", "", value or "").upper()
    if compact and not re.fullmatch(r"[0-9A-F]{12}", compact):
        raise Failure("invalid_mac", "Il MAC deve contenere 6 coppie di caratteri esadecimali.")
    return ":".join(compact[i:i + 2] for i in range(0, 12, 2)) if compact else ""


def wifi_password(value):
    """NetworkManager accetta una passphrase WPA o una PSK esadecimale di 64 caratteri."""
    return (8 <= len(value.encode("utf-8")) <= 63 and "\x00" not in value) or bool(re.fullmatch(r"[0-9A-Fa-f]{64}", value))


def field32(value, code, label, minimum=1):
    """Campo Air Guard da 32 caratteri completato con asterischi."""
    if not isinstance(value, str) or not minimum <= len(value) <= 32:
        raise Failure(code, f"{label} deve avere da {minimum} a 32 caratteri.")
    if any(not 32 <= ord(c) <= 126 for c in value):
        raise Failure("unsupported_encoding", f"{label}: usare solo caratteri ASCII, senza lettere accentate.")
    if value.endswith("*"):
        raise Failure("ambiguous_padding", f"{label} non può terminare con un asterisco: la VMC usa l'asterisco come riempimento.")
    return value.ljust(32, "*")


def network_packet(ssid, password):
    return ("VMSL " + field32(ssid, "invalid_ssid", "«Rete Wi-Fi di casa»")
            + field32(password, "invalid_password", "«Password del Wi-Fi di casa»", 8)
            + SUFFIX_INFRASTRUCTURE).encode("ascii")


def access_point_packet():
    return ("VMSL " + "0".ljust(32, "*") + "0".ljust(32, "*") + SUFFIX_ACCESS_POINT).encode("ascii")


def password_packet(current, new):
    return ("VMPW " + field32(current, "invalid_ap_password", "La password attuale della rete VMC", 8)
            + field32(new, "invalid_new_password", "La nuova password", 8)).encode("ascii")


def check_ap(request):
    if not request["ap_ssid"]:
        raise Failure("invalid_ap_ssid", "Inserire il nome della rete Wi-Fi della VMC (VMC_xxxxxxxx).")
    if not 1 <= len(request["ap_ssid"].encode("utf-8")) <= 32:
        raise Failure("invalid_ap_ssid", "Il nome della rete VMC deve contenere al massimo 32 byte.")
    if not wifi_password(request["ap_password"]):
        raise Failure("invalid_ap_password", "Inserire una password valida per la rete VMC: quella iniziale è 12345678.")


def base_request(data, keys):
    if not isinstance(data, dict):
        raise Failure("invalid_request", "Richiesta non valida.")
    request = {key: str(data.get(key, "")) for key in keys}
    request.update(wifi_interface="", restore_password="", lan_cidr="", ap_ip="")
    return request


def normalize_request(data):
    request = base_request(data, ("home_ssid", "home_password", "ap_ssid", "ap_password", "final_ip"))
    # Facoltativi: password della rete Wi-Fi a cui è collegato ora il server e rete di ricerca.
    request.update(restore_password=str(data.get("restore_password", "")), lan_cidr=str(data.get("lan_cidr", "")).strip())
    check_ap(request)
    if request["restore_password"] and not wifi_password(request["restore_password"]):
        raise Failure("invalid_restore_password", "«Password del Wi-Fi attuale del server» deve avere da 8 a 63 caratteri.")
    network_packet(request["home_ssid"], request["home_password"])
    request["final_ip"] = request["final_ip"].strip()
    if request["final_ip"]:
        request["final_ip"] = private_ip(request["final_ip"])
    # La prenotazione si fa sul router. Alla VMC inviamo sempre la rete in DHCP.
    request.update(operation="Prima configurazione", ip_mode="IP riservato sul router" if request["final_ip"] else "DHCP",
                   current_ip="", expected_mac="")
    return request


def normalize_ap_password(data):
    request = base_request(data, ("ap_ssid", "ap_password", "new_password", "home_ssid", "home_password"))
    check_ap(request)
    if not re.fullmatch(AP_PASSWORD_PATTERN, request["new_password"]):
        raise Failure("invalid_new_password", "La nuova password deve avere da 8 a 32 caratteri tra lettere senza accenti, numeri e $ @ ! % ? &.")
    if request["new_password"] == request["ap_password"]:
        raise Failure("same_password", "La nuova password coincide con quella attuale.")
    password_packet(request["ap_password"], request["new_password"])
    return request


def read_identity(root):
    """Ultima VMC configurata: nessuna password e nessun MAC dell'access point."""
    try:
        data = json.loads((Path(root) / "identity.json").read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def configured_identity(data, root):
    if not isinstance(data, dict):
        raise Failure("invalid_request", "Richiesta non valida.")
    identity = read_identity(root)
    if not identity.get("ap_ssid") or data.get("ap_ssid") != identity["ap_ssid"] or not identity.get("ip"):
        raise Failure("not_configured", "Prima completare il collegamento della VMC.")
    return {"ip": private_ip(identity["ip"]), "ap_ssid": identity["ap_ssid"],
            "expected_mac": mac(identity.get("mac", "")), "expected_name": identity.get("name", "")}


def normalize_verification(data, root):
    if not isinstance(data, dict):
        raise Failure("invalid_request", "Richiesta non valida.")
    ip = private_ip(str(data.get("ip", "")).strip())
    identity = read_identity(root)
    if not identity.get("ap_ssid") or data.get("ap_ssid") != identity["ap_ssid"]:
        raise Failure("not_configured", "Prima completare il collegamento della VMC.")
    if not identity.get("mac"):
        raise Failure("mac_unavailable", "Il MAC non è stato rilevato sulla rete di casa. Controllare MAC e IP nell'elenco dispositivi del router: il nuovo IP non può essere confermato automaticamente.")
    return {"ip": ip, "ap_ssid": identity["ap_ssid"], "expected_mac": mac(identity["mac"]),
            "expected_name": identity["name"]}


def normalize_rename(data, root):
    request = configured_identity(data, root)
    name = str(data.get("name", "")).strip()
    if not re.fullmatch(NAME_PATTERN, name):
        raise Failure("invalid_name", "Il nuovo nome deve avere da 1 a 12 caratteri: lettere senza accenti, numeri, _ oppure -.")
    request["new_name"] = name
    return request


def normalize_ap_mode(data, root):
    return configured_identity(data, root)


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, path)


class Status:
    def __init__(self, root):
        self.root = Path(root)
        self.data = {"version": VERSION, "stage": "In attesa", "progress": 0, "message": "Compilare i dati e premere Collega VMC alla rete.",
                     "network_sent": False, "success": False, "wifi_interfaces": [], "vmc_ip": "", "vmc_name": "", "vmc_mac": "",
                     "mac_source": "", "vmc_network_ssid": "", "vmc_router": "", "error_code": "", "finished": False,
                     "job_id": "", "action": ""}

    def emit(self, stage, progress=0, message="", **values):
        self.data.update(stage=stage, progress=progress, message=message, **values)
        atomic_json(self.root / "status.json", self.data)


class Supervisor:
    def __init__(self, url=None, token=None):
        self.url = (url or "http://" + os.environ.get("SUPERVISOR", os.environ.get("HASSIO", "supervisor"))).rstrip("/")
        self.token = token or os.environ.get("SUPERVISOR_TOKEN") or os.environ.get("HASSIO_TOKEN")
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def call(self, path, payload=None, timeout=None):
        if not self.token:
            raise Failure("supervisor_unavailable", "La gestione Wi-Fi richiede Home Assistant OS e il Supervisor accessibile dal processo Home Assistant.")
        req = urllib.request.Request(self.url + path, data=None if payload is None else json.dumps(payload).encode(), headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"})
        try:
            with self.opener.open(req, timeout=timeout or (70 if payload is not None else 8)) as response:
                body = json.load(response)
        except urllib.error.HTTPError as exc:
            raise Failure("supervisor_http", f"Il Supervisor ha rifiutato l'operazione (HTTP {exc.code}).") from None
        except (OSError, ValueError):
            raise Failure("supervisor_unavailable", "Il Supervisor non risponde. Nessun invio alla VMC può essere confermato.") from None
        if body.get("result") != "ok":
            raise Failure("supervisor_error", "Il Supervisor non ha completato l'operazione di rete.")
        return body.get("data") or {}

    def info(self):
        return self.call("/network/info")

    def update(self, interface, payload):
        return self.call("/network/interface/" + urllib.parse.quote(interface, safe="") + "/update", payload)

    def accesspoints(self, interface):
        data = self.call("/network/interface/" + urllib.parse.quote(interface, safe="") + "/accesspoints", timeout=45)
        return data.get("accesspoints") or []


def name_answer_complete(data):
    """True se la risposta a VMNM? è completa. Il protocollo non ha un delimitatore fisso:
    la risposta è completa con un a capo (CR/LF) o un NUL, con gli asterischi di
    riempimento dopo il nome, oppure se non è una risposta «VMNM». «VMNM», «VMNM » e
    «VMNM Pr» senza altro possono essere solo la prima parte di una risposta spezzata."""
    text = bytes(data).lstrip(b"\x00\r\n ")
    if any(c in text for c in b"\r\n\x00"):
        return True
    if len(text) < 5:
        return not b"VMNM ".startswith(text)
    return not text.startswith(b"VMNM ") or text.endswith(b"*")


class Transport:
    def exchange(self, ip, payload, interface="", timeout=2.0, read=True, complete=None):
        """Invia payload e legge la risposta. Dopo il primo pezzo si attende 0,12 s al massimo;
        se complete(risposta) dice che la risposta non è finita, si continua a leggere fino a
        timeout secondi dall'invio."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if interface:
                try:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, (interface + "\0").encode())
                except (OSError, AttributeError):
                    raise Failure("wifi_socket", "Non è possibile usare la scheda Wi-Fi scelta per raggiungere la VMC.") from None
            sock.connect((ip, PORT))
            sock.sendall(payload)
            if not read:
                return b""
            deadline = time.monotonic() + timeout
            chunks = bytearray()
            while len(chunks) < 512:
                try:
                    part = sock.recv(512 - len(chunks))
                except socket.timeout:
                    if chunks:
                        break
                    raise
                if not part:
                    break
                chunks.extend(part)
                if complete is None or complete(chunks):
                    sock.settimeout(0.12)
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    sock.settimeout(remaining)
            return bytes(chunks)

    def command(self, ip, text, interface="", complete=None):
        try:
            return self.exchange(ip, text.encode("ascii"), interface, complete=complete).decode("ascii").strip("\x00\r\n ")
        except UnicodeError:
            raise Failure("invalid_vmc", "La VMC ha restituito una risposta non leggibile.") from None

    def identify(self, ip, interface=""):
        text = self.command(ip, "VMNM?", interface, complete=name_answer_complete)
        name = text[5:].rstrip("* ").strip() if text.startswith("VMNM ") else ""
        if not name:
            raise Failure("invalid_vmc", "Il dispositivo non risponde come una VMC Helty Air Guard.")
        return name

    def rename(self, ip, name):
        return self.command(ip, "VMNM " + name) == "OK"

    def network_info(self, ip):
        """Rete memorizzata nella VMC. La password presente nella risposta viene scartata."""
        text = self.command(ip, "VMSL?")
        if text.startswith("VMSL "):
            text = text[5:]
        if len(text) < 114:
            return {}
        clean = lambda value: value.replace("*", "").strip()
        return {"ssid": clean(text[0:32]), "router": clean(text[84:99]), "subnet": clean(text[99:114])}

    def send(self, ip, packet, interface=""):
        self.exchange(ip, packet, interface, read=False)

    def neighbor_mac(self, ip):
        # Solo un vicino su una rete direttamente collegata: un MAC del gateway
        # o dell'access point iniziale non serve per prenotare l'IP della VMC.
        try:
            target = int(ipaddress.IPv4Address(ip))
            routes = []
            for line in Path("/proc/net/route").read_text().splitlines()[1:]:
                fields = line.split()
                if len(fields) < 8:
                    continue
                try:
                    destination = int.from_bytes(bytes.fromhex(fields[1]), "little")
                    gateway = int(fields[2], 16)
                    flags = int(fields[3], 16)
                    mask = int.from_bytes(bytes.fromhex(fields[7]), "little")
                except ValueError:
                    continue
                if flags & 1 and target & mask == destination:
                    routes.append((bin(mask).count("1"), gateway, fields[0], int(fields[6])))
            if not routes:
                return ""
            prefix, gateway, device, _metric = max(routes, key=lambda route: (route[0], -route[3]))
            if gateway or not prefix:
                return ""
            lines = Path("/proc/net/arp").read_text().splitlines()[1:]
        except (OSError, ValueError):
            return ""
        for line in lines:
            parts = line.split()
            if len(parts) < 6 or parts[0] != ip or parts[5] != device:
                continue
            try:
                actual = mac(parts[3])
                complete = int(parts[2], 0) & 2
                if complete and actual and actual != "00:00:00:00:00:00" and not int(actual[:2], 16) & 1:
                    return actual
            except (Failure, ValueError):
                continue
        return ""


def interfaces(info):
    return info.get("interfaces", [])


def addresses(interface):
    ipv4 = interface.get("ipv4") or {}
    values = ipv4.get("address", ipv4.get("ip_address", []))
    return [values] if isinstance(values, str) else values


def lan_targets(info, cidr=""):
    networks = []
    # cidr: una o più reti di ricerca separate da virgole (ad esempio cavo e Wi-Fi del server).
    values = [c.strip() for c in cidr.split(",") if c.strip()] if cidr else [a for i in interfaces(info) if i.get("connected") for a in addresses(i)]
    for value in values:
        try:
            network = ipaddress.ip_network(value, strict=False)
        except ValueError:
            raise Failure("invalid_subnet", "La rete di ricerca deve avere il formato rete/24 (ad esempio 192.168.1.x/24).") from None
        if network.version != 4 or not any(network.subnet_of(n) for n in PRIVATE):
            continue
        if network.num_addresses > 256:
            raise Failure("subnet_too_large", "La rete locale è troppo ampia per la ricerca automatica: sono supportate sottoreti fino a 256 indirizzi, ad esempio 192.168.1.x/24.")
        networks.append(network)
    if not networks:
        raise Failure("no_lan", "Non è stata individuata una rete locale. Controllare che il server sia collegato alla rete di casa e riprovare.")
    own = {str(ipaddress.ip_interface(a).ip) for i in interfaces(info) for a in addresses(i)}
    return sorted({str(ip) for n in networks for ip in n.hosts()} - own)


def restore_payload(interface, password=""):
    payload = {"enabled": bool(interface.get("enabled"))}
    if not interface.get("enabled"):
        # L'endpoint v1 del Supervisor rimuove il profilo temporaneo.
        return payload
    for family in ("ipv4", "ipv6"):
        original = interface.get(family)
        if original:
            allowed = ("method", "address", "nameservers", "gateway", "route_metric", "addr_gen_mode", "ip6_privacy")
            payload[family] = {k: v for k, v in original.items() if k in allowed and v is not None}
            if original.get("method") == "static" and "address" not in payload[family]:
                legacy = original.get("ip_address", [])
                payload[family]["address"] = [legacy] if isinstance(legacy, str) else legacy
            if original.get("method") != "static":
                # v1 riporta gli indirizzi DHCP correnti: non trasformarli in statici.
                for key in ("address", "gateway", "nameservers"):
                    payload[family].pop(key, None)
    wifi = interface.get("wifi") or {}
    if wifi.get("ssid"):
        config = {k: wifi[k] for k in ("ssid", "mode", "auth") if k in wifi}
        if config.get("auth") == "wpa-psk":
            if not password:
                raise Failure("restore_password_required", "Il Wi-Fi del server è collegato alla rete " + wifi["ssid"] + ": per ripristinarlo al termine scrivere la password di quella rete nel campo «Password del Wi-Fi attuale del server». In alternativa usare una scheda Wi-Fi libera. Nessuna modifica è stata eseguita.")
            config["psk"] = password
        elif config.get("auth", "open") != "open":
            raise Failure("unsupported_restore", "Il profilo Wi-Fi attuale del server usa un'autenticazione non supportata.")
        payload["wifi"] = config
    return payload


def password_hint(payload):
    """Avviso per un ripristino non riuscito che usava una password del Wi-Fi del server."""
    wifi = payload.get("wifi") if isinstance(payload, dict) else None
    if isinstance(wifi, dict) and wifi.get("psk"):
        return " La password della rete " + str(wifi.get("ssid", "")) + " potrebbe essere sbagliata."
    return ""


def ap_profile(ssid, password):
    return {"enabled": True, "ipv4": {"method": "auto", "route_metric": 4096}, "ipv6": {"method": "disabled"},
            "wifi": {"mode": "infrastructure", "auth": "wpa-psk", "ssid": ssid, "psk": password}}


LED_HINT = (" Guardare il LED Allarme filtri della VMC e confrontare i lampeggi con la tabella Errori connessione"
            " (sezione Errori e ripristino della scheda).")


class Engine:
    def __init__(self, root, supervisor=None, transport=None, sleep=time.sleep, monotonic=time.monotonic, verify_seconds=90):
        self.root = Path(root)
        self.supervisor = supervisor or Supervisor()
        self.transport = transport or Transport()
        self.status = Status(root)
        self.sleep, self.now, self.verify_seconds = sleep, monotonic, verify_seconds

    # ---- server ---------------------------------------------------------
    def diagnose(self):
        self.status.emit("Verifica del server", 10, "Lettura delle interfacce di Home Assistant OS.")
        info = self.supervisor.info()
        wifi = [{"interface": i["interface"], "enabled": i.get("enabled", False), "connected": i.get("connected", False), "ssid": (i.get("wifi") or {}).get("ssid", "")} for i in interfaces(info) if i.get("type") == "wireless"]
        ethernet = [i["interface"] for i in interfaces(info) if i.get("type") == "ethernet" and i.get("connected")]
        self.status.emit("Server verificato" if wifi else "Wi-Fi non disponibile", 100, "Scheda Wi-Fi disponibile per il primo collegamento." if wifi else "Il Supervisor non rileva una scheda Wi-Fi. Per la prima configurazione serve una scheda Wi-Fi integrata nel computer di Home Assistant oppure una chiavetta USB Wi-Fi collegata e riconosciuta da Home Assistant OS.", wifi_interfaces=wifi, ethernet_interfaces=ethernet, wifi_available=bool(wifi), success=bool(wifi))
        return info

    def read_restore(self, checkpoint):
        """Contenuto di restore.json. Un file illeggibile (troncato, modificato a mano, senza
        una chiave) viene messo da parte come restore.json.illeggibile, così non blocca
        le procedure successive."""
        try:
            backup = json.loads(checkpoint.read_text(encoding="utf-8"))
            if not isinstance(backup, dict) or not isinstance(backup.get("interface"), str) or not backup["interface"] or not isinstance(backup.get("payload"), dict):
                raise ValueError("struttura non valida")
        except (OSError, ValueError) as exc:
            aside = checkpoint.with_name(checkpoint.name + ".illeggibile")
            try:
                os.replace(checkpoint, aside)
                LOGGER.warning("File di ripristino del Wi-Fi del server non leggibile (%s): spostato in %s", exc, aside)
            except OSError as error:
                LOGGER.warning("File di ripristino del Wi-Fi del server non leggibile (%s) e non spostato: %s", exc, error)
            raise Failure("restore_failed", "Il file di ripristino del Wi-Fi del server non era leggibile ed è stato messo da parte. Controllare che il server sia collegato alla sua rete, poi riprovare.") from exc
        return backup

    def restore(self):
        checkpoint = self.root / "restore.json"
        if not checkpoint.exists():
            return
        backup = self.read_restore(checkpoint)
        self.status.emit("Ripristino rete server", max(self.status.data.get("progress", 0), 65), "Ripristino della connessione precedente del server.")
        self.supervisor.update(backup["interface"], backup["payload"])
        if backup.get("connected"):
            deadline = self.now() + 25
            while self.now() < deadline:
                current = next((i for i in interfaces(self.supervisor.info()) if i.get("interface") == backup["interface"]), {})
                if current.get("connected") and (current.get("wifi") or {}).get("ssid") == backup.get("ssid"):
                    break
                self.sleep(1)
            else:
                raise Failure("restore_failed", "Il Wi-Fi del server non è tornato alla rete precedente." + password_hint(backup["payload"]) + " Riprovare; se la connessione non torna, controllare il server localmente.")
        checkpoint.unlink()

    def recover(self):
        self.restore()
        self.status.emit("Rete server ripristinata", 100, "Il ripristino è completato. Le impostazioni della VMC non sono state riscritte.", success=True)

    def choose_wifi(self, info, requested):
        eligible = [i for i in interfaces(info) if i.get("type") == "wireless"]
        if requested:
            eligible = [i for i in eligible if i.get("interface") == requested]
        if not eligible:
            raise Failure("no_wifi", "Il Supervisor non rileva una scheda Wi-Fi disponibile. Serve un computer di Home Assistant con scheda Wi-Fi integrata oppure con una chiavetta USB Wi-Fi compatibile collegata; in alternativa configurare la VMC con l'app Air Guard.")
        eligible.sort(key=lambda i: (bool(i.get("connected")), bool(i.get("enabled") and (i.get("wifi") or {}).get("ssid"))))
        return eligible[0]

    def wait_ap(self, interface, ssid, seconds):
        """Attende il collegamento alla rete VMC e restituisce il gateway, cioè la VMC."""
        deadline = self.now() + seconds
        while self.now() < deadline:
            active = next((i for i in interfaces(self.supervisor.info()) if i.get("interface") == interface), {})
            if active.get("connected") and (active.get("wifi") or {}).get("ssid") == ssid:
                gateway = (active.get("ipv4") or {}).get("gateway", "")
                if gateway:
                    return private_ip(gateway)
            self.sleep(1)
        return ""

    @contextlib.contextmanager
    def ap_session(self, info, request, unreachable):
        """Collega il Wi-Fi del server alla rete VMC_xxxxxxxx e lo ripristina sempre all'uscita."""
        chosen = copy.deepcopy(self.choose_wifi(info, request.get("wifi_interface", "")))
        interface = chosen["interface"]
        original_ssid = (chosen.get("wifi") or {}).get("ssid", "")
        password = request.get("restore_password", "")
        if original_ssid and original_ssid == request.get("home_ssid") and request.get("home_password"):
            password = request["home_password"]
        payload = restore_payload(chosen, password)
        atomic_json(self.root / "restore.json", {"interface": interface, "payload": payload, "connected": chosen.get("connected", False), "ssid": original_ssid})
        mutation_started = False
        try:
            self.status.emit("Collegamento alla VMC", 25, "Il server si collega alla rete " + request["ap_ssid"] + " con la password indicata, come lo smartphone nel manuale.")
            mutation_started = True
            self.supervisor.update(interface, ap_profile(request["ap_ssid"], request["ap_password"]))
            source_ip = self.wait_ap(interface, request["ap_ssid"], 35)
            if not source_ip:
                raise Failure("ap_unreachable", unreachable)
            if request.get("ap_ip"):
                source_ip = private_ip(request["ap_ip"])
            yield source_ip, interface
        finally:
            if mutation_started:
                try:
                    self.restore()
                except (Failure, OSError, ValueError):
                    raise Failure("restore_failed", "Ripristino del Wi-Fi del server non completato." + password_hint(payload) + " La configurazione di recupero è conservata: riprovare oppure riavviare Home Assistant per il recupero automatico.") from None
            elif (self.root / "restore.json").exists():
                (self.root / "restore.json").unlink()

    def ap_visible(self, ssid, seconds):
        """True se la rete VMC_xxxxxxxx è visibile, None se il server non può cercarla."""
        try:
            wireless = [i["interface"] for i in interfaces(self.supervisor.info()) if i.get("type") == "wireless"]
        except Failure:
            return None
        if not wireless:
            return None
        deadline = self.now() + seconds
        while True:
            try:
                if any(ap.get("ssid") == ssid for ap in self.supervisor.accesspoints(wireless[0])):
                    return True
            except Failure:
                pass
            if self.now() >= deadline:
                return False
            self.sleep(5)

    # ---- VMC sulla rete di casa ---------------------------------------------
    def confirm_identity(self, request):
        ip = request["ip"]
        try:
            name = self.transport.identify(ip)
        except OSError:
            raise Failure("vmc_unreachable", "La VMC non risponde all'indirizzo " + ip + ". Controllare che sia accesa e collegata alla rete di casa.") from None
        if request["expected_name"] and name != request["expected_name"]:
            raise Failure("identity_unconfirmed", "All'indirizzo " + ip + " risponde " + name + " invece di " + request["expected_name"] + ". Nessun comando è stato inviato.")
        if request["expected_mac"]:
            actual = self.transport.neighbor_mac(ip)
            if actual and actual != request["expected_mac"]:
                raise Failure("identity_unconfirmed", "Il MAC all'indirizzo " + ip + " non corrisponde alla VMC configurata. Nessun comando è stato inviato.")
        return name

    def read_network(self, ip):
        try:
            data = self.transport.network_info(ip)
        except (OSError, Failure):
            return {}
        return {"vmc_network_ssid": data.get("ssid", ""), "vmc_router": data.get("router", "")}

    def discover(self, targets, name, expected):
        def probe(ip):
            try:
                found_name = self.transport.identify(ip)
                found_mac = self.transport.neighbor_mac(ip)
                if (not name or found_name == name) and (not expected or found_mac == expected):
                    return {"ip": ip, "name": found_name, "mac": found_mac}
            except (OSError, Failure):
                return None
            return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
            return [candidate for candidate in pool.map(probe, targets) if candidate]

    # ---- Manuale: Connessione alla rete WiFi (ricerca VMC_xxxxxxxx) ----------
    def scan(self):
        self.status.emit("Ricerca reti Wi-Fi", 20, "Il server cerca le reti Wi-Fi visibili, come la scansione dello smartphone.")
        info = self.supervisor.info()
        wireless = [i for i in interfaces(info) if i.get("type") == "wireless"]
        if not wireless:
            raise Failure("no_wifi", "Il Supervisor non rileva una scheda Wi-Fi: scrivere a mano il nome della rete VMC letto sullo smartphone.")
        try:
            found = self.supervisor.accesspoints(wireless[0]["interface"])
        except Failure:
            raise Failure("scan_failed", "La scheda Wi-Fi del server non ha restituito l'elenco delle reti. Scrivere a mano il nome della rete VMC letto sullo smartphone.") from None
        networks = {}
        for ap in found:
            ssid = str(ap.get("ssid") or "")
            if not ssid:
                continue
            signal_level = int(ap.get("signal") or 0)
            frequency = int(ap.get("frequency") or 0)
            band = "5 GHz" if frequency >= 4900 else "2,4 GHz" if frequency else ""
            if ssid not in networks or signal_level > networks[ssid]["signal"]:
                networks[ssid] = {"ssid": ssid, "signal": signal_level, "band": band}
        ordered = sorted(networks.values(), key=lambda n: -n["signal"])
        vmc = [n for n in ordered if n["ssid"].upper().startswith("VMC_")]
        others = [n for n in ordered if not n["ssid"].upper().startswith("VMC_")][:10]
        atomic_json(self.root / "scan.json", {"vmc_networks": vmc, "wifi_networks": others})
        if len(vmc) == 1:
            message = "Trovata la rete " + vmc[0]["ssid"] + ": il nome è stato inserito nel campo della rete VMC."
        elif vmc:
            message = "Trovate " + str(len(vmc)) + " reti VMC: scrivere nel campo quella della VMC da collegare (le cifre sono il numero di serie)."
        else:
            message = "Nessuna rete VMC_xxxxxxxx visibile dal server. Avvicinare il server o verificare che la VMC sia in modalità Access Point (vedi Ripristino Wi-Fi)."
        self.status.emit("Ricerca completata", 100, message, success=bool(vmc), vmc_networks=vmc)

    # ---- Manuale: Configurazione rete > Infrastruttura ------------------------
    def run(self, data):
        request = normalize_request(data)
        packet = network_packet(request["home_ssid"], request["home_password"])
        info = self.diagnose()
        self.status.data["success"] = False
        targets = [request["final_ip"]] if request["ip_mode"] == "IP riservato sul router" else lan_targets(info, request["lan_cidr"])
        self.status.emit("Controllo rete di casa", 20, "Controllo delle VMC già presenti per evitare una conferma del dispositivo sbagliato.")
        previous_devices = self.discover(targets, "", "")
        name = ""
        unreachable = "La rete VMC non è raggiungibile o non assegna un indirizzo. Controllare nome e password della rete VMC e che la VMC sia in modalità Access Point."
        with self.ap_session(info, request, unreachable) as (source_ip, source_interface):
            self.status.emit("Identificazione VMC", 40, "Lettura del nome della VMC prima dell'invio.")
            try:
                name = self.transport.identify(source_ip, source_interface)
            except OSError:
                raise Failure("vmc_unreachable", "La rete VMC è stata raggiunta, ma il dispositivo non risponde sulla porta 5001. Controllare che sia una VMC Helty compatibile.") from None
            if any(device["name"] == name for device in previous_devices):
                raise Failure("ambiguous_device", "Una VMC con lo stesso nome è già presente sulla rete di casa. Rinominare una delle due VMC prima di riprovare: nessuna nuova rete è stata inviata.")
            self.status.emit("Invio rete di casa", 50, "Invio della rete " + request["home_ssid"] + " in modalità Infrastruttura (SALVA nel manuale).", vmc_name=name)
            self.transport.send(source_ip, packet, source_interface)
            self.status.data["network_sent"] = True
            self.status.emit("Attesa cambio rete", 60, "Attesa del collegamento della VMC alla nuova rete.", network_sent=True)
            self.sleep(3)
        self.status.emit("Ricerca nuovo indirizzo", 80, "Ricerca della stessa VMC sulla rete di casa.")
        deadline = self.now() + self.verify_seconds
        while self.now() < deadline:
            candidates = self.discover(targets, name, request["expected_mac"])
            if len(candidates) > 1:
                raise Failure("ambiguous_device", "Più VMC rispondono con lo stesso nome: il collegamento non può essere confermato. Rinominare le VMC con nomi distinti.")
            if len(candidates) == 1:
                found = candidates[0]
                atomic_json(self.root / "identity.json", {"ap_ssid": request["ap_ssid"],
                            "ip": found["ip"], "name": found["name"], "mac": found["mac"]})
                message = "La VMC è collegata ed è stata verificata sulla nuova rete."
                if not found["mac"]:
                    message += " Il MAC non è rilevabile dalla rete del server: leggerlo nell'elenco dei dispositivi del router."
                self.status.emit("Completato", 100, message, success=True, vmc_ip=found["ip"],
                                 vmc_name=found["name"], vmc_mac=found["mac"],
                                 mac_source="LAN" if found["mac"] else "", network_sent=True,
                                 **self.read_network(found["ip"]))
                return
            self.sleep(3)
        # Manuale: con password o cifratura errate per 3 volte la VMC torna in Access Point.
        self.status.emit("Diagnosi", 90, "La VMC non è ancora comparsa: controllo se è tornata in Access Point.")
        if self.ap_visible(request["ap_ssid"], 45):
            raise Failure("back_to_access_point", "La rete " + request["ap_ssid"] + " è di nuovo visibile: la VMC non è riuscita a collegarsi ed è tornata in Access Point. Secondo il manuale succede con password errata o cifratura non supportata (ad esempio WEP). Controllare nome e password della rete di casa e riprovare." + LED_HINT)
        raise Failure("verification_timeout", "La rete è stata inviata, ma la VMC non è stata ritrovata sulla rete di casa." + LED_HINT + " Controllare anche nel router l'IP assegnato.")

    def verify(self, data):
        request = normalize_verification(data, self.root)
        ip, expected = request["ip"], request["expected_mac"]
        self.status.emit("Verifica indirizzo IP", 15, "Controllo della VMC all'indirizzo " + ip + ".")
        deadline = self.now() + min(self.verify_seconds, 30)
        while self.now() < deadline:
            try:
                name = self.transport.identify(ip)
            except OSError:
                self.sleep(2)
                continue
            actual = self.transport.neighbor_mac(ip)
            if actual != expected or name != request["expected_name"]:
                raise Failure("identity_unconfirmed", "Il dispositivo a questo IP non corrisponde alla VMC configurata, oppure il suo MAC non è leggibile dalla rete del server. Controllare l'associazione MAC/IP sul router.")
            identity = read_identity(self.root)
            identity["ip"] = ip
            atomic_json(self.root / "identity.json", identity)
            self.status.emit("Completato", 100, "L'indirizzo è stato verificato: risponde la stessa VMC configurata.",
                             success=True, vmc_ip=ip, vmc_name=name, vmc_mac=actual, mac_source="LAN", **self.read_network(ip))
            return
        raise Failure("vmc_unreachable", "La VMC non risponde all'IP inserito. Controllare l'indirizzo e la prenotazione nel router; perché la VMC prenda il nuovo IP, spegnerla e riaccenderla dal suo interruttore.")

    # ---- Manuale: Rinomina VMC ---------------------------------------------
    def rename(self, data):
        request = normalize_rename(data, self.root)
        ip, new_name = request["ip"], request["new_name"]
        self.status.emit("Verifica VMC", 20, "Controllo della VMC all'indirizzo " + ip + ".")
        current = self.confirm_identity(request)
        if current != new_name:
            self.status.emit("Controllo nomi", 35, "Controllo che il nome " + new_name + " non sia già usato da un'altra VMC.")
            try:
                targets = [t for t in lan_targets(self.supervisor.info()) if t != ip]
            except Failure:
                targets = []
            if self.discover(targets, new_name, ""):
                raise Failure("duplicate_name", "Il nome " + new_name + " è già usato da un'altra VMC sulla rete di casa: sceglierne uno diverso.")
            self.status.emit("Invio nuovo nome", 60, "RINOMINA VMC: invio del nome " + new_name + ".")
            try:
                accepted = self.transport.rename(ip, new_name)
            except OSError:
                raise Failure("vmc_unreachable", "La VMC non ha risposto durante l'invio del nuovo nome.") from None
            if not accepted:
                raise Failure("rename_refused", "La VMC non ha confermato il nuovo nome (risposta diversa da OK).")
            self.sleep(1)
            try:
                current = self.transport.identify(ip)
            except OSError:
                current = ""
            if current != new_name:
                raise Failure("rename_unconfirmed", "Il nuovo nome è stato inviato, ma la VMC risponde ancora con " + (current or "nessun nome") + ".")
        identity = read_identity(self.root)
        identity["name"] = new_name
        atomic_json(self.root / "identity.json", identity)
        self.status.emit("Completato", 100, "La VMC ora si chiama " + new_name + ". Il nome della rete " + request["ap_ssid"] + " non cambia.",
                         success=True, vmc_ip=ip, vmc_name=new_name, vmc_mac=request["expected_mac"])

    # ---- Manuale: Cambia password VMC (solo in Access Point) ------------------
    def change_ap_password(self, data):
        request = normalize_ap_password(data)
        packet = password_packet(request["ap_password"], request["new_password"])
        info = self.diagnose()
        self.status.data["success"] = False
        unreachable = "La rete " + request["ap_ssid"] + " non è raggiungibile con la password attuale indicata. Secondo il manuale la password si cambia solo in modalità Access Point: se la VMC è già collegata alla rete di casa, la sua rete VMC non è attiva."
        with self.ap_session(info, request, unreachable) as (source_ip, interface):
            self.status.emit("Identificazione VMC", 40, "Lettura del nome della VMC prima del cambio password.")
            try:
                name = self.transport.identify(source_ip, interface)
            except OSError:
                raise Failure("vmc_unreachable", "La rete VMC è stata raggiunta, ma il dispositivo non risponde sulla porta 5001.") from None
            self.status.emit("Invio nuova password", 50, "CAMBIA PASSWORD VMC: invio della nuova password.", vmc_name=name)
            self.transport.send(source_ip, packet, interface)
            self.status.data["network_sent"] = True
            self.status.emit("Verifica nuova password", 60, "Il server si ricollega alla rete " + request["ap_ssid"] + " con la nuova password.", network_sent=True)
            self.sleep(5)
            self.supervisor.update(interface, ap_profile(request["ap_ssid"], request["new_password"]))
            gateway = self.wait_ap(interface, request["ap_ssid"], 45)
            confirmed = False
            if gateway:
                try:
                    confirmed = self.transport.identify(gateway, interface) == name
                except (OSError, Failure):
                    confirmed = False
            if not confirmed:
                raise Failure("password_unconfirmed", "La nuova password è stata inviata, ma il server non riesce a collegarsi alla rete VMC con la nuova password. Provare dallo smartphone con la nuova e con la vecchia password; se nessuna funziona usare il Ripristino Wi-Fi del manuale (la password tornerà 12345678).")
        self.status.emit("Completato", 100, "La password della rete " + request["ap_ssid"] + " è cambiata ed è stata verificata. Da ora usarla al posto di 12345678 per collegarsi alla rete VMC.",
                         success=True, vmc_name=name)

    # ---- Manuale: Configurazione rete > Access Point ---------------------------
    def access_point(self, data):
        request = normalize_ap_mode(data, self.root)
        ip = request["ip"]
        self.status.emit("Verifica VMC", 20, "Controllo della VMC all'indirizzo " + ip + ".")
        name = self.confirm_identity(request)
        self.status.emit("Invio modalità Access Point", 45, "CONFIGURAZIONE RETE > ACCESS POINT: invio del comando a " + name + ".", vmc_name=name)
        try:
            self.transport.send(ip, access_point_packet())
        except OSError:
            raise Failure("vmc_unreachable", "La VMC non ha accettato il comando.") from None
        self.status.data["network_sent"] = True
        self.status.emit("Attesa Access Point", 65, "Attesa della rete " + request["ap_ssid"] + ".", network_sent=True)
        self.sleep(10)
        visible = self.ap_visible(request["ap_ssid"], 60)
        if visible:
            (self.root / "identity.json").unlink(missing_ok=True)
            self.status.emit("Completato", 100, "La VMC è tornata in modalità Access Point: la rete " + request["ap_ssid"] + " è di nuovo visibile. Per ricollegarla alla rete di casa ripetere il collegamento della VMC.",
                             success=True, vmc_ip="", vmc_name=name, vmc_mac="")
            return
        try:
            still_there = self.transport.identify(ip) == name
        except (OSError, Failure):
            still_there = False
        if still_there:
            raise Failure("ap_not_applied", "La VMC risponde ancora sulla rete di casa: il passaggio in Access Point non è stato applicato.")
        raise Failure("ap_unconfirmed", "La VMC non risponde più sulla rete di casa, ma la rete " + request["ap_ssid"] + " non è visibile dal server. Controllare dallo smartphone; se non compare usare il Ripristino Wi-Fi del manuale.")


def read_status(root=ROOT):
    root = Path(root)
    try:
        data = json.loads((root / "status.json").read_text())
    except (OSError, ValueError):
        data = Status(root).data
    identity = read_identity(root)
    data.update(configured_ap_ssid=identity.get("ap_ssid", ""), configured_ip=identity.get("ip", ""),
                configured_name=identity.get("name", ""), configured_mac=identity.get("mac", ""))
    try:
        scan = json.loads((root / "scan.json").read_text())
    except (OSError, ValueError):
        scan = {}
    data.update(vmc_networks=scan.get("vmc_networks", []), wifi_networks=scan.get("wifi_networks", []))
    if data.get("job_id") and not data.get("finished"):
        with open(root / "worker.lock", "a") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return data
            # Un worker terminato in modo anomalo non deve bloccare la scheda.
            data.update(finished=True, success=False, error_code="interrupted",
                        stage="Ripristino necessario" if (root / "restore.json").exists() else "Errore",
                        message="La procedura è stata interrotta. Ripetere l'operazione per tentare il recupero; se la rete era già stata inviata, controllare nel router l'indirizzo della VMC.")
            atomic_json(root / "status.json", {k: v for k, v in data.items() if not k.startswith("configured_") and k not in ("vmc_networks", "wifi_networks")})
    return data
