"""Script e comandi di shell del package dentro il motore (fase 4): nessuna entità.

Script
------
Ogni script del package è uno ``ScriptInterno``: la stessa ``Sequenza`` della fase 3,
con le regole di ``ScriptEntity`` per i modi in cui il package lo usa:

- ``script.<chiave>`` (la chiamata aspetta la fine, ``_service_handler``):
  ``ScriptInterno.esegui``;
- ``script.turn_on`` (l'esecuzione parte in un task nuovo e la chiamata aspetta solo il
  primo cambiamento, ``async_turn_on(wait=False)``): ``ScriptInterno.avvia``;
- ``script.turn_off`` (``async_turn_off``): ``ScriptInterno.ferma``.

Stesse modalità (single, restart, queued, parallel con il massimo), stesse variabili e
campi, stessa pila contro le ricorsioni (``script_stack_cv``), stesse regole di Home Assistant
per fermare gli script alla chiusura (``chiusura.RegistroSequenze``). Manca ciò che
dell'entità si vede fuori: lo stato ``script.<chiave>`` e i suoi ``state_changed``,
l'evento ``script_started``, la traccia, ``this`` (nessun modello del package lo legge) e
``last_triggered`` ripreso dopo un riavvio (nessuno lo legge).

Comandi
-------
Ogni ``shell_command`` del package è un ``Comando`` di ``ComandiVMC``. Chi lo chiama non
cambia: ``shell_command.<nome>`` arriva qui dal contesto del motore
(``Contesto.chiama_servizio``) e dai pulsanti. Al posto di ``printf ... | nc`` e dei file
.sh il comando va alla VMC con il client TCP (``invia``). Il comando che scriveva l'IP
nei file non c'è (b46): l'IP si cambia solo dall'ingranaggio della VMC.

Le automazioni del package che ascoltano le chiamate dei comandi (trigger ``event`` su
``call_service`` con ``domain: shell_command``) restano le stesse: ``ComandiVMC`` è il
loro aggancio diretto. Nel punto in cui ``ServiceRegistry.async_call`` lanciava l'evento
``call_service``, ``notifica`` lo manda nel canale del motore (``seguire.CambiInterni``:
subito, o dopo la consegna in corso, come il bus) e alla consegna chiama i loro
ascoltatori con lo stesso evento (tipo, dati, contesto), nello stesso ordine e con le
stesse regole del bus (``_async_dispatch``) e del trigger ``event`` (``handle_event``);
l'evento però non passa dal bus.
"""

from __future__ import annotations

import asyncio
import logging
import re
import shlex
from collections.abc import Awaitable, Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Any

import probatio
from homeassistant.const import (
    ATTR_DOMAIN,
    ATTR_ENTITY_ID,
    ATTR_SERVICE,
    ATTR_SERVICE_DATA,
    CONF_ID,
    EVENT_CALL_SERVICE,
)
from homeassistant.core import (
    CALLBACK_TYPE,
    Context,
    Event,
    EventOrigin,
    HassJob,
    HomeAssistant,
    ServiceResponse,
    callback,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.script import script_stack_cv
from homeassistant.helpers.template import Template
from homeassistant.util.async_ import create_eager_task

from ..client import ErroreVMC
from .definizioni import COMANDO_NESSUNO, COMANDO_NOME, COMANDO_VMC, Comando
from .seguire import cambi_interni

if TYPE_CHECKING:
    from .contesto import Contesto
    from .esecuzione import ComeScript

_LOGGER = logging.getLogger(__name__)

DOMINIO_SCRIPT = "script"
DOMINIO_COMANDI = "shell_command"
ACCENDI = "turn_on"
SPEGNI = "turn_off"
INVERTI = "toggle"
ATTR_VARIABLES = "variables"

# Lo schema di ``script.turn_on``, ``turn_off`` e ``toggle`` (come lo registra
# l'integrazione script di Home Assistant: homeassistant/components/script/services.py).
SCHEMA_ACCENDI_SPEGNI = cv.make_entity_service_schema(
    {probatio.Optional(ATTR_VARIABLES): {str: cv.match_all}}
)

# Il segno che il traduttore mette su un trigger ``event`` di una chiamata di un comando:
# Home Assistant non lo aggancia (``enabled: False``, ma la posizione conta ancora per
# ``trigger.idx`` e ``trigger.id``), lo aggancia ``ComandiVMC``.
AGGANCIO = "aggancio_comandi"

# Come vmc_<nome>_script_cambio_nome.sh (con LC_ALL=C): da 1 a 10 tra lettere senza
# accenti, cifre, «_» e «-».
_NOME_VALIDO = re.compile(r"[A-Za-z0-9_-]{1,10}")

Invia = Callable[[str], Awaitable[Any]]


# --- script ----------------------------------------------------------------------------


class ScriptInterno:
    """Uno script del package senza entità (come ScriptEntity, senza stato)."""

    def __init__(self, chiave: str, script: ComeScript) -> None:
        self.chiave = chiave
        self.entity_id = f"{DOMINIO_SCRIPT}.{chiave}"
        self.script = script
        self.hass: HomeAssistant = script.sequenza.hass
        # come ScriptEntity._changed: lo scrive ogni cambiamento dell'esecuzione
        self._cambiato = asyncio.Event()
        script.change_listener = self._al_cambio

    @callback
    def _al_cambio(self) -> None:
        """Come ScriptEntity.async_change_listener, senza stato da scrivere."""
        self._cambiato.set()

    @property
    def in_corso(self) -> bool:
        return self.script.is_running

    async def _esegui(
        self, variabili: Mapping[str, Any] | None, contesto: Context
    ) -> None:
        """Come ScriptEntity._async_run, senza traccia, ``script_started`` e ``this``."""
        await self.script.async_run({**(variabili or {})}, contesto)

    async def esegui(
        self, variabili: Mapping[str, Any] | None, contesto: Context
    ) -> None:
        """``script.<chiave>``: come ``_async_start_run(wait=True)``."""
        esecuzione = self._esegui(variabili, contesto)
        # come Home Assistant: una copia della pila, così due chiamate in parallelo non
        # si vedono, ma una ricorsione vietata si vede ancora
        if pila := script_stack_cv.get():
            script_stack_cv.set(pila.copy())
        await esecuzione

    async def avvia(
        self, variabili: Mapping[str, Any] | None, contesto: Context
    ) -> None:
        """``script.turn_on``: come ``_async_start_run(wait=False)``: un task nuovo con
        una pila nuova, poi si aspetta il primo cambiamento (uno script ``single`` già in
        corso: il prossimo cambiamento di quello in corso)."""
        esecuzione = self._esegui(variabili, contesto)
        script_stack_cv.set([])
        self._cambiato.clear()
        self.hass.async_create_task(esecuzione, eager_start=True)
        await self._cambiato.wait()

    async def ferma(self) -> None:
        """``script.turn_off``: come ``ScriptEntity.async_turn_off``."""
        await self.script.async_stop()

    async def scarica(self) -> None:
        """Come ``async_will_remove_from_hass`` dell'entità: niente più esecuzioni."""
        await self.script.async_unload()


class ScriptInterni:
    """Gli script del package di una VMC, per chiave nell'ordine del package (l'ordine
    delle entità del dominio ``script``, che ``script.turn_on`` segue)."""

    def __init__(self) -> None:
        self.script: dict[str, ScriptInterno] = {}
        self._per_entita: dict[str, ScriptInterno] = {}

    def aggiungi(self, script: ScriptInterno) -> None:
        self.script[script.chiave] = script
        self._per_entita[script.entity_id] = script

    def gestisce(
        self, servizio: str, dati: Mapping[str, Any], bersaglio: Mapping[str, Any]
    ) -> bool:
        """Se ``script.<servizio>`` con questi dati è per gli script del motore.

        ``script.turn_on``, ``turn_off`` e ``toggle`` lo sono quando tutte le entità
        citate sono script del motore; script del motore e altri insieme sono un errore
        (il package non li mescola)."""
        if servizio in self.script:
            return True
        if servizio not in (ACCENDI, SPEGNI, INVERTI):
            return False
        entita = bersaglio.get(ATTR_ENTITY_ID, dati.get(ATTR_ENTITY_ID))
        if entita is None:
            return False
        try:
            nomi = cv.comp_entity_ids(entita)
        except probatio.Invalid:
            return False
        if isinstance(nomi, str):
            return False
        nostri = [n for n in nomi if n in self._per_entita]
        if not nostri:
            return False
        if len(nostri) != len(nomi):
            raise HomeAssistantError(
                f"script.{servizio}: script del motore e altri script insieme: {nomi}"
            )
        return True

    async def chiama(
        self,
        servizio: str,
        dati: Mapping[str, Any],
        bersaglio: Mapping[str, Any],
        contesto: Context,
        *,
        risposta: bool = False,
    ) -> ServiceResponse:
        """La chiamata ``script.<servizio>`` (come ``ServiceRegistry.async_call`` e i
        servizi del dominio ``script``), senza l'evento ``call_service``."""
        dati_servizio = dict(dati)
        if bersaglio:
            dati_servizio.update(bersaglio)
        if (script := self.script.get(servizio)) is not None:
            # ScriptEntity._service_handler (schema: un dizionario qualsiasi; risposta
            # facoltativa, uno script del package non ne dà)
            await script.esegui(dati_servizio, contesto)
            return {} if risposta else None
        if risposta:
            raise probatio.Invalid(
                "Script does not support 'response_variable' for service "
                f"'script.{servizio}' which does not support response data."
            )
        validati = SCHEMA_ACCENDI_SPEGNI(dati_servizio)
        voluti = set(validati[ATTR_ENTITY_ID])
        # come async_extract_entities: nell'ordine delle entità, ognuna una volta
        scelti = [s for s in self.script.values() if s.entity_id in voluti]
        variabili = validati.get(ATTR_VARIABLES)
        if servizio == ACCENDI:
            for script in scelti:
                await script.avvia(variabili, contesto)
        elif servizio == SPEGNI:
            # come _turn_off_service: tutti insieme
            if scelti:
                await asyncio.wait([create_eager_task(s.ferma()) for s in scelti])
        else:
            # come _toggle_service e ToggleEntity.async_toggle
            for script in scelti:
                if script.in_corso:
                    await script.ferma()
                else:
                    await script.avvia(variabili, contesto)
        return None

    async def scarica(self) -> None:
        for script in self.script.values():
            await script.scarica()


# --- comandi ---------------------------------------------------------------------------


def nome_valido(argomenti: list[str]) -> str | None:
    """Il nome che vmc_<nome>_script_cambio_nome.sh manda alla VMC (``NOME="$*"``), o
    None se non è valido (lo script non manda nulla)."""
    nome = " ".join(argomenti)
    return nome if _NOME_VALIDO.fullmatch(nome) else None


class ComandiVMC:
    """I comandi di shell del package di una VMC, con l'aggancio per chi li ascolta."""

    def __init__(
        self,
        c: Contesto,
        comandi: Iterable[Comando],
        *,
        invia: Invia | None = None,
    ) -> None:
        self.c = c
        self.hass = c.hass
        self.comandi = {comando.nome: comando for comando in comandi}
        self.invia = invia
        self._ascoltatori: list[
            tuple[HassJob[[Event], Any], Callable[[Mapping[str, Any]], bool] | None]
        ] = []

    def __contains__(self, nome: object) -> bool:
        return nome in self.comandi

    # --- aggancio ----------------------------------------------------------------------

    @callback
    def ascolta(
        self,
        ascoltatore: Callable[[Event], Any],
        filtro: Callable[[Mapping[str, Any]], bool] | None = None,
    ) -> CALLBACK_TYPE:
        """L'aggancio diretto: ``ascoltatore`` riceve l'evento ``call_service`` di ogni
        comando eseguito (i cui dati passano ``filtro``), come un ascoltatore del bus
        (``hass.bus.async_listen(EVENT_CALL_SERVICE, ...)``)."""
        voce = (HassJob(ascoltatore, f"comando {ascoltatore}"), filtro)
        self._ascoltatori.append(voce)

        @callback
        def togli() -> None:
            self._ascoltatori.remove(voce)

        return togli

    @callback
    def notifica(self, nome: str, dati: Mapping[str, Any], contesto: Context) -> None:
        """L'evento ``call_service`` del comando ``nome`` agli ascoltatori, nel canale del
        motore (dove il bus di Home Assistant lo consegnerebbe: subito, o dopo la consegna
        in corso)."""
        cambi_interni(self.hass).manda(
            self._notifica, {"nome": nome, "dati": dati}, contesto
        )

    @callback
    def _notifica(self, annuncio: Event[Any]) -> None:
        """Come ``EventBus._async_dispatch``: un solo evento, creato per il primo
        ascoltatore che lo vuole, gli ascoltatori di quel momento nell'ordine in cui si
        sono agganciati."""
        dati_evento = {
            ATTR_DOMAIN: DOMINIO_COMANDI,
            ATTR_SERVICE: annuncio.data["nome"],
            ATTR_SERVICE_DATA: annuncio.data["dati"],
        }
        evento: Event[Any] | None = None
        for job, filtro in list(self._ascoltatori):
            if filtro is not None:
                try:
                    if not filtro(dati_evento):
                        continue
                except Exception:
                    _LOGGER.exception("Error in event filter")
                    continue
            if evento is None:
                evento = Event(
                    EVENT_CALL_SERVICE,
                    dati_evento,
                    EventOrigin.local,
                    annuncio.time_fired_timestamp,
                    annuncio.context,
                )
            try:
                self.hass.async_run_hass_job(job, evento)
            except Exception:
                _LOGGER.exception("Error running job: %s", job)

    @callback
    def aggancia_trigger(
        self,
        configurazioni: list[Mapping[str, Any]],
        azione: Callable[..., Any],
        nome: str,
    ) -> CALLBACK_TYPE | None:
        """I trigger ``event`` segnati ``AGGANCIO`` di un'automazione, agganciati qui con
        le regole di ``async_initialize_triggers`` (``trigger.id`` e ``trigger.idx``
        dalla posizione) e del trigger ``event`` (filtro sui dati, ``handle_event``)."""
        segnati = [
            (indice, conf)
            for indice, conf in enumerate(configurazioni)
            if conf.get(AGGANCIO)
        ]
        # prima si controllano tutti: un errore non lascia nulla agganciato
        for _, conf in segnati:
            tipi = [
                t.template if isinstance(t, Template) else t for t in conf["event_type"]
            ]
            if tipi != [EVENT_CALL_SERVICE] or "context" in conf:
                raise HomeAssistantError(
                    f"{nome}: trigger dei comandi non agganciabile: {conf}"
                )
        togli: list[CALLBACK_TYPE] = []
        for indice, conf in segnati:
            voci = dict(conf.get("event_data") or {}).items()
            dati_trigger = {
                "id": conf.get(CONF_ID, f"{indice}"),
                "idx": f"{indice}",
                "alias": conf.get("alias"),
            }
            togli.append(
                self.ascolta(
                    self._gestore(
                        HassJob(azione, f"event trigger {nome}"), dati_trigger
                    ),
                    (lambda dati, voci=voci: dati.items() >= voci) if voci else None,
                )
            )
        if not togli:
            return None

        @callback
        def stacca() -> None:
            for funzione in togli:
                funzione()

        return stacca

    def _gestore(
        self, job: HassJob[..., Any], dati_trigger: Mapping[str, Any]
    ) -> Callable[[Event], None]:
        """Come ``handle_event`` del trigger ``event``: l'automazione parte al giro
        successivo del ciclo degli eventi."""
        hass = self.hass

        @callback
        def gestisci(evento: Event) -> None:
            hass.loop.call_soon(
                hass.async_run_hass_job,
                job,
                {
                    "trigger": {
                        **dati_trigger,
                        "platform": "event",
                        "event": evento,
                        "description": f"event '{evento.event_type}'",
                    }
                },
                evento.context,
            )

        return gestisci

    # --- esecuzione --------------------------------------------------------------------

    async def esegui(
        self,
        nome: str,
        dati: Mapping[str, Any],
        bersaglio: Mapping[str, Any],
        contesto: Context,
        *,
        risposta: bool = False,
    ) -> ServiceResponse:
        """``shell_command.<nome>`` (come ``ServiceRegistry.async_call`` e il servizio
        di ``shell_command``): prima chi ascolta, poi il comando.

        Come lo shell_command, un comando che la VMC non riceve o un nome non valido
        finiscono nel registro senza errore per chi chiama; un errore nel modello degli
        argomenti arriva a chi chiama, e così un motore senza ``invia``."""
        comando = self.comandi[nome]
        dati_servizio = dict(dati)
        if bersaglio:
            dati_servizio.update(bersaglio)
        self.notifica(nome, dati_servizio, contesto)
        uscita = ""
        riuscito = True
        if comando.tipo == COMANDO_VMC:
            uscita, riuscito = await self._invia(nome, comando.testo)
        elif comando.tipo == COMANDO_NOME:
            nuovo = nome_valido(self._argomenti(comando, dati_servizio))
            if nuovo is None:
                riuscito = False
                _LOGGER.error("%s: nome non valido, nulla inviato alla VMC", nome)
            else:
                uscita, riuscito = await self._invia(nome, f"VMNM {nuovo}")
        elif comando.tipo != COMANDO_NESSUNO:
            raise HomeAssistantError(f"{nome}: comando di tipo sconosciuto {comando}")
        if not risposta:
            return None
        return {
            "stdout": uscita.strip(),
            "stderr": "",
            "returncode": 0 if riuscito else 1,
        }

    def _argomenti(self, comando: Comando, dati: Mapping[str, Any]) -> list[str]:
        """Gli argomenti del file .sh: il modello reso con i dati della chiamata, diviso
        come lo divideva ``shell_command`` (``shlex.split``)."""
        return shlex.split(self.c.testo(comando.argomenti.funzione, dati))

    async def _invia(self, nome: str, testo: str) -> tuple[str, bool]:
        """Il comando alla VMC; come nc, un comando non ricevuto si annota soltanto."""
        if self.invia is None:
            raise HomeAssistantError(f"{nome}: nessun collegamento con la VMC")
        try:
            uscita = await self.invia(testo)
        except (ErroreVMC, TimeoutError, OSError) as err:
            _LOGGER.error("%s: comando %r non inviato alla VMC: %s", nome, testo, err)
            return "", False
        return str(uscita or ""), True
