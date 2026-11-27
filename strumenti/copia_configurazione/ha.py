"""Home Assistant vero per il banco: il processo e le API che usa il frontend.

Home Assistant gira come in una casa: ``python -m homeassistant -c <cartella>``, un
processo per ogni avvio (un riavvio chiesto con ``homeassistant.restart`` fa uscire il
processo con il codice 100 e il banco lo riavvia, come fa il Supervisor). Il banco parla
con Home Assistant solo come il frontend: API REST e websocket con un gettone di accesso
di lunga durata creato all'onboarding, flussi di configurazione e di riparazione con le
stesse richieste dei pulsanti dell'interfaccia.
"""

from __future__ import annotations

import asyncio
import contextlib
import itertools
import json
import os
import signal
import sys
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import aiohttp

PORTA = 8123
BASE = f"http://127.0.0.1:{PORTA}"
CODICE_RIAVVIO = 100
UTENTE, PAROLA, NOME_UTENTE = "proprietario", "parola-del-banco-123", "Proprietario"
LIMITE_MEMORIA_MB = 2000
ALLARME_MEMORIA_MB = 1200
"""Oltre questa memoria il banco chiama ``ProcessoHA.allarme`` una volta (per guardare
cosa sta girando in Home Assistant prima che venga fermato)."""
"""Memoria residente (RSS) oltre la quale il banco ferma Home Assistant: la macchina è
condivisa e un Home Assistant che cresce senza fine fa uccidere dal kernel anche i
processi degli altri. Con le 3 VMC della b41 Home Assistant sta sotto 1 GB."""


def memoria_mb(pid: int) -> float | None:
    """La memoria residente (VmRSS) del processo, in MB; None se non c'è più."""
    try:
        for riga in Path(f"/proc/{pid}/status").read_text().splitlines():
            if riga.startswith("VmRSS:"):
                return int(riga.split()[1]) / 1024
    except OSError:
        return None
    return None


class ErroreHA(RuntimeError):
    """Home Assistant non fa quello che il banco si aspetta."""


class ProcessoHA:
    """Un Home Assistant vero sulla cartella di configurazione ``cartella``."""

    def __init__(
        self, cartella: Path, registro: Path, ping: Path | None = None
    ) -> None:
        self.cartella = cartella
        self.registro = registro
        self.ping = ping
        self.processo: asyncio.subprocess.Process | None = None
        self.avvii = 0
        self._log = None
        self.picco_mb = 0.0
        """La memoria residente più alta vista in tutti gli avvii (MB)."""
        self.oltre_il_limite: str | None = None
        """Se il banco ha fermato Home Assistant per la memoria: quando e quanta."""
        self._sorveglianza: asyncio.Task | None = None
        self.allarme: Callable[[float], Awaitable[None]] | None = None

    async def avvia(self) -> None:
        """Avvia il processo (non aspetta che sia pronto: ``attendi_avvio``)."""
        if self.processo is not None and self.processo.returncode is None:
            raise ErroreHA("Home Assistant è già avviato")
        self.avvii += 1
        ambiente = dict(os.environ)
        if self.ping is not None:
            ambiente["PATH"] = f"{self.ping}:{ambiente.get('PATH', '')}"
        ambiente["PYTHONDONTWRITEBYTECODE"] = "1"
        ambiente["PYTHONFAULTHANDLER"] = "1"
        self.registro.parent.mkdir(parents=True, exist_ok=True)
        self._log = self.registro.open("ab")
        self._log.write(f"\n===== avvio {self.avvii} {time.ctime()} =====\n".encode())
        self._log.flush()
        # -P e cartella di lavoro = configurazione: con «python -m» la cartella di lavoro
        # va in sys.path e, se ha una cartella custom_components (la radice di questo
        # repository), Home Assistant carica l'integrazione da lì e non da
        # /config/custom_components (custom_components è un pacchetto senza __init__ e il
        # suo __path__ si ricalcola quando Home Assistant toglie config_dir da sys.path)
        self.processo = await asyncio.create_subprocess_exec(
            sys.executable,
            "-P",
            "-m",
            "homeassistant",
            "-c",
            str(self.cartella),
            "--skip-pip",
            "--log-no-color",
            "--log-file",
            str(self.cartella / "home-assistant.log"),
            stdout=self._log,
            stderr=self._log,
            env=ambiente,
            cwd=self.cartella,
        )
        self._sorveglianza = asyncio.create_task(self._sorveglia(self.processo))

    async def _sorveglia(self, processo: asyncio.subprocess.Process) -> None:
        """Misura la memoria del processo ogni mezzo secondo; oltre ``LIMITE_MEMORIA_MB``
        lo ferma con SIGABRT (le pile dei thread in ``ha.out``) e poi lo uccide (meglio un passo fallito con un messaggio chiaro che il kernel che
        uccide un processo qualunque della macchina)."""
        allarme_dato = False
        while processo.returncode is None:
            rss = memoria_mb(processo.pid)
            if rss is not None:
                self.picco_mb = max(self.picco_mb, rss)
                if rss > ALLARME_MEMORIA_MB and not allarme_dato and self.allarme:
                    allarme_dato = True
                    with contextlib.suppress(Exception):
                        await asyncio.wait_for(self.allarme(rss), 10)
                    continue
                if rss > LIMITE_MEMORIA_MB:
                    self.oltre_il_limite = (
                        f"avvio {self.avvii}: {rss:.0f} MB alle {time.strftime('%X')}"
                    )
                    # SIGABRT: faulthandler scrive in ha.out dove sono tutti i thread
                    with contextlib.suppress(ProcessLookupError):
                        processo.send_signal(signal.SIGABRT)
                    with contextlib.suppress(TimeoutError):
                        await asyncio.wait_for(processo.wait(), 5)
                    with contextlib.suppress(ProcessLookupError):
                        processo.kill()
                    return
            await asyncio.sleep(0.5)

    async def attendi_uscita(self, secondi: float = 120) -> int:
        """Aspetta che il processo esca; restituisce il codice di uscita."""
        assert self.processo is not None
        try:
            codice = await asyncio.wait_for(self.processo.wait(), secondi)
        except TimeoutError as errore:
            raise ErroreHA(f"Home Assistant non si ferma entro {secondi} s") from errore
        if self._log is not None:
            self._log.close()
            self._log = None
        return codice

    async def termina(self, secondi: float = 120) -> int:
        """Fermata ordinata (SIGTERM, come il Supervisor): Home Assistant salva tutto."""
        if self.processo is None or self.processo.returncode is not None:
            return self.processo.returncode if self.processo else 0
        self.processo.send_signal(signal.SIGTERM)
        return await self.attendi_uscita(secondi)

    def uccidi(self) -> None:
        if self.processo is not None and self.processo.returncode is None:
            self.processo.kill()
        if self._sorveglianza is not None:
            self._sorveglianza.cancel()

    @property
    def vivo(self) -> bool:
        return self.processo is not None and self.processo.returncode is None


class ClientHA:
    """Le API REST e websocket di Home Assistant, con un gettone di accesso."""

    def __init__(self, gettone: str | None = None) -> None:
        self.gettone = gettone
        self.sessione: aiohttp.ClientSession | None = None
        self.ws: aiohttp.ClientWebSocketResponse | None = None
        self._id = itertools.count(1)

    async def apri(self) -> None:
        if self.sessione is None:
            self.sessione = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120)
            )

    async def chiudi(self) -> None:
        if self.ws is not None:
            with contextlib.suppress(Exception):
                await self.ws.close()
            self.ws = None
        if self.sessione is not None:
            await self.sessione.close()
            self.sessione = None

    def _intestazioni(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.gettone}"} if self.gettone else {}

    async def richiesta(
        self,
        metodo: str,
        percorso: str,
        dati: Any = None,
        *,
        attesi: tuple[int, ...] = (200, 201),
        form: dict[str, str] | None = None,
        autenticata: bool = True,
    ) -> Any:
        await self.apri()
        assert self.sessione is not None
        intestazioni = self._intestazioni() if autenticata else {}
        async with self.sessione.request(
            metodo,
            f"{BASE}{percorso}",
            json=dati if form is None else None,
            data=form,
            headers=intestazioni,
        ) as risposta:
            testo = await risposta.text()
            if risposta.status not in attesi:
                raise ErroreHA(f"{metodo} {percorso}: {risposta.status} {testo[:500]}")
            if not testo:
                return None
            try:
                return json.loads(testo)
            except ValueError:
                return testo

    async def pronto(self) -> bool:
        """True se l'API risponde (Home Assistant avviato almeno fino a http)."""
        try:
            await self.apri()
            assert self.sessione is not None
            async with self.sessione.get(
                f"{BASE}/api/onboarding", timeout=aiohttp.ClientTimeout(total=5)
            ) as risposta:
                return risposta.status in (200, 401, 404)
        except (aiohttp.ClientError, OSError, TimeoutError):
            return False

    # ------------------------------------------------------------------ websocket
    async def collega_ws(self) -> None:
        await self.apri()
        assert self.sessione is not None
        if self.ws is not None and not self.ws.closed:
            return
        self.ws = await self.sessione.ws_connect(
            f"{BASE}/api/websocket", max_msg_size=0
        )
        benvenuto = await self.ws.receive_json()
        if benvenuto.get("type") != "auth_required":
            raise ErroreHA(f"websocket: {benvenuto}")
        await self.ws.send_json({"type": "auth", "access_token": self.gettone})
        esito = await self.ws.receive_json()
        if esito.get("type") != "auth_ok":
            raise ErroreHA(f"websocket: {esito}")

    async def ws_comando(self, tipo: str, **dati: Any) -> Any:
        numero = next(self._id)
        for tentativo in (1, 2):
            await self.collega_ws()
            assert self.ws is not None
            try:
                await self.ws.send_json({"id": numero, "type": tipo, **dati})
                break
            except (aiohttp.ClientError, ConnectionError):
                # collegamento di un avvio precedente di Home Assistant: si riapre
                self.ws = None
                if tentativo == 2:
                    raise
        while True:
            messaggio = await asyncio.wait_for(self.ws.receive_json(), 120)
            if messaggio.get("id") != numero or messaggio.get("type") != "result":
                continue
            if not messaggio.get("success"):
                raise ErroreHA(f"{tipo}: {messaggio.get('error')}")
            return messaggio.get("result")

    async def scollega_ws(self) -> None:
        if self.ws is not None:
            with contextlib.suppress(Exception):
                await self.ws.close()
            self.ws = None

    # -------------------------------------------------------------------- servizi
    async def servizio(
        self, dominio: str, nome: str, dati: dict[str, Any] | None = None
    ) -> Any:
        return await self.richiesta(
            "POST", f"/api/services/{dominio}/{nome}", dati or {}
        )

    async def stati(self) -> list[dict[str, Any]]:
        return await self.richiesta("GET", "/api/states")

    async def stato(self, entity_id: str) -> dict[str, Any] | None:
        try:
            return await self.richiesta("GET", f"/api/states/{entity_id}")
        except ErroreHA as errore:
            if " 404 " in str(errore):
                return None
            raise


async def attendi_avvio(
    processo: ProcessoHA, client: ClientHA, secondi: float = 300
) -> float:
    """Aspetta che Home Assistant risponda e sia «RUNNING»; restituisce i secondi."""
    inizio = time.monotonic()
    while time.monotonic() - inizio < secondi:
        if not processo.vivo:
            raise ErroreHA(
                f"Home Assistant è uscito durante l'avvio (codice "
                f"{processo.processo.returncode if processo.processo else '?'})"
            )
        if client.gettone is None:
            if await client.pronto():
                return time.monotonic() - inizio
        else:
            with contextlib.suppress(ErroreHA, aiohttp.ClientError, OSError):
                configurazione = await client.richiesta("GET", "/api/config")
                if configurazione.get("state") == "RUNNING":
                    return time.monotonic() - inizio
        await asyncio.sleep(1)
    raise ErroreHA(f"Home Assistant non è avviato entro {secondi} s")


async def onboarding(client: ClientHA) -> str:
    """L'onboarding di una casa nuova (utente, posizione, analisi, integrazioni) come
    lo fa il frontend; restituisce un gettone di accesso di lunga durata."""
    id_client = f"{BASE}/"
    esito = await client.richiesta(
        "POST",
        "/api/onboarding/users",
        {
            "client_id": id_client,
            "name": NOME_UTENTE,
            "username": UTENTE,
            "password": PAROLA,
            "language": "it",
        },
        autenticata=False,
    )
    gettoni = await client.richiesta(
        "POST",
        "/auth/token",
        form={
            "grant_type": "authorization_code",
            "code": esito["auth_code"],
            "client_id": id_client,
        },
        autenticata=False,
    )
    client.gettone = gettoni["access_token"]
    await client.richiesta("POST", "/api/onboarding/core_config", {})
    await client.richiesta("POST", "/api/onboarding/analytics", {})
    await client.richiesta(
        "POST",
        "/api/onboarding/integration",
        {"client_id": id_client, "redirect_uri": f"{BASE}/?auth_callback=1"},
    )
    lungo = await client.ws_comando(
        "auth/long_lived_access_token", client_name="banco", lifespan=3650
    )
    await client.scollega_ws()
    client.gettone = lungo
    return lungo
