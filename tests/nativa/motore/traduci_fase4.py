"""Il codice generato della fase 4: il package tradotto con tutte le opzioni della fase 4.

``motore/generato/`` resta il codice della fase 3 (aiutanti, timer, script e comandi di
shell di Home Assistant): lo usano i banchi della fase 3 e la variante ``nativa`` del
simulatore. Il motore dell'integrazione nativa (``nativa/assemblaggio.py``) usa invece
``motore/generato_fase4/``, lo stesso package tradotto con:

- la mappa dei nomi (``rinomina.da_fase_1``) per i 173 aiutanti che domani sono entità
  native (colonna «Domani» della fase 1): letture, trigger, condizioni e bersagli con gli
  entity_id di domani; i nomi dei servizi restano quelli degli aiutanti
  (``input_boolean.turn_on``...): il motore li manda alle entità native
  (``ScritturaComandi``, ``Contesto.chiama_servizio``);
- gli script e i comandi di shell dentro il motore (``comandi``);
- i timer del motore (``timer_motore``);
- i valori interni nella memoria del motore (``interni``), quando il traduttore li sa
  tradurre (parte «interni» della fase 4).

Il modulo ``sensori.py`` ha in più i sensori template del package (sezione ``template:``
senza trigger) con la configurazione che Home Assistant valida e i modelli tradotti al
posto dei Template: l'assemblaggio ne fa entità ``StateSensorEntity`` e
``StateBinarySensorEntity`` di Home Assistant, così i sensori si ricalcolano negli stessi
istanti e nello stesso ordine dei sensori template di oggi (ognuno segue le entità che il
suo modello ha letto l'ultima volta, timer del motore compresi).

Si rigenera con ``VMC_RIGENERA=1 pytest tests/nativa/motore/test_traduzione_fase4.py``.
"""

from __future__ import annotations

import enum
import inspect
from typing import Any

import yaml
from homeassistant.components.template.config import async_validate_config
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template

from custom_components.vmc_master.trasforma import (
    adatta_link_repository,
    adatta_versione,
    rimuovi_sezioni_solo_master,
)

from ..genera_tabelle import NOMI_NATIVI
from .rinomina import Rinomina, da_fase_1
from .traduci import (
    INTESTAZIONE,
    PACKAGE,
    RADICE,
    Generatore,
    _Caricatore,
    _moduli_modelli,
    _moduli_motore,
    leggi_comandi,
    leggi_package,
    traduzione,
)
from .traduci_jinja import RINOMINA, TIMER_MOTORE, NonTraducibile, testo_costante

GENERATO_FASE4 = RADICE / "custom_components/vmc_master/nativa/motore/generato_fase4"

# I tipi di aiutante che domani sono entità native (gli interni restano fuori dalla
# mappa: tengono il nome di oggi dentro il motore, come timer, script e comandi).
TIPI_MAPPA = (
    "input_boolean",
    "input_number",
    "input_select",
    "input_text",
    "input_datetime",
)


def mappa_fase4() -> Rinomina:
    """La mappa dei nomi della fase 4: 173 aiutanti -> entità native (nessun servizio)."""
    return da_fase_1(TIPI_MAPPA, {})


def _opzioni_interni() -> dict[str, Any]:
    """Il parametro dei valori interni, se il traduttore lo ha (parte «interni»)."""
    if "interni" not in inspect.signature(traduzione).parameters:
        return {}
    from custom_components.vmc_master.nativa.motore.memoria_interna import INTERNI

    return {"interni": INTERNI}


async def traduci_fase4(hass: HomeAssistant) -> dict[str, str]:
    """I moduli di ``generato_fase4/`` (nome file -> testo), divisi come quelli di
    ``generato/`` (``traduci.traduci``)."""
    automazioni, script = leggi_package()
    jinja, g, _, motore = await traduzione(
        hass,
        automazioni,
        script,
        rinomina=mappa_fase4(),
        comandi=leggi_comandi(),
        timer_motore=True,
        **_opzioni_interni(),
    )
    sensori = await modulo_sensori(hass, g)
    return {
        "__init__.py": '"""Codice generato dal package (fase 4: entità native)."""\n',
        **_moduli_modelli(jinja),
        **_moduli_motore(g, motore),
        "sensori.py": sensori,
    }


_IMPORTA_SENSORI = (
    "\nfrom homeassistant.components.binary_sensor import BinarySensorDeviceClass\n"
    "from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass\n\n"
    "from ...versione import VERSIONE_INTEGRAZIONE\n"
    "from . import modelli as M\n\n"
)
_SEGNAPOSTO_VERSIONE = "VERSIONE_DELL_INTEGRAZIONE"
_IP_DEL_PACKAGE = "999.999.999.999"


def _sensori_template(package: dict[str, Any]) -> list[dict[str, Any]]:
    """Le sezioni ``template:`` del package senza trigger (quelle con i trigger sono i
    sensori con memoria di entita.py)."""
    return [
        sezione
        for sezione in package.get("template", [])
        if "triggers" not in sezione and "trigger" not in sezione
    ]


def _modello_sensore(g: Generatore, template: Template) -> str:
    """Il modello di un sensore template nel codice, come in un trigger (Home Assistant
    lo segue), comprese le letture dei timer del motore: il sensore li segue come oggi
    (le letture si annotano nel ``RenderInfo`` e i cambi arrivano con
    ``sensori_template.AnnunciDeiTimer``)."""
    if template.is_static:
        return f"c.statico({testo_costante(template.template)})"
    return f"c.modello(M.{g.jinja.funzione(template.template)})"


def _valore_sensore(g: Generatore, valore: Any) -> str:
    """Un valore della configurazione validata nel codice: i modelli (``_modello_sensore``),
    le enumerazioni (classi del dispositivo e dello stato) con il loro costruttore, il
    resto come nei trigger."""
    if isinstance(valore, Template):
        return _modello_sensore(g, valore)
    if isinstance(valore, enum.Enum):
        return f"{type(valore).__name__}({valore.value!r})"
    if isinstance(valore, dict):
        voci = (
            f"{g.valore(k, trigger=True)}: {_valore_sensore(g, v)}"
            for k, v in valore.items()
        )
        return "{" + ", ".join(voci) + "}"
    return g.valore(valore, trigger=True)


async def modulo_sensori(hass: HomeAssistant, g: Generatore) -> str:
    """``sensori.py``: ``sensori(c, ip)``, i sensori template del package senza trigger come
    (dominio, configurazione validata da Home Assistant con i modelli tradotti), nel loro
    ordine nel package."""
    # come leggi_package: il package come lo installa l'integrazione per la Master, con la
    # versione dell'integrazione nel sensore «Package Ver.» (adatta_versione): nel codice
    # quella di tabelle.py, come il modello della fase 2
    testo = adatta_versione(
        adatta_link_repository(
            rimuovi_sezioni_solo_master(
                (PACKAGE / "vmc_master.yaml").read_text("utf-8")
            )
        ),
        _SEGNAPOSTO_VERSIONE,
    )
    package = yaml.load(testo, Loader=_Caricatore)
    validata = await async_validate_config(
        hass, {"template": _sensori_template(package)}
    )
    voci: list[str] = []
    # i nomi visibili che la versione nativa cambia (genera_tabelle.NOMI_NATIVI)
    da_rinominare = {
        k for k in NOMI_NATIVI if k.split(".", 1)[0] in ("sensor", "binary_sensor")
    }
    rinominati: set[str] = set()
    gettone = RINOMINA.set(mappa_fase4())
    gettone_timer = TIMER_MOTORE.set(True)
    try:
        for sezione in validata["template"]:
            if set(sezione) - {"sensor", "binary_sensor", "button"}:
                raise NonTraducibile(f"sezione template inattesa: {sorted(sezione)}")
            for dominio in ("sensor", "binary_sensor"):
                for config in sezione.get(dominio, []):
                    oggetto = str(config.get("default_entity_id", "")).split(".", 1)[-1]
                    chiave = f"{dominio}.{oggetto.removeprefix('vmc_master_')}"
                    if chiave in da_rinominare:
                        config = {**config, "name": Template(NOMI_NATIVI[chiave], hass)}
                        rinominati.add(chiave)
                    campi = ", ".join(
                        f"{g.valore(k, trigger=True)}: {_valore_sensore(g, v)}"
                        for k, v in config.items()
                    )
                    voci.append(f"        ({dominio!r}, {{{campi}}}),\n")
    finally:
        TIMER_MOTORE.reset(gettone_timer)
        RINOMINA.reset(gettone)
    if rinominati != da_rinominare:
        raise NonTraducibile(f"nomi nativi senza sensore: {da_rinominare - rinominati}")
    versione = f"c.statico('v.{_SEGNAPOSTO_VERSIONE}')"
    if sum(v.count(versione) for v in voci) != 1:
        raise NonTraducibile("il sensore della versione non è quello atteso")
    voci = [
        v.replace(versione, "c.statico('v.' + VERSIONE_INTEGRAZIONE)") for v in voci
    ]
    # l'IP della VMC che l'integrazione scrive nel package (sostituisci_ip): il sensore «IP
    # configurato» lo mostra, nel codice è l'argomento ``ip``
    segnaposto = f"c.statico({_IP_DEL_PACKAGE!r})"
    if sum(v.count(segnaposto) for v in voci) != 1 or any(
        _IP_DEL_PACKAGE in v.replace(segnaposto, "") for v in voci
    ):
        raise NonTraducibile("l'IP del package non è solo nel sensore «IP configurato»")
    voci = [v.replace(segnaposto, "c.statico(ip)") for v in voci]
    return (
        INTESTAZIONE.format(
            titolo="Sensori template del package con i modelli tradotti (fase 4)."
        )
        + _IMPORTA_SENSORI
        + "\n"
        + "def sensori(c, ip):\n"
        + '    """(dominio, configurazione) dei sensori template della VMC di ``c`` con\n'
        + '    l\'indirizzo ``ip``, in ordine."""\n'
        + "    return [\n"
        + "".join(voci)
        + "    ]\n"
    )
