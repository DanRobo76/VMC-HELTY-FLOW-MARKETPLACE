"""I sensori con l'istante di fine dei timer del motore (fase 4).

Oggi la scheda mostra i 34 timer del package (``timer.vmc_<nome>_*``): i 29 «countdown»
in righe che compaiono solo mentre il timer è attivo (``state: active``), con il conto
alla rovescia che il frontend calcola da ``finishes_at``; i 5 «lettura» sempre, nella
finestra «Timer Lettura Dati VMC», con il conto alla rovescia e ``last-updated``.
Nell'integrazione nativa i timer sono del motore (``motore/timer.py``) e la scheda legge
questi sensori: ``sensor.vmc_<nome>_<oggetto>`` (lo stesso oggetto del timer), classe
``timestamp``, stato = l'istante di fine (``finishes_at``) mentre il timer è attivo,
``unknown`` quando è fermo (o in pausa, che il package non usa). Nessun attributo.

Il registro di Home Assistant scrive una riga a ogni cambio di stato di un sensore, e
un'integrazione del catalogo non può escludere le sue entità: per questo il sensore
cambia solo quando cambia l'istante di fine. I timer «lettura» finiscono e ripartono
subito (la Countdown Letture VMC li riavvia nello stesso istante): la fine si scrive solo
se il timer non riparte entro ``ATTESA_LETTURE`` secondi, così ogni giro è una riga sola
(il nuovo istante di fine) invece di due (``unknown`` e poi il nuovo istante).

Progetto E (``SOLO_CON_LA_FINESTRA``, il valore normale): la scheda mostra i 5 sensori
«lettura» solo dentro la finestra «Prossime letture», quindi scrivono solo mentre il suo
interruttore (``switch.vmc_<nome>_opzione_finestra_prossime_letture``) è acceso.
All'accensione ognuno scrive subito l'istante di fine di quel momento (o ``unknown``),
così la scheda mostra il conto giusto dal primo istante; da spenta resta l'ultimo stato
scritto. Con ``solo_con_la_finestra=False`` (progetto A, «Sempre») scrivono sempre.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.components.timer.const import STATUS_IDLE
from homeassistant.const import STATE_ON
from homeassistant.core import CALLBACK_TYPE, callback
from homeassistant.helpers.event import async_call_later

from .entita import nome_visibile
from .motore.timer import TimerDelMotore, TimerMotore
from .stato import Cambi, StatoVMC
from .tabelle import DOMANI, IMPOSTAZIONI

# Secondi che un timer «lettura» finito aspetta prima di scrivere la fine: la Countdown
# Letture VMC lo riavvia nello stesso istante in cui finisce.
ATTESA_LETTURE = 1.0

# L'interruttore della finestra «Prossime letture» della scheda (chiave di StatoVMC).
CHIAVE_FINESTRA = "input_boolean.opzione_finestra_prossime_letture"

# Progetto E (True, il valore normale): i sensori «lettura» scrivono solo mentre la
# finestra «Prossime letture» è accesa. False: progetto A («Sempre»), scrivono sempre.
SOLO_CON_LA_FINESTRA = True


class SensoreTimer(SensorEntity):
    """L'istante di fine di un timer del motore (``unknown`` quando è fermo)."""

    _attr_should_poll = False
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(
        self,
        timer: TimerDelMotore,
        stato: StatoVMC,
        chiave: str,
        *,
        solo_con_la_finestra: bool = SOLO_CON_LA_FINESTRA,
    ) -> None:
        """Sensore del timer ``chiave`` (es. «timer.countdown_avvisi») della VMC di
        ``stato``; ``solo_con_la_finestra`` vale per i timer «lettura»."""
        nome = stato.nome
        voce = IMPOSTAZIONI[chiave]
        oggetto = f"vmc_{nome}_{chiave.split('.', 1)[1]}"
        self._registro = timer
        self._timer: TimerMotore = timer.timer[f"timer.{oggetto}"]
        self.entity_id = f"sensor.{oggetto}"
        self._attr_unique_id = oggetto
        self._attr_name = nome_visibile(voce["name"], nome)
        self._attr_icon = voce.get("icon")
        lettura = chiave.startswith("timer.lettura_")
        self._attesa = ATTESA_LETTURE if lettura else 0.0
        self._finestra: StatoVMC | None = (
            stato if lettura and solo_con_la_finestra else None
        )
        # l'entity_id dell'interruttore della finestra (switch.vmc_<nome>_...)
        self._interruttore = (
            f"{DOMANI[CHIAVE_FINESTRA]}.vmc_{nome}_{CHIAVE_FINESTRA.split('.', 1)[1]}"
        )
        self._fine: datetime | None = self._timer.fine
        self._annulla_attesa: CALLBACK_TYPE | None = None

    @property
    def native_value(self) -> datetime | None:
        return self._fine

    @property
    def segue_la_finestra(self) -> bool:
        """Vero se scrive solo con la finestra «Prossime letture» accesa (progetto E)."""
        return self._finestra is not None

    async def async_added_to_hass(self) -> None:
        """Segue le scritture del suo timer."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self._registro.ascolta(self._scritto, self._timer.entity_id)
        )
        self.async_on_remove(self._ferma_attesa)
        if self._finestra is not None:
            self.async_on_remove(self._finestra.ascolta(self._cambi_finestra))

    @property
    def _scrive(self) -> bool:
        """Vero se il sensore scrive (progetto A, o finestra «Prossime letture» accesa)."""
        return (
            self._finestra is None or self._finestra.stato(CHIAVE_FINESTRA) == STATE_ON
        )

    @callback
    def _cambi_finestra(self, cambi: Cambi) -> None:
        """Progetto E: la finestra «Prossime letture» si accende o si spegne."""
        vecchio, nuovo = cambi.get(CHIAVE_FINESTRA, (None, None))
        if vecchio == nuovo:
            return
        self._ferma_attesa()
        if not self._scrive:
            # spenta: resta l'ultimo stato scritto
            return
        # accesa: subito l'istante di fine di adesso (o unknown, anche se il timer è
        # appena finito), con il contesto dell'accensione (l'interruttore ha già scritto
        # il suo stato: ascolta StatoVMC «prima» degli altri)
        interruttore = self.hass.states.get(self._interruttore)
        stato = self._timer.stato_ha
        contesto = (
            interruttore.context
            if interruttore is not None
            else None
            if stato is None
            else stato.context
        )
        self._pubblica(self._timer.fine, contesto)

    @callback
    def _ferma_attesa(self) -> None:
        if self._annulla_attesa is not None:
            self._annulla_attesa()
            self._annulla_attesa = None

    @callback
    def _scritto(self, timer: TimerMotore) -> None:
        if not self._scrive:
            return
        fine = timer.fine
        stato = timer.stato_ha
        if (
            fine is None
            and self._attesa
            and timer.state == STATUS_IDLE
            and self._fine is not None
            and stato is not None
            and stato.attributes.get("last_transition") == "finished"
        ):
            # finito: si scrive solo se non riparte subito
            if self._annulla_attesa is None:
                contesto = stato.context

                @callback
                def scaduta(_istante: datetime) -> None:
                    self._pubblica(None, contesto)

                self._annulla_attesa = async_call_later(
                    self.hass, self._attesa, scaduta
                )
            return
        self._ferma_attesa()
        self._pubblica(fine, None if stato is None else stato.context)

    @callback
    def _pubblica(self, fine: datetime | None, contesto: Any) -> None:
        self._annulla_attesa = None
        if fine == self._fine:
            return
        self._fine = fine
        if contesto is not None:
            # lo stesso contesto della scrittura del timer (chi l'ha avviato o fermato)
            self.async_set_context(contesto)
        self.async_write_ha_state()


def crea_sensori_timer(
    timer: TimerDelMotore,
    stato: StatoVMC,
    *,
    solo_con_la_finestra: bool = SOLO_CON_LA_FINESTRA,
) -> list[SensoreTimer]:
    """I 34 sensori dei timer del package della VMC di ``stato``."""
    return [
        SensoreTimer(timer, stato, chiave, solo_con_la_finestra=solo_con_la_finestra)
        for chiave in IMPOSTAZIONI
        if chiave.startswith("timer.")
    ]


# I timer che i modelli di StatoVMC leggono (solo lo stato): Velocità Registrata legge i
# due timer di annullamento della memoria Free Heating/Cooling.
LETTI_DAI_MODELLI = (
    "timer.countdown_free_heating_annullamento",
    "timer.countdown_free_cooling_annullamento",
)


def collega_a_stato(timer: TimerDelMotore, stato: StatoVMC) -> CALLBACK_TYPE:
    """I timer del motore che i modelli leggono come ingressi di StatoVMC (chiave
    «timer.<oggetto>» senza «vmc_<nome>_», solo lo stato): a ogni scrittura del timer,
    come il sensore modello di oggi che rilegge il timer a ogni suo cambio. Solo questi:
    StatoVMC ricalcola i modelli a ogni ingresso cambiato. Restituisce come smettere."""
    smetti: list[CALLBACK_TYPE] = []
    for chiave in LETTI_DAI_MODELLI:
        t = timer.timer[stato.entity_id(chiave)]

        @callback
        def scritto(t: TimerMotore, chiave: str = chiave) -> None:
            contesto = None if t.stato_ha is None else t.stato_ha.context
            stato.imposta({chiave: t.state}, contesto)

        scritto(t)
        smetti.append(timer.ascolta(scritto, t.entity_id))

    @callback
    def smetti_tutti() -> None:
        for una in smetti:
            una()

    return smetti_tutti
