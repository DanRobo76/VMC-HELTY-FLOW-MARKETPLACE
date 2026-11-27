"""Collegamento TCP con la VMC (porta 5001), senza file .sh e senza nc.

Riproduce i due modi in cui il Package parla oggi con la VMC:

- le letture dei sensori ``tcp`` (VMGH?, VMGI?, VMNM?, VMSL?): la richiesta parte
  senza a capo, si aspetta al massimo 3 s la connessione e 3 s la risposta, si
  leggono al massimo 1024 byte e il testo resta com'è (nessun trim);
- i comandi degli ``shell_command`` (``printf 'VMWH0000002\\n' | timeout 5 nc -w 3
  IP 5001`` e ``echo "VMNM nome" | ...``): il comando parte con l'a capo, la
  risposta si aspetta al massimo 3 s e tutto si chiude entro 5 s.

Differenza voluta rispetto al Package: un solo scambio alla volta per ogni VMC
(un lucchetto per VMC), così una lettura non si sovrappone mai a un comando.
"""

from __future__ import annotations

import asyncio
import contextlib

PORTA = 5001
ATTESA = 3  # secondi: timeout: 3 dei sensori tcp e nc -w 3 dei comandi
DURATA_COMANDO = 5  # secondi: timeout 5 davanti a nc
DIMENSIONE = 1024  # byte letti, come buffer_size predefinito dei sensori tcp


class ErroreVMC(Exception):
    """La VMC non risponde: connessione, invio o lettura non riusciti."""


class ClientVMC:
    """Scambi TCP con una VMC, uno alla volta."""

    def __init__(self, host: str, porta: int = PORTA, attesa: float = ATTESA) -> None:
        """Prepara il collegamento con la VMC all'indirizzo ``host``."""
        self.host = host
        self.porta = porta
        self.attesa = attesa
        self._lucchetto = asyncio.Lock()

    async def interroga(self, richiesta: str) -> str:
        """Invia una richiesta (es. «VMGH?») e restituisce la risposta, come un sensore tcp.

        Solleva ErroreVMC se la VMC non si collega, non riceve o non risponde entro
        l'attesa. Una risposta vuota (la VMC chiude senza scrivere) vale «».
        """
        async with self._lucchetto:
            lettore, scrittore = await self._collega()
            try:
                try:
                    scrittore.write(richiesta.encode())
                    await asyncio.wait_for(scrittore.drain(), self.attesa)
                except (OSError, TimeoutError) as err:
                    raise ErroreVMC(f"invio di {richiesta!r} non riuscito: {err}") from err
                try:
                    dati = await asyncio.wait_for(lettore.read(DIMENSIONE), self.attesa)
                except (OSError, TimeoutError) as err:
                    raise ErroreVMC(f"nessuna risposta a {richiesta!r}: {err}") from err
            finally:
                await self._chiudi(scrittore)
        try:
            return dati.decode()
        except UnicodeDecodeError as err:
            # Il sensore tcp qui si fermava con un errore nel registro: la lettura
            # non vale e il sensore resta com'era. Qui la lettura risulta non riuscita.
            raise ErroreVMC(f"risposta a {richiesta!r} non leggibile: {err}") from err

    async def comanda(self, comando: str) -> str:
        """Invia un comando (es. «VMWH0000002») con l'a capo, come gli shell_command.

        Restituisce la risposta della VMC, o «» se non arriva entro l'attesa: come
        con nc, il comando conta come inviato anche senza risposta. Solleva
        ErroreVMC solo se la connessione o l'invio non riescono.
        """
        async with self._lucchetto:
            async with asyncio.timeout(DURATA_COMANDO):
                lettore, scrittore = await self._collega()
                try:
                    try:
                        scrittore.write(f"{comando}\n".encode())
                        await asyncio.wait_for(scrittore.drain(), self.attesa)
                    except (OSError, TimeoutError) as err:
                        raise ErroreVMC(f"invio di {comando!r} non riuscito: {err}") from err
                    try:
                        dati = await asyncio.wait_for(lettore.read(DIMENSIONE), self.attesa)
                    except (OSError, TimeoutError):
                        dati = b""
                finally:
                    await self._chiudi(scrittore)
        return dati.decode(errors="replace")

    async def _collega(self) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Apre la connessione TCP entro l'attesa."""
        try:
            return await asyncio.wait_for(
                asyncio.open_connection(self.host, self.porta), self.attesa
            )
        except (OSError, TimeoutError, UnicodeError) as err:
            raise ErroreVMC(f"VMC {self.host}:{self.porta} non raggiungibile: {err}") from err

    async def _chiudi(self, scrittore: asyncio.StreamWriter) -> None:
        """Chiude la connessione senza far fallire lo scambio già concluso."""
        scrittore.close()
        with contextlib.suppress(OSError, TimeoutError):
            await asyncio.wait_for(scrittore.wait_closed(), self.attesa)


def maschera_lan(valore: str) -> str:
    """Risposta a VMSL? con la password del Wi-Fi coperta, come il value_template del Package.

    La risposta è rete (32) + password (32) + IP, porta, gateway, maschera e modalità;
    la VMC vera la manda senza «VMSL » davanti, altre possono averlo. I 32 caratteri
    dopo la rete diventano asterischi, gli altri restano.
    """
    v = valore.strip()
    p = 5 if v[:5] == "VMSL " else 0
    if len(v) > p + 32:
        risultato = v[: p + 32] + "*" * (min(len(v), p + 64) - p - 32) + v[p + 64 :]
    else:
        risultato = v
    return risultato.strip()
