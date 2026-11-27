"""Il codice generato della fase 4: il package tradotto con tutte le opzioni della fase 4.

``motore/generato/`` resta il codice della fase 3 (aiutanti, timer, script e comandi di
shell di Home Assistant): lo usano i banchi della fase 3 e la variante ``nativa`` del
simulatore. Il motore dell'integrazione nativa (``nativa/assemblaggio.py``) usa invece
``motore/generato_fase4/``, lo stesso package tradotto con:

- la mappa dei nomi (``rinomina.da_fase_1``) per i 172 aiutanti che domani sono entità
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

Dalla b46 il motore nativo non ha le parti del package di ``escluse()``: il campo «Cambia IP
VMC» della scheda e ciò che serviva solo a lui (l'automazione che cambiava l'IP e
riavviava Home Assistant, il comando che scriveva l'IP nei file, il sensore che controllava
il campo; ``genera_tabelle.TOLTE``). L'IP si cambia solo dall'ingranaggio della VMC. Il
package si traduce lo stesso intero, nello stesso ordine, così i nomi delle funzioni
(``mNNNN``, ``kNNNN``, ``sNNNN``) restano quelli di prima; poi escono dal codice le parti
escluse, con le condizioni, le sequenze e i modelli che servono solo a loro
(``togli_escluse``), e le entità tolte escono dagli elenchi delle chiamate (la pulizia
della cronologia). Nessun'altra parte del codice le nomina; la frase della descrizione
dell'Automazione VMC Master che rimandava all'automazione tolta dice dove si cambia l'IP
(``DESCRIZIONI``).

Si rigenera con ``VMC_RIGENERA=1 pytest tests/nativa/motore/test_traduzione_fase4.py``.
"""

from __future__ import annotations

import enum
import functools
import inspect
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

import yaml
from homeassistant.components.template.config import async_validate_config
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template
from homeassistant.util import slugify

from custom_components.vmc_master.trasforma import (
    adatta_link_repository,
    adatta_versione,
    rimuovi_sezioni_solo_master,
)

from ..genera_tabelle import NOMI_NATIVI, TOLTE
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


@dataclass(frozen=True)
class Escluse:
    """Le parti del package che il motore nativo non ha (nomi della Master)."""

    automazioni: frozenset[str]
    """Gli id delle automazioni escluse."""
    comandi: frozenset[str]
    """I nomi dei comandi di shell esclusi."""
    sensori: frozenset[str]
    """I ``default_entity_id`` dei sensori template esclusi."""
    entita: frozenset[str]
    """Tutti gli entity_id tolti (``genera_tabelle.TOLTE``)."""


@functools.cache
def escluse() -> Escluse:
    """Le parti del package che il motore nativo non ha (b46), da ``genera_tabelle.TOLTE``
    (un'automazione tolta è quella con l'entity_id che le dà il suo alias)."""
    entita = frozenset(
        f"{dominio}.vmc_master_{oggetto}"
        for dominio, _, oggetto in (k.partition(".") for k in TOLTE)
    )
    ids = frozenset(
        str(a["id"])
        for a in leggi_package()[0]
        if f"automation.{slugify(a['alias'])}" in entita
    )
    if len(ids) != sum(e.startswith("automation.") for e in entita):
        raise NonTraducibile("automazioni tolte non trovate nel package")
    return Escluse(
        automazioni=ids,
        comandi=frozenset(
            e.split(".", 1)[1] for e in entita if e.startswith("shell_command.")
        ),
        sensori=frozenset(e for e in entita if e.startswith("sensor.")),
        entita=entita,
    )


def senza_entita_tolte(valore: Any, entita: frozenset[str] | None = None) -> Any:
    """La configurazione ``valore`` senza le entità tolte negli elenchi ``entity_id`` (la
    pulizia della cronologia le elenca con le altre). Un'entità tolta scritta da sola
    ferma la traduzione: la parte che la usa andrebbe esclusa."""
    if entita is None:
        entita = escluse().entita
    if isinstance(valore, Mapping):
        uscita = {}
        for chiave, voce in valore.items():
            if chiave == "entity_id" and isinstance(voce, list):
                voce = [e for e in voce if e not in entita]
            elif chiave == "entity_id" and voce in entita:
                raise NonTraducibile(f"entità tolta usata da sola: {voce}")
            uscita[chiave] = senza_entita_tolte(voce, entita)
        return uscita
    if isinstance(valore, list):
        return [senza_entita_tolte(v, entita) for v in valore]
    return valore


# Le frasi delle descrizioni che rimandano a una parte tolta (b46), ognuna in una sola
# descrizione, e la frase della versione nativa.
DESCRIZIONI = {
    (
        "- Il Cambio dell'IP non è in questa automazione: lo esegue subito l'automazione «VMC"
        " Master - Cambio IP VMC (Riavvio di H.A.)» del Package."
    ): (
        "- Il Cambio dell'IP non è in questa automazione: si fa da Impostazioni → Dispositivi"
        " e servizi → VMC Master → ⚙️ → Cambia l'IP della VMC."
    ),
}


def _descrizione_nativa(automazione: dict[str, Any], trovate: list[str]) -> dict[str, Any]:
    """L'automazione con le frasi di ``DESCRIZIONI`` della versione nativa (in
    ``trovate`` quelle cambiate)."""
    descrizione = automazione.get("description")
    if not isinstance(descrizione, str):
        return automazione
    for prima, dopo in DESCRIZIONI.items():
        if prima in descrizione:
            trovate.append(prima)
            descrizione = descrizione.replace(prima, dopo)
    return {**automazione, "description": descrizione}


def package_nativo() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Automazioni e script del package (``leggi_package``) come li traduce la fase 4: le
    entità tolte escono dagli elenchi delle parti che restano e le descrizioni non
    rimandano alle parti tolte (le automazioni escluse restano come sono: escono dal
    codice dopo, ``togli_escluse``)."""
    automazioni, script = leggi_package()
    trovate: list[str] = []
    native = [
        a
        if str(a.get("id")) in escluse().automazioni
        else _descrizione_nativa(senza_entita_tolte(a), trovate)
        for a in automazioni
    ]
    if sorted(trovate) != sorted(DESCRIZIONI):
        raise NonTraducibile(f"frasi delle descrizioni trovate: {trovate}")
    return native, {chiave: senza_entita_tolte(s) for chiave, s in script.items()}


_NOME_FUNZIONE = re.compile(r"\b[ksm]\d{4}\b")


def _usati(testi: Iterable[str], blocchi: Mapping[str, str]) -> set[str]:
    """I nomi delle funzioni (``kNNNN``, ``sNNNN``, ``mNNNN``) che usano i ``testi``,
    con quelli che usano le condizioni e le sequenze usate (``blocchi``: nome -> codice;
    un modello non usa altre funzioni)."""
    visti: set[str] = set()
    da_vedere = [n for testo in testi for n in _NOME_FUNZIONE.findall(testo)]
    while da_vedere:
        if (nome := da_vedere.pop()) in visti:
            continue
        visti.add(nome)
        da_vedere += _NOME_FUNZIONE.findall(blocchi.get(nome, ""))
    return visti


def togli_escluse(
    g: Generatore, motore: str, sensori: list[str], sensori_esclusi: list[str]
) -> tuple[str, frozenset[str]]:
    """``motore`` senza le automazioni e i comandi di ``escluse()`` (una riga ciascuno in
    ``crea`` e in ``comandi``) e i nomi delle condizioni, delle sequenze e dei modelli che
    servono solo alle parti escluse (con i sensori esclusi: ``sensori_esclusi``), da
    togliere dal codice. Quello che resta (``motore``, ``sensori``) non deve nominare
    nessuna entità tolta."""
    prima, separatore, crea = motore.partition("\n\n\ndef crea(c):\n")
    righe = crea.splitlines(keepends=True)
    segni = [f"id=c.N({a!r})" for a in escluse().automazioni] + [
        f"Comando(nome=c.N({c!r})" for c in escluse().comandi
    ]
    righe_escluse = []
    for segno in segni:
        trovate = [r for r in righe if segno in r]
        if len(trovate) != 1:
            raise NonTraducibile(f"{segno}: {len(trovate)} righe in crea/comandi")
        righe_escluse += trovate
        righe.remove(trovate[0])
    crea = "".join(righe)
    blocchi = {
        re.match(r"(?:async )?def ([ks]\d{4})\(", b).group(1): b
        for b in g.condizioni + g.sequenze
    }
    tenuti = _usati([crea, *sensori], blocchi)
    tolti = frozenset(_usati(righe_escluse + sensori_esclusi, blocchi) - tenuti)
    restano = [crea, *sensori] + [blocchi[n] for n in tenuti if n in blocchi]
    restano += [
        codice
        for codice in g.jinja.codice
        if re.match(r"def (m\d{4})\(", codice).group(1) in tenuti
    ]
    for entita in escluse().entita:
        # anche con il dominio di domani (la mappa dei nomi)
        oggetto = entita.split(".", 1)[1]
        if any(oggetto in testo for testo in restano):
            raise NonTraducibile(f"{entita}: ancora nel codice della fase 4")
    return prima + separatore + crea, tolti


def mappa_fase4() -> Rinomina:
    """La mappa dei nomi della fase 4: 172 aiutanti -> entità native (nessun servizio)."""
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
    automazioni, script = package_nativo()
    jinja, g, _, motore = await traduzione(
        hass,
        automazioni,
        script,
        rinomina=mappa_fase4(),
        comandi=leggi_comandi(),
        timer_motore=True,
        **_opzioni_interni(),
    )
    sensori, voci, voci_escluse = await modulo_sensori(hass, g)
    motore, tolti = togli_escluse(g, motore, voci, voci_escluse)
    return {
        "__init__.py": '"""Codice generato dal package (fase 4: entità native)."""\n',
        **_moduli_modelli(jinja, tolti),
        **_moduli_motore(g, motore, tolti),
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


async def modulo_sensori(
    hass: HomeAssistant, g: Generatore
) -> tuple[str, list[str], list[str]]:
    """``sensori.py``: ``sensori(c, ip)``, i sensori template del package senza trigger come
    (dominio, configurazione validata da Home Assistant con i modelli tradotti), nel loro
    ordine nel package; con le voci del modulo e quelle dei sensori esclusi
    (``escluse().sensori``: tradotte come le altre, così i modelli dopo di loro tengono il
    loro numero, ma fuori dal modulo)."""
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
    voci_escluse: list[str] = []
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
                    voce = f"        ({dominio!r}, {{{campi}}}),\n"
                    if config.get("default_entity_id") in escluse().sensori:
                        voci_escluse.append(voce)
                    else:
                        voci.append(voce)
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
    if len(voci_escluse) != len(escluse().sensori):
        raise NonTraducibile("sensori esclusi non trovati nel package")
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
        + "    ]\n",
        voci,
        voci_escluse,
    )
