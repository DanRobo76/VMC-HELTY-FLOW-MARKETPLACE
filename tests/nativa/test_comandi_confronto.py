"""Le impostazioni native (comandi.py) a confronto con gli aiutanti del package.

Nello stesso Home Assistant ci sono i 172 aiutanti del package (come li installa la b42
per la VMC master) che domani diventano entità native, e le 172 entità native di
``crea_comandi``. Ogni entità riceve la stessa sequenza di scritture del suo aiutante,
nello stesso istante: per i valori di confine, fuori dai limiti, opzioni che non ci
sono, testi vuoti o troppo lunghi, «5» e «5.0», valori ripetuti. Si confrontano, per
ogni scrittura: gli eventi ``state_changed`` e ``state_reported`` (istante, stato,
attributi, last_changed, last_reported, forma del contesto), l'errore e gli avvisi nel
registro. Home Assistant (l'aiutante) è l'oracolo.

Tre vie per le entità native:

- «motore»: ``ScritturaComandi.chiama`` con il servizio di oggi (le scritture del motore);
- «registrato»: gli stessi servizi registrati in un dominio di prova (con l'evento
  ``call_service``);
- «utente»: i servizi del dominio nativo (switch.turn_on, number.set_value...), come
  dalla scheda; qui gli errori sono quelli del dominio nativo (elencati in
  ``DIFFERENZE_UTENTE``).

Gli attributi che le entità native non hanno (``editable``, ``initial``, ``has_date``...)
sono tutti e soli quelli di ``ATTRIBUTI_SOLO_AIUTANTE``.
"""

from __future__ import annotations

import csv
import json
import logging
import re
from collections import Counter
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import probatio
import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.const import (
    EVENT_CALL_SERVICE,
    EVENT_STATE_CHANGED,
    EVENT_STATE_REPORTED,
)
from homeassistant.core import Context, Event, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import restore_state
from homeassistant.helpers.json import json_bytes
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockEntityPlatform, MockUser

from custom_components.vmc_master.nativa.comandi import (
    DOMINI_AIUTANTI,
    SERVIZI_MOTORE,
    ComandoVMC,
    ScritturaComandi,
    chiavi_comandi,
    crea_comandi,
)
from custom_components.vmc_master.nativa.entita import crea_entita
from custom_components.vmc_master.nativa.stato import StatoVMC
from custom_components.vmc_master.nativa.tabelle import DOMANI, IMPOSTAZIONI, TOLTE

from . import confronto as c
from .genera_tabelle import NOMI_NATIVI
from .servizi_di_prova import registra_servizi

T0 = datetime(2026, 11, 25, 9, 0, 0, tzinfo=UTC)
NOME = c.NOME
DOMINIO_PROVA = "vmc_prova_comandi"

ATTRIBUTI_SOLO_AIUTANTE: dict[tuple[str, str], set[str]] = {
    ("input_boolean", "switch"): {"editable"},
    ("input_boolean", "binary_sensor"): {"editable"},
    ("input_number", "number"): {"editable", "initial"},
    ("input_number", "sensor"): {"editable", "initial", "min", "max", "step", "mode"},
    ("input_select", "select"): {"editable"},
    ("input_select", "sensor"): {"editable"},
    ("input_text", "text"): {"editable"},
    ("input_text", "sensor"): {"editable", "min", "max", "pattern", "mode"},
    ("input_datetime", "time"): {
        "editable",
        "has_date",
        "has_time",
        "hour",
        "minute",
        "second",
        "timestamp",
    },
}
"""Gli attributi dell'aiutante che l'entità nativa non ha (nessun altro è diverso)."""


def _oggi(chiave: str) -> str:
    dominio, oggetto = chiave.split(".", 1)
    return f"{dominio}.vmc_{NOME}_{oggetto}"


def _domani(chiave: str) -> str:
    return f"{DOMANI[chiave]}.vmc_{NOME}_{chiave.split('.', 1)[1]}"


def _aiutanti() -> dict[str, dict[str, Any]]:
    """La configurazione degli aiutanti del package che domani sono entità native; nelle
    opzioni che elencano entity_id (le entità escluse dal Recorder) senza le voci tolte
    (b46: ``TOLTE``), come nelle impostazioni native."""
    pacchetto = c.package()
    voluti = {_oggi(chiave) for chiave in chiavi_comandi()}
    tolte = {_oggi(chiave) for chiave in TOLTE}

    def senza_tolte(conf: dict[str, Any]) -> dict[str, Any]:
        if isinstance(conf.get("options"), list):
            return {**conf, "options": [o for o in conf["options"] if o not in tolte]}
        return conf

    return {
        dominio: {
            oggetto: senza_tolte(conf)
            for oggetto, conf in (pacchetto.get(dominio) or {}).items()
            if f"{dominio}.{oggetto}" in voluti
        }
        for dominio in DOMINI_AIUTANTI
    }


# --- conteggi e identità -----------------------------------------------------------------------


def test_le_entita_della_colonna_domani() -> None:
    """172 entità: quelle della colonna «Domani» della fase 1, stesso oggetto, unique_id
    come i sensori (vmc_<nome>_<oggetto>)."""
    entita = crea_comandi(StatoVMC(None, NOME))  # type: ignore[arg-type]
    conteggi = {dominio: len(gruppo) for dominio, gruppo in entita.items()}
    assert conteggi == {
        "binary_sensor": 77,
        "number": 10,
        "select": 14,
        "sensor": 3,
        "switch": 37,
        "text": 1,
        "time": 30,
    }
    tutte = [voce for gruppo in entita.values() for voce in gruppo]
    assert len(tutte) == 172
    assert {voce.entity_id for voce in tutte} == {_domani(k) for k in chiavi_comandi()}
    for voce in tutte:
        assert voce.unique_id == f"vmc_{NOME}_{voce.chiave.split('.', 1)[1]}"
    tipi = {}
    for voce in tutte:
        coppia = (voce.dominio_di_oggi, voce.entity_id.split(".")[0])
        tipi[coppia] = tipi.get(coppia, 0) + 1
    assert tipi == {
        ("input_boolean", "binary_sensor"): 77,
        ("input_boolean", "switch"): 37,
        ("input_datetime", "time"): 30,
        ("input_number", "number"): 10,
        ("input_number", "sensor"): 1,
        ("input_select", "select"): 14,
        ("input_select", "sensor"): 1,
        ("input_text", "sensor"): 1,
        ("input_text", "text"): 1,
    }
    # l'altra VMC: stessi oggetti col suo nome
    altra = crea_comandi(StatoVMC(None, "sala"))  # type: ignore[arg-type]
    assert altra["switch"][0].entity_id.startswith("switch.vmc_sala_")


def test_servizi_del_motore_sono_quelli_del_package() -> None:
    """``SERVIZI_MOTORE`` sono esattamente i servizi degli aiutanti che il package chiama
    sulle 172 voci (inventario della fase 4: nessun increment, decrement, select_next)."""
    inventario = Path(__file__).parent / "motore" / "inventario_aiutanti.csv"
    chiamati: set[str] = set()
    with inventario.open(encoding="utf-8") as flusso:
        for riga in csv.DictReader(flusso, delimiter=";"):
            if riga["tipo_oggi"] not in DOMINI_AIUTANTI:
                continue
            if riga["domani"] in ("interna", "tolta"):
                continue
            for voce in filter(None, riga["servizi"].split("; ")):
                servizio = voce.rsplit("=", 1)[0]
                if servizio.split(".")[0] in DOMINI_AIUTANTI:
                    chiamati.add(servizio)
    assert chiamati == set(SERVIZI_MOTORE)


# --- il banco: aiutanti e entità native nello stesso Home Assistant ---------------------------


class _Banco:
    """Aiutanti, entità native, registro degli eventi e degli avvisi."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self.stato = StatoVMC(hass, NOME)
        self.entita = crea_comandi(self.stato)
        self.tutte: list[ComandoVMC] = [v for g in self.entita.values() for v in g]
        self.per_chiave = {voce.chiave: voce for voce in self.tutte}
        self.indietro = {voce.entity_id: _oggi(voce.chiave) for voce in self.tutte}
        self.lato = {**dict.fromkeys(self.indietro, "domani")}
        self.lato.update(dict.fromkeys(self.indietro.values(), "oggi"))
        self.scrittura = ScritturaComandi(hass, self.tutte)
        self.contesti: dict[str, int] = {}
        self.eventi: dict[str, list[tuple[Any, ...]]] = {"oggi": [], "domani": []}
        self.chiamate: list[dict[str, Any]] = []
        self.avvisi: list[str] = []
        nomi = "|".join(
            re.escape(n) for n in sorted(self.indietro, key=len, reverse=True)
        )
        self._sostituzioni = re.compile(
            rf"(?<![A-Za-z0-9_.])(?:{nomi})(?![A-Za-z0-9_])"
        )

    async def prepara(self, freezer: FrozenDateTimeFactory) -> None:
        hass = self.hass
        freezer.move_to(T0)
        await hass.config.async_set_time_zone("Europe/Rome")
        assert await async_setup_component(hass, "homeassistant", {})
        for dominio, voci in _aiutanti().items():
            assert await async_setup_component(hass, dominio, {dominio: voci})
        for dominio, gruppo in self.entita.items():
            assert await async_setup_component(hass, dominio, {})
            piattaforma = MockEntityPlatform(
                hass, domain=dominio, platform_name="vmc_master"
            )
            await piattaforma.async_add_entities(gruppo)
        await hass.async_block_till_done()
        self.utente = MockUser(is_owner=True).add_to_hass(hass)
        hass.bus.async_listen(EVENT_STATE_CHANGED, self._annota)
        hass.bus.async_listen(EVENT_STATE_REPORTED, self._annota, self._nostra)
        hass.bus.async_listen(EVENT_CALL_SERVICE, self._chiamata)
        gestore = logging.Handler(logging.WARNING)
        # gli avvisi di Home Assistant e dell'integrazione (non quelli di asyncio, che
        # vede i salti dell'orologio finto come compiti lenti)
        gestore.emit = self._avviso  # type: ignore[method-assign]
        logging.getLogger().addHandler(gestore)
        self._gestore = gestore

    def _avviso(self, record: logging.LogRecord) -> None:
        if record.name.startswith(("homeassistant", "custom_components")):
            self.avvisi.append(self.nomi(record.getMessage()))

    def chiudi(self) -> None:
        logging.getLogger().removeHandler(self._gestore)

    def nomi(self, testo: str) -> str:
        """Il testo con i nomi di domani tornati quelli di oggi."""
        return self._sostituzioni.sub(lambda m: self.indietro[m.group(0)], testo)

    def contesto(
        self, numero: int, *, utente: bool = False, genitore: bool = False
    ) -> Context:
        contesto = Context(
            user_id=self.utente.id if utente else None,
            parent_id="genitore" if genitore else None,
        )
        self.contesti[contesto.id] = numero
        return contesto

    def _forma(self, contesto: Context) -> tuple[Any, ...]:
        return (
            self.contesti.get(contesto.id, "nuovo"),
            contesto.user_id is not None,
            contesto.parent_id,
        )

    @callback
    def _nostra(self, dati: Mapping[str, Any]) -> bool:
        return dati["entity_id"] in self.lato

    @callback
    def _annota(self, evento: Event) -> None:
        entita = evento.data["entity_id"]
        lato = self.lato.get(entita)
        if lato is None:
            return
        nuovo = evento.data["new_state"]
        oggi = self.indietro.get(entita, entita)
        dominio_oggi = oggi.split(".")[0]
        tolti = ATTRIBUTI_SOLO_AIUTANTE[(dominio_oggi, self._dominio_domani(oggi))]
        attributi = dict(nuovo.attributes)
        if lato == "oggi":
            assert tolti <= set(attributi), oggi
            attributi = {k: v for k, v in attributi.items() if k not in tolti}
            chiave = (
                f"{dominio_oggi}.{oggi.split('.', 1)[1].removeprefix(f'vmc_{NOME}_')}"
            )
            if chiave in NOMI_NATIVI and "friendly_name" in attributi:
                attributi["friendly_name"] = NOMI_NATIVI[chiave]  # nome nativo voluto
        self.eventi[lato].append(
            (
                oggi,
                (evento.time_fired - T0).total_seconds(),
                evento.event_type,
                nuovo.state,
                json.loads(json_bytes(attributi)),
                (nuovo.last_changed - T0).total_seconds(),
                (nuovo.last_reported - T0).total_seconds(),
                self._forma(evento.context),
            )
        )

    def _dominio_domani(self, oggi: str) -> str:
        dominio, oggetto = oggi.split(".", 1)
        return DOMANI[f"{dominio}.{oggetto.removeprefix(f'vmc_{NOME}_')}"]

    @callback
    def _chiamata(self, evento: Event) -> None:
        self.chiamate.append(dict(evento.data))

    async def una_chiamata(
        self, servizio: str, dati: dict[str, Any], contesto: Context, via: str = "ha"
    ) -> tuple[Any, list[str]]:
        """Una chiamata; restituisce (errore, avvisi nel registro)."""
        self.avvisi.clear()
        errore = None
        try:
            if via == "motore":
                await self.scrittura.chiama(servizio, dati, contesto)
            else:
                dominio, nome = servizio.split(".")
                await self.hass.services.async_call(
                    dominio, nome, dati, blocking=True, context=contesto
                )
        except (HomeAssistantError, probatio.Invalid) as err:
            errore = self._errore(err)
        await self.hass.async_block_till_done()
        return errore, list(self.avvisi)

    def _errore(self, err: Exception) -> tuple[Any, ...]:
        segnaposto = getattr(err, "translation_placeholders", None) or {}
        return (
            type(err).__name__,
            getattr(err, "translation_domain", None),
            getattr(err, "translation_key", None),
            {k: self.nomi(str(v)) for k, v in segnaposto.items()},
            self.nomi(str(err)),
        )

    def controlla_stato(self) -> None:
        """StatoVMC e la macchina degli stati dicono lo stesso valore (la vista)."""
        for voce in self.tutte:
            assert (
                self.stato.stato(voce.chiave)
                == self.hass.states.get(voce.entity_id).state
            )


# --- le sequenze di scritture ------------------------------------------------------------------


Passo = tuple[str, dict[str, Any], str | None, dict[str, Any], frozenset[str]]
MOTORE = frozenset({"motore", "registrato"})
UTENTE = frozenset({"utente"})
TUTTE = MOTORE | UTENTE


def _sequenza(chiave: str) -> list[Passo]:
    """Le scritture per una voce: (servizio di oggi, dati, servizio nativo, dati nativi,
    vie in cui si fa).

    Senza servizio nativo la scrittura è solo del motore (spie, sensori, set_options,
    set_datetime con data/datetime/timestamp); select_next e simili (che il package non
    usa e il motore non ha) solo dall'utente.
    """
    dominio = chiave.split(".")[0]
    domani = DOMANI[chiave]
    conf = IMPOSTAZIONI[chiave]
    passi: list[Passo] = []

    def passo(servizio: str, dati: dict[str, Any], nativo: str | None = None) -> None:
        passi.append((servizio, dati, nativo, dati, TUTTE if nativo else MOTORE))

    if dominio == "input_boolean":
        nativo = domani == "switch"
        for servizio in (
            "turn_on",
            "turn_on",
            "turn_off",
            "turn_on",
            "turn_off",
            "turn_off",
        ):
            passo(
                f"input_boolean.{servizio}",
                {},
                f"switch.{servizio}" if nativo else None,
            )
        if nativo:  # toggle: solo dalla scheda (il package non lo chiama)
            for _ in range(2):
                passi.append(("input_boolean.toggle", {}, "switch.toggle", {}, UTENTE))
    elif dominio == "input_number":
        minimo, massimo, passo_n = conf["min"], conf["max"], conf.get("step", 1)
        valori: list[Any] = [
            massimo,
            minimo,
            (minimo + massimo) / 2,
            minimo + passo_n / 3,  # non è un multiplo del passo: nessuno arrotonda
            str(int(minimo) + 1),  # «5» -> 5.0
            float(minimo) + 1,
            float(minimo) + 1,  # uguale: state_reported
            massimo + passo_n,  # fuori dai limiti
            minimo - 1,
            "abc",
        ]
        if minimo <= 0.1 + 0.2 <= massimo:
            valori.append(0.1 + 0.2)
        if minimo <= 0 <= massimo:
            valori.append(-0.0)
        nativo_n = "number.set_value" if domani == "number" else None
        for valore in valori:
            passo("input_number.set_value", {"value": valore}, nativo_n)
    elif dominio == "input_select":
        opzioni = [o.replace("{nome}", NOME) for o in conf["options"]]
        if domani == "sensor":
            return []  # nessuno la scrive: solo update_entity (sotto)
        for opzione in [*opzioni[1:], opzioni[0], opzioni[0], "Boh"]:
            passo(
                "input_select.select_option",
                {"option": opzione},
                "select.select_option",
            )
        for nome in ("select_next", "select_previous", "select_last", "select_first"):
            passi.append((f"input_select.{nome}", {}, f"select.{nome}", {}, UTENTE))
        dati_n = {"cycle": False}
        passi.append(
            ("input_select.select_next", dati_n, "select.select_next", dati_n, UTENTE)
        )
        # set_options: solo il motore
        passo(
            "input_select.set_options",
            {"options": [opzioni[0], "sensor.a", "sensor.b"]},
        )
        passo(
            "input_select.select_option", {"option": "sensor.b"}, "select.select_option"
        )
        passo(
            "input_select.set_options", {"options": ["sensor.c", "sensor.d"]}
        )  # sparisce
        passo(
            "input_select.set_options", {"options": "sensor.c"}
        )  # un testo: una lista
        passo("input_select.set_options", {"options": ["x", "x", "y"]})  # doppioni
        passo("input_select.set_options", {"options": []})
        passo("input_select.set_options", {"options": opzioni})
    elif dominio == "input_text":
        massimo = conf.get("max", 100)
        nativo_t = "text.set_value" if domani == "text" else None
        valori_t: list[Any] = [
            "abc",
            "",
            "x" * massimo,
            "x" * (massimo + 1),
            12,
            "abc",
            "",
        ]
        if "pattern" in conf:
            valori_t += ["con spazi", "VMC_2"]
        for valore in valori_t:
            passo("input_text.set_value", {"value": valore}, nativo_t)
    elif dominio == "input_datetime":
        for ora in ("07:30:00", "21:05", "21:05:00", "00:00"):
            dati_o = {"time": ora}
            passi.append(
                ("input_datetime.set_datetime", dati_o, "time.set_value", dati_o, TUTTE)
            )
        for dati in (
            {"datetime": "2026-11-25 06:15:30"},
            {"datetime": "2026-11-25T06:15:30+05:00"},
            {"timestamp": 3600 * 5},
            {
                "timestamp": 3600 * 5 + 0.75
            },  # frazioni di secondo: lo stato non le mostra
            {"date": "2026-12-01"},  # senza data: «Nothing to set»
            {"time": "07:30:00", "datetime": "2026-11-25 06:15:30"},
            {"time": "07:30:15.5"},
            {},
        ):
            passo("input_datetime.set_datetime", dati)
    return passi


DIFFERENZE_UTENTE = {
    # number.set_value fuori dai limiti: errore del dominio number
    ("input_number.set_value", "Invalid", None, None): (
        "ServiceValidationError",
        "number",
        "out_of_range",
    ),
    # select.select_option con un'opzione che non c'è: chiave di traduzione di select
    (
        "input_select.select_option",
        "ServiceValidationError",
        "input_select",
        "invalid_option",
    ): (
        "ServiceValidationError",
        "select",
        "not_valid_option",
    ),
    # text.set_value troppo lungo o fuori modello: errore invece dell'avviso nel registro
    ("input_text.set_value", None, None, None): ("ServiceValidationError", "text", "*"),
}
"""Gli errori della via «utente» diversi dall'aiutante: (servizio, errore di oggi) ->
errore del servizio nativo. Gli eventi restano uguali (nessuno dei due scrive)."""


VIA_MOTORE = (1567, 0, (836, 589))
"""Via «motore»/«registrato»: scritture, differenze, (state_changed, state_reported)."""
VIA_UTENTE = (906, 50, (494, 352))
ERRORI_MOTORE = {
    # «Nothing to set» (solo la data), ora con le frazioni / ora e datetime insieme, nulla
    ("input_datetime.set_datetime", "Invalid", None, None): 30,
    ("input_datetime.set_datetime", "MultipleInvalid", None, None): 60,
    ("input_datetime.set_datetime", "MultipleInvalid", None, "required_any_of"): 30,
    # fuori dai limiti (sopra e sotto), «abc»
    ("input_number.set_value", "Invalid", None, None): 22,
    ("input_number.set_value", "MultipleInvalid", None, "expected_type"): 11,
    # opzione che non c'è, opzioni doppie, nessuna opzione
    (
        "input_select.select_option",
        "ServiceValidationError",
        "input_select",
        "invalid_option",
    ): 14,
    (
        "input_select.set_options",
        "ServiceValidationError",
        "input_select",
        "duplicate_options",
    ): 14,
    ("input_select.set_options", "MultipleInvalid", None, "value_not_empty"): 14,
}
"""Gli errori dell'aiutante (uguali a quelli dell'entità nativa) nella via «motore»."""
ERRORI_UTENTE = {
    ("input_number.set_value", "Invalid", None, None): 20,
    ("input_number.set_value", "MultipleInvalid", None, "expected_type"): 10,
    (
        "input_select.select_option",
        "ServiceValidationError",
        "input_select",
        "invalid_option",
    ): 28,
}
AVVISI_MOTORE = {
    ("input_select.set_options", "Current option"): 28,  # l'opzione scelta sparisce
    ("input_text.set_value", "Invalid value"): 3,  # troppo lungo (2), fuori modello (1)
}
AVVISI_UTENTE = {("input_text.set_value", "Invalid value"): 2}


async def _corsa(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, via: str
) -> tuple[_Banco, dict[str, int]]:
    """Tutte le sequenze, aiutante e entità nativa; restituisce il banco e i conteggi."""
    banco = _Banco(hass)
    await banco.prepara(freezer)
    servizi = {}
    if via == "registrato":
        servizi = registra_servizi(banco.scrittura, DOMINIO_PROVA)
    conteggi: dict[str, Any] = {
        "scritture": 0,
        "errori": Counter(),
        "avvisi": Counter(),
        "diverse_utente": 0,
    }
    numero = 0
    adesso = T0
    try:
        for chiave in chiavi_comandi():
            oggi, domani = _oggi(chiave), _domani(chiave)
            passi = _sequenza(chiave)
            aggiorna = "homeassistant.update_entity"
            passi.append((aggiorna, {}, aggiorna, {}, TUTTE))
            for servizio, dati, nativo, dati_nativi, vie in passi:
                if via not in vie:
                    continue
                numero += 1
                adesso += timedelta(seconds=1)
                freezer.move_to(adesso)
                utente = via == "utente"
                contesto = banco.contesto(numero, utente=utente, genitore=not utente)
                errore_oggi, avvisi_oggi = await banco.una_chiamata(
                    servizio, {"entity_id": oggi, **dati}, contesto
                )
                contesto = banco.contesto(numero, utente=utente, genitore=not utente)
                bersaglio = {"entity_id": domani, **dati_nativi}
                if servizio.startswith("homeassistant."):
                    errore, avvisi = await banco.una_chiamata(
                        servizio, bersaglio, contesto
                    )
                elif via == "motore":
                    errore, avvisi = await banco.una_chiamata(
                        servizio, bersaglio, contesto, via="motore"
                    )
                elif via == "registrato":
                    errore, avvisi = await banco.una_chiamata(
                        servizi[servizio], bersaglio, contesto
                    )
                else:
                    assert nativo is not None
                    errore, avvisi = await banco.una_chiamata(
                        nativo, bersaglio, contesto
                    )
                conteggi["scritture"] += 1
                if errore_oggi is not None:
                    conteggi["errori"][(servizio, *errore_oggi[:3])] += 1
                for avviso in avvisi_oggi:
                    conteggi["avvisi"][(servizio, avviso.split(":")[0])] += 1
                if via == "utente" and (errore_oggi, avvisi_oggi) != (errore, avvisi):
                    _differenza_utente(
                        servizio, errore_oggi, avvisi_oggi, errore, avvisi
                    )
                    conteggi["diverse_utente"] += 1
                else:
                    assert (errore, avvisi) == (errore_oggi, avvisi_oggi), (
                        servizio,
                        dati,
                    )
            banco.controlla_stato()
    finally:
        banco.chiudi()
    return banco, conteggi


def _differenza_utente(
    servizio: str,
    errore_oggi: Any,
    avvisi_oggi: list[str],
    errore: Any,
    avvisi: list[str],
) -> None:
    """Una differenza della via «utente» deve essere una di ``DIFFERENZE_UTENTE``."""
    chiave = (servizio, *(errore_oggi[:3] if errore_oggi else (None, None, None)))
    if errore_oggi is not None and errore_oggi[0] == "Invalid":
        chiave = (servizio, "Invalid", None, None)
    atteso = DIFFERENZE_UTENTE[chiave]
    assert errore is not None
    assert errore[:2] == atteso[:2], (servizio, errore_oggi, errore)
    assert atteso[2] == "*" or errore[2] == atteso[2], (servizio, errore_oggi, errore)
    assert avvisi == []
    if servizio == "input_text.set_value":
        assert errore_oggi is None
        assert len(avvisi_oggi) == 1
        assert avvisi_oggi[0].startswith("Invalid value: ")


def _per_entita(eventi: list[tuple[Any, ...]]) -> dict[str, list[tuple[Any, ...]]]:
    uscita: dict[str, list[tuple[Any, ...]]] = {}
    for voce in eventi:
        uscita.setdefault(voce[0], []).append(voce[1:])
    return uscita


@pytest.mark.parametrize("via", ["motore", "registrato", "utente"])
async def test_ogni_comando_come_il_suo_aiutante(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, via: str
) -> None:
    """Per ognuna delle 172 voci, stessa sequenza all'aiutante e all'entità nativa: stessi
    eventi (istanti, stato, attributi, last_changed/last_reported, contesto), stessi
    errori e avvisi (via «utente»: solo le differenze di ``DIFFERENZE_UTENTE``)."""
    banco, conteggi = await _corsa(hass, freezer, via)
    oggi = _per_entita(banco.eventi["oggi"])
    domani = _per_entita(banco.eventi["domani"])
    assert set(oggi) == set(domani) == {_oggi(k) for k in chiavi_comandi()}
    for entita, attesi in oggi.items():
        assert domani[entita] == attesi, entita
    # la prova tocca davvero quello che deve
    tipi = [voce[2] for voce in banco.eventi["oggi"]]
    contesti = {voce[7] for voce in banco.eventi["oggi"]}
    scritture = sum(
        len([passo for passo in _sequenza(k) if via in passo[4]]) + 1
        for k in chiavi_comandi()
    )
    assert conteggi["scritture"] == scritture
    errori, avvisi = dict(conteggi["errori"]), dict(conteggi["avvisi"])
    eventi = (tipi.count(EVENT_STATE_CHANGED), tipi.count(EVENT_STATE_REPORTED))
    if via == "utente":
        assert (scritture, conteggi["diverse_utente"], eventi) == VIA_UTENTE
        assert errori == ERRORI_UTENTE
        assert avvisi == AVVISI_UTENTE
        assert all(forma[1] for forma in contesti if forma[0] != "nuovo")
    else:
        assert (scritture, conteggi["diverse_utente"], eventi) == VIA_MOTORE
        assert errori == ERRORI_MOTORE
        assert avvisi == AVVISI_MOTORE
        assert all(forma[2] == "genitore" for forma in contesti if forma[0] != "nuovo")
    if via == "registrato":
        nostre = [d for d in banco.chiamate if d["domain"] == DOMINIO_PROVA]
        loro = [d for d in banco.chiamate if d["domain"] in DOMINI_AIUTANTI]
        assert len(nostre) == len(loro)
        for nostra, sua in zip(nostre, loro, strict=True):
            assert nostra["service"] == f"{sua['domain']}_{sua['service']}"
            assert banco.nomi(
                json.dumps(nostra["service_data"], default=str)
            ) == json.dumps(sua["service_data"], default=str)


# --- più entità in una chiamata ------------------------------------------------------------------


async def test_piu_entita_in_una_chiamata(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Una chiamata del motore con molte entità (il package spegne decine di spie in una
    volta, anche interruttori e spie insieme, e cambia 5 orari insieme): stessi cambi,
    stesso istante, stesso contesto; ogni entità scritta nel suo compito come in Home
    Assistant, nello stesso ordine (quello dell'intersezione fra l'insieme dei bersagli e
    le entità del dominio, aggiunte nell'ordine del package: con gli stessi nomi di oggi,
    lo stesso insieme). Un'entità che non c'è: lo stesso avviso, e le altre sono
    scritte."""
    banco = _Banco(hass)
    await banco.prepara(freezer)
    try:
        booleani = [k for k in chiavi_comandi() if k.startswith("input_boolean.")]
        orari = [k for k in chiavi_comandi() if k.startswith("input_datetime.")][:5]
        casi = [
            ("input_boolean.turn_on", booleani, {}),
            ("input_boolean.turn_off", booleani[::3], {}),
            ("input_boolean.turn_off", booleani, {}),
            ("input_datetime.set_datetime", orari, {"time": "06:45"}),
        ]
        for numero, (servizio, chiavi, dati) in enumerate(casi, 1):
            freezer.move_to(T0 + timedelta(seconds=numero))
            for lato, nomi in (("oggi", _oggi), ("domani", _domani)):
                bersagli = [nomi(k) for k in chiavi]
                if numero == 3:
                    bersagli.append(f"{servizio.split('.')[0]}.vmc_{NOME}_non_esiste")
                contesto = banco.contesto(numero, genitore=True)
                via = "ha" if lato == "oggi" else "motore"
                errore, avvisi = await banco.una_chiamata(
                    servizio, {"entity_id": bersagli, **dati}, contesto, via=via
                )
                assert errore is None
                if numero == 3:
                    assert len(avvisi) == 1
                    assert "non_esiste" in avvisi[0]
        oggi, domani = banco.eventi["oggi"], banco.eventi["domani"]
        assert len(oggi) == 114 + 38 + 114 + 5
        assert oggi == domani
        assert {voce[7] for voce in oggi} == {
            (1, False, "genitore"),
            (2, False, "genitore"),
        } | {
            (3, False, "genitore"),
            (4, False, "genitore"),
        }
    finally:
        banco.chiudi()


# --- dopo un riavvio ---------------------------------------------------------------------------


def _conservati(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Gli stati che Home Assistant salverebbe alla chiusura, passati per il JSON."""
    memoria = restore_state.async_get(hass)
    return json.loads(
        json_bytes([s.as_dict() for s in memoria.async_get_stored_states()])
    )


@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_ripristino_dopo_il_riavvio(freezer: FrozenDateTimeFactory) -> None:
    """Prima del riavvio: valori diversi in ogni voce (stessa scrittura all'aiutante e
    all'entità nativa). Dopo: ognuna riparte come il suo aiutante («conserva il valore»,
    «riparte da off / 0 / vuoto») e StatoVMC ha lo stesso valore. Anche stati salvati
    strani: numero fuori dai limiti o senza i dati del numero, opzione sparita, ora o
    acceso/spento illeggibili."""
    from pytest_homeassistant_custom_component.common import async_test_home_assistant

    async with async_test_home_assistant() as hass:
        banco = _Banco(hass)
        await banco.prepara(freezer)
        try:
            for numero, chiave in enumerate(chiavi_comandi(), 1):
                servizio, dati = _valore_diverso(chiave)
                if servizio is None:
                    continue
                for lato, nome in (("ha", _oggi(chiave)), ("motore", _domani(chiave))):
                    contesto = banco.contesto(numero)
                    errore, _ = await banco.una_chiamata(
                        servizio, {"entity_id": nome, **dati}, contesto, via=lato
                    )
                    assert errore is None
            prima = {k: hass.states.get(_oggi(k)).state for k in chiavi_comandi()}
            conservati = _conservati(hass)
        finally:
            banco.chiudi()
        await hass.async_stop(force=True)

    assert len(conservati) == 2 * 172
    strani = _stati_strani(conservati)
    for variante, salvati in (("normali", conservati), ("strani", strani)):
        async with async_test_home_assistant() as hass:
            memoria = restore_state.async_get(hass)
            for voce in salvati:
                salvato = restore_state.StoredState.from_dict(voce)
                memoria.last_states_by_entity_id[salvato.state.entity_id] = salvato
            banco = _Banco(hass)
            await banco.prepara(freezer)
            banco.chiudi()
            dopo = {}
            for chiave in chiavi_comandi():
                oggi = hass.states.get(_oggi(chiave))
                domani = hass.states.get(_domani(chiave))
                assert domani.state == oggi.state, (variante, chiave)
                assert banco.stato.stato(chiave) == oggi.state
                dopo[chiave] = oggi.state
            if variante == "normali":
                _controlla_riavvio(prima, dopo)
            await hass.async_stop(force=True)


def _valore_diverso(chiave: str) -> tuple[str | None, dict[str, Any]]:
    """Una scrittura che porta la voce lontano dal valore di partenza."""
    dominio = chiave.split(".")[0]
    conf = IMPOSTAZIONI[chiave]
    if dominio == "input_boolean":
        return "input_boolean.turn_on", {}
    if dominio == "input_number":
        return "input_number.set_value", {"value": conf["max"]}
    if dominio == "input_select":
        if DOMANI[chiave] == "sensor":
            return None, {}
        if len(conf["options"]) == 1:
            return "input_select.set_options", {
                "options": [conf["options"][0], "sensor.x"]
            }
        return "input_select.select_option", {"option": conf["options"][-1]}
    if dominio == "input_text":
        return "input_text.set_value", {"value": "abc"}
    return "input_datetime.set_datetime", {"time": "06:15:30"}


def _controlla_riavvio(prima: dict[str, str], dopo: dict[str, str]) -> None:
    """Dopo il riavvio vale la colonna «Dopo un riavvio» della fase 1."""
    import csv

    from .motore.rinomina import FASE_1

    regole = {}
    with FASE_1.open(encoding="utf-8-sig", newline="") as flusso:
        for riga in csv.DictReader(flusso, delimiter=";"):
            regole[riga["Entità oggi"]] = riga["Dopo un riavvio"]
    conteggi: dict[str, int] = {}
    for chiave in chiavi_comandi():
        regola = regole[_oggi(chiave)]
        conteggi[regola] = conteggi.get(regola, 0) + 1
        if regola == "conserva il valore":
            atteso = prima[chiave]
            if chiave.startswith("input_select."):
                opzioni = [
                    o.replace("{nome}", NOME) for o in IMPOSTAZIONI[chiave]["options"]
                ]
                if atteso not in opzioni:
                    atteso = opzioni[0]  # opzione aggiunta da set_options: sparisce
            assert dopo[chiave] == atteso, chiave
        else:
            assert dopo[chiave] == {"riparte da off": "off", "riparte da 0": "0.0"}.get(
                regola, ""
            ), chiave
    assert conteggi == {
        "conserva il valore": 150,
        "riparte da off": 19,
        "riparte vuoto": 2,
        "riparte da 0": 1,
    }


def _stati_strani(conservati: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Gli stessi stati salvati, con valori che i servizi non scrivono mai."""
    uscita = []
    for voce in json.loads(json.dumps(conservati)):
        stato = voce["state"]
        dominio = stato["entity_id"].split(".")[0]
        if dominio in ("input_boolean", "switch", "binary_sensor"):
            stato["state"] = "unavailable"
        elif dominio in ("input_number", "number"):
            if "offset" in stato["entity_id"]:
                voce["extra_data"]["native_value"] = 10.0**22  # fuori dai limiti
            else:
                voce["extra_data"] = None  # senza i dati del numero: dal testo
                stato["state"] = "3.5"
        elif dominio in ("input_select", "select"):
            stato["state"] = "Non c'è più"
        elif dominio in ("input_datetime", "time"):
            stato["state"] = "25:61"
        uscita.append(voce)
    return uscita


# --- tempi: lo stato prima dei sensori che lo leggono ------------------------------------------


async def test_l_impostazione_cambia_prima_dei_sensori(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    """Come un aiutante cambia prima del template che lo legge, l'entità nativa scrive il
    suo stato prima del sensore nativo che la legge (StatoVMC: ascolto con ``prima``),
    anche se il sensore è stato aggiunto per primo.

    Oggi: input_select + template «Set Velocità 1° Fascia Calendario» del package.
    Domani: select + sensore nativo di entita.py (qui «sensor.nativa_...»). Stessi cambi,
    nello stesso ordine e allo stesso istante, con lo stesso contesto: il template prende
    quello della scrittura dell'aiutante, il sensore nativo quello della scrittura
    dell'impostazione (StatoVMC.contesto_cambi; nella fase 2 ne prendeva uno nuovo)."""
    freezer.move_to(T0)
    assert await async_setup_component(hass, "homeassistant", {})
    chiave, sensore = (
        "input_select.speed_1_fascia_calendario",
        "sensor.speed_1_fascia_calendario",
    )
    aiutante = _aiutanti()["input_select"]
    oggetto = _oggi(chiave).split(".", 1)[1]
    assert await async_setup_component(
        hass, "input_select", {"input_select": {oggetto: aiutante[oggetto]}}
    )
    modello = [
        {"sensor": [s]}
        for b in c.package()["template"]
        if "triggers" not in b
        for s in b.get("sensor") or []
        if s["default_entity_id"] == _oggi(sensore)
    ]
    assert await async_setup_component(hass, "template", {"template": modello})
    stato = StatoVMC(hass, NOME)
    sensori, _ = crea_entita(stato)
    nativo = next(s for s in sensori if s.chiave == sensore)
    nativo.entity_id = "sensor.nativa_speed_1_fascia_calendario"
    piattaforma = MockEntityPlatform(hass, domain="sensor", platform_name="vmc_master")
    await piattaforma.async_add_entities([nativo])  # il sensore prima dell'impostazione
    scelta = next(e for e in crea_comandi(stato)["select"] if e.chiave == chiave)
    assert await async_setup_component(hass, "select", {})
    piattaforma = MockEntityPlatform(hass, domain="select", platform_name="vmc_master")
    await piattaforma.async_add_entities([scelta])
    await hass.async_block_till_done()
    visti: list[tuple[str, str, str]] = []
    contesti: dict[str, str] = {}

    @callback
    def annota(evento: Event) -> None:
        nuovo = evento.data["new_state"]
        lato = (
            "domani"
            if nuovo.entity_id.split(".")[0] == "select" or "nativa" in nuovo.entity_id
            else "oggi"
        )
        tipo = "sensore" if nuovo.entity_id.startswith("sensor.") else "scelta"
        visti.append(
            (lato, tipo, nuovo.state, contesti.get(evento.context.id, "nuovo"))
        )

    hass.bus.async_listen(EVENT_STATE_CHANGED, annota)
    for opzione in ("Notturna", "Velocità 3"):
        for lato, servizio, entita in (
            ("oggi", "input_select.select_option", _oggi(chiave)),
            ("domani", "select.select_option", scelta.entity_id),
        ):
            contesto = Context()
            contesti[contesto.id] = f"{lato} {opzione}"
            dominio, nome = servizio.split(".")
            await hass.services.async_call(
                dominio,
                nome,
                {"entity_id": entita, "option": opzione},
                blocking=True,
                context=contesto,
            )
            await hass.async_block_till_done()
    oggi = [voce[1:3] for voce in visti if voce[0] == "oggi"]
    domani = [voce[1:3] for voce in visti if voce[0] == "domani"]
    assert (
        oggi
        == domani
        == [
            ("scelta", "Notturna"),
            ("sensore", "Notturna"),
            ("scelta", "Velocità 3"),
            ("sensore", "Velocità 3"),
        ]
    )
    # i contesti: la scelta ha quello della chiamata in tutti e due, e così il template e
    # il sensore nativo
    assert [v[3] for v in visti if v[0] == "oggi"] == [
        "oggi Notturna",
        "oggi Notturna",
        "oggi Velocità 3",
        "oggi Velocità 3",
    ]
    assert [v[3] for v in visti if v[0] == "domani"] == [
        "domani Notturna",
        "domani Notturna",
        "domani Velocità 3",
        "domani Velocità 3",
    ]
