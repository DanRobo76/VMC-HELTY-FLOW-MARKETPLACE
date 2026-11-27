"""Esecuzioni del motore, con le stesse regole dello script engine di Home Assistant.

Ogni automazione e ogni script del package e' una ``Sequenza`` (come
``homeassistant.helpers.script.Script``) con la stessa modalita': ``queued`` con lo stesso
massimo, ``restart``, ``single`` o ``parallel``. Ogni avvio e' un'``Esecuzione`` (come
``_ScriptRun``); ogni sequenza annidata (``choose``, ``if``, ``repeat``, ``sequence``) e'
una ``SequenzaAnnidata`` (come lo Script di una sequenza annidata in Home Assistant) e i
suoi avvii sono esecuzioni figlie in un proprio task, come in Home Assistant, cosi'
l'ordine con cui le esecuzioni si alternano allo stesso istante resta lo stesso.

Il corpo di una sequenza e' una funzione ``async def corpo(r)`` scritta dal traduttore:
``r`` e' l'esecuzione, con le variabili (``r.V``), il contesto del motore (``r.c``) e i
passi (``r.servizio``, ``r.pausa``, ``r.attendi``, ``r.sotto``...).
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable, Iterable, Mapping
from datetime import timedelta
from typing import TYPE_CHECKING, Any

import async_interrupt
import probatio
from homeassistant.components.logger import LOGSEVERITY
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_EXCLUDE,
    ENTITY_MATCH_ALL,
    ENTITY_MATCH_NONE,
)
from homeassistant.core import Context, HomeAssistant
from homeassistant.exceptions import (
    ConditionError,
    HomeAssistantError,
    InvalidEntityFormatError,
    NoEntitySpecifiedError,
    ServiceNotFound,
    TemplateError,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.script import script_stack_cv
from homeassistant.util.async_ import create_eager_task

from .chiusura import registro_sequenze

if TYPE_CHECKING:
    from .contesto import Contesto

_LOGGER = logging.getLogger(__name__)

MODO_QUEUED = "queued"
MODO_RESTART = "restart"
MODO_SINGLE = "single"
MODO_PARALLEL = "parallel"

# Come CONFIGURATION_ERRORS di Home Assistant: non si ignorano con continue_on_error.
ERRORI_CONFIGURAZIONE = (
    probatio.Invalid,
    TemplateError,
    ServiceNotFound,
    InvalidEntityFormatError,
    NoEntitySpecifiedError,
    ConditionError,
)

# Come REPEAT_WARN_ITERATIONS / REPEAT_TERMINATE_ITERATIONS di Home Assistant.
GIRI_AVVISO = 5000
GIRI_MASSIMI = 10000

Corpo = Callable[["Esecuzione"], Awaitable[None]]
Condizione = Callable[["Contesto", Mapping[str, Any]], bool]


class Ferma(Exception):
    """Azione «stop» (come _StopScript): finisce l'esecuzione di primo livello."""


class Annulla(Exception):
    """Azione «stop» con errore, o attesa scaduta senza continuare (come _AbortScript)."""


class ErroreCondizione(ConditionError):
    """Una condizione non si e' potuta valutare (come ConditionErrorMessage)."""

    def __init__(self, messaggio: str) -> None:
        super().__init__(messaggio)
        self.messaggio = messaggio

    def output(self, indent: int) -> Any:
        yield self._indent(indent, self.messaggio)

    def __str__(self) -> str:
        return self.messaggio


class _Fermata(Exception):
    """L'esecuzione e' stata fermata (come ScriptStoppedError)."""


class Modello:
    """Un modello Jinja tradotto, dentro dati, attese o variabili (come Template)."""

    __slots__ = ("funzione",)

    def __init__(self, funzione: Callable[[Contesto, Mapping[str, Any]], str]) -> None:
        self.funzione = funzione


class Variabili:
    """Variabili di un'esecuzione, con gli ambiti di ScriptRunVariables senza «parallel».

    Senza azioni «parallel» ogni assegnazione va nell'ambito di primo livello; solo
    ``repeat`` e' locale al proprio ciclo (define_local). I cicli annidati hanno ognuno il
    proprio ``repeat``: si tengono in una pila. Come ScriptRunVariables (_assign: la
    variabile va nell'ambito piu' vicino in cui e' definita) un'assegnazione di ``repeat``
    dentro un ciclo cambia il ``repeat`` del ciclo piu' interno. Come ScriptRunVariables
    non e' un ``dict``: chi la copia (``dict(V)``, ``kwargs.update(V)``, che leggono
    ``keys()`` e ``V[nome]``) vede il ``repeat`` del ciclo piu' interno.

    Ha solo cio' che usano il codice tradotto, il motore e Home Assistant (``V[nome]``,
    ``V[nome] = valore``, ``nome in V``, ``keys()``): nessuno toglie variabili, ne' le
    conta.
    """

    __slots__ = ("_ripeti", "_valori")

    def __init__(self, iniziali: Mapping[str, Any] | None = None) -> None:
        self._valori: dict[str, Any] = dict(iniziali or {})
        self._ripeti: list[dict[str, Any]] = []

    def __getitem__(self, nome: str) -> Any:
        if nome == "repeat" and self._ripeti:
            return self._ripeti[-1]
        return self._valori[nome]

    def __setitem__(self, nome: str, valore: Any) -> None:
        if nome == "repeat" and self._ripeti:
            self._ripeti[-1] = valore
            return
        self._valori[nome] = valore

    def __contains__(self, nome: object) -> bool:
        return (nome == "repeat" and bool(self._ripeti)) or nome in self._valori

    def keys(self) -> list[str]:
        """I nomi delle variabili, con il ``repeat`` del ciclo piu' interno."""
        if self._ripeti and "repeat" not in self._valori:
            return [*self._valori, "repeat"]
        return list(self._valori)


def rendi_variabili(
    c: Contesto, valori: Mapping[str, Any], avvio: Mapping[str, Any] | None
) -> dict[str, Any]:
    """Come ScriptVariables.async_render (``variables`` di un'automazione o di uno
    script): una per volta, ognuna vede le precedenti; quelle dell'avvio restano."""
    resi = dict(avvio or {})
    for nome, valore in valori.items():
        if nome in resi:
            continue
        resi[nome] = c.resa_complessa(valore, resi)
    return resi


class Sequenza:
    """Una sequenza di primo livello con la sua modalita' (come Script).

    ``al_cambio`` e' l'ascoltatore dei cambiamenti (come change_listener: la logica
    scrive il proprio stato interno, lo script interno sveglia chi aspetta il suo primo
    cambiamento). Lo mette chi usa la sequenza quando nasce (``logiche.Logica``,
    ``ComeScript``), prima di ogni avvio.
    """

    def __init__(
        self,
        c: Contesto,
        nome: str,
        corpo: Corpo,
        modo: str = MODO_SINGLE,
        massimo: int | None = None,
        *,
        avviso_massimo: str = "WARNING",
        variabili: Mapping[str, Any] | None = None,
        dominio: str = "script",
    ) -> None:
        self.c = c
        self.hass: HomeAssistant = c.hass
        self.nome = nome
        self.corpo = corpo
        self.modo = modo
        # come Script: max_runs predefinito 10 per queued e parallel
        self.massimo = massimo if massimo is not None else 10
        self.esecuzioni: list[Esecuzione] = []
        self._coda = asyncio.Lock()
        self.al_cambio: Callable[[], None] | None = None
        self.avviso_massimo = avviso_massimo
        self.variabili = variabili
        # come Script.unique_id: per la pila degli script in corso (ricorsioni vietate)
        self.id_unico = f"{dominio}.{nome}-{id(self)}"
        self.ultimo_avvio: Any = None
        # come Script.last_action: l'ultimo passo iniziato (alias o descrizione)
        self.ultima_azione: str | None = None
        self._annidate: dict[Corpo, SequenzaAnnidata] = {}

    @property
    def in_corso(self) -> bool:
        return bool(self.esecuzioni)

    def annidata(self, corpo: Corpo) -> SequenzaAnnidata:
        """La sequenza annidata ``corpo`` di questa sequenza (come Script._get_repeat_script,
        _async_get_choose_data...: uno Script per posizione, creato al primo avvio)."""
        if (annidata := self._annidate.get(corpo)) is None:
            annidata = self._annidate[corpo] = SequenzaAnnidata(self, self)
        return annidata

    @property
    def con_massimo(self) -> bool:
        """Come Script.supports_max."""
        return self.modo in (MODO_PARALLEL, MODO_QUEUED)

    def cambiato(self) -> None:
        """Come Script._changed."""
        self.al_cambio()  # type: ignore[misc]

    async def esegui(
        self,
        variabili: Mapping[str, Any] | None,
        contesto: Context,
        avviata: Callable[[], None] | None = None,
    ) -> None:
        """Come Script.async_run di primo livello: un errore arriva al chiamante.

        Il contesto c'e' sempre: la logica passa quello del trigger, lo script quello
        della chiamata del servizio."""
        if registro_sequenze(self.hass).vietate:
            _LOGGER.info(
                "%s: Home Assistant is shutting down, starting script blocked",
                self.nome,
            )
            return
        if self.in_corso:
            if self.modo == MODO_SINGLE:
                self._avviso("Already running")
                return
            if self.modo != MODO_RESTART and len(self.esecuzioni) == self.massimo:
                self._avviso("Maximum number of runs exceeded")
                return
        if self.variabili:
            try:
                variabili = rendi_variabili(self.c, self.variabili, variabili)
            except TemplateError as err:
                _LOGGER.error("%s: Error rendering variables: %s", self.nome, err)
                raise
        V = Variabili(variabili)
        V["context"] = contesto
        pila = script_stack_cv.get()
        if (
            self.modo in (MODO_RESTART, MODO_QUEUED)
            and pila is not None
            and self.id_unico in pila
        ):
            elenco = "\n".join(f"- {voce.partition('-')[0]}" for voce in pila)
            _LOGGER.warning(
                "%s: Disallowed recursion detected, %s tried to start %s which is "
                "already running in the current execution path; "
                "Traceback (most recent call last):\n%s",
                self.nome,
                pila[-1].partition("-")[0],
                self.id_unico.partition("-")[0],
                elenco,
            )
            return
        esecuzione = Esecuzione(self, V, contesto, coda=self.modo == MODO_QUEUED)
        c_erano = bool(self.esecuzioni)
        self.esecuzioni.append(esecuzione)
        if self.modo == MODO_RESTART and c_erano:
            await self.ferma(aggiorna=False, risparmia=esecuzione)
        if avviata is not None:
            avviata()
        self.ultimo_avvio = self.c.adesso_utc()
        self.cambiato()
        try:
            await asyncio.shield(create_eager_task(esecuzione.esegui()))
        except asyncio.CancelledError:
            await esecuzione.ferma()
            self.cambiato()
            raise

    def _avviso(self, messaggio: str) -> None:
        """Come Script._log con max_exceeded (SILENT: niente)."""
        if self.avviso_massimo != "SILENT":
            _LOGGER.log(
                LOGSEVERITY[self.avviso_massimo], "%s: %s", self.nome, messaggio
            )

    async def ferma(
        self, aggiorna: bool = True, risparmia: Esecuzione | None = None
    ) -> None:
        """Come Script.async_stop."""
        attese = [
            create_eager_task(e.ferma()) for e in self.esecuzioni if e is not risparmia
        ]
        if not attese:
            return

        async def _aspetta() -> None:
            await asyncio.wait(attese)
            if aggiorna:
                self.cambiato()

        await asyncio.shield(create_eager_task(_aspetta()))


class ComeScript:
    """La parte di ``Script`` di Home Assistant che usa uno script del package
    (``interni.ScriptInterno``), sopra una ``Sequenza`` del motore.

    Come ogni ``Script`` di primo livello si iscrive nel registro delle sequenze
    (``chiusura.RegistroSequenze``): alla chiusura di Home Assistant le esecuzioni in corso
    si fermano e, 60 secondi dopo, non ne partono più, con le regole degli script di Home
    Assistant.
    """

    def __init__(self, sequenza: Sequenza) -> None:
        self.sequenza = sequenza
        self.name = sequenza.nome
        self._scaricato = False
        self._togli = registro_sequenze(sequenza.hass).iscrivi(sequenza)

    def _al_cambio(self, ascoltatore: Callable[[], None]) -> None:
        self.sequenza.al_cambio = ascoltatore

    # come Script.change_listener: lo scrive chi usa lo script, nessuno lo legge
    change_listener = property(fset=_al_cambio)

    @property
    def is_running(self) -> bool:
        return self.sequenza.in_corso

    @property
    def runs(self) -> int:
        return len(self.sequenza.esecuzioni)

    @property
    def script_mode(self) -> str:
        return self.sequenza.modo

    @property
    def max_runs(self) -> int:
        return self.sequenza.massimo

    @property
    def supports_max(self) -> bool:
        return self.sequenza.con_massimo

    @property
    def last_triggered(self) -> Any:
        return self.sequenza.ultimo_avvio

    @property
    def last_action(self) -> str | None:
        return self.sequenza.ultima_azione

    async def async_run(
        self,
        run_variables: Mapping[str, Any] | None = None,
        context: Context | None = None,
        started_action: Callable[..., Any] | None = None,
    ) -> None:
        """Come Script.async_run (nessuno script del package restituisce dati)."""
        if self._scaricato:
            raise RuntimeError(
                f"Cannot run script '{self.name}' after it has been unloaded"
            )
        await self.sequenza.esegui(run_variables, context, started_action)  # type: ignore[arg-type]

    async def async_stop(self, update_state: bool = True, spare: Any = None) -> None:
        await self.sequenza.ferma(aggiorna=update_state)

    async def async_unload(self) -> None:
        """Come Script.async_unload: niente più esecuzioni, si fermano quelle in corso
        e lo script esce dal registro delle sequenze. Si chiama una volta sola."""
        self._scaricato = True
        await self.sequenza.ferma()
        self._togli()


class SequenzaAnnidata:
    """Una sequenza annidata (come lo Script di una ``choose``, ``if``, ``repeat`` o
    ``sequence`` in Home Assistant: modalita' ``parallel`` con il massimo della sequenza di
    primo livello).

    Come in Home Assistant e' una per posizione, comune a tutte le esecuzioni che la
    avviano: le esecuzioni in corso e l'ultimo passo (last_action) sono suoi, e finche' e'
    in corso passa i cambiamenti a quella che la contiene (_chain_change_listener), con il
    proprio ultimo passo.
    """

    __slots__ = ("_annidate", "contenitore", "esecuzioni", "sequenza", "ultima_azione")

    def __init__(
        self, sequenza: Sequenza, contenitore: Sequenza | SequenzaAnnidata
    ) -> None:
        self.sequenza = sequenza
        self.contenitore = contenitore
        self.esecuzioni: list[Esecuzione] = []
        self.ultima_azione: str | None = None
        self._annidate: dict[Corpo, SequenzaAnnidata] = {}

    @property
    def in_corso(self) -> bool:
        return bool(self.esecuzioni)

    def annidata(self, corpo: Corpo) -> SequenzaAnnidata:
        """Come ``Sequenza.annidata``."""
        if (annidata := self._annidate.get(corpo)) is None:
            annidata = self._annidate[corpo] = SequenzaAnnidata(self.sequenza, self)
        return annidata

    def cambiato(self) -> None:
        """Come Script._changed di una sequenza annidata: _chain_change_listener di quella
        che la contiene."""
        if self.esecuzioni:
            self.contenitore.ultima_azione = self.ultima_azione
            self.contenitore.cambiato()


class Esecuzione:
    """Un'esecuzione di una sequenza, o di una sequenza annidata (come _ScriptRun).

    ``script`` e' la sequenza eseguita (come _ScriptRun._script): la ``Sequenza`` di primo
    livello o una ``SequenzaAnnidata``, con le esecuzioni in corso e l'ultimo passo.
    """

    def __init__(
        self,
        sequenza: Sequenza,
        V: Variabili,
        contesto: Context,
        *,
        coda: bool = False,
        script: SequenzaAnnidata | None = None,
    ) -> None:
        self.sequenza = sequenza
        self.script: Sequenza | SequenzaAnnidata = (
            sequenza if script is None else script
        )
        self.c: Contesto = sequenza.c
        self.hass = sequenza.hass
        self.V = V
        self.contesto = contesto
        self._coda = coda
        self._con_coda = False
        self._fermo: asyncio.Future[None] = self.hass.loop.create_future()
        self._fermata = asyncio.Event()
        self._partita = False

    # --- ciclo di vita (come _ScriptRun / _QueuedScriptRun) ------------------------------

    async def esegui(self, corpo: Corpo | None = None) -> None:
        if self._coda:
            try:
                async with async_interrupt.interrupt(self._fermo, _Fermata, None):
                    await self.sequenza._coda.acquire()
            except _Fermata as err:
                self._fine()
                raise asyncio.CancelledError from err
            self._con_coda = True
        self._partita = True
        primo = self.script is self.sequenza
        # come _ScriptRun.async_run: la pila degli script in corso
        if primo:
            if (pila := script_stack_cv.get()) is None:
                pila = []
                script_stack_cv.set(pila)
            pila.append(self.sequenza.id_unico)
        try:
            if not self._fermo.done():
                await (corpo or self.sequenza.corpo)(self)
        except (Annulla, Ferma):
            if not primo:
                raise
        except _Fermata:
            pass
        finally:
            if primo:
                pila.pop()
            self._fine()

    def _fine(self) -> None:
        """Come _ScriptRun._finish (e _QueuedScriptRun._finish)."""
        if self._con_coda:
            self.sequenza._coda.release()
            self._con_coda = False
        script = self.script
        script.esecuzioni.remove(self)
        if not script.in_corso:
            script.ultima_azione = None
        self.cambiato()
        self._fermata.set()

    async def ferma(self) -> None:
        if not self._fermo.done():
            self._fermo.set_result(None)
        if self._partita:
            await self._fermata.wait()

    def verifica(self) -> None:
        """Tra un passo e l'altro: se l'esecuzione e' stata fermata non si va avanti."""
        if self._fermo.done():
            raise _Fermata

    def passo(self, descrizione: str) -> None:
        """Inizio di un passo (come _step_log): alias del passo o descrizione, ultimo passo
        (Script.last_action) della sequenza eseguita."""
        self.verifica()
        self.script.ultima_azione = descrizione

    def cambiato(self) -> None:
        """Come _ScriptRun._changed: Script._changed della sequenza eseguita (per una
        sequenza annidata, la catena fino all'entita')."""
        if not self._fermo.done():
            self.script.cambiato()

    async def _lunga(self, compito: asyncio.Task[Any]) -> Any:
        """Come _async_run_long_action: un compito lungo interrotto se si ferma."""
        try:
            async with async_interrupt.interrupt(self._fermo, _Fermata, None):
                return await compito
        except _Fermata as err:
            raise asyncio.CancelledError from err

    # --- sequenze annidate ----------------------------------------------------------------

    async def sotto(self, corpo: Corpo) -> None:
        """Una sequenza annidata (choose, if, repeat, sequence), con gli stessi task di
        Home Assistant (_async_run_script: un task di hass, poi Script.async_run che
        protegge con shield il task dell'esecuzione), cosi' le esecuzioni si alternano
        allo stesso modo quando una sequenza annidata riprende dopo una pausa."""
        annidata = self.script.annidata(corpo)
        figlio = Esecuzione(self.sequenza, self.V, self.contesto, script=annidata)
        await self._lunga(
            self.hass.async_create_task(
                _annidata(annidata, figlio, corpo), eager_start=True
            )
        )

    # --- condizioni -----------------------------------------------------------------------

    def prova(self, condizioni: Iterable[Condizione]) -> bool | None:
        """Come _test_conditions: False alla prima falsa, None se una va in errore."""
        try:
            for condizione in condizioni:
                if condizione(self.c, self.V) is False:
                    return False
        except ConditionError as err:
            _LOGGER.warning("%s: errore nella condizione: %s", self.sequenza.nome, err)
            return None
        return True

    def passo_condizione(self, condizione: Condizione, descrizione: str) -> bool:
        """Azione «condition»: un errore vale falso. ``descrizione``: alias o tipo."""
        self.passo(descrizione)
        try:
            return bool(condizione(self.c, self.V))
        except ConditionError as err:
            _LOGGER.warning("%s: errore nella condizione: %s", self.sequenza.nome, err)
            return False

    # --- passi ----------------------------------------------------------------------------

    def resa(self, valore: Any) -> Any:
        """Come render_complex con le variabili dell'esecuzione."""
        return self.c.resa_complessa(valore, self.V)

    def periodo(self, valore: Any) -> timedelta:
        """Durata di una pausa o di un'attesa (come _get_pos_time_period_template): un
        errore ferma l'esecuzione (_AbortScript)."""
        try:
            return cv.positive_time_period(self.resa(valore))
        except (TemplateError, probatio.Invalid) as err:
            _LOGGER.error("Error rendering %s template: %s", self.sequenza.nome, err)
            raise Annulla from err

    async def servizio(
        self,
        azione: str | Modello,
        dati: Mapping[str, Any] | Modello | None = None,
        bersaglio: Mapping[str, Any] | Modello | None = None,
        *,
        entita: list[str] | None = None,
        continua_se_errore: bool = False,
        risposta: str | None = None,
        alias: str | None = None,
    ) -> None:
        """Chiamata di un servizio (come _async_step_call_service).

        Come in Home Assistant, con ``continue_on_error`` si ignora solo un
        HomeAssistantError che non sia di configurazione (_handle_exception): un altro
        errore della chiamata diventa HomeAssistantError, ma un errore che non e' di Home
        Assistant mentre si preparano i parametri (per esempio un bersaglio reso che non e'
        un dizionario) ferma l'esecuzione."""
        self.passo(alias or "call service")
        try:
            dominio_servizio, dati_resi, bersaglio_reso = self._prepara_chiamata(
                azione, dati, bersaglio, entita
            )
            try:
                esito = await self._lunga(
                    self.hass.async_create_task(
                        self.c.chiama_servizio(
                            self,
                            dominio_servizio,
                            dati_resi,
                            bersaglio_reso,
                            risposta=risposta is not None,
                        ),
                        eager_start=True,
                    )
                )
            except (*ERRORI_CONFIGURAZIONE, HomeAssistantError):
                raise
            except Exception as err:
                if not continua_se_errore:
                    raise
                raise HomeAssistantError(err) from err
        except Exception as err:
            # come _handle_exception
            if (
                not continua_se_errore
                or isinstance(err, ERRORI_CONFIGURAZIONE)
                or not isinstance(err, HomeAssistantError)
            ):
                raise
            return
        if risposta is not None:
            self.V[risposta] = esito

    def _prepara_chiamata(
        self,
        azione: str | Modello,
        dati: Mapping[str, Any] | Modello | None,
        bersaglio: Mapping[str, Any] | Modello | None,
        entita: list[str] | None,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        """Servizio, dati e bersaglio resi (come service.async_prepare_call_from_config):
        gli errori dei modelli diventano HomeAssistantError, gli altri restano."""
        if isinstance(azione, Modello):
            dominio_servizio: Any = azione
            try:
                dominio_servizio = self.resa(azione)
                dominio_servizio = cv.service(dominio_servizio)
            except TemplateError as err:
                raise HomeAssistantError(
                    f"Error rendering service name template: {err}"
                ) from err
            except probatio.Invalid as err:
                raise HomeAssistantError(
                    f"Template rendered invalid service: {dominio_servizio}"
                ) from err
        else:
            dominio_servizio = azione
        bersaglio_reso: dict[str, Any] = {}
        if bersaglio is not None:
            try:
                bersaglio_reso.update(self.resa(bersaglio))
                if ATTR_ENTITY_ID in bersaglio_reso:
                    bersaglio_reso[ATTR_ENTITY_ID] = self._entita_valide(
                        bersaglio_reso[ATTR_ENTITY_ID]
                    )
            except TemplateError as err:
                raise HomeAssistantError(
                    f"Error rendering service target template: {err}"
                ) from err
            except probatio.Invalid as err:
                raise HomeAssistantError(
                    "Template rendered invalid entity IDs: "
                    f"{bersaglio_reso[ATTR_ENTITY_ID]}"
                ) from err
            if escludi := bersaglio_reso.get(CONF_EXCLUDE):
                try:
                    bersaglio_reso[CONF_EXCLUDE] = cv.TARGET_EXCLUDE_SCHEMA(escludi)
                except probatio.Invalid as err:
                    raise HomeAssistantError(
                        f"Template rendered invalid exclude block: {escludi}"
                    ) from err
        dati_resi: dict[str, Any] = {}
        if dati is not None:
            try:
                resi = self.resa(dati)
                if not isinstance(resi, dict):
                    raise HomeAssistantError(
                        "Error rendering data template: Result is not a Dictionary"
                    )
                dati_resi.update(resi)
            except TemplateError as err:
                raise HomeAssistantError(
                    f"Error rendering data template: {err}"
                ) from err
        if entita is not None:
            bersaglio_reso[ATTR_ENTITY_ID] = entita
        return dominio_servizio, dati_resi, bersaglio_reso

    def _entita_valide(self, valore: Any) -> Any:
        """Come async_prepare_call_from_config: entity_id del bersaglio validati (anche
        gli id del registro delle entità)."""
        entita = cv.comp_entity_ids_or_uuids(valore)
        if entita in (ENTITY_MATCH_ALL, ENTITY_MATCH_NONE):
            return entita
        return er.async_validate_entity_ids(er.async_get(self.hass), entita)

    async def pausa(self, durata: Any, alias: str | None = None) -> None:
        """Azione «delay» (come _async_step_delay)."""
        self.verifica()
        durata_td = self.periodo(durata)
        self.passo(alias or f"delay {durata_td}")
        secondi = durata_td.total_seconds()
        self.cambiato()
        if not secondi:
            return
        scaduto = self.hass.loop.create_future()
        maniglia = self.hass.loop.call_later(secondi, _completa, scaduto)
        try:
            await asyncio.wait(
                [self._fermo, scaduto], return_when=asyncio.FIRST_COMPLETED
            )
        finally:
            if not scaduto.done():
                maniglia.cancel()

    async def attendi(
        self,
        modello: Callable[[Contesto, Mapping[str, Any]], str],
        timeout: Any = None,
        continua: bool = True,
        alias: str | None = None,
    ) -> None:
        """Azione «wait_template» (come _async_step_wait_template)."""
        self.verifica()
        secondi = None if timeout is None else self.periodo(timeout).total_seconds()
        self.passo(alias or "wait template")
        self.V["wait"] = {"remaining": secondi, "completed": False}
        if self.c.condizione(modello, self.V):
            self.V["wait"]["completed"] = True
            self.cambiato()
            return
        if secondi == 0:
            self.cambiato()
            self._scaduta(continua)
            return
        fatto = self.hass.loop.create_future()
        attese: list[asyncio.Future[None]] = [self._fermo, fatto]
        scaduto = maniglia = None
        if secondi:
            scaduto = self.hass.loop.create_future()
            maniglia = self.hass.loop.call_later(secondi, _completa, scaduto)
            attese.append(scaduto)

        def vero() -> None:
            self.V["wait"]["remaining"] = (
                maniglia.when() - self.hass.loop.time() if maniglia else None
            )
            self.V["wait"]["completed"] = True
            _completa(fatto)

        togli = self.c.segui_attesa(modello, self.V, vero)
        self.cambiato()
        try:
            await asyncio.wait(attese, return_when=asyncio.FIRST_COMPLETED)
            if scaduto is not None and scaduto.done():
                self._scaduta(continua)
        finally:
            if scaduto is not None and not scaduto.done() and maniglia is not None:
                maniglia.cancel()
            togli()

    def _scaduta(self, continua: bool) -> None:
        self.V["wait"]["remaining"] = 0.0
        if not continua:
            raise Annulla("attesa scaduta")

    def variabili(self, valori: Mapping[str, Any], alias: str | None = None) -> None:
        """Azione «variables» (come ScriptVariables.async_simple_render)."""
        self.passo(alias or "assigning variables")
        for nome, valore in valori.items():
            self.V[nome] = self.resa(valore)

    # --- cicli ----------------------------------------------------------------------------

    async def ripeti_finche(
        self, corpo: Corpo, condizioni: Iterable[Condizione]
    ) -> None:
        """repeat/until (come _async_do_step_repeat: un giro dopo l'altro, finche' le
        condizioni o una fermata non lo interrompono)."""
        condizioni = tuple(condizioni)
        self.V._ripeti.append({})
        giro = 0
        try:
            while True:
                giro += 1
                self.V._ripeti[-1] = {"first": giro == 1, "index": giro}
                await self.sotto(corpo)
                if self._fermo.done():
                    break
                if self.prova(condizioni) in (True, None):
                    break
                if giro == GIRI_AVVISO:
                    _LOGGER.warning(
                        "%s: Until condition looped %s times",
                        self.sequenza.nome,
                        GIRI_AVVISO,
                    )
                if giro >= GIRI_MASSIMI:
                    _LOGGER.critical(
                        "%s: Until condition terminated because it looped %s times",
                        self.sequenza.nome,
                        GIRI_MASSIMI,
                    )
                    raise Annulla("ciclo «until» oltre il massimo di giri")
                await asyncio.sleep(0)
        finally:
            self.V._ripeti.pop()

    async def ripeti_mentre(
        self, corpo: Corpo, condizioni: Iterable[Condizione]
    ) -> None:
        """repeat/while (come until, con le condizioni prima di ogni giro)."""
        condizioni = tuple(condizioni)
        self.V._ripeti.append({})
        giro = 0
        try:
            while True:
                giro += 1
                self.V._ripeti[-1] = {"first": giro == 1, "index": giro}
                if self._fermo.done():
                    break
                if not self.prova(condizioni):
                    break
                if giro > 1:
                    if giro == GIRI_AVVISO + 1:
                        _LOGGER.warning(
                            "%s: While condition looped %s times",
                            self.sequenza.nome,
                            GIRI_AVVISO,
                        )
                    if giro > GIRI_MASSIMI:
                        _LOGGER.critical(
                            "%s: While condition terminated because it looped %s times",
                            self.sequenza.nome,
                            GIRI_MASSIMI,
                        )
                        raise Annulla("ciclo «while» oltre il massimo di giri")
                    await asyncio.sleep(0)
                await self.sotto(corpo)
        finally:
            self.V._ripeti.pop()

    async def ripeti_volte(self, corpo: Corpo, volte: Any) -> None:
        """repeat/count."""
        if isinstance(volte, Modello):
            try:
                volte = int(self.resa(volte))
            except (TemplateError, ValueError) as err:
                raise Annulla from err
        self.V._ripeti.append({})
        try:
            for giro in range(1, volte + 1):
                self.V._ripeti[-1] = {
                    "first": giro == 1,
                    "index": giro,
                    "last": giro == volte,
                }
                await self.sotto(corpo)
                if self._fermo.done():
                    break
        finally:
            self.V._ripeti.pop()

    async def ripeti_per_ogni(self, corpo: Corpo, elementi: Any) -> None:
        """repeat/for_each."""
        try:
            elementi = self.resa(elementi)
        except (TemplateError, ValueError) as err:
            raise Annulla from err
        if not isinstance(elementi, list):
            raise Annulla("«for_each» deve essere una lista")
        quanti = len(elementi)
        self.V._ripeti.append({})
        try:
            for giro, elemento in enumerate(elementi, 1):
                # come set_repeat_var con count = quanti, che dentro il ciclo non e' zero
                voce = {"first": giro == 1, "index": giro, "last": giro == quanti}
                if elemento is not None:
                    voce["item"] = elemento
                self.V._ripeti[-1] = voce
                if self._fermo.done():
                    break
                await self.sotto(corpo)
        finally:
            self.V._ripeti.pop()


async def _annidata(
    annidata: SequenzaAnnidata, figlio: Esecuzione, corpo: Corpo
) -> None:
    """Come Script.async_run di una sequenza annidata (modalita' ``parallel``, con il
    massimo della sequenza di primo livello).

    Il massimo non si raggiunge mai. Ogni esecuzione in corso di una sequenza annidata
    viene da un'esecuzione di primo livello diversa e ancora in corso (una figlia esce
    prima che finisca chi l'ha avviata: anche fermata, ``_lunga`` aspetta la fine del
    task di ``_annidata``, che aspetta la figlia), e chi entra non c'e' ancora. Prima di
    entrare ce ne sono quindi al piu' ``massimo - 1`` con ``parallel``, che non avvia
    piu' di ``massimo`` esecuzioni, e nessuna con ``single``, ``queued`` e ``restart``,
    che ne hanno una sola alla volta nel corpo."""
    sequenza = annidata.sequenza
    if registro_sequenze(sequenza.hass).vietate:
        _LOGGER.info(
            "%s: Home Assistant is shutting down, starting script blocked",
            sequenza.nome,
        )
        return
    annidata.esecuzioni.append(figlio)
    annidata.cambiato()
    try:
        await asyncio.shield(create_eager_task(figlio.esegui(corpo)))
    except asyncio.CancelledError:
        await figlio.ferma()
        annidata.cambiato()
        raise


def _completa(futuro: asyncio.Future[None]) -> None:
    if not futuro.done():
        futuro.set_result(None)
