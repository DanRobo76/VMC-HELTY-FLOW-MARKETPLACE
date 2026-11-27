"""Collegamento TCP con la VMC e letture periodiche, con una VMC finta in locale."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from unittest.mock import patch

import aiohttp
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.vmc_master.nativa import client as modulo_client
from custom_components.vmc_master.nativa import letture as modulo_letture
from custom_components.vmc_master.nativa.client import (
    ClientVMC,
    ErroreVMC,
    maschera_lan,
)
from custom_components.vmc_master.nativa.letture import (
    ERRORE_CONNESSIONE,
    LETTURE_TCP,
    OFF_LINE,
    ON_LINE,
    LetturaPing,
    LetturaTCP,
    LetturaVersione,
    raggiungibile,
    tag_versione,
)

pytestmark = pytest.mark.usefixtures("socket_enabled")

VMGH = "VMGO,00002" + ",00000" * 13
VMGI = "VMGI,00210,00100,00500,00600," + "00000," * 6 + "00050" + ",00000" * 3


class VmcFinta:
    """Una VMC finta: risponde alle richieste e ricorda cosa ha ricevuto."""

    def __init__(self, risposte: dict[str, bytes] | None = None) -> None:
        """Prepara le risposte (richiesta senza a capo -> byte inviati)."""
        self.risposte = risposte or {}
        self.ricevuti: list[bytes] = []
        self.aperte = 0
        self.massimo_aperte = 0
        self.ritardo = 0.0
        self.muta = False
        self.server: asyncio.Server | None = None

    async def _gestisci(self, lettore, scrittore) -> None:
        self.aperte += 1
        self.massimo_aperte = max(self.massimo_aperte, self.aperte)
        try:
            dati = await lettore.read(1024)
            self.ricevuti.append(dati)
            if self.ritardo:
                await asyncio.sleep(self.ritardo)
            if not self.muta:
                chiave = dati.decode(errors="replace").rstrip("\n")
                scrittore.write(self.risposte.get(chiave, b"OK"))
                await scrittore.drain()
            else:
                await asyncio.sleep(10)
        finally:
            self.aperte -= 1
            scrittore.close()

    async def avvia(self) -> int:
        """Avvia il server su 127.0.0.1 e restituisce la porta."""
        self.server = await asyncio.start_server(self._gestisci, "127.0.0.1", 0)
        return self.server.sockets[0].getsockname()[1]

    async def ferma(self) -> None:
        """Ferma il server."""
        assert self.server is not None
        self.server.close()
        await self.server.wait_closed()


@pytest.fixture
async def vmc():
    """Una VMC finta avviata, fermata a fine test."""
    finta = VmcFinta(
        {
            "VMGH?": VMGH.encode(),
            "VMGI?": VMGI.encode(),
            "VMNM?": b"VMNM Master",
            "VMSL?": b"Rete di casa"
            + b" " * 20
            + b"segreta"
            + b" " * 25
            + b"192.168.1.160",
        }
    )
    porta = await finta.avvia()
    finta.porta = porta
    yield finta
    await finta.ferma()


async def test_interroga_come_sensore_tcp(vmc) -> None:
    """La richiesta parte senza a capo e la risposta resta com'è."""
    client = ClientVMC("127.0.0.1", vmc.porta)
    assert await client.interroga("VMGH?") == VMGH
    assert vmc.ricevuti == [b"VMGH?"]


async def test_interroga_risposta_con_spazi_e_a_capo(vmc) -> None:
    """Nessun trim: il sensore tcp del Package teneva anche spazi e a capo."""
    vmc.risposte["VMNM?"] = b"VMNM Master\r\n"
    client = ClientVMC("127.0.0.1", vmc.porta)
    assert await client.interroga("VMNM?") == "VMNM Master\r\n"


async def test_comanda_come_shell_command(vmc) -> None:
    """Il comando parte con l'a capo, come printf '...\\n' | nc."""
    client = ClientVMC("127.0.0.1", vmc.porta)
    assert await client.comanda("VMWH0000002") == "OK"
    assert vmc.ricevuti == [b"VMWH0000002\n"]


async def test_comanda_senza_risposta_conta_come_inviato(vmc) -> None:
    """Se la VMC non risponde entro l'attesa, il comando resta inviato."""
    vmc.muta = True
    client = ClientVMC("127.0.0.1", vmc.porta, attesa=0.2)
    assert await client.comanda("VMWH0000000") == ""
    assert vmc.ricevuti == [b"VMWH0000000\n"]


async def test_interroga_senza_risposta_e_errore(vmc) -> None:
    """Il sensore tcp diventava non disponibile se la VMC non rispondeva."""
    vmc.muta = True
    client = ClientVMC("127.0.0.1", vmc.porta, attesa=0.2)
    with pytest.raises(ErroreVMC, match="nessuna risposta"):
        await client.interroga("VMGH?")


async def test_vmc_spenta() -> None:
    """Porta chiusa o indirizzo non valido: errore, sia per letture sia per comandi."""
    server = await asyncio.start_server(lambda r, w: None, "127.0.0.1", 0)
    porta = server.sockets[0].getsockname()[1]
    server.close()
    await server.wait_closed()
    client = ClientVMC("127.0.0.1", porta, attesa=0.5)
    with pytest.raises(ErroreVMC, match="non raggiungibile"):
        await client.interroga("VMGH?")
    with pytest.raises(ErroreVMC, match="non raggiungibile"):
        await client.comanda("VMWH0000001")


async def test_indirizzo_non_valido() -> None:
    """Indirizzo che non si risolve o non si codifica: VMC non raggiungibile."""
    import socket

    for errore in (
        socket.gaierror(-2, "Name or service not known"),
        UnicodeError("label too long"),
    ):

        async def apri(*argomenti, errore=errore, **kwargs):
            raise errore

        with (
            patch("asyncio.open_connection", apri),
            pytest.raises(ErroreVMC, match="non raggiungibile"),
        ):
            await ClientVMC("999.999.999.999").interroga("VMGH?")


async def test_risposta_non_leggibile(vmc) -> None:
    """Byte non UTF-8: la lettura non vale (il sensore tcp si fermava con un errore)."""
    vmc.risposte["VMGH?"] = b"\xff\xfe"
    client = ClientVMC("127.0.0.1", vmc.porta)
    with pytest.raises(ErroreVMC, match="non leggibile"):
        await client.interroga("VMGH?")
    vmc.risposte["VMWH0000001"] = b"\xffOK"
    assert await client.comanda("VMWH0000001") == "�OK"


async def test_un_solo_scambio_alla_volta(vmc) -> None:
    """Letture e comandi della stessa VMC non si sovrappongono mai."""
    vmc.ritardo = 0.05
    client = ClientVMC("127.0.0.1", vmc.porta)
    risultati = await asyncio.gather(
        client.interroga("VMGH?"),
        client.comanda("VMWH0000003"),
        client.interroga("VMGI?"),
        client.interroga("VMNM?"),
    )
    assert risultati == [VMGH, "OK", VMGI, "VMNM Master"]
    assert vmc.massimo_aperte == 1


async def test_errori_di_invio_e_chiusura(vmc) -> None:
    """Invio non riuscito: errore; chiusura non riuscita: lo scambio resta valido."""
    client = ClientVMC("127.0.0.1", vmc.porta)

    class ScrittoreRotto:
        def write(self, dati):
            raise ConnectionResetError("rotta")

        def close(self):
            pass

        async def wait_closed(self):
            raise ConnectionResetError("rotta")

    async def collega_rotto():
        return asyncio.StreamReader(), ScrittoreRotto()

    with patch.object(client, "_collega", collega_rotto):
        with pytest.raises(ErroreVMC, match="invio"):
            await client.interroga("VMGH?")
        with pytest.raises(ErroreVMC, match="invio"):
            await client.comanda("VMWH0000001")


@pytest.mark.parametrize(
    ("valore", "atteso"),
    [
        ("", ""),
        ("  corta  ", "corta"),
        ("R" * 32, "R" * 32),
        ("R" * 32 + "P", "R" * 32 + "*"),
        ("R" * 32 + "P" * 32 + "192.168.1.160", "R" * 32 + "*" * 32 + "192.168.1.160"),
        (
            "VMSL " + "R" * 32 + "P" * 32 + "192.168.1.160 ",
            "VMSL " + "R" * 32 + "*" * 32 + "192.168.1.160",
        ),
        ("VMSL " + "R" * 30, "VMSL " + "R" * 30),
    ],
)
def test_maschera_lan(valore: str, atteso: str) -> None:
    """La password del Wi-Fi (32 caratteri dopo la rete) diventa asterischi."""
    assert maschera_lan(valore) == atteso


async def test_maschera_lan_uguale_al_package(hass: HomeAssistant) -> None:
    """Stesso risultato del value_template del sensore lan, per lunghezze da 0 a 130."""
    from homeassistant.helpers.template import Template

    from .confronto import package

    conf = next(
        s
        for s in package()["sensor"]
        if s.get("platform") == "tcp" and s["payload"] == "VMSL?"
    )
    sorgente = conf["value_template"]
    for prefisso in ("", "VMSL ", " VMSL "):
        for n in range(131):
            valore = prefisso + "".join(chr(65 + i % 26) for i in range(n)) + " \r\n"
            atteso = Template(sorgente, hass).async_render(
                parse_result=False, value=valore
            )
            assert maschera_lan(valore) == atteso, (prefisso, n)


async def test_letture_tcp(hass: HomeAssistant, vmc) -> None:
    """Ogni lettura ha la sua richiesta e il suo intervallo; VMSL esce con la password coperta."""
    client = ClientVMC("127.0.0.1", vmc.porta)
    assert [(lt.chiave, lt.richiesta, lt.intervallo) for lt in LETTURE_TCP] == [
        ("sensor.status_ventola", "VMGH?", 5),
        ("sensor.sensori", "VMGI?", 1227),
        ("sensor.nome", "VMNM?", 43227),
        ("sensor.lan", "VMSL?", 57641),
    ]
    valori = {}
    for lettura in LETTURE_TCP:
        coordinatore = LetturaTCP(hass, None, client, lettura)
        assert coordinatore.update_interval is None  # il giro è avvia_periodica
        assert coordinatore.intervallo == lettura.intervallo
        await coordinatore.async_refresh()
        assert coordinatore.last_update_success
        valori[lettura.chiave] = coordinatore.data
    assert valori == {
        "sensor.status_ventola": VMGH,
        "sensor.sensori": VMGI,
        "sensor.nome": "VMNM Master",
        "sensor.lan": "Rete di casa" + " " * 20 + "*" * 32 + "192.168.1.160",
    }


async def test_lettura_tcp_non_riuscita(hass: HomeAssistant, vmc) -> None:
    """VMC muta: la lettura non riesce (sensore non disponibile), poi torna."""
    client = ClientVMC("127.0.0.1", vmc.porta, attesa=0.2)
    coordinatore = LetturaTCP(hass, None, client, LETTURE_TCP[0])
    vmc.muta = True
    await coordinatore.async_refresh()
    assert not coordinatore.last_update_success
    vmc.muta = False
    await coordinatore.async_refresh()
    assert coordinatore.last_update_success
    assert coordinatore.data == VMGH


async def test_richieste_ravvicinate_senza_pausa(hass: HomeAssistant, vmc) -> None:
    """Due richieste di lettura di fila partono entrambe (letture ravvicinate a 1 s)."""
    client = ClientVMC("127.0.0.1", vmc.porta)
    coordinatore = LetturaTCP(hass, None, client, LETTURE_TCP[0])
    await coordinatore.async_request_refresh()
    await coordinatore.async_request_refresh()
    await asyncio.sleep(
        0.05
    )  # il Debouncer esegue la seconda alla fine della pausa (0 s)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert vmc.ricevuti == [b"VMGH?", b"VMGH?"]


async def test_lettura_ping(hass: HomeAssistant) -> None:
    """ON-Line se la VMC risponde al ping, altrimenti OFF-Line; ogni 10 s."""
    risposte = [True, False]

    async def prova(host: str) -> bool:
        assert host == "192.168.1.50"
        return risposte.pop(0)

    coordinatore = LetturaPing(hass, None, "192.168.1.50", prova)
    assert coordinatore.update_interval is None
    assert coordinatore.intervallo == 10
    await coordinatore.async_refresh()
    assert coordinatore.data == ON_LINE
    await coordinatore.async_refresh()
    assert coordinatore.data == OFF_LINE


async def test_raggiungibile() -> None:
    """icmplib senza privilegi; senza permessi si usa il comando ping di sistema."""
    from icmplib.exceptions import (
        NameLookupError,
        SocketPermissionError,
    )

    class Esito:
        def __init__(self, ricevuti):
            self.packets_received = ricevuti

    async def ping_ok(host, **kwargs):
        assert kwargs == {"count": 3, "interval": 1, "timeout": 1, "privileged": False}
        return Esito(1)

    async def ping_zero(host, **kwargs):
        return Esito(0)

    async def ping_nome(host, **kwargs):
        raise NameLookupError(host)

    async def ping_permesso(host, **kwargs):
        raise SocketPermissionError(False)

    with patch("icmplib.async_ping", ping_ok):
        assert await raggiungibile("192.168.1.50") is True
    with patch("icmplib.async_ping", ping_zero):
        assert await raggiungibile("192.168.1.50") is False
    with patch("icmplib.async_ping", ping_nome):
        assert await raggiungibile("999.999.999.999") is False

    class Processo:
        def __init__(self, uscita=b"", lento=False):
            self.uscita = uscita
            self.lento = lento
            self.ucciso = False

        async def communicate(self):
            if self.lento:
                await asyncio.sleep(60)
            return self.uscita, b""

        def kill(self):
            self.ucciso = True

        async def wait(self):
            return -9

    chiamate = []

    def crea(processo):
        async def crea_processo(*argomenti, **kwargs):
            chiamate.append(argomenti)
            return processo

        return crea_processo

    with patch("icmplib.async_ping", ping_permesso):
        with patch(
            "asyncio.create_subprocess_exec", crea(Processo(b"64 bytes from 1.2.3.4"))
        ):
            assert await raggiungibile("192.168.1.50") is True
        assert chiamate[-1] == ("ping", "-c", "3", "-W", "1", "-w", "4", "192.168.1.50")
        with patch(
            "asyncio.create_subprocess_exec", crea(Processo(b"100% packet loss"))
        ):
            assert await raggiungibile("192.168.1.50") is False
        lento = Processo(lento=True)
        with (
            patch("asyncio.create_subprocess_exec", crea(lento)),
            patch.object(modulo_letture, "PING_DURATA", -5.9),
        ):
            assert await raggiungibile("192.168.1.50") is False
        assert lento.ucciso

        async def senza_ping(*argomenti, **kwargs):
            raise FileNotFoundError("ping")

        with patch("asyncio.create_subprocess_exec", senza_ping):
            assert await raggiungibile("192.168.1.50") is False


@pytest.mark.parametrize(
    ("dati", "atteso"),
    [
        ({"tag_name": "v9.0.0b41"}, "v9.0.0b41"),
        ({"tag_name": ""}, ERRORE_CONNESSIONE),
        ({"message": "API rate limit exceeded"}, ERRORE_CONNESSIONE),
        ([], ERRORE_CONNESSIONE),
        (None, ERRORE_CONNESSIONE),
    ],
)
def test_tag_versione(dati, atteso) -> None:
    """Come il value_template del sensore rest del Package."""
    assert tag_versione(dati) == atteso


async def test_lettura_versione(hass: HomeAssistant, aioclient_mock) -> None:
    """Tag della release; «Errore Connessione» senza tag; non disponibile senza risposta."""
    url = modulo_letture.URL_VERSIONE
    assert url.endswith("/DanRobo76/VMC-HELTY-FLOW-MASTER/releases/latest")
    coordinatore = LetturaVersione(hass, None)
    assert coordinatore.update_interval is None
    assert coordinatore.intervallo == 86400

    aioclient_mock.get(url, json={"tag_name": "v9.0.0b41"})
    await coordinatore.async_refresh()
    assert coordinatore.data == "v9.0.0b41"
    assert (
        aioclient_mock.mock_calls[-1][3]["Accept"] == "application/vnd.github.v3+json"
    )

    aioclient_mock.clear_requests()
    aioclient_mock.get(url, status=403, json={"message": "API rate limit exceeded"})
    await coordinatore.async_refresh()
    assert coordinatore.data == ERRORE_CONNESSIONE

    aioclient_mock.clear_requests()
    aioclient_mock.get(url, text="<html>non json</html>")
    await coordinatore.async_refresh()
    assert coordinatore.data == ERRORE_CONNESSIONE

    aioclient_mock.clear_requests()
    aioclient_mock.get(url, exc=aiohttp.ClientError("rete"))
    await coordinatore.async_refresh()
    assert not coordinatore.last_update_success

    aioclient_mock.clear_requests()
    aioclient_mock.get(url, exc=TimeoutError())
    await coordinatore.async_refresh()
    assert not coordinatore.last_update_success


async def test_intervallo_scatta(hass: HomeAssistant, vmc) -> None:
    """Col giro avviato, la lettura di stato riparte da sola ogni 5 s; fermato, no."""
    client = ClientVMC("127.0.0.1", vmc.porta)
    coordinatore = LetturaTCP(hass, None, client, LETTURE_TCP[0])
    await coordinatore.async_refresh()
    ferma = coordinatore.avvia_periodica()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=6))
    await hass.async_block_till_done(wait_background_tasks=True)
    ferma()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=12))
    await hass.async_block_till_done(wait_background_tasks=True)
    assert vmc.ricevuti == [b"VMGH?", b"VMGH?"]


def test_costanti() -> None:
    """Porta, attese e dimensione come nel Package."""
    assert modulo_client.PORTA == 5001
    assert modulo_client.ATTESA == 3
    assert modulo_client.DURATA_COMANDO == 5
    assert modulo_client.DIMENSIONE == 1024


async def test_motivo_mai_vuoto(vmc) -> None:
    """Un'attesa scaduta non ha testo («TimeoutError()»): il messaggio nel registro dice il
    motivo invece di finire con «:» (prova del proprietario del 27-11-2026)."""
    vmc.muta = True
    with pytest.raises(ErroreVMC) as errore:
        await ClientVMC("127.0.0.1", vmc.porta, attesa=0.2).interroga("VMGH?")
    assert str(errore.value) == "nessuna risposta a 'VMGH?': nessuna risposta entro 0.2 secondi"

    async def apri_senza_fine(*_argomenti, **_kwargs):
        await asyncio.sleep(10)

    with patch("asyncio.open_connection", apri_senza_fine):
        for scambio in ("interroga", "comanda"):
            with pytest.raises(ErroreVMC) as errore:
                await getattr(ClientVMC("192.168.33.67", attesa=0.1), scambio)("VMGH?")
            assert str(errore.value) == (
                "VMC 192.168.33.67:5001 non raggiungibile: nessuna risposta entro 0.1 secondi"
            )
    assert modulo_client.motivo_errore(OSError(113, "No route to host")) == (
        "[Errno 113] No route to host"
    )
    assert modulo_client.motivo_errore(TimeoutError(), 3) == "nessuna risposta entro 3 secondi"
    assert modulo_client.motivo_errore(TimeoutError()) == "nessuna risposta in tempo"
    assert modulo_client.motivo_errore(ConnectionResetError()) == "ConnectionResetError"


async def test_versione_senza_risposta_dice_il_motivo(
    hass: HomeAssistant, aioclient_mock
) -> None:
    coordinatore = LetturaVersione(hass, None)
    aioclient_mock.get(modulo_letture.URL_VERSIONE, exc=TimeoutError())
    await coordinatore.async_refresh()
    assert str(coordinatore.last_exception) == (
        f"GitHub non risponde: nessuna risposta entro {modulo_letture.ATTESA_VERSIONE:g} secondi"
    )


async def test_lettura_lunga_avvisa_solo_con_la_vmc_raggiungibile(
    hass: HomeAssistant, vmc, caplog: pytest.LogCaptureFixture
) -> None:
    """Lettura ancora in corso al giro seguente: si salta. L'avviso «più lunga
    dell'intervallo» compare solo se la VMC risponde (lettura lenta); con la VMC già
    segnalata come non raggiungibile non si ripete a ogni giro."""
    coordinatore = LetturaTCP(hass, None, ClientVMC("127.0.0.1", vmc.porta), LETTURE_TCP[0])
    await coordinatore.lettura_con_blocco()
    assert vmc.ricevuti == [b"VMGH?"]
    async with coordinatore._in_corso:
        await coordinatore.lettura_con_blocco()
        assert caplog.text.count("più lunga dell'intervallo di 5 s") == 1
        coordinatore.last_update_success = False
        await coordinatore.lettura_con_blocco()
        assert caplog.text.count("più lunga dell'intervallo di 5 s") == 1
    assert vmc.ricevuti == [b"VMGH?"]
