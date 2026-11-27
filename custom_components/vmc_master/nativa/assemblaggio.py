"""Una VMC nativa intera (fase 4): letture, stato, entità e motore insieme.

Qui si mettono insieme le parti delle fasi 2, 3 e 4 per una VMC, al posto di tutto il
package di oggi (aiutanti, timer, script, comandi di shell, automazioni, sensori
template, tcp, ping e rest):

- ``VMCNativa`` (vmc.py): coordinatori delle letture e ``StatoVMC``, con i 121 modelli;
- le 137 entità dei sensori: 121 sensori calcolati con i modelli tradotti, entità
  dell'integrazione che si comportano come i sensori template (sensori_template.py,
  sensori_modello.py: stessi istanti e stesso ordine dei sensori template di oggi; i
  cambi dei timer del motore arrivano a chi li legge con ``AnnunciDeiTimer``),
  gli altri 16 (letture, sensori con memoria) viste su ``StatoVMC`` (entita.py);
- le 173 impostazioni native (comandi.py), viste su ``StatoVMC``;
- la memoria interna (motore/memoria_interna.py): i 68 valori interni, con il loro
  archivio (``Store``) e i loro cambi anche in ``StatoVMC`` (i sensori che li leggono);
- il motore (motore/ha.py) con il codice tradotto con tutte le opzioni della fase 4
  (``motore/generato_fase4/``: mappa dei nomi, script e comandi di shell dentro il
  motore, timer del motore, valori interni nella memoria): le automazioni restano
  entità ``automation``; il motore legge le entità visibili dalla macchina degli stati
  con i nomi di domani; scrive le impostazioni (e i valori interni insieme a loro) con
  ``ScritturaComandi`` (i servizi degli aiutanti di oggi); manda i comandi alla VMC con
  ``ClientVMC``;
- i 34 sensori con l'istante di fine dei timer del motore (sensori_timer.py);
- i 25 pulsanti degli script e dei comandi della scheda (pulsanti.py).

Il collegamento con la voce di configurazione dell'integrazione è della fase 5:
``VMCAssemblata.avvia`` riceve chi aggiunge le entità a Home Assistant (``aggiungi``),
e ``aggiungi_con_piattaforme`` è il modo interno (simulatore, prove) di farlo senza
voce di configurazione.
"""

from __future__ import annotations

import importlib
import logging
from collections.abc import Awaitable, Callable, Mapping
from datetime import timedelta
from types import ModuleType
from typing import Any

from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import EntityPlatform
from homeassistant.setup import async_setup_component

from .client import ClientVMC
from .comandi import ComandoVMC, ScritturaComandi, crea_comandi
from .entita import crea_entita, nome_visibile
from .motore.ha import Motore
from .motore.interni import CambiaIp
from .motore.memoria_interna import MemoriaInterna
from .pulsanti import PulsanteVMC, crea_pulsanti
from .sensori_template import (
    AnnunciDeiTimer,
    a_gruppi,
    chiave_del_sensore,
    in_ordine,
)
from .sensori_timer import SensoreTimer, collega_a_stato, crea_sensori_timer
from .tabelle import IMPOSTAZIONI
from .vmc import CHIAVE_VERSIONE, VMCNativa

_LOGGER = logging.getLogger(__name__)

DOMINIO = "vmc_master"
CODICE_FASE4 = "custom_components.vmc_master.nativa.motore.generato_fase4.motore"
"""Il codice tradotto della fase 4 (``crea`` e ``comandi``)."""
CODICE_SENSORI = "custom_components.vmc_master.nativa.motore.generato_fase4.sensori"
"""I sensori template tradotti della fase 4 (``sensori``)."""

Aggiungi = Callable[[str, list[Entity]], Awaitable[None]]
"""Chi aggiunge a Home Assistant le entità di un dominio (es. «switch»)."""


def configurazione_timer(nome: str) -> dict[str, dict[str, Any]]:
    """I 34 timer del package della VMC ``nome`` come la chiave ``timer:`` del package
    (oggetto -> nome, icona, durata): la configurazione dei timer del motore."""
    timer: dict[str, dict[str, Any]] = {}
    for chiave, voce in IMPOSTAZIONI.items():
        if not chiave.startswith("timer."):
            continue
        conf: dict[str, Any] = {"name": nome_visibile(voce["name"], nome)}
        for campo in ("icon", "duration"):
            if campo in voce:
                conf[campo] = voce[campo]
        timer[f"vmc_{nome}_{chiave.split('.', 1)[1]}"] = conf
    return timer


class VMCAssemblata:
    """Una VMC dell'integrazione nativa: tutte le sue parti, collegate."""

    def __init__(
        self,
        hass: HomeAssistant,
        nome: str,
        host: str,
        *,
        client: ClientVMC | None = None,
        prova_ping: Callable[[str], Any] | None = None,
        cambia_ip: CambiaIp | None = None,
        codice: ModuleType | None = None,
        codice_sensori: ModuleType | None = None,
        versione: bool = True,
    ) -> None:
        """Le parti della VMC ``nome`` all'indirizzo ``host``.

        ``client`` e ``prova_ping`` (facoltativi) sostituiscono il collegamento TCP e il
        ping veri (prove, simulatore); ``cambia_ip`` è come l'integrazione cambia
        l'indirizzo della VMC (comando «cambio IP» della scheda); ``codice`` è il codice
        tradotto (di norma ``generato_fase4``) e ``codice_sensori`` quello dei sensori
        template (di norma ``generato_fase4.sensori``); con ``versione`` False la lettura della
        versione su GitHub non c'è (nessun sensore e nessuna lettura: come nel
        simulatore, che non va in rete).
        """
        self.hass = hass
        self.nome = nome
        self.vmc = VMCNativa(
            hass,
            None,
            nome,
            host,
            client=client,
            prova_ping=prova_ping,
            versione=versione,
        )
        self.stato = self.vmc.stato
        self.client = self.vmc.client
        self.memoria = MemoriaInterna(hass, nome, stato=self.stato)
        self.motore = Motore(hass, nome, memoria=self.memoria)
        self.c = self.motore.c
        self._codice = codice
        self._cambia_ip = cambia_ip
        self._versione = versione
        if codice_sensori is None:
            codice_sensori = importlib.import_module(CODICE_SENSORI)
        # i sensori template (dopo il motore: i loro modelli leggono come il motore)
        self.template = in_ordine(hass, self.c, codice_sensori, host)
        # la chiave dall'unique_id (nel package è l'oggetto dell'entity_id): l'entity_id
        # che il sensore template si dà da solo evita quelli che hanno uno stato, quindi
        # dopo una ricarica (stati «unavailable» delle entità scaricate) sarebbe «..._2»
        coperti = {
            chiave_del_sensore(f"{e.entity_id.partition('.')[0]}.{e.unique_id}", nome)
            for e in self.template
        }
        sensori, binari = crea_entita(self.stato, self.vmc.letture_dei_sensori())
        if not versione:
            sensori = [s for s in sensori if s.chiave != CHIAVE_VERSIONE]
        # gli altri sensori: letture, sensori con memoria, i modelli che restano
        self.sensori = [s for s in sensori if s.chiave not in coperti]
        self.binari = [s for s in binari if s.chiave not in coperti]
        self.comandi: dict[str, list[ComandoVMC]] = crea_comandi(self.stato)
        self.scrittura = ScritturaComandi(
            hass,
            [voce for gruppo in self.comandi.values() for voce in gruppo],
            memoria=self.memoria,
        )
        self.pulsanti: list[PulsanteVMC] = []
        self.sensori_timer: list[SensoreTimer] = []
        self.annunci_timer: AnnunciDeiTimer | None = None
        self._annulla: list[CALLBACK_TYPE] = []

    @property
    def codice(self) -> ModuleType:
        """Il codice tradotto con tutte le opzioni della fase 4."""
        if self._codice is None:
            self._codice = importlib.import_module(CODICE_FASE4)
        return self._codice

    def entita(self) -> dict[str, list[Entity]]:
        """Le entità della VMC per dominio (dopo ``avvia``)."""
        uscita: dict[str, list[Entity]] = {}
        for dominio, gruppo in self.comandi.items():
            uscita.setdefault(dominio, []).extend(gruppo)
        uscita.setdefault("sensor", []).extend(self.sensori)
        uscita.setdefault("binary_sensor", []).extend(self.binari)
        for dominio, gruppo in a_gruppi(self.template):
            uscita[dominio].extend(gruppo)
        uscita["sensor"].extend(self.sensori_timer)
        uscita.setdefault("button", []).extend(self.pulsanti)
        return uscita

    async def avvia(
        self,
        aggiungi: Aggiungi,
        configurazione: Mapping[str, Any] | None = None,
    ) -> None:
        """Avvia la VMC: impostazioni, letture e sensori, motore, timer e pulsanti.

        ``aggiungi(dominio, entità)`` aggiunge le entità a Home Assistant;
        ``configurazione`` è quella di Home Assistant (per avviare l'integrazione
        ``automation`` se non c'è già).
        """
        # i valori interni e le impostazioni prima di tutto: i loro valori (iniziali o
        # ripristinati, come gli aiutanti all'avvio) sono gli ingressi dei modelli
        await self.memoria.async_carica()
        for dominio, gruppo in self.comandi.items():
            await aggiungi(dominio, list(gruppo))
        await self.vmc.avvia()
        await aggiungi("sensor", list(self.sensori))
        await aggiungi("binary_sensor", list(self.binari))
        # il motore: le impostazioni native per le scritture, poi automazioni, script,
        # comandi e timer
        self.c.scrittura = self.scrittura
        codice = self.codice
        await self.motore.avvia(
            codice.crea,
            configurazione,
            comandi=codice.comandi,
            invia=self.client.comanda,
            cambia_ip=self._cambia_ip,
            timer=configurazione_timer(self.nome),
        )
        # i sensori template dopo il motore: i loro modelli leggono anche dai timer del
        # motore (che ci sono da qui), e i cambi dei timer arrivano a chi li segue.
        # Home Assistant li fa partire all'avvio (EVENT_HOMEASSISTANT_START, prima che
        # le automazioni agganciano i trigger), o subito se è già avviato
        timer = self.c.timer
        assert timer is not None
        self.annunci_timer = AnnunciDeiTimer(self.hass, timer)
        self._annulla.append(self.annunci_timer.ferma)
        # nell'ordine del package, sensori e sensori binari insieme (a_gruppi)
        for dominio, gruppo in a_gruppi(self.template):
            await aggiungi(dominio, gruppo)
        self._annulla.append(collega_a_stato(timer, self.stato))
        self.sensori_timer = crea_sensori_timer(timer, self.stato)
        self.pulsanti = crea_pulsanti(self.c)
        await aggiungi("sensor", list(self.sensori_timer))
        await aggiungi("button", list(self.pulsanti))

    async def ferma(self) -> None:
        """Ferma letture, motore (script e timer) e collegamenti."""
        for annulla in self._annulla:
            annulla()
        self._annulla.clear()
        await self.motore.scarica_interni()
        if self.c.timer is not None:
            self.c.timer.ferma()
        self.vmc.ferma()
        self.memoria.ferma()


async def aggiungi_con_piattaforme(hass: HomeAssistant) -> Aggiungi:
    """Il modo interno di aggiungere le entità senza voce di configurazione (simulatore,
    prove): una piattaforma ``vmc_master`` per dominio, come quelle che la voce di
    configurazione creerà nella fase 5. Avvia le integrazioni dei domini che servono."""
    piattaforme: dict[str, EntityPlatform] = {}

    async def aggiungi(dominio: str, entita: list[Entity]) -> None:
        if (piattaforma := piattaforme.get(dominio)) is None:
            if not await async_setup_component(hass, dominio, {}):
                raise RuntimeError(f"{dominio} non si avvia")
            piattaforma = piattaforme[dominio] = EntityPlatform(
                hass=hass,
                logger=_LOGGER,
                domain=dominio,
                platform_name=DOMINIO,
                platform=None,
                scan_interval=timedelta(seconds=30),
                entity_namespace=None,
            )
        await piattaforma.async_add_entities(entita)

    return aggiungi
