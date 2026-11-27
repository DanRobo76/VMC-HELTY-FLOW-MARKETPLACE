"""Il motore tradotto di una VMC su Home Assistant: logiche, script e comandi.

Ogni automazione del package è una logica dell'integrazione (``logiche.Logica``): nessuna
entità, i trigger agganciati con il codice dell'integrazione (``attivazioni``) e lo stato
che l'automazione scriveva tenuto fra i valori interni (``stati_logiche``). Ogni script del
package è uno script interno (``interni.ScriptInterno``) e ogni comando di shell un comando
del motore (``interni.ComandiVMC``). Alla chiusura di Home Assistant le esecuzioni in
corso si fermano con le regole degli script di Home Assistant (``chiusura``).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.script_variables import ScriptVariables

from .contesto import Contesto
from .definizioni import Automazione, Comando, Script
from .esecuzione import ComeScript, Modello, Sequenza
from .interni import CambiaIp, ComandiVMC, Invia, ScriptInterni, ScriptInterno
from .logiche import DOMINIO as DOMINIO_LOGICHE
from .logiche import Logica
from .memoria_interna import MemoriaInterna
from .stati_logiche import stati_logiche
from .timer import TRIGGER as TRIGGER_TIMER
from .timer import TimerDelMotore, attacca_trigger_timer

DOMINIO_SCRIPT = "script"

ScriptComeEntita = Callable[["Motore", list[tuple[Script, Sequenza]]], Awaitable[None]]
"""Per le prove della fase 3 (il codice di ``generato/``, che chiama gli script come
servizi di Home Assistant): crea le entità degli script del package sopra le loro
sequenze. Non serve all'integrazione."""


class Motore:
    """Il motore tradotto di una VMC su Home Assistant."""

    def __init__(
        self,
        hass: HomeAssistant,
        nome: str = "master",
        memoria: MemoriaInterna | None = None,
    ) -> None:
        """Il motore della VMC ``nome``; con ``memoria`` (fase 4) i valori interni sono
        nella memoria interna invece che negli aiutanti di oggi."""
        self.hass = hass
        self.c = Contesto(hass, nome)
        if memoria is not None:
            self.c.usa_memoria(memoria)
        self.stati = stati_logiche(hass)
        self.sequenze: list[Sequenza] = []
        self.automazioni: list[Logica] = []
        self.script: list[Any] = []

    def _come_template(self, valore: Any) -> Any:
        """Le variabili di un'automazione si rendono come in Home Assistant: Template al
        posto di ``Modello``."""
        if isinstance(valore, Modello):
            return self.c.modello(valore.funzione)
        if isinstance(valore, list):
            return [self._come_template(v) for v in valore]
        if isinstance(valore, Mapping):
            return {
                self._come_template(k): self._come_template(v)
                for k, v in valore.items()
            }
        return valore

    def _logica(self, a: Automazione) -> Logica:
        sequenza = Sequenza(
            self.c,
            a.alias,
            a.corpo,
            a.modo,
            a.massimo,
            avviso_massimo=a.avviso_massimo,
            dominio=DOMINIO_LOGICHE,
        )
        self.sequenze.append(sequenza)
        variabili = (
            ScriptVariables(self._come_template(dict(a.variabili)))
            if a.variabili
            else None
        )
        return Logica(
            self.c,
            a,
            sequenza,
            self.stati,
            comandi=self.c.comandi,
            altre_piattaforme={TRIGGER_TIMER: attacca_trigger_timer},
            variabili=variabili,
        )

    def _sequenza_script(self, s: Script) -> Sequenza:
        sequenza = Sequenza(
            self.c,
            s.alias or s.chiave,
            s.corpo,
            s.modo,
            s.massimo,
            avviso_massimo=s.avviso_massimo,
            variabili=s.variabili,
            dominio=DOMINIO_SCRIPT,
        )
        self.sequenze.append(sequenza)
        return sequenza

    async def avvia(
        self,
        crea: Callable[[Contesto], tuple[list[Automazione], list[Script]]]
        | None = None,
        *,
        comandi: Callable[[Contesto], list[Comando]] | None = None,
        invia: Invia | None = None,
        cambia_ip: CambiaIp | None = None,
        timer: Mapping[str, Mapping[str, Any] | None] | None = None,
        script_come_entita: ScriptComeEntita | None = None,
    ) -> None:
        """Crea e avvia le logiche e gli script del motore (``crea``: quelli del package,
        o altri per le prove).

        Gli script restano dentro il motore (``ScriptInterni``, nessuna entità). Con
        ``comandi`` (fase 4: la funzione ``comandi`` del codice tradotto) i comandi di
        shell sono comandi del motore (``ComandiVMC``): vanno alla VMC con ``invia`` (il
        client TCP) e il cambio d'indirizzo all'integrazione con ``cambia_ip``.

        ``timer`` (fase 4): la configurazione dei timer del motore (come la chiave
        ``timer:`` del package), per il codice tradotto con ``timer_motore``; senza, il
        motore non ha timer (il codice di ``generato/`` usa i timer di Home Assistant).

        ``script_come_entita`` (solo prove della fase 3): crea le entità degli script al
        posto degli script interni.
        """
        if crea is None:
            from .generato.motore import crea

        if timer is not None:
            self.c.timer = TimerDelMotore(self.c, timer)
            await self.c.timer.prepara()
        automazioni, script = crea(self.c)
        if script_come_entita is not None:
            await script_come_entita(
                self, [(s, self._sequenza_script(s)) for s in script]
            )
        else:
            self.c.interni = ScriptInterni()
            for s in script:
                self.c.interni.aggiungi(
                    ScriptInterno(s.chiave, ComeScript(self._sequenza_script(s)))
                )
        if comandi is not None:
            self.c.comandi = ComandiVMC(
                self.c, comandi(self.c), invia=invia, cambia_ip=cambia_ip
            )
        self.automazioni = [self._logica(a) for a in automazioni]
        # come le entità aggiunte una dopo l'altra: ognuna aggancia i trigger (o lo
        # rimanda all'avvio di Home Assistant) e scrive il primo stato
        for logica in self.automazioni:
            await logica.avvia()

    async def ferma(self) -> None:
        """Le logiche si staccano (le esecuzioni in corso si fermano, gli stati interni
        si tolgono), poi gli script del motore si fermano e non ripartono più."""
        for logica in self.automazioni:
            await logica.ferma()
        await self.scarica_interni()

    async def scarica_interni(self) -> None:
        """Gli script del motore si fermano e non ripartono più. Gli agganci dei comandi
        li staccano le logiche quando si fermano, come i loro altri trigger."""
        if self.c.interni is not None:
            await self.c.interni.scarica()
