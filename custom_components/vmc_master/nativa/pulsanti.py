"""I pulsanti della VMC: gli script e i comandi di shell che la scheda chiama (fase 4).

Ogni pulsante ha l'oggetto dello script o del comando di oggi
(``script.vmc_<nome>_profilo_audio`` -> ``button.vmc_<nome>_profilo_audio``) e premuto fa
la stessa cosa che fa oggi la scheda, con il contesto della pressione (l'utente che ha
premuto, come la chiamata della scheda):

- pulsante di uno script: ``script.turn_on`` dello script del motore (parte in un task
  suo, la pressione aspetta il primo cambiamento, come la chiamata della scheda);
- pulsante di un comando: ``shell_command.<nome>`` del motore (la pressione aspetta la
  fine del comando; chi ascolta le chiamate dei comandi lo sente come oggi).

Nomi e icone dalla tabella ``PULSANTI`` (tabelle.py).
"""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import Context

from .entita import nome_visibile
from .motore.contesto import Contesto
from .tabelle import PULSANTI

TIPO_SCRIPT = "script"
TIPO_COMANDO = "comando"


class PulsanteVMC(ButtonEntity):
    """Un pulsante della VMC che avvia uno script o un comando del motore."""

    _attr_should_poll = False

    def __init__(self, c: Contesto, chiave: str) -> None:
        """Pulsante per la chiave (es. «button.profilo_audio») della VMC del motore ``c``."""
        voce = PULSANTI[chiave]
        oggetto = chiave.split(".", 1)[1]
        self._c = c
        self._tipo = voce["tipo"]
        # lo script o il comando di oggi con lo stesso oggetto
        self._bersaglio = f"vmc_{c.nome}_{oggetto}"
        self.entity_id = f"button.vmc_{c.nome}_{oggetto}"
        self._attr_unique_id = f"vmc_{c.nome}_{oggetto}"
        self._attr_name = nome_visibile(voce["nome"], c.nome)
        self._attr_icon = voce["icona"]

    async def async_press(self) -> None:
        """Come la chiamata della scheda, con il contesto della pressione."""
        contesto = self._context or Context()
        if self._tipo == TIPO_SCRIPT:
            if self._c.interni is None:
                raise RuntimeError("script del motore non avviati")
            await self._c.interni.chiama(
                "turn_on", {}, {"entity_id": [f"script.{self._bersaglio}"]}, contesto
            )
            return
        if self._c.comandi is None:
            raise RuntimeError("comandi del motore non avviati")
        await self._c.comandi.esegui(self._bersaglio, {}, {}, contesto)


def crea_pulsanti(c: Contesto) -> list[PulsanteVMC]:
    """I 25 pulsanti della VMC del motore ``c`` (13 script e 12 comandi)."""
    return [PulsanteVMC(c, chiave) for chiave in PULSANTI]
