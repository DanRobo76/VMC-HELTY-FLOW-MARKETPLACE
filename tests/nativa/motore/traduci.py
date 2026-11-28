"""Traduttore del motore logico del package in Python (fase 3).

Legge le automazioni e gli script del package (dopo ``rimuovi_sezioni_solo_master``),
li fa validare a Home Assistant (così ogni valore ha già la forma che usa Home Assistant:
liste di entity_id, durate, Template al posto dei testi con Jinja...) e scrive due moduli:

- ``generato/modelli.py``: una funzione per ogni modello Jinja distinto
  (``traduci_jinja.py``);
- ``generato/motore.py``: le condizioni (``kNNNN``), le sequenze di azioni (``sNNNN``) e
  ``crea(c)``, che restituisce automazioni e script per la VMC del contesto ``c``.

Nel package i due moduli sono divisi in moduli più piccoli (``traduci``): ``modelli.py`` e
``motore.py`` importano le loro parti.

``generato/`` è in ``tests/nativa/motore/``, fuori dall'integrazione: lo usano solo le prove
e gli strumenti, e importa i moduli del motore con il loro nome intero (``MOTORE``).

Il codice generato non si modifica a mano: si rigenera con
``VMC_RIGENERA=1 pytest tests/nativa/motore/test_traduzione.py``.
"""

from __future__ import annotations

import base64
import re
import zlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import time, timedelta
from pathlib import Path
from typing import Any

import yaml
from homeassistant.components.automation.config import (
    async_validate_config_item as valida_automazione,
)
from homeassistant.components.script.config import (
    async_validate_config_item as valida_script,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template, TemplateEnvironment

from custom_components.vmc_master.const import NOME_MASTER
from custom_components.vmc_master.installatore import automazione_come_package
from custom_components.vmc_master.nativa.motore import jinja as J
from custom_components.vmc_master.nativa.motore.definizioni import (
    COMANDO_NESSUNO,
    COMANDO_NOME,
    COMANDO_VMC,
)
from custom_components.vmc_master.nativa.motore.interni import AGGANCIO
from custom_components.vmc_master.nativa.motore.memoria_interna import MemoriaInterna
from custom_components.vmc_master.nativa.motore.timer import (
    DOMINIO_SERVIZI,
    EVENTI_TIMER,
    SERVIZI,
    TRIGGER,
)
from custom_components.vmc_master.trasforma import (
    adatta_link_repository,
    rimuovi_sezioni_solo_master,
)

from .traduci_jinja import (
    GLOBALI,
    RINOMINA,
    TIMER_MOTORE,
    NonTraducibile,
    Traduttore,
    testo_costante,
)

RADICE = Path(__file__).resolve().parents[3]
PACKAGE = RADICE / "custom_components/vmc_master/package"
GENERATO = RADICE / "tests/nativa/motore/generato"
MOTORE = "custom_components.vmc_master.nativa.motore"
"""Da dove il codice generato importa i moduli del motore (``jinja``, ``condizioni``,
``definizioni``, ``esecuzione``): con il nome intero, perché ``GENERATO`` e i moduli delle
prove sono fuori dal motore. Solo il codice della fase 4, che è dentro il motore
(``generato_fase4/``), li importa con ``..`` (``traduci_fase4``)."""

INTESTAZIONE = '''"""{titolo}

Generato da tests/nativa/motore/traduci.py dal package della b42: non modificare a mano.
"""

# ruff: noqa
# fmt: off
'''

# Variabili sempre presenti in un'esecuzione.
VARIABILI_FISSE = {"trigger", "this", "context", "repeat", "wait"}


class _Caricatore(yaml.SafeLoader):
    """YAML del package: i tag di Home Assistant (!secret...) restano il loro valore."""


def _qualsiasi_tag(caricatore: yaml.SafeLoader, _suffisso: str, nodo: yaml.Node) -> Any:
    if isinstance(nodo, yaml.ScalarNode):
        return caricatore.construct_scalar(nodo)
    if isinstance(nodo, yaml.SequenceNode):
        return caricatore.construct_sequence(nodo, deep=True)
    return caricatore.construct_mapping(nodo, deep=True)  # type: ignore[arg-type]


_Caricatore.add_multi_constructor("!", _qualsiasi_tag)


def leggi_package() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Automazioni e script del package, come li installa l'integrazione per la Master
    (``installatore.genera_file``), nell'ordine in cui Home Assistant li carica:
    ``packages: !include_dir_named`` legge i file della cartella in ordine di nome, prima
    ``vmc_master.yaml`` (le 13 automazioni e gli script) e poi
    ``vmc_master_automazione.yaml`` (l'Automazione VMC Master, ultima). Senza le sezioni
    «solo master», con i link del repository dell'integrazione e, per l'automazione
    principale, l'id che le dà ``automazione_come_package`` (``automazione_vmc_master``:
    per le altre VMC ``c.N`` lo rinomina come l'integrazione). L'IP e la versione che
    l'integrazione scrive nei file non toccano automazioni e script (lo controlla
    ``test_piu_vmc.py``)."""
    principale = yaml.load(
        automazione_come_package(
            adatta_link_repository(
                rimuovi_sezioni_solo_master(
                    (PACKAGE / "vmc_master_automazione.txt").read_text("utf-8")
                )
            ),
            NOME_MASTER,
        ),
        Loader=_Caricatore,
    )["automation"][0]
    package = yaml.load(
        adatta_link_repository(
            rimuovi_sezioni_solo_master(
                (PACKAGE / "vmc_master.yaml").read_text("utf-8")
            )
        ),
        Loader=_Caricatore,
    )
    return [*package.get("automation", []), principale], package.get("script", {})


def leggi_comandi() -> dict[str, str]:
    """I comandi di shell del package (nome -> riga di comando), come li installa
    l'integrazione per la Master, senza le sezioni «solo master»: servono al traduttore
    con gli script e i comandi dentro il motore (fase 4)."""
    package = yaml.load(
        rimuovi_sezioni_solo_master((PACKAGE / "vmc_master.yaml").read_text("utf-8")),
        Loader=_Caricatore,
    )
    return dict(package.get("shell_command", {}))


@dataclass
class Generatore:
    """Scrive il modulo del motore dalle configurazioni validate."""

    jinja: Traduttore
    condizioni: list[str] = field(default_factory=list)
    sequenze: list[str] = field(default_factory=list)
    variabili: set[str] = field(default_factory=set)
    _cache_condizioni: dict[str, str] = field(default_factory=dict)
    # fase 4, script e comandi dentro il motore: i comandi di shell del package (nome ->
    # riga di comando) e gli script del package; None: script e shell_command di Home
    # Assistant (il codice di sempre)
    comandi: Mapping[str, str] | None = None
    script: frozenset[str] = frozenset()
    # i trigger segnati per l'aggancio dei comandi
    agganci: int = 0
    # fase 4, memoria interna: entity_id (della Master) dei valori interni, che il motore
    # tiene nella memoria interna; vuoto senza memoria interna
    valori_interni: frozenset[str] = frozenset()

    # --- valori ---------------------------------------------------------------------------

    def modello(self, template: Template) -> str:
        return f"M.{self.jinja.funzione(template.template)}"

    def _seguito(self, template: Template) -> str:
        """Un modello che Home Assistant segue (trigger, attese): non può leggere i timer
        del motore, che Home Assistant non vede cambiare."""
        modello = self.modello(template)
        if modello.removeprefix("M.") in self.jinja.instradati:
            raise NonTraducibile(
                f"lettura di un timer del motore in un modello seguito: {template.template!r}"
            )
        return modello

    def valore(self, valore: Any, *, trigger: bool = False) -> str:
        """Un valore validato nel codice (dentro una funzione con ``c``).

        Nei trigger i Template restano Template di Home Assistant (li usano le piattaforme
        dei trigger): ``c.statico`` per un testo senza Jinja, ``c.modello`` per un modello
        tradotto. Nelle azioni un modello è il segnaposto ``Modello``.
        """
        if isinstance(valore, Template):
            if valore.is_static:
                if not trigger:
                    raise NonTraducibile(f"Template statico {valore.template!r}")
                return f"c.statico({testo_costante(valore.template)})"
            if trigger:
                return f"c.modello({self._seguito(valore)})"
            return f"Modello({self.modello(valore)})"
        if isinstance(valore, str):
            return testo_costante(valore)
        if (
            isinstance(valore, bool)
            or valore is None
            or isinstance(valore, (int, float))
        ):
            return repr(valore)
        if isinstance(valore, timedelta):
            return (
                f"timedelta(days={valore.days}, seconds={valore.seconds}, "
                f"microseconds={valore.microseconds})"
            )
        if isinstance(valore, time):
            if valore.tzinfo is not None:
                raise NonTraducibile(f"ora con fuso {valore!r}")
            return f"time({valore.hour}, {valore.minute}, {valore.second}, {valore.microsecond})"
        if isinstance(valore, list):
            return (
                "[" + ", ".join(self.valore(v, trigger=trigger) for v in valore) + "]"
            )
        if isinstance(valore, tuple):
            return (
                "("
                + "".join(self.valore(v, trigger=trigger) + ", " for v in valore)
                + ")"
            )
        if isinstance(valore, Mapping):
            voci = (
                f"{self.valore(k, trigger=trigger)}: {self.valore(v, trigger=trigger)}"
                for k, v in valore.items()
            )
            return "{" + ", ".join(voci) + "}"
        raise NonTraducibile(f"valore {type(valore).__name__}: {valore!r}")

    # --- condizioni -----------------------------------------------------------------------

    def condizione(self, config: Mapping[str, Any]) -> str:
        """Il nome della funzione ``k(c, V)`` della condizione validata ``config``."""
        if config.get("enabled", True) is not True:
            raise NonTraducibile(f"condizione con enabled {config.get('enabled')!r}")
        tipo = config["condition"]
        if tipo == "template":
            corpo = f"C.modello(c, {self.modello(config['value_template'])}, V)"
        elif tipo == "trigger":
            corpo = f"C.trigger(V, {self.valore(list(config['id']))})"
        elif tipo in ("and", "or", "not"):
            nomi = [self.condizione(sotto) for sotto in config["conditions"]]
            funzione = {"and": "C.e", "or": "C.o", "not": "C.non"}[tipo]
            corpo = f"{funzione}(c, V, ({''.join(n + ', ' for n in nomi)}))"
        elif tipo == "state":
            if TIMER_MOTORE.get():
                _nessun_timer(config.get("entity_id", []), "condizione state")
            stati = config.get("state", [])
            if not isinstance(stati, list):
                stati = [stati]
            extra = ""
            if config.get("for") is not None:
                extra += f", per={self.valore(config['for'])}"
            if config.get("attribute") is not None:
                extra += f", attributo={self.valore(config['attribute'])}"
            if config.get("match", "all") == "any":
                extra += ", qualsiasi=True"
            corpo = (
                f"C.stato(c, V, {self.valore(list(config.get('entity_id', [])))}, "
                f"{self.valore(stati)}{extra})"
            )
        else:
            raise NonTraducibile(f"condizione {tipo}")
        if corpo in self._cache_condizioni:
            return self._cache_condizioni[corpo]
        nome = f"k{len(self._cache_condizioni) + 1:04d}"
        self._cache_condizioni[corpo] = nome
        self.condizioni.append(f"def {nome}(c, V):\n    return {corpo}")
        return nome

    def condizioni_tupla(self, configs: list[Mapping[str, Any]]) -> str:
        return "(" + "".join(self.condizione(c) + ", " for c in configs) + ")"

    # --- azioni ---------------------------------------------------------------------------

    def sequenza(self, azioni: list[Mapping[str, Any]], dove: str) -> str:
        """Il nome della funzione ``async def s(r)`` della sequenza ``azioni``."""
        nome = f"s{len(self.sequenze) + 1:04d}"
        self.sequenze.append("")  # posto riservato: le sequenze annidate vengono dopo
        posto = len(self.sequenze) - 1
        righe = [f"async def {nome}(r):", f"    # {dove}", "    c, V = r.c, r.V"]
        for indice, azione in enumerate(azioni):
            righe += [
                "    " + riga for riga in self.azione(azione, f"{dove} > {indice}")
            ]
        self.sequenze[posto] = "\n".join(righe)
        return nome

    def azione(self, azione: Mapping[str, Any], dove: str) -> list[str]:
        """Le righe Python di un'azione validata."""
        azione = dict(azione)
        if azione.pop("enabled", True) is not True:
            raise NonTraducibile(f"azione con enabled: {dove}")
        alias = azione.pop("alias", None)
        a_alias = f", alias={testo_costante(alias)}" if alias is not None else ""
        continua = azione.pop("continue_on_error", False)
        if continua and "action" not in azione:
            raise NonTraducibile(f"continue_on_error fuori da una chiamata: {dove}")
        azione.pop("metadata", None)
        if "delay" in azione:
            return [f"await r.pausa({self.valore(azione['delay'])}{a_alias})"]
        if "wait_template" in azione:
            timeout = self.valore(azione["timeout"]) if "timeout" in azione else "None"
            extra = ""
            if azione.get("continue_on_timeout", True) is not True:
                extra = ", continua=False"
            modello = self._seguito(azione["wait_template"])
            return [f"await r.attendi({modello}, timeout={timeout}{extra}{a_alias})"]
        if "condition" in azione:
            nome = self.condizione(azione)
            descrizione = (
                testo_costante(alias)
                if alias is not None
                else repr(azione["condition"])
            )
            return [f"if not r.passo_condizione({nome}, {descrizione}):", "    return"]
        if "repeat" in azione:
            ripeti = azione["repeat"]
            corpo = self.sequenza(ripeti["sequence"], f"{dove} repeat")
            righe = ["r.verifica()"]
            if "until" in ripeti:
                righe.append(
                    f"await r.ripeti_finche({corpo}, {self.condizioni_tupla(ripeti['until'])})"
                )
            elif "while" in ripeti:
                righe.append(
                    f"await r.ripeti_mentre({corpo}, {self.condizioni_tupla(ripeti['while'])})"
                )
            elif "count" in ripeti:
                righe.append(
                    f"await r.ripeti_volte({corpo}, {self.valore(ripeti['count'])})"
                )
            elif "for_each" in ripeti:
                righe.append(
                    f"await r.ripeti_per_ogni({corpo}, {self.valore(ripeti['for_each'])})"
                )
            else:
                raise NonTraducibile(f"repeat {sorted(ripeti)}")
            return righe
        if "choose" in azione:
            righe = ["r.verifica()"]
            for indice, scelta in enumerate(azione["choose"]):
                corpo = self.sequenza(scelta["sequence"], f"{dove} choose {indice}")
                parola = "if" if indice == 0 else "elif"
                righe += [
                    f"{parola} r.prova({self.condizioni_tupla(scelta['conditions'])}):",
                    f"    await r.sotto({corpo})",
                ]
            if azione.get("default") is not None:
                corpo = self.sequenza(azione["default"], f"{dove} default")
                righe += ["else:", f"    await r.sotto({corpo})"]
            return righe
        if "if" in azione:
            allora = self.sequenza(azione["then"], f"{dove} then")
            righe = [
                "r.verifica()",
                f"if r.prova({self.condizioni_tupla(azione['if'])}):",
                f"    await r.sotto({allora})",
            ]
            if azione.get("else") is not None:
                altrimenti = self.sequenza(azione["else"], f"{dove} else")
                righe += ["else:", f"    await r.sotto({altrimenti})"]
            return righe
        if "variables" in azione:
            valori = azione["variables"].as_dict()
            self.variabili.update(valori)
            return [f"r.variabili({self.valore(valori)}{a_alias})"]
        if "action" in azione:
            return [self._chiamata(azione, continua, a_alias)]
        if "stop" in azione:
            if "response_variable" in azione:
                raise NonTraducibile(f"stop con response_variable: {dove}")
            eccezione = "Annulla" if azione.get("error") else "Ferma"
            return [
                "r.verifica()",
                f"raise {eccezione}({testo_costante(azione['stop'])})",
            ]
        if "sequence" in azione:
            corpo = self.sequenza(azione["sequence"], f"{dove} sequence")
            return ["r.verifica()", f"await r.sotto({corpo})"]
        raise NonTraducibile(f"azione {sorted(azione)}: {dove}")

    def _chiamata(self, azione: dict[str, Any], continua: bool, a_alias: str) -> str:
        if self.comandi is not None:
            self._controlla_interni(azione)
        argomenti_originali = dict(azione)
        nome = azione.pop("action")
        if isinstance(nome, str) and (mappa := RINOMINA.get()) is not None:
            nome = mappa.servizio(nome)
        if TIMER_MOTORE.get():
            nome = _servizio_timer(nome)
        argomenti = [self.valore(nome)]
        if "data_template" in azione:
            raise NonTraducibile("data_template")
        if "data" in azione:
            dati = azione.pop("data")
            argomenti.append(self.valore(dati))
            if isinstance(nome, str) and isinstance(dati, Mapping):
                if nome.startswith("script.") and nome != "script.turn_on":
                    self.variabili.update(k for k in dati if isinstance(k, str))
                elif nome == "script.turn_on" and isinstance(
                    dati.get("variables"), Mapping
                ):
                    self.variabili.update(dati["variables"])
        else:
            argomenti.append("None")
        if "target" in azione:
            argomenti.append(self.valore(azione.pop("target")))
        else:
            argomenti.append("None")
        if "entity_id" in azione:
            argomenti.append(f"entita={self.valore(azione.pop('entity_id'))}")
        if continua:
            argomenti.append("continua_se_errore=True")
        if "response_variable" in azione:
            argomenti.append(f"risposta={azione.pop('response_variable')!r}")
            self.variabili.add(argomenti[-1].split("=", 1)[1].strip("'"))
        if azione:
            raise NonTraducibile(f"chiamata con {sorted(azione)}")
        if self.valori_interni:
            self._verifica_valori_interni(nome, argomenti_originali)
        while argomenti[-1] == "None":
            argomenti.pop()
        return f"await r.servizio({', '.join(argomenti)}{a_alias})"

    def _verifica_valori_interni(self, nome: Any, azione: Mapping[str, Any]) -> None:
        """Con la memoria interna, una chiamata con un valore interno scritto nel
        bersaglio deve essere una di quelle che il motore sa fare: un servizio degli
        aiutanti sulla memoria (``MemoriaInterna.gestisce``) con soli valori interni,
        uno degli interruttori anche con altre entità, l'aggiornamento delle entità (i
        valori interni si tolgono) o la pulizia della cronologia (resta com'è). I
        bersagli scritti con un modello si controllano durante l'esecuzione."""
        costanti: list[str] = []
        for contenitore in (azione.get("target"), azione.get("data")):
            if isinstance(contenitore, Mapping):
                costanti += _entita_costanti(contenitore.get("entity_id"))
        costanti += _entita_costanti(azione.get("entity_id"))
        if not (interni := [e for e in costanti if e in self.valori_interni]):
            return
        if not isinstance(nome, str):
            raise NonTraducibile(f"servizio scritto con un modello su {interni}")
        dominio, _, servizio = nome.partition(".")
        if MemoriaInterna.gestisce(dominio, servizio):
            if len(interni) == len(costanti) or dominio == "input_boolean":
                return
            raise NonTraducibile(f"{nome} su valori interni e altre entità: {costanti}")
        if nome in ("homeassistant.update_entity", "recorder.purge_entities"):
            if nome == "homeassistant.update_entity" and len(interni) == len(costanti):
                raise NonTraducibile(f"{nome} solo su valori interni: {costanti}")
            return
        raise NonTraducibile(f"{nome} su valori interni: {interni}")

    def _controlla_interni(self, azione: Mapping[str, Any]) -> None:
        """Con script e comandi dentro il motore: ogni ``script.*`` e
        ``shell_command.*`` dal nome costante è uno script o un comando del package (i
        nomi resi da un modello li sceglie il motore mentre gira) e nessuno chiede una
        risposta."""
        nome = azione["action"]
        if not isinstance(nome, str):
            return
        dominio, _, servizio = nome.partition(".")
        if dominio not in ("script", "shell_command"):
            return
        if "response_variable" in azione:
            raise NonTraducibile(f"{nome} con response_variable")
        if dominio == "shell_command":
            if servizio not in (self.comandi or {}):
                raise NonTraducibile(f"comando sconosciuto: {nome}")
            return
        if servizio not in ("turn_on", "turn_off", "toggle"):
            if servizio not in self.script:
                raise NonTraducibile(f"script sconosciuto: {nome}")
            return
        entita = (azione.get("target") or {}).get("entity_id")
        if (
            entita is None
            or "entity_id" in azione
            or "entity_id" in (azione.get("data") or {})
        ):
            raise NonTraducibile(f"{nome} senza entity_id costante nel bersaglio")
        voluti = {f"script.{chiave}" for chiave in self.script}
        if not isinstance(entita, list) or not all(
            isinstance(e, str) and e in voluti for e in entita
        ):
            raise NonTraducibile(f"{nome}: non solo script del package: {entita}")

    # --- trigger --------------------------------------------------------------------------

    def trigger(self, trigger: Mapping[str, Any]) -> str:
        if trigger.get("variables"):
            raise NonTraducibile(f"trigger con variables: {trigger}")
        if TIMER_MOTORE.get():
            trigger = _trigger_timer(trigger)
        voce = dict(trigger)
        if self.comandi is not None and voce.get("platform") in ("event", TRIGGER):
            self._aggancio(voce)
        return self.valore(voce, trigger=True)

    def _aggancio(self, voce: dict[str, Any]) -> None:
        """Con i comandi dentro il motore un trigger sulle loro chiamate (``event``
        ``call_service`` con ``domain: shell_command``) si segna per l'aggancio diretto
        (``interni.AGGANCIO``): Home Assistant non lo aggancia più (``enabled: False``),
        lo aggancia il motore. Gli eventi delle chiamate degli script e i loro
        ``script_started`` non ci sono più: un trigger su di loro non si traduce."""
        tipi = [_testo(t) for t in voce["event_type"]]
        if "script_started" in tipi:
            raise NonTraducibile(f"trigger su script_started: {voce}")
        if "call_service" not in tipi:
            return
        dati = {k: _testo(v) for k, v in (voce.get("event_data") or {}).items()}
        if (
            tipi != ["call_service"]
            or dati.get("domain") != "shell_command"
            or dati.get("service") not in (self.comandi or {})
            or set(dati) != {"domain", "service"}
            or "context" in voce
            or voce.get("enabled", True) is not True
        ):
            raise NonTraducibile(f"trigger su call_service non agganciabile: {voce}")
        voce["enabled"] = False
        voce[AGGANCIO] = True
        self.agganci += 1

    # --- comandi --------------------------------------------------------------------------

    def comandi_motore(self) -> str:
        """La funzione ``comandi(c)``: i comandi di shell del package come ``Comando``."""
        voci = []
        for nome, riga in (self.comandi or {}).items():
            tipo, testo, argomenti = _comando(riga)
            parti = [f"nome={self.valore(nome)}", f"tipo={tipo!r}"]
            if testo:
                parti.append(f"testo={testo!r}")
            if argomenti is not None:
                parti.append(f"argomenti=Modello(M.{self.jinja.funzione(argomenti)})")
            voci.append("Comando(" + ", ".join(parti) + ")")
        return (
            "\n\n\ndef comandi(c):\n"
            + '    """I comandi di shell per la VMC del contesto ``c``."""\n'
            + "    return [\n"
            + "".join(f"        {voce},\n" for voce in voci)
            + "    ]\n"
        )


# --- i timer del motore (timer_motore) ------------------------------------------------------


def _nessun_timer(entita: Any, dove: str) -> None:
    """Un trigger o una condizione che legge gli stati: nessun timer (i timer del motore
    non sono nella macchina degli stati)."""
    if isinstance(entita, str):
        entita = [entita]
    for voce in entita or []:
        if isinstance(voce, str) and voce.lower().startswith("timer."):
            raise NonTraducibile(f"{dove} su {voce} con i timer del motore")


def _servizio_timer(nome: Any) -> Any:
    """Il servizio di un timer va ai timer del motore (``motore_timer.<servizio>``). Un
    nome composto da un modello resta com'è: se diventa ``timer.<servizio>`` mentre il
    motore gira, ``Contesto.chiama_servizio`` lo manda ai timer del motore."""
    if isinstance(nome, Template) and nome.is_static:
        nome = nome.template
    if not isinstance(nome, str):
        return nome
    dominio, _, servizio = nome.partition(".")
    if dominio.lower() != "timer":
        return nome
    if servizio not in SERVIZI:
        raise NonTraducibile(f"servizio {nome} con i timer del motore")
    return f"{DOMINIO_SERVIZI}.{servizio}"


def _trigger_timer(trigger: Mapping[str, Any]) -> Mapping[str, Any]:
    """Un trigger con i timer del motore: un trigger evento che può sentire un evento dei
    timer diventa ``TRIGGER`` (lo stesso trigger evento di Home Assistant, che sente anche
    il bus dei timer del motore); un trigger che legge lo stato di un timer, o che
    aspetta la chiamata di un servizio dei timer (``call_service``), non si traduce."""
    piattaforma = trigger.get("platform")
    if piattaforma != "event":
        _nessun_timer(trigger.get("entity_id", []), f"trigger {piattaforma}")
        return trigger
    tipi = trigger.get("event_type", [])
    testi = [t.template if isinstance(t, Template) else t for t in tipi]
    dinamici = [t for t in tipi if isinstance(t, Template) and not t.is_static]
    if "call_service" in testi or dinamici:
        dati = trigger.get("event_data") or {}
        dominio = dati.get("domain")
        if isinstance(dominio, Template) and dominio.is_static:
            dominio = dominio.template
        if not isinstance(dominio, str) or dominio.lower() == "timer":
            raise NonTraducibile(
                f"trigger call_service senza un dominio diverso da timer: {trigger}"
            )
    if dinamici or EVENTI_TIMER.intersection(testi):
        return {**trigger, "platform": TRIGGER}
    return trigger


def _testo(valore: Any) -> Any:
    """Il testo di un Template statico (o il valore com'è)."""
    return valore.template if isinstance(valore, Template) else valore


# Le righe dei comandi di shell del package (dopo l'installazione: l'IP e il nome della
# VMC al loro posto).
_COMANDO_VMC = re.compile(r"printf '(VMWH\d{7})\\n' \| timeout 5 nc -w 3 \S+ 5001")
_COMANDO_SH = re.compile(
    r"bash /config/packages/vmc_helty_flow/(\w+)/vmc_\1_script_cambio_(nome|ip)\.sh(.*)"
)
_COMANDO_RITORNI = re.compile(
    r"find /config/packages/vmc_helty_flow/\w+ -type f -name \"\*\.sh\" "
    r"-exec sed -i 's/\\r\$//' \{\} \\;"
)


def _comando(riga: str) -> tuple[str, str, str | None]:
    """Tipo, testo per la VMC e modello degli argomenti di un comando di shell.

    Per i file .sh gli argomenti sono il resto della riga dopo il percorso del file:
    ``shell_command`` rende il modello di tutto il resto della riga e lo divide con
    ``shlex.split`` (il primo pezzo è il file); dividere solo la parte dopo il file dà
    gli stessi argomenti."""
    if trovato := _COMANDO_VMC.fullmatch(riga):
        return COMANDO_VMC, trovato.group(1), None
    if trovato := _COMANDO_SH.fullmatch(riga):
        # il file che scriveva l'IP nei file del package (b46): per Home Assistant nessun
        # effetto, come il «find ... sed»; il motore nativo non lo ha
        # (``traduci_fase4.escluse``), il package lo chiama ancora
        tipo = COMANDO_NOME if trovato.group(2) == "nome" else COMANDO_NESSUNO
        return tipo, "", trovato.group(3)
    if _COMANDO_RITORNI.fullmatch(riga):
        return COMANDO_NESSUNO, "", None
    raise NonTraducibile(f"comando di shell sconosciuto: {riga!r}")


async def traduci(
    hass: HomeAssistant,
    *,
    comandi: bool = False,
    interni: Iterable[str] | None = None,
    timer_motore: bool = False,
) -> dict[str, str]:
    """I moduli generati dal package (nome file -> testo).

    Lo stesso codice di ``traduci_configurazione``, diviso in moduli di al più
    ``LIMITE_MODULO`` byte (``modelli.py`` e ``motore.py`` restano quelli da importare) e
    con i testi dei modelli compressi (vedi ``_moduli_modelli``). Fase 4, tutto spento
    se non lo si chiede (vedi ``traduzione``): ``comandi`` script e comandi di shell
    dentro il motore (con ``leggi_comandi``), ``interni`` le chiavi dei valori interni,
    ``timer_motore`` i timer del motore.
    """
    automazioni, script = leggi_package()
    jinja, g, _, motore = await traduzione(
        hass,
        automazioni,
        script,
        comandi=leggi_comandi() if comandi else None,
        interni=interni,
        timer_motore=timer_motore,
    )
    return {
        "__init__.py": '"""Codice generato dal package (fase 3)."""\n',
        **_moduli_modelli(jinja),
        **_moduli_motore(g, motore),
    }


# Byte di codice al massimo in un modulo generato del package. Python compila un modulo
# intero in memoria (albero sintattico, simboli, istruzioni: circa 30 byte per byte di
# codice) e quasi tutta la memoria liberata dopo resta al processo: con un modulo da 3 MB
# Home Assistant, al primo avvio senza .pyc, arriva a 145 MB in più e ne tiene 113 fino
# al riavvio. Con moduli piccoli il picco è quello del modulo più grande.
LIMITE_MODULO = 200_000

_INIZIO_SORGENTI = "_SORGENTI = (\n"
_INIZIO_INTERNI = (
    "# i valori interni (fase 4): nella memoria interna del motore\nINTERNI = (\n"
)


def _da(importa_da: str, modulo: str) -> str:
    """Il modulo ``modulo`` del motore come si scrive dopo «from» (``importa_da``: il nome
    intero del motore, ``MOTORE``, o ``..``)."""
    return importa_da + modulo if importa_da.endswith(".") else f"{importa_da}.{modulo}"


def _importa_motore(
    comandi: bool, nome_modelli: str = "modelli", importa_da: str = MOTORE
) -> str:
    """Gli import di un modulo del motore generato (con ``Comando`` se ci sono i
    comandi): i moduli del motore da ``importa_da``, i modelli da ``nome_modelli``."""
    definizioni = "Automazione, Comando, Script" if comandi else "Automazione, Script"
    return (
        "\nfrom datetime import time, timedelta\n\n"
        f"from {importa_da} import condizioni as C\n"
        f"from {_da(importa_da, 'definizioni')} import {definizioni}\n"
        f"from {_da(importa_da, 'esecuzione')} import Annulla, Ferma, Modello\n"
        f"from . import {nome_modelli} as M\n"
    )


def _in_parti(blocchi: list[str]) -> list[list[str]]:
    """I blocchi in ordine, in parti di al più ``LIMITE_MODULO`` byte (un blocco più
    grande resta da solo)."""
    parti: list[list[str]] = []
    dimensione = LIMITE_MODULO
    for blocco in blocchi:
        if dimensione + len(blocco) > LIMITE_MODULO:
            parti.append([])
            dimensione = 0
        parti[-1].append(blocco)
        dimensione += len(blocco) + 3
    return parti


def _moduli_modelli(
    jinja: Traduttore,
    tolti: frozenset[str] = frozenset(),
    *,
    importa_da: str = MOTORE,
) -> dict[str, str]:
    """``modelli_NN.py`` con le funzioni dei modelli e ``modelli.py``, che le importa tutte
    e dà a ognuna il suo ``sorgente``.

    I testi dei modelli (``mNNNN.sorgente``, per i messaggi d'errore e come testo dei
    ``Template``) sono 1,3 MB, ma si ripetono molto: in ``modelli.py`` stanno compressi
    (zlib e base64, circa 60 kB) e si scompattano una volta all'import.

    ``tolti`` (fase 4): i modelli che escono dal codice (``traduci_fase4.escluse``). Le
    parti si dividono come se ci fossero e gli altri modelli tengono il loro numero: il
    codice cambia solo dove si toglie. Il testo di un modello tolto è vuoto.

    ``importa_da``: da dove i moduli importano ``jinja`` (vedi ``MOTORE``).
    """
    testi = {nome: testo for testo, nome in jinja.funzioni.items()}
    testi.update(dict.fromkeys(tolti & testi.keys(), ""))
    funzioni = []
    for numero, blocco in enumerate(jinja.codice, 1):
        nome = f"m{numero:04d}"
        codice, separatore, _ = blocco.partition(f"\n\n\n{nome}.sorgente = ")
        if not separatore or not codice.startswith(f"def {nome}("):
            raise NonTraducibile(f"modello {nome} non riconosciuto")
        if "\x00" in testi[nome]:
            raise NonTraducibile(f"modello {nome} con \\x00")
        funzioni.append(codice)
    parti = [
        [f for f in parte if re.match(r"def (m\d{4})\(", f).group(1) not in tolti]
        for parte in _in_parti(funzioni)
    ]
    moduli = {}
    for numero, parte in enumerate(parti, 1):
        titolo = f"Modelli Jinja del package, tradotti in Python (parte {numero} di {len(parti)})."
        moduli[f"modelli_{numero:02d}.py"] = (
            INTESTAZIONE.format(titolo=titolo)
            + f"\nfrom {importa_da} import jinja as J\n\n\n"
            + "\n\n\n".join(parte)
            + "\n"
        )
    compressi = base64.b64encode(
        zlib.compress(
            "\x00".join(testi[f"m{n:04d}"] for n in range(1, len(testi) + 1)).encode(
                "utf-8"
            ),
            9,
        )
    ).decode("ascii")
    righe = "".join(
        f'    "{compressi[i : i + 96]}"\n' for i in range(0, len(compressi), 96)
    )
    # con modelli tolti il loro testo è vuoto e non c'è la loro funzione
    assegna = (
        "        spazio[f'm{numero:04d}'].sorgente = testo\n"
        if not tolti
        else "        if testo:\n"
        "            spazio[f'm{numero:04d}'].sorgente = testo\n"
    )
    moduli["modelli.py"] = (
        INTESTAZIONE.format(titolo="Modelli Jinja del package, tradotti in Python.")
        + "\nimport base64\nimport zlib\n\n"
        + "".join(f"from .{m[:-3]} import *\n" for m in moduli)
        + "\n# Il testo di ogni modello, compresso: i testi da m0001 in poi, separati da \\x00"
        + (".\n" if not tolti else " (vuoto: modello tolto).\n")
        + _INIZIO_SORGENTI
        + righe
        + ")\n\n\n"
        + "def _sorgenti():\n"
        + "    testi = zlib.decompress(base64.b64decode(_SORGENTI)).decode('utf-8')\n"
        + "    spazio = globals()\n"
        + "    for numero, testo in enumerate(testi.split('\\x00'), 1):\n"
        + assegna
        + "\n\n"
        + "_sorgenti()\n"
        + "del _sorgenti, _SORGENTI\n"
    )
    return moduli


def _moduli_motore(
    g: Generatore,
    motore: str,
    tolti: frozenset[str] = frozenset(),
    *,
    importa_da: str = MOTORE,
) -> dict[str, str]:
    """``motore_NN.py`` con le condizioni e le sequenze e ``motore.py`` con ``crea``.

    Ogni modulo importa dagli altri i nomi che usa: una condizione usa solo condizioni
    scritte prima (le sue parti), una sequenza solo condizioni e sequenze scritte dopo (le
    sue sequenze annidate), quindi gli import non fanno mai un giro.

    ``tolti`` (fase 4): le condizioni e le sequenze che escono dal codice
    (``traduci_fase4.escluse``; ``motore`` è già senza le loro automazioni e i loro
    comandi). Le parti si dividono come se ci fossero e le altre tengono il loro numero.

    ``importa_da``: da dove i moduli importano i moduli del motore (vedi ``MOTORE``).
    """
    prima, separatore, crea = motore.partition("\n\n\ndef crea(c):\n")
    if not separatore:
        raise NonTraducibile("crea non trovata")
    # i valori interni (fase 4), se ci sono, restano in motore.py prima di crea
    _, con_interni, interni = prima.partition(_INIZIO_INTERNI)
    importa_motore = _importa_motore(g.comandi is not None, importa_da=importa_da)
    parti = [
        [b for b in parte if _nome_blocco(b) not in tolti]
        for parte in _in_parti(g.condizioni) + _in_parti(g.sequenze)
    ]
    dove = {}
    for numero, parte in enumerate(parti, 1):
        for blocco in parte:
            dove[_nome_blocco(blocco)] = numero

    def importa(codice: str, numero: int | None) -> str:
        usati: dict[int, set[str]] = {}
        for nome in set(re.findall(r"\b[ks]\d{4}\b", codice)):
            if nome in dove and dove[nome] != numero:
                usati.setdefault(dove[nome], set()).add(nome)
        righe = ""
        for altro, nomi in sorted(usati.items()):
            elenco = sorted(nomi)
            righe += (
                f"from .motore_{altro:02d} import (\n"
                + "".join(
                    "    " + ", ".join(elenco[i : i + 10]) + ",\n"
                    for i in range(0, len(elenco), 10)
                )
                + ")\n"
            )
        return righe

    moduli = {}
    for numero, parte in enumerate(parti, 1):
        codice = "\n\n\n".join(parte)
        titolo = f"Automazioni e script del package, tradotti in Python (parte {numero} di {len(parti)})."
        moduli[f"motore_{numero:02d}.py"] = (
            INTESTAZIONE.format(titolo=titolo)
            + importa_motore
            + importa(codice, numero)
            + "\n\n"
            + codice
            + "\n"
        )
    crea = "def crea(c):\n" + crea
    moduli["motore.py"] = (
        INTESTAZIONE.format(
            titolo="Automazioni e script del package, tradotti in Python."
        )
        + importa_motore
        + importa(crea, None)
        + "\n\n"
        + (_INIZIO_INTERNI + interni + "\n\n\n" if con_interni else "")
        + crea
    )
    return moduli


def _nome_blocco(blocco: str) -> str:
    """Il nome della condizione (``kNNNN``) o della sequenza (``sNNNN``) di un blocco."""
    return re.match(r"(?:async )?def ([ks]\d{4})\(", blocco).group(1)


def _entita_costanti(valore: Any) -> list[str]:
    """Gli entity_id scritti (non con un modello) in un ``entity_id`` validato."""
    if isinstance(valore, str):
        return [e.strip().lower() for e in valore.split(",") if e.strip()]
    if isinstance(valore, list):
        return [e for v in valore if isinstance(v, str) for e in _entita_costanti(v)]
    return []


def contenuto(testo: str) -> str:
    """Il testo di un modulo generato con i testi dei modelli scompattati: due
    ``modelli.py`` con gli stessi testi sono uguali anche se zlib li comprime in un altro
    modo (un'altra versione)."""
    inizio, separatore, resto = testo.partition(_INIZIO_SORGENTI)
    if not separatore:
        return testo
    blocco, _, fine = resto.partition("\n)\n")
    compressi = "".join(riga.strip().strip('"') for riga in blocco.splitlines())
    testi = zlib.decompress(base64.b64decode(compressi)).decode("utf-8")
    return inizio + repr(testi) + fine


async def traduci_configurazione(
    hass: HomeAssistant,
    automazioni: list[dict[str, Any]],
    script: Mapping[str, dict[str, Any]],
    nome_modelli: str = "modelli",
    rinomina: Any = None,
    comandi: Mapping[str, str] | None = None,
    *,
    timer_motore: bool = False,
    interni: Iterable[str] | None = None,
) -> tuple[str, str]:
    """Il testo dei moduli dei modelli e del motore per automazioni e script qualsiasi
    (il motore importa i modelli come ``from . import <nome_modelli> as M``)."""
    _, _, modelli, motore = await traduzione(
        hass,
        automazioni,
        script,
        nome_modelli,
        rinomina,
        comandi,
        timer_motore=timer_motore,
        interni=interni,
    )
    return modelli, motore


async def traduzione(
    hass: HomeAssistant,
    automazioni: list[dict[str, Any]],
    script: Mapping[str, dict[str, Any]],
    nome_modelli: str = "modelli",
    rinomina: Any = None,
    comandi: Mapping[str, str] | None = None,
    *,
    timer_motore: bool = False,
    interni: Iterable[str] | None = None,
) -> tuple[Traduttore, Generatore, str, str]:
    """Come ``traduci_configurazione``, con il traduttore dei modelli (``funzioni``:
    testo -> nome) e il generatore (``variabili``: i nomi delle variabili usate).

    ``rinomina`` (fase 4, facoltativa: ``rinomina.Rinomina``) è la mappa dei nomi: con
    lei i testi costanti e i nomi dei servizi escono già con le entità di domani;
    senza, il codice generato è quello di sempre.

    ``comandi`` (fase 4, facoltativo: i comandi di shell, nome -> riga di comando, come
    ``leggi_comandi``) mette script e comandi dentro il motore: le chiamate restano
    quelle di oggi (``script.*``, ``shell_command.*``: il motore le manda ai suoi script
    e comandi, ``Contesto.chiama_servizio``), i trigger sulle chiamate dei comandi si
    segnano per l'aggancio diretto, un nome costante che non è del package o un trigger
    che non si può agganciare fermano la traduzione, e il codice ha in più
    ``comandi(c)``. Senza, il codice generato è quello di sempre.

    ``timer_motore`` (fase 4, spento se non lo si chiede): i timer del package diventano
    i timer del motore (``motore/timer.py``). I servizi ``timer.*`` diventano
    ``motore_timer.*``, i trigger evento che sentono gli eventi dei timer diventano
    ``motore_timer`` e le letture dei modelli che possono riguardare un timer passano da
    ``c.timer``; i timer tengono il loro entity_id di oggi. Quello che i timer del motore
    non sanno fare (un trigger o una condizione sullo stato di un timer, una lettura
    di un timer in un modello seguito da Home Assistant...) ferma la traduzione.

    ``interni`` (fase 4, facoltativo) sono le chiavi dei valori interni (come
    ``memoria_interna.INTERNI``): con loro ``crea(c)`` dichiara i valori interni
    (``c.memoria_interna(INTERNI)``) e il motore li legge e li scrive nella memoria
    interna, con i nomi scritti e con quelli composti dai modelli; le chiamate con un
    valore interno scritto nel bersaglio devono essere di quelle che il motore sa fare
    (``Generatore._verifica_valori_interni``). Senza, il codice generato è quello di
    sempre. I tre parametri della fase 4 sono indipendenti e vanno anche insieme.
    """
    if comandi is not None and rinomina is not None:
        tolti = [
            n for n in rinomina.entita if n.startswith(("script.", "shell_command."))
        ]
        if tolti or any(
            n.startswith(("script.", "shell_command.")) for n in rinomina.servizi
        ):
            raise NonTraducibile(
                f"la mappa dei nomi cambia script o comandi del motore: {tolti}"
            )
    if (
        timer_motore
        and rinomina is not None
        and any(nome.startswith("timer.") for nome in rinomina.entita)
    ):
        raise ValueError("con timer_motore i timer restano timer: fuori dalla mappa")
    gettone = RINOMINA.set(rinomina)
    gettone_timer = TIMER_MOTORE.set(timer_motore)
    try:
        return await _traduzione(
            hass,
            automazioni,
            script,
            nome_modelli,
            comandi,
            None if interni is None else tuple(interni),
        )
    finally:
        TIMER_MOTORE.reset(gettone_timer)
        RINOMINA.reset(gettone)


async def _traduzione(
    hass: HomeAssistant,
    automazioni: list[dict[str, Any]],
    script: Mapping[str, dict[str, Any]],
    nome_modelli: str,
    comandi: Mapping[str, str] | None = None,
    interni: tuple[str, ...] | None = None,
) -> tuple[Traduttore, Generatore, str, str]:
    ambiente = TemplateEnvironment(hass)
    jinja = Traduttore(
        filtri_ha={n for n in ambiente.filters if not hasattr(J, f"f_{n}")},
        test_ha={n for n in ambiente.tests if not hasattr(J, f"t_{n}")},
        globali_ha=set(ambiente.globals),
    )
    g = Generatore(
        jinja,
        comandi=comandi,
        script=frozenset(script),
        valori_interni=frozenset(
            f"{dominio}.vmc_{NOME_MASTER}_{oggetto}"
            for dominio, _, oggetto in (k.partition(".") for k in interni or ())
        ),
    )
    voci_automazioni = []
    for posto, config in enumerate(automazioni):
        validata = await valida_automazione(hass, "automation", config)
        if validata is None or getattr(validata, "validation_status", "ok") != "ok":
            raise NonTraducibile(f"automazione non valida: {config.get('alias')}")
        voci_automazioni.append(_automazione(g, dict(validata), posto))
    voci_script = []
    for chiave, config in script.items():
        validato = await valida_script(hass, chiave, config)
        if validato is None or getattr(validato, "validation_status", "ok") != "ok":
            raise NonTraducibile(f"script non valido: {chiave}")
        voci_script.append(_script(g, chiave, validato))
    if comuni := (g.variabili | VARIABILI_FISSE) & (GLOBALI | jinja.globali_ha):
        raise NonTraducibile(
            f"variabili con il nome di una funzione globale: {sorted(comuni)}"
        )
    # prima dei modelli: i comandi aggiungono i modelli dei loro argomenti
    comandi_motore = g.comandi_motore() if comandi is not None else ""
    modelli = INTESTAZIONE.format(
        titolo="Modelli Jinja del package, tradotti in Python."
    )
    modelli += (
        f"\nfrom {MOTORE} import jinja as J\n\n\n" + "\n\n\n".join(jinja.codice) + "\n"
    )
    motore = INTESTAZIONE.format(
        titolo="Automazioni e script del package, tradotti in Python."
    )
    motore += (
        _importa_motore(comandi is not None, nome_modelli)
        + "\n\n"
        + "\n\n\n".join(g.condizioni)
        + "\n\n\n"
        + "\n\n\n".join(g.sequenze)
        + (
            ""
            if interni is None
            else "\n\n\n"
            + _INIZIO_INTERNI
            + "".join(f"    {chiave!r},\n" for chiave in interni)
            + ")"
        )
        + "\n\n\ndef crea(c):\n"
        + '    """Automazioni e script per la VMC del contesto ``c``."""\n'
        + ("" if interni is None else "    c.memoria_interna(INTERNI)\n")
        + "    automazioni = [\n"
        + "".join(f"        {voce},\n" for voce in voci_automazioni)
        + "    ]\n    script = [\n"
        + "".join(f"        {voce},\n" for voce in voci_script)
        + "    ]\n    return automazioni, script\n"
        + comandi_motore
    )
    return jinja, g, modelli, motore


def _automazione(g: Generatore, config: dict[str, Any], posto: int) -> str:
    # il nome come lo dà Home Assistant (_automation_name): l'alias, o «automation N»
    # con N il posto nella lista delle automazioni
    alias = config.get("alias") or f"automation {posto}"
    noti = {
        "id", "alias", "description", "mode", "max", "max_exceeded", "initial_state",
        "triggers", "conditions", "actions", "variables", "trigger_variables", "trace",
    }  # fmt: skip
    if altre := set(config) - noti:
        raise NonTraducibile(f"automazione {alias}: chiavi {sorted(altre)}")
    if config.get("trigger_variables"):
        raise NonTraducibile(f"automazione {alias}: trigger_variables")
    variabili = config["variables"].as_dict() if config.get("variables") else None
    if variabili:
        g.variabili.update(variabili)
    corpo = g.sequenza(config["actions"], f"automazione {alias}")
    condizioni = config.get("conditions")
    parti = [
        f"alias={g.valore(alias)}",
        f"id={g.valore(config.get('id'))}",
        f"descrizione={g.valore(config.get('description'))}",
        f"modo={config.get('mode', 'single')!r}",
        f"massimo={config.get('max')!r}",
        f"avviso_massimo={config.get('max_exceeded', 'WARNING')!r}",
        f"stato_iniziale={config.get('initial_state')!r}",
        "trigger=[" + ", ".join(g.trigger(t) for t in config["triggers"]) + "]",
        f"condizioni={g.condizioni_tupla(condizioni) if condizioni else None}",
        f"corpo={corpo}",
    ]
    if variabili:
        parti.append(f"variabili={g.valore(variabili)}")
    return "Automazione(" + ", ".join(parti) + ")"


def _script(g: Generatore, chiave: str, config: Any) -> str:
    config = dict(config)
    noti = {
        "alias", "sequence", "mode", "max", "max_exceeded", "icon", "description",
        "fields", "variables", "trace",
    }  # fmt: skip
    if altre := set(config) - noti:
        raise NonTraducibile(f"script {chiave}: chiavi {sorted(altre)}")
    variabili = config["variables"].as_dict() if config.get("variables") else None
    if variabili:
        g.variabili.update(variabili)
    g.variabili.update(config.get("fields", {}))
    corpo = g.sequenza(config["sequence"], f"script {chiave}")
    parti = [
        f"chiave={g.valore(chiave)}",
        f"alias={g.valore(config.get('alias'))}",
        f"descrizione={g.valore(config.get('description'))}",
        f"icona={g.valore(config.get('icon'))}",
        f"modo={config.get('mode', 'single')!r}",
        f"massimo={config.get('max')!r}",
        f"avviso_massimo={config.get('max_exceeded', 'WARNING')!r}",
        f"campi={g.valore(dict(config.get('fields', {})))}",
        f"corpo={corpo}",
    ]
    if variabili:
        parti.append(f"variabili={g.valore(variabili)}")
    return "Script(" + ", ".join(parti) + ")"
